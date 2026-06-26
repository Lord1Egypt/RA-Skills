import type { ReplyContext } from "../../types/index.js";

export function createKefuReplyContext(params: {
  accountId: string;
  raw: ReplyContext["raw"];
  peerId?: string;
  peerKind?: "direct" | "group";
}): ReplyContext {
  return {
    transport: "kefu",
    accountId: params.accountId,
    peerId: params.peerId,
    peerKind: params.peerKind ?? "direct",
    raw: params.raw,
  };
}
