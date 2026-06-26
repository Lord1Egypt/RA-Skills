import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

type Usage = {
  provider?: string;
  model?: string;
  input?: number;
  output?: number;
  total?: number;
  ts: number;
  sessionKey?: string;
};

type Quota = {
  percent?: number;
  weeklyPercent?: number;
  resetLabel?: string;
  ts: number;
};

type Config = {
  enabled?: boolean;
  enabledChannels?: string[];
  disabledConversations?: string[];
  disabledChannels?: string[];
  cacheMs?: number;
  quotaCacheMs?: number;
  contextReserveTokens?: number;
  appendSubagents?: boolean;
};

const recentBySession = new Map<string, Usage>();
const recentOutputs: Usage[] = [];
let quotaCache: Quota | null = null;
let quotaFetchInFlight: Promise<Quota | null> | null = null;

const MODEL_CONTEXT: Record<string, number> = {
  "openai-codex/gpt-5.5": 391000,
  "gpt-5.5": 391000,
  "openai-codex/gpt-5.4-mini": 266000,
  "gpt-5.4-mini": 266000,
  "ollama/kimi-k2.6:cloud": 250000,
  "kimi-k2.6:cloud": 250000,
  "ollama/qwen3.5:397b-cloud": 250000,
  "qwen3.5:397b-cloud": 250000
};

function n(v: unknown): number | undefined {
  return typeof v === "number" && Number.isFinite(v) ? v : undefined;
}

function fmt(v?: number): string {
  if (!Number.isFinite(v)) return "n/a";
  const x = Number(v);
  if (x >= 1_000_000) return `${Math.round(x / 100_000) / 10}m`;
  if (x >= 10_000) return `${Math.round(x / 1000)}k`;
  if (x >= 1000) return `${Math.round(x / 100) / 10}k`;
  return String(Math.round(x));
}

function colorForUsage(percent?: number): string {
  if (!Number.isFinite(percent)) return "⚪";
  if (Number(percent) >= 80) return "🔴";
  if (Number(percent) >= 50) return "🟡";
  return "🟢";
}

function colorForRemaining(percent?: number): string {
  if (!Number.isFinite(percent)) return "⚪";
  if (Number(percent) < 20) return "🔴";
  if (Number(percent) <= 50) return "🟡";
  return "🟢";
}

function worst(...colors: string[]): string {
  if (colors.includes("🔴")) return "🔴";
  if (colors.includes("🟡")) return "🟡";
  if (colors.includes("🟢")) return "🟢";
  return "⚪";
}

function modelLabel(provider?: string, model?: string): string {
  const m = model || "model";
  if (!provider || m.includes("/")) return m;
  return `${provider}/${m}`;
}

function contextWindow(model?: string, provider?: string): number | undefined {
  const label = modelLabel(provider, model);
  return MODEL_CONTEXT[label] ?? MODEL_CONTEXT[model || ""] ?? undefined;
}

function latestUsage(sessionKey?: string): Usage | undefined {
  if (sessionKey && recentBySession.has(sessionKey)) return recentBySession.get(sessionKey);
  return recentOutputs.at(-1);
}

function aggregateSubagents(root?: Usage, cacheMs = 120000): { input: number; output: number } | null {
  if (!root) return null;
  const cutoff = Date.now() - cacheMs;
  let input = 0;
  let output = 0;
  for (const u of recentOutputs) {
    if (u === root || u.ts < cutoff) continue;
    if (Math.abs(root.ts - u.ts) > cacheMs) continue;
    if (u.sessionKey && root.sessionKey && u.sessionKey === root.sessionKey) continue;
    input += u.input ?? 0;
    output += u.output ?? 0;
  }
  return input || output ? { input, output } : null;
}

function authProfilesPath(): string {
  return path.join(os.homedir(), ".openclaw", "agents", "main", "agent", "auth-profiles.json");
}

function findCodexAccessToken(): string | null {
  try {
    const raw = JSON.parse(fs.readFileSync(authProfilesPath(), "utf8"));
    for (const profile of Object.values(raw.profiles ?? {}) as any[]) {
      if (profile?.provider !== "openai-codex" || profile?.type !== "oauth") continue;
      if (typeof profile.access === "string") return profile.access;
      if (typeof profile.access?.accessToken === "string") return profile.access.accessToken;
    }
  } catch {
    return null;
  }
  return null;
}

function resetLabelFromNow(resetAt?: unknown): string | undefined {
  if (typeof resetAt !== "number") return undefined;
  const ms = resetAt > 10_000_000_000 ? resetAt - Date.now() : resetAt * 1000 - Date.now();
  if (!Number.isFinite(ms) || ms <= 0) return undefined;
  const h = Math.max(1, Math.round(ms / 3600000));
  return `${h}h`;
}

