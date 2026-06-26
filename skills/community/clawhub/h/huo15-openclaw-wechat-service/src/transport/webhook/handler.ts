/**
 * 微信服务号 Webhook HTTP 入口
 *
 * 流程：
 * 1. 解析 path → 查找注册的 webhook 目标
 * 2. GET：服务器 URL 校验（echostr）
 * 3. POST：取 body → 如是 safe/compat 模式先取 Encrypt → 验签 → 解密 → 解析 XML
 * 4. 立即响应 200 "success" 或被动回复 XML，后台异步跑 agent
 */

import type { IncomingMessage, ServerResponse } from "node:http";
import crypto from "node:crypto";

import { sendCustomerServiceMessage } from "../../api/customer-service.js";
import { accessTokenHandleFor } from "../../access-token.js";
import { checkAutoReply, renderWelcomeText } from "../../auto-reply.js";
import {
  computeServerVerifySignature,
  decryptEncrypted,
  verifyMsgSignature,
  verifyServerSignature,
} from "../../crypto.js";
import { tryGetWechatServiceRuntime } from "../../runtime.js";
import {
  buildPassiveReplyXml,
  parseInboundMessage,
  extractEncryptField,
} from "../../shared/xml-parser.js";
import type {
  ResolvedWechatServiceAccount,
  WechatServiceConfig,
} from "../../types.js";
import { dispatchInboundEvent } from "../../runtime/dispatcher.js";
import {
  buildUnifiedInboundEvent,
  resolveEventRoutingAgentId,
} from "./normalize.js";
import type { OpenClawConfig, PluginRuntime } from "openclaw/plugin-sdk";
import {
  MAX_REQUEST_BODY_SIZE,
  logRouteFailure,
  readTextBody,
  resolvePath,
  resolveQueryParams,
  resolveSignatureParam,
  writeRouteFailure,
} from "./common.js";
import { getWebhookTargets, type WebhookTarget } from "./registry.js";

const HELP_SUFFIX = "\n\n微信服务号接入问题？请检查 channels[\"wechat-service\"].accounts 配置 + 公众号后台 URL/Token/EncodingAESKey 是否一致。";

export async function handleWechatServiceHttpRequest(
  req: IncomingMessage,
  res: ServerResponse,
): Promise<boolean> {
  const path = resolvePath(req);
  const reqId = crypto.randomUUID().slice(0, 8);
  const method = req.method ?? "UNKNOWN";

  const targets = getWebhookTargets(path);
  if (targets.length === 0) {
    return false;
  }

  const query = resolveQueryParams(req);
  const timestamp = query.get("timestamp") ?? "";
  const nonce = query.get("nonce") ?? "";
  const signature = resolveSignatureParam(query);

  console.log(
    `[wechat-service] inbound(http): reqId=${reqId} path=${path} method=${method} targets=${targets.length} signed=${Boolean(signature)}`,
  );

  if (method === "GET") {
    return handleServerVerification({
      req,
      res,
      path,
      reqId,
      query,
      timestamp,
      nonce,
      signature,
      targets,
    });
  }

  if (method !== "POST") {
    writeRouteFailure(res, "wechat_service_method_not_allowed", "only GET/POST allowed");
    return true;
  }

  const rawBody = await readTextBody(req, MAX_REQUEST_BODY_SIZE);
  if (!rawBody.ok) {
    writeRouteFailure(res, "wechat_service_payload_too_large", rawBody.error);
    return true;
  }

  return handleInbound({
    res,
    path,
    reqId,
    timestamp,
    nonce,
    signature,
    rawBody: rawBody.value,
    targets,
  });
}

async function handleServerVerification(params: {
  req: IncomingMessage;
  res: ServerResponse;
  path: string;
  reqId: string;
  query: URLSearchParams;
  timestamp: string;
  nonce: string;
  signature: string;
  targets: WebhookTarget[];
}): Promise<boolean> {
  const { res, path, reqId, query, timestamp, nonce, signature, targets } = params;
  const echostr = query.get("echostr") ?? "";

  for (const target of targets) {
    const { account } = target;
    if (!account.token) continue;
    const matchesPlain = verifyServerSignature({
      token: account.token,
      timestamp,
      nonce,
      signature,
    });
    if (matchesPlain) {
      res.statusCode = 200;
      res.setHeader("Content-Type", "text/plain; charset=utf-8");
      res.end(echostr);
      target.runtime.log?.(
        `[wechat-service] server_verify_ok reqId=${reqId} accountId=${account.accountId} path=${path}`,
      );
      target.touchTransportSession?.({ running: true, lastInboundAt: Date.now() });
      return true;
    }

    if (account.encryptMode !== "plain" && account.encodingAESKey) {
      const matchesSafe = verifyMsgSignature({
        token: account.token,
        timestamp,
        nonce,
        encrypt: echostr,
        signature,
      });
      if (matchesSafe) {
        try {
          const plain = decryptEncrypted({
            encodingAESKey: account.encodingAESKey,
            receiveId: account.appId,
            encrypt: echostr,
          });
          res.statusCode = 200;
          res.setHeader("Content-Type", "text/plain; charset=utf-8");
          res.end(plain);
          target.runtime.log?.(
            `[wechat-service] server_verify_ok(safe) reqId=${reqId} accountId=${account.accountId} path=${path}`,
          );
          target.touchTransportSession?.({ running: true, lastInboundAt: Date.now() });
          return true;
        } catch (err) {
          target.runtime.error?.(
            `[wechat-service] server_verify_decrypt_failed reqId=${reqId} accountId=${account.accountId}: ${err instanceof Error ? err.message : String(err)}`,
          );
        }
      }
    }
  }

  logRouteFailure({
    reqId,
    path,
    method: "GET",
    reason: "wechat_service_signature_invalid",
    candidateAccountIds: targets.map((t) => t.account.accountId),
  });
  writeRouteFailure(res, "wechat_service_signature_invalid", `URL verification signature mismatch${HELP_SUFFIX}`);
  return true;
}

