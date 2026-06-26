import type { ActionItem } from './types.js';

const TRACKING_PARAM_PREFIXES = ['utm_'];

export function normalizeUrl(url: string): string {
  let u = url.trim();
  if (!u) return '';

  u = u.toLowerCase();
  u = u.replace(/^https?:\/\//, '');

  try {
    u = decodeURIComponent(u);
  } catch { /* malformed encoding — keep as-is */ }

  u = u.replace(/([^:])\/{2,}/g, '$1/');

  const qIndex = u.indexOf('?');
  let base = qIndex === -1 ? u : u.slice(0, qIndex);
  const queryString = qIndex === -1 ? '' : u.slice(qIndex + 1);

  base = base.replace(/\/+$/, '');

  let filteredQuery = '';
  if (queryString) {
    const params = queryString.split('&').filter((param) => {
      const key = param.split('=')[0];
      return !TRACKING_PARAM_PREFIXES.some((prefix) => key.startsWith(prefix));
    });
    filteredQuery = params.join('&');
  }

  return filteredQuery ? `${base}?${filteredQuery}` : base;
}

function extractDomainAndPath(normalized: string): string {
  const qIndex = normalized.indexOf('?');
  return qIndex === -1 ? normalized : normalized.slice(0, qIndex);
}

/**
 * Return a 0-to-1 confidence score for URL matching between two action items.
 * Exact normalized match -> 1.0
 * Same domain+path but different query -> 0.7
 * Either has no URL -> 0.0
 * Different domains -> 0.0
 */
export function matchByUrl(a: ActionItem, b: ActionItem): number {
  if (!a.url || !b.url) return 0.0;

  const normA = normalizeUrl(a.url);
  const normB = normalizeUrl(b.url);

  if (!normA || !normB) return 0.0;

  if (normA === normB) return 1.0;

  const dpA = extractDomainAndPath(normA);
  const dpB = extractDomainAndPath(normB);

  if (dpA === dpB) return 0.7;

  return 0.0;
}

export function bigrams(s: string): string[] {
  const result: string[] = [];
  for (let i = 0; i < s.length - 1; i++) {
    result.push(s.slice(i, i + 2));
  }
  return result;
}

export function diceCoefficient(a: string[], b: string[]): number {
  if (a.length === 0 || b.length === 0) return 0.0;

  const setB = [...b];
  let intersections = 0;

  for (const bg of a) {
    const idx = setB.indexOf(bg);
    if (idx !== -1) {
      intersections++;
      setB.splice(idx, 1);
    }
  }

  return (2 * intersections) / (a.length + b.length);
}

export function normalizeTitleText(title: string): string {
  return title.trim().replace(/\s+/g, ' ').toLowerCase();
}

/**
 * Return a 0-to-1 confidence score for title matching between two action items.
 * Exact match after normalization -> 1.0
 * Partial overlap -> Dice coefficient
 * Either title empty/null -> 0.0
 * Non-exact match when either title has fewer than 3 bigrams -> 0.0
 */
export function matchByTitle(a: ActionItem, b: ActionItem): number {
  const titleA = a.title;
  const titleB = b.title;

  if (!titleA || !titleB) return 0.0;

  const normA = normalizeTitleText(titleA);
  const normB = normalizeTitleText(titleB);

  if (!normA || !normB) return 0.0;

  if (normA === normB) return 1.0;

  // Cap at 0.0 for non-exact matches when either title has fewer than 3 bigrams
  const bigramsA = bigrams(normA);
  const bigramsB = bigrams(normB);
  if (bigramsA.length < 3 || bigramsB.length < 3) return 0.0;

  return diceCoefficient(bigramsA, bigramsB);
}

const ONE_HOUR_MS = 60 * 60 * 1000;
const SEVENTY_TWO_HOURS_MS = 72 * ONE_HOUR_MS;
const DECAY_RANGE_MS = SEVENTY_TWO_HOURS_MS - ONE_HOUR_MS;

/**
 * Return a 0-to-1 confidence score for timestamp proximity between two items.
 * Within 1 hour -> 1.0
 * Linear decay from 1.0 to 0.0 between 1 hour and 72 hours
 * Beyond 72 hours -> 0.0
 * Either has no createdAt -> 0.0
 */
export function matchByTimestamp(a: ActionItem, b: ActionItem): number {
  if (!a.createdAt || !b.createdAt) return 0.0;

  const timeA = new Date(a.createdAt).getTime();
  const timeB = new Date(b.createdAt).getTime();

  if (isNaN(timeA) || isNaN(timeB)) return 0.0;

  const diffMs = Math.abs(timeA - timeB);

  if (diffMs <= ONE_HOUR_MS) return 1.0;
  if (diffMs >= SEVENTY_TWO_HOURS_MS) return 0.0;

  return 1.0 - (diffMs - ONE_HOUR_MS) / DECAY_RANGE_MS;
}

// URL is the strongest dedup signal (unique per resource); title catches
// cross-source duplicates; timestamp is a weak tiebreaker to avoid merging
// items that happen to share a title but were created months apart.
export function computeConfidence(
  urlScore: number,
  titleScore: number,
  timestampScore: number,
): number {
  return 0.45 * urlScore + 0.35 * titleScore + 0.20 * timestampScore;
}

// Cross-source threshold is higher (0.85 vs 0.75) because different sources
// may legitimately have similar-looking items that are actually distinct.
export function shouldMerge(
  a: ActionItem,
  b: ActionItem,
  confidence: number,
): boolean {
  if (a.sourceType !== b.sourceType) {
    return confidence >= 0.85;
  }
  return confidence >= 0.75;
}

export interface MergeRef {
  source: string;
  id: string;
}

export interface DedupedItem extends ActionItem {
  mergedFrom?: MergeRef[];
}

export function mergeItems(primary: ActionItem, secondary: ActionItem, confidence: number): DedupedItem {
  const merged: DedupedItem = { ...primary };

  const nullableFields: Array<keyof ActionItem> = [
    'dueAt', 'blocker', 'replyDraft', 'followUpQuestion', 'suggestedNextAction',
  ];
  for (const key of nullableFields) {
    if (merged[key] === null && secondary[key] !== null) {
      (merged as any)[key] = secondary[key];
    }
  }

  merged.dedupeKeys = [...new Set([...primary.dedupeKeys, ...secondary.dedupeKeys])];
  merged.confidence = confidence;
  merged.mergedFrom = [{ source: secondary.source, id: secondary.id }];

  return merged;
}

// Greedy merge: highest-confidence pairs first, so ambiguous merges don't
// block high-confidence ones. O(n^2) is acceptable for typical inbox sizes.
export function deduplicateItems(items: readonly ActionItem[]): DedupedItem[] {
  if (items.length === 0) return [];
  if (items.length === 1) return [{ ...items[0] }];

  const sorted = [...items].sort((a, b) => a.id.localeCompare(b.id));

  interface MergePair {
    i: number;
    j: number;
    confidence: number;
    earliestCreatedAt: number;
  }

  const pairs: MergePair[] = [];

  for (let i = 0; i < sorted.length; i++) {
    for (let j = i + 1; j < sorted.length; j++) {
      const confidence = computeConfidence(
        matchByUrl(sorted[i], sorted[j]),
        matchByTitle(sorted[i], sorted[j]),
        matchByTimestamp(sorted[i], sorted[j]),
      );

      if (shouldMerge(sorted[i], sorted[j], confidence)) {
        const timeI = new Date(sorted[i].createdAt).getTime();
        const timeJ = new Date(sorted[j].createdAt).getTime();
        pairs.push({
          i,
          j,
          confidence,
          earliestCreatedAt: Math.min(timeI, timeJ),
        });
      }
    }
  }

  pairs.sort((a, b) => {
    if (b.confidence !== a.confidence) return b.confidence - a.confidence;
    if (a.earliestCreatedAt !== b.earliestCreatedAt) return a.earliestCreatedAt - b.earliestCreatedAt;
    const aKey = `${sorted[a.i].id},${sorted[a.j].id}`;
    const bKey = `${sorted[b.i].id},${sorted[b.j].id}`;
    return aKey.localeCompare(bKey);
  });

  const consumed = new Set<number>();
  const results: DedupedItem[] = [];

  for (const pair of pairs) {
    if (consumed.has(pair.i) || consumed.has(pair.j)) continue;

    const itemA = sorted[pair.i];
    const itemB = sorted[pair.j];

    const timeA = new Date(itemA.createdAt).getTime();
    const timeB = new Date(itemB.createdAt).getTime();

    const [primary, secondary] = timeA <= timeB ? [itemA, itemB] : [itemB, itemA];

    results.push(mergeItems(primary, secondary, pair.confidence));

    consumed.add(pair.i);
    consumed.add(pair.j);
  }

  for (let i = 0; i < sorted.length; i++) {
    if (!consumed.has(i)) {
      results.push({ ...sorted[i] });
    }
  }

  return results;
}
