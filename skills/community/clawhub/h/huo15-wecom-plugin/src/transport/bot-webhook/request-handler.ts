import type { IncomingMessage, ServerResponse } from "node:http";

import { getWecomRuntime } from "../../runtime.js";
import { decryptWecomEncrypted, verifyWecomSignature } from "../../crypto.js";
import { resolveWecomEgressProxyUrl } from "../../config/index.js";
import { LIMITS, type StreamStore } from "../../monitor/state.js";
import type { StartBotAgentStreamParams } from "../../capability/bot/stream-orchestrator.js";
import type { WecomBotInboundMessage as WecomInboundMessage } from "../../types/index.js";
import type { WecomRuntimeAuditEvent, WecomWebhookTarget } from "../../types/runtime-context.js";
import { wecomFetch } from "../../http.js";
import {
  logRouteFailure,
  resolveQueryParams,
  resolveSignatureParam,
  type RouteFailureReason,
  writeRouteFailure,
} from "../http/common.js";
import {
  buildEncryptedBotWebhookReply,
  buildStreamPlaceholderReply,
  buildStreamReplyFromState,
  buildStreamTextPlaceholderReply,
  jsonOk,
  parseWecomPlainMessage,
  readBotWebhookJsonBody,
  resolveBotIdentitySet,
} from "./protocol.js";
import { storeActiveReply } from "./active-reply.js";
import { buildInboundBody, resolveWecomSenderUserId, shouldProcessBotInboundMessage } from "./message-shape.js";

const ERROR_HELP = "\n\n遇到问题？联系作者: YanHaidao (微信: YanHaidao)";

type RecordBotOperationalEvent = (
  target: Pick<WecomWebhookTarget, "account" | "auditSink">,
  event: Omit<WecomRuntimeAuditEvent, "transport">,
) => void;

