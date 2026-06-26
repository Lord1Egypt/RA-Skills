import {
  CliError,
  DEFAULT_BACKOFF_MS,
  DEFAULT_RETRY_COUNT,
  DEFAULT_TIMEOUT_MS,
  ExitCode,
  toErrorMessage,
} from "./config.ts";
import type { HttpResult } from "./types.ts";

export interface HttpRequest {
  method: "GET" | "POST";
  url: string;
  params?: Record<string, string>;
  headers?: Record<string, string>;
  body?: unknown;
  timeoutMs?: number;
  retries?: number;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function buildUrlWithParams(url: string, params?: Record<string, string>): string {
  if (!params || Object.keys(params).length === 0) {
    return url;
  }

  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    query.set(key, value);
  }

  return `${url}?${query.toString()}`;
}

export async function requestWithRetry(request: HttpRequest): Promise<HttpResult> {
  const timeoutMs = request.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const retries = request.retries ?? DEFAULT_RETRY_COUNT;
  const fullUrl = request.method === "GET"
    ? buildUrlWithParams(request.url, request.params)
    : request.url;

  let lastError: unknown;

  for (let attempt = 0; attempt <= retries; attempt += 1) {
    const isLastAttempt = attempt === retries;

    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), timeoutMs);

      const fetchOptions: RequestInit = {
        method: request.method,
        signal: controller.signal,
        headers: {
          Accept: "application/json",
          ...request.headers,
        },
      };

      if (request.method === "POST" && request.body !== undefined) {
        fetchOptions.body = JSON.stringify(request.body);
        (fetchOptions.headers as Record<string, string>)["Content-Type"] = "application/json";
      }

      const response = await fetch(fullUrl, fetchOptions);
      clearTimeout(timer);

      let payload: unknown;
      try {
        payload = await response.json();
      } catch (jsonError) {
        throw new CliError(
          `Failed to parse JSON response from ${fullUrl}: ${toErrorMessage(jsonError)}`,
          ExitCode.NETWORK,
          { cause: jsonError },
        );
      }

      if (!response.ok) {
        if (!isLastAttempt && (response.status >= 500 || response.status === 429)) {
          await sleep(DEFAULT_BACKOFF_MS * 2 ** attempt);
          continue;
        }
      }

      return { status: response.status, payload };
    } catch (error) {
      lastError = error;

      if (error instanceof CliError) {
        throw error;
      }

      if (!isLastAttempt) {
        await sleep(DEFAULT_BACKOFF_MS * 2 ** attempt);
        continue;
      }
    }
  }

  if (lastError instanceof CliError) {
    throw lastError;
  }

  throw new CliError(
    `Network request failed after retries: ${toErrorMessage(lastError)}`,
    ExitCode.NETWORK,
    { cause: lastError },
  );
}
