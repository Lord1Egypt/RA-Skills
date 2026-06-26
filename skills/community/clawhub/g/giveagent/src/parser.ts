/**
 * Parser for GiveAgent protocol post content.
 *
 * Converts raw GiveAgent post text into typed structs.
 * Designed to be lenient: handles emoji variants, extra whitespace, and
 * missing optional fields gracefully.
 */

import type {
  ParsedPost,
  GivingPost,
  WantPost,
  Category,
  Condition,
  Location,
  PickupMethod,
  Size,
} from "./types.js";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const VALID_CATEGORIES: Category[] = [
  "furniture", "electronics", "clothing", "books",
  "kitchen", "kids", "sports", "home",
  "garden", "office", "media", "other",
];

const VALID_CONDITIONS: Condition[] = [
  "New", "Like New", "Good", "Fair", "For Parts",
];

const VALID_SIZES: Size[] = [
  "Pocket", "Small", "Medium", "Large", "XL", "Furniture-sized",
];

const VALID_PICKUP_METHODS: PickupMethod[] = [
  "Pickup Only", "Can Ship Locally", "Flexible",
];

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Detect post type from raw content and delegate to the appropriate parser.
 * Returns null if the post type cannot be determined.
 */
export function parsePost(raw: string): ParsedPost | null {
  if (!raw || typeof raw !== "string") return null;

  const firstLine = raw.split("\n")[0]?.trim() ?? "";

  if (/\[GIVING\]/i.test(firstLine)) return parseGivingPost(raw);
  if (/\[WANT\]/i.test(firstLine)) return parseWantPost(raw);

  // CLAIMED / EXPIRED return minimal typed stubs (no full round-trip needed)
  if (/\[CLAIMED\]/i.test(firstLine)) return parseClaimedPost(raw);
  if (/\[EXPIRED\]/i.test(firstLine)) return parseExpiredPost(raw);

  return null;
}

/**
 * Parse a [GIVING] post into a GivingPost struct.
 * Returns null if required fields (item, condition, category, location) are missing.
 */
export function parseGivingPost(content: string): GivingPost | null {
  const item = extractField(content, "Item");
  const conditionRaw = extractField(content, "Condition");
  const categoryRaw = extractField(content, "Category");
  const locationRaw = extractField(content, "Location");
  const sizeRaw = extractField(content, "Size");
  const pickupRaw = extractField(content, "Pickup");
  const photoUrl = extractField(content, "Photo") ?? undefined;
  const notes = extractField(content, "Notes") ?? undefined;
  const availableUntilRaw = extractField(content, "Available until");

  if (!item || !conditionRaw || !categoryRaw || !locationRaw) return null;

  const condition = parseCondition(conditionRaw);
  const category = parseCategory(categoryRaw);
  const location = parseLocation(locationRaw);

  if (!condition || !category || !location) return null;

  const size = sizeRaw ? (parseSize(sizeRaw) ?? ("Medium" as Size)) : ("Medium" as Size);
  const pickup = pickupRaw
    ? (parsePickupMethod(pickupRaw) ?? ("Pickup Only" as PickupMethod))
    : ("Pickup Only" as PickupMethod);

  const availableUntil = availableUntilRaw
    ? (parseDate(availableUntilRaw) ?? defaultAvailableUntil())
    : defaultAvailableUntil();

  return {
    postType: "GIVING",
    item,
    condition,
    category,
    location,
    size,
    pickup,
    photoUrl: photoUrl || undefined,
    notes: notes || undefined,
    availableUntil,
  };
}

/**
 * Parse a [WANT] post into a WantPost struct.
 * Returns null if required fields (lookingFor, category, location) are missing.
 */
export function parseWantPost(content: string): WantPost | null {
  const lookingFor = extractField(content, "Looking for");
  const categoryRaw = extractField(content, "Category");
  const locationRaw = extractField(content, "Area");
  const sizeRange = extractField(content, "Size range") ?? undefined;
  const minConditionRaw = extractField(content, "Condition");
  const canPickupRaw = extractField(content, "Can");
  const notes = extractField(content, "Notes") ?? undefined;

  if (!lookingFor || !categoryRaw || !locationRaw) return null;

  const category = parseCategory(categoryRaw);
  const location = parseLocation(locationRaw);

  if (!category || !location) return null;

  const minCondition = minConditionRaw
    ? (parseCondition(minConditionRaw) ?? undefined)
    : undefined;

  const canPickup = canPickupRaw
    ? (parsePickupMethod(canPickupRaw) ?? ("Pickup Only" as PickupMethod))
    : ("Pickup Only" as PickupMethod);

  return {
    postType: "WANT",
    lookingFor,
    category,
    location,
    sizeRange: sizeRange || undefined,
    minCondition,
    canPickup,
    notes: notes || undefined,
  };
}

/**
 * Extract the value for a named field from structured post content.
 *
 * Matches lines that start with an optional emoji, optional whitespace,
 * then the field name (case-insensitive), then a colon.
 * Returns the trimmed value after the colon, or null if not found.
 */
