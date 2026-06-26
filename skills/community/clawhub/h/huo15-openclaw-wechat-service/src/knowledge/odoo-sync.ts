/**
 * Odoo knowledge.article 同步（JSON-RPC）。
 *
 * 流程：
 *  1. common.login(db, user, pass) → uid（按 account+db+user 缓存）
 *  2. object.execute_kw(...) 调用 knowledge.article.{search, create, write}
 *
 * 按 (accountId, senderId, date) 唯一定位一个 article：
 *  - 存在 → write 追加 body
 *  - 不存在 → create with parent_id
 */

import crypto from "node:crypto";

import { Agent, ProxyAgent, fetch as undiciFetch } from "undici";

import type {
  ResolvedWechatServiceAccount,
  WechatServiceKnowledgeOdooConfig,
  WechatServiceNetworkConfig,
  WechatServiceUnifiedInboundEvent,
} from "../types.js";

type LoginCacheEntry = { uid: number; ts: number };

const loginCache = new Map<string, LoginCacheEntry>();
const LOGIN_TTL_MS = 30 * 60 * 1000;

function cacheKey(cfg: WechatServiceKnowledgeOdooConfig): string {
  return `${cfg.url}|${cfg.db}|${cfg.username}`;
}

function selectDispatcher(network?: WechatServiceNetworkConfig) {
  if (network?.egressProxyUrl?.trim()) {
    return new ProxyAgent({ uri: network.egressProxyUrl.trim() });
  }
  return new Agent({
    connect: { timeout: network?.timeoutMs ?? 15_000 },
    bodyTimeout: network?.timeoutMs ?? 30_000,
    headersTimeout: network?.timeoutMs ?? 15_000,
  });
}

async function jsonrpc(params: {
  url: string;
  path: string;
  service: string;
  method: string;
  args: unknown[];
  network?: WechatServiceNetworkConfig;
}): Promise<unknown> {
  const base = params.url.endsWith("/") ? params.url.slice(0, -1) : params.url;
  const res = await undiciFetch(`${base}${params.path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method: "call",
      params: {
        service: params.service,
        method: params.method,
        args: params.args,
      },
      id: crypto.randomInt(1, 1_000_000_000),
    }),
    dispatcher: selectDispatcher(params.network),
  });
  const data = (await res.json()) as { result?: unknown; error?: { message?: string; data?: { message?: string } } };
  if (data.error) {
    throw new Error(
      `[wechat-service] odoo ${params.service}.${params.method} failed: ${data.error.data?.message ?? data.error.message ?? JSON.stringify(data.error)}`,
    );
  }
  return data.result;
}

async function loginOdoo(
  cfg: WechatServiceKnowledgeOdooConfig,
  network?: WechatServiceNetworkConfig,
): Promise<number> {
  const key = cacheKey(cfg);
  const now = Date.now();
  const cached = loginCache.get(key);
  if (cached && now - cached.ts < LOGIN_TTL_MS) return cached.uid;
  const uid = (await jsonrpc({
    url: cfg.url,
    path: "/jsonrpc",
    service: "common",
    method: "login",
    args: [cfg.db, cfg.username, cfg.password],
    network,
  })) as number | false;
  if (!uid || typeof uid !== "number") {
    throw new Error(`[wechat-service] odoo login failed for ${cfg.username}@${cfg.db}`);
  }
  loginCache.set(key, { uid, ts: now });
  return uid;
}

async function callKw(params: {
  cfg: WechatServiceKnowledgeOdooConfig;
  network?: WechatServiceNetworkConfig;
  uid: number;
  model: string;
  method: string;
  args: unknown[];
  kwargs?: Record<string, unknown>;
}): Promise<unknown> {
  return jsonrpc({
    url: params.cfg.url,
    path: "/jsonrpc",
    service: "object",
    method: "execute_kw",
    args: [
      params.cfg.db,
      params.uid,
      params.cfg.password,
      params.model,
      params.method,
      params.args,
      params.kwargs ?? {},
    ],
    network: params.network,
  });
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function formatTime(ts: number): { date: string; time: string } {
  const d = new Date(ts);
  const pad = (n: number) => String(n).padStart(2, "0");
  return {
    date: `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`,
    time: `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`,
  };
}

export type OdooWriteResult = {
  articleId: number;
  created: boolean;
  title: string;
};

export async function writeOdooTranscript(params: {
  account: ResolvedWechatServiceAccount;
  event: WechatServiceUnifiedInboundEvent;
  replyText: string;
}): Promise<OdooWriteResult | undefined> {
  const odoo = params.account.knowledgeSync?.odoo;
  if (!odoo?.url || !odoo.db || !odoo.username || !odoo.password) return undefined;
  const network = params.account.network;
  const uid = await loginOdoo(odoo, network);
  const senderId =
    params.event.conversation.senderId || params.event.raw.fromUserName || "unknown";
  const createdAtMs =
    (params.event.raw.createTime || Math.floor(Date.now() / 1000)) * 1000;
  const { date, time } = formatTime(createdAtMs);
  const accountName = params.account.name ?? params.account.accountId;
  const title = `[wechat-service] ${accountName} · ${senderId} · ${date}`;
  const entryHtml =
    `<h3>${escapeHtml(time)}</h3>` +
    `<p><strong>用户${params.event.senderName ? `（${escapeHtml(params.event.senderName)}）` : ""}</strong>：${escapeHtml(params.event.text || "(空)")}</p>` +
    `<p><strong>AI</strong>：${escapeHtml(params.replyText || "(无回复)")}</p>`;

  const existing = (await callKw({
    cfg: odoo,
    network,
    uid,
    model: "knowledge.article",
    method: "search_read",
    args: [[["name", "=", title]], ["id", "body"]],
    kwargs: { limit: 1 },
  })) as Array<{ id: number; body?: string | false }>;

  if (Array.isArray(existing) && existing[0]) {
    const prev = typeof existing[0].body === "string" ? existing[0].body : "";
    const nextBody = prev + entryHtml;
    await callKw({
      cfg: odoo,
      network,
      uid,
      model: "knowledge.article",
      method: "write",
      args: [[existing[0].id], { body: nextBody }],
    });
    return { articleId: existing[0].id, created: false, title };
  }

  const createVals: Record<string, unknown> = {
    name: title,
    body:
      `<p>来源：微信服务号「${escapeHtml(accountName)}」（accountId=${escapeHtml(params.account.accountId)}）</p>` +
      `<p>用户 openid：${escapeHtml(senderId)}</p>` +
      `<p>日期：${escapeHtml(date)}</p>` +
      "<hr/>" +
      entryHtml,
  };
  if (typeof odoo.articleParentId === "number") {
    createVals.parent_id = odoo.articleParentId;
  }
  const articleId = (await callKw({
    cfg: odoo,
    network,
    uid,
    model: "knowledge.article",
    method: "create",
    args: [createVals],
  })) as number;
  return { articleId, created: true, title };
}

export function invalidateOdooLogin(cfg: WechatServiceKnowledgeOdooConfig): void {
  loginCache.delete(cacheKey(cfg));
}
