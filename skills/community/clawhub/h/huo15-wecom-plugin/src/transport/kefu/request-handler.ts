import type { IncomingMessage, ServerResponse } from "node:http";

import { decryptWecomEncrypted, verifyWecomSignature } from "../../crypto.js";
import { extractEncryptFromXml } from "../../crypto/xml.js";
import { parseXml } from "../../shared/xml-parser.js";
import { LIMITS as WECOM_LIMITS } from "../../types/constants.js";
import type { KefuWebhookTarget } from "../http/registry.js";
import {
  logRouteFailure,
  readTextBody,
  resolveQueryParams,
  resolveSignatureParam,
  type RouteFailureReason,
  writeRouteFailure,
} from "../http/common.js";
import { processKefuCallback } from "./handler.js";

const ERROR_HELP = "\n\n遇到问题？联系作者: YanHaidao (微信: YanHaidao)";

function truncateForLog(raw: string, maxChars = 600): string {
  const compact = raw.replace(/\s+/g, " ").trim();
  if (compact.length <= maxChars) return compact;
  return `${compact.slice(0, maxChars)}...(truncated)`;
}

export async function handleKefuCallbackRequest(params: {
  req: IncomingMessage;
  res: ServerResponse;
  path: string;
  reqId: string;
  targets: KefuWebhookTarget[];
}): Promise<boolean> {
  const { req, res, path, reqId, targets } = params;
  if (targets.length === 0) {
    console.error(
      `[wecom] inbound(kefu): reqId=${reqId} path=${path} no_registered_target availableTargets=0`,
    );
    res.statusCode = 404;
    res.setHeader("Content-Type", "text/plain; charset=utf-8");
    res.end(`kefu not configured for path=${path} - 客服未配置或回调路径错误${ERROR_HELP}`);
    return true;
  }

  const query = resolveQueryParams(req);
  const timestamp = query.get("timestamp") ?? "";
  const nonce = query.get("nonce") ?? "";
  const signature = resolveSignatureParam(query);

  if (req.method === "GET") {
    const echostr = query.get("echostr") ?? "";
    const signatureMatches = targets.filter((target) =>
      verifyWecomSignature({
        token: target.kefu.token,
        timestamp,
        nonce,
        encrypt: echostr,
        signature,
      }),
    );
    if (signatureMatches.length !== 1) {
      const reason: RouteFailureReason =
        signatureMatches.length === 0 ? "wecom_account_not_found" : "wecom_account_conflict";
      const candidateIds = (signatureMatches.length > 0 ? signatureMatches : targets).map(
        (target) => target.kefu.accountId,
      );
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
          ? "Kefu callback account conflict: multiple accounts matched signature."
          : "Kefu callback account not found: signature verification failed.",
      );
      return true;
    }
    const selected = signatureMatches[0]!;
    try {
      const plain = decryptWecomEncrypted({
        encodingAESKey: selected.kefu.encodingAESKey,
        receiveId: selected.kefu.corpId,
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

  let encrypted = "";
  try {
    encrypted = extractEncryptFromXml(rawBody.value);
  } catch {
    res.statusCode = 400;
    res.setHeader("Content-Type", "text/plain; charset=utf-8");
    res.end(`invalid xml - 缺少 Encrypt 字段${ERROR_HELP}`);
    return true;
  }

  const signatureMatches = targets.filter((target) =>
    verifyWecomSignature({
      token: target.kefu.token,
      timestamp,
      nonce,
      encrypt: encrypted,
      signature,
    }),
  );
  if (signatureMatches.length !== 1) {
    const reason: RouteFailureReason =
      signatureMatches.length === 0 ? "wecom_account_not_found" : "wecom_account_conflict";
    const candidateIds = (signatureMatches.length > 0 ? signatureMatches : targets).map(
      (target) => target.kefu.accountId,
    );
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
        ? "Kefu callback account conflict: multiple accounts matched signature."
        : "Kefu callback account not found: signature verification failed.",
    );
    return true;
  }

  const selected = signatureMatches[0]!;
  let decrypted = "";
  let parsed: ReturnType<typeof parseXml> | null = null;
  try {
    decrypted = decryptWecomEncrypted({
      encodingAESKey: selected.kefu.encodingAESKey,
      receiveId: selected.kefu.corpId,
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
    `[wecom] inbound(kefu): reqId=${reqId} accountId=${selected.kefu.accountId} path=${path} decryptedPreview=${JSON.stringify(truncateForLog(decrypted))}`,
  );
  selected.touchTransportSession?.({ lastInboundAt: Date.now(), running: true });

  const parsedRecord = parsed as Record<string, unknown>;
  const token = String(parsedRecord.Token ?? "").trim();
  const openKfIdRaw = parsedRecord.OpenKfId ?? parsedRecord.OpenKfID ?? parsedRecord.open_kfid;
  const openKfId = openKfIdRaw != null ? String(openKfIdRaw).trim() : "";

  res.statusCode = 200;
  res.setHeader("Content-Type", "text/plain; charset=utf-8");
  res.end("");

  void processKefuCallback({
    target: selected,
    envelope: {
      token,
      openKfId: openKfId || undefined,
      rawXml: decrypted,
      reqId,
    },
  }).catch((err) => {
    selected.runtimeEnv.error?.(
      `[wecom] inbound(kefu): reqId=${reqId} accountId=${selected.kefu.accountId} process_failed err=${String(err)}`,
    );
  });
  return true;
}
