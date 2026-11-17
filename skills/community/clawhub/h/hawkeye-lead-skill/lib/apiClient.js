import { BASE_URL, COOKIE_NAME } from "./config.js";
import { getToken } from "./auth.js";

export class UsageError extends Error {
  constructor(message) {
    super(message);
    this.exitCode = 1;
  }
}

export class AuthError extends Error {
  constructor(message) {
    super(message);
    this.exitCode = 2;
  }
}

export class UpstreamError extends Error {
  constructor(message, body) {
    super(message);
    this.exitCode = 3;
    this.body = body;
  }
}

export class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.exitCode = 4;
  }
}

// entry 是 lib/schemas.js 里 API_SCHEMAS 的一个条目（{path, method, ...}）。
export function buildRequest(entry, bodyObj) {
  const token = getToken();
  const headers = { "Content-Type": "application/json" };
  if (token) {
    headers.Cookie = `${COOKIE_NAME}=${token}`;
  }
  return {
    method: entry.method,
    url: `${BASE_URL}${entry.path}`,
    headers,
    bodyObj,
  };
}

// 目前没有真实"token 已过期"的响应样本，先用组合信号判断，后续拿到真实样本后再校正。
function looksLikeAuthExpired(status, contentType, text, json) {
  if (status === 401 || status === 403) return true;
  if (contentType && contentType.includes("text/html")) return true;
  if (/^\s*<!DOCTYPE|^\s*<html/i.test(text || "")) return true;
  if (json) {
    const code = json.code;
    const msg = String(json.msg ?? json.message ?? "");
    const suspiciousCode = [401, 403, -1, 50110].includes(code);
    const suspiciousMsg = /login|登录|unauthor|token|过期|expire|无权限/i.test(msg);
    if (suspiciousCode && suspiciousMsg) return true;
  }
  return false;
}

export async function callApi(entry, bodyObj) {
  const token = getToken();
  if (!token) {
    throw new AuthError(
      "尚未设置 token，请先获取 access-token 并执行 auth set-token <token>。"
    );
  }
  const { method, url, headers } = buildRequest(entry, bodyObj);

  let response;
  try {
    response = await fetch(url, {
      method,
      headers,
      body: JSON.stringify(bodyObj ?? {}),
    });
  } catch (err) {
    throw new NetworkError(`请求 ${entry.path} 失败（网络错误）：${err.message}`);
  }

  const contentType = response.headers.get("content-type") || "";
  const text = await response.text();
  let json = null;
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    // 非 JSON 响应，交给下面的鉴权失效判断处理
  }

  if (looksLikeAuthExpired(response.status, contentType, text, json)) {
    throw new AuthError(
      "认证已失效或未登录。请重新获取 token（参见 SKILL.md 的认证设置说明）后执行 auth set-token <token>。"
    );
  }

  if (!response.ok) {
    throw new UpstreamError(
      `${entry.path} 返回 HTTP ${response.status}`,
      json ?? text
    );
  }

  return json ?? text;
}
