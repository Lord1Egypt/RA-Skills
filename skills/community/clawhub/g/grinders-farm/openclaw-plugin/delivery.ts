/**
 * 仅放在 openclaw-plugin/ 内，不 import 仓库 ../src。
 * 安装到 ~/.openclaw/extensions/grinders-farm 时也能工作。
 */
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

export const OPENCLAW_DELIVERY_PATH = path.join(os.homedir(), ".grinders-farm", "openclaw-delivery.json");
export const OPENCLAW_DELIVERIES_PATH = path.join(os.homedir(), ".grinders-farm", "openclaw-deliveries.json");

export interface OpenclawDeliveryFile {
  channel: string;
  accountId?: string;
  target: string;
  threadId?: string | number;
  /** 可选：与 `openclaw sessions --json` 的 key 一致，用于 chat.inject */
  sessionKey?: string;
}

function persistOpenclawDelivery(payload: OpenclawDeliveryFile): void {
  fs.mkdirSync(path.dirname(OPENCLAW_DELIVERY_PATH), { recursive: true });
  fs.writeFileSync(OPENCLAW_DELIVERY_PATH, JSON.stringify(payload, null, 2), "utf8");
  persistOpenclawDeliveryList(payload);
}

function loadOpenclawDeliveryList(): OpenclawDeliveryFile[] {
  if (!fs.existsSync(OPENCLAW_DELIVERIES_PATH)) return [];
  try {
    const raw = JSON.parse(fs.readFileSync(OPENCLAW_DELIVERIES_PATH, "utf8")) as unknown;
    if (!Array.isArray(raw)) return [];
    return raw
      .map((entry) => {
        if (!entry || typeof entry !== "object") return null;
        const r = entry as Record<string, unknown>;
        const channel = typeof r.channel === "string" ? r.channel.trim() : "";
        const target = typeof r.target === "string" ? r.target.trim() : "";
        if (!channel || !target) return null;
        return {
          channel,
          target,
          ...(typeof r.accountId === "string" && r.accountId.trim() ? { accountId: r.accountId.trim() } : {}),
          ...(r.threadId != null ? { threadId: r.threadId as string | number } : {}),
          ...(typeof r.sessionKey === "string" && r.sessionKey.trim() ? { sessionKey: r.sessionKey.trim() } : {}),
        } satisfies OpenclawDeliveryFile;
      })
      .filter((entry): entry is OpenclawDeliveryFile => entry != null);
  } catch {
    return [];
  }
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
  const current = loadOpenclawDeliveryList();
  const key = deliveryKey(payload);
  const deduped = current.filter((entry) => deliveryKey(entry) !== key);
  deduped.push(payload);
  fs.writeFileSync(OPENCLAW_DELIVERIES_PATH, JSON.stringify(deduped, null, 2), "utf8");
}

/**
 * 从插件命令 ctx 写入投递。优先 to/from；若缺失则用 senderId（Web 控制端等常有 senderId 无 to/from）。
 * channel 优先 ctx.channel，否则 ctx.channelId。
 */
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
  if (!channel || !target) return false;
  persistOpenclawDelivery({
    channel,
    target,
    ...(ctx.accountId?.trim() ? { accountId: ctx.accountId.trim() } : {}),
    ...(ctx.messageThreadId != null ? { threadId: ctx.messageThreadId } : {}),
  });
  return true;
}

/**
 * 先 sync 保存；失败时再试 OpenClaw 的会话绑定（部分界面 to/from 为空但绑定里有 conversationId）。
 */
export async function bindDeliveryFromPluginCommand(ctx: {
  channel?: string;
  channelId?: string;
  accountId?: string;
  to?: string;
  from?: string;
  senderId?: string;
  messageThreadId?: string | number;
  getCurrentConversationBinding?: () => Promise<{
    channel: string;
    accountId: string;
    conversationId: string;
    threadId?: string | number;
  } | null>;
}): Promise<boolean> {
  if (saveOpenclawDeliveryFromBridge(ctx)) return true;
  if (typeof ctx.getCurrentConversationBinding !== "function") return false;
  try {
    const b = await ctx.getCurrentConversationBinding();
    if (!b?.channel?.trim() || !b.conversationId?.trim()) return false;
    persistOpenclawDelivery({
      channel: b.channel.trim(),
      target: b.conversationId.trim(),
      accountId: b.accountId?.trim(),
      threadId: b.threadId,
    });
    return true;
  } catch {
    return false;
  }
}

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
    persistOpenclawDeliveryList(payload);
    return true;
  }
  persistOpenclawDeliveryList(payload);
  return true;
}

/** message_received 备用：部分通道 inbound_claim 字段不全 */
export function trySaveOpenclawDeliveryFromMessageHook(
  event: { from: string },
  ctx: { channelId: string; accountId?: string; conversationId?: string },
): boolean {
  const target = ctx.conversationId?.trim() || event.from?.trim();
  const channel = ctx.channelId?.trim();
  if (!target || !channel) return false;
  const payload: OpenclawDeliveryFile = {
    channel,
    target,
    ...(ctx.accountId?.trim() ? { accountId: ctx.accountId.trim() } : {}),
  };
  if (!fs.existsSync(OPENCLAW_DELIVERY_PATH)) {
    fs.mkdirSync(path.dirname(OPENCLAW_DELIVERY_PATH), { recursive: true });
    fs.writeFileSync(OPENCLAW_DELIVERY_PATH, JSON.stringify(payload, null, 2), "utf8");
    persistOpenclawDeliveryList(payload);
    return true;
  }
  persistOpenclawDeliveryList(payload);
  return true;
}
