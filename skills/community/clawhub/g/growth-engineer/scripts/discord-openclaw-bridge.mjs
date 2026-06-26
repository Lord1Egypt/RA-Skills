#!/usr/bin/env node
import process from "node:process";

const DISCORD_API_BASE_URL = "https://discord.com/api/v10";
const ALLOWED_GUILD_ID = "1431275274770845708";
const OPENCLAW_CHANNEL_ID = "1471908112100495617";
const HERMES_CHANNEL_ID = "1503376909977780414";
const OPENCLAW_BOT_ID = "1471692354187559134";
const PRIMARY_TARGET_LABEL = "openclaw";
const MIN_ASK_TIMEOUT_SECONDS = 600;
const DISCORD_TARGETS = [
  {
    label: PRIMARY_TARGET_LABEL,
    guildId: ALLOWED_GUILD_ID,
    channelId: OPENCLAW_CHANNEL_ID,
    allowedMentionUsers: [OPENCLAW_BOT_ID],
  },
  {
    label: "hermes",
    guildId: ALLOWED_GUILD_ID,
    channelId: HERMES_CHANNEL_ID,
    allowedMentionUsers: [],
  },
];

const usage = `Usage:
  node scripts/discord-openclaw-bridge.mjs read [--limit 20]
  node scripts/discord-openclaw-bridge.mjs send "message"
  node scripts/discord-openclaw-bridge.mjs send --stdin
  node scripts/discord-openclaw-bridge.mjs watch [--interval 5] [--limit 10]
  node scripts/discord-openclaw-bridge.mjs ask "message" [--timeout 600]

Required environment:
  DISCORD_BOT_TOKEN

Hard-locked target:
  guild    ${ALLOWED_GUILD_ID}
  channels ${DISCORD_TARGETS.map((target) => `${target.label}:${target.channelId}`).join(", ")}`;

function readFlag(args, name, fallback) {
  const index = args.indexOf(name);
  if (index === -1) {
    return fallback;
  }
  const value = args[index + 1];
  if (!value || value.startsWith("--")) {
    throw new Error(`Missing value for ${name}`);
  }
  return value;
}

function hasFlag(args, name) {
  return args.includes(name);
}

function asPositiveInteger(value, label) {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed <= 0) {
    throw new Error(`${label} must be a positive integer`);
  }
  return parsed;
}

function getToken() {
  const token = process.env.DISCORD_BOT_TOKEN?.trim();
  if (!token) {
    throw new Error("DISCORD_BOT_TOKEN is required. Put it in .env or export it in your shell.");
  }
  return token;
}

