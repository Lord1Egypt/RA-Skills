import type { IncomingMessage, ServerResponse } from "node:http";

import { decryptWecomEncrypted, verifyWecomSignature } from "../../crypto.js";
import { extractEncryptFromXml } from "../../crypto/xml.js";
import { getWecomRuntime } from "../../runtime.js";
import { handleAgentWebhook } from "../../agent/index.js";
import { extractAgentId, parseXml } from "../../shared/xml-parser.js";
import { LIMITS as WECOM_LIMITS } from "../../types/constants.js";
import type { AgentWebhookTarget } from "../http/registry.js";
import {
  logRouteFailure,
  readTextBody,
  resolveQueryParams,
  resolveSignatureParam,
  type RouteFailureReason,
  writeRouteFailure,
} from "../http/common.js";

const ERROR_HELP = "\n\n遇到问题？联系作者: YanHaidao (微信: YanHaidao)";

function truncateForLog(raw: string, maxChars = 600): string {
  const compact = raw.replace(/\s+/g, " ").trim();
  if (compact.length <= maxChars) return compact;
  return `${compact.slice(0, maxChars)}...(truncated)`;
}

function buildParsedAgentSummary(parsed: ReturnType<typeof parseXml>): string {
  const data = parsed as Record<string, unknown>;
  const msgType = String(data.MsgType ?? "").trim() || "unknown";
  const fromUser = String(data.FromUserName ?? "").trim() || "N/A";
  const toUser = String(data.ToUserName ?? "").trim() || "N/A";
  const event = String(data.Event ?? "").trim() || "N/A";
  const msgId = String(data.MsgId ?? "").trim() || "N/A";
  const chatId = String(data.ChatId ?? data.chatid ?? "").trim() || "N/A";
  const agentId = String(data.AgentID ?? "").trim() || "N/A";
  return `msgType=${msgType} from=${fromUser} to=${toUser} event=${event} msgId=${msgId} chatId=${chatId} agentId=${agentId}`;
}

function normalizeAgentIdValue(value: unknown): number | undefined {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  const raw = String(value ?? "").trim();
  if (!raw) return undefined;
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : undefined;
}

