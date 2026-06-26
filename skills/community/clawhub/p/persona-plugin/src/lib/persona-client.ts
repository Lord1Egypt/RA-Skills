/**
 * Lightweight HTTP client for the HughKnew Persona API.
 * Follows the same fetch-based pattern as ClawTalkClient.
 */

export interface PersonaClientConfig {
  readonly server: string;
  readonly apiKey: string;
}

export class PersonaApiError extends Error {
  constructor(
    public readonly statusCode: number,
    message: string,
    public readonly body?: unknown,
  ) {
    super(message);
    this.name = 'PersonaApiError';
  }
}

export class PersonaClient {
  private readonly baseUrl: string;
  private readonly headers: Record<string, string>;

  constructor(config: PersonaClientConfig) {
    this.baseUrl = config.server.replace(/\/$/, '');
    this.headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${config.apiKey}`,
    };
  }

  private async request<T>(method: string, path: string, body?: unknown): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const signal = AbortSignal.timeout(15_000);

    let response: Response;
    try {
      response = await fetch(url, {
        method,
        headers: this.headers,
        body: body !== undefined ? JSON.stringify(body) : undefined,
        signal,
      });
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      throw new PersonaApiError(0, `Persona API unreachable: ${msg}`);
    }

    const text = await response.text();
    let parsed: unknown;
    try {
      parsed = JSON.parse(text);
    } catch {
      parsed = text;
    }

    if (!response.ok) {
      const errMsg =
        typeof parsed === 'object' && parsed !== null && 'error' in parsed
          ? (parsed as { error: string }).error
          : `${method} ${path} failed (${response.status})`;
      throw new PersonaApiError(response.status, errMsg, parsed);
    }

    return parsed as T;
  }

  // ── Callers ───────────────────────────────────────────────

  async getCaller(phone: string) {
    return this.request<CallerProfileResponse>(
      'GET',
      `/caller/${encodeURIComponent(phone)}`,
    );
  }

  async upsertCaller(phone: string, data: UpsertCallerData) {
    return this.request<{ caller: Caller }>(
      'POST',
      `/caller/${encodeURIComponent(phone)}`,
      data,
    );
  }

  // ── Calls ─────────────────────────────────────────────────

  async logCallEnd(phone: string, data: CallEndData) {
    return this.request<CallEndResponse>(
      'POST',
      `/caller/${encodeURIComponent(phone)}/call-end`,
      data,
    );
  }

  async getCallHistory(phone: string, limit = 10, offset = 0) {
    return this.request<CallHistoryResponse>(
      'GET',
      `/caller/${encodeURIComponent(phone)}/calls?limit=${limit}&offset=${offset}`,
    );
  }

  // ── Persona Documents ───────────────────────────────────

  async updatePersonaDocs(phone: string, documents: Record<string, Record<string, unknown>>) {
    return this.request<PersonaUpdateResponse>(
      'PUT',
      `/caller/${encodeURIComponent(phone)}/persona`,
      { documents },
    );
  }

  // ── Health ────────────────────────────────────────────────

  async health() {
    return this.request<{ status: string }>('GET', '/health');
  }
}

// ── Response types ──────────────────────────────────────────

export interface Caller {
  id: string;
  phone: string;
  display_name: string | null;
  relationship: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface PersonaDoc {
  id: string;
  caller_id: string;
  doc_type: string;
  content: Record<string, unknown>;
  version: number;
  created_at: string;
}

export interface CallerProfileResponse {
  caller: Caller;
  persona: {
    soul: PersonaDoc | null;
    identity: PersonaDoc | null;
    memory: PersonaDoc | null;
    [key: string]: PersonaDoc | null;
  };
  prompt_context: string;
  recent_calls: CallRecord[];
}

export interface CallRecord {
  id: string;
  caller_id: string;
  call_id: string | null;
  conversation_id: string | null;
  direction: string;
  duration_seconds: number | null;
  purpose: string | null;
  summary: string | null;
  transcript: unknown;
  metadata: unknown;
  created_at: string;
}

export interface UpsertCallerData {
  display_name?: string;
  relationship?: string;
  notes?: string;
}

export interface CallEndData {
  call_id?: string;
  duration_seconds?: number;
  direction?: 'inbound' | 'outbound';
  purpose?: string;
  summary: string;
}

export interface CallEndResponse {
  call: CallRecord;
  document_versions: Record<string, number>;
  persona_update: 'processing' | 'completed' | string;
}

export interface PersonaUpdateResponse {
  caller_id: string;
  document_versions: Record<string, number>;
  updated: string[];
}

export interface CallHistoryResponse {
  calls: CallRecord[];
  phone: string;
  limit: number;
  offset: number;
}
