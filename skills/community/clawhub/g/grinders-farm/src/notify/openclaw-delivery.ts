import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

/** 由 OpenClaw 插件在用户执行 /farm 时写入，无需手填 target。 */
export const OPENCLAW_DELIVERY_PATH = path.join(os.homedir(), ".grinders-farm", "openclaw-delivery.json");
export const OPENCLAW_DELIVERIES_PATH = path.join(os.homedir(), ".grinders-farm", "openclaw-deliveries.json");

export interface OpenclawDeliveryFile {
  channel: string;
  accountId?: string;
  target: string;
  threadId?: string | number;
  /** Web 控制端推送用，对应 `openclaw gateway call chat.inject` 的 sessionKey */
  sessionKey?: string;
}

function normalizeDelivery(raw: unknown): OpenclawDeliveryFile | null {
  if (!raw || typeof raw !== "object") return null;
  const r = raw as Record<string, unknown>;
  const target = typeof r.target === "string" ? r.target.trim() : "";
  const channel = typeof r.channel === "string" ? r.channel.trim() : "";
  if (!target || !channel) return null;
  return {
    channel,
    target,
    ...(typeof r.accountId === "string" && r.accountId.trim() ? { accountId: r.accountId.trim() } : {}),
    ...(r.threadId != null ? { threadId: r.threadId as string | number } : {}),
    ...(typeof r.sessionKey === "string" && r.sessionKey.trim() ? { sessionKey: r.sessionKey.trim() } : {}),
  };
}

function deliveryKey(entry: OpenclawDeliveryFile): string {
  const channel = entry.channel.trim().toLowerCase();
  const account = entry.accountId?.trim() ?? "";
  const target = entry.target.trim();
  const thread = entry.threadId == null ? "" : String(entry.threadId);
  const session = entry.sessionKey?.trim() ?? "";
  return [channel, account, target, thread, session].join("|");
}

function persistOpenclawDeliveryList(payload: OpenclawDeliveryFile): void {
  const existing = loadOpenclawDeliveries();
  const key = deliveryKey(payload);
  const next = existing.filter((entry) => deliveryKey(entry) !== key);
  next.push(payload);
  fs.writeFileSync(OPENCLAW_DELIVERIES_PATH, JSON.stringify(next, null, 2), "utf8");
}

export function loadOpenclawDelivery(): OpenclawDeliveryFile | null {
  if (!fs.existsSync(OPENCLAW_DELIVERY_PATH)) return null;
  try {
    const raw = JSON.parse(fs.readFileSync(OPENCLAW_DELIVERY_PATH, "utf8")) as unknown;
    return normalizeDelivery(raw);
  } catch {
    return null;
  }
}

export function loadOpenclawDeliveries(): OpenclawDeliveryFile[] {
  if (!fs.existsSync(OPENCLAW_DELIVERIES_PATH)) {
    const one = loadOpenclawDelivery();
    return one ? [one] : [];
  }
  try {
    const raw = JSON.parse(fs.readFileSync(OPENCLAW_DELIVERIES_PATH, "utf8")) as unknown;
    if (!Array.isArray(raw)) return [];
    return raw.map((entry) => normalizeDelivery(entry)).filter((entry): entry is OpenclawDeliveryFile => entry != null);
  } catch {
    return [];
  }
}

/** OpenClaw 插件在 /farm 命令里调用：把当前会话写成推送目标（用户无需手配）。 */
export function saveOpenclawDeliveryFromBridge(ctx: {
  channel?: string;
  channelId?: string;
  accountId?: string;
  to?: string;
  from?: string;
  senderId?: string;
  messageThreadId?: string | number;
}): boolean {
  const channel = (ctx.channel ?? ctx.channelId)?.toString().trim();
  const target = (ctx.to ?? ctx.from ?? ctx.senderId)?.toString().trim();
  if (!target || !channel) return false;
  const payload: OpenclawDeliveryFile = {
    channel,
    target,
    ...(ctx.accountId?.trim() ? { accountId: ctx.accountId.trim() } : {}),
    ...(ctx.messageThreadId != null ? { threadId: ctx.messageThreadId } : {}),
  };
  fs.mkdirSync(path.dirname(OPENCLAW_DELIVERY_PATH), { recursive: true });
  fs.writeFileSync(OPENCLAW_DELIVERY_PATH, JSON.stringify(payload, null, 2), "utf8");
  persistOpenclawDeliveryList(payload);
  return true;
}

/**
 * 入站消息自动绑定推送。
 * - `openclaw-delivery.json`：仅在首次缺失时写入（兼容单目标）
 * - `openclaw-deliveries.json`：每次都会去重追加（多目标 fan-out）
 */
export function trySaveOpenclawDeliveryFromInboundClaim(event: {
  channel: string;
  accountId?: string;
  conversationId?: string;
  senderId?: string;
  threadId?: string | number;
}): boolean {
  const target = event.conversationId?.trim() || event.senderId?.trim();
  const channel = event.channel?.trim();
  if (!target || !channel) return false;
  const payload: OpenclawDeliveryFile = {
    channel,
    target,
    ...(event.accountId?.trim() ? { accountId: event.accountId.trim() } : {}),
    ...(event.threadId != null ? { threadId: event.threadId } : {}),
  };
  if (!fs.existsSync(OPENCLAW_DELIVERY_PATH)) {
    fs.mkdirSync(path.dirname(OPENCLAW_DELIVERY_PATH), { recursive: true });
    fs.writeFileSync(OPENCLAW_DELIVERY_PATH, JSON.stringify(payload, null, 2), "utf8");
  }
  persistOpenclawDeliveryList(payload);
  return true;
}
