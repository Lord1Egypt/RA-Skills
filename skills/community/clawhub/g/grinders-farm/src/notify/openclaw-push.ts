import { spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { GameEngine } from "../game/engine.js";
import { LocalStorage } from "../storage/local-storage.js";
import { loadOpenclawDeliveries, loadOpenclawDelivery } from "./openclaw-delivery.js";

export const NOTIFY_CONFIG_PATH = path.join(os.homedir(), ".grinders-farm", "notify.json");
const IMAGE_SERVER_INFO_FILE = path.join(os.homedir(), ".grinders-farm", "image-server.json");
const OPENCLAW_MEDIA_DIR = path.join(os.homedir(), ".openclaw", "media", "grinders-farm");

/**
 * 推送目标。日常只需：
 * - 环境变量 `GRINDERS_FARM_NOTIFY_TARGET`，或
 * - `~/.grinders-farm/notify.json` 里只写 `"target": "..."` 即可。
 * 其余字段均为可选（多账号、指定频道等）。
 */
export interface NotifyConfig {
  enabled: boolean;
  target?: string;
  targets?: NotifyTarget[];
  channel?: string;
  account?: string;
  attachImage?: boolean;
  onAutoAdvance?: boolean;
  messagePrefix?: string;
}

export interface NotifyTarget {
  target: string;
  channel?: string;
  account?: string;
  threadId?: string | number;
  sessionKey?: string;
}

const MAX_BODY_CHARS = 3800;
const DEFAULT_WEBCHAT_INJECT_TIMEOUT_MS = 8000;

function envBool(name: string, defaultTrue: boolean): boolean {
  const v = process.env[name]?.trim().toLowerCase();
  if (v === "0" || v === "false" || v === "no" || v === "off") return false;
  if (v === "1" || v === "true" || v === "yes" || v === "on") return true;
  return defaultTrue;
}

function configFromEnv(): NotifyConfig | null {
  const target = process.env.GRINDERS_FARM_NOTIFY_TARGET?.trim();
  if (!target) return null;
  return {
    enabled: true,
    target,
    channel: process.env.GRINDERS_FARM_NOTIFY_CHANNEL?.trim() || undefined,
    account: process.env.GRINDERS_FARM_NOTIFY_ACCOUNT?.trim() || undefined,
    attachImage: envBool("GRINDERS_FARM_NOTIFY_IMAGE", true),
    onAutoAdvance: envBool("GRINDERS_FARM_NOTIFY_ON_AUTO_ADVANCE", true),
  };
}

function configFromOpenclawDelivery(): NotifyConfig | null {
  const deliveries = loadOpenclawDeliveries();
  if (deliveries.length === 0) return null;
  const targets = deliveries.map((d) => ({
    target: d.target,
    channel: d.channel,
    account: d.accountId,
    ...(d.threadId != null ? { threadId: d.threadId } : {}),
    ...(d.sessionKey ? { sessionKey: d.sessionKey } : {}),
  }));
  return {
    enabled: true,
    target: targets[0]?.target,
    targets,
    channel: targets[0]?.channel,
    account: targets[0]?.account,
    attachImage: true,
    onAutoAdvance: true,
  };
}

function configFromFile(): NotifyConfig | null {
  if (!fs.existsSync(NOTIFY_CONFIG_PATH)) return null;
  try {
    const raw = JSON.parse(fs.readFileSync(NOTIFY_CONFIG_PATH, "utf8")) as Record<string, unknown>;
    if (!raw || typeof raw !== "object") return null;
    if (raw.enabled === false) return null;
    const target = typeof raw.target === "string" ? raw.target.trim() : "";
    const targetsRaw = Array.isArray(raw.targets) ? raw.targets : [];
    const targets = targetsRaw
      .map((entry): NotifyTarget | null => {
        if (!entry || typeof entry !== "object") return null;
        const item = entry as Record<string, unknown>;
        const itemTarget = typeof item.target === "string" ? item.target.trim() : "";
        if (!itemTarget) return null;
        return {
          target: itemTarget,
          ...(typeof item.channel === "string" && item.channel.trim() ? { channel: item.channel.trim() } : {}),
          ...(typeof item.account === "string" && item.account.trim() ? { account: item.account.trim() } : {}),
          ...(typeof item.threadId === "string" || typeof item.threadId === "number"
            ? { threadId: item.threadId as string | number }
            : {}),
          ...(typeof item.sessionKey === "string" && item.sessionKey.trim() ? { sessionKey: item.sessionKey.trim() } : {}),
        };
      })
      .filter((entry): entry is NotifyTarget => entry != null);
    if (!target && targets.length === 0) return null;
    return {
      enabled: true,
      ...(target ? { target } : {}),
      ...(targets.length > 0 ? { targets } : {}),
      channel: typeof raw.channel === "string" && raw.channel.trim() ? raw.channel.trim() : undefined,
      account: typeof raw.account === "string" && raw.account.trim() ? raw.account.trim() : undefined,
      attachImage: raw.attachImage !== false,
      onAutoAdvance: raw.onAutoAdvance !== false,
      messagePrefix: typeof raw.messagePrefix === "string" ? raw.messagePrefix : undefined,
    };
  } catch {
    return null;
  }
}

/**
 * 优先级：环境变量 → OpenClaw 插件写入的会话投递（~/.grinders-farm/openclaw-delivery.json）→ notify.json
 */
export function loadNotifyConfig(): NotifyConfig | null {
  return configFromEnv() ?? configFromOpenclawDelivery() ?? configFromFile();
}

/** `openclaw message send` 不支持 webchat；Web 控制端改用 Gateway `chat.inject` */
export function isUnsupportedOpenclawMessageChannel(channel?: string): boolean {
  const c = channel?.trim().toLowerCase();
  return c === "webchat";
}

/**
 * Web 控制端：向会话追加一条「助手」消息并广播到 WebChat（不经 message send）。
 * 默认 `agent:<GRINDERS_FARM_AGENT_ID||main>:main`，与 `openclaw sessions` 中主会话一致。
 */
export function resolveWebchatSessionKey(): string {
  const fromEnv = process.env.GRINDERS_FARM_WEBCHAT_SESSION_KEY?.trim();
  if (fromEnv) return fromEnv;
  const all = loadOpenclawDeliveries();
  const fromDeliveryList = all.find((entry) => entry.channel.trim().toLowerCase() === "webchat" && entry.sessionKey?.trim());
  if (fromDeliveryList?.sessionKey?.trim()) return fromDeliveryList.sessionKey.trim();
  const d = loadOpenclawDelivery();
  if (d?.sessionKey?.trim()) return d.sessionKey.trim();
  const agentId = process.env.GRINDERS_FARM_AGENT_ID?.trim() || "main";
  return `agent:${agentId}:main`;
}

function notifyTargetKey(entry: NotifyTarget): string {
  const channel = entry.channel?.trim().toLowerCase() ?? "";
  const account = entry.account?.trim() ?? "";
  const target = entry.target.trim();
  const thread = entry.threadId == null ? "" : String(entry.threadId);
  const session = entry.sessionKey?.trim() ?? "";
  return [channel, account, target, thread, session].join("|");
}

function resolveNotifyTargets(cfg: NotifyConfig): NotifyTarget[] {
  const merged: NotifyTarget[] = [];
  if (cfg.target?.trim()) {
    merged.push({
      target: cfg.target.trim(),
      channel: cfg.channel,
      account: cfg.account,
    });
  }
  if (Array.isArray(cfg.targets)) {
    merged.push(...cfg.targets);
  }
  const dedup = new Map<string, NotifyTarget>();
  for (const target of merged) {
    if (!target?.target?.trim()) continue;
    const normalized: NotifyTarget = {
      target: target.target.trim(),
      ...(target.channel?.trim() ? { channel: target.channel.trim() } : {}),
      ...(target.account?.trim() ? { account: target.account.trim() } : {}),
      ...(target.threadId != null ? { threadId: target.threadId } : {}),
      ...(target.sessionKey?.trim() ? { sessionKey: target.sessionKey.trim() } : {}),
    };
    dedup.set(notifyTargetKey(normalized), normalized);
  }
  return Array.from(dedup.values());
}

function isTelegramLikeChannel(channel?: string): boolean {
  const c = channel?.trim().toLowerCase() ?? "";
  return c === "tg" || c.includes("telegram");
}

function buildTelegramNotifyCaption(farmText: string, fallback: string): string {
  const nonTableLines = farmText
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0 && !line.startsWith("|"));
  const firstLine = nonTableLines[0];
  if (!firstLine) return fallback;

  const hasDay = firstLine.includes("第") && firstLine.includes("天");
  const hasGold = /(?:💰\s*)?\d+\s*G\b/i.test(firstLine);
  const hasEnglishDay = /\bday\s*\d+\b/i.test(firstLine);
  if (hasDay || hasGold || hasEnglishDay) {
    const orderDoneLine = nonTableLines.find((line) => line.startsWith("✅ 完成订单："));
    const orderLine = nonTableLines.find((line) => line.startsWith("📦 订单:"));
    const marketLine = nonTableLines.find((line) => line.startsWith("📉 市场反馈："));
    const parts = [firstLine, orderDoneLine, orderLine, marketLine].filter(Boolean);
    return parts.join("\n");
  }
  return fallback;
}

