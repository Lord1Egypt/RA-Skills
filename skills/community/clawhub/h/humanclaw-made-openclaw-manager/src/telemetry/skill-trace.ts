import { SkillTraceRecord, nowIso, uid } from '../types';
import { FsStore } from '../storage/fs-store';
import { EventService } from '../control-plane/event-service';

export class SkillTraceService {
  constructor(private readonly store: FsStore, private readonly eventService: EventService) {}

  async record(trace: Omit<SkillTraceRecord, 'trace_id' | 'timestamp'>) {
    const payload: SkillTraceRecord = {
      ...trace,
      trace_id: uid('trace'),
      timestamp: nowIso(),
    };
    await this.store.appendJsonl(this.store.skillTracesFile(trace.session_id, trace.run_id), payload);
    return payload;
  }

  async list(sessionId: string, runId: string) {
    return this.store.readJsonl<SkillTraceRecord>(this.store.skillTracesFile(sessionId, runId));
  }

  async wrap<T>(
    params: {
      session_id: string;
      run_id: string;
      skill_name: string;
      skill_version?: string | null;
      role?: 'primary' | 'supporting' | 'observer';
      input_summary?: string;
    },
    execute: () => Promise<{ output_summary?: string; outcome?: 'advanced' | 'neutral' | 'regressed'; value: T }>
  ) {
    const started = Date.now();
    await this.eventService.append(params.session_id, params.run_id, 'skill_invoked', {
      skill_name: params.skill_name,
      skill_version: params.skill_version || null,
      role: params.role || 'supporting',
      input_summary: params.input_summary || '',
    });

    const result = await execute();
    const trace = await this.record({
      session_id: params.session_id,
      run_id: params.run_id,
      skill_name: params.skill_name,
      skill_version: params.skill_version ?? null,
      role: params.role ?? 'supporting',
      input_summary: params.input_summary ?? '',
      output_summary: result.output_summary ?? '',
      outcome: result.outcome ?? 'neutral',
      latency_ms: Date.now() - started,
    });

    await this.eventService.append(params.session_id, params.run_id, 'skill_completed', {
      skill_name: trace.skill_name,
      output_summary: trace.output_summary,
      outcome: trace.outcome,
      latency_ms: trace.latency_ms,
    });

    return result.value;
  }
}
