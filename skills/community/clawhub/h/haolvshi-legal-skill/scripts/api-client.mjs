import { setTimeout as delay } from 'node:timers/promises';
import { ApiError } from './errors.mjs';

function appendQuery(url, query = {}) {
  for (const [key, value] of Object.entries(query)) {
    if (value === undefined || value === null || value === '') continue;
    if (Array.isArray(value)) {
      value.forEach(item => url.searchParams.append(key, String(item)));
    } else {
      url.searchParams.set(key, String(value));
    }
  }
}

function parseTextPayload(text) {
  const trimmed = text.trim();
  if (!trimmed) return null;

  let value = trimmed;
  for (let i = 0; i < 2 && typeof value === 'string'; i += 1) {
    try {
      value = JSON.parse(value);
    } catch {
      break;
    }
  }
  return value;
}

function serviceMessage(payload) {
  return payload?.response?.msg
    || payload?.response?.errorMsg
    || payload?.msg
    || payload?.message
    || '服务请求失败';
}

export function unwrapServiceResult(payload) {
  if (!payload || typeof payload !== 'object' || !payload.response) {
    return payload;
  }

  if (payload.response.success !== true) {
    throw new ApiError(
      `SERVICE_${payload.response.code ?? 'FAILED'}`,
      serviceMessage(payload),
      { details: payload.response }
    );
  }
  return payload.data;
}

export class ApiClient {
  constructor(config, options = {}) {
    this.config = config;
    this.fetchImpl = options.fetchImpl || globalThis.fetch;
    if (typeof this.fetchImpl !== 'function') {
      throw new ApiError('FETCH_UNAVAILABLE', '当前运行环境缺少网络请求能力');
    }
  }

  async request(pathname, options = {}) {
    const method = String(options.method || 'GET').toUpperCase();
    const url = new URL(`${this.config.apiBase}/${String(pathname).replace(/^\/+/, '')}`);
    appendQuery(url, options.query);

    const headers = new Headers(options.headers || {});
    headers.set('Accept', options.accept || 'application/json, text/plain;q=0.9, */*;q=0.8');
    headers.set('User-Agent', this.config.userAgent);
    if (options.userId) headers.set('userId', options.userId);
    if (options.token) headers.set('token', options.token);

    let body;
    if (options.formData) {
      body = options.formData;
    } else if (options.body !== undefined) {
      headers.set('Content-Type', 'application/json; charset=utf-8');
      body = JSON.stringify(options.body);
    }

    const timeoutMs = options.timeoutMs || this.config.requestTimeoutMs;
    const attempts = method === 'GET' ? 3 : 1;
    let lastError;

    for (let attempt = 1; attempt <= attempts; attempt += 1) {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), timeoutMs);
      try {
        const response = await this.fetchImpl(url, {
          method,
          headers,
          body,
          signal: controller.signal,
          redirect: 'follow'
        });
        const buffer = Buffer.from(await response.arrayBuffer());

        if (!response.ok) {
          const text = buffer.toString('utf8');
          throw new ApiError('HTTP_ERROR', `接口返回 HTTP ${response.status}`, {
            retryable: response.status >= 500,
            httpStatus: response.status,
            details: text.slice(0, 1000)
          });
        }

        if (options.responseType === 'buffer') {
          return { buffer, headers: response.headers, url: response.url };
        }

        const payload = parseTextPayload(buffer.toString('utf8'));
        return options.unwrap === false ? payload : unwrapServiceResult(payload);
      } catch (error) {
        const aborted = error?.name === 'AbortError';
        lastError = error instanceof ApiError
          ? error
          : new ApiError(
              aborted ? 'REQUEST_TIMEOUT' : 'NETWORK_ERROR',
              aborted ? `接口请求超过 ${timeoutMs} 毫秒` : `网络请求失败：${error.message}`,
              { retryable: true, cause: error }
            );

        if (attempt >= attempts || !lastError.retryable) throw lastError;
        await delay(250 * attempt);
      } finally {
        clearTimeout(timer);
      }
    }

    throw lastError;
  }

  get(pathname, options = {}) {
    return this.request(pathname, { ...options, method: 'GET' });
  }

  post(pathname, body, options = {}) {
    return this.request(pathname, { ...options, method: 'POST', body });
  }

  upload(pathname, formData, options = {}) {
    return this.request(pathname, { ...options, method: 'POST', formData });
  }
}
