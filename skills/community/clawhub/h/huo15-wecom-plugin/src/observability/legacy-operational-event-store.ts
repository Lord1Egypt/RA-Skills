import { LIMITS } from "../monitor/limits.js";
import type { WecomAuditCategory, WecomTransportKind } from "../types/index.js";

export type MonitorOperationalEvent = {
  accountId?: string;
  transport: WecomTransportKind;
  category: WecomAuditCategory;
  summary: string;
  messageId?: string;
  createdAt: number;
};

export class LegacyOperationalEventStore {
  private readonly events: MonitorOperationalEvent[] = [];

  append(event: Omit<MonitorOperationalEvent, "createdAt">): void {
    this.events.push({
      ...event,
      createdAt: Date.now(),
    });
    if (this.events.length > 200) {
      this.events.shift();
    }
  }

  list(): MonitorOperationalEvent[] {
    return [...this.events];
  }

  prune(now: number = Date.now()): void {
    const cutoff = now - LIMITS.ACTIVE_REPLY_TTL_MS;
    while (this.events.length > 0 && this.events[0] && this.events[0].createdAt < cutoff) {
      this.events.shift();
    }
  }
}
