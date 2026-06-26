const TRUE_VALUES = new Set(["1", "true", "yes", "y", "on"]);
const FALSE_VALUES = new Set(["0", "false", "no", "n", "off"]);
const API_BASE_URL = "https://tianshan-api.kungfu-trader.com";
const DEFAULT_PLATFORM = "openclaw";
const DEFAULT_MARKET_TIMEZONE = "Asia/Shanghai";

export function getEnv(name, { required = false, defaultValue = undefined } = {}) {
  const value = process.env[name];
  if (value === undefined || value === null || value === "") {
    if (required) {
      throw new Error(`Missing required environment variable: ${name}`);
    }
    return defaultValue;
  }
  return value;
}

export function getBaseUrl() {
  return API_BASE_URL;
}

export function getOpenKey() {
  const openkey = process.env.KUNGFU_OPENKEY?.trim();
  if (!openkey) {
    throw new Error("Missing required openkey: KUNGFU_OPENKEY");
  }
  return openkey;
}

export function getPlatformHeader() {
  return process.env.KUNGFU_PLATFORM?.trim() || DEFAULT_PLATFORM;
}

export function cleanObject(input) {
  return Object.fromEntries(
    Object.entries(input).filter(([, value]) => value !== undefined && value !== null && value !== "")
  );
}

export function toInteger(value) {
  if (value === undefined || value === null || value === "") {
    return undefined;
  }
  const parsed = Number.parseInt(String(value), 10);
  if (Number.isNaN(parsed)) {
    throw new Error(`Expected integer, got: ${value}`);
  }
  return parsed;
}

export function toBoolean(value) {
  if (value === undefined || value === null || value === "") {
    return undefined;
  }
  const normalized = String(value).trim().toLowerCase();
  if (TRUE_VALUES.has(normalized)) {
    return true;
  }
  if (FALSE_VALUES.has(normalized)) {
    return false;
  }
  throw new Error(`Expected boolean-like value, got: ${value}`);
}

export function buildDefaultHeaders(extraHeaders = {}) {
  return {
    Accept: "application/json",
    Authorization: `Bearer ${getOpenKey()}`,
    "x-kungfu-platform": getPlatformHeader(),
    ...extraHeaders
  };
}

function formatCompactDate(date, timeZone = DEFAULT_MARKET_TIMEZONE) {
  const formatter = new Intl.DateTimeFormat("en-US", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  });
  const parts = formatter.formatToParts(date);
  const partMap = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${partMap.year}${partMap.month}${partMap.day}`;
}

const DEFAULT_SEARCH_TIMEOUT_MS = 15000;
const SUPPORTED_SEARCH_PROVIDERS = new Set(["web_search"]);

export function getResearchSearchProvider() {
  const provider = process.env.KUNGFU_RESEARCH_SEARCH_PROVIDER?.trim();
  return provider || null;
}

export function isResearchSearchEnabled() {
  return process.env.KUNGFU_ENABLE_RESEARCH_SEARCH === "1";
}

export function getResearchSearchEndpoint() {
  const endpoint = process.env.KUNGFU_RESEARCH_SEARCH_ENDPOINT?.trim();
  return endpoint || null;
}

export function getResearchSearchApiKey() {
  const apiKey = process.env.KUNGFU_RESEARCH_SEARCH_API_KEY?.trim();
  return apiKey || null;
}

export function getResearchSearchTimeoutMs() {
  const raw = process.env.KUNGFU_RESEARCH_SEARCH_TIMEOUT_MS;
  if (!raw) return DEFAULT_SEARCH_TIMEOUT_MS;
  const parsed = Number.parseInt(String(raw), 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : DEFAULT_SEARCH_TIMEOUT_MS;
}

export function isSupportedSearchProvider(provider) {
  return SUPPORTED_SEARCH_PROVIDERS.has(provider);
}

export function getDefaultResearchTargetDate() {
  const override = process.env.KUNGFU_RESEARCH_DEFAULT_TARGET_DATE?.trim();
  if (override) {
    if (!/^\d{8}$/.test(override)) {
      throw new Error("KUNGFU_RESEARCH_DEFAULT_TARGET_DATE must use YYYYMMDD format.");
    }
    return override;
  }

  return formatCompactDate(new Date());
}