function sanitizeOpenclawCliError(combined: string): string {
  const lines = combined.split("\n").map((l) => l.trimEnd());
  const err = lines.find(
    (l) =>
      /^Error:/i.test(l) ||
      l.includes("Unknown channel") ||
      l.includes("Gateway call failed:") ||
      l.includes("session not found"),
  );
  if (err) return err.slice(0, 280);
  const first = lines.find(
    (l) =>
      l.length > 0 &&
      !l.includes("─") &&
      !l.includes("╮") &&
      !l.includes("◇") &&
      !l.startsWith("Config warnings"),
  );
  return (first ?? combined).slice(0, 280);
}

function resolveOpenclawBin(): string {
  const fromEnv = process.env.OPENCLAW_BIN?.trim();
  if (fromEnv) return fromEnv;
  try {
    const which = spawnSync("sh", ["-lc", "command -v openclaw"], {
      encoding: "utf8",
      maxBuffer: 1024 * 1024,
    });
    const fromWhich = (which.stdout ?? "").trim();
    if (fromWhich) return fromWhich;
  } catch {
    // keep trying
  }
  const candidates = [
    process.env.OPENCLAW_PATH?.trim(),
    process.env.NVM_BIN ? path.join(process.env.NVM_BIN, "openclaw") : "",
    path.join(path.dirname(process.execPath), "openclaw"),
    "/opt/homebrew/bin/openclaw",
    "/usr/local/bin/openclaw",
  ]
    .map((p) => (p ?? "").trim())
    .filter(Boolean);
  for (const p of candidates) {
    try {
      fs.accessSync(p, fs.constants.X_OK);
      return p;
    } catch {
      // keep trying
    }
  }
  return "openclaw";
}

