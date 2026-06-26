/**
 * ZhenInsure Chat & Handoff Skill Proxy
 *
 * Exposes consumer-facing AI chat and human-advisor handoff
 * through API Key authentication.
 *
 * All endpoints are synchronous (non-streaming) JSON —
 * designed for skill action calls where SSE is not viable.
 */

const DEFAULT_BASE_URL = "https://www.zhenins.com";
const SKILL_VERSION = "2.0.0";
const REQUEST_TIMEOUT_MS = Number(process.env.ZHENINSURE_TIMEOUT_MS) || 20000;

const ALLOWED_ENDPOINTS = new Map([
  ["/api/v1/skill/chat/conversations", ["POST"]],
  ["/api/v1/skill/chat/messages", ["POST"]],
  ["/api/v1/skill/chat/handoff", ["POST"]],
]);

const COST_TABLE = {
  "/api/v1/skill/chat/conversations": { POST: 0 },
  "/api/v1/skill/chat/messages": { POST: 15 },
  "/api/v1/skill/chat/handoff": { POST: 0 },
};

const CONSOLE_URLS = {
  apiKeys: "https://console.zhenrobot.com/zhenins/keys",
  billing: "https://console.zhenrobot.com/zhenins/billing",
};

function fmtCost(c) {
  return c === 0 ? "Free" : `¥${(c / 100).toFixed(2)}`;
}

function normBase(raw) {
  if (!raw) return DEFAULT_BASE_URL;
  return String(raw).trim().replace(/\/+$/, "") || DEFAULT_BASE_URL;
}

function allowed(ep, method) {
  const m = ALLOWED_ENDPOINTS.get(ep);
  return m ? m.includes(method.toUpperCase()) : false;
}

export async function proxy(context) {
  const apiKey =
    context?.secrets?.ZHENINSURE_API_KEY ??
    context?.env?.ZHENINSURE_API_KEY ??
    process.env.ZHENINSURE_API_KEY;

  const baseUrl = normBase(
    context?.config?.ZHENINSURE_BASE_URL ??
    context?.env?.ZHENINSURE_BASE_URL ??
    process.env.ZHENINSURE_BASE_URL
  );

  const args = context?.args ?? context?.parameters ?? {};
  const endpoint = args.endpoint;
  const method = (args.method ?? "POST").toUpperCase();
  const body = args.body;

  if (!apiKey) {
    return {
      success: false,
      error: "missing_api_key",
      message: "ZHENINSURE_API_KEY 未配置。请运行：\n  claw config set ZHENINSURE_API_KEY sk_live_xxxx",
      action: { type: "manage_keys", url: CONSOLE_URLS.apiKeys, description: "前往 Console 管理 API Key" },
    };
  }

  if (!/^sk_live_[A-Za-z0-9_-]{32,}$/.test(apiKey)) {
    return {
      success: false,
      error: "invalid_api_key_format",
      message: "API Key 格式不正确。",
      action: { type: "manage_keys", url: CONSOLE_URLS.apiKeys, description: "前往 Console 重新生成" },
    };
  }

  if (!endpoint) {
    return {
      success: false,
      error: "missing_endpoint",
      message: "缺少 endpoint。可用：\n" + Array.from(ALLOWED_ENDPOINTS.keys()).join("\n"),
    };
  }

  if (!allowed(endpoint, method)) {
    return {
      success: false,
      error: "forbidden_endpoint",
      endpoint, method,
      message: `端点不可用。允许列表：${Array.from(ALLOWED_ENDPOINTS.entries())
        .map(([p, ms]) => `${p} [${ms.join(", ")}]`).join("; ")}`,
    };
  }

  if (method === "GET" && body != null) {
    return { success: false, error: "invalid_request", message: "GET 请求不支持 body。" };
  }

  const costCents = COST_TABLE[endpoint]?.[method] ?? null;
  const url = `${baseUrl}${endpoint}`;

  let res;
  try {
    const ctl = new AbortController();
    const timer = setTimeout(() => ctl.abort(), REQUEST_TIMEOUT_MS);
    res = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
        "User-Agent": `ZhenInsure-Skill/${SKILL_VERSION}`,
        Accept: "application/json",
      },
      body: method === "POST" && body ? JSON.stringify(body) : undefined,
      signal: ctl.signal,
    });
    clearTimeout(timer);
  } catch (e) {
    if (e.name === "AbortError") {
      return { success: false, error: "timeout", message: `请求超时（${REQUEST_TIMEOUT_MS}ms），请稍后重试。`, endpoint, method, cost: fmtCost(costCents) };
    }
    return { success: false, error: "network_error", message: `网络失败：${e.message}`, endpoint, method, cost: fmtCost(costCents) };
  }

  let data = null;
  try {
    const ct = res.headers.get("content-type") || "";
    if (ct.includes("application/json")) data = await res.json();
    else { const t = await res.text(); if (t) data = { raw_body: t }; }
  } catch { /* ignore */ }

  if (res.ok) {
    return { success: true, endpoint, method, cost: fmtCost(costCents), data, message: `成功 — ${endpoint}` };
  }

  const detail = data?.detail ?? data?.message ?? data?.error ?? `HTTP ${res.status}`;

  if (res.status === 402 || (res.status === 403 && /余额|balance|insufficient/.test(String(detail)))) {
    return {
      success: false,
      error: "insufficient_balance",
      endpoint, method, cost: null, raw: data, status: res.status,
      message: `余额不足：${detail}\n预计费用：${fmtCost(costCents)}\n请充值后继续。`,
      action: { type: "recharge", url: CONSOLE_URLS.billing, description: "前往 Console 充值" },
    };
  }

  if (res.status === 401 || res.status === 403) {
    return {
      success: false,
      error: res.status === 401 ? "unauthorized" : "forbidden",
      endpoint, method, cost: null, raw: data, status: res.status,
      message: `鉴权失败：${detail}\n请检查 API Key。`,
      action: { type: "manage_keys", url: CONSOLE_URLS.apiKeys, description: "前往 Console 管理 API Key" },
    };
  }

  if (res.status === 429) {
    return { success: false, error: "rate_limited", endpoint, method, cost: null, raw: data, status: res.status, message: `限流：${detail}\n请稍后重试。` };
  }

  if (res.status >= 500) {
    return { success: false, error: "server_error", endpoint, method, cost: null, raw: data, status: res.status, message: `服务端错误 (${res.status})：${detail}\n请稍后重试。` };
  }

  return { success: false, error: "api_error", endpoint, method, cost: null, raw: data, status: res.status, message: `API 错误 (${res.status})：${detail}` };
}

export default proxy;
