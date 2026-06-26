import type { DeliveryTask, RawFrameReference, ReplyContext, TransportSessionSnapshot, UnifiedInboundEvent } from "../types/index.js";

export type WecomConversation = UnifiedInboundEvent["conversation"];
export type WecomRawEnvelope = RawFrameReference;
export type WecomReplyContext = ReplyContext;
export type WecomTransportSession = TransportSessionSnapshot;
export type WecomDeliveryTask = DeliveryTask;
