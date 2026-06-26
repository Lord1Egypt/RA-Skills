import { PubSub, type Message as PubSubMessage } from "@google-cloud/pubsub";
import { google, type gmail_v1 } from "googleapis";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/device-pair";

type Config = {
  chatId?: string;
  gcpProject?: string;
  pubsubSubscription?: string;
  llmApiKey?: string;
  llmBaseUrl?: string;
  llmModel?: string;
  credentialsPath?: string;
};

type ClassifyResult = {
  important: boolean;
  summary: string;
};

const CLASSIFY_PROMPT = `You are an email triage assistant. Given an email, decide if it needs the user's attention NOW.

Reply with JSON only: { "important": true/false, "summary": "one sentence in the same language as the email" }

Important: real person writing to you, requires action/reply/decision, mentions deadline, payment, or urgent issue.
Not important: newsletter, marketing, automated notification, social media alert, digest.`;

async function classifyEmail(
  cfg: Config,
  from: string,
  subject: string,
  body: string
): Promise<ClassifyResult> {
  if (!cfg.llmApiKey) {
    return { important: true, summary: subject };
  }

  const baseUrl = cfg.llmBaseUrl ?? "https://api.openai.com/v1";
  const model = cfg.llmModel ?? "gpt-4o-mini";

  try {
    const res = await fetch(`${baseUrl}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${cfg.llmApiKey}`,
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: CLASSIFY_PROMPT },
          {
            role: "user",
            content: `From: ${from}\nSubject: ${subject}\n\n${body.slice(0, 500)}`,
          },
        ],
        response_format: { type: "json_object" },
        max_tokens: 150,
      }),
    });
    const data = (await res.json()) as any;
    const parsed = JSON.parse(data.choices?.[0]?.message?.content ?? "{}");
    return {
      important: Boolean(parsed.important),
      summary: String(parsed.summary || subject),
    };
  } catch {
    return { important: true, summary: subject };
  }
}

function extractBody(payload: gmail_v1.Schema$MessagePart | undefined): string {
  if (!payload) return "";
  if (payload.mimeType === "text/plain" && payload.body?.data) {
    return Buffer.from(payload.body.data, "base64url").toString("utf-8");
  }
  if (payload.parts) {
    for (const part of payload.parts) {
      if (part.mimeType === "text/plain" && part.body?.data) {
        return Buffer.from(part.body.data, "base64url").toString("utf-8");
      }
      if (part.parts) {
        const nested = extractBody(part);
        if (nested) return nested;
      }
    }
  }
  return "";
}

