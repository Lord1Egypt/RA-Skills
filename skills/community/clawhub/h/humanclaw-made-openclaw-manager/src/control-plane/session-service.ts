import fs from 'node:fs/promises';
import {
  AdoptSessionInput,
  CheckpointInput,
  CloseSessionInput,
  SessionRecord,
  SessionState,
  defaultSessionScores,
  nowIso,
  uid,
} from '../types';
import { FsStore } from '../storage/fs-store';
import { writeSessionIndexes } from '../storage/indexes';
import { EventService } from './event-service';
import { RunService } from './run-service';
import { CheckpointService } from './checkpoint-service';
import { SpoolService } from './spool-service';
import { withNamedLock } from '../storage/locks';

const TERMINAL_RUN_STATES = new Set(['completed', 'failed', 'cancelled', 'superseded']);

const uniqueStrings = (items: string[]) => Array.from(new Set(items.map((item) => item.trim()).filter(Boolean)));

const defaultNextMachineActions = (state: SessionState) => {
  if (state === 'blocked') {
    return ['Resolve the leading blocker or escalate it.'];
  }
  if (state === 'waiting_human') {
    return ['Wait for a human decision, then continue the run.'];
  }
  if (state === 'archived') {
    return [];
  }
  return ['Continue the active run from the latest checkpoint.'];
};

const deriveStateFromCheckpoint = (
  session: SessionRecord,
  input: CheckpointInput,
  fallback: SessionState = session.current_state
): SessionState => {
  if (input.current_state) {
    return input.current_state;
  }
  const blockers = input.blockers ?? session.blockers;
  const pending = input.pending_human_decisions ?? session.pending_human_decisions;
  if (blockers.length) {
    return 'blocked';
  }
  if (pending.length) {
    return 'waiting_human';
  }
  if (fallback === 'archived') {
    return 'running';
  }
  return fallback === 'blocked' || fallback === 'waiting_human' ? 'running' : fallback;
};

export class SessionService {
  constructor(
    private readonly store: FsStore,
    private readonly runService: RunService,
    private readonly eventService: EventService,
    private readonly checkpointService: CheckpointService,
    private readonly spoolService: SpoolService
  ) {}

  private async scanSessions() {
    try {
      const entries = await fs.readdir(this.store.sessionsDir, { withFileTypes: true });
      const sessions = await Promise.all(
        entries
          .filter((entry) => entry.isDirectory())
          .map((entry) => this.store.readJson<SessionRecord | null>(this.store.sessionFile(entry.name), null))
      );
      return sessions
        .filter((session): session is SessionRecord => Boolean(session))
        .sort((a, b) => b.updated_at.localeCompare(a.updated_at));
    } catch {
      return [] as SessionRecord[];
    }
  }

  async listSessions(): Promise<SessionRecord[]> {
    const indexed = await this.store.readJson<SessionRecord[]>(`${this.store.indexesDir}\\sessions.json`, []);
    if (indexed.length) {
      return indexed.sort((a, b) => b.updated_at.localeCompare(a.updated_at));
    }
    const scanned = await this.scanSessions();
    await writeSessionIndexes(this.store, scanned);
    return scanned;
  }

  async getSession(sessionId: string) {
    return this.store.readJson<SessionRecord | null>(this.store.sessionFile(sessionId), null);
  }

  async listRuns(sessionId: string) {
    return this.runService.list(sessionId);
  }

  async getLatestCheckpoint(sessionId: string, preferredRunId?: string | null) {
    if (preferredRunId) {
      const checkpoint = await this.checkpointService.get(sessionId, preferredRunId);
      if (checkpoint) {
        return checkpoint;
      }
    }
    const runs = await this.runService.list(sessionId);
    for (const run of [...runs].reverse()) {
      const checkpoint = await this.checkpointService.get(sessionId, run.run_id);
      if (checkpoint) {
        return checkpoint;
      }
    }
    return null;
  }

