import type { RuntimeStore } from "./interfaces.js";
import type { DeliveryTask, ReplyContext, TransportSessionSnapshot, UnifiedInboundEvent } from "../types/index.js";
import { buildDedupKey } from "../domain/policies.js";

export class InMemoryRuntimeStore implements RuntimeStore {
  private readonly seen = new Set<string>();
  private readonly replyContexts = new Map<string, ReplyContext>();
  private readonly transportSessions = new Map<string, TransportSessionSnapshot>();
  private readonly deliveryTasks = new Map<string, DeliveryTask>();

  markInboundSeen(event: UnifiedInboundEvent): boolean {
    const key = buildDedupKey(event);
    if (this.seen.has(key)) {
      return false;
    }
    this.seen.add(key);
    return true;
  }

  readReplyContext(messageId: string): ReplyContext | undefined {
    return this.replyContexts.get(messageId);
  }

  writeReplyContext(messageId: string, context: ReplyContext): void {
    this.replyContexts.set(messageId, context);
  }

  readTransportSession(accountId: string, transport: TransportSessionSnapshot["transport"]): TransportSessionSnapshot | undefined {
    return this.transportSessions.get(`${accountId}:${transport}`);
  }

  writeTransportSession(snapshot: TransportSessionSnapshot): void {
    this.transportSessions.set(`${snapshot.accountId}:${snapshot.transport}`, snapshot);
  }

  writeDeliveryTask(task: DeliveryTask): void {
    this.deliveryTasks.set(task.messageId, task);
  }

  readDeliveryTask(messageId: string): DeliveryTask | undefined {
    return this.deliveryTasks.get(messageId);
  }
}
