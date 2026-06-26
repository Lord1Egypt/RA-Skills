import crypto from "node:crypto";
import AiBot, {
  generateReqId,
  type BaseMessage,
  type EventMessage,
  type WsFrame,
} from "@wecom/aibot-node-sdk";
import type { WecomAccountRuntime } from "../../app/account-runtime.js";
import { registerBotWsPushHandle, unregisterBotWsPushHandle } from "../../app/index.js";
import { clearWecomMcpAccountCache } from "../../capability/mcp/index.js";
import type { RuntimeLogSink } from "../../types/index.js";
import { mapBotWsFrameToInboundEvent } from "./inbound.js";
import { uploadAndSendBotWsMedia } from "./media.js";
import { createBotWsReplyHandle } from "./reply.js";
import { createBotWsSessionSnapshot } from "./session.js";

export class BotWsSdkAdapter {
  private client?: AiBot.WSClient;
  private readonly ownerId: string;
  private restarting = false;

  constructor(
    private readonly runtime: WecomAccountRuntime,
    private readonly log: RuntimeLogSink,
  ) {
    this.ownerId = `${this.runtime.account.accountId}:ws:${crypto.randomUUID().slice(0, 8)}`;
  }

  start(): void {
    this.restarting = false;
    const bot = this.runtime.account.bot;
    if (!bot?.wsConfigured || !bot.ws) {
      throw new Error(`WeCom bot account "${this.runtime.account.accountId}" missing WS config.`);
    }
    this.log.info?.(
      `[wecom-ws] start account=${this.runtime.account.accountId} botId=${bot.ws.botId} wsUrl=default heartbeat=default reconnectInterval=default`,
    );
    const client = new AiBot.WSClient({
      botId: bot.ws.botId,
      secret: bot.ws.secret,
      logger: {
        debug: (message, ...args) =>
          this.log.info?.(`[wecom-ws] ${message} ${args.join(" ")}`.trim()),
        info: (message, ...args) =>
          this.log.info?.(`[wecom-ws] ${message} ${args.join(" ")}`.trim()),
        warn: (message, ...args) =>
          this.log.warn?.(`[wecom-ws] ${message} ${args.join(" ")}`.trim()),
        error: (message, ...args) =>
          this.log.error?.(`[wecom-ws] ${message} ${args.join(" ")}`.trim()),
      },
    });
    this.client = client;
    registerBotWsPushHandle(this.runtime.account.accountId, {
      isConnected: () => client.isConnected,
      replyCommand: async ({ cmd, body, headers }) => {
        const replyHeaders = {
          ...(headers ?? {}),
          req_id: headers?.req_id ?? generateReqId("wecom_ws"),
        };
        const result = await client.reply({ headers: replyHeaders }, body ?? {}, cmd);
        this.runtime.touchTransportSession("bot-ws", {
          ownerId: this.ownerId,
          running: true,
          connected: client.isConnected,
          authenticated: client.isConnected,
          lastOutboundAt: Date.now(),
          lastError: undefined,
        });
        return result as unknown as Record<string, unknown>;
      },
      sendMarkdown: async (chatId, content) => {
        // v2.8.31 ⭐ 真根因：@wecom/aibot-node-sdk SendMsgBody 联合类型只允许
        // SendMarkdownMsgBody { msgtype: 'markdown' } / SendTemplateCardMsgBody / SendMediaMsgBody。
        // **不支持 markdown_v2，也不支持 text**。之前 v2.8.26 用 markdown_v2 主动推送一直撞
        // 40008（5/5 全天 13 条全部是 sendMessage(markdown_v2)），降级 text 同样撞 40008
        // 但被 try-catch 吞了 console.warn 又走 stderr 没 redirect 到 gateway.log。
        // 修法：sendMessage 这条路径必须用 msgtype: "markdown"（SDK 支持的唯一富文本类型）。
        // markdown_v2 仅在 Agent API HTTP 路径（agent-api/core.ts）支持。
        await client.sendMessage(chatId, {
          msgtype: "markdown",
          markdown: { content },
        });
        this.runtime.touchTransportSession("bot-ws", {
          ownerId: this.ownerId,
          running: true,
          connected: client.isConnected,
          authenticated: client.isConnected,
          lastOutboundAt: Date.now(),
          lastError: undefined,
        });
      },
      sendMedia: async ({ chatId, mediaUrl, text, mediaLocalRoots, maxBytes }) => {
        const result = await uploadAndSendBotWsMedia({
          wsClient: client,
          chatId,
          mediaUrl,
          mediaLocalRoots,
          maxBytes,
        });
        if (result.ok && text?.trim()) {
          // v2.8.31 ⭐ SDK 不支持 markdown_v2，sendMessage 必须用 markdown。
          await client.sendMessage(chatId, {
            msgtype: "markdown",
            markdown: { content: text.trim() },
          });
        }
        this.runtime.touchTransportSession("bot-ws", {
          ownerId: this.ownerId,
          running: true,
          connected: client.isConnected,
          authenticated: client.isConnected,
          lastOutboundAt: Date.now(),
          lastError: result.ok ? undefined : result.error,
        });
        return result;
      },
    });

    client.on("connected", () => {
      this.log.info?.(`[wecom-ws] connected account=${this.runtime.account.accountId}`);
      this.runtime.updateTransportSession(
        createBotWsSessionSnapshot({
          accountId: this.runtime.account.accountId,
          ownerId: this.ownerId,
          connected: true,
          authenticated: false,
        }),
      );
    });

    client.on("authenticated", () => {
      this.log.info?.(`[wecom-ws] authenticated account=${this.runtime.account.accountId}`);
      this.runtime.updateTransportSession(
        createBotWsSessionSnapshot({
          accountId: this.runtime.account.accountId,
          ownerId: this.ownerId,
          connected: true,
          authenticated: true,
        }),
      );
    });

    client.on("disconnected", (reason) => {
      clearWecomMcpAccountCache(this.runtime.account.accountId);
      const normalizedReason = String(reason ?? "").toLowerCase();
      const kicked =
        normalizedReason.includes("kick") ||
        normalizedReason.includes("owner") ||
        normalizedReason.includes("replaced");
      this.log.warn?.(
        `[wecom-ws] disconnected account=${this.runtime.account.accountId} kicked=${String(kicked)} reason=${reason ?? "unknown"}`,
      );
      if (kicked) {
        this.runtime.recordOperationalIssue({
          transport: "bot-ws",
          category: "ws-kicked",
          summary: `ws owner lost: ${reason ?? "unknown"}`,
          error: reason ?? "unknown",
        });
      }
      if (kicked) {
        // Real kick — mark as not-running so health-monitor can restart.
        this.runtime.updateTransportSession(
          createBotWsSessionSnapshot({
            accountId: this.runtime.account.accountId,
            ownerId: this.ownerId,
            running: false,
            connected: false,
            authenticated: false,
            lastDisconnectedAt: Date.now(),
            lastError: reason,
          }),
        );
      } else {
        // Informational disconnect (e.g. "New connection established").
        // The SDK handles reconnection internally; touching only timestamps
        // avoids destabilising the health-monitor which would otherwise
        // restart → new WS → server kills old → infinite loop.
        this.runtime.touchTransportSession("bot-ws", {
          ownerId: this.ownerId,
          lastDisconnectedAt: Date.now(),
          lastError: reason,
        });
      }
    });

    client.on("reconnecting", (attempt) => {
      this.log.warn?.(
        `[wecom-ws] reconnecting account=${this.runtime.account.accountId} attempt=${attempt}`,
      );
    });

    client.on("error", (error) => {
      this.log.error?.(
        `[wecom-ws] error account=${this.runtime.account.accountId} message=${error.message}`,
      );
      this.runtime.updateTransportSession(
        createBotWsSessionSnapshot({
          accountId: this.runtime.account.accountId,
          ownerId: this.ownerId,
          running: false,
          connected: client.isConnected,
          authenticated: client.isConnected,
          lastError: error.message,
        }),
      );
    });

    const handleFrame = async (frame: WsFrame<BaseMessage | EventMessage>) => {
      const botAccount = this.runtime.account.bot;
      if (!botAccount) {
        return;
      }
      // Skip system events that are handled by the SDK lifecycle hooks.
      // Routing them to the agent causes reply failures that destabilise
      // the health-monitor (connected=false on touch → restart loop).
      const body = frame.body;
      if (body && (body as EventMessage).msgtype === "event") {
        const eventType = String((body as EventMessage).event?.eventtype ?? "");
        if (eventType === "disconnected_event") {
          this.log.info?.(
            `[wecom-ws] frame account=${this.runtime.account.accountId} cmd=${frame.cmd} event=disconnected_event (skipped — handled by lifecycle)`,
          );
          return;
        }
      }
      this.log.info?.(
        `[wecom-ws] frame account=${this.runtime.account.accountId} cmd=${frame.cmd} reqId=${frame.headers.req_id ?? "n/a"}`,
      );
      this.runtime.touchTransportSession("bot-ws", {
        ownerId: this.ownerId,
        running: true,
        connected: client.isConnected,
        authenticated: client.isConnected,
        lastInboundAt: Date.now(),
      });
      const event = mapBotWsFrameToInboundEvent({
        account: botAccount,
        frame,
      });
      const replyHandle = createBotWsReplyHandle({
        client,
        frame,
        accountId: this.runtime.account.accountId,
        inboundKind: event.inboundKind,
        placeholderContent: botAccount.config.streamPlaceholderContent,
        progressMode: botAccount.config.progressMode,
        progressDelayedMs: botAccount.config.progressDelayedMs,
        autoSendPlaceholder:
          event.inboundKind === "text" ||
          event.inboundKind === "image" ||
          event.inboundKind === "file" ||
          event.inboundKind === "voice" ||
          event.inboundKind === "mixed",
        onDeliver: () => {
          this.runtime.touchTransportSession("bot-ws", {
            ownerId: this.ownerId,
            running: true,
            connected: client.isConnected,
            authenticated: client.isConnected,
            lastOutboundAt: Date.now(),
          });
        },
        onFail: (error) => {
          this.runtime.touchTransportSession("bot-ws", {
            ownerId: this.ownerId,
            running: client.isConnected,
            connected: client.isConnected,
            authenticated: client.isConnected,
            lastError: error instanceof Error ? error.message : String(error),
          });
        },
        onReconnectNeeded: (accountId) => {
          this.log.warn?.(
            `[wecom-ws] watchdog triggered reconnect for account=${accountId}`,
          );
          // Trigger WS reconnect by disconnecting; the SDK auto-reconnects.
          // Also stop current adapter to allow clean restart.
          this.stop();
          // Reset and restart after a brief delay to avoid reconnect storms
          setTimeout(() => {
            this.log.info?.(
              `[wecom-ws] restarting adapter for account=${accountId}`,
            );
            this.start();
          }, 1000);
        },
      });

      const staticWelcomeText =
        event.inboundKind === "welcome" ? botAccount.config.welcomeText?.trim() : undefined;
      if (staticWelcomeText) {
        this.log.info?.(
          `[wecom-ws] static welcome reply account=${this.runtime.account.accountId} messageId=${event.messageId} peer=${event.conversation.peerKind}:${event.conversation.peerId} len=${staticWelcomeText.length}`,
        );
        await replyHandle.deliver(
          {
            text: staticWelcomeText,
          },
          { kind: "final" },
        );
        this.log.info?.(
          `[wecom-ws] static welcome delivered account=${this.runtime.account.accountId} messageId=${event.messageId}`,
        );
        return;
      }

      await this.runtime.handleEvent(event, replyHandle);
    };

    const runHandleFrame = (frame: WsFrame<BaseMessage | EventMessage>) => {
      void handleFrame(frame).catch((error) => {
        const message = error instanceof Error ? error.message : String(error);
        this.log.error?.(
          `[wecom-ws] frame handler failed account=${this.runtime.account.accountId} reqId=${frame.headers?.req_id ?? "n/a"} message=${message}`,
        );
        this.runtime.recordOperationalIssue({
          transport: "bot-ws",
          category: "runtime-error",
          messageId: frame.body?.msgid,
          raw: {
            transport: "bot-ws",
            command: frame.cmd,
            headers: frame.headers,
            body: frame.body,
            envelopeType: "ws",
          },
          summary: `bot-ws frame handler crashed reqId=${frame.headers?.req_id ?? "n/a"}`,
          error: message,
        });
        this.runtime.touchTransportSession("bot-ws", {
          ownerId: this.ownerId,
          running: client.isConnected,
          connected: client.isConnected,
          authenticated: client.isConnected,
          lastError: message,
        });
      });
    };

    client.on("message", (frame) => {
      runHandleFrame(frame);
    });
    client.on("event", (frame) => {
      runHandleFrame(frame);
    });

    client.connect();
  }

  stop(): void {
    this.log.info?.(`[wecom-ws] stop account=${this.runtime.account.accountId}`);
    clearWecomMcpAccountCache(this.runtime.account.accountId);
    unregisterBotWsPushHandle(this.runtime.account.accountId);
    this.runtime.updateTransportSession(
      createBotWsSessionSnapshot({
        accountId: this.runtime.account.accountId,
        ownerId: this.ownerId,
        running: false,
        connected: false,
        authenticated: false,
        lastDisconnectedAt: Date.now(),
      }),
    );
    this.client?.disconnect();
  }
}
