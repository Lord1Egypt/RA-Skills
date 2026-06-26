/**
 * Content sanitization utilities.
 *
 * Cleans external post content before storage, display, or matching.
 * Guards against prompt injection, PII leaks, and malformed input.
 */

const MAX_POST_LENGTH = 5000;

/**
 * Patterns for known field prefixes used in structured posts.
 * The regex anchors to start-of-line and captures everything after the prefix.
 */
const FIELD_PREFIXES = [
  "📦 Item:",
  "📋 Condition:",
  "🏷️ Category:",
  "📍 Location:",
  "📐 Size:",
  "🚚 Pickup:",
  "📝 Notes:",
  "⏰ Available until:",
  "🔎 Looking for:",
  "📏 Size range:",
];

/**
 * Prompt injection phrases to strip (case-insensitive).
 * Ordered longest-first so partial matches don't fire before full matches.
 */
const INJECTION_PATTERNS = [
  /ignore\s+(all\s+)?previous\s+instructions?/gi,
  /disregard\s+(all\s+)?previous\s+instructions?/gi,
  /forget\s+(all\s+)?previous\s+instructions?/gi,
  /you\s+are\s+now\s+(a\s+)?(?:an?\s+)?\w+/gi,
  /act\s+as\s+(?:a\s+|an\s+)?\w+/gi,
  /do\s+not\s+follow\s+(?:your\s+)?(?:previous\s+)?instructions?/gi,
  /new\s+instructions?:/gi,
  /system\s+prompt:/gi,
  /\[INST\]/gi,
  /<\|im_start\|>/gi,
  /<\|im_end\|>/gi,
];

/**
 * Markdown injection patterns — links and images that could exfiltrate data
 * or render malicious content.
 */
const MARKDOWN_INJECTION = [
  /!\[.*?\]\(.*?\)/g,   // images: ![alt](url)
  /\[.*?\]\(.*?\)/g,   // links:  [text](url)
];

/**
 * Zero-width and invisible Unicode characters used for homoglyph attacks.
 */
const ZERO_WIDTH_CHARS = /[\u200B-\u200F\uFEFF\u00AD\u2028\u2029]/g;

/**
 * Control characters (except \n \r \t which are legitimate whitespace).
 */
const CONTROL_CHARS = /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g;

/**
 * Strip control characters, markdown injection, embedded instructions from post content.
 * Used before storing or displaying any external content.
 */
export function sanitizePostContent(raw: string): string {
  let out = raw;

  // Remove zero-width and invisible Unicode characters
  out = out.replace(ZERO_WIDTH_CHARS, "");

  // Remove control characters (preserve \n, \r, \t)
  out = out.replace(CONTROL_CHARS, "");

  // Strip markdown image and link injection
  for (const pattern of MARKDOWN_INJECTION) {
    out = out.replace(pattern, "");
  }

  // Strip prompt injection phrases
  for (const pattern of INJECTION_PATTERNS) {
    out = out.replace(pattern, "");
  }

  // Enforce maximum length
  if (out.length > MAX_POST_LENGTH) {
    out = out.slice(0, MAX_POST_LENGTH);
  }

  return out;
}

/**
 * Extract only structured fields from content for safe matching.
 * Strips everything that isn't a recognized field line.
 */
export function sanitizeForMatching(raw: string): string {
  const lines = raw.split("\n");
  const kept: string[] = [];

  for (const line of lines) {
    const trimmed = line.trim();
    const isField = FIELD_PREFIXES.some((prefix) => trimmed.startsWith(prefix));
    if (isField) {
      kept.push(stripEmoji(trimmed));
    }
  }

  return kept.join("\n");
}

// ---------------------------------------------------------------------------
// Address / PII detection
// ---------------------------------------------------------------------------

/**
 * Western street address patterns.
 * Matches "123 Main Street", "45 Oak Ave", "1600 Pennsylvania Avenue".
 */
const WESTERN_STREET =
  /\b\d{1,5}\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3}\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Place|Pl|Terrace|Ter|Highway|Hwy)\b/i;

/**
 * East Asian address patterns commonly used in Taiwan / Hong Kong / China.
 * Matches "No. 45, Sec. 2, Zhongshan Rd", "No 12 Section 3" etc.
 */
const EAST_ASIAN_STREET =
  /\bNo\.?\s*\d+(?:,\s*(?:Sec(?:tion)?\.?|Lane|Alley)\.?\s*\d+)*\s*,\s*[A-Z][a-zA-Z\s]+(?:Road|Rd|Street|St|Avenue|Ave)\b/i;

/**
 * GPS coordinate pair — decimal degrees with enough precision to locate someone.
 * Requires at least 3 decimal places to avoid matching normal numbers.
 */
const GPS_COORDINATES =
  /[-+]?\d{1,3}\.\d{3,}\s*,\s*[-+]?\d{1,3}\.\d{3,}/;

/**
 * Phone numbers in international and local formats.
 * Covers: +886-2-1234-5678, (02) 1234-5678, +1 (555) 123-4567, etc.
 */
const PHONE_NUMBER =
  /(?:\+\d{1,3}[\s.-]?)?(?:\(?\d{1,4}\)?[\s.-]?){1,3}\d{3,4}[\s.-]?\d{4}/;

/**
 * Apartment / unit / building references.
 */
const APARTMENT =
  /\b(?:Apt|Apartment|Unit|Flat|Room|Rm|Floor|Fl|Building|Bldg|Suite|Ste)\.?\s*#?\d+[A-Za-z]?\b/i;

/**
 * Detect street addresses, GPS coordinates, phone numbers in text.
 * Returns true if any PII/location leak is found.
 */
export function containsAddressLeak(text: string): boolean {
  if (GPS_COORDINATES.test(text)) return true;
  if (PHONE_NUMBER.test(text)) return true;
  if (WESTERN_STREET.test(text)) return true;
  if (EAST_ASIAN_STREET.test(text)) return true;
  if (APARTMENT.test(text)) return true;
  return false;
}

// ---------------------------------------------------------------------------
// Emoji stripping
// ---------------------------------------------------------------------------

/**
 * Remove emoji from text for clean keyword extraction.
 * Uses Unicode property escapes (ES2018+) for reliable emoji matching.
 */
export function stripEmoji(text: string): string {
  return text
    .replace(/\p{Emoji_Presentation}/gu, "")
    .replace(/\p{Emoji}\uFE0F/gu, "")
    .replace(/[\u200D\uFE0F]/gu, "")
    .replace(/\s{2,}/g, " ")
    .trim();
}
