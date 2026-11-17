/**
 * Value-level redaction.
 *
 * GA4 is not supposed to contain personal data, but in practice it does: a
 * checkout page path carries an order token, a password-reset link carries an
 * email, a badly built site puts a user id in the URL. Those values arrive in
 * dimension values like `pagePath` and `landingPagePlusQueryString`.
 *
 * Everything here is a pure function over strings so the guarantees in
 * PRIVACY.md are testable without a network or a credential.
 */

/** Query parameters whose values survive redaction because they carry no identity. */
export const DEFAULT_KEPT_QUERY_PARAMS: readonly string[] = [
  "utm_source",
  "utm_medium",
  "utm_campaign",
  "utm_term",
  "utm_content",
  "utm_id",
  "page",
  "q",
  "query",
  "search",
  "sort",
  "category",
  "lang",
  "locale",
  "ref",
  "source",
];

/** GA4 emits these as literal dimension values; they are never personal data. */
const GA4_SENTINELS = new Set([
  "(not set)",
  "(other)",
  "(none)",
  "(direct)",
  "(no data)",
  "(not provided)",
]);

export type RedactionOptions = {
  /** When false, values pass through untouched. */
  enabled: boolean;
  /** Query parameter names whose values are preserved. */
  keepQueryParams: readonly string[];
  /** Additional caller-supplied patterns, masked as `[redacted:custom]`. */
  extraPatterns: readonly RegExp[];
};

export type RedactionResult = {
  value: string;
  /** Number of substitutions made, so a tool can report "n values redacted". */
  redactions: number;
};

/**
 * Ordered so that broader, more structured patterns win over narrower ones:
 * a JWT must be recognised before its base64 segments look like bare tokens.
 */
const VALUE_PATTERNS: ReadonlyArray<{ label: string; pattern: RegExp }> = [
  {
    label: "jwt",
    pattern: /\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b/g,
  },
  {
    label: "email",
    // Also matches percent-encoded "@" (%40), which is how emails usually
    // survive a trip through a URL and into GA4.
    pattern: /\b[A-Za-z0-9._%+-]+(?:@|%40|%2540)[A-Za-z0-9.\-%]+\.[A-Za-z]{2,}\b/gi,
  },
  {
    label: "uuid",
    pattern: /\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b/gi,
  },
  {
    label: "phone",
    pattern: /(?:\+[1-9]\d{7,14}\b|\(\d{3}\)\s?\d{3}-\d{4}\b)/g,
  },
  {
    label: "token",
    // Long opaque strings: hex digests, session ids, API keys. Requires both a
    // digit and a letter so ordinary slugs and words are not caught.
    pattern: /\b(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Za-z])[A-Za-z0-9_-]{32,}\b/g,
  },
];

/** Card-like digit runs, confirmed with Luhn so product ids are not masked. */
const CARD_CANDIDATE = /\b(?:\d[ -]?){12,18}\d\b/g;
const PRIVATE_KEY_BLOCK = /-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----/g;
const BEARER_TOKEN = /(Bearer\s+)[A-Za-z0-9._~+/=-]{8,}/gi;
const JSON_SECRET_FIELD =
  /("(?:access_token|refresh_token|id_token|private_key|client_secret|api_key|apiKey)"\s*:\s*")[^"]*(")/gi;

function luhnValid(digits: string): boolean {
  let sum = 0;
  let double = false;
  for (let index = digits.length - 1; index >= 0; index--) {
    let digit = digits.charCodeAt(index) - 48;
    if (double) {
      digit *= 2;
      if (digit > 9) {
        digit -= 9;
      }
    }
    sum += digit;
    double = !double;
  }
  return sum % 10 === 0;
}

/**
 * Replace the values of query parameters that are not explicitly kept.
 *
 * Operates on the raw string rather than `new URL()` because GA4 dimension
 * values are frequently relative paths, and because round-tripping through
 * `URL` re-encodes characters and changes values the user recognises.
 */
function redactQueryString(
  value: string,
  keep: readonly string[],
): { value: string; redactions: number } {
  // A fragment carries key=value pairs just as often as a query string does
  // (OAuth implicit-flow tokens land there), so both delimiters are treated the
  // same way.
  const separator = firstIndexOfAny(value, ["?", "#"]);
  if (separator === -1) {
    return { value, redactions: 0 };
  }
  const kept = new Set(keep.map((name) => name.toLowerCase()));
  const head = value.slice(0, separator + 1);
  const tail = value.slice(separator + 1);
  // A fragment after a query string is handled as its own pair list.
  const hash = tail.indexOf("#");
  const query = hash === -1 ? tail : tail.slice(0, hash);
  const fragment = hash === -1 ? "" : tail.slice(hash);

  let redactions = 0;
  const rebuilt = query
    .split("&")
    .map((pair) => {
      if (!pair) {
        return pair;
      }
      const equals = pair.indexOf("=");
      if (equals === -1) {
        return pair;
      }
      const name = pair.slice(0, equals);
      const paramValue = pair.slice(equals + 1);
      if (kept.has(name.toLowerCase()) || paramValue === "" || paramValue === REDACTED) {
        return pair;
      }
      redactions++;
      return `${name}=${REDACTED}`;
    })
    .join("&");

  const fragmentResult = fragment ? redactQueryString(fragment, keep) : { value: "", redactions: 0 };
  return {
    value: `${head}${rebuilt}${fragmentResult.value}`,
    redactions: redactions + fragmentResult.redactions,
  };
}

const REDACTED = "[redacted]";

function firstIndexOfAny(value: string, needles: readonly string[]): number {
  let best = -1;
  for (const needle of needles) {
    const at = value.indexOf(needle);
    if (at !== -1 && (best === -1 || at < best)) {
      best = at;
    }
  }
  return best;
}

/**
 * Redact a single GA4 dimension value.
 *
 * Idempotent: running it over an already-redacted value is a no-op, which
 * matters because tools re-render cached rows.
 */
export function redactValue(value: string, options: RedactionOptions): RedactionResult {
  if (!options.enabled || value === "" || GA4_SENTINELS.has(value)) {
    return { value, redactions: 0 };
  }

  const query = redactQueryString(value, options.keepQueryParams);
  let result = query.value;
  let redactions = query.redactions;

  for (const { label, pattern } of VALUE_PATTERNS) {
    result = result.replace(new RegExp(pattern.source, pattern.flags), (match) => {
      redactions++;
      return `[redacted:${label}]`;
    });
  }

  result = result.replace(new RegExp(CARD_CANDIDATE.source, CARD_CANDIDATE.flags), (match) => {
    const digits = match.replace(/[ -]/g, "");
    if (!luhnValid(digits)) {
      return match;
    }
    redactions++;
    return "[redacted:card]";
  });

  for (const pattern of options.extraPatterns) {
    const flags = pattern.flags.includes("g") ? pattern.flags : `${pattern.flags}g`;
    result = result.replace(new RegExp(pattern.source, flags), () => {
      redactions++;
      return "[redacted:custom]";
    });
  }

  return { value: result, redactions };
}

/**
 * Redact credentials out of free text before it reaches a log, an error
 * message, or a tool result. Applied unconditionally; this one is not
 * configurable, because there is no legitimate reason to surface a key.
 */
export function redactText(text: string): string {
  return text
    .replace(PRIVATE_KEY_BLOCK, "[redacted:private-key]")
    .replace(JSON_SECRET_FIELD, `$1${REDACTED}$2`)
    .replace(BEARER_TOKEN, `$1${REDACTED}`);
}
