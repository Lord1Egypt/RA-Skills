import { LIMITS } from "../monitor/limits.js";
import type { ActiveReplyState } from "../types/legacy-stream.js";

export class ActiveReplyStore {
  private activeReplies = new Map<string, ActiveReplyState>();

  constructor(private policy: "once" | "multi" = "once") {}

  store(streamId: string, responseUrl?: string, proxyUrl?: string): void {
    const url = responseUrl?.trim();
    if (!url) return;
    this.activeReplies.set(streamId, { response_url: url, proxyUrl, createdAt: Date.now() });
  }

  getUrl(streamId: string): string | undefined {
    return this.activeReplies.get(streamId)?.response_url;
  }

  async use(streamId: string, fn: (params: { responseUrl: string; proxyUrl?: string }) => Promise<void>): Promise<void> {
    const state = this.activeReplies.get(streamId);
    if (!state?.response_url) return;
    if (this.policy === "once" && state.usedAt) {
      throw new Error(`response_url already used for stream ${streamId} (Policy: once)`);
    }
    try {
      await fn({ responseUrl: state.response_url, proxyUrl: state.proxyUrl });
      state.usedAt = Date.now();
    } catch (err: unknown) {
      state.lastError = err instanceof Error ? err.message : String(err);
      throw err;
    }
  }

  prune(now: number = Date.now()): void {
    const cutoff = now - LIMITS.ACTIVE_REPLY_TTL_MS;
    for (const [id, state] of this.activeReplies.entries()) {
      if (state.createdAt < cutoff) {
        this.activeReplies.delete(id);
      }
    }
  }
}
