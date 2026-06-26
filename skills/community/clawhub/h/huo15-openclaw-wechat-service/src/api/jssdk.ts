/**
 * JS-SDK 签名 API
 *
 * https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html
 *
 * 流程：
 *  1. getJsapiTicket() 拉取 jsapi_ticket（有效期 7200s，缓存策略同 access_token）
 *  2. signJsapi({url, ticket, nonceStr?, timestamp?}) 生成 signature
 *  3. 前端 wx.config({appId, timestamp, nonceStr, signature, jsApiList}) 调用
 */

import crypto from "node:crypto";

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type JsapiTicketEntry = {
  accountId: string;
  ticket: string;
  expiresAt: number;
  fetchedAt: number;
};

type JsapiTicketKind = "jsapi" | "wx_card";

const ticketCache = new Map<string, JsapiTicketEntry>();
const inflight = new Map<string, Promise<JsapiTicketEntry>>();
const EARLY_REFRESH_MS = 120_000;

function cacheKey(accountId: string, type: JsapiTicketKind): string {
  return `${accountId}::${type}`;
}

export async function getJsapiTicket(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  type?: JsapiTicketKind;
  forceRefresh?: boolean;
}): Promise<JsapiTicketEntry> {
  const type = params.type ?? "jsapi";
  const key = cacheKey(params.account.accountId, type);
  const now = Date.now();
  const existing = ticketCache.get(key);
  if (!params.forceRefresh && existing && existing.expiresAt - now > EARLY_REFRESH_MS) {
    return existing;
  }
  const pending = inflight.get(key);
  if (pending) return pending;
  const task = (async () => {
    const accessToken = await params.tokenHandle.getAccessToken();
    const data = await jsonRequest<{
      ticket?: string;
      expires_in?: number;
    }>({
      method: "GET",
      endpoint: "cgi-bin/ticket/getticket",
      query: { access_token: accessToken, type },
      network: params.account.network,
    });
    if (!data.ticket) {
      throw new Error("[wechat-service] ticket/getticket missing ticket");
    }
    const entry: JsapiTicketEntry = {
      accountId: params.account.accountId,
      ticket: data.ticket,
      expiresAt: now + Math.max(60, data.expires_in ?? 7200) * 1000,
      fetchedAt: now,
    };
    ticketCache.set(key, entry);
    return entry;
  })()
    .finally(() => {
      inflight.delete(key);
    });
  inflight.set(key, task);
  return task;
}

export function invalidateJsapiTicket(accountId: string, type: JsapiTicketKind = "jsapi"): void {
  ticketCache.delete(cacheKey(accountId, type));
}

export type JsapiSignResult = {
  appId: string;
  timestamp: number;
  nonceStr: string;
  signature: string;
  url: string;
  jsapiTicket: string;
};

export async function signJsapi(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  url: string;
  nonceStr?: string;
  timestamp?: number;
}): Promise<JsapiSignResult> {
  const { ticket } = await getJsapiTicket({
    account: params.account,
    tokenHandle: params.tokenHandle,
  });
  const nonceStr = params.nonceStr ?? randomNonce();
  const timestamp = params.timestamp ?? Math.floor(Date.now() / 1000);
  const cleanUrl = stripFragment(params.url);
  const raw = [
    `jsapi_ticket=${ticket}`,
    `noncestr=${nonceStr}`,
    `timestamp=${timestamp}`,
    `url=${cleanUrl}`,
  ].join("&");
  const signature = crypto.createHash("sha1").update(raw, "utf8").digest("hex");
  return {
    appId: params.account.appId,
    timestamp,
    nonceStr,
    signature,
    url: cleanUrl,
    jsapiTicket: ticket,
  };
}

function stripFragment(url: string): string {
  const hashIdx = url.indexOf("#");
  return hashIdx >= 0 ? url.slice(0, hashIdx) : url;
}

function randomNonce(len = 16): string {
  return crypto.randomBytes(len).toString("hex").slice(0, len);
}