export function createBotWebhookRequestHandler(params: {
  streamStore: StreamStore;
  logInfo: (target: WecomWebhookTarget, message: string) => void;
  logVerbose: (target: WecomWebhookTarget, message: string) => void;
  recordBotOperationalEvent: RecordBotOperationalEvent;
  startAgentForStream: (params: StartBotAgentStreamParams) => Promise<void>;
}) {
  const { streamStore, logInfo, logVerbose, recordBotOperationalEvent, startAgentForStream } = params;

  return async function handleBotWebhookRequest(args: {
    req: IncomingMessage;
    res: ServerResponse;
    path: string;
    reqId: string;
    targets: WecomWebhookTarget[];
  }): Promise<boolean> {
    const { req, res, path, reqId, targets } = args;
    const query = resolveQueryParams(req);
    const timestamp = query.get("timestamp") ?? "";
    const nonce = query.get("nonce") ?? "";
    const signature = resolveSignatureParam(query);

    if (req.method === "GET") {
      const echostr = query.get("echostr") ?? "";
      const signatureMatches = targets.filter(
        (target) =>
          target.account.token &&
          verifyWecomSignature({ token: target.account.token, timestamp, nonce, encrypt: echostr, signature }),
      );
      if (signatureMatches.length !== 1) {
        const reason: RouteFailureReason =
          signatureMatches.length === 0 ? "wecom_account_not_found" : "wecom_account_conflict";
        const candidateIds = (signatureMatches.length > 0 ? signatureMatches : targets).map((target) => target.account.accountId);
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
            ? "Bot callback account conflict: multiple accounts matched signature."
            : "Bot callback account not found: signature verification failed.",
        );
        return true;
      }
      const target = signatureMatches[0]!;
      try {
        const plain = decryptWecomEncrypted({
          encodingAESKey: target.account.encodingAESKey,
          receiveId: target.account.receiveId,
          encrypt: echostr,
        });
        res.statusCode = 200;
        res.setHeader("Content-Type", "text/plain; charset=utf-8");
        res.end(plain);
        return true;
      } catch (err) {
        res.statusCode = 400;
        res.setHeader("Content-Type", "text/plain; charset=utf-8");
        res.end(`decrypt failed - 解密失败，请检查 EncodingAESKey${ERROR_HELP}`);
        return true;
      }
    }

    if (req.method !== "POST") return false;

    const body = await readBotWebhookJsonBody(req, 1024 * 1024);
    if (!body.ok) {
      res.statusCode = 400;
      res.end(body.error || "invalid payload");
      return true;
    }
    const record = body.value as any;
    const encrypt = String(record?.encrypt ?? record?.Encrypt ?? "");
    console.log(
      `[wecom] inbound(bot): reqId=${reqId} rawJsonBytes=${Buffer.byteLength(JSON.stringify(record), "utf8")} hasEncrypt=${Boolean(encrypt)} encryptLen=${encrypt.length}`,
    );
    const signatureMatches = targets.filter(
      (target) =>
        target.account.token && verifyWecomSignature({ token: target.account.token, timestamp, nonce, encrypt, signature }),
    );
    if (signatureMatches.length !== 1) {
      const reason: RouteFailureReason =
        signatureMatches.length === 0 ? "wecom_account_not_found" : "wecom_account_conflict";
      const candidateIds = (signatureMatches.length > 0 ? signatureMatches : targets).map((target) => target.account.accountId);
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
          ? "Bot callback account conflict: multiple accounts matched signature."
          : "Bot callback account not found: signature verification failed.",
      );
      return true;
    }

    const target = signatureMatches[0]!;
    let msg: WecomInboundMessage;
    try {
      const plain = decryptWecomEncrypted({
        encodingAESKey: target.account.encodingAESKey,
        receiveId: target.account.receiveId,
        encrypt,
      });
      msg = parseWecomPlainMessage(plain);
    } catch {
      res.statusCode = 400;
      res.setHeader("Content-Type", "text/plain; charset=utf-8");
      res.end(`decrypt failed - 解密失败，请检查 EncodingAESKey${ERROR_HELP}`);
      return true;
    }

    const expected = resolveBotIdentitySet(target);
    if (expected.size > 0) {
      const inboundAibotId = String((msg as any).aibotid ?? "").trim();
      if (!inboundAibotId || !expected.has(inboundAibotId)) {
        target.runtime.error?.(
          `[wecom] inbound(bot): reqId=${reqId} accountId=${target.account.accountId} aibotid_mismatch expected=${Array.from(expected).join(",")} actual=${inboundAibotId || "N/A"}`,
        );
      }
    }

    logInfo(target, `inbound(bot): reqId=${reqId} selectedAccount=${target.account.accountId} path=${path}`);
    target.touchTransportSession?.({ lastInboundAt: Date.now(), running: true });
    const msgtype = String(msg.msgtype ?? "").toLowerCase();
    const proxyUrl = resolveWecomEgressProxyUrl(target.config);

    if (msgtype === "event") {
      const eventtype = String((msg as any).event?.eventtype ?? "").toLowerCase();

      if (eventtype === "template_card_event") {
        const msgid = msg.msgid ? String(msg.msgid) : undefined;
        if (msgid && streamStore.getStreamByMsgId(msgid)) {
          logVerbose(target, `template_card_event: already processed msgid=${msgid}, skipping`);
          recordBotOperationalEvent(target, {
            category: "duplicate-reply",
            messageId: msgid,
            summary: `duplicate template card event msgid=${msgid}`,
            raw: {
              transport: "bot-webhook",
              envelopeType: "json",
              body: msg,
            },
          });
          jsonOk(res, buildEncryptedBotWebhookReply({ account: target.account, plaintextJson: {}, nonce, timestamp }));
          return true;
        }

        const cardEvent = (msg as any).event?.template_card_event;
        let interactionDesc = `[卡片交互] 按钮: ${cardEvent?.event_key || "unknown"}`;
        if (cardEvent?.selected_items?.selected_item?.length) {
          const selects = cardEvent.selected_items.selected_item.map(
            (i: any) => `${i.question_key}=${i.option_ids?.option_id?.join(",")}`,
          );
          interactionDesc += ` 选择: ${selects.join("; ")}`;
        }
        if (cardEvent?.task_id) interactionDesc += ` (任务ID: ${cardEvent.task_id})`;

        jsonOk(res, buildEncryptedBotWebhookReply({ account: target.account, plaintextJson: {}, nonce, timestamp }));

        const streamId = streamStore.createStream({ msgid });
        streamStore.markStarted(streamId);
        storeActiveReply(streamId, msg.response_url);
        const core = getWecomRuntime();
        startAgentForStream({
          target: { ...target, core },
          accountId: target.account.accountId,
          msg: { ...msg, msgtype: "text", text: { content: interactionDesc } } as any,
          streamId,
        }).catch((err) => target.runtime.error?.(`interaction failed: ${String(err)}`));
        return true;
      }

      if (eventtype === "enter_chat") {
        const welcome = target.account.config.welcomeText?.trim();
        jsonOk(
          res,
          buildEncryptedBotWebhookReply({
            account: target.account,
            plaintextJson: welcome ? { msgtype: "text", text: { content: welcome } } : {},
            nonce,
            timestamp,
          }),
        );
        return true;
      }

      jsonOk(res, buildEncryptedBotWebhookReply({ account: target.account, plaintextJson: {}, nonce, timestamp }));
      return true;
    }

    if (msgtype === "stream") {
      const streamId = String((msg as any).stream?.id ?? "").trim();
      const state = streamStore.getStream(streamId);
      const reply = state
        ? buildStreamReplyFromState(state)
        : buildStreamReplyFromState({
            streamId: streamId || "unknown",
            createdAt: Date.now(),
            updatedAt: Date.now(),
            started: true,
            finished: true,
            content: "",
          });
      jsonOk(res, buildEncryptedBotWebhookReply({ account: target.account, plaintextJson: reply, nonce, timestamp }));
      return true;
    }

    try {
      const decision = shouldProcessBotInboundMessage(msg);
      if (!decision.shouldProcess) {
        logInfo(
          target,
          `inbound: skipped msgtype=${msgtype} reason=${decision.reason} chattype=${String(msg.chattype ?? "")} chatid=${String(msg.chatid ?? "")} from=${resolveWecomSenderUserId(msg) || "N/A"}`,
        );
        jsonOk(res, buildEncryptedBotWebhookReply({ account: target.account, plaintextJson: {}, nonce, timestamp }));
        return true;
      }

      const userid = decision.senderUserId!;
      const chatId = decision.chatId ?? userid;
      const conversationKey = `wecom:${target.account.accountId}:${userid}:${chatId}`;
      const msgContent = buildInboundBody(msg);

      logInfo(
        target,
        `inbound: msgtype=${msgtype} chattype=${String(msg.chattype ?? "")} chatid=${String(msg.chatid ?? "")} from=${userid} msgid=${String(msg.msgid ?? "")} hasResponseUrl=${Boolean((msg as any).response_url)}`,
      );

      if (msg.msgid) {
        const existingStreamId = streamStore.getStreamByMsgId(String(msg.msgid));
        if (existingStreamId) {
          logInfo(target, `message: 重复的 msgid=${msg.msgid}，跳过处理并返回占位符 streamId=${existingStreamId}`);
          recordBotOperationalEvent(target, {
            category: "duplicate-reply",
            messageId: String(msg.msgid),
            summary: `duplicate inbound msgid=${String(msg.msgid)} streamId=${existingStreamId}`,
            raw: {
              transport: "bot-webhook",
              envelopeType: "json",
              body: msg,
            },
          });
          jsonOk(
            res,
            buildEncryptedBotWebhookReply({
              account: target.account,
              plaintextJson: buildStreamPlaceholderReply({
                streamId: existingStreamId,
                placeholderContent: target.account.config.streamPlaceholderContent,
              }),
              nonce,
              timestamp,
            }),
          );
          return true;
        }
      }

      const { streamId, status } = streamStore.addPendingMessage({
        conversationKey,
        target,
        msg,
        msgContent,
        nonce,
        timestamp,
        debounceMs: (target.account.config as any).debounceMs,
      });

      if (msg.response_url) {
        storeActiveReply(streamId, msg.response_url, proxyUrl);
      }

      const defaultPlaceholder = target.account.config.streamPlaceholderContent;
      const queuedPlaceholder = "已收到，已排队处理中...";
      const mergedQueuedPlaceholder = "已收到，已合并排队处理中...";

      if (status === "active_new") {
        jsonOk(
          res,
          buildEncryptedBotWebhookReply({
            account: target.account,
            plaintextJson: buildStreamPlaceholderReply({
              streamId,
              placeholderContent: defaultPlaceholder,
            }),
            nonce,
            timestamp,
          }),
        );
        return true;
      }

      if (status === "queued_new") {
        logInfo(target, `queue: 已进入下一批次 streamId=${streamId} msgid=${String(msg.msgid ?? "")}`);
        jsonOk(
          res,
          buildEncryptedBotWebhookReply({
            account: target.account,
            plaintextJson: buildStreamPlaceholderReply({
              streamId,
              placeholderContent: queuedPlaceholder,
            }),
            nonce,
            timestamp,
          }),
        );
        return true;
      }

      const ackStreamId = streamStore.createStream({ msgid: String(msg.msgid ?? "") || undefined });
      streamStore.updateStream(ackStreamId, (s) => {
        s.finished = false;
        s.started = true;
        s.content = mergedQueuedPlaceholder;
      });
      if (msg.msgid) streamStore.setStreamIdForMsgId(String(msg.msgid), ackStreamId);
      streamStore.addAckStreamForBatch({ batchStreamId: streamId, ackStreamId });
      logInfo(
        target,
        `queue: 已合并排队（回执流） ackStreamId=${ackStreamId} mergedIntoStreamId=${streamId} msgid=${String(msg.msgid ?? "")}`,
      );
      jsonOk(
        res,
        buildEncryptedBotWebhookReply({
          account: target.account,
          plaintextJson: buildStreamTextPlaceholderReply({ streamId: ackStreamId, content: mergedQueuedPlaceholder }),
          nonce,
          timestamp,
        }),
      );
      return true;
    } catch (err) {
      target.runtime.error?.(`[wecom] Bot message handler crashed: ${String(err)}`);
      jsonOk(
        res,
        buildEncryptedBotWebhookReply({
          account: target.account,
          plaintextJson: { msgtype: "text", text: { content: "服务内部错误：Bot 处理异常，请稍后重试。" } },
          nonce,
          timestamp,
        }),
      );
      return true;
    }
  };
}
