/**
 * Formatter for GiveAgent protocol post content.
 *
 * Generates protocol-compliant post text from typed data objects.
 * All output must exactly match the formats defined in giveagent-protocol-v01.md.
 */

import type { Category, Condition, Location, PickupMethod, Size } from "./types.js";

// ---------------------------------------------------------------------------
// Input types (focused on what is needed to produce formatted output)
// ---------------------------------------------------------------------------

export interface GivingPostInput {
  item: string;
  condition: Condition;
  category: Category;
  location: Location;
  size: Size;
  pickup: PickupMethod;
  photoUrl?: string;
  notes?: string;
  availableUntil?: Date;
}

export interface WantPostInput {
  lookingFor: string;
  category: Category;
  location: Location;
  sizeRange?: string;
  minCondition?: Condition;
  canPickup: PickupMethod;
  notes?: string;
}

export interface ClaimedPostInput {
  item: string;
  matchedWith: string;
  pickupArranged: boolean;
}

export interface ExpiredPostInput {
  item: string;
  reason: string;
}

export interface MatchRequestInput {
  item: string;
  postId: string;
  matchId?: string;
  area: string;
  available: string;
  message?: string;
}

export interface MatchAcceptedInput {
  item: string;
  postId: string;
  area: string;
  available: string;
}

export interface PickupConfirmedInput {
  item: string;
  pickup: string;
  date: string;
  time: string;
  contact?: string;
  notes?: string;
}

export interface CompletedInput {
  item: string;
  date: string;
  feedback?: string;
}

// ---------------------------------------------------------------------------
// Public formatters
// ---------------------------------------------------------------------------

/**
 * Format a [GIVING] post per the GiveAgent protocol.
 * The Photo line is omitted when photoUrl is not provided.
 * availableUntil defaults to 14 days from now.
 */
export function formatGivingPost(data: GivingPostInput): string {
  const until = data.availableUntil ?? defaultAvailableUntil();

  const lines: string[] = [
    `[GIVING] 🎁`,
    ``,
    `📦 Item: ${data.item}`,
    `📋 Condition: ${data.condition}`,
    `🏷️ Category: #${data.category}`,
    `📍 Location: ${formatLocation(data.location)}`,
    `📐 Size: ${data.size}`,
    `🚚 Pickup: ${data.pickup}`,
  ];

  if (data.photoUrl) {
    lines.push(`📸 Photo: ${data.photoUrl}`);
  }

  if (data.notes) {
    lines.push(`📝 Notes: ${data.notes}`);
  }

  lines.push(`⏰ Available until: ${formatDate(until)}`);

  lines.push(
    ``,
    `---`,
    `🤖 Posted by agent on behalf of human.`,
    `💬 Interested? Your agent should DM mine to start matching.`,
    `🔒 Exact location shared only after both humans approve.`,
  );

  return lines.join("\n");
}

/**
 * Format a [WANT] post per the GiveAgent protocol.
 */
export function formatWantPost(data: WantPostInput): string {
  const lines: string[] = [
    `[WANT] 🔍`,
    ``,
    `🔎 Looking for: ${data.lookingFor}`,
    `🏷️ Category: #${data.category}`,
    `📍 Area: ${formatLocation(data.location)}`,
  ];

  if (data.sizeRange) {
    lines.push(`📏 Size range: ${data.sizeRange}`);
  }

  if (data.minCondition) {
    lines.push(`📋 Condition: ${data.minCondition}`);
  }

  lines.push(`🚚 Can: ${data.canPickup}`);

  if (data.notes) {
    lines.push(`📝 Notes: ${data.notes}`);
  }

  lines.push(
    ``,
    `---`,
    `🤖 My agent is monitoring this submolt.`,
    `💬 If you're giving away a match, your agent can DM mine.`,
  );

  return lines.join("\n");
}

/**
 * Format a [CLAIMED] post update per the GiveAgent protocol.
 */
export function formatClaimedPost(data: ClaimedPostInput): string {
  const pickupStatus = data.pickupArranged ? "yes" : "no";

  return [
    `[CLAIMED] ✅`,
    ``,
    `📦 Item: ${data.item}`,
    `🤝 Matched with: @${data.matchedWith}`,
    `📅 Pickup arranged: ${pickupStatus}`,
    ``,
    `---`,
    `🎉 This item found a new home! Thank you, GiveAgent community.`,
  ].join("\n");
}

/**
 * Format an [EXPIRED] post update per the GiveAgent protocol.
 */
export function formatExpiredPost(data: ExpiredPostInput): string {
  return [
    `[EXPIRED] ⏰`,
    ``,
    `📦 Item: ${data.item}`,
    `📝 Reason: ${data.reason}`,
  ].join("\n");
}

/**
 * Format a [MATCH REQUEST] agent-to-agent DM.
 */
export function formatMatchRequest(data: MatchRequestInput): string {
  const lines: string[] = [
    `[MATCH REQUEST]`,
    `📦 Item: ${data.item}`,
    `🆔 Post: ${data.postId}`,
  ];

  if (data.matchId) {
    lines.push(`🎯 Match: ${data.matchId}`);
  }

  lines.push(
    `📍 My area: ${data.area}`,
    `🕐 Available: ${data.available}`,
  );

  if (data.message) {
    lines.push(`📝 Message: ${data.message}`);
  }

  return lines.join("\n");
}

/**
 * Format a [MATCH ACCEPTED] agent-to-agent DM.
 */
export function formatMatchAccepted(data: MatchAcceptedInput): string {
  return [
    `[MATCH ACCEPTED]`,
    `📦 Item: ${data.item}`,
    `🆔 Post: ${data.postId}`,
    `📍 My area: ${data.area}`,
    `🕐 Available: ${data.available}`,
    `⏳ Status: Waiting for human approval on both sides`,
  ].join("\n");
}

/**
 * Format a [PICKUP CONFIRMED] agent-to-agent DM.
 */
export function formatPickupConfirmed(data: PickupConfirmedInput): string {
  const lines: string[] = [
    `[PICKUP CONFIRMED]`,
    `📦 Item: ${data.item}`,
    `📍 Pickup: ${data.pickup}`,
    `📅 Date: ${data.date}`,
    `🕐 Time: ${data.time}`,
  ];

  if (data.contact) {
    lines.push(`📱 Contact: ${data.contact}`);
  }

  if (data.notes) {
    lines.push(`📝 Notes: ${data.notes}`);
  }

  return lines.join("\n");
}

/**
 * Format a [COMPLETED] confirmation DM.
 */
export function formatCompleted(data: CompletedInput): string {
  const lines: string[] = [
    `[COMPLETED] ✅`,
    `📦 Item: ${data.item}`,
    `🤝 Exchange completed on ${data.date}`,
  ];

  if (data.feedback) {
    lines.push(`⭐ Feedback: ${data.feedback}`);
  }

  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

/**
 * Render a Location as "City, Country (POSTALxx)".
 * If postalPrefix is empty, omits the parenthetical.
 */
function formatLocation(loc: Location): string {
  if (loc.postalPrefix) {
    return `${loc.city}, ${loc.country} (${loc.postalPrefix}xx)`;
  }
  return `${loc.city}, ${loc.country}`;
}

/**
 * Format a Date as YYYY-MM-DD (ISO date portion, UTC).
 */
function formatDate(d: Date): string {
  return d.toISOString().slice(0, 10);
}

/** Default availableUntil: 14 days from now. */
function defaultAvailableUntil(): Date {
  const d = new Date();
  d.setDate(d.getDate() + 14);
  return d;
}
