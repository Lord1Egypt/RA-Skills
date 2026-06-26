import os from "node:os";
import path from "node:path";
import { createChatChannelPlugin } from "openclaw/plugin-sdk/channel-core";
import type { ChannelPlugin } from "openclaw/plugin-sdk/channel-core";
import type { OpenClawConfig } from "openclaw/plugin-sdk/config-runtime";
import { ZulipClient } from "./client.js";
import { ZulipChannelConfigSchema } from "./config-schema.js";
import { startZulipGateway } from "./gateway.js";
import { normalizeZulipEvent, buildInboundTarget } from "./inbound.js";
import {
  initDatabase,
  MetadataStore,
  handleMetaCommand,
  syncPrefixToMetadata,
} from "./metadata/index.js";
import { normalizeZulipMessagingTarget } from "./normalize.js";
import { zulipOutboundBaseAdapter } from "./outbound-base.js";
import { secretTargetRegistryEntries, collectRuntimeConfigAssignments } from "./secret-contract.js";
import { sendMessageZulip } from "./send.js";
import type { CoreConfig, ZulipProbe } from "./types.js";

type ResolvedZulipAccount = {
  accountId?: string | null;
  realm: string;
  email: string;
  configured: boolean;
};

const meta = {
  id: "zulip",
  label: "Zulip",
  selectionLabel: "Zulip (Realm + Bot)",
  docsPath: "/channels/zulip",
  docsLabel: "zulip",
  blurb: "Zulip team chat with stream/topic routing and DM support.",
  order: 90,
  detailLabel: "Zulip",
  systemImage: "bubble.left.and.bubble.right",
};

function resolveZulipAccount(params: {
  cfg: OpenClawConfig;
  accountId?: string | null;
}): ResolvedZulipAccount {
  const zulip = (params.cfg as Record<string, unknown>).channels as
    | Record<string, unknown>
    | undefined;
  const zulipCfg = zulip?.zulip as Record<string, unknown> | undefined;
  const realm = (zulipCfg?.realm as string) ?? "";
  const email = (zulipCfg?.email as string) ?? "";
  return {
    accountId: params.accountId ?? null,
    realm,
    email,
    configured: realm.length > 0 && email.length > 0,
  };
}

