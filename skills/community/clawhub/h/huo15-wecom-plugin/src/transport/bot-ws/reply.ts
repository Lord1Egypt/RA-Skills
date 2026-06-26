import {
  generateReqId,
  type WsFrame,
  type BaseMessage,
  type EventMessage,
  type WSClient,
} from "@wecom/aibot-node-sdk";
import { formatErrorMessage } from "openclaw/plugin-sdk/infra-runtime";
import { resolveWecomMediaMaxBytes, resolveWecomMergedMediaLocalRoots } from "../../config/index.js";
import { extractMediaDirectives } from "../../outbound.js";
import { getAccountRuntime, getWecomRuntime } from "../../runtime.js";
import type { ReplyHandle, ReplyPayload } from "../../types/index.js";
import type { WecomProgressMode } from "../../types/config.js";
import { toWeComMarkdownV2 } from "../../wecom_msg_adapter/markdown_adapter.js";
import { uploadAndReplyBotWsMedia } from "./media.js";
import { sendAgentApiText } from "../agent-api/client.js";

const PLACEHOLDER_KEEPALIVE_MS = 3000;
const MAX_KEEPALIVE_MS = 120 * 1000; // Force stop keepalive after 120s if ignored
const DEFAULT_PROGRESS_MODE: WecomProgressMode = "progress";
const DEFAULT_PROGRESS_DELAYED_MS = 30_000;
const HEARTBEAT_DEFAULT_TEXT = "⏳ 正在思考中...\n\n";

// v2.8.17 ⭐ 阶段化 placeholder 文案（progressMode="progress"）
function buildProgressPlaceholder(elapsedMs: number): string {
  if (elapsedMs < 30_000) {
    return "⏳ 正在思考中...\n\n";
  }
  if (elapsedMs < 60_000) {
    const sec = Math.floor(elapsedMs / 1000);
    return `⏳ 仍在处理中（已 ${sec}s）...\n\n`;
  }
  if (elapsedMs < 120_000) {
    const min = Math.floor(elapsedMs / 60_000);
    return `⏳ 任务较复杂（已 ${min}m），请稍候...\n\n`;
  }
  const min = Math.floor(elapsedMs / 60_000);
  return `⏳ 任务仍在执行（已 ${min}m+），完成后会主动推送结果。\n\n`;
}
// v2.8.5 ⭐ partial streaming cap — limit fire-and-forget partial replyStream calls to
// avoid SDK reply queue saturation (each pending partial waits ~5s for WS ack).
// Excess block chunks are silently accumulated and flushed in the final reply.
const MAX_PARTIAL_REPLIES = 8;

// ── WS Health Watchdog ──
// Per-account counter of consecutive ack timeouts within a rolling window.
// When threshold is exceeded, triggers a callback (e.g. WS reconnect).
interface AckTimeoutWatchdog {
  accountId: string;
  count: number;
  firstHitAt: number;
  timer?: ReturnType<typeof setTimeout>;
}
const ACK_TIMEOUT_WARNING_THRESHOLD = 5;  // consecutive timeouts before warning
const ACK_TIMEOUT_RECONNECT_THRESHOLD = 8; // consecutive timeouts before call reconnect
const ACK_TIMEOUT_WINDOW_MS = 120_000;     // reset counter if no hits within 2 min

const ackWatchdogs = new Map<string, AckTimeoutWatchdog>();

function hitAckTimeoutWatchdog(params: {
  accountId: string;
  onReconnectNeeded?: (accountId: string) => void;
}): void {
  const key = params.accountId;
  const now = Date.now();
  let wd = ackWatchdogs.get(key);
  if (!wd || now - wd.firstHitAt > ACK_TIMEOUT_WINDOW_MS) {
    wd = { accountId: key, count: 0, firstHitAt: now };
    ackWatchdogs.set(key, wd);
  }
  wd.count += 1;

  // Reset timer: clear counter if no more timeouts within the window
  if (wd.timer) clearTimeout(wd.timer);
  wd.timer = setTimeout(() => {
    ackWatchdogs.delete(key);
  }, ACK_TIMEOUT_WINDOW_MS);

  if (wd.count >= ACK_TIMEOUT_RECONNECT_THRESHOLD) {
    console.warn(
      `[wecom-ws] watchdog: ${wd.count} consecutive ack timeouts for account=${key}, triggering reconnect`,
    );
    ackWatchdogs.delete(key); // reset after firing
    params.onReconnectNeeded?.(key);
  } else if (wd.count >= ACK_TIMEOUT_WARNING_THRESHOLD) {
    console.warn(
      `[wecom-ws] watchdog: ${wd.count} ack timeouts within window for account=${key} (threshold=${ACK_TIMEOUT_RECONNECT_THRESHOLD})`,
    );
  }
}