  async adopt(input: AdoptSessionInput) {
    return withNamedLock('manager:sessions', async () => {
      const sessionId = uid('sess');
      const now = nowIso();
      const initialRun = await this.runService.create(sessionId, 'adopt', 'Initial adoption run', 'running');
      const session: SessionRecord = {
        session_id: sessionId,
        title: input.title.trim(),
        objective: input.objective.trim(),
        owner: input.owner ?? null,
        source_channels: uniqueStrings(input.source_channels ?? ['chat']),
        current_state: 'running',
        active_run_id: initialRun.run_id,
        priority: input.priority ?? 'normal',
        blockers: [],
        pending_human_decisions: [],
        derived_summary: input.initial_message?.trim() || 'Session adopted from an existing OpenClaw thread.',
        tags: uniqueStrings(input.tags ?? []),
        metadata: input.metadata ?? {},
        scores: defaultSessionScores(),
        created_at: now,
        updated_at: now,
        archived_at: null,
      };

      await this.store.ensureSessionLayout(sessionId, initialRun.run_id);
      await this.store.writeJson(this.store.sessionFile(sessionId), session);
      await this.eventService.append(sessionId, initialRun.run_id, 'run_started', {
        trigger: 'adopt',
      });
      await this.eventService.append(sessionId, initialRun.run_id, 'state_changed', {
        previous_state: null,
        next_state: 'running',
        reason: 'session adopted',
      });
      if (input.initial_message?.trim()) {
        await this.eventService.append(sessionId, initialRun.run_id, 'message_received', {
          source_type: 'chat',
          source_thread_key: 'local-chat',
          content: input.initial_message.trim(),
        });
        await this.spoolService.appendInbound(sessionId, initialRun.run_id, {
          request_id: uid('req'),
          external_trigger_id: uid('msg'),
          source_type: 'chat',
          source_thread_key: 'local-chat',
          message_type: 'user_message',
          content: input.initial_message.trim(),
          attachments: [],
          timestamp: now,
          metadata: {},
        });
      }
      await this.checkpointService.upsert(session, {
        next_machine_actions: ['Review the adopted thread and continue the work.'],
        next_human_actions: [],
        current_state: 'running',
      });

      await this.refreshIndexes();
      return session;
    });
  }

  async resume(sessionId: string, note = 'Resume existing session') {
    return withNamedLock(`manager:session:${sessionId}`, async () => {
      const session = await this.getSession(sessionId);
      if (!session) {
        throw new Error(`Session not found: ${sessionId}`);
      }

      const previousRun = session.active_run_id
        ? await this.runService.get(sessionId, session.active_run_id)
        : await this.runService.latest(sessionId);
      const previousRunId = previousRun?.run_id || null;
      const checkpoint = await this.getLatestCheckpoint(sessionId, previousRunId);
      const summary = await this.store.readText(this.store.summaryFile(sessionId), session.derived_summary);
      const spoolPreview = previousRunId ? (await this.spoolService.list(sessionId, previousRunId)).slice(-10) : [];

      if (previousRun && !TERMINAL_RUN_STATES.has(previousRun.status)) {
        await this.runService.updateStatus(sessionId, previousRun.run_id, 'superseded', 'Superseded by explicit resume.');
      }

      const run = await this.runService.create(sessionId, 'resume', note, 'running', {
        restored_from_run_id: previousRunId,
        summary,
        checkpoint,
        spool_preview: spoolPreview,
      });
      await this.spoolService.append(sessionId, run.run_id, 'resume_context', {
        restored_from_run_id: previousRunId,
        summary_preview: summary.slice(0, 800),
        checkpoint,
        spool_preview: spoolPreview,
      });

      const next: SessionRecord = {
        ...session,
        current_state: 'running',
        active_run_id: run.run_id,
        derived_summary: session.derived_summary,
        updated_at: nowIso(),
        archived_at: null,
        metadata: {
          ...session.metadata,
          last_resumed_from_run_id: previousRunId,
        },
      };
      await this.store.writeJson(this.store.sessionFile(sessionId), next);
      await this.eventService.append(sessionId, run.run_id, 'checkpoint_restored', {
        restored_from_run_id: previousRunId,
        checkpoint,
      });
      await this.eventService.append(sessionId, run.run_id, 'run_started', {
        trigger: 'resume',
        note,
      });
      await this.eventService.append(sessionId, run.run_id, 'state_changed', {
        previous_state: session.current_state,
        next_state: 'running',
        reason: 'resume requested',
      });
      await this.checkpointService.upsert(next, {
        blockers: checkpoint?.blockers ?? session.blockers,
        pending_human_decisions: checkpoint?.pending_human_decisions ?? session.pending_human_decisions,
        artifact_refs: checkpoint?.artifact_refs ?? [],
        next_machine_actions: checkpoint?.next_machine_actions?.length
          ? checkpoint.next_machine_actions
          : defaultNextMachineActions('running'),
        next_human_actions: checkpoint?.next_human_actions ?? [],
        summary: session.derived_summary,
        current_state: 'running',
      });

      await this.refreshIndexes();
      return next;
    });
  }