async function handleInbound(params: {
  res: ServerResponse;
  path: string;
  reqId: string;
  timestamp: string;
  nonce: string;
  signature: string;
  rawBody: string;
  targets: WebhookTarget[];
}): Promise<boolean> {
  const { res, path, reqId, timestamp, nonce, signature, rawBody, targets } = params;

  let decryptedXml = rawBody;
  let encryptedField: string | undefined;
  try {
    encryptedField = extractEncryptField(rawBody);
  } catch {
    encryptedField = undefined;
  }

  const matchedTargets: WebhookTarget[] = [];
  if (encryptedField) {
    for (const target of targets) {
      const { account } = target;
      if (!account.token || !account.encodingAESKey) continue;
      const matches = verifyMsgSignature({
        token: account.token,
        timestamp,
        nonce,
        encrypt: encryptedField,
        signature,
      });
      if (matches) matchedTargets.push(target);
    }
  } else {
    for (const target of targets) {
      const { account } = target;
      if (!account.token) continue;
      const matches = verifyServerSignature({
        token: account.token,
        timestamp,
        nonce,
        signature,
      });
      if (matches) matchedTargets.push(target);
    }
  }

  if (matchedTargets.length !== 1) {
    logRouteFailure({
      reqId,
      path,
      method: "POST",
      reason:
        matchedTargets.length === 0
          ? "wechat_service_signature_invalid"
          : "wechat_service_account_conflict",
      candidateAccountIds: (matchedTargets.length ? matchedTargets : targets).map(
        (t) => t.account.accountId,
      ),
    });
    writeRouteFailure(
      res,
      matchedTargets.length === 0
        ? "wechat_service_signature_invalid"
        : "wechat_service_account_conflict",
      matchedTargets.length === 0
        ? `POST signature mismatch for path=${path}${HELP_SUFFIX}`
        : `Multiple accounts matched signature — set distinct tokens per account.${HELP_SUFFIX}`,
    );
    return true;
  }

  const selected = matchedTargets[0]!;

  if (encryptedField) {
    try {
      decryptedXml = decryptEncrypted({
        encodingAESKey: selected.account.encodingAESKey,
        receiveId: selected.account.appId,
        encrypt: encryptedField,
      });
    } catch (err) {
      selected.runtime.error?.(
        `[wechat-service] decrypt_failed reqId=${reqId} accountId=${selected.account.accountId}: ${err instanceof Error ? err.message : String(err)}`,
      );
      writeRouteFailure(res, "wechat_service_decrypt_failed", `decrypt failed${HELP_SUFFIX}`);
      return true;
    }
  }

  let inbound;
  try {
    inbound = parseInboundMessage(decryptedXml);
  } catch (err) {
    selected.runtime.error?.(
      `[wechat-service] invalid_xml reqId=${reqId} accountId=${selected.account.accountId}: ${err instanceof Error ? err.message : String(err)}`,
    );
    writeRouteFailure(res, "wechat_service_invalid_xml", `invalid xml body${HELP_SUFFIX}`);
    return true;
  }

  const event = buildUnifiedInboundEvent({
    accountId: selected.account.accountId,
    inbound,
  });

  // ---- 立即响应 ----
  // 在 async 模式下，给粉丝一个被动回复占位文本（"收到，正在为你处理..."），
  // 避免 agent LLM 跑完之前粉丝那边"啥反应都没有"的体验。
  // 真正的 agent 回复随后通过 customservice/send 发出（48h 窗口）。
  //
  // 注意：微信被动回复**只能给"普通消息"用**，对 event 类（关注/扫码/点击等）
  // 应仍返回 "success"（避免微信侧重发）。
  // 同时排除 unknown 类型，保证 placeholder 仅对 text/image/voice/video/short_video/
  // location/link 等"用户主动发的消息"生效。
  const isUserMessage =
    inbound.msgType !== "event" && inbound.msgType !== "unknown";
  const placeholderText = selected.account.replyPlaceholderText?.trim();
  const useAsyncPlaceholder =
    selected.account.replyMode === "async" &&
    isUserMessage &&
    Boolean(placeholderText);

  res.statusCode = 200;
  if (useAsyncPlaceholder) {
    const placeholderXml = buildPassiveReplyXml({
      toUser: inbound.fromUserName,
      fromUser: inbound.toUserName,
      reply: { type: "text", content: placeholderText! },
    });
    res.setHeader("Content-Type", "application/xml; charset=utf-8");
    res.end(placeholderXml);
  } else {
    res.setHeader("Content-Type", "text/plain; charset=utf-8");
    res.end("success");
  }
  selected.touchTransportSession?.({ running: true, lastInboundAt: Date.now() });
  selected.runtime.log?.(
    `[wechat-service] acked(${useAsyncPlaceholder ? "placeholder" : "success"}) reqId=${reqId} accountId=${selected.account.accountId} msgType=${inbound.msgType}${inbound.event ? `/${inbound.event}` : ""} from=${inbound.fromUserName}`,
  );

  // ---- subscribe 欢迎语 ----
  // 用户关注时，如果配了 autoReply.welcomeText 模板，下发欢迎语。
  if (inbound.msgType === "event" && inbound.event === "subscribe") {
    const coreForWelcome = selected.core ?? tryGetWechatServiceRuntime();
    if (coreForWelcome) {
      const cfg = coreForWelcome.config.loadConfig();
      const welcomeText = renderWelcomeText(cfg, undefined);
      if (welcomeText) {
        void sendCustomerServiceMessage({
          account: selected.account,
          tokenHandle: accessTokenHandleFor(selected.account),
          message: {
            touser: inbound.fromUserName,
            msgtype: "text",
            text: { content: welcomeText },
          },
        }).catch((err) => {
          selected.runtime.error?.(
            `[wechat-service] welcome_send_failed reqId=${reqId} accountId=${selected.account.accountId}: ${err instanceof Error ? err.message : String(err)}`,
          );
        });
      }
    }
  }

  void (async () => {
    const core = selected.core ?? tryGetWechatServiceRuntime();
    if (!core) {
      selected.runtime.error?.(
        `[wechat-service] agent_dispatch_skipped reqId=${reqId} accountId=${selected.account.accountId} reason=core-runtime-missing`,
      );
      return;
    }
    const cfg = core.config.loadConfig();

    // ---- 菜单点击 / 扫码 / 位置上报 等"被动事件"短路 ----
    // 默认不把这些事件丢给 LLM agent 回应（用户的诉求："点击底部菜单不要回复"）。
    // 仅当显式配置了 routing.events.<eventKey> = "<agentId>" 时才走 agent，
    // 让运营能针对具体菜单 key 做"按钮触发剧本"——不配=安静收下，不打扰粉丝。
    //
    // 不影响：
    //  - subscribe 欢迎语（上面 sendCustomerServiceMessage 已发）
    //  - 用户文本/图片/语音/视频/位置消息（这些 msgType !== "event"）
    if (inbound.msgType === "event") {
      const routedAgent = resolveEventRoutingAgentId({
        inbound,
        routing: selected.account.routing,
      });
      if (!routedAgent) {
        selected.runtime.log?.(
          `[wechat-service] event_short_circuit reqId=${reqId} accountId=${selected.account.accountId} event=${inbound.event ?? "unknown"} (no routing.events.<key> configured → not dispatching to agent)`,
        );
        return;
      }
    }

    // ---- 自动回复（关键词 / 业务时间） ----
    const autoReplyResult = checkAutoReply(cfg, inbound);
    if (autoReplyResult.handled) {
      try {
        await sendCustomerServiceMessage({
          account: selected.account,
          tokenHandle: accessTokenHandleFor(selected.account),
          message: {
            touser: inbound.fromUserName,
            msgtype: "text",
            text: { content: autoReplyResult.reply },
          },
        });
        selected.runtime.log?.(
          `[wechat-service] auto_reply reqId=${reqId} accountId=${selected.account.accountId} from=${inbound.fromUserName} length=${autoReplyResult.reply.length}`,
        );
      } catch (err) {
        selected.runtime.error?.(
          `[wechat-service] auto_reply_send_failed reqId=${reqId} accountId=${selected.account.accountId}: ${err instanceof Error ? err.message : String(err)}`,
        );
      }
      return;
    }

    await runAgentDispatch({
      core,
      cfg,
      account: selected.account,
      event,
    });
  })();

  return true;
}

async function runAgentDispatch(params: {
  core: PluginRuntime;
  cfg: OpenClawConfig;
  account: ResolvedWechatServiceAccount;
  event: ReturnType<typeof buildUnifiedInboundEvent>;
}): Promise<void> {
  try {
    await dispatchInboundEvent({
      core: params.core,
      cfg: params.cfg,
      account: params.account,
      event: params.event,
    });
  } catch (err) {
    console.error(
      `[wechat-service] agent_dispatch_error accountId=${params.account.accountId}: ${err instanceof Error ? err.message : String(err)}`,
    );
  }
}

void (undefined as unknown as WechatServiceConfig | undefined);