function isInvalidReqIdError(error: unknown): boolean {
  if (!error || typeof error !== "object") {
    return false;
  }
  const errcode = "errcode" in error ? Number(error.errcode) : undefined;
  const errmsg = "errmsg" in error ? String(error.errmsg ?? "") : "";
  return errcode === 846605 || errmsg.includes("invalid req_id");
}

function isExpiredStreamUpdateError(error: unknown): boolean {
  if (!error || typeof error !== "object") {
    return false;
  }
  const errcode = "errcode" in error ? Number(error.errcode) : undefined;
  const errmsg = "errmsg" in error ? String(error.errmsg ?? "").toLowerCase() : "";
  return errcode === 846608 || errmsg.includes("stream message update expired");
}

/** SDK rejects with a plain Error whose message contains "ack timeout" when
 * the WeCom server does not acknowledge a reply within 5 s.  Once timed out
 * the reqId slot is released; further replies on the same reqId will fail. */
function isAckTimeoutError(error: unknown): boolean {
  return error instanceof Error && error.message.includes("ack timeout");
}

function isTerminalReplyError(error: unknown): boolean {
  return (
    isInvalidReqIdError(error) || isExpiredStreamUpdateError(error) || isAckTimeoutError(error)
  );
}

function formatMediaFailure(mediaUrl: string, error?: string, rejectReason?: string): string {
  const reason = rejectReason || error || "unknown";
  return `媒体发送失败：${mediaUrl} (${reason})`;
}

// Global registry to track active keepalives by peerId
interface ActiveKeepalive {
  reqId: string;
  stop: () => void;
}
const activeKeepalivesByPeer = new Map<string, Set<ActiveKeepalive>>();

