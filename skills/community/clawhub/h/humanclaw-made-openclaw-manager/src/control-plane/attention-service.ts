import {
  AttentionKind,
  AttentionUnit,
  DriftViewItem,
  FocusDigest,
  RiskViewItem,
  SessionMapEntry,
  SessionRecord,
  SessionScores,
  defaultSessionScores,
  nowIso,
  uid,
} from '../types';
import { FsStore } from '../storage/fs-store';
import { writeAttentionQueue } from '../storage/indexes';

const hoursSince = (iso: string) => (Date.now() - new Date(iso).getTime()) / 36e5;

const clamp = (value: number, min = 0, max = 100) => Math.max(min, Math.min(max, value));

const priorityFromScore = (score: number): AttentionUnit['priority'] => {
  if (score >= 75) {
    return 'high';
  }
  if (score >= 40) {
    return 'normal';
  }
  return 'low';
};

const recommendedAction = (kind: AttentionKind) => {
  switch (kind) {
    case 'blocked':
      return 'Unblock the session, capture the blocker, or explicitly escalate it for local follow-up.';
    case 'waiting_human':
      return 'Provide the pending human decision and resume the run.';
    case 'stale':
      return 'Refresh the summary, checkpoint, or explicitly close the thread.';
    case 'desynced':
      return 'Repair the session/run linkage and restore a checkpoint.';
    case 'summary_drift':
      return 'Refresh the checkpoint summary before continuing.';
    case 'high_value':
      return 'Keep this session in focus and protect its progress.';
  }
};

const deriveScores = (session: SessionRecord): SessionScores => {
  const staleHours = hoursSince(session.updated_at);
  const urgency = clamp(
    (session.priority === 'high' ? 55 : session.priority === 'normal' ? 32 : 15) +
      (session.pending_human_decisions.length ? 20 : 0) +
      (session.blockers.length ? 18 : 0) +
      (staleHours >= 24 ? Math.min(20, staleHours / 2) : 0)
  );
  const value = clamp((session.priority === 'high' ? 82 : session.priority === 'normal' ? 56 : 34) + (!session.archived_at ? 8 : -12));
  const blockage = clamp(
    session.blockers.length * 32 +
      session.pending_human_decisions.length * 24 +
      (session.current_state === 'blocked' ? 24 : 0) +
      (session.current_state === 'waiting_human' ? 20 : 0)
  );
  const staleness = clamp(staleHours * 2.5);
  const uncertainty = clamp(
    (session.derived_summary.trim().length < 80 ? 28 : 0) +
      (!session.active_run_id && !session.archived_at ? 26 : 0) +
      (session.tags.length === 0 ? 12 : 0) +
      (session.source_channels.length > 1 ? 10 : 0)
  );
  const attentionPriority = clamp(
    urgency * 0.3 + value * 0.15 + blockage * 0.25 + staleness * 0.15 + uncertainty * 0.15
  );
  return {
    urgency_score: Math.round(urgency),
    value_score: Math.round(value),
    blockage_score: Math.round(blockage),
    staleness_score: Math.round(staleness),
    uncertainty_score: Math.round(uncertainty),
    attention_priority: Math.round(attentionPriority),
  };
};

export class AttentionService {
  constructor(private readonly store: FsStore) {}

  private async readIndexedSessions() {
    return this.store.readJson<SessionRecord[]>(`${this.store.indexesDir}\\sessions.json`, []);
  }

  private shouldFlagSummaryDrift(session: SessionRecord) {
    const staleHours = hoursSince(session.updated_at);
    return !session.archived_at && staleHours >= 12 && session.derived_summary.trim().length < 120;
  }

  private shouldFlagDesync(session: SessionRecord) {
    return !session.archived_at && ((session.current_state !== 'archived' && !session.active_run_id) || (session.current_state === 'running' && !session.active_run_id));
  }