function resolveFarmImageUrl(imagePath: string): string {
  try {
    if (fs.existsSync(IMAGE_SERVER_INFO_FILE)) {
      const raw = JSON.parse(fs.readFileSync(IMAGE_SERVER_INFO_FILE, "utf8")) as { baseUrl?: unknown };
      if (typeof raw.baseUrl === "string" && raw.baseUrl.trim()) {
        const baseUrl = raw.baseUrl.trim().replace(/\/+$/, "");
        return `${baseUrl}/${encodeURIComponent(path.basename(imagePath))}`;
      }
    }
  } catch {
    // fall through to file:// fallback
  }
  return `file://${imagePath}`;
}

function stageMediaForOpenclaw(imagePath: string): string | null {
  try {
    fs.mkdirSync(OPENCLAW_MEDIA_DIR, { recursive: true });
    const ext = path.extname(imagePath) || ".png";
    const staged = path.join(OPENCLAW_MEDIA_DIR, `farm-notify-${Date.now()}${ext}`);
    fs.copyFileSync(imagePath, staged);
    return staged;
  } catch {
    return null;
  }
}

export interface PushFarmSnapshotOptions {
  dryRun?: boolean;
}

export interface PushFarmSnapshotResult {
  ok: boolean;
  message: string;
}

function pushWebchatViaGatewayInject(params: {
  body: string;
  label: string;
  sessionKey?: string;
  dryRun?: boolean;
}): PushFarmSnapshotResult {
  const sessionKey = params.sessionKey?.trim() || resolveWebchatSessionKey();
  if (params.dryRun) {
    return {
      ok: true,
      message: `Dry-run: 将执行 openclaw gateway call chat.inject → sessionKey=${sessionKey}`,
    };
  }
  const bin = resolveOpenclawBin();
  const injectParams = JSON.stringify({
    sessionKey,
    message: params.body,
    label: params.label,
  });
  const timeoutMsRaw = process.env.GRINDERS_FARM_WEBCHAT_INJECT_TIMEOUT_MS?.trim();
  const parsedTimeout = timeoutMsRaw ? Number.parseInt(timeoutMsRaw, 10) : Number.NaN;
  const timeoutMs =
    Number.isFinite(parsedTimeout) && parsedTimeout >= 1000 ? parsedTimeout : DEFAULT_WEBCHAT_INJECT_TIMEOUT_MS;
  const args = ["gateway", "call", "chat.inject", "--params", injectParams, "--json", "--timeout", String(timeoutMs)];
  const token = process.env.OPENCLAW_GATEWAY_TOKEN?.trim();
  if (token) args.push("--token", token);
  const r = spawnSync(bin, args, {
    encoding: "utf8",
    maxBuffer: 16 * 1024 * 1024,
    env: { ...process.env },
  });

  const stderr = (r.stderr ?? "").trim();
  const stdout = (r.stdout ?? "").trim();
  const code = r.status ?? (r.error ? 1 : 0);

  if (r.error) {
    const hint =
      (r.error as NodeJS.ErrnoException).code === "ENOENT"
        ? `找不到 openclaw 命令（已尝试: ${bin}）。请安装并加入 PATH，或设置 OPENCLAW_BIN。`
        : String(r.error.message);
    return { ok: false, message: hint };
  }

  if (code !== 0) {
    const short = sanitizeOpenclawCliError([stderr, stdout].filter(Boolean).join("\n"));
    return {
      ok: false,
      message: `chat.inject 失败 (exit ${code}) ${short || stderr || "(无输出)"}。若会话不匹配，请设 GRINDERS_FARM_WEBCHAT_SESSION_KEY（见 openclaw sessions --json 的 key）或 GRINDERS_FARM_AGENT_ID。`,
    };
  }

  let parsed: { ok?: boolean; messageId?: string } | null = null;
  try {
    parsed = JSON.parse(stdout) as { ok?: boolean; messageId?: string };
  } catch {
    /* ignore */
  }
  const id = parsed?.messageId ?? "";
  return {
    ok: true,
    message: id ? `已推送到 Web 控制端（chat.inject，messageId=${id}）` : `已推送到 Web 控制端（chat.inject）\n${stdout || "ok"}`,
  };
}

