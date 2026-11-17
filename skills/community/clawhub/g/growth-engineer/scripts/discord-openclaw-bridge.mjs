#!/usr/bin/env node
import process from "node:process";
import { createHash } from "node:crypto";
import { promises as fs } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const DISCORD_API_BASE_URL = "https://discord.com/api/v10";
const DISCORD_REQUEST_TIMEOUT_MS = 15_000;
const DISCORD_MAX_RATE_LIMIT_RETRIES = 2;
const DISCORD_MAX_RETRY_AFTER_MS = 15_000;
const DISCORD_RECEIPT_RETENTION_MS = 14 * 24 * 60 * 60 * 1000;
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
    required: true,
  },
  {
    label: "hermes",
    guildId: ALLOWED_GUILD_ID,
    channelId: HERMES_CHANNEL_ID,
    allowedMentionUsers: [],
    required: true,
  },
];

const usage = `Usage:
  node scripts/discord-openclaw-bridge.mjs read [--limit 20]
  node scripts/discord-openclaw-bridge.mjs send "message"
  node scripts/discord-openclaw-bridge.mjs send --stdin
  node scripts/discord-openclaw-bridge.mjs preview "message"
  node scripts/discord-openclaw-bridge.mjs preview --stdin
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
    throw new DiscordBridgeError(
      "DISCORD_BOT_TOKEN is required. Put it in .env or export it in your shell.",
    );
  }
  return token;
}

class DiscordBridgeError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.name = "DiscordBridgeError";
    this.details = details;
  }
}

class DiscordTargetAggregateError extends Error {
  constructor(failures, sent) {
    const requiredFailures = failures.filter((failure) => failure.required);
    const summary = requiredFailures
      .map((failure) => `${failure.label}: ${failure.reason}`)
      .join("; ");
    super(`Discord delivery incomplete for ${requiredFailures.length} required target(s): ${summary}`);
    this.name = "DiscordTargetAggregateError";
    this.failures = failures;
    this.sent = sent;
  }
}

function sanitizeDiscordApiMessage(value) {
  return String(value || "")
    .replace(/https?:\/\/\S+/gi, "[url]")
    .replace(/<[@#][!&]?\d+>/g, "[mention]")
    .replace(/\b\d{12,}\b/g, "[id]")
    .replace(/\b[\w-]{20,}\.[\w-]{6,}\.[\w-]{20,}\b/g, "[redacted]")
    .replace(/[\u0000-\u001f\u007f]+/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 160);
}

function safeDiscordFailureReason(error) {
  if (error instanceof DiscordBridgeError) {
    return error.message;
  }
  return "Unexpected Discord delivery failure.";
}

async function readDiscordJson(response) {
  try {
    return await response.json();
  } catch {
    return undefined;
  }
}

function discordRetryAfterMs(response, payload) {
  const bodySeconds = Number(payload?.retry_after);
  const headerSeconds = Number(response.headers?.get?.("retry-after"));
  const retrySeconds = Number.isFinite(bodySeconds)
    ? bodySeconds
    : Number.isFinite(headerSeconds)
      ? headerSeconds
      : 1;
  return Math.min(
    DISCORD_MAX_RETRY_AFTER_MS,
    Math.max(0, Math.ceil(retrySeconds * 1000)),
  );
}

function waitFor(milliseconds) {
  return new Promise((resolveWait) => setTimeout(resolveWait, milliseconds));
}

async function discordFetch(path, options = {}, runtime = {}) {
  const fetchImpl = runtime.fetchImpl ?? globalThis.fetch;
  const sleepImpl = runtime.sleepImpl ?? waitFor;
  const token = runtime.token ?? getToken();
  const timeoutMs = runtime.timeoutMs ?? DISCORD_REQUEST_TIMEOUT_MS;
  const maxRateLimitRetries = runtime.maxRateLimitRetries ?? DISCORD_MAX_RATE_LIMIT_RETRIES;

  for (let attempt = 0; attempt <= maxRateLimitRetries; attempt += 1) {
    const controller = new AbortController();
    const parentSignal = options.signal;
    const forwardAbort = () => controller.abort();
    if (parentSignal?.aborted) {
      controller.abort();
    } else {
      parentSignal?.addEventListener?.("abort", forwardAbort, { once: true });
    }
    const timeout = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const response = await fetchImpl(`${DISCORD_API_BASE_URL}${path}`, {
        ...options,
        signal: controller.signal,
        headers: {
          Authorization: `Bot ${token}`,
          "Content-Type": "application/json",
          ...options.headers,
        },
      });

      if (response.status === 429) {
        const retryPayload = await readDiscordJson(response);
        if (attempt >= maxRateLimitRetries) {
          throw new DiscordBridgeError(
            `Discord rate limit persisted after ${attempt + 1} attempt(s).`,
            { status: 429, retryable: true },
          );
        }
        await sleepImpl(discordRetryAfterMs(response, retryPayload));
        continue;
      }

      if (!response.ok) {
        const errorPayload = await readDiscordJson(response);
        const code = sanitizeDiscordApiMessage(errorPayload?.code);
        const detail = sanitizeDiscordApiMessage(errorPayload?.message);
        const safeDetail = [
          code ? `code ${code}` : "",
          detail,
        ].filter(Boolean).join(": ");
        throw new DiscordBridgeError(
          `Discord API request failed (HTTP ${response.status}${safeDetail ? `, ${safeDetail}` : ""}).`,
          { status: response.status, retryable: response.status >= 500 },
        );
      }

      if (response.status === 204) {
        return undefined;
      }
      const payload = await readDiscordJson(response);
      if (payload === undefined) {
        throw new DiscordBridgeError("Discord returned an unreadable response.");
      }
      return payload;
    } catch (error) {
      if (error instanceof DiscordBridgeError) {
        throw error;
      }
      if (parentSignal?.aborted) {
        throw new DiscordBridgeError("Discord request was cancelled.", { retryable: false });
      }
      if (controller.signal.aborted) {
        throw new DiscordBridgeError(
          `Discord request timed out after ${Math.ceil(timeoutMs / 1000)} seconds.`,
          { retryable: true },
        );
      }
      throw new DiscordBridgeError(
        "Discord request failed before a response was received.",
        { retryable: true },
      );
    } finally {
      clearTimeout(timeout);
      parentSignal?.removeEventListener?.("abort", forwardAbort);
    }
  }

  throw new DiscordBridgeError("Discord request exhausted its retry budget.", { retryable: true });
}

function getPrimaryTarget() {
  return DISCORD_TARGETS.find((target) => target.label === PRIMARY_TARGET_LABEL) ?? DISCORD_TARGETS[0];
}

async function validateTargetChannel(target) {
  const channel = await discordFetch(`/channels/${target.channelId}`);
  if (channel.guild_id !== target.guildId) {
    throw new DiscordBridgeError(
      `Refusing the ${target.label} target because Discord returned an unexpected guild.`,
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
    value: truncateDiscordText(value, 900) || "-",
    inline,
  };
}

const CONNECTOR_LABELS = new Map([
  ["analytics", "AnalyticsCLI"],
  ["analyticscli", "AnalyticsCLI"],
  ["appstoreconnect", "App Store Connect"],
  ["asc", "App Store Connect"],
  ["revenue", "Revenue"],
  ["revenuecat", "RevenueCat"],
  ["sentry", "Sentry"],
  ["glitchtip", "GlitchTip"],
  ["github", "GitHub"],
  ["coolify", "Deployments"],
  ["seo", "Search data"],
  ["gsc", "Google Search Console"],
  ["stripe", "Stripe"],
  ["paddle", "Paddle"],
]);

const FIELD_LABELS = new Map([
  ["action", "Next action"],
  ["cadence", "Schedule"],
  ["charts", "Charts"],
  ["charts generated", "Charts"],
  ["detail", "What happened"],
  ["findings", "Findings"],
  ["fix", "Next action"],
  ["generated proposals", "Findings"],
  ["link", "Evidence"],
  ["proof", "Last checked"],
  ["run status", "Status"],
  ["sources", "Data checked"],
  ["sources inspected", "Data checked"],
  ["suppressed today", "Already reported"],
]);

function compactWhitespace(value) {
  return String(value || "")
    .replace(/[ \t]+/g, " ")
    .replace(/ *\n */g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function formatLinksWithoutPreviews(value, label = "Evidence") {
  let text = String(value || "");
  text = text.replace(/\((https?:\/\/[^\s)]+)\)/gi, (_match, url) => `[${label}](${url})`);
  return text.replace(/https?:\/\/[^\s<>)\]]+/gi, (match, offset, source) => {
    if (source.slice(Math.max(0, offset - 2), offset) === "](" || source[offset - 1] === "<") {
      return match;
    }
    const trailing = match.match(/[.,;:!?]+$/)?.[0] || "";
    const url = trailing ? match.slice(0, -trailing.length) : match;
    return `[${label}](${url})${trailing}`;
  });
}

function understandableText(value) {
  return compactWhitespace(value)
    .replace(/\bnot_connected\b/gi, "Not connected")
    .replace(/\bsource collection\b/gi, "data collection")
    .replace(/\bsource is still disabled\b/gi, "connection is disabled")
    .replace(/\bgenerated proposals?\b/gi, "findings")
    .replace(/\bpreviously reported finding\(s\)/gi, "findings already reported")
    .replace(/\bGitHub artifact creation was attempted for the findings\.?/gi, "Review the GitHub result and assign an owner.")
    .replace(/\bGitHub artifact creation was attempted\.?/gi, "Review the GitHub result and assign an owner.")
    .replace(/\bGitHub artifact attempted\.?/gi, "Review the GitHub result and assign an owner.")
    .replace(/\bexternal alert only\.?/gi, "Review the alert and assign an owner.");
}

function cleanDisplayText(value, linkLabel = "Evidence") {
  return formatLinksWithoutPreviews(understandableText(value), linkLabel);
}

function humanConnectorLabel(value) {
  const text = compactWhitespace(value).replace(/^[-*]\s*/, "");
  const mapped = CONNECTOR_LABELS.get(text.toLowerCase().replace(/[^a-z0-9]/g, ""));
  return mapped || text || "Connection";
}

function titleCaseWords(value) {
  return String(value || "")
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

function humanPriority(value) {
  const priority = String(value || "").trim().toLowerCase();
  if (priority === "p0" || priority === "critical" || priority === "urgent") return "Critical";
  if (priority === "p1" || priority === "high") return "High";
  if (priority === "p2" || priority === "medium") return "Medium";
  if (priority === "p3" || priority === "low") return "Low";
  return titleCaseWords(priority || "Finding");
}

function humanArea(value) {
  const area = String(value || "").trim().toLowerCase();
  const known = {
    acquisition: "Acquisition",
    activation: "Activation",
    agent: "Agent workflow",
    data_quality: "Data quality",
    "data-quality": "Data quality",
    engagement: "Engagement",
    feedback: "Feedback",
    monetization: "Revenue",
    onboarding: "Onboarding",
    paywall: "Paywall",
    performance: "Performance",
    reliability: "Reliability",
    retention: "Retention",
    revenue: "Revenue",
    web: "Web",
  };
  return known[area] || titleCaseWords(area || "Product");
}

function humanFieldLabel(value) {
  const text = compactWhitespace(value);
  return FIELD_LABELS.get(text.toLowerCase()) || humanConnectorLabel(text);
}

function humanSchedule(value) {
  const schedule = compactWhitespace(value).toLowerCase();
  const known = {
    "ad-hoc growth pass": "On demand",
    "deep-analysis": "Deep analysis",
    daily: "Daily",
    healthcheck: "Health check",
    monthly: "Monthly",
    strategy: "Strategy review",
    weekly: "Weekly",
    "weekly-strategy": "Weekly strategy",
  };
  return known[schedule] || titleCaseWords(schedule);
}

function fitDiscordFields(fields, characterBudget) {
  const fitted = [];
  let remaining = Math.max(0, characterBudget);
  for (const field of fields.slice(0, 20)) {
    const name = truncateDiscordText(field?.name, 256) || "Detail";
    const availableForValue = Math.min(900, remaining - name.length);
    if (availableForValue < 1) break;
    const value = truncateDiscordText(field?.value, availableForValue) || "-";
    fitted.push({ name, value, inline: field?.inline === true });
    remaining -= name.length + value.length;
  }
  return fitted;
}

function splitNamedLine(line) {
  const clean = String(line || "").replace(/^-\s*/, "").trim();
  const bracketMarker = clean.indexOf(": [");
  if (bracketMarker > 0) {
    return [clean.slice(0, bracketMarker).trim(), clean.slice(bracketMarker + 2).trim()];
  }
  const splitAt = clean.indexOf(": ");
  if (splitAt > 0) {
    return [clean.slice(0, splitAt).trim(), clean.slice(splitAt + 2).trim()];
  }
  return null;
}

function makeStructuredPayload({ title, description = "", color, fields, footer, timestamp, fallbackText }) {
  const safeTitle = truncateDiscordText(title, 100);
  const safeDescription = description
    ? truncateDiscordText(cleanDisplayText(description), 600)
    : "";
  const safeFooter = truncateDiscordText(footer, 120);
  const fieldBudget = 5_700 - safeTitle.length - safeDescription.length - safeFooter.length;
  return {
    content: "",
    embeds: [
      {
        title: safeTitle,
        ...(safeDescription ? { description: safeDescription } : {}),
        color,
        fields: fitDiscordFields(fields, fieldBudget),
        footer: { text: safeFooter },
        timestamp: timestamp || new Date().toISOString(),
      },
    ],
    fallbackText,
  };
}

function parseFindingCount(value) {
  const match = String(value || "").match(/(\d+)\s+(?:finding|proposal|issue)/i);
  return match ? Number(match[1]) : 0;
}

function formatProjectFindings(value) {
  const entries = compactWhitespace(value)
    .split(/\s+\|\s+|\n+/)
    .map((entry) => entry.replace(/^[-*•]\s*/, "").trim())
    .filter(Boolean);
  return entries.slice(0, 5).map((entry) => `• ${cleanDisplayText(entry)}`).join("\n");
}

function defaultNextAction(findingCount) {
  return findingCount > 0
    ? "Review the highest-priority finding, assign an owner, and define its verification metric."
    : "No action needed.";
}

function buildStructuredOpenClawDailyPayload(text, lines) {
  const isHealthcheck = /^OpenClaw healthcheck/i.test(lines[0]);
  const findingCount = parseFindingCount(lines[0]);
  const isOk = findingCount === 0
    && (/\bOK\b/i.test(lines[0]) || /:\s*0\s+finding/i.test(lines[0]));
  const projects = [];
  let inTopByProject = false;
  let action = "";
  let alreadyReported = "";
  let chartCount = "";
  let explicitStatus = "";
  const legacyFindings = [];
  let pendingLegacyFinding = null;
  const flushLegacyFinding = () => {
    if (pendingLegacyFinding) legacyFindings.push(pendingLegacyFinding);
    pendingLegacyFinding = null;
  };

  for (const line of lines.slice(1)) {
    if (/^Top by project:/i.test(line)) {
      inTopByProject = true;
      continue;
    }
    if (/^Action:/i.test(line)) {
      flushLegacyFinding();
      action = line.replace(/^Action:\s*/i, "");
      inTopByProject = false;
      continue;
    }
    if (/^Suppressed today:/i.test(line)) {
      flushLegacyFinding();
      alreadyReported = line.replace(/^Suppressed today:\s*/i, "");
      inTopByProject = false;
      continue;
    }
    if (/^Charts:/i.test(line)) {
      flushLegacyFinding();
      chartCount = line.replace(/^Charts:\s*/i, "");
      inTopByProject = false;
      continue;
    }
    if (/^Runner completed/i.test(line)) {
      flushLegacyFinding();
      explicitStatus = line;
      inTopByProject = false;
      continue;
    }
    if (inTopByProject && /^-\s*/.test(line)) {
      const named = splitNamedLine(line);
      if (named) projects.push({ project: named[0], findings: named[1] });
      continue;
    }
    if (/^Link:/i.test(line) && pendingLegacyFinding) {
      pendingLegacyFinding.details.push(line.replace(/^Link:\s*/i, ""));
      continue;
    }
    if (/^\d+\s+events?,/i.test(line) && pendingLegacyFinding) {
      pendingLegacyFinding.details.push(line);
      continue;
    }
    const named = splitNamedLine(line);
    if (
      named
      && /^(sentry|glitchtip|analytics|analyticscli|github|asc|appStoreConnect|revenue|revenuecat|coolify|seo|stripe|paddle)/i.test(named[0])
    ) {
      flushLegacyFinding();
      pendingLegacyFinding = { source: named[0], finding: named[1], details: [] };
    }
  }
  flushLegacyFinding();

  const status = explicitStatus
    ? cleanDisplayText(explicitStatus)
    : isOk
      ? "No new findings"
      : `${findingCount} new finding${findingCount === 1 ? "" : "s"} ready for review`;
  const visibleScopes = projects.length + legacyFindings.length;
  const impact = findingCount > 0 && projects.length > 0 && legacyFindings.length === 0
    ? `${projects.length} project${projects.length === 1 ? " has" : "s have"} a new actionable signal.`
    : findingCount > 0 && legacyFindings.length > 0 && projects.length === 0
      ? `${legacyFindings.length} data source${legacyFindings.length === 1 ? " has" : "s have"} a new actionable signal.`
      : findingCount > 0 && visibleScopes > 0
        ? `${visibleScopes} project/data-source entr${visibleScopes === 1 ? "y has" : "ies have"} a new actionable signal.`
    : findingCount > 0
      ? `${findingCount} actionable signal${findingCount === 1 ? "" : "s"} require review.`
    : "No new actionable signal was produced.";
  const fields = [
    discordField("Status", status, true),
    discordField("Impact", impact),
    discordField("Next action", cleanDisplayText(action || defaultNextAction(findingCount))),
  ];
  if (alreadyReported) fields.push(discordField("Already reported", cleanDisplayText(alreadyReported), true));
  if (chartCount) fields.push(discordField("Charts", cleanDisplayText(chartCount), true));
  for (const entry of projects.slice(0, 8)) {
    fields.push(discordField(`Project · ${entry.project}`, formatProjectFindings(entry.findings)));
  }
  for (const entry of legacyFindings.slice(0, Math.max(0, 8 - projects.length))) {
    const priorityMatch = entry.finding.match(/^\[(p[0-3]|critical|urgent|high|medium|low)\]\s*(.+)$/i);
    fields.push(discordField(
      `Source · ${humanConnectorLabel(entry.source)}${priorityMatch ? ` · ${humanPriority(priorityMatch[1])}` : ""}`,
      formatProjectFindings([priorityMatch?.[2] || entry.finding, ...entry.details].join("\n")),
    ));
  }

  return makeStructuredPayload({
    title: `${isHealthcheck ? "Health check" : "Daily check"} · ${isOk ? "Clear" : `${findingCount} finding${findingCount === 1 ? "" : "s"}`}`,
    color: isOk ? 0x12b76a : 0xf79009,
    fields,
    footer: "Growth Engineer",
    fallbackText: text,
  });
}

function connectorEntryField(entry) {
  const status = titleCaseWords(
    String(entry.status || "Needs attention")
      .replace(/\bnot_connected\b/gi, "Not connected")
      .replace(/_/g, " "),
  );
  const details = [
    `**${status}**`,
    entry.detail ? cleanDisplayText(entry.detail) : "",
    entry.fix ? `Next: ${cleanDisplayText(entry.fix, "Open")}` : "",
  ].filter(Boolean);
  return discordField(humanConnectorLabel(entry.name), details.join("\n"));
}

function buildConnectorPayloadFromEntries({
  text,
  entries,
  checkedAt = "",
  timestamp,
  kind = "connector probe",
}) {
  const blocked = entries.some((entry) => /blocked|failed|error/i.test(String(entry.status || entry.detail)));
  const count = entries.length;
  const isSourceCollection = kind === "source collection";
  const fields = [
    discordField(
      "Status",
      `${count} ${isSourceCollection ? "data source" : "connection"}${count === 1 ? "" : "s"} ${count === 1 ? "needs" : "need"} attention`,
      true,
    ),
    discordField(
      "Impact",
      isSourceCollection
        ? "This review may be incomplete because scheduled data collection failed."
        : "Scheduled analysis may be incomplete while these connections are unavailable.",
    ),
    discordField(
      "Next action",
      isSourceCollection
        ? "Repair or retry the affected data source, then rerun the Growth Engineer."
        : "Repair the affected connection, then rerun the health check.",
    ),
  ];
  if (checkedAt) fields.push(discordField("Last checked", cleanDisplayText(checkedAt), true));
  for (const entry of entries.slice(0, 10)) fields.push(connectorEntryField(entry));
  if (count > 10) fields.push(discordField("More connections", `${count - 10} additional connections need attention.`));

  return makeStructuredPayload({
    title: `${isSourceCollection ? "Data collection" : "Connections"} · ${count} issue${count === 1 ? "" : "s"}`,
    color: blocked ? 0xd92d20 : 0xf79009,
    fields,
    footer: `Growth Engineer · ${isSourceCollection ? "data collection" : "connector health"}`,
    timestamp,
    fallbackText: text,
  });
}

function buildStructuredConnectorPayload(text, lines) {
  const kind = /^OpenClaw source collection:/i.test(lines[0])
    ? "source collection"
    : "connector probe";
  const entries = [];
  let current = null;
  let checkedAt = "";
  const pushCurrent = () => {
    if (current) entries.push(current);
    current = null;
  };

  for (const line of lines.slice(1)) {
    if (/^Secrets stay/i.test(line) || /CONNECTOR_HEALTH_ALERT/i.test(line)) continue;
    if (/^At\s+\d{4}-/i.test(line)) {
      checkedAt = line;
      continue;
    }
    if (/^Fix:/i.test(line)) {
      if (current) current.fix = line.replace(/^Fix:\s*/i, "");
      continue;
    }
    if (/^-\s*/.test(line)) {
      pushCurrent();
      const named = splitNamedLine(line);
      if (!named) continue;
      const statusMatch = named[1].match(/^([a-z_ -]+)\s+-\s+([\s\S]+)$/i);
      current = {
        name: named[0],
        status: statusMatch?.[1] || "Needs attention",
        detail: statusMatch?.[2] || named[1],
        fix: "",
      };
      continue;
    }
    if (current && line.trim()) {
      current.detail = `${current.detail}\n${line}`;
    }
  }
  pushCurrent();

  if (entries.length === 0) {
    const count = parseFindingCount(lines[0]) || 1;
    for (let index = 0; index < count; index += 1) {
      entries.push({ name: `Connection ${index + 1}`, status: "Needs attention", detail: "", fix: "" });
    }
  }
  return buildConnectorPayloadFromEntries({ text, entries, checkedAt, kind });
}

function buildStructuredConnectorRecoveryPayload(text, kind, timestamp) {
  const isSourceCollection = kind === "source collection";
  const title = isSourceCollection
    ? "Data collection · Recovered"
    : "Connection check · Recovered";
  const impact = isSourceCollection
    ? "Scheduled reviews can use the restored data source again."
    : "Scheduled reviews can use the restored connection again.";
  return makeStructuredPayload({
    title,
    color: 0x12b76a,
    fields: [
      discordField("Status", "Recovered", true),
      discordField("Impact", impact),
      discordField(
        "Next action",
        "No repair action is needed. Confirm that the next scheduled run completes normally.",
      ),
    ],
    footer: "Growth Engineer · recovery",
    timestamp,
    fallbackText: text,
  });
}

function parsePriorityArea(value) {
  const match = String(value || "").match(/\((p[0-3]|critical|urgent|high|medium|low)\s*,\s*([^)]+)\)\s*$/i);
  if (!match) return null;
  return {
    priority: humanPriority(match[1]),
    area: humanArea(match[2]),
    title: String(value).slice(0, match.index).trim(),
  };
}

function buildStructuredGrowthRunPayload(text, lines) {
  let schedule = "";
  let dataChecked = "";
  let findingCount = 0;
  let summary = "";
  let chartCount = "";
  let action = "";
  let inFindings = false;
  let inCharts = false;
  const findings = [];
  let currentFinding = null;

  for (const line of lines.slice(1)) {
    if (/^(Top findings|App-by-app findings and next steps):/i.test(line)) {
      inFindings = true;
      inCharts = false;
      continue;
    }
    if (/^Cadence:/i.test(line)) {
      schedule = line.replace(/^Cadence:\s*/i, "");
      continue;
    }
    if (/^Sources inspected:/i.test(line)) {
      dataChecked = line.replace(/^Sources inspected:\s*/i, "");
      continue;
    }
    if (/^Generated proposals:/i.test(line)) {
      findingCount = Number(line.replace(/^Generated proposals:\s*/i, "")) || 0;
      continue;
    }
    if (/^Summary:/i.test(line)) {
      summary = line.replace(/^Summary:\s*/i, "");
      continue;
    }
    if (/^GitHub artifact/i.test(line)) {
      action = line;
      continue;
    }
    if (/^Charts generated:/i.test(line)) {
      chartCount = line.replace(/^Charts generated:\s*/i, "");
      inCharts = true;
      inFindings = false;
      continue;
    }
    if (/^No secrets/i.test(line)) continue;
    if (inCharts && /^-\s*/.test(line)) continue;
    if (inFindings && /^-\s*/.test(line)) {
      const raw = line.replace(/^-\s*/, "");
      const parsed = parsePriorityArea(raw);
      currentFinding = {
        title: parsed?.title || raw,
        priority: parsed?.priority || "Finding",
        area: parsed?.area || "Product",
        evidence: [],
        impact: "",
      };
      findings.push(currentFinding);
      continue;
    }
    if (currentFinding && /^Evidence:/i.test(line)) {
      currentFinding.evidence.push(line.replace(/^Evidence:\s*/i, ""));
      continue;
    }
    if (currentFinding && /^Impact:/i.test(line)) {
      currentFinding.impact = line.replace(/^Impact:\s*/i, "");
    }
  }

  if (findingCount === 0) findingCount = findings.length;
  const impactLines = findings.map((finding) => finding.impact).filter(Boolean).slice(0, 3);
  const affectedAreas = [...new Set(findings.map((finding) => finding.area).filter(Boolean))];
  const impact = impactLines.length > 0
    ? impactLines.map((line) => `• ${cleanDisplayText(line)}`).join("\n")
    : findingCount > 0
      ? `${findingCount === 1 ? "1 opportunity" : `${findingCount} opportunities`} across ${affectedAreas.join(", ") || "the product"} require review.`
      : "No new actionable signal was produced.";
  const fields = [
    discordField("Status", `Run complete · ${findingCount} finding${findingCount === 1 ? "" : "s"} ready for review`, true),
    discordField("Impact", impact),
    discordField("Next action", cleanDisplayText(action || defaultNextAction(findingCount))),
  ];
  if (schedule) fields.push(discordField("Schedule", humanSchedule(schedule), true));
  if (dataChecked) {
    const readableSources = dataChecked
      .split(",")
      .map((source) => humanConnectorLabel(source))
      .join(" · ");
    fields.push(discordField("Data checked", readableSources, true));
  }
  if (chartCount) fields.push(discordField("Charts", cleanDisplayText(chartCount), true));
  for (const [index, finding] of findings.slice(0, 8).entries()) {
    const parts = [`**${cleanDisplayText(finding.title)}**`];
    if (finding.impact) parts.push(`Impact: ${cleanDisplayText(finding.impact)}`);
    if (finding.evidence.length > 0) {
      parts.push(`Evidence: ${finding.evidence.slice(0, 2).map((item) => cleanDisplayText(item)).join(" · ")}`);
    }
    fields.push(discordField(`Finding ${index + 1} · ${finding.priority} · ${finding.area}`, parts.join("\n")));
  }

  return makeStructuredPayload({
    title: `Growth review · ${findingCount} finding${findingCount === 1 ? "" : "s"}`,
    description: summary,
    color: findingCount > 0 ? 0xf79009 : 0x12b76a,
    fields,
    footer: "Growth Engineer",
    fallbackText: text,
  });
}

function normalizeGenericEmbed(embed) {
  const rawFields = Array.isArray(embed?.fields)
    ? embed.fields.slice(0, 20).map((field) =>
        discordField(
          field?.name,
          cleanDisplayText(field?.value),
          field?.inline === true,
        ))
    : [];
  const title = embed?.title ? truncateDiscordText(cleanDisplayText(embed.title), 256) : "";
  const description = embed?.description
    ? truncateDiscordText(cleanDisplayText(embed.description), 1000)
    : "";
  const footerText = embed?.footer?.text
    ? truncateDiscordText(cleanDisplayText(embed.footer.text), 200)
    : "";
  return {
    ...embed,
    ...(title ? { title } : {}),
    ...(description ? { description } : {}),
    fields: fitDiscordFields(rawFields, 5_700 - title.length - description.length - footerText.length),
    ...(footerText
      ? { footer: { ...embed.footer, text: footerText } }
      : {}),
  };
}

function isConnectorEmbed(embed) {
  return /connector health|CONNECTOR_HEALTH_ALERT/i.test(
    `${embed?.title || ""} ${embed?.footer?.text || ""}`,
  );
}

function isConnectorRecoveryEmbed(embed) {
  return /(?:connector probe|source collection)\s+recovered|CONNECTOR_HEALTH_RECOVERED/i.test(
    `${embed?.title || ""} ${embed?.footer?.text || ""}`,
  );
}

function isGrowthEmbed(embed) {
  return /Growth Engineer|GROWTH_RUN|OpenClaw (?:daily|healthcheck|growth run|growth review|connector health|connector probe|source collection)|CONNECTOR_HEALTH_(?:ALERT|RECOVERED)/i.test(
    `${embed?.title || ""} ${embed?.footer?.text || ""}`,
  );
}

function normalizeExistingGrowthEmbed(embed, fallbackText) {
  if (isConnectorRecoveryEmbed(embed)) {
    const kind = /source collection/i.test(String(embed?.title || ""))
      ? "source collection"
      : "connector probe";
    return buildStructuredConnectorRecoveryPayload(
      fallbackText,
      kind,
      embed?.timestamp,
    ).embeds[0];
  }
  if (isConnectorEmbed(embed)) {
    const entries = (Array.isArray(embed?.fields) ? embed.fields : []).map((field) => {
      const lines = String(field?.value || "").split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
      const statusLine = lines.find((line) => /^Status:/i.test(line));
      const fixLine = lines.find((line) => /^Fix:/i.test(line));
      const detail = lines.filter((line) => !/^Status:|^Fix:/i.test(line)).join("\n");
      return {
        name: field?.name || "Connection",
        status: statusLine?.replace(/^Status:\s*/i, "") || "Needs attention",
        detail,
        fix: fixLine?.replace(/^Fix:\s*/i, "") || "",
      };
    });
    return buildConnectorPayloadFromEntries({
      text: fallbackText,
      entries,
      timestamp: embed?.timestamp,
      kind: /source collection/i.test(String(embed?.title || ""))
        ? "source collection"
        : "connector probe",
    }).embeds[0];
  }

  const sourceFields = Array.isArray(embed?.fields) ? embed.fields : [];
  const metaNames = /^(Cadence|Sources|Findings|Action|Suppressed today|Charts)$/i;
  const findings = sourceFields.filter((field) => !metaNames.test(String(field?.name || "")));
  const findingCountField = sourceFields.find((field) => /^Findings$/i.test(String(field?.name || "")));
  const findingCount = Number(findingCountField?.value) || parseFindingCount(embed?.title) || findings.length;
  const actionField = sourceFields.find((field) => /^Action$/i.test(String(field?.name || "")));
  const isDaily = /OpenClaw daily/i.test(String(embed?.title || ""));
  const isHealthcheck = /OpenClaw healthcheck/i.test(String(embed?.title || ""));
  const fields = [
    discordField(
      "Status",
      findingCount > 0
        ? `${findingCount} finding${findingCount === 1 ? "" : "s"} ready for review`
        : "No new findings",
      true,
    ),
    discordField(
      "Impact",
      findingCount > 0
        ? `${findingCount} product opportunit${findingCount === 1 ? "y requires" : "ies require"} review.`
        : "No new actionable signal was produced.",
    ),
    discordField("Next action", cleanDisplayText(actionField?.value || defaultNextAction(findingCount))),
  ];
  for (const field of sourceFields.filter((entry) => /^(Cadence|Sources|Suppressed today|Charts)$/i.test(String(entry?.name || "")))) {
    let value = cleanDisplayText(field.value);
    if (/^Cadence$/i.test(String(field.name))) value = humanSchedule(field.value);
    if (/^Sources$/i.test(String(field.name))) {
      value = String(field.value || "")
        .split(",")
        .map((source) => humanConnectorLabel(source))
        .join(" · ");
    }
    fields.push(discordField(humanFieldLabel(field.name), value, field.inline === true));
  }
  for (const [index, field] of findings.slice(0, 8).entries()) {
    const priorityArea = String(field?.name || "").split(/\s*•\s*/);
    const label = priorityArea.length === 2
      ? `Finding ${index + 1} · ${humanPriority(priorityArea[0])} · ${humanArea(priorityArea[1])}`
      : `${isDaily || isHealthcheck ? "Project" : "Finding"} · ${field?.name || `Finding ${index + 1}`}`;
    fields.push(discordField(label, formatProjectFindings(field?.value)));
  }
  return makeStructuredPayload({
    title: `${isDaily ? "Daily check" : isHealthcheck ? "Health check" : "Growth review"} · ${
      findingCount > 0
        ? `${findingCount} finding${findingCount === 1 ? "" : "s"}`
        : "Clear"
    }`,
    description: /No secrets/i.test(String(embed?.description || "")) ? "" : embed?.description,
    color: findingCount > 0 ? 0xf79009 : 0x12b76a,
    fields,
    footer: "Growth Engineer",
    timestamp: embed?.timestamp,
    fallbackText,
  }).embeds[0];
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
  const recoveryMatch = lines[0].match(/^OpenClaw (connector probe|source collection) recovered\.?$/i);
  if (recoveryMatch || /CONNECTOR_HEALTH_RECOVERED/.test(text)) {
    return buildStructuredConnectorRecoveryPayload(
      text,
      recoveryMatch?.[1]?.toLowerCase() || "connector probe",
    );
  }
  if (
    /^OpenClaw (?:connector health|source collection):/i.test(lines[0])
    || /CONNECTOR_HEALTH_ALERT/.test(text)
  ) {
    return buildStructuredConnectorPayload(text, lines);
  }
  if (/^OpenClaw (daily|healthcheck)(:|\s)/i.test(lines[0])) {
    return buildStructuredOpenClawDailyPayload(text, lines);
  }
  if (/^OpenClaw Growth run finished/i.test(lines[0])) {
    return buildStructuredGrowthRunPayload(text, lines);
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
        const fallbackText = String(payload.fallbackText || payload.fallback_text || "").trim();
        const fromFallback = fallbackText ? structuredTextToEmbedPayload(fallbackText) : null;
        if (fromFallback) {
          const originalTimestamp = embeds[0]?.timestamp;
          if (originalTimestamp) fromFallback.embeds[0].timestamp = originalTimestamp;
          return fromFallback;
        }
        return {
          content: truncateDiscordText(formatLinksWithoutPreviews(payload.content, "Open"), 2000),
          embeds: embeds.slice(0, 10).map((embed) =>
            isGrowthEmbed(embed)
              ? normalizeExistingGrowthEmbed(embed, fallbackText)
              : normalizeGenericEmbed(embed)),
          fallbackText,
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

async function deliverToTargets(deliverTarget, targets = DISCORD_TARGETS) {
  const settled = await Promise.allSettled(
    targets.map(async (target) => ({
      target,
      messages: await deliverTarget(target),
    })),
  );
  const sent = [];
  const failures = [];

  for (const [index, result] of settled.entries()) {
    const target = targets[index];
    if (result.status === "fulfilled") {
      for (const message of result.value.messages) {
        sent.push({ target, message });
      }
      continue;
    }
    failures.push({
      label: target.label,
      required: target.required !== false,
      reason: safeDiscordFailureReason(result.reason),
    });
  }

  const requiredFailures = failures.filter((failure) => failure.required);
  if (requiredFailures.length > 0) {
    throw new DiscordTargetAggregateError(failures, sent);
  }
  for (const failure of failures) {
    console.warn(`optional Discord target failed (${failure.label}): ${failure.reason}`);
  }
  return sent;
}

async function readDeliveryReceipts(receiptPath) {
  if (!receiptPath) return { version: 1, events: {} };
  try {
    const parsed = JSON.parse(await fs.readFile(receiptPath, "utf8"));
    return parsed?.events && typeof parsed.events === "object"
      ? { version: 1, events: parsed.events }
      : { version: 1, events: {} };
  } catch {
    return { version: 1, events: {} };
  }
}

async function writeDeliveryReceipts(receiptPath, state) {
  if (!receiptPath) return;
  const cutoff = Date.now() - DISCORD_RECEIPT_RETENTION_MS;
  const events = Object.fromEntries(
    Object.entries(state?.events || {})
      .filter(([, entry]) => {
        const updatedAt = Date.parse(String(entry?.updatedAt || ""));
        return !Number.isFinite(updatedAt) || updatedAt >= cutoff;
      })
      .slice(-500),
  );
  await fs.mkdir(dirname(receiptPath), { recursive: true });
  const temporaryPath = `${receiptPath}.${process.pid}.${Date.now()}.tmp`;
  await fs.writeFile(
    temporaryPath,
    `${JSON.stringify({ version: 1, events }, null, 2)}\n`,
    { encoding: "utf8", mode: 0o600 },
  );
  await fs.rename(temporaryPath, receiptPath);
}

async function deliverToTargetsWithReceipts(
  deliverTarget,
  {
    eventId = "",
    targets = DISCORD_TARGETS,
    receiptPath = process.env.OPENCLAW_DISCORD_RECEIPT_PATH || "",
    loadReceipts = readDeliveryReceipts,
    saveReceipts = writeDeliveryReceipts,
  } = {},
) {
  const normalizedEventId = String(eventId || "").trim();
  if (!normalizedEventId || !receiptPath) {
    return deliverToTargets(deliverTarget, targets);
  }
  const eventKey = createHash("sha256")
    .update(normalizedEventId)
    .digest("hex");
  const state = await loadReceipts(receiptPath);
  const event = state.events?.[eventKey] || { targets: {} };
  const pendingTargets = targets.filter(
    (target) => event.targets?.[target.label]?.sent !== true,
  );
  if (pendingTargets.length === 0) return [];

  const persistSent = async (sent) => {
    const nextTargets = { ...(event.targets || {}) };
    for (const { target } of sent) {
      nextTargets[target.label] = {
        sent: true,
        updatedAt: new Date().toISOString(),
      };
    }
    state.events = {
      ...(state.events || {}),
      [eventKey]: {
        targets: nextTargets,
        updatedAt: new Date().toISOString(),
      },
    };
    await saveReceipts(receiptPath, state);
  };

  try {
    const sent = await deliverToTargets(deliverTarget, pendingTargets);
    await persistSent(sent);
    return sent;
  } catch (error) {
    if (error instanceof DiscordTargetAggregateError) {
      await persistSent(error.sent);
    }
    throw error;
  }
}

async function sendDiscordPayload(payload, eventId = "") {
  return deliverToTargetsWithReceipts(async (target) => {
    await validateTargetChannel(target);
    const message = await discordFetch(`/channels/${target.channelId}/messages`, {
      method: "POST",
      body: JSON.stringify({
        allowed_mentions: { parse: [], users: target.allowedMentionUsers },
        content: payload.content || "",
        embeds: payload.embeds,
      }),
    });
    return [message];
  }, { eventId });
}

async function sendMessage(content) {
  const eventId = String(
    process.env.OPENCLAW_NOTIFICATION_EVENT_ID || "",
  ).trim();
  const embedPayload = normalizeEmbedPayload(content);
  if (embedPayload) {
    return await sendDiscordPayload(embedPayload, eventId);
  }

  const chunks = chunkMessage(content);
  if (chunks.length === 0) {
    throw new Error("Refusing to send an empty message.");
  }

  return deliverToTargetsWithReceipts(async (target) => {
    await validateTargetChannel(target);
    const sent = [];
    for (const chunk of chunks) {
      const message = await discordFetch(`/channels/${target.channelId}/messages`, {
        method: "POST",
        body: JSON.stringify({
          allowed_mentions: { parse: [], users: target.allowedMentionUsers },
          content: chunk,
        }),
      });
      sent.push(message);
    }
    return sent;
  }, { eventId });
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

  if (command === "preview") {
    const content = hasFlag(args, "--stdin") ? await readStdin() : args.join(" ");
    const payload = normalizeEmbedPayload(content);
    console.log(JSON.stringify(
      payload ?? {
        content: "",
        embeds: [],
        plainTextChunks: chunkMessage(content),
      },
      null,
      2,
    ));
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

function printSuccessfulDeliveries(sent) {
  for (const { target, message } of sent) {
    console.log(`sent ${target.label} ${message.id}`);
  }
}

const isDirectExecution = process.argv[1]
  && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url));

if (isDirectExecution) {
  main().catch((error) => {
    if (error instanceof DiscordTargetAggregateError) {
      printSuccessfulDeliveries(error.sent);
      for (const failure of error.failures) {
        console.error(`failed ${failure.label}: ${failure.reason}`);
      }
    } else {
      console.error(
        error instanceof DiscordBridgeError
          ? error.message
          : sanitizeDiscordApiMessage(error?.message) || "Unexpected Discord bridge failure.",
      );
    }
    process.exitCode = 1;
  });
}

export {
  DISCORD_MAX_RATE_LIMIT_RETRIES,
  DISCORD_MAX_RETRY_AFTER_MS,
  DISCORD_REQUEST_TIMEOUT_MS,
  DiscordTargetAggregateError,
  deliverToTargets,
  deliverToTargetsWithReceipts,
  discordFetch,
};