  deriveForSession(session: SessionRecord): AttentionUnit[] {
    const scores = deriveScores(session);
    const base = {
      session_id: session.session_id,
      created_at: nowIso(),
      updated_at: nowIso(),
      ...scores,
    };

    const items: AttentionUnit[] = [];

    if (session.current_state === 'blocked' || session.blockers.length) {
      items.push({
        attention_id: uid('attn'),
        kind: 'blocked',
        priority: priorityFromScore(scores.attention_priority + 18),
        summary: session.blockers[0] || 'Session is blocked.',
        recommended_action: recommendedAction('blocked'),
        ...base,
      });
    }

    if (session.current_state === 'waiting_human' || session.pending_human_decisions.length) {
      items.push({
        attention_id: uid('attn'),
        kind: 'waiting_human',
        priority: priorityFromScore(scores.attention_priority + 12),
        summary: session.pending_human_decisions[0] || 'Human decision is required.',
        recommended_action: recommendedAction('waiting_human'),
        ...base,
      });
    }

    if (!session.archived_at && hoursSince(session.updated_at) >= 24) {
      items.push({
        attention_id: uid('attn'),
        kind: 'stale',
        priority: priorityFromScore(scores.attention_priority),
        summary: 'Session is stale and needs review.',
        recommended_action: recommendedAction('stale'),
        ...base,
      });
    }

    if (this.shouldFlagDesync(session)) {
      items.push({
        attention_id: uid('attn'),
        kind: 'desynced',
        priority: priorityFromScore(scores.attention_priority + 8),
        summary: 'Session state and active run are out of sync.',
        recommended_action: recommendedAction('desynced'),
        ...base,
      });
    }

    if (this.shouldFlagSummaryDrift(session)) {
      items.push({
        attention_id: uid('attn'),
        kind: 'summary_drift',
        priority: priorityFromScore(scores.attention_priority),
        summary: 'Session summary is stale relative to current work.',
        recommended_action: recommendedAction('summary_drift'),
        ...base,
      });
    }

    if (!session.archived_at && session.priority === 'high') {
      items.push({
        attention_id: uid('attn'),
        kind: 'high_value',
        priority: priorityFromScore(scores.attention_priority),
        summary: 'High-priority session should stay in focus.',
        recommended_action: recommendedAction('high_value'),
        ...base,
      });
    }

    return items;
  }

  async refresh(allSessions: SessionRecord[]) {
    const nextSessions = allSessions.map((session) => ({
      ...session,
      scores: deriveScores(session),
    }));
    const items = nextSessions
      .flatMap((session) => this.deriveForSession(session))
      .sort((a, b) => b.attention_priority - a.attention_priority || b.updated_at.localeCompare(a.updated_at));

    await writeAttentionQueue(this.store, items);

    for (const session of nextSessions) {
      await this.store.writeJson(this.store.sessionFile(session.session_id), session);
      await this.store.writeJson(
        this.store.attentionFile(session.session_id),
        items.filter((item) => item.session_id === session.session_id)
      );
    }

    return items;
  }

  async list() {
    return this.store.readJson<AttentionUnit[]>(`${this.store.indexesDir}\\attention_queue.json`, []);
  }

  async listForSession(sessionId: string) {
    return this.store.readJson<AttentionUnit[]>(this.store.attentionFile(sessionId), []);
  }

  async sessionMap() {
    const sessions = await this.readIndexedSessions();
    return sessions
      .map((session): SessionMapEntry => ({
        session_id: session.session_id,
        title: session.title,
        current_state: session.current_state,
        priority: session.priority,
        source_channels: session.source_channels,
        blockers: session.blockers,
        pending_human_decisions: session.pending_human_decisions,
        updated_at: session.updated_at,
        recommended_action:
          session.pending_human_decisions[0] ||
          session.blockers[0] ||
          (session.archived_at ? 'Closed.' : 'Continue or checkpoint the session.'),
        ...(session.scores || defaultSessionScores()),
      }))
      .sort((a, b) => b.attention_priority - a.attention_priority || b.updated_at.localeCompare(a.updated_at));
  }

  async focus(limit = 5): Promise<FocusDigest> {
    const items = await this.list();
    return {
      generated_at: nowIso(),
      top_items: items.slice(0, limit),
      candidate_shadows: [],
      ignored_items: Math.max(0, items.length - limit),
    };
  }

  async riskView(): Promise<RiskViewItem[]> {
    const sessions = await this.readIndexedSessions();
    return sessions
      .flatMap((session) =>
        this.deriveForSession(session)
          .filter((item) => ['blocked', 'waiting_human', 'desynced'].includes(item.kind))
          .map((item) => ({
            session_id: session.session_id,
            title: session.title,
            risk_kind: item.kind,
            summary: item.summary,
            recommended_action: item.recommended_action,
            scores: {
              urgency_score: item.urgency_score,
              value_score: item.value_score,
              blockage_score: item.blockage_score,
              staleness_score: item.staleness_score,
              uncertainty_score: item.uncertainty_score,
              attention_priority: item.attention_priority,
            },
          }))
      )
      .sort((a, b) => b.scores.attention_priority - a.scores.attention_priority);
  }

  async driftView(): Promise<DriftViewItem[]> {
    const sessions = await this.readIndexedSessions();
    return sessions
      .filter((session) => !session.archived_at)
      .map((session) => ({
        session_id: session.session_id,
        title: session.title,
        stale: hoursSince(session.updated_at) >= 24,
        summary_drift: this.shouldFlagSummaryDrift(session),
        desynced: this.shouldFlagDesync(session),
        updated_at: session.updated_at,
      }))
      .filter((item) => item.stale || item.summary_drift || item.desynced)
      .sort((a, b) => b.updated_at.localeCompare(a.updated_at));
  }
}
