import fs from 'node:fs/promises';
import { RunRecord, RunStatus, nowIso, uid } from '../types';
import { FsStore } from '../storage/fs-store';

export class RunService {
  constructor(private readonly store: FsStore) {}

  async create(sessionId: string, trigger: string, note = '', status: RunStatus = 'accepted', resumeContext: RunRecord['resume_context'] = null) {
    const run: RunRecord = {
      run_id: uid('run'),
      session_id: sessionId,
      status,
      trigger,
      note,
      resume_context: resumeContext,
      started_at: nowIso(),
      updated_at: nowIso(),
      ended_at: null,
    };
    await this.store.ensureSessionLayout(sessionId, run.run_id);
    await this.store.writeJson(this.store.runFile(sessionId, run.run_id), run);
    await this.store.writeTextIfMissing(this.store.eventsFile(sessionId, run.run_id), '');
    await this.store.writeTextIfMissing(this.store.spoolFile(sessionId, run.run_id), '');
    await this.store.writeTextIfMissing(this.store.skillTracesFile(sessionId, run.run_id), '');
    return run;
  }

  async get(sessionId: string, runId: string) {
    return this.store.readJson<RunRecord | null>(this.store.runFile(sessionId, runId), null);
  }

  async list(sessionId: string) {
    try {
      const entries = await fs.readdir(this.store.runsDir(sessionId), { withFileTypes: true });
      const runs = await Promise.all(
        entries
          .filter((entry) => entry.isDirectory())
          .map((entry) => this.get(sessionId, entry.name))
      );
      return runs
        .filter((run): run is RunRecord => Boolean(run))
        .sort((a, b) => a.started_at.localeCompare(b.started_at));
    } catch {
      return [] as RunRecord[];
    }
  }

  async latest(sessionId: string) {
    const runs = await this.list(sessionId);
    return runs.at(-1) || null;
  }

  async updateStatus(sessionId: string, runId: string, status: RunStatus, note?: string) {
    const run = await this.get(sessionId, runId);
    if (!run) {
      throw new Error(`Run not found: ${runId}`);
    }

    const ended = ['completed', 'failed', 'cancelled', 'superseded'].includes(status) ? nowIso() : run.ended_at;
    const next: RunRecord = {
      ...run,
      status,
      note: note ?? run.note,
      updated_at: nowIso(),
      ended_at: ended,
    };
    await this.store.writeJson(this.store.runFile(sessionId, runId), next);
    return next;
  }
}