async function discordFetch(path, options = {}) {
  const response = await fetch(`${DISCORD_API_BASE_URL}${path}`, {
    ...options,
    headers: {
      Authorization: `Bot ${getToken()}`,
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (response.status === 429) {
    const retry = await response.json().catch(() => ({}));
    const retryAfter = Number(retry.retry_after ?? 1);
    await new Promise((resolve) => setTimeout(resolve, Math.ceil(retryAfter * 1000)));
    return discordFetch(path, options);
  }

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Discord API ${response.status} for ${path}: ${text}`);
  }

  if (response.status === 204) {
    return undefined;
  }
  return response.json();
}

function getPrimaryTarget() {
  return DISCORD_TARGETS.find((target) => target.label === PRIMARY_TARGET_LABEL) ?? DISCORD_TARGETS[0];
}

async function validateTargetChannel(target) {
  const channel = await discordFetch(`/channels/${target.channelId}`);
  if (channel.guild_id !== target.guildId) {
    throw new Error(
      `Refusing to use ${target.label} channel ${target.channelId}; Discord returned guild ${channel.guild_id ?? "unknown"}.`,
    );
  }
  return channel;
}

function formatMessage(message) {
  const author = message.author?.bot
    ? `${message.author.username} [bot]`
    : (message.author?.global_name ?? message.author?.username ?? "unknown");
  const timestamp = new Date(message.timestamp).toISOString();
  const content = message.content?.trim() ? message.content.trim() : "(no text content)";
  const attachments = Array.isArray(message.attachments) && message.attachments.length > 0
    ? `\n  attachments: ${message.attachments.map((item) => item.url).join(", ")}`
    : "";
  return `[${timestamp}] ${author} (${message.id})\n  ${content}${attachments}`;
}

async function readMessages({ limit, after }) {
  const target = getPrimaryTarget();
  await validateTargetChannel(target);
  const params = new URLSearchParams({ limit: String(limit) });
  if (after) {
    params.set("after", after);
  }
  const messages = await discordFetch(`/channels/${target.channelId}/messages?${params}`);
  return messages.reverse();
}

function printMessages(messages) {
  for (const message of messages) {
    console.log(formatMessage(message));
  }
}

function truncateDiscordText(value, maxLength) {
  const text = String(value || "").trim();
  if (text.length <= maxLength) {
    return text;
  }
  return `${text.slice(0, Math.max(0, maxLength - 3)).trim()}...`;
}

function chunkMessage(content) {
  const chunks = [];
  const maxLength = 1900;
  let remaining = String(content || "").trim();

  while (remaining.length > maxLength) {
    let splitAt = remaining.lastIndexOf("\n", maxLength);
    if (splitAt < maxLength * 0.5) {
      splitAt = remaining.lastIndexOf(" ", maxLength);
    }
    if (splitAt < maxLength * 0.5) {
      splitAt = maxLength;
    }
    chunks.push(remaining.slice(0, splitAt).trim());
    remaining = remaining.slice(splitAt).trim();
  }

  if (remaining) {
    chunks.push(remaining);
  }
  return chunks;
}

function discordField(name, value, inline = false) {
  return {
    name: truncateDiscordText(name, 256) || "Detail",
    value: truncateDiscordText(value, 1024) || "-",
    inline,
  };
}

function splitNamedLine(line) {
  const clean = String(line || "").replace(/^-\s*/, "").trim();
  const bracketMarker = clean.indexOf(": [");
  if (bracketMarker > 0) {
    return [clean.slice(0, bracketMarker).trim(), clean.slice(bracketMarker + 2).trim()];
  }
  const splitAt = clean.lastIndexOf(": ");
  if (splitAt > 0) {
    return [clean.slice(0, splitAt).trim(), clean.slice(splitAt + 2).trim()];
  }
  return null;
}

function buildStructuredOpenClawDailyPayload(text, lines) {
  const title = truncateDiscordText(lines[0], 256);
  const fields = [];
  let inTopByProject = false;
  let pendingFinding = null;
  const flushPendingFinding = () => {
    if (pendingFinding) {
      fields.push(discordField(pendingFinding.name, pendingFinding.value));
      pendingFinding = null;
    }
  };

  for (const line of lines.slice(1)) {
    if (/^Top by project:/i.test(line)) {
      inTopByProject = true;
      continue;
    }
    if (/^Action:/i.test(line)) {
      flushPendingFinding();
      fields.push(discordField("Action", line.replace(/^Action:\s*/i, ""), true));
      continue;
    }
    if (/^Suppressed today:/i.test(line)) {
      flushPendingFinding();
      fields.push(discordField("Suppressed today", line.replace(/^Suppressed today:\s*/i, ""), true));
      continue;
    }
    if (/^Charts:/i.test(line)) {
      flushPendingFinding();
      fields.push(discordField("Charts", line.replace(/^Charts:\s*/i, ""), true));
      continue;
    }
    if (/^Runner completed/i.test(line)) {
      flushPendingFinding();
      fields.push(discordField("Run status", line));
      continue;
    }
    if (/^Link:/i.test(line)) {
      if (pendingFinding) {
        pendingFinding.value = `${pendingFinding.value}\n${line}`;
      } else {
        fields.push(discordField("Link", line.replace(/^Link:\s*/i, "")));
      }
      continue;
    }
    if (/^\d+\s+events?,/i.test(line) && pendingFinding) {
      pendingFinding.value = `${pendingFinding.value}\n${line}`;
      continue;
    }
    if (inTopByProject && /^-\s*/.test(line)) {
      flushPendingFinding();
      const named = splitNamedLine(line);
      if (named) {
        fields.push(discordField(named[0], named[1]));
      }
      continue;
    }
    const named = splitNamedLine(line);
    if (named && /^(sentry|glitchtip|analytics|github|asc|appStoreConnect|revenue|coolify|stripe|paddle)/i.test(named[0])) {
      flushPendingFinding();
      pendingFinding = { name: named[0], value: named[1] };
      continue;
    }
    if (line.trim()) {
      flushPendingFinding();
      fields.push(discordField("Detail", line));
    }
  }
  flushPendingFinding();

  return {
    content: "",
    embeds: [
      {
        title,
        color: /^OpenClaw (daily|healthcheck): OK/i.test(title) ? 0x12b76a : 0xf79009,
        fields: fields.slice(0, 20),
        footer: { text: "GROWTH_RUN" },
        timestamp: new Date().toISOString(),
      },
    ],
    fallbackText: text,
  };
}

function buildStructuredConnectorPayload(text, lines) {
  const title = truncateDiscordText(lines[0], 256);
  const fields = [];
  let description = "";
  for (const line of lines.slice(1)) {
    if (/^Secrets stay/i.test(line)) {
      description = line;
      continue;
    }
    if (/^Fix:/i.test(line)) {
      fields.push(discordField("Fix", line.replace(/^Fix:\s*/i, "")));
      continue;
    }
    if (/^At\s+\d{4}-/i.test(line)) {
      fields.push(discordField("Proof", line));
      continue;
    }
    if (/CONNECTOR_HEALTH_ALERT/i.test(line)) {
      continue;
    }
    const named = splitNamedLine(line);
    if (named) {
      fields.push(discordField(named[0], named[1]));
    } else if (line.trim()) {
      fields.push(discordField("Detail", line));
    }
  }
  return {
    content: "",
    embeds: [
      {
        title,
        description,
        color: /blocked|failed|issue/i.test(text) ? 0xd92d20 : 0xf79009,
        fields: fields.slice(0, 20),
        footer: { text: "CONNECTOR_HEALTH_ALERT" },
        timestamp: new Date().toISOString(),
      },
    ],
    fallbackText: text,
  };
}

function structuredTextToEmbedPayload(input) {
  const text = String(input || "").trim();
  if (!text) {
    return null;
  }

  const lines = text.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  if (lines.length === 0) {
    return null;
  }
  if (/^OpenClaw connector health:/i.test(lines[0]) || /CONNECTOR_HEALTH_ALERT/.test(text)) {
    return buildStructuredConnectorPayload(text, lines);
  }
  if (/^OpenClaw (daily|healthcheck)(:|\s)/i.test(lines[0])) {
    return buildStructuredOpenClawDailyPayload(text, lines);
  }
  return null;
}

function normalizeEmbedPayload(input) {
  const raw = String(input || "");
  if (process.env.OPENCLAW_DISCORD_DELIVERY_FORMAT === "embed" || process.argv.includes("--json") || raw.trim().startsWith("{")) {
    try {
      const payload = JSON.parse(raw);
      const embeds = Array.isArray(payload.embeds) ? payload.embeds : [];
      if (embeds.length > 0) {
        return {
          content: String(payload.content || "").slice(0, 2000),
          embeds: embeds.slice(0, 10),
          fallbackText: String(payload.fallbackText || payload.fallback_text || "").trim(),
        };
      }
    } catch {
      if (process.argv.includes("--json")) {
        return null;
      }
    }
  }
  return structuredTextToEmbedPayload(raw);
}

async function sendDiscordPayload(payload) {
  const sent = [];
  for (const target of DISCORD_TARGETS) {
    await validateTargetChannel(target);
    const message = await discordFetch(`/channels/${target.channelId}/messages`, {
      method: "POST",
      body: JSON.stringify({
        allowed_mentions: { parse: [], users: target.allowedMentionUsers },
        content: payload.content || "",
        embeds: payload.embeds,
      }),
    });
    sent.push({ target, message });
  }
  return sent;
}

async function sendMessage(content) {
  const embedPayload = normalizeEmbedPayload(content);
  if (embedPayload) {
    return await sendDiscordPayload(embedPayload);
  }

  const chunks = chunkMessage(content);
  if (chunks.length === 0) {
    throw new Error("Refusing to send an empty message.");
  }

  const sent = [];
  for (const target of DISCORD_TARGETS) {
    await validateTargetChannel(target);
    for (const chunk of chunks) {
      const message = await discordFetch(`/channels/${target.channelId}/messages`, {
        method: "POST",
        body: JSON.stringify({
          allowed_mentions: { parse: [], users: target.allowedMentionUsers },
          content: chunk,
        }),
      });
      sent.push({ target, message });
    }
  }
  return sent;
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf8");
}

async function watchMessages({ intervalSeconds, limit, timeoutSeconds }) {
  const initial = await readMessages({ limit });
  printMessages(initial);

  let newestId = initial.at(-1)?.id;
  const startTime = Date.now();

  while (true) {
    if (timeoutSeconds && Date.now() - startTime > timeoutSeconds * 1000) {
      return;
    }

    await new Promise((resolve) => setTimeout(resolve, intervalSeconds * 1000));
    const messages = await readMessages({ limit: 50, after: newestId });
    if (messages.length === 0) {
      continue;
    }
    printMessages(messages);
    newestId = messages.at(-1).id;
  }
}

async function main() {
  const rawArgs = process.argv.slice(2);
  if (rawArgs[0] === "--") {
    rawArgs.shift();
  }
  const [command, ...args] = rawArgs;
  if (!command || command === "--help" || command === "-h") {
    console.log(usage);
    return;
  }

  if (command === "read") {
    const limit = asPositiveInteger(readFlag(args, "--limit", "20"), "--limit");
    const messages = await readMessages({ limit });
    printMessages(messages);
    return;
  }

  if (command === "send") {
    const content = hasFlag(args, "--stdin") ? await readStdin() : args.join(" ");
    const sent = await sendMessage(content);
    for (const { target, message } of sent) {
      console.log(`sent ${target.label} ${message.id}`);
    }
    return;
  }

  if (command === "watch") {
    const intervalSeconds = asPositiveInteger(readFlag(args, "--interval", "5"), "--interval");
    const limit = asPositiveInteger(readFlag(args, "--limit", "10"), "--limit");
    await watchMessages({ intervalSeconds, limit });
    return;
  }

  if (command === "ask") {
    const requestedTimeoutSeconds = asPositiveInteger(readFlag(args, "--timeout", String(MIN_ASK_TIMEOUT_SECONDS)), "--timeout");
    const timeoutSeconds = Math.max(requestedTimeoutSeconds, MIN_ASK_TIMEOUT_SECONDS);
    const filteredArgs = args.filter((arg, index) => arg !== "--timeout" && args[index - 1] !== "--timeout");
    const sent = await sendMessage(filteredArgs.join(" "));
    console.log(`sent ${sent.map(({ target, message }) => `${target.label}:${message.id}`).join(", ")}`);
    await watchMessages({ intervalSeconds: 5, limit: 1, timeoutSeconds });
    return;
  }

  throw new Error(`Unknown command: ${command}\n\n${usage}`);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