export function extractField(content: string, fieldName: string): string | null {
  const lines = content.split("\n");

  // Escape special regex characters in the field name
  const escaped = fieldName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  // Match: optional emoji chars, optional spaces, field name, colon, value
  // We allow any Unicode in prefix position (emoji, variation selectors, spaces)
  const pattern = new RegExp(
    `^[\\s\\p{Emoji}\\p{Emoji_Presentation}\\uFE0F\\uFE0E]*${escaped}\\s*:\\s*(.+)$`,
    "iu"
  );

  for (const line of lines) {
    const trimmed = line.trim();
    const match = trimmed.match(pattern);
    if (match) {
      return match[1]!.trim();
    }
  }
  return null;
}

/**
 * Parse a raw category string (with or without # prefix) into a Category enum value.
 * Case-insensitive.
 */
export function parseCategory(raw: string): Category | null {
  const cleaned = raw.replace(/^#/, "").trim().toLowerCase();
  const found = VALID_CATEGORIES.find((c) => c.toLowerCase() === cleaned);
  return found ?? null;
}

/**
 * Parse a raw condition string into a Condition enum value.
 * Case-insensitive; normalises "like new" → "Like New" etc.
 */
export function parseCondition(raw: string): Condition | null {
  const cleaned = raw.trim();
  const found = VALID_CONDITIONS.find(
    (c) => c.toLowerCase() === cleaned.toLowerCase()
  );
  return found ?? null;
}

/**
 * Parse a date string into a Date object.
 * Supports ISO format (YYYY-MM-DD) and common human-readable formats.
 * Returns null if the string cannot be parsed into a valid date.
 */
export function parseDate(raw: string): Date | null {
  if (!raw || !raw.trim()) return null;

  const cleaned = raw.trim();

  // ISO format: YYYY-MM-DD (most precise, try first)
  const isoMatch = cleaned.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (isoMatch) {
    const d = new Date(`${cleaned}T00:00:00.000Z`);
    return isNaN(d.getTime()) ? null : d;
  }

  // Common formats: MM/DD/YYYY, DD/MM/YYYY, Month DD YYYY
  const d = new Date(cleaned);
  if (!isNaN(d.getTime())) return d;

  return null;
}

/**
 * Return true if the giving post's availableUntil date is in the past.
 */
export function isExpired(post: GivingPost): boolean {
  return post.availableUntil.getTime() < Date.now();
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function parseClaimedPost(content: string): import("./types.js").ClaimedPost | null {
  const item = extractField(content, "Item");
  if (!item) return null;

  const matchedWith = extractField(content, "Matched with") ?? "unknown";
  const pickupRaw = extractField(content, "Pickup arranged") ?? "";
  const pickupArranged = /yes/i.test(pickupRaw);

  return {
    postType: "CLAIMED",
    item,
    matchedWith,
    pickupArranged,
    originalPostId: "",
  };
}

function parseExpiredPost(content: string): import("./types.js").ExpiredPost | null {
  const item = extractField(content, "Item");
  if (!item) return null;

  const reasonRaw = extractField(content, "Reason") ?? "";
  const reason = parseExpiredReason(reasonRaw);

  return {
    postType: "EXPIRED",
    item,
    reason,
    originalPostId: "",
  };
}

function parseExpiredReason(
  raw: string
): "withdrawn by owner" | "deadline passed" | "item discarded" {
  const lower = raw.toLowerCase();
  if (lower.includes("withdrawn")) return "withdrawn by owner";
  if (lower.includes("deadline") || lower.includes("passed")) return "deadline passed";
  return "item discarded";
}

/**
 * Parse a location string in the format "City, Country (XXXxx)" into a Location object.
 * Examples:
 *   "Taipei, Taiwan (106xx)"     → { city: "Taipei", country: "Taiwan", postalPrefix: "106" }
 *   "San Francisco, USA (941xx)" → { city: "San Francisco", country: "USA", postalPrefix: "941" }
 */
function parseLocation(raw: string): Location | null {
  if (!raw || !raw.trim()) return null;

  const cleaned = raw.trim();

  // Match "City, Country (POSTALxx)" — the postal prefix ends before "xx"
  const withPostal = cleaned.match(/^(.+?),\s*(.+?)\s*\(([A-Za-z0-9]+?)x+\)\s*$/);
  if (withPostal) {
    return {
      city: withPostal[1]!.trim(),
      country: withPostal[2]!.trim(),
      postalPrefix: withPostal[3]!.trim(),
    };
  }

  // Fallback: "City, Country" without postal code
  const withoutPostal = cleaned.match(/^(.+?),\s*(.+)$/);
  if (withoutPostal) {
    return {
      city: withoutPostal[1]!.trim(),
      country: withoutPostal[2]!.trim(),
      postalPrefix: "",
    };
  }

  return null;
}

function parseSize(raw: string): Size | null {
  const cleaned = raw.trim();
  const found = VALID_SIZES.find(
    (s) => s.toLowerCase() === cleaned.toLowerCase()
  );
  return found ?? null;
}

function parsePickupMethod(raw: string): PickupMethod | null {
  const cleaned = raw.trim();
  const found = VALID_PICKUP_METHODS.find(
    (p) => p.toLowerCase() === cleaned.toLowerCase()
  );
  return found ?? null;
}

function defaultAvailableUntil(): Date {
  const d = new Date();
  d.setDate(d.getDate() + 14);
  return d;
}
