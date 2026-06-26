import { LegacyOperationalEventStore, type MonitorOperationalEvent } from "../observability/legacy-operational-event-store.js";
import { ActiveReplyStore } from "../store/active-reply-store.js";
import { StreamStore } from "../store/stream-batch-store.js";
import { LIMITS } from "./limits.js";

export { LIMITS, StreamStore, ActiveReplyStore };
export type { MonitorOperationalEvent };

class MonitorState {
  public readonly streamStore = new StreamStore();
  public readonly activeReplyStore = new ActiveReplyStore("multi");
  public readonly operationalEvents = new LegacyOperationalEventStore();

  private pruneInterval?: NodeJS.Timeout;

  public startPruning(intervalMs: number = 60_000): void {
    if (this.pruneInterval) return;
    this.pruneInterval = setInterval(() => {
      const now = Date.now();
      this.streamStore.prune(now);
      this.activeReplyStore.prune(now);
      this.operationalEvents.prune(now);
    }, intervalMs);
  }

  public stopPruning(): void {
    if (this.pruneInterval) {
      clearInterval(this.pruneInterval);
      this.pruneInterval = undefined;
    }
  }
}

export const monitorState = new MonitorState();
