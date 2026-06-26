import { CheckpointInput, CheckpointRecord, SessionRecord, nowIso } from '../types';
import { FsStore } from '../storage/fs-store';

const renderSummary = (session: SessionRecord, checkpoint: CheckpointRecord) => `# ${session.title}

## Objective
${session.objective}

## Current state
${session.current_state}

## Derived summary
${session.derived_summary || 'No summary yet.'}

## Blockers
${checkpoint.blockers.length ? checkpoint.blockers.map((item) => `- ${item}`).join('\n') : '- none'}

## Pending human decisions
${checkpoint.pending_human_decisions.length ? checkpoint.pending_human_decisions.map((item) => `- ${item}`).join('\n') : '- none'}

## Next machine actions
${checkpoint.next_machine_actions.length ? checkpoint.next_machine_actions.map((item) => `- ${item}`).join('\n') : '- none'}

## Next human actions
${checkpoint.next_human_actions.length ? checkpoint.next_human_actions.map((item) => `- ${item}`).join('\n') : '- none'}
`;

export class CheckpointService {
  constructor(private readonly store: FsStore) {}

  async get(sessionId: string, runId: string) {
    return this.store.readJson<CheckpointRecord | null>(this.store.checkpointFile(sessionId, runId), null);
  }

  async upsert(session: SessionRecord, checkpointInput: CheckpointInput = {}) {
    if (!session.active_run_id) {
      throw new Error('Session has no active run.');
    }

    const existing = await this.get(session.session_id, session.active_run_id);

    const checkpoint: CheckpointRecord = {
      session_id: session.session_id,
      active_run_id: session.active_run_id,
      current_state: checkpointInput.current_state ?? session.current_state,
      blockers: checkpointInput.blockers ?? existing?.blockers ?? session.blockers ?? [],
      pending_human_decisions:
        checkpointInput.pending_human_decisions ?? existing?.pending_human_decisions ?? session.pending_human_decisions ?? [],
      artifact_refs: checkpointInput.artifact_refs ?? existing?.artifact_refs ?? [],
      next_machine_actions: checkpointInput.next_machine_actions ?? existing?.next_machine_actions ?? [],
      next_human_actions: checkpointInput.next_human_actions ?? existing?.next_human_actions ?? [],
      summary_version: (existing?.summary_version || 0) + 1,
      updated_at: nowIso(),
    };

    await this.store.writeJson(this.store.checkpointFile(session.session_id, session.active_run_id), checkpoint);
    await this.store.writeText(this.store.summaryFile(session.session_id), renderSummary(session, checkpoint));
    return checkpoint;
  }
}
