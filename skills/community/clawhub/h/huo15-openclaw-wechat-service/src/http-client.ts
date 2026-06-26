/**
 * 轻量 HTTP 客户端：基于 undici.fetch，统一 JSON 请求/响应处理、超时和代理。
 */

import { Agent, ProxyAgent, fetch as undiciFetch } from "undici";

import type { WechatServiceNetworkConfig } from "./types.js";

export const DEFAULT_API_BASE_URL = "https://api.weixin.qq.com";

export type WechatApiError = Error & {
  errcode?: number;
  errmsg?: string;
  endpoint?: string;
  httpStatus?: number;
  raw?: unknown;
};

export function buildWechatApiError(params: {
  endpoint: string;
  errcode?: number;
  errmsg?: string;
  httpStatus?: number;
  raw?: unknown;
}): WechatApiError {
  const err = new Error(
    `[wechat-service] API ${params.endpoint} failed: errcode=${params.errcode ?? "n/a"} errmsg=${params.errmsg ?? "n/a"} httpStatus=${params.httpStatus ?? "n/a"}`,
  ) as WechatApiError;
  err.errcode = params.errcode;
  err.errmsg = params.errmsg;
  err.endpoint = params.endpoint;
  err.httpStatus = params.httpStatus;
  err.raw = params.raw;
  return err;
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

export type JsonRequestOptions = {
  method?: "GET" | "POST" | "PUT" | "DELETE";
  endpoint: string;
  baseUrl?: string;
  query?: Record<string, string | number | boolean | undefined | null>;
  body?: unknown;
  network?: WechatServiceNetworkConfig;
  signal?: AbortSignal;
  headers?: Record<string, string>;
  treatErrcodeAsError?: boolean;
};

function buildUrl(params: JsonRequestOptions): string {
  const base = params.baseUrl ?? params.network?.apiBaseUrl ?? DEFAULT_API_BASE_URL;
  const u = new URL(params.endpoint, base.endsWith("/") ? base : `${base}/`);
  for (const [k, v] of Object.entries(params.query ?? {})) {
    if (v == null) continue;
    u.searchParams.set(k, String(v));
  }
  return u.toString();
}

/**
 * **jsonRequest**
 *
 * 发起 JSON 请求，并统一解析微信 `{ errcode, errmsg }` 错误格式。
 * 当 `treatErrcodeAsError` 为 true（默认）时，非 0 的 errcode 会抛出 WechatApiError。
 */
export async function jsonRequest<T extends Record<string, unknown> = Record<string, unknown>>(
  opts: JsonRequestOptions,
): Promise<T> {
  const dispatcher = selectDispatcher(opts.network);
  const url = buildUrl(opts);
  const method = opts.method ?? (opts.body ? "POST" : "GET");
  const headers: Record<string, string> = {
    Accept: "application/json",
    ...(opts.headers ?? {}),
  };
  let bodyPayload: string | Buffer | undefined;
  if (opts.body != null) {
    if (typeof opts.body === "string" || Buffer.isBuffer(opts.body)) {
      bodyPayload = opts.body as string | Buffer;
    } else {
      headers["Content-Type"] = headers["Content-Type"] ?? "application/json";
      bodyPayload = JSON.stringify(opts.body);
    }
  }
  const res = await undiciFetch(url, {
    method,
    headers,
    body: bodyPayload,
    dispatcher,
    signal: opts.signal,
  });
  const httpStatus = res.status;
  const contentType = res.headers.get("content-type") ?? "";
  const raw = await res.arrayBuffer();
  const text = Buffer.from(raw).toString("utf8");
  let parsed: unknown = undefined;
  if (contentType.includes("application/json") || /^\s*\{/.test(text)) {
    try {
      parsed = JSON.parse(text);
    } catch {
      parsed = undefined;
    }
  }
  if (!res.ok) {
    throw buildWechatApiError({
      endpoint: opts.endpoint,
      errcode: (parsed as { errcode?: number })?.errcode,
      errmsg: (parsed as { errmsg?: string })?.errmsg,
      httpStatus,
      raw: parsed ?? text,
    });
  }
  const data = (parsed ?? { raw: text }) as T;
  const errcode = (data as { errcode?: number }).errcode;
  if (opts.treatErrcodeAsError !== false && typeof errcode === "number" && errcode !== 0) {
    throw buildWechatApiError({
      endpoint: opts.endpoint,
      errcode,
      errmsg: (data as { errmsg?: string }).errmsg,
      httpStatus,
      raw: data,
    });
  }
  return data;
}

/**
 * **binaryRequest**
 *
 * 下载微信侧二进制资源（如临时素材）。返回 buffer + content-type + 推荐文件名。
 */
export async function binaryRequest(opts: JsonRequestOptions): Promise<{
  buffer: Buffer;
  contentType: string;
  filename?: string;
  httpStatus: number;
  jsonError?: { errcode: number; errmsg?: string };
}> {
  const dispatcher = selectDispatcher(opts.network);
  const url = buildUrl(opts);
  const method = opts.method ?? "GET";
  const res = await undiciFetch(url, {
    method,
    headers: opts.headers,
    body:
      opts.body == null
        ? undefined
        : typeof opts.body === "string" || Buffer.isBuffer(opts.body)
          ? (opts.body as string | Buffer)
          : JSON.stringify(opts.body),
    dispatcher,
    signal: opts.signal,
  });
  const contentType = res.headers.get("content-type") ?? "application/octet-stream";
  const dispositon = res.headers.get("content-disposition") ?? "";
  const filenameMatch = /filename="?([^"]+)"?/i.exec(dispositon);
  const filename = filenameMatch?.[1];
  const buffer = Buffer.from(await res.arrayBuffer());
  let jsonError: { errcode: number; errmsg?: string } | undefined;
  if (contentType.includes("application/json")) {
    try {
      const parsed = JSON.parse(buffer.toString("utf8")) as { errcode?: number; errmsg?: string };
      if (typeof parsed.errcode === "number" && parsed.errcode !== 0) {
        jsonError = { errcode: parsed.errcode, errmsg: parsed.errmsg };
      }
    } catch {
      /* ignore */
    }
  }
  return { buffer, contentType, filename, httpStatus: res.status, jsonError };
}