export async function handleAgentCallbackRequest(params: {
  req: IncomingMessage;
  res: ServerResponse;
  path: string;
  reqId: string;
  targets: AgentWebhookTarget[];
}): Promise<boolean> {
  const { req, res, path, reqId, targets } = params;
  if (targets.length === 0) {
    console.error(
      `[wecom] inbound(agent): reqId=${reqId} path=${path} no_registered_target availableTargets=0`,
    );
    res.statusCode = 404;
    res.setHeader("Content-Type", "text/plain; charset=utf-8");
    res.end(`agent not configured for path=${path} - Agent 模式未配置或回调路径错误，请运行 openclaw onboarding${ERROR_HELP}`);
    return true;
  }

  const query = resolveQueryParams(req);
  const timestamp = query.get("timestamp") ?? "";
  const nonce = query.get("nonce") ?? "";
  const signature = resolveSignatureParam(query);
  const hasSig = Boolean(signature);
  const remote = req.socket?.remoteAddress ?? "unknown";

  if (req.method === "GET") {
    const echostr = query.get("echostr") ?? "";
    const signatureMatches = targets.filter((target) =>
      verifyWecomSignature({
        token: target.agent.token,
        timestamp,
        nonce,
        encrypt: echostr,
        signature,
      }),
    );
    if (signatureMatches.length !== 1) {
      const reason: RouteFailureReason =
        signatureMatches.length === 0 ? "wecom_account_not_found" : "wecom_account_conflict";
      const candidateIds = (signatureMatches.length > 0 ? signatureMatches : targets).map((target) => target.agent.accountId);
      logRouteFailure({
        reqId,
        path,
        method: "GET",
        reason,
        candidateAccountIds: candidateIds,
      });
      writeRouteFailure(
        res,
        reason,
        reason === "wecom_account_conflict"
          ? "Agent callback account conflict: multiple accounts matched signature."
          : "Agent callback account not found: signature verification failed.",
      );
      return true;
    }
    const selected = signatureMatches[0]!;
    try {
      const plain = decryptWecomEncrypted({
        encodingAESKey: selected.agent.encodingAESKey,
        receiveId: selected.agent.corpId,
        encrypt: echostr,
      });
      res.statusCode = 200;
      res.setHeader("Content-Type", "text/plain; charset=utf-8");
      res.end(plain);
      return true;
    } catch {
      res.statusCode = 400;
      res.setHeader("Content-Type", "text/plain; charset=utf-8");
      res.end(`decrypt failed - 解密失败，请检查 EncodingAESKey${ERROR_HELP}`);
      return true;
    }
  }

  if (req.method !== "POST") {
    return false;
  }

  const rawBody = await readTextBody(req, WECOM_LIMITS.MAX_REQUEST_BODY_SIZE);
  if (!rawBody.ok) {
    res.statusCode = 400;
    res.setHeader("Content-Type", "text/plain; charset=utf-8");
    res.end(rawBody.error || "invalid payload");
    return true;
  }

  console.log(
    `[wecom] inbound(agent): reqId=${reqId} path=${path} rawXmlBytes=${Buffer.byteLength(rawBody.value, "utf8")} rawPreview=${JSON.stringify(truncateForLog(rawBody.value))}`,
  );

  let encrypted = "";
  try {
    encrypted = extractEncryptFromXml(rawBody.value);
  } catch {
    res.statusCode = 400;
    res.setHeader("Content-Type", "text/plain; charset=utf-8");
    res.end(`invalid xml - 缺少 Encrypt 字段${ERROR_HELP}`);
    return true;
  }

  console.log(
    `[wecom] inbound(agent): reqId=${reqId} path=${path} encryptedLen=${encrypted.length}`,
  );

  const signatureMatches = targets.filter((target) =>
    verifyWecomSignature({
      token: target.agent.token,
      timestamp,
      nonce,
      encrypt: encrypted,
      signature,
    }),
  );
  if (signatureMatches.length !== 1) {
    const reason: RouteFailureReason =
      signatureMatches.length === 0 ? "wecom_account_not_found" : "wecom_account_conflict";
    const candidateIds = (signatureMatches.length > 0 ? signatureMatches : targets).map((target) => target.agent.accountId);
    logRouteFailure({
      reqId,
      path,
      method: "POST",
      reason,
      candidateAccountIds: candidateIds,
    });
    writeRouteFailure(
      res,
      reason,
      reason === "wecom_account_conflict"
        ? "Agent callback account conflict: multiple accounts matched signature."
        : "Agent callback account not found: signature verification failed.",
    );
    return true;
  }

  const selected = signatureMatches[0]!;
  let decrypted = "";
  let parsed: ReturnType<typeof parseXml> | null = null;
  try {
    decrypted = decryptWecomEncrypted({
      encodingAESKey: selected.agent.encodingAESKey,
      receiveId: selected.agent.corpId,
      encrypt: encrypted,
    });
    parsed = parseXml(decrypted);
  } catch {
    res.statusCode = 400;
    res.setHeader("Content-Type", "text/plain; charset=utf-8");
    res.end(`decrypt failed - 解密失败，请检查 EncodingAESKey${ERROR_HELP}`);
    return true;
  }
  if (!parsed) {
    res.statusCode = 400;
    res.setHeader("Content-Type", "text/plain; charset=utf-8");
    res.end(`invalid xml - XML 解析失败${ERROR_HELP}`);
    return true;
  }

  selected.runtimeEnv.log?.(
    `[wecom] inbound(agent): reqId=${reqId} accountId=${selected.agent.accountId} decryptedBytes=${Buffer.byteLength(decrypted, "utf8")} parsed=${buildParsedAgentSummary(parsed)} decryptedPreview=${JSON.stringify(truncateForLog(decrypted))}`,
  );

  const inboundAgentId = normalizeAgentIdValue(extractAgentId(parsed));
  if (
    inboundAgentId !== undefined &&
    selected.agent.agentId !== undefined &&
    inboundAgentId !== selected.agent.agentId
  ) {
    selected.runtimeEnv.error?.(
      `[wecom] inbound(agent): reqId=${reqId} accountId=${selected.agent.accountId} agentId_mismatch expected=${selected.agent.agentId} actual=${inboundAgentId}`,
    );
  }

  const core = getWecomRuntime();
  selected.runtimeEnv.log?.(
    `[wecom] inbound(agent): reqId=${reqId} method=${req.method ?? "UNKNOWN"} remote=${remote} timestamp=${timestamp ? "yes" : "no"} nonce=${nonce ? "yes" : "no"} msg_signature=${hasSig ? "yes" : "no"} accountId=${selected.agent.accountId}`,
  );
  selected.touchTransportSession?.({ lastInboundAt: Date.now(), running: true });
  return handleAgentWebhook({
    req,
    res,
    verifiedPost: {
      timestamp,
      nonce,
      signature,
      encrypted,
      decrypted,
      parsed,
    },
    agent: selected.agent,
    config: selected.config,
    core,
    log: selected.runtimeEnv.log,
    error: selected.runtimeEnv.error,
    auditSink: selected.auditSink,
    touchTransportSession: selected.touchTransportSession,
  });
}
