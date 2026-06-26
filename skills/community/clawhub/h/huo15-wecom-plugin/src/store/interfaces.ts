import type { DeliveryTask, ReplyContext, TransportSessionSnapshot, UnifiedInboundEvent } from "../types/index.js";

export type RuntimeStore = {
  markInboundSeen: (event: UnifiedInboundEvent) => boolean;
  readReplyContext: (messageId: string) => ReplyContext | undefined;
  writeReplyContext: (messageId: string, context: ReplyContext) => void;
  readTransportSession: (accountId: string, transport: TransportSessionSnapshot["transport"]) => TransportSessionSnapshot | undefined;
  writeTransportSession: (snapshot: TransportSessionSnapshot) => void;
  writeDeliveryTask: (task: DeliveryTask) => void;
  readDeliveryTask: (messageId: string) => DeliveryTask | undefined;
};
