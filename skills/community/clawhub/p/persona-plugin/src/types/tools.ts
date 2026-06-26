// ── Tool param types ────────────────────────────────────────

export interface GetCallerParams {
  readonly phone: string;
}

export interface LogCallParams {
  readonly phone: string;
  readonly summary: string;
  readonly call_id?: string;
  readonly duration_seconds?: number;
  readonly direction?: 'inbound' | 'outbound';
  readonly purpose?: string;
}

// ── Tool result types ───────────────────────────────────────

export interface GetCallerResult {
  readonly found: boolean;
  readonly caller: unknown;
  readonly persona: unknown;
  readonly prompt_context: string;
  readonly recent_calls: unknown[];
  readonly message: string;
}

export interface LogCallResult {
  readonly call: unknown;
  readonly persona_update: string;
  readonly document_versions: Record<string, number>;
  readonly message: string;
}