function escMd(s: string): string {
  return s.replace(/[_*[\]()~`>#+\-=|{}.!]/g, "\\$&");
}

function formatMessage(from: string, subject: string, summary: string): string {
  const sender = from.replace(/<.*>/, "").trim() || from;
  return `📬 *${escMd(sender)}*\n${escMd(subject)}\n\n${escMd(summary)}`;
}

export default function register(api: OpenClawPluginApi) {
  let subscription: ReturnType<PubSub["subscription"]> | null = null;
  let watchTimer: ReturnType<typeof setInterval> | null = null;
  let lastHistoryId: string | null = null;
  const notifiedIds = new Set<string>();
  let processing = false;
  const pendingHistoryIds: string[] = [];

  async function processHistoryId(gmail: gmail_v1.Gmail, newHistoryId: string) {
    if (!lastHistoryId) {
      lastHistoryId = newHistoryId;
      return;
    }

    const history = await gmail.users.history.list({
      userId: "me",
      startHistoryId: lastHistoryId,
      historyTypes: ["messageAdded"],
    });

    lastHistoryId = newHistoryId;

    const records = history.data.history || [];
    const newIds: string[] = [];
    for (const record of records) {
      for (const added of record.messagesAdded || []) {
        const id = added.message?.id;
        if (id && !notifiedIds.has(id)) {
          newIds.push(id);
          notifiedIds.add(id);
        }
      }
    }

    if (newIds.length === 0) return;

    const cfg = (api.pluginConfig ?? {}) as Config;
    const chatId = cfg.chatId!;
    const send = api.runtime?.channel?.telegram?.sendMessageTelegram;
    if (!send) {
      api.logger.warn?.("mail-agent: telegram runtime not available");
      return;
    }

    for (const msgId of newIds) {
      try {
        const msg = await gmail.users.messages.get({
          userId: "me",
          id: msgId,
          format: "full",
        });

        const labels = msg.data.labelIds || [];
        if (!labels.includes("INBOX") || !labels.includes("UNREAD")) continue;
        if (labels.includes("SENT")) continue;

        const headers = msg.data.payload?.headers || [];
        const getHeader = (name: string) =>
          headers.find((h) => h.name === name)?.value || "";

        const from = getHeader("From");
        const subject = getHeader("Subject") || "(no subject)";
        const body = extractBody(msg.data.payload);

        const { important, summary } = await classifyEmail(cfg, from, subject, body);

        if (!important) {
          api.logger.info?.(`mail-agent: filtered — ${subject}`);
          continue;
        }

        await send(chatId, formatMessage(from, subject, summary), {
          parse_mode: "MarkdownV2",
        });
        api.logger.info?.(`mail-agent: notified — ${subject}`);
      } catch (err: any) {
        api.logger.warn?.(`mail-agent: failed to process ${msgId}: ${err?.message}`);
      }
    }

    if (notifiedIds.size > 500) {
      const arr = [...notifiedIds];
      arr.slice(0, arr.length - 200).forEach((id) => notifiedIds.delete(id));
    }
  }

  async function handlePubSubMessage(
    gmail: gmail_v1.Gmail,
    data: string
  ) {
    try {
      const parsed = JSON.parse(data);
      const newHistoryId = parsed.historyId as string;
      api.logger.info?.(`mail-agent: notification historyId=${newHistoryId}`);

      if (processing) {
        pendingHistoryIds.push(newHistoryId);
        return;
      }
      processing = true;
      try {
        await processHistoryId(gmail, newHistoryId);
        while (pendingHistoryIds.length > 0) {
          await processHistoryId(gmail, pendingHistoryIds.shift()!);
        }
      } finally {
        processing = false;
      }
    } catch (err: any) {
      api.logger.warn?.(`mail-agent: handle error: ${err?.message}`);
    }
  }

  api.registerService({
    id: "mail-agent-watcher",

    start: async () => {
      const cfg = (api.pluginConfig ?? {}) as Config;

      if (!cfg.chatId) {
        api.logger.warn?.("mail-agent: chatId not configured");
        return;
      }
      if (!cfg.gcpProject || !cfg.pubsubSubscription) {
        api.logger.warn?.("mail-agent: gcpProject and pubsubSubscription required");
        return;
      }

      const auth = new google.auth.GoogleAuth({
        scopes: ["https://www.googleapis.com/auth/gmail.readonly"],
        ...(cfg.credentialsPath ? { keyFilename: cfg.credentialsPath } : {}),
      });
      const gmail = google.gmail({ version: "v1", auth });

      // Register Gmail watch
      try {
        const res = await gmail.users.watch({
          userId: "me",
          requestBody: {
            topicName: `projects/${cfg.gcpProject}/topics/mail-agent-inbox`,
            labelIds: ["INBOX"],
          },
        });
        lastHistoryId = res.data.historyId || null;
        api.logger.info?.(`mail-agent: watch registered, historyId=${lastHistoryId}`);
      } catch (err: any) {
        api.logger.warn?.(`mail-agent: watch registration failed: ${err?.message}`);
        return;
      }

      // Re-register watch every 6 days (expires after 7)
      watchTimer = setInterval(async () => {
        try {
          await gmail.users.watch({
            userId: "me",
            requestBody: {
              topicName: `projects/${cfg.gcpProject}/topics/mail-agent-inbox`,
              labelIds: ["INBOX"],
            },
          });
        } catch {}
      }, 6 * 24 * 60 * 60 * 1000);

      // Subscribe to Pub/Sub
      const pubsub = new PubSub({ projectId: cfg.gcpProject });
      subscription = pubsub.subscription(cfg.pubsubSubscription);
      subscription.on("message", (msg: PubSubMessage) => {
        handlePubSubMessage(gmail, msg.data?.toString() || "");
        msg.ack();
      });
      subscription.on("error", (err: Error) => {
        api.logger.warn?.(`mail-agent: subscription error: ${err.message}`);
      });

      api.logger.info?.("mail-agent: watching inbox");
    },

    stop: async () => {
      if (watchTimer) {
        clearInterval(watchTimer);
        watchTimer = null;
      }
      if (subscription) {
        subscription.removeAllListeners();
        await subscription.close();
        subscription = null;
      }
      api.logger.info?.("mail-agent: stopped");
    },
  });
}
