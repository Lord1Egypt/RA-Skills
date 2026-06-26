import type { IncomingMessage, ServerResponse } from "node:http";

import crypto from "node:crypto";

import { handleAgentCallbackRequest } from "../agent-callback/request-handler.js";
import { handleKefuCallbackRequest } from "../kefu/request-handler.js";
import type { WecomWebhookTarget } from "../../types/runtime-context.js";
import {
  getAgentWebhookTargets,
  getKefuWebhookTargets,
  getWecomWebhookTargets,
  hasMatrixExplicitRoutesRegistered,
} from "./registry.js";
import {
  isAgentCallbackPathCandidate,
  isKefuCallbackPathCandidate,
  isNonMatrixWecomBasePath,
  logRouteFailure,
  resolvePath,
  resolveQueryParams,
  writeRouteFailure,
} from "./common.js";

export async function handleWecomHttpRequest(params: {
  req: IncomingMessage;
  res: ServerResponse;
  handleBotWebhookRequest: (params: {
    req: IncomingMessage;
    res: ServerResponse;
    path: string;
    reqId: string;
    targets: WecomWebhookTarget[];
  }) => Promise<boolean>;
}): Promise<boolean> {
  const { req, res, handleBotWebhookRequest } = params;

  const path = resolvePath(req);
  const reqId = crypto.randomUUID().slice(0, 8);
  const remote = req.socket?.remoteAddress ?? "unknown";
  const ua = String(req.headers["user-agent"] ?? "");
  const cl = String(req.headers["content-length"] ?? "");
  const q = resolveQueryParams(req);
  const hasTimestamp = Boolean(q.get("timestamp"));
  const hasNonce = Boolean(q.get("nonce"));
  const hasEchostr = Boolean(q.get("echostr"));
  const hasMsgSig = Boolean(q.get("msg_signature"));
  const hasSignature = Boolean(q.get("signature"));
  console.log(
    `[wecom] inbound(http): reqId=${reqId} path=${path} method=${req.method ?? "UNKNOWN"} remote=${remote} ua=${ua ? `"${ua}"` : "N/A"} contentLength=${cl || "N/A"} query={timestamp:${hasTimestamp},nonce:${hasNonce},echostr:${hasEchostr},msg_signature:${hasMsgSig},signature:${hasSignature}}`,
  );

  if (hasMatrixExplicitRoutesRegistered() && isNonMatrixWecomBasePath(path)) {
    logRouteFailure({
      reqId,
      path,
      method: req.method ?? "UNKNOWN",
      reason: "wecom_matrix_path_required",
      candidateAccountIds: [],
    });
    writeRouteFailure(
      res,
      "wecom_matrix_path_required",
      "Matrix mode requires explicit account path. Use /plugins/wecom/bot/{accountId} or /plugins/wecom/agent/{accountId}.",
    );
    return true;
  }

  const agentTargets = getAgentWebhookTargets(path);
  if (agentTargets.length > 0 || isAgentCallbackPathCandidate(path)) {
    return handleAgentCallbackRequest({
      req,
      res,
      path,
      reqId,
      targets: agentTargets,
    });
  }

  const kefuTargets = getKefuWebhookTargets(path);
  if (kefuTargets.length > 0 || isKefuCallbackPathCandidate(path)) {
    return handleKefuCallbackRequest({
      req,
      res,
      path,
      reqId,
      targets: kefuTargets,
    });
  }

  const botTargets = getWecomWebhookTargets(path);
  if (botTargets.length === 0) {
    return false;
  }

  return handleBotWebhookRequest({
    req,
    res,
    path,
    reqId,
    targets: botTargets,
  });
}
