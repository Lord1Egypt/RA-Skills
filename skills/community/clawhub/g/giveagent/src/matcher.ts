import type { WantListItem, GivingPost, WantPost, InventoryItem, MatchResult } from "./types.js";

/**
 * Common English stop words to filter out from keyword extraction.
 */
const STOP_WORDS = new Set([
  "a", "an", "the", "is", "for", "to", "of", "in", "on", "and", "or",
  "with", "my", "i", "me", "at", "by", "from", "as", "it", "be"
]);

/**
 * Extract keywords from a query string.
 * Lowercases, removes stop words, returns unique tokens.
 */
export function extractKeywords(query: string): string[] {
  if (!query || query.trim() === "") {
    return [];
  }

  const tokens = query
    .toLowerCase()
    .split(/\s+/)
    .map(token => token.trim())
    .filter(token => token.length > 0)
    .filter(token => !STOP_WORDS.has(token));

  // Return unique keywords
  return Array.from(new Set(tokens));
}

/**
 * Score a single want item against a single giving post.
 *
 * Scoring algorithm:
 * - Category match: +3 points
 * - Each keyword match in item name: +2 points
 * - Each keyword match in notes: +1 point
 * - City match: +2 points (REQUIRED — no match without same city)
 * - Threshold: 4+ points to qualify
 */
export function scoreMatch(
  want: WantListItem,
  giving: GivingPost
): { score: number; matchedOn: string[] } | null {
  // Must have keywords to match on
  if (want.keywords.length === 0) {
    return null;
  }

  let score = 0;
  const matchedOn: string[] = [];

  // Category match: +3 points
  if (want.category && want.category === giving.category) {
    score += 3;
    matchedOn.push(`category:${giving.category}`);
  }

  // Keyword matching in item name
  const itemNameLower = giving.item.toLowerCase();
  for (const keyword of want.keywords) {
    if (itemNameLower.includes(keyword)) {
      score += 2;
      matchedOn.push(`item:${keyword}`);
    }
  }

  // Keyword matching in notes (if present)
  if (giving.notes) {
    const notesLower = giving.notes.toLowerCase();
    for (const keyword of want.keywords) {
      if (notesLower.includes(keyword) && !itemNameLower.includes(keyword)) {
        // Only count if not already matched in item name
        score += 1;
        matchedOn.push(`notes:${keyword}`);
      }
    }
  }

  // City matching: +2 points (REQUIRED — must match to qualify)
  const wantCity = want.location?.city?.toLowerCase() || "";
  const givingCity = giving.location?.city?.toLowerCase() || "";

  if (!wantCity || !givingCity || wantCity !== givingCity) {
    return null;
  }
  score += 2;
  matchedOn.push(`city:${giving.location.city}`);

  // Threshold check: must have 4+ points
  if (score < 4) {
    return null;
  }

  return { score, matchedOn };
}

/**
 * Find matches between want list items and giving posts.
 *
 * Scoring algorithm (Phase 1):
 * - Category match: +3 points
 * - Each keyword match in item name: +2 points
 * - Each keyword match in notes: +1 point
 * - City match: +2 points (REQUIRED — no match without same city)
 * - Threshold: 4+ points to qualify
 *
 * Returns matches sorted by score descending.
 */
export function findMatches(
  wants: WantListItem[],
  givings: GivingPost[]
): MatchResult[] {
  const matches: MatchResult[] = [];

  for (const want of wants) {
    // Skip inactive wants
    if (want.status !== "active") {
      continue;
    }

    for (const giving of givings) {
      const result = scoreMatch(want, giving);

      if (result !== null) {
        matches.push({
          wantItem: want,
          givingPost: giving,
          score: result.score,
          matchedOn: result.matchedOn,
        });
      }
    }
  }

  // Sort by score descending
  matches.sort((a, b) => b.score - a.score);

  return matches;
}

/**
 * Reverse match: find want posts that match inventory items.
 * Used when scanning [WANT] posts against our giving inventory.
 */
export function findReverseMatches(
  inventory: InventoryItem[],
  wantPosts: WantPost[]
): MatchResult[] {
  const matches: MatchResult[] = [];

  for (const item of inventory) {
    // Skip inactive inventory
    if (item.status !== "active") {
      continue;
    }

    // Create a synthetic WantListItem from the WantPost
    for (const wantPost of wantPosts) {
      // Create synthetic WantListItem from WantPost
      const syntheticWant: WantListItem = {
        id: wantPost.postId || `want-${Date.now()}`,
        query: wantPost.lookingFor,
        keywords: extractKeywords(wantPost.lookingFor),
        category: wantPost.category,
        location: wantPost.location,
        added: wantPost.createdAt || new Date(),
        status: "active",
        priority: "medium",
      };

      // Create synthetic GivingPost from InventoryItem
      const syntheticGiving: GivingPost = {
        postType: "GIVING",
        item: item.item,
        condition: "Good", // Default condition
        category: item.category,
        location: wantPost.location, // Use want post location for matching
        size: "Medium", // Default size
        pickup: "Pickup Only", // Default pickup
        availableUntil: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days
        postId: item.postId,
      };

      const result = scoreMatch(syntheticWant, syntheticGiving);

      if (result !== null) {
        matches.push({
          wantItem: syntheticWant,
          givingPost: syntheticGiving,
          score: result.score,
          matchedOn: result.matchedOn,
        });
      }
    }
  }

  // Sort by score descending
  matches.sort((a, b) => b.score - a.score);

  return matches;
}
