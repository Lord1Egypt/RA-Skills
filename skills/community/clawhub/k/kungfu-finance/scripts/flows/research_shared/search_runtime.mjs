import {
  getPlatformHeader,
  getResearchSearchApiKey,
  getResearchSearchEndpoint,
  getResearchSearchProvider,
  getResearchSearchTimeoutMs,
  isResearchSearchEnabled,
  isSupportedSearchProvider
} from "../../core/runtime.mjs";

function tryParseJson(text) {
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

function buildBaseContract() {
  return {
    enabled: isResearchSearchEnabled(),
    implemented: false,
    provider: getResearchSearchProvider(),
    status: "disabled",
    reason: "search_runtime_not_enabled",
    allowlist_boundary: "separate_required",
    credential_boundary: "separate_from_kungfu_openkey",
    inherits_kungfu_openkey: false
  };
}

export function buildResearchSearchRuntimeContract() {
  const contract = buildBaseContract();

  if (!contract.enabled) {
    return contract;
  }

  if (!contract.provider) {
    return {
      ...contract,
      status: "misconfigured",
      reason: "search_runtime_provider_missing"
    };
  }

  if (!isSupportedSearchProvider(contract.provider)) {
    return {
      ...contract,
      status: "misconfigured",
      reason: "search_runtime_provider_unsupported"
    };
  }

  const endpoint = getResearchSearchEndpoint();
  if (!endpoint) {
    return {
      ...contract,
      implemented: true,
      status: "misconfigured",
      reason: "search_runtime_missing_endpoint"
    };
  }

  const apiKey = getResearchSearchApiKey();
  if (!apiKey) {
    return {
      ...contract,
      implemented: true,
      status: "misconfigured",
      reason: "search_runtime_missing_api_key"
    };
  }

  return {
    ...contract,
    implemented: true,
    status: "ready",
    reason: null
  };
}

function normalizeSearchItem(item) {
  return {
    title: item?.title || "未命名结果",
    url: item?.url || null,
    snippet: item?.snippet || null,
    source_name: item?.source_name || item?.source || item?.domain || null,
    published_at: item?.published_at || item?.publishedAt || item?.date || null
  };
}

function normalizeSearchResponse(payload) {
  const rawSearches = Array.isArray(payload?.searches)
    ? payload.searches
    : Array.isArray(payload?.results)
      ? payload.results
      : [];

  return rawSearches.map((search) => ({
    search_id: search?.search_id || search?.id || "unknown_search",
    topic: search?.topic || null,
    query: search?.query || null,
    result_count: Array.isArray(search?.results) ? search.results.length : 0,
    results: Array.isArray(search?.results) ? search.results.map(normalizeSearchItem) : []
  }));
}

export async function runResearchSearch(
  {
    flow,
    target_date,
    subject,
    queries = []
  },
  {
    fetchImpl
  } = {}
) {
  const contract = buildResearchSearchRuntimeContract();
  const queryCount = Array.isArray(queries) ? queries.length : 0;

  if (contract.status !== "ready") {
    return {
      ...contract,
      query_count: queryCount,
      result_count: 0,
      searches: []
    };
  }

  const endpoint = getResearchSearchEndpoint();
  const apiKey = getResearchSearchApiKey();
  const timeoutMs = getResearchSearchTimeoutMs();
  const effectiveFetch = fetchImpl ?? fetch;

  try {
    const response = await effectiveFetch(endpoint, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
        "x-kungfu-platform": getPlatformHeader()
      },
      body: JSON.stringify({
        flow,
        target_date,
        subject,
        queries
      }),
      signal: AbortSignal.timeout(timeoutMs)
    });

    const text = await response.text();
    const parsed = tryParseJson(text);

    if (!response.ok) {
      const detail =
        typeof parsed === "string"
          ? parsed
          : parsed?.detail || parsed?.message || JSON.stringify(parsed);

      return {
        ...contract,
        status: "provider_error",
        reason: "search_runtime_request_failed",
        query_count: queryCount,
        result_count: 0,
        searches: [],
        error: {
          status: response.status,
          message: detail
        }
      };
    }

    const searches = normalizeSearchResponse(parsed);
    const resultCount = searches.reduce((sum, item) => sum + item.result_count, 0);

    return {
      ...contract,
      status: "completed",
      reason: null,
      query_count: queryCount,
      result_count: resultCount,
      searches
    };
  } catch (error) {
    const reason =
      error?.name === "TimeoutError"
        ? "search_runtime_timeout"
        : "search_runtime_request_failed";

    return {
      ...contract,
      status: "provider_error",
      reason,
      query_count: queryCount,
      result_count: 0,
      searches: [],
      error: {
        message: error?.message || "search runtime request failed"
      }
    };
  }
}