export const zulipPlugin: ChannelPlugin<ResolvedZulipAccount, ZulipProbe> = createChatChannelPlugin(
  {
    base: {
      id: "zulip",
      meta,
      capabilities: {
        chatTypes: ["direct", "group"],
        media: true,
        blockStreaming: false,
      },
      reload: { configPrefixes: ["channels.zulip"] },
      configSchema: ZulipChannelConfigSchema,
      config: {
        listAccountIds: () => [],
        resolveAccount: (cfg, accountId) => resolveZulipAccount({ cfg, accountId }),
        hasConfiguredState: ({ env }) =>
          typeof env?.ZULIP_REALM === "string" &&
          env.ZULIP_REALM.trim().length > 0 &&
          typeof env?.ZULIP_EMAIL === "string" &&
          env.ZULIP_EMAIL.trim().length > 0 &&
          typeof env?.ZULIP_API_KEY === "string" &&
          env.ZULIP_API_KEY.trim().length > 0,
        isConfigured: (account) => account.configured,
      },
      secrets: {
        secretTargetRegistryEntries,
        collectRuntimeConfigAssignments,
      },
      messaging: {
        normalizeTarget: normalizeZulipMessagingTarget,
      },
      gateway: {
        startAccount: async (ctx) => {
          const cfg = ctx.cfg as CoreConfig;
          const zulipCfg = cfg.channels?.zulip;
          if (!zulipCfg?.realm || !zulipCfg?.email || !zulipCfg?.apiKey) {
            throw new Error("Zulip realm, email, and apiKey are required");
          }
          ctx.log?.info?.(`zulip: starting gateway for ${zulipCfg.realm}`);

          // Get own user ID for self-message filtering
          const client = new ZulipClient({
            realm: zulipCfg.realm,
            email: zulipCfg.email,
            apiKey: zulipCfg.apiKey,
          });
          const ownUser = await client.getOwnUser();
          const ownUserId = ownUser.user_id;
          ctx.log?.info?.(`zulip: bot user_id=${ownUserId} (${ownUser.email})`);

          // Initialize metadata subsystem
          const dbPath = path.join(os.homedir(), ".openclaw", "data", "zulip-metadata.sqlite");
          const db = initDatabase(dbPath);
          const metadataStore = new MetadataStore(db);

          const accountId = ctx.accountId ?? "default";
          const handle = startZulipGateway(
            {
              realm: zulipCfg.realm,
              email: zulipCfg.email,
              apiKey: zulipCfg.apiKey,
            },
            {
              onMessage: async (event) => {
                const msg = normalizeZulipEvent(event, ownUserId);

                // Intercept /meta commands before AI dispatch
                const stripped = msg.text.replace(/<[^>]*>/g, "").trim();
                if (stripped.startsWith("/meta ") || stripped === "/meta") {
                  const streamId = event.message.stream_id;
                  const topicName = event.message.subject;
                  if (streamId != null && topicName) {
                    const response = handleMetaCommand(
                      metadataStore,
                      { streamId, topicName },
                      stripped,
                    );
                    const target = buildInboundTarget(msg, accountId);
                    await sendMessageZulip(target, response, { accountId });
                  }
                  return;
                }

                const target = buildInboundTarget(msg, accountId);
                ctx.log?.info?.(`zulip: inbound from ${msg.senderEmail} → ${target}`);


                // Dispatch to AI via channelRuntime if available.
                // Uses finalizeInboundContext → dispatchReplyWithBufferedBlockDispatcher
                // pattern (see qqbot/discord adapters for reference).
                if (ctx.channelRuntime) {
                  const runtime = ctx.channelRuntime as unknown as { reply: { finalizeInboundContext: (p: Record<string, unknown>) => unknown; dispatchReplyWithBufferedBlockDispatcher: (p: Record<string, unknown>) => Promise<void> } };
                  const ctxPayload = runtime.reply.finalizeInboundContext({
                    Body: msg.text,
                    BodyForAgent: msg.text,
                    RawBody: msg.text,
                    CommandBody: msg.text,
                    From: msg.senderEmail,
                    To: `zulip:${accountId}`,
                    SessionKey: target,
                    AccountId: accountId,
                    ChatType: msg.isGroup ? "group" : "direct",
                    SenderId: String(msg.senderId),
                    SenderName: msg.senderName,
                    Provider: "zulip",
                    Surface: "zulip",
                    MessageSid: String(msg.messageId),
                    Timestamp: msg.timestamp * 1000,
                    OriginatingChannel: "zulip",
                    OriginatingTo: target,
                    CommandAuthorized: false,
                  });

                  await runtime.reply.dispatchReplyWithBufferedBlockDispatcher({
                    ctx: ctxPayload,
                    cfg: ctx.cfg,
                    dispatcherOptions: {
                      deliver: async (payload: { text?: string }) => {
                        const text = payload.text?.trim();
                        if (text) {
                          await sendMessageZulip(target, text, { accountId });
                        }
                      },
                    },
                  });
                }
              },
              onTopicRename: async (streamId, oldTopic, newTopic) => {
                syncPrefixToMetadata(metadataStore, streamId, oldTopic, newTopic);
                ctx.log?.info?.(`zulip: topic renamed: "${oldTopic}" → "${newTopic}"`);
              },
              onError: (err) => {
                ctx.log?.info?.(`zulip: gateway error: ${String(err)}`);
              },

              onConnected: (info) => {
                ctx.log?.info?.(`zulip: connected (queue=${info.queueId})`);
              },
              log: (msg) => ctx.log?.info?.(msg),
            },
            { abortSignal: ctx.abortSignal },
          );
          return {
            stop: async () => {
              await handle.stop();
              db.close();
              ctx.log?.info?.("zulip: metadata store closed");
            },
          };
        },
      },
    },
    outbound: {
      base: zulipOutboundBaseAdapter,
      attachedResults: {
        channel: "zulip",
        sendText: async ({ to, text, accountId, replyToId }) => {
          const result = await sendMessageZulip(to, text, {
            accountId: accountId ?? undefined,
            replyTo: replyToId ?? undefined,
          });
          return { messageId: String(result.messageId), target: result.target };
        },
        sendMedia: async ({ to, text, mediaUrl, accountId, replyToId }) => {
          if (mediaUrl) {
            // For URLs we don't have blob data, send as a text message with link
            const message = text ? `${text}\n${mediaUrl}` : mediaUrl;
            const r1 = await sendMessageZulip(to, message, {
              accountId: accountId ?? undefined,
              replyTo: replyToId ?? undefined,
            });
            return { messageId: String(r1.messageId), target: r1.target };
          }
          const r2 = await sendMessageZulip(to, text, {
            accountId: accountId ?? undefined,
            replyTo: replyToId ?? undefined,
          });
          return { messageId: String(r2.messageId), target: r2.target };
        },
      },
    },
  },
);
