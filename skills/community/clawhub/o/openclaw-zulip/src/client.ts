/**
 * Zulip REST API client.
 *
 * Thin fetch-based wrapper covering the minimal API surface needed by the
 * OpenClaw Zulip channel adapter. Uses HTTP Basic Auth (email:apiKey).
 *
 * @see https://zulip.com/api/rest
 */

import type {
  ZulipClientConfig,
  ServerSettings,
  OwnUser,
  SendMessageParams,
  SendMessageResponse,
  UploadFileResponse,
  GetMessagesParams,
  GetMessagesResponse,
  RegisterQueueParams,
  RegisterResponse,
  EventsResponse,
  ZulipApiError,
} from "./types.js";

export class ZulipApiRequestError extends Error {
  constructor(
    public readonly code: string | undefined,
    message: string,
    public readonly status?: number,
  ) {
    super(message);
    this.name = "ZulipApiRequestError";
  }
}

export class ZulipClient {
  private readonly baseUrl: string;
  private readonly authHeader: string;
  private readonly timeout: number;

  constructor(private readonly config: ZulipClientConfig) {
    // Normalize realm: strip trailing slash
    const realm = config.realm.replace(/\/+$/, "");
    this.baseUrl = `${realm}/api/v1`;
    this.authHeader = `Basic ${btoa(`${config.email}:${config.apiKey}`)}`;
    this.timeout = config.timeout ?? 90_000;
  }

  // ─── Probe ───

  /** GET /server_settings — no auth required. */
  async getServerSettings(): Promise<ServerSettings> {
    const realm = this.config.realm.replace(/\/+$/, "");
    const res = await this.rawFetch(`${realm}/api/v1/server_settings`, {
      method: "GET",
      // No auth header — this endpoint is public
    });
    return this.parseResponse<ServerSettings>(res);
  }

  // ─── Identity ───

  /** GET /users/me — get bot's own user info. */
  async getOwnUser(): Promise<OwnUser> {
    return this.get<OwnUser>("/users/me");
  }

  // ─── Messaging ───

  /** POST /messages — send a channel or DM message. */
  async sendMessage(params: SendMessageParams): Promise<SendMessageResponse> {
    const body = new URLSearchParams();
    body.set("type", params.type);
    body.set("to", Array.isArray(params.to) ? JSON.stringify(params.to) : String(params.to));
    if (params.topic != null) {
      body.set("topic", params.topic);
    }
    body.set("content", params.content);
    return this.post<SendMessageResponse>("/messages", body);
  }

  /** GET /messages — fetch message history with narrow filters. */
  async getMessages(params: GetMessagesParams): Promise<GetMessagesResponse> {
    const qs = new URLSearchParams();
    qs.set("anchor", String(params.anchor));
    qs.set("num_before", String(params.num_before));
    qs.set("num_after", String(params.num_after));
    if (params.narrow) {
      qs.set("narrow", JSON.stringify(params.narrow));
    }
    return this.get<GetMessagesResponse>(`/messages?${qs}`);
  }

  // ─── Media ───

  /** POST /user_uploads — upload a file, returns URI for embedding in messages. */
  async uploadFile(
    filename: string,
    data: Blob,
    _contentType: string,
  ): Promise<UploadFileResponse> {
    const form = new FormData();
    form.append("filename", data, filename);

    const res = await this.rawFetch(`${this.baseUrl}/user_uploads`, {
      method: "POST",
      headers: { Authorization: this.authHeader },
      body: form,
      signal: AbortSignal.timeout(this.timeout),
    });
    return this.parseResponse<UploadFileResponse>(res);
  }

  // ─── Event Queue ───

  /** POST /register — register an event queue for long-polling. */
  async registerQueue(params: RegisterQueueParams = {}): Promise<RegisterResponse> {
    const body = new URLSearchParams();
    if (params.event_types) {
      body.set("event_types", JSON.stringify(params.event_types));
    }
    if (params.narrow) {
      body.set("narrow", JSON.stringify(params.narrow));
    }
    if (params.all_public_streams != null) {
      body.set("all_public_streams", String(params.all_public_streams));
    }
    if (params.apply_markdown != null) {
      body.set("apply_markdown", String(params.apply_markdown));
    }
    if (params.idle_queue_timeout != null) {
      body.set("idle_queue_timeout", String(params.idle_queue_timeout));
    }
    return this.post<RegisterResponse>("/register", body);
  }

  /** GET /events — long-poll for events from a registered queue. */
  async getEvents(
    queueId: string,
    lastEventId: number,
    dontBlock = false,
  ): Promise<EventsResponse> {
    const qs = new URLSearchParams({
      queue_id: queueId,
      last_event_id: String(lastEventId),
    });
    if (dontBlock) {
      qs.set("dont_block", "true");
    }
    // Long-poll may block server-side; use extended timeout
    return this.get<EventsResponse>(`/events?${qs}`, this.timeout + 30_000);
  }

  /** DELETE /events — destroy an event queue. */
  async deleteQueue(queueId: string): Promise<void> {
    const body = new URLSearchParams({ queue_id: queueId });
    const res = await this.rawFetch(`${this.baseUrl}/events`, {
      method: "DELETE",
      headers: {
        Authorization: this.authHeader,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body,
      signal: AbortSignal.timeout(this.timeout),
    });
    await this.parseResponse(res);
  }

  // ─── Internals ───

  private async get<T>(path: string, timeout?: number): Promise<T> {
    const res = await this.rawFetch(`${this.baseUrl}${path}`, {
      method: "GET",
      headers: { Authorization: this.authHeader },
      signal: AbortSignal.timeout(timeout ?? this.timeout),
    });
    return this.parseResponse<T>(res);
  }

  private async post<T>(path: string, body: URLSearchParams): Promise<T> {
    const res = await this.rawFetch(`${this.baseUrl}${path}`, {
      method: "POST",
      headers: {
        Authorization: this.authHeader,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body,
      signal: AbortSignal.timeout(this.timeout),
    });
    return this.parseResponse<T>(res);
  }

  private async rawFetch(url: string, init: RequestInit): Promise<Response> {
    const maxRetries = 5;
    let attempt = 0;

    while (true) {
      const res = await fetch(url, init);

      if (res.status !== 429 || attempt >= maxRetries) {
        return res;
      }

      // Exponential backoff with jitter, respecting Retry-After header
      const retryAfter = res.headers.get("Retry-After");
      const baseMs = retryAfter ? Number(retryAfter) * 1000 : 1000 * 2 ** attempt;
      const jitter = Math.random() * 1000;
      const waitMs = Math.min(baseMs + jitter, 60_000);
      await new Promise((r) => setTimeout(r, waitMs));
      attempt++;
    }
  }

  private async parseResponse<T>(res: Response): Promise<T> {
    const json = (await res.json()) as (T & { result?: string }) | ZulipApiError;

    if ("result" in json && json.result === "error") {
      const err = json as ZulipApiError;
      throw new ZulipApiRequestError(err.code, err.msg, res.status);
    }

    return json as T;
  }
}
