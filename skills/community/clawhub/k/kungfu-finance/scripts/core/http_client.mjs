import { buildDefaultHeaders, cleanObject, getBaseUrl } from "./runtime.mjs";

function buildUrl(path, query = {}) {
  const url = new URL(path, getBaseUrl());
  const cleanQuery = cleanObject(query);
  for (const [key, value] of Object.entries(cleanQuery)) {
    url.searchParams.set(key, String(value));
  }
  return url;
}

function tryParseJson(text) {
  if (!text) {
    return null;
  }
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

function mapHttpError(status, detail) {
  if (status === 401) {
    return {
      code: "AUTH_INVALID",
      message: detail || "鉴权凭证无效或已过期"
    };
  }

  if (status === 403) {
    return {
      code: "PERMISSION_DENIED",
      message: detail || "当前账号无权访问该能力"
    };
  }

  if (status === 429) {
    return {
      code: "RATE_LIMITED",
      message: detail || "请求过于频繁，请稍后再试"
    };
  }

  return {
    code: "UPSTREAM_ERROR",
    message: detail || "上游服务请求失败"
  };
}

export function createHttpClient({ fetchImpl } = {}) {
  async function requestJson(method, path, { query = {}, headers = {}, body, timeoutMs = 30000 } = {}) {
    const url = buildUrl(path, query);
    const effectiveFetch = fetchImpl ?? fetch;
    const response = await effectiveFetch(url, {
      method,
      headers: buildDefaultHeaders({
        ...(body ? { "Content-Type": "application/json" } : {}),
        ...headers
      }),
      body: body ? JSON.stringify(body) : undefined,
      signal: AbortSignal.timeout(timeoutMs)
    });

    const text = await response.text();
    const parsed = tryParseJson(text);

    if (!response.ok) {
      const detail =
        typeof parsed === "string"
          ? parsed
          : parsed?.detail || parsed?.message || JSON.stringify(parsed);
      const mapped = mapHttpError(response.status, detail);
      const error = new Error(mapped.message);
      error.code = mapped.code;
      error.status = response.status;
      error.detail = detail;
      throw error;
    }

    return parsed;
  }

  async function getJson(path, query = {}, options = {}) {
    return requestJson("GET", path, { query, ...options });
  }

  return {
    requestJson,
    getJson
  };
}

const defaultClient = createHttpClient();

export async function requestJson(method, path, options = {}) {
  return defaultClient.requestJson(method, path, options);
}

export async function getJson(path, query = {}, options = {}) {
  return defaultClient.getJson(path, query, options);
}