  async checkpoint(sessionId: string, input: CheckpointInput = {}) {
    return withNamedLock(`manager:session:${sessionId}`, async () => {
      const session = await this.getSession(sessionId);
      if (!session || !session.active_run_id) {
        throw new Error(`Session not found or inactive: ${sessionId}`);
      }

      const nextState = deriveStateFromCheckpoint(session, input);
      const nextSummary = input.summary?.trim() || session.derived_summary;
      const next: SessionRecord = {
        ...session,
        current_state: nextState,
        blockers: uniqueStrings(input.blockers ?? session.blockers),
        pending_human_decisions: uniqueStrings(input.pending_human_decisions ?? session.pending_human_decisions),
        derived_summary: nextSummary,
        updated_at: nowIso(),
      };
      await this.store.writeJson(this.store.sessionFile(sessionId), next);
      if (session.current_state !== nextState) {
        await this.eventService.append(sessionId, session.active_run_id, 'state_changed', {
          previous_state: session.current_state,
          next_state: nextState,
          reason: 'checkpoint update',
        });
      }
      await this.eventService.append(sessionId, session.active_run_id, 'summary_refreshed', {
        summary: nextSummary,
      });
      if (next.blockers.length) {
        await this.eventService.append(sessionId, session.active_run_id, 'blocker_detected', {
          blockers: next.blockers,
        });
      }
      if (next.pending_human_decisions.length) {
        await this.eventService.append(sessionId, session.active_run_id, 'human_decision_requested', {
          pending_human_decisions: next.pending_human_decisions,
        });
      }
      if ((input.artifact_refs ?? []).length) {
        await this.spoolService.append(sessionId, session.active_run_id, 'artifact_note', {
          artifact_refs: input.artifact_refs,
        });
      }
      const checkpoint = await this.checkpointService.upsert(next, {
        ...input,
        blockers: next.blockers,
        pending_human_decisions: next.pending_human_decisions,
        summary: nextSummary,
        current_state: nextState,
        next_machine_actions: input.next_machine_actions ?? defaultNextMachineActions(nextState),
      });

      await this.refreshIndexes();
      return { session: next, checkpoint };
    });
  }

  async close(sessionId: string, input: CloseSessionInput = {}) {
    return withNamedLock(`manager:session:${sessionId}`, async () => {
      const session = await this.getSession(sessionId);
      if (!session || !session.active_run_id) {
        throw new Error(`Session not found or inactive: ${sessionId}`);
      }

      const runId = session.active_run_id;
      const archivedAt = nowIso();
      const closeOutcome = input.outcome || 'completed';
      const summary = input.notes?.trim() || session.derived_summary;
      const checkpointSession: SessionRecord = {
        ...session,
        current_state: 'archived',
        active_run_id: runId,
        derived_summary: summary,
        updated_at: archivedAt,
        archived_at: archivedAt,
        metadata: {
          ...session.metadata,
          closure_type: input.closure_type || 'completed',
          close_outcome: closeOutcome,
          last_closed_run_id: runId,
        },
      };

      await this.eventService.append(sessionId, runId, 'summary_refreshed', {
        summary,
      });
      await this.eventService.append(sessionId, runId, 'state_changed', {
        previous_state: session.current_state,
        next_state: 'archived',
        reason: 'session closed',
      });
      await this.eventService.append(sessionId, runId, 'session_archived', {
        closure_type: input.closure_type || 'completed',
        outcome: closeOutcome,
        notes: input.notes || '',
      });
      await this.checkpointService.upsert(checkpointSession, {
        blockers: [],
        pending_human_decisions: [],
        next_machine_actions: [],
        next_human_actions: [],
        summary,
        current_state: 'archived',
      });

      const terminalStatus =
        closeOutcome === 'failed' || closeOutcome === 'cancelled'
          ? closeOutcome
          : closeOutcome === 'superseded'
            ? 'superseded'
            : 'completed';
      await this.runService.updateStatus(sessionId, runId, terminalStatus, input.notes || 'Session closed');

      const next: SessionRecord = {
        ...checkpointSession,
        active_run_id: null,
      };
      await this.store.writeJson(this.store.sessionFile(sessionId), next);
      await this.refreshIndexes();
      return next;
    });
  }

  async refreshIndexes() {
    const sessions = await this.scanSessions();
    await writeSessionIndexes(this.store, sessions);
    return sessions;
  }
}
