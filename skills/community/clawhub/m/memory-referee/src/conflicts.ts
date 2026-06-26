import type { MemoryRecord, ConflictPair } from './types.js';

const NEGATION_RE = /\b(not|never|no|false|incorrect|isn't|aren't|doesn't|don't)\b/gi;
const NUMBER_RE = /\b\d+(?:\.\d+)?\b/g;
const WORD_RE = /\b[a-zA-Z]{3,}\b/g;

/**
 * Normalise a subject string for grouping:
 * lowercase, collapse whitespace, strip leading/trailing punctuation.
 */
function normaliseSubject(subject: string): string {
  return subject
    .toLowerCase()
    .replace(/[-_]+/g, ' ')
    .replace(/\s+/g, ' ')
    .replace(/^[^a-z0-9]+|[^a-z0-9]+$/g, '')
    .trim();
}

/**
 * Tokenise content into an array of lowercase words (≥1 char).
 */
function tokenise(content: string): string[] {
  return content.toLowerCase().match(/\b[a-z']+\b/g) ?? [];
}

/**
 * Extract all numeric values (integers and decimals) from a string.
 */
function extractNumbers(content: string): number[] {
  return (content.match(NUMBER_RE) ?? []).map(Number);
}

/**
 * Extract lowercase nouns (words ≥3 letters, no stop words) from content.
 * We keep this simple — any word ≥3 letters that is not a stop word is a
 * candidate noun.  Caller decides which are "shared" by checking verbatim
 * presence in the other record.
 */
const STOP_WORDS = new Set([
  'the', 'and', 'for', 'are', 'was', 'were', 'has', 'have', 'had',
  'that', 'this', 'with', 'from', 'its', 'into', 'also', 'but',
  'not', 'nor', 'yet', 'via', 'per', 'she', 'her', 'him', 'his',
  'they', 'them', 'our', 'your', 'their', 'who', 'what', 'when',
  'how', 'why', 'been', 'being', 'does', 'did', 'will', 'can',
  'may', 'might', 'must', 'shall', 'should', 'would', 'could',
  'more', 'than', 'each', 'every', 'any', 'all', 'both', 'some',
  'such', 'then', 'only', 'just', 'even', 'over', 'under', 'very',
  'same', 'true', 'false', 'about', 'after', 'before', 'since',
  'while', 'where', 'which', 'there', 'here', 'other', 'another',
  "isn't", "aren't", "doesn't", "don't", 'never', 'incorrect',
]);

function extractCandidateNouns(content: string): string[] {
  const words = (content.toLowerCase().match(WORD_RE) ?? []);
  return [...new Set(words.filter(w => !STOP_WORDS.has(w)))];
}

/**
 * Check negation-proximity signal.
 *
 * Returns a reason string if: record `a` contains a negation token within 8
 * tokens of a noun that also appears verbatim in record `b`'s content, OR
 * vice-versa.  Returns null if the signal does not fire.
 *
 * "Within 8 tokens" means: scan the token array of the negating record; at
 * each negation token position, check whether any of the shared nouns appear
 * within 8 positions (before or after) in that same token array.
 */
function negationProximityReason(a: MemoryRecord, b: MemoryRecord): string | null {
  const tokensA = tokenise(a.content);
  const tokensB = tokenise(b.content);

  const nounsA = extractCandidateNouns(a.content);
  const nounsB = extractCandidateNouns(b.content);

  // Nouns present in BOTH records (verbatim match in other record's content).
  const sharedNouns = new Set([
    ...nounsA.filter(n => b.content.toLowerCase().includes(n)),
    ...nounsB.filter(n => a.content.toLowerCase().includes(n)),
  ]);

  if (sharedNouns.size === 0) return null;

  const WINDOW = 8;

  // Check whether `tokens` has a negation within WINDOW positions of a shared noun.
  function hasNegationNearSharedNoun(tokens: string[]): string | null {
    for (let i = 0; i < tokens.length; i++) {
      if (!NEGATION_RE.test(tokens[i])) continue;
      NEGATION_RE.lastIndex = 0; // reset stateful regex
      // Look within window around position i.
      const lo = Math.max(0, i - WINDOW);
      const hi = Math.min(tokens.length - 1, i + WINDOW);
      for (let j = lo; j <= hi; j++) {
        if (j !== i && sharedNouns.has(tokens[j])) {
          return tokens[j];
        }
      }
    }
    return null;
  }

  const hitA = hasNegationNearSharedNoun(tokensA);
  if (hitA !== null) {
    return `negation proximity: record A negates near shared noun "${hitA}"`;
  }
  const hitB = hasNegationNearSharedNoun(tokensB);
  if (hitB !== null) {
    return `negation proximity: record B negates near shared noun "${hitB}"`;
  }
  return null;
}

/**
 * Check numeric-divergence signal.
 *
 * Returns a reason string if both records assert exactly one numeric value
 * and those values differ by more than 10%.  Returns null otherwise.
 */
function numericDivergenceReason(a: MemoryRecord, b: MemoryRecord): string | null {
  const numsA = extractNumbers(a.content);
  const numsB = extractNumbers(b.content);

  if (numsA.length !== 1 || numsB.length !== 1) return null;

  const va = numsA[0];
  const vb = numsB[0];

  if (va === 0 && vb === 0) return null;

  const larger = Math.max(Math.abs(va), Math.abs(vb));
  const diff = Math.abs(va - vb);

  if (diff / larger > 0.1) {
    return `numeric divergence: record A asserts ${va}, record B asserts ${vb} (>${(diff / larger * 100).toFixed(0)}% apart)`;
  }
  return null;
}

/**
 * Detect contradictions between MemoryRecords sharing the same normalised subject.
 *
 * Groups records by normalised subject, then compares every ordered pair within
 * each group using two independent signals:
 *   1. Negation proximity — negation token within 8 tokens of a shared noun.
 *   2. Numeric divergence — both records assert exactly one number, >10% apart.
 *
 * Emits a ConflictPair for each pair where at least one signal fires.
 * Input records are not mutated.
 */
export function detectConflicts(records: MemoryRecord[]): ConflictPair[] {
  if (records.length === 0) return [];

  // Exclude records that have been explicitly resolved.
  const active = records.filter(
    r => r.resolution !== 'resolved' && r.resolvedAt === undefined,
  );

  // Group by normalised subject.
  const groups = new Map<string, MemoryRecord[]>();
  for (const record of active) {
    const key = normaliseSubject(record.entity);
    let bucket = groups.get(key);
    if (bucket === undefined) {
      bucket = [];
      groups.set(key, bucket);
    }
    bucket.push(record);
  }

  const conflicts: ConflictPair[] = [];

  for (const group of groups.values()) {
    if (group.length < 2) continue;

    for (let i = 0; i < group.length - 1; i++) {
      for (let j = i + 1; j < group.length; j++) {
        const a = group[i];
        const b = group[j];

        const reasons: string[] = [];

        const negReason = negationProximityReason(a, b);
        if (negReason !== null) reasons.push(negReason);

        const numReason = numericDivergenceReason(a, b);
        if (numReason !== null) reasons.push(numReason);

        if (reasons.length > 0) {
          conflicts.push({ a, b, reason: reasons.join('; ') });
        }
      }
    }
  }

  return conflicts;
}