/**
 * Renders current farm, then runs `openclaw message send`.
 * Web 控制端（webchat）使用 `openclaw gateway call chat.inject`。
 */
export async function pushFarmSnapshot(opts?: PushFarmSnapshotOptions): Promise<PushFarmSnapshotResult> {
  const cfg = loadNotifyConfig();
  if (!cfg) {
    return {
      ok: false,
      message: [
        "还没有推送目标。推荐：在每个需要接收推送的频道里各发一次 /farm 命令（例如 /farm farm），",
        "插件会把会话写入 ~/.grinders-farm/openclaw-deliveries.json，之后自动推送会对全部已绑定频道生效。",
        "",
        "若不在聊天里操作，也可：export GRINDERS_FARM_NOTIFY_TARGET=… 或编辑 notify.json（见 SKILL）。",
      ].join("\n"),
    };
  }
  const targets = resolveNotifyTargets(cfg);
  if (targets.length === 0) {
    return {
      ok: false,
      message: "没有可用推送目标（target/targets 为空）。",
    };
  }

  const storage = new LocalStorage();
  const engine = new GameEngine(storage);
  const view = await engine.executeCommand("farm");
  if (!view.success) {
    return { ok: false, message: view.message };
  }

  const prefix = (cfg.messagePrefix ?? "🌾 Grinder's Farm").trim();
  const telegramCaption = buildTelegramNotifyCaption(view.message, prefix);
  const imageUrlLine = view.imagePath ? `\n\n🖼 查看高清像素图: ${resolveFarmImageUrl(view.imagePath)}` : "";
  let body = `${prefix}\n\n${view.message}`;
  if (imageUrlLine) {
    const maxMainLen = Math.max(200, MAX_BODY_CHARS - imageUrlLine.length);
    if (body.length > maxMainLen) {
      body = `${body.slice(0, maxMainLen - 30)}\n\n…(正文过长已截断)`;
    }
    body += imageUrlLine;
  }
  if (body.length > MAX_BODY_CHARS) {
    body = `${body.slice(0, MAX_BODY_CHARS - 30)}\n\n…(正文过长已截断)`;
  }
  const bin = resolveOpenclawBin();
  const imagePath = view.imagePath;
  const stagedImagePath = cfg.attachImage !== false && imagePath && fs.existsSync(imagePath) ? stageMediaForOpenclaw(imagePath) : null;
  const results: Array<{ ok: boolean; label: string; message: string }> = [];

  for (const target of targets) {
    const channel = target.channel?.trim().toLowerCase() ?? "";
    const label = channel ? `${channel}:${target.target}` : target.target;
    if (channel === "webchat") {
      const webRes = pushWebchatViaGatewayInject({
        body,
        label: prefix,
        sessionKey: target.sessionKey,
        dryRun: opts?.dryRun,
      });
      results.push({ ok: webRes.ok, label, message: webRes.message });
      continue;
    }

    // Telegram pushes should be image-first with a short caption; avoid sending
    // the full emoji table together with media to prevent visual duplication.
    const targetMessage = isTelegramLikeChannel(channel) && stagedImagePath ? telegramCaption : body;
    const args: string[] = ["message", "send", "--target", target.target, "--message", targetMessage];
    if (target.channel?.trim()) args.push("--channel", target.channel.trim());
    if (target.account?.trim()) args.push("--account", target.account.trim());
    if (target.threadId != null) args.push("--thread-id", String(target.threadId));
    if (opts?.dryRun) args.push("--dry-run");
    if (stagedImagePath) args.push("--media", stagedImagePath);

    const r = spawnSync(bin, args, {
      encoding: "utf8",
      maxBuffer: 16 * 1024 * 1024,
      env: { ...process.env },
    });
    const combined = [r.stdout, r.stderr].filter(Boolean).join("\n").trim();
    const code = r.status ?? (r.error ? 1 : 0);

    if (r.error) {
      const hint =
        (r.error as NodeJS.ErrnoException).code === "ENOENT"
          ? `找不到 openclaw 命令（已尝试: ${bin}）。请安装并加入 PATH，或设置 OPENCLAW_BIN 为可执行文件绝对路径。`
          : String(r.error.message);
      results.push({ ok: false, label, message: hint });
      continue;
    }

    if (code !== 0) {
      if (combined.includes("LocalMediaAccessError") && args.includes("--media")) {
        const noMediaArgs = args.filter((_, idx, all) => !(all[idx - 1] === "--media" || all[idx] === "--media"));
        const retry = spawnSync(bin, noMediaArgs, {
          encoding: "utf8",
          maxBuffer: 16 * 1024 * 1024,
          env: { ...process.env },
        });
        const retryCode = retry.status ?? (retry.error ? 1 : 0);
        if (retryCode === 0) {
          const retryOut = [retry.stdout, retry.stderr].filter(Boolean).join("\n").trim();
          results.push({ ok: true, label, message: `文本-only（媒体被本地策略拦截） ${retryOut || "ok"}` });
          continue;
        }
      }
      const short = sanitizeOpenclawCliError(combined || "");
      results.push({ ok: false, label, message: `openclaw message send 失败 (exit ${code}) ${short || "(无输出)"}` });
      continue;
    }

    results.push({
      ok: true,
      label,
      message: opts?.dryRun ? `Dry-run 成功（未真正发送） ${combined || "(无额外输出)"}` : combined || "ok",
    });
  }

  const okCount = results.filter((r) => r.ok).length;
  const failCount = results.length - okCount;
  const details = results.map((r) => `${r.ok ? "✅" : "❌"} ${r.label} → ${r.message}`).join("\n");
  return {
    ok: failCount === 0,
    message: `推送完成：成功 ${okCount} / 失败 ${failCount}\n${details}`,
  };
}

export function shouldNotifyOnAutoAdvance(): boolean {
  const cfg = loadNotifyConfig();
  if (!cfg || cfg.onAutoAdvance === false) return false;
  return true;
}