function parseQuota(data: any): Quota {
  const candidates = [
    data?.rate_limit?.primary_window,
    data?.codex,
    data?.plus,
    data?.pro,
    data?.usage,
    data
  ];
  let percent: number | undefined;
  let weeklyPercent: number | undefined;
  let resetLabel: string | undefined;
  for (const c of candidates) {
    if (!c || typeof c !== "object") continue;
    percent ??= n(c.remaining_percent) ?? n(c.remainingPercent) ?? n(c.percent_remaining) ?? n(c.percentRemaining);
    const usedPercent = n(c.used_percent) ?? n(c.usedPercent);
    if (percent == null && usedPercent != null) percent = Math.max(0, Math.min(100, 100 - usedPercent));
    weeklyPercent ??= n(c.weekly_remaining_percent) ?? n(c.weeklyRemainingPercent);
    const secondaryUsedPercent = n(data?.rate_limit?.secondary_window?.used_percent) ?? n(data?.rate_limit?.secondary_window?.usedPercent);
    if (weeklyPercent == null && secondaryUsedPercent != null) weeklyPercent = Math.max(0, Math.min(100, 100 - secondaryUsedPercent));
    resetLabel ??= resetLabelFromNow(c.reset_at ?? c.resetAt);
    if (percent == null && Number.isFinite(c.requests_used) && Number.isFinite(c.requests_limit)) {
      percent = Math.round(((c.requests_limit - c.requests_used) / c.requests_limit) * 100);
    }
  }
  return { percent, weeklyPercent, resetLabel: resetLabel ?? "5h", ts: Date.now() };
}

async function fetchCodexQuota(cacheMs: number): Promise<Quota | null> {
  if (quotaCache && Date.now() - quotaCache.ts < cacheMs) return quotaCache;
  if (quotaFetchInFlight) return quotaFetchInFlight;
  quotaFetchInFlight = (async () => {
    const token = findCodexAccessToken();
    if (!token) return quotaCache;
    try {
      const res = await fetch("https://chatgpt.com/backend-api/wham/usage", {
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/json"
        },
        signal: AbortSignal.timeout(4000)
      });
      if (!res.ok) return quotaCache;
      quotaCache = parseQuota(await res.json());
      return quotaCache;
    } catch {
      return quotaCache;
    } finally {
      quotaFetchInFlight = null;
    }
  })();
  return quotaFetchInFlight;
}

function appendFooter(content: string, footer: string): string {
  const line = `\n\n_${footer}_`;
  if (content.includes("↑") && content.includes("%ctx")) return content;
  if (content.length + line.length > 1800) return content;
  return `${content}${line}`;
}

export default definePluginEntry({
  id: "openclaw-output-metrics-footer",
  name: "OpenClaw Output Metrics Footer",
  description: "Append compact context/token/quota metrics to OpenClaw channel outputs.",
  register(api) {
    const cfg = (api.pluginConfig ?? {}) as Config;
    if (cfg.enabled === false) return;
    const cacheMs = cfg.cacheMs ?? 120000;
    const quotaCacheMs = cfg.quotaCacheMs ?? 60000;
    const reserve = cfg.contextReserveTokens ?? 40000;

    api.on("llm_output", async (event: any, ctx: any) => {
      const usage: Usage = {
        provider: event.provider ?? ctx.modelProviderId,
        model: event.model ?? ctx.modelId,
        input: n(event.usage?.input),
        output: n(event.usage?.output),
        total: n(event.usage?.total),
        ts: Date.now(),
        sessionKey: ctx.sessionKey
      };
      recentOutputs.push(usage);
      if (usage.sessionKey) recentBySession.set(usage.sessionKey, usage);
      while (recentOutputs.length > 80) recentOutputs.shift();
    }, { name: "openclaw-output-metrics-footer-llm-output" });

    api.on("message_sending", async (event: any, ctx: any) => {
      const channel = String(ctx.channelId ?? event.metadata?.channel ?? "");
      if ((cfg.enabledChannels ?? []).length > 0 && !(cfg.enabledChannels ?? []).includes(channel)) return;
      if ((cfg.disabledChannels ?? []).includes(ctx.channelId)) return;
      if ((cfg.disabledConversations ?? []).includes(ctx.conversationId)) return;
      if (!event.content || typeof event.content !== "string") return;

      const usage = latestUsage();
      const quota = await fetchCodexQuota(quotaCacheMs);
      const label = modelLabel(usage?.provider, usage?.model);
      const win = contextWindow(usage?.model, usage?.provider);
      const total = usage?.total ?? ((usage?.input ?? 0) + (usage?.output ?? 0));
      const effectiveTotal = Math.max(0, total + reserve);
      const ctxPct = win ? Math.round((effectiveTotal / win) * 100) : undefined;
      const status = worst(colorForUsage(ctxPct), colorForRemaining(quota?.percent));
      const parts = [
        `${status} ↑${fmt(usage?.input)} ↓${fmt(usage?.output)}`,
        `${Number.isFinite(ctxPct) ? ctxPct : "n/a"}%ctx`
      ];
      if (quota?.percent != null) parts.push(`${quota.resetLabel ?? "5h"} ${quota.percent}%`);
      parts.push(label);
      const sub = cfg.appendSubagents === false ? null : aggregateSubagents(usage, cacheMs);
      if (sub) parts.push(`sub ↑${fmt(sub.input)} ↓${fmt(sub.output)}`);
      return { content: appendFooter(event.content, parts.join(" · ")) };
    }, { name: "openclaw-output-metrics-footer-message-sending" });
  }
});
