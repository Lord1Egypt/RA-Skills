import { bootstrapManagerRuntime } from './bootstrap';

export const recordSkillInvocation = async (
  runtime: Awaited<ReturnType<typeof bootstrapManagerRuntime>>,
  params: {
    session_id: string;
    run_id: string;
    skill_name: string;
    skill_version?: string | null;
    role?: 'primary' | 'supporting' | 'observer';
    input_summary?: string;
    output_summary?: string;
    outcome?: 'advanced' | 'neutral' | 'regressed';
    latency_ms?: number | null;
  }
) =>
  runtime.skillTraceService.record({
    session_id: params.session_id,
    run_id: params.run_id,
    skill_name: params.skill_name,
    skill_version: params.skill_version ?? null,
    role: params.role ?? 'supporting',
    input_summary: params.input_summary ?? '',
    output_summary: params.output_summary ?? '',
    outcome: params.outcome ?? 'neutral',
    latency_ms: params.latency_ms ?? null,
  });

export const wrapSkillExecution = async <T>(
  runtime: Awaited<ReturnType<typeof bootstrapManagerRuntime>>,
  params: {
    session_id: string;
    run_id: string;
    skill_name: string;
    skill_version?: string | null;
    role?: 'primary' | 'supporting' | 'observer';
    input_summary?: string;
  },
  execute: () => Promise<{ output_summary?: string; outcome?: 'advanced' | 'neutral' | 'regressed'; value: T }>
) => runtime.skillTraceService.wrap(params, execute);

export const heartbeatMaintenance = async (runtime: Awaited<ReturnType<typeof bootstrapManagerRuntime>>) => {
  const sessions = await runtime.sessionService.refreshIndexes();
  await runtime.attentionService.refresh(sessions);
  const capabilityReportPath = await runtime.capabilityFactService.writeMarkdownReport().catch(() => null);
  return {
    refreshed_sessions: sessions.length,
    capability_report_path: capabilityReportPath,
  };
};
