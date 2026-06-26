const DEFAULT_BASE_URL = "https://api.podfetcher.com";
const DEFAULT_API_KEY_HEADER = "X-API-Key";
const DEFAULT_TIMEOUT_MS = 15_000;

/**
 * @typedef {Object} PodfetcherClientOptions
 * @property {string} [baseUrl]
 * @property {string} [apiKey]
 * @property {string} [apiKeyHeader]
 * @property {number} [timeoutMs]
 */

export class PodfetcherApiError extends Error {
  /**
   * @param {Object} params
   * @param {number} params.status
   * @param {string} [params.code]
   * @param {string} [params.message]
   * @param {Record<string, string> | undefined} [params.details]
   * @param {unknown} [params.body]
   */
  constructor({ status, code, message, details, body }) {
    super(message || `Request failed with status ${status}`);
    this.name = "PodfetcherApiError";
    this.status = status;
    this.code = code;
    this.details = details;
    this.body = body;
  }
}

/**
 * @param {PodfetcherClientOptions} [options]
 */
export function createPodfetcherClient(options = {}) {
  const baseUrl = options.baseUrl || process.env.PODFETCHER_BASE_URL || DEFAULT_BASE_URL;
  const apiKey = options.apiKey ?? process.env.PODFETCHER_API_KEY;
  const apiKeyHeader = options.apiKeyHeader || process.env.PODFETCHER_API_KEY_HEADER || DEFAULT_API_KEY_HEADER;
  const timeoutMs = parsePositiveInt(options.timeoutMs, DEFAULT_TIMEOUT_MS);

  /**
   * @param {string} path
   * @param {Object} [requestOptions]
   * @param {"GET"|"POST"} [requestOptions.method]
   * @param {Record<string, unknown>} [requestOptions.query]
   * @param {unknown} [requestOptions.body]
   * @param {string} [requestOptions.idempotencyKey]
   */
  async function request(path, requestOptions = {}) {
    if (!apiKey) {
      throw new Error(
        "Missing API key. Provide --api-key or set PODFETCHER_API_KEY.",
      );
    }

    const method = requestOptions.method || "GET";
    const url = new URL(path, ensureTrailingSlash(baseUrl));
    appendQuery(url, requestOptions.query || {});

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    const headers = {
      Accept: "application/json",
      [apiKeyHeader]: apiKey,
    };
    if (requestOptions.idempotencyKey) {
      headers["Idempotency-Key"] = requestOptions.idempotencyKey;
    }
    if (requestOptions.body !== undefined) {
      headers["Content-Type"] = "application/json";
    }

    let response;
    try {
      response = await fetch(url, {
        method,
        headers,
        body:
          requestOptions.body === undefined
            ? undefined
            : JSON.stringify(requestOptions.body),
        signal: controller.signal,
      });
    } catch (error) {
      if (error?.name === "AbortError") {
        throw new Error(`Request timed out after ${timeoutMs}ms (${method} ${url.pathname})`);
      }
      throw new Error(
        `Network request failed (${method} ${url.origin}${url.pathname}): ${error?.message || String(error)}`,
      );
    } finally {
      clearTimeout(timeoutId);
    }

    const text = await response.text();
    const payload = parseJsonOrNull(text);

    if (!response.ok) {
      if (payload && typeof payload === "object") {
        throw new PodfetcherApiError({
          status: response.status,
          code: payload.code,
          message: payload.message || `Request failed with status ${response.status}`,
          details: payload.details,
          body: payload,
        });
      }
      throw new PodfetcherApiError({
        status: response.status,
        message: text || `Request failed with status ${response.status}`,
      });
    }

    return payload;
  }

  return {
    /**
     * @param {Object} params
     * @param {string} params.q
     * @param {number} [params.limit]
     * @param {string} [params.cursor]
     */
    async searchShows({ q, limit, cursor }) {
      return request("/v1/shows/search", {
        method: "GET",
        query: { q, limit, cursor },
      });
    },

    /**
     * @param {Object} params
     * @param {string} params.showId
     * @param {string} [params.since]
     * @param {string} [params.from]
     * @param {string} [params.to]
     * @param {string} [params.orderBy]
     * @param {string} [params.order]
     * @param {number} [params.limit]
     * @param {string} [params.cursor]
     */
    async listEpisodes({ showId, since, from, to, orderBy, order, limit, cursor }) {
      return request(`/v1/shows/${encodeURIComponent(showId)}/episodes`, {
        method: "GET",
        query: { since, from, to, orderBy, order, limit, cursor },
      });
    },

    /**
     * @param {Object} params
     * @param {string} params.episodeId
     * @param {string} [params.idempotencyKey]
     */
    async fetchTranscript({ episodeId, idempotencyKey }) {
      return request(`/v1/episodes/${encodeURIComponent(episodeId)}/transcript:fetch`, {
        method: "POST",
        idempotencyKey,
      });
    },

    /**
     * @param {Object} params
     * @param {string} params.jobId
     */
    async getTranscriptJob({ jobId }) {
      return request(`/v1/transcript-jobs/${encodeURIComponent(jobId)}`, {
        method: "GET",
      });
    },

    /**
     * Fetches transcript and optionally polls job status until READY.
     * @param {Object} params
     * @param {string} params.episodeId
     * @param {string} [params.idempotencyKey]
     * @param {number} [params.pollIntervalMs]
     * @param {number} [params.waitTimeoutMs]
     */
    async fetchTranscriptAndWait({
      episodeId,
      idempotencyKey,
      pollIntervalMs = 1_000,
      waitTimeoutMs = 60_000,
    }) {
      const first = await this.fetchTranscript({ episodeId, idempotencyKey });
      if (isTranscriptReadyResponse(first)) {
        return first;
      }
      if (!isTranscriptProcessingResponse(first)) {
        throw new Error("Unexpected transcript response shape");
      }

      const startedAt = Date.now();
      let lastStatus = "PROCESSING";
      while (Date.now() - startedAt < waitTimeoutMs) {
        await sleep(pollIntervalMs);
        const job = await this.getTranscriptJob({ jobId: first.jobId });
        lastStatus = job.status || lastStatus;

        if (job.status === "FAILED") {
          throw new Error(
            `Transcript job ${first.jobId} failed: ${job.failureReason || "unknown reason"}`,
          );
        }
        if (job.status !== "READY") {
          continue;
        }

        const resolved = await this.fetchTranscript({ episodeId });
        if (isTranscriptReadyResponse(resolved)) {
          return resolved;
        }
      }

      throw new Error(
        `Timed out after ${waitTimeoutMs}ms waiting for transcript job ${first.jobId} (last status: ${lastStatus})`,
      );
    },
  };
}

/**
 * @param {unknown} payload
 * @returns {boolean}
 */
export function isTranscriptReadyResponse(payload) {
  return Boolean(
    payload &&
      typeof payload === "object" &&
      "episodeId" in payload &&
      "transcript" in payload,
  );
}

/**
 * @param {unknown} payload
 * @returns {boolean}
 */
export function isTranscriptProcessingResponse(payload) {
  return Boolean(
    payload &&
      typeof payload === "object" &&
      "jobId" in payload &&
      payload.status === "PROCESSING",
  );
}

function ensureTrailingSlash(input) {
  return input.endsWith("/") ? input : `${input}/`;
}

function parsePositiveInt(value, fallback) {
  if (value === undefined || value === null) {
    return fallback;
  }
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return fallback;
  }
  return Math.floor(parsed);
}

function appendQuery(url, query) {
  for (const [key, value] of Object.entries(query)) {
    if (value === undefined || value === null || value === "") {
      continue;
    }
    url.searchParams.set(key, String(value));
  }
}

function parseJsonOrNull(text) {
  if (!text) {
    return null;
  }
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