export function createBotWsReplyHandle(params: {
  client: WSClient;
  frame: WsFrame<BaseMessage | EventMessage>;
  accountId: string;
  inboundKind: string;
  placeholderContent?: string;
  autoSendPlaceholder?: boolean;
  /**
   * v2.8.17+ 长任务进度反馈模式。默认 "progress"。
   */
  progressMode?: WecomProgressMode;
  /**
   * v2.8.17+ progressMode="delayed" 时的沉默时长（毫秒）。默认 30000。
   */
  progressDelayedMs?: number;
  onDeliver?: () => void;
  onFail?: (error: unknown) => void;
  onReconnectNeeded?: (accountId: string) => void;
}): ReplyHandle {
  let streamId: string | undefined;
  // v2.8.26 ⭐ 跟踪 streamId 是否已被 last=true 终结（如 v2.8.24 placeholder timeout
  // finalize 路径）。一旦终结，企微 server 不再让同 streamId 更新内容。下次 deliver
  // 时必须用**新 streamId 重启流**。
  let streamFinalized = false;
  // v2.8.30 ⭐ 跟踪 streamId 创建时间。企微 stream 协议有"10 分钟过期窗口"——同 streamId
  // 距首次创建超过 10 min 后再 partial 更新会撞 errcode=846608 "stream message update
  // expired"。长任务（subagent / 异步 tool）+ notifyPeerActive 停掉本 reply handle 的
  // placeholder timeout（其他 reply 触发的 stop）→ streamFinalized 永远不被设置 →
  // 后续 deliver block 用旧 streamId → 撞 846608。
  // 修法：resolveStreamId 检测 streamId 已用 9 分钟（10 分钟过期前）主动 rotate 新 streamId。
  let streamStartedAt = 0;
  const STREAM_MAX_AGE_MS = 9 * 60 * 1000; // 9 分钟（企微 10 分钟过期前重启）
  let accumulatedText = "";
  let deferredMediaUrls: string[] = [];
  const resolveStreamId = () => {
    const now = Date.now();
    if (streamFinalized) {
      // v2.8.26：旧流已 last=true 终结，开新流
      streamId = generateReqId("stream-restart");
      streamStartedAt = now;
      streamFinalized = false;
      console.log(
        `[wecom-ws] streamId 已终结 → 重启新 streamId=${streamId}（v2.8.26 修 placeholder finalize 后内容静默丢失）`,
      );
    } else if (streamId && now - streamStartedAt > STREAM_MAX_AGE_MS) {
      // v2.8.30 ⭐ 主动 rotate：旧 streamId 接近 10 分钟过期窗口，提前换新避免 846608
      const oldStreamId = streamId;
      const ageMs = now - streamStartedAt;
      streamId = generateReqId("stream-rotate");
      streamStartedAt = now;
      console.log(
        `[wecom-ws] streamId 已用 ${Math.round(ageMs / 1000)}s（>9min）接近企微 10min 过期 → 主动 rotate ${oldStreamId} → ${streamId}（v2.8.30 修长任务 846608）`,
      );
    }
    if (!streamId) {
      streamId = generateReqId("stream");
      streamStartedAt = now;
    }
    return streamId;
  };

  // v2.8.17 ⭐ progressMode 决定 placeholder 文案策略
  const progressMode: WecomProgressMode = params.progressMode ?? DEFAULT_PROGRESS_MODE;
  const progressDelayedMs = Math.max(
    0,
    params.progressDelayedMs ?? DEFAULT_PROGRESS_DELAYED_MS,
  );
  // 显式 placeholderContent 覆盖优先级最高（兼容老 config）；否则用 heartbeat 默认
  const overridePlaceholderText = params.placeholderContent?.trim();
  const startedAt = Date.now();
  const computeCurrentPlaceholder = (): string => {
    if (overridePlaceholderText) return overridePlaceholderText;
    if (progressMode === "progress") {
      return buildProgressPlaceholder(Date.now() - startedAt);
    }
    return HEARTBEAT_DEFAULT_TEXT;
  };

  let streamSettled = false;
  let placeholderInFlight = false;
  let placeholderKeepalive: ReturnType<typeof setInterval> | undefined;
  let placeholderTimeout: ReturnType<typeof setTimeout> | undefined;
  // v2.8.5 ⭐ count of fire-and-forget partial replyStream calls; capped at MAX_PARTIAL_REPLIES
  let partialReplyCount = 0;

  // Extract peerId for clustering handles
  const body = params.frame.body as any;
  const peerId = String(
    (body?.chattype === "group" ? body?.chatid || body?.from?.userid : body?.from?.userid) ||
      "unknown",
  );
  const peerKind: "direct" | "group" =
    body?.chattype === "group" ? "group" : "direct";
  const reqId = params.frame.headers.req_id || "unknown";

  const isEvent =
    params.inboundKind === "welcome" ||
    params.inboundKind === "event" ||
    params.inboundKind === "template-card-event";

  const stopPlaceholderKeepalive = () => {
    if (placeholderKeepalive) {
      clearInterval(placeholderKeepalive);
      placeholderKeepalive = undefined;
    }
    if (placeholderTimeout) {
      clearTimeout(placeholderTimeout);
      placeholderTimeout = undefined;
    }

    // Remove from registry
    const keepalives = activeKeepalivesByPeer.get(peerId);
    if (keepalives) {
      for (const ka of keepalives) {
        if (ka.reqId === reqId) {
          keepalives.delete(ka);
        }
      }
      if (keepalives.size === 0) {
        activeKeepalivesByPeer.delete(peerId);
      }
    }
  };

  const settleStream = () => {
    if (streamSettled) return;
    streamSettled = true;
    stopPlaceholderKeepalive();
  };

  /**
   * v2.8.28 抽 helper / v2.8.29 ⭐ regression 修复：finalize 用 accumulatedText 而不是 placeholder
   *
   * 通用"立刻终结当前 stream"helper —— 用 last=true 标记 streamId 让企微 client UI
   * 解锁交互（"内容由AI生成" 标识 + 可复制 / 可点链接）。
   *
   * **v2.8.29 修 regression**：v2.8.27/v2.8.28 当时用 `computeCurrentPlaceholder()` 文案
   * （"正在思考..."）作为 last=true 终结内容——但**企微流式协议中 last=true 帧会完全
   * 替换之前 partial 推的所有内容**。导致 LLM 实际输出过 block textLen=582 完整回复，
   * 但 final 来时被 finalize 用"正在思考..."覆盖→ 用户只看到 placeholder！
   *
   * 修法：优先用 accumulatedText（保留之前 block partial 已推的内容），
   * 仅当 accumulatedText 为空（dispatch 极速 done 没产出）时才用 placeholder 文案。
   *
   * 触发场景：
   * - final 完全空内容 + accumulatedText 空：dispatch 极速 done → 用 placeholder 终结
   * - final 完全空内容 + accumulatedText 有：LLM 推过 block 但 final 空 → 用 accumulatedText 终结
   *   （这是常见路径——OpenClaw core 把内容放 block，final 只是结束信号）
   */
  const finalizeStreamIfNeeded = async (reason: string): Promise<void> => {
    if (streamSettled || isEvent || !streamId) return;
    try {
      // v2.8.29 ⭐ 关键修复：优先用 accumulatedText 而不是 placeholder
      // 否则覆盖 block 完整回复内容
      const settleText = accumulatedText
        ? toWeComMarkdownV2(accumulatedText)
        : computeCurrentPlaceholder();
      const settleSource = accumulatedText ? "accumulatedText" : "placeholder";
      await params.client.replyStream(
        params.frame,
        streamId,
        settleText,
        true, // ← last=true 终结
      );
      streamSettled = true;
      streamFinalized = true;
      stopPlaceholderKeepalive();
      console.log(
        `[wecom-ws] finalizeStreamIfNeeded(${reason}): 用 last=true 终结 streamId=${streamId} 解锁企微 UI（peer=${peerKind}:${peerId}, source=${settleSource}, len=${settleText.length}）`,
      );
    } catch (e) {
      // ack timeout / reqId 失效—— 不致命，placeholder timeout 会 120s 后兜底
      console.warn(
        `[wecom-ws] finalizeStreamIfNeeded(${reason}) 失败（${e instanceof Error ? e.message : String(e)}）— 等 placeholder timeout 兜底`,
      );
    }
  };

  const sendPlaceholder = () => {
    if (streamSettled || placeholderInFlight || isEvent) return;
    if (progressMode === "off") return;
    placeholderInFlight = true;
    params.client
      .replyStream(params.frame, resolveStreamId(), computeCurrentPlaceholder(), false)
      .catch((error) => {
        if (!isTerminalReplyError(error)) {
          return;
        }
        settleStream();
        params.onFail?.(error);
      })
      .finally(() => {
        placeholderInFlight = false;
      });
  };

  const notifyPeerActive = () => {
    // A genuine reply or reasoning is happening on THIS handle.
    // It means the core SDK has chosen this handle to deliver the response.
    // We can safely terminate all other orphaned keepalives for this peer to prevent infinite loops.
    const keepalives = activeKeepalivesByPeer.get(peerId);
    if (keepalives) {
      for (const ka of keepalives) {
        if (ka.reqId !== reqId) {
          ka.stop();
        }
      }
    }
  };

  const mergeDeferredMediaUrls = (urls: string[]): string[] => {
    if (urls.length === 0) {
      return deferredMediaUrls;
    }
    const merged = [...deferredMediaUrls];
    for (const url of urls) {
      if (!merged.includes(url)) {
        merged.push(url);
      }
    }
    deferredMediaUrls = merged;
    return deferredMediaUrls;
  };

  /**
   * Fallback delivery via Agent API when WS delivery fails or WS is disconnected.
   * This ensures replies are still delivered even after gateway restart or WS reconnect.
   */
  const fallbackAgentApiDelivery = async (text: string): Promise<void> => {
    const accountRuntime = getAccountRuntime(params.accountId);
    const agent = accountRuntime?.account.agent;
    if (!agent?.apiConfigured) {
      console.warn(
        `[wecom-ws] fallback: no agent API config for account=${params.accountId}, cannot deliver text fallback`,
      );
      return;
    }
    try {
      if (peerKind === "group") {
        await sendAgentApiText({ agent, chatId: peerId, text });
      } else {
        await sendAgentApiText({ agent, toUser: peerId, text });
      }
      console.log(
        `[wecom-ws] fallback: delivered text via Agent API to ${peerKind}=${peerId}`,
      );
    } catch (err) {
      console.error(
        `[wecom-ws] fallback: Agent API delivery failed for ${peerKind}=${peerId}: ${err instanceof Error ? err.message : String(err)}`,
      );
      throw err;
    }
  };

  if (params.autoSendPlaceholder !== false && !isEvent && progressMode !== "off") {
    if (progressMode === "delayed") {
      // v2.8.17 ⭐ "delayed" 模式：默认沉默；progressDelayedMs 之后单次发，不循环
      placeholderTimeout = setTimeout(() => {
        sendPlaceholder();
        placeholderTimeout = undefined;
      }, progressDelayedMs);
    } else {
      // "progress" / "heartbeat" 模式：立即发 + 每 PLACEHOLDER_KEEPALIVE_MS 重发
      sendPlaceholder();
      placeholderKeepalive = setInterval(() => {
        sendPlaceholder();
      }, PLACEHOLDER_KEEPALIVE_MS);

      // Safety net: force stop keepalive after MAX_KEEPALIVE_MS
      // in case the message is completely ignored by the core and never triggers deliver/fail
      placeholderTimeout = setTimeout(async () => {
        // v2.8.24 ⭐ 关键修复：120s 触发时用 last=true 终结当前 stream，让企微 UI 解锁
        // 交互（"内容由AI生成"标识 + 可复制 / 可点链接）。之前只 stopKeepalive 不发
        // last=true，streamId 永远停在最后一帧 last=false，企微 client 一直显示
        // "AI 生成中..." 锁交互，用户长任务（reasoning / 工具链长 > 120s）时常报
        // "复制不了消息"。修法：用最终档 placeholder 文案标 last=true（"任务仍在
        // 执行（已 2m+），完成后会主动推送结果"），企微 UI 立刻解锁。
        if (!streamSettled && !isEvent && streamId) {
          const finalPlaceholderText =
            progressMode === "progress"
              ? buildProgressPlaceholder(Date.now() - startedAt)
              : computeCurrentPlaceholder();
          try {
            await params.client.replyStream(
              params.frame,
              streamId,
              finalPlaceholderText,
              true, // ← 关键：last=true 终结 stream
            );
            streamSettled = true;
            // v2.8.26 ⭐ 标记 streamId 已终结。下次 resolveStreamId() 会自动开新 streamId。
            // 之前 v2.8.24 只设 streamSettled，但 deliver 路径 resolveStreamId 仍返回旧
            // streamId（已 finalize），后续 replyStream 调用企微 server ack 但 client UI
            // 不更新——final 内容静默丢失。
            streamFinalized = true;
            console.log(
              `[wecom-ws] placeholder timeout 120s: streamId=${streamId} 已用 last=true 终结 + 标记 streamFinalized，企微 UI 解锁交互（peer=${peerKind}:${peerId}, mode=${progressMode}）`,
            );
          } catch (e) {
            // 终结失败（reqId 失效 / 流已过期 / WS 断）—— 不致命
            // 企微 client 长 idle 后自己会解锁；后续 deliver 真 final 时也可能
            // 再尝试一次 last=true（如果 streamId 仍有效）
            console.warn(
              `[wecom-ws] placeholder timeout finalize 失败（${e instanceof Error ? e.message : String(e)}）— 企微 UI 会等长 idle 自己解锁`,
            );
          }
        } else if (progressMode === "progress" && !streamSettled) {
          // 兼容老路径：streamId 还没生成（极小概率）→ 走原行为发 placeholder
          sendPlaceholder();
        }
        stopPlaceholderKeepalive();
      }, MAX_KEEPALIVE_MS);
    }

    // Register keepalive
    let keepalives = activeKeepalivesByPeer.get(peerId);
    if (!keepalives) {
      keepalives = new Set();
      activeKeepalivesByPeer.set(peerId, keepalives);
    }
    keepalives.add({ reqId, stop: stopPlaceholderKeepalive });
  }

  return {
    context: {
      transport: "bot-ws",
      accountId: params.accountId,
      reqId: params.frame.headers.req_id,
      peerId,
      peerKind,
      raw: {
        transport: "bot-ws",
        command: params.frame.cmd,
        headers: params.frame.headers,
        body: params.frame.body,
        envelopeType: "ws",
      },
    },
    deliver: async (payload: ReplyPayload, info) => {
      // Mark this chat as active on this handle
      notifyPeerActive();

      if (payload.isReasoning) {
        // We reset the safety timeout if reasoning is actively streaming
        if (placeholderTimeout && !isEvent) {
          clearTimeout(placeholderTimeout);
          placeholderTimeout = setTimeout(() => {
            stopPlaceholderKeepalive();
          }, MAX_KEEPALIVE_MS);
        }
        return;
      }

      // v2.8.20 ⭐ 解析 LLM emit 的 "MEDIA: <path>" 单行指令（与 outbound.sendText 同源）。
      // index.ts 的 WECOM_BOT_WS_MEDIA_GUIDANCE 通过 system context 引导 LLM 用 MEDIA: 行
      // 发文件，但 v2.8.19 只修了 outbound.sendText 路径——bot-ws reply.ts 是入站消息的"被动
      // 回复"通道（reqId 绑定，群聊里 @机器人触发），用户实测群里 emit MEDIA: 仍然没收到
      // 文件。本版在 reply 路径同样接管：抽出 mediaPaths 合并到 incomingMediaUrls，让现有
      // mediaUrls handling（uploadAndReplyBotWsMedia 走 aibot_respond_msg 被动回复通道）
      // 接管发送，同时 text 替换为去掉 MEDIA: 行的残余正文。
      // v2.8.21 ⭐ 加诊断 log（让 gateway.log 能看到 parser 触发情况，区分三态：
      //   ① LLM 没 emit MEDIA: → 沉默
      //   ② emit 了且抽出 → "MEDIA directive(s) detected via reply.deliver"
      //   ③ 文本里有 "MEDIA:" 子串但行级匹配未命中（嵌入正文中部 / 引号 / 列表项里）→ warn
      // 之前 v2.8.20 没加任何 log，gateway.log 看不到 parser 是否触发，导致下游会话误判
      // "extractMediaDirectives 从未被调用"——其实可能调了但没 mediaPath 也没 substring。
      let normalizedText = payload.text ?? "";
      const directiveMediaPaths: string[] = [];
      if (normalizedText) {
        const ex = extractMediaDirectives(normalizedText);
        if (ex.mediaPaths.length > 0) {
          normalizedText = ex.residualText;
          directiveMediaPaths.push(...ex.mediaPaths);
          console.log(
            `[wecom-ws] MEDIA directive(s) detected via reply.deliver (count=${ex.mediaPaths.length}, kind=${info.kind}, peer=${peerKind}:${peerId}, paths=${JSON.stringify(ex.mediaPaths)})`,
          );
        } else if (/MEDIA:/i.test(normalizedText)) {
          // 补救诊断：text 里出现了 "MEDIA:" 但 parser 没抽出来——
          // 多半是 LLM 把 MEDIA: 嵌入正文中部、或在引号/列表项里、或行首有非空白字符。
          const sample = normalizedText.match(/[^\n]*MEDIA:[^\n]*/i)?.[0]?.slice(0, 200) ?? "(unknown)";
          console.warn(
            `[wecom-ws] MEDIA: substring present but no directive line matched (kind=${info.kind}, peer=${peerKind}:${peerId}, sample=${JSON.stringify(sample)}). LLM 必须把 'MEDIA: <path>' 单独成行，前后不要有正文/列表/引号/emoji。`,
          );
        }
      }

      const text = normalizedText.trim() || "";
      const incomingMediaUrls = [
        ...(payload.mediaUrls || (payload.mediaUrl ? [payload.mediaUrl] : [])),
        ...directiveMediaPaths,
      ];
      const hasIncomingMedia = incomingMediaUrls.length > 0;
      if (info.kind !== "final" && hasIncomingMedia) {
        mergeDeferredMediaUrls(incomingMediaUrls);
      }
      const mediaUrls =
        info.kind === "final" ? mergeDeferredMediaUrls(incomingMediaUrls) : incomingMediaUrls;
      if (!text && mediaUrls.length === 0) {
        // v2.8.28 ⭐ kind=final + 空内容（textLen=0 mediaCount=0）的 dispatch 极速 done 场景
        // 必须立刻 finalize stream 让企微 UI 解锁。否则 placeholder 卡 last=false 等 120s
        // timeout 才被兜底，用户看到"正在思考..."spinner 100+ 秒。v2.8.27 漏修这条早退点。
        if (info.kind === "final") {
          await finalizeStreamIfNeeded("final-empty-textmedia");
        }
        return;
      }

      if (info.kind === "block") {
        if (!text) {
          return;
        }
        accumulatedText = accumulatedText ? `${accumulatedText}\n${text}` : text;
      }

      const outboundText =
        info.kind === "final"
          ? accumulatedText
            ? text
              ? `${accumulatedText}\n${text}`
              : accumulatedText
            : text
          : accumulatedText || text;

      let finalText = outboundText;
      if (info.kind === "final" && mediaUrls.length > 0) {
        const cfg = getWecomRuntime().config.loadConfig();
        const mediaLocalRoots = resolveWecomMergedMediaLocalRoots({ cfg });
        const mediaMaxBytes = resolveWecomMediaMaxBytes(cfg, params.accountId);
        const mediaFailures: string[] = [];
        const mediaNotes: string[] = [];
        let mediaSent = 0;
        for (const mediaUrl of mediaUrls) {
          // v2.8.8 ⭐ Use replyMedia (aibot_respond_msg) instead of sendMediaMessage
          // (aibot_send_msg). reply.ts is invoked in the context of responding to a
          // user message; the SDK's replyMedia binds the media to the inbound req_id
          // so it appears as a contextual reply, not a free-standing active push.
          const result = await uploadAndReplyBotWsMedia({
            wsClient: params.client,
            frame: params.frame,
            mediaUrl,
            mediaLocalRoots,
            maxBytes: mediaMaxBytes,
          });
          if (result.ok) {
            mediaSent += 1;
            if (result.downgradeNote) {
              mediaNotes.push(result.downgradeNote);
            }
            continue;
          }
          mediaFailures.push(formatMediaFailure(mediaUrl, result.error, result.rejectReason));
        }

        if (!finalText && mediaSent > 0) {
          finalText = "文件已发送。";
        }
        if (mediaFailures.length > 0) {
          finalText = finalText
            ? `${finalText}\n\n${mediaFailures.join("\n")}`
            : mediaFailures.join("\n");
        }
        if (mediaNotes.length > 0) {
          finalText = finalText
            ? `${finalText}\n\n${mediaNotes.join("\n")}`
            : mediaNotes.join("\n");
        }
        deferredMediaUrls = [];
      }
      if (!finalText) {
        // v2.8.27 → v2.8.28 抽成 helper finalizeStreamIfNeeded（覆盖更多早退点）
        if (info.kind === "final") {
          await finalizeStreamIfNeeded("final-no-text");
        }
        return;
      }

      // Event frames do not support streaming chunks
      if (isEvent && info.kind !== "final") {
        return;
      }

      // v2.8.5 ⭐ Stream partial chunks via replyStream(last=false) so user sees progress.
      // Cap at MAX_PARTIAL_REPLIES to avoid SDK reply queue saturation
      // (each pending partial waits ~5s for WS ack; too many partials can stall final).
      // Excess block chunks are silently accumulated and flushed in the final reply.
      // Partial sends are fire-and-forget: any failure is non-terminal because final
      // delivery will (re)send the complete accumulated content.
      if (info.kind !== "final") {
        if (partialReplyCount < MAX_PARTIAL_REPLIES) {
          partialReplyCount += 1;
          // Stop placeholder keepalive when first real partial arrives — otherwise
          // the next keepalive tick would overwrite this partial with the placeholder.
          stopPlaceholderKeepalive();
          notifyPeerActive();
          void params.client
            .replyStream(
              params.frame,
              resolveStreamId(),
              toWeComMarkdownV2(outboundText),
              false,
            )
            .catch((error) => {
              // ack timeout / invalid reqId / expired stream are all non-terminal here:
              // the final reply will deliver the full accumulated content.
              // We still feed the watchdog to detect chronic WS health degradation.
              if (isAckTimeoutError(error)) {
                hitAckTimeoutWatchdog({
                  accountId: params.accountId,
                  onReconnectNeeded: params.onReconnectNeeded,
                });
              }
            });
        }
        return;
      }

      settleStream();

      // WS disconnected → Agent API is the only option.
      if (!params.client.isConnected) {
        console.warn(
          `[wecom-ws] WS not connected for account=${params.accountId} peer=${peerId}, using agent fallback`,
        );
        try {
          await fallbackAgentApiDelivery(toWeComMarkdownV2(finalText));
          params.onDeliver?.();
        } catch (err) {
          params.onFail?.(err);
        }
        return;
      }

      try {
        if (params.inboundKind === "welcome") {
          await params.client.replyWelcome(params.frame, {
            msgtype: "text",
            text: { content: finalText },
          });
        } else if (isEvent) {
          // Send push message for other events
          // v2.8.31 ⭐ SDK SendMsgBody 只允许 msgtype: 'markdown'，不支持 markdown_v2。
          await params.client.sendMessage(peerId, {
            msgtype: "markdown",
            markdown: { content: toWeComMarkdownV2(finalText) },
          });
        } else {
          // Race WS replyStream with a timeout to avoid being blocked by the
          // SDK's global reply queue (which can backlog during ack timeouts).
          // If WS doesn't ack within 6s, fall back to Agent API immediately.
          const WS_REPLY_TIMEOUT_MS = 6000;
          await Promise.race([
            params.client.replyStream(
              params.frame,
              resolveStreamId(),
              toWeComMarkdownV2(finalText),
              true,
            ),
            new Promise<void>((_, reject) =>
              setTimeout(
                () => reject(new Error(`WS reply timed out after ${WS_REPLY_TIMEOUT_MS}ms`)),
                WS_REPLY_TIMEOUT_MS,
              ),
            ),
          ]);
        }
      } catch (error) {
        // replyStream (or replyWelcome / sendMessage) failed.
        // Fallback tiers: Bot WS active push → Agent API.
        const isWsTimeout = error instanceof Error &&
          (error.message.includes("ack timeout") || error.message.includes("timed out"));
        // v2.8.17 ⭐ 长任务结果回流修复：reqId 失效 / 流过期 ≠ 全死。
        // SDK 的 replyStream 通道（绑定 inbound req_id）已关闭，但
        // sendMessage 主动推送 / Agent API 是独立通道，仍能把已生成的内容送出去。
        // 之前直接 onFail 会让用户看到"OpenClaw UI 有结果，但企微一直停在'思考中…'"。
        const isReplyChannelDead =
          isInvalidReqIdError(error) || isExpiredStreamUpdateError(error);
        if (isWsTimeout) {
          hitAckTimeoutWatchdog({
            accountId: params.accountId,
            onReconnectNeeded: params.onReconnectNeeded,
          });
          console.warn(
            `[wecom-ws] ${error instanceof Error ? error.message : String(error)} for ${peerId}, trying fallback`,
          );
        } else if (isReplyChannelDead) {
          console.warn(
            `[wecom-ws] reply channel closed (${error instanceof Error ? error.message : String(error)}) for ${peerId}, trying active push fallback`,
          );
        } else {
          console.warn(
            `[wecom-ws] WS delivery failed for ${peerId}: ${error instanceof Error ? error.message : String(error)}, trying fallback`,
          );
        }

        // Tier 1: Bot WS active push (sendMessage works for both direct & group
        // chats where the bot is a member — unlike Agent API appchat/send which
        // only works for app-created group chats).
        if (params.client.isConnected) {
          try {
            // v2.8.31 ⭐ SDK 只支持 msgtype: 'markdown'。
            await params.client.sendMessage(peerId, {
              msgtype: "markdown",
              markdown: { content: toWeComMarkdownV2(finalText) },
            });
            console.log(
              `[wecom-ws] fallback: delivered via sendMessage to ${peerKind}=${peerId}`,
            );
            params.onDeliver?.();
            return;
          } catch (sendErr) {
            console.warn(
              `[wecom-ws] sendMessage fallback failed for ${peerKind}=${peerId}: ${sendErr instanceof Error ? sendErr.message : String(sendErr)}`,
            );
          }
        }

        // Tier 2: Agent API (last resort — requires Agent app in the chat).
        try {
          await fallbackAgentApiDelivery(toWeComMarkdownV2(finalText));
          params.onDeliver?.();
          return;
        } catch (fallbackErr) {
          params.onFail?.(fallbackErr);
          return;
        }
      }
      params.onDeliver?.();
    },
    fail: async (error: unknown) => {
      notifyPeerActive();
      settleStream();
      if (isTerminalReplyError(error)) {
        params.onFail?.(error);
        return;
      }
      const message = formatErrorMessage(error);
      const text = `WeCom WS reply failed: ${message}`;

      // Short-term fix: if WS is disconnected, use fallback delivery for error messages too
      if (!params.client.isConnected) {
        console.warn(
          `[wecom-ws] WS not connected in fail() for account=${params.accountId} peer=${peerId}, using fallback`,
        );
        try {
          await fallbackAgentApiDelivery(text);
        } catch {
          // fallback failed, still call onFail
        }
        params.onFail?.(error);
        return;
      }

      try {
        if (params.inboundKind === "welcome") {
          await params.client.replyWelcome(params.frame, {
            msgtype: "text",
            text: { content: text },
          });
        } else if (isEvent) {
          // v2.8.31 ⭐ SDK 只支持 msgtype: 'markdown'。
          await params.client.sendMessage(peerId, {
            msgtype: "markdown",
            markdown: { content: text },
          });
        } else {
          await params.client.replyStream(params.frame, resolveStreamId(), text, true);
        }
      } catch (sendError) {
        // Fallback for send error
        try {
          await fallbackAgentApiDelivery(text);
        } catch {
          // fallback failed
        }
        params.onFail?.(sendError);
        return;
      }
      params.onFail?.(error);
    },
    markExternalActivity: () => {
      notifyPeerActive();
      stopPlaceholderKeepalive();
    },
  };
}
