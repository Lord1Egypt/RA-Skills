import type { MemoryRecord, RecordKind } from './types';

export interface ClassifyResult {
  id: string;
  kind: RecordKind;
  confidence: number;
}

// [keyword, weight] pairs. Weights reflect signal strength.
type WeightedEntry = [string, number];

const FACT_KEYWORDS: WeightedEntry[] = [
  ['observed', 2.0],
  ['confirmed', 2.0],
  ['verified', 2.0],
  ['verify', 1.5],
  ['proved', 2.0],
  ['demonstrated', 1.5],
  ['documented', 1.5],
  ['recorded', 1.5],
  ['measured', 1.5],
  ['detected', 1.5],
  ['established', 1.5],
  ['concluded', 1.5],
  ['determined', 1.5],
  ['tested', 1.5],
  ['achieved', 1.5],
  ['showed', 1.5],
  ['found', 1.0],
  ['noted', 1.0],
  ['reported', 1.0],
  ['identified', 1.0],
  ['stated', 1.0],
  ['known', 1.0],
];

const GOAL_KEYWORDS: WeightedEntry[] = [
  ['intend', 2.0],
  ['intends', 2.0],
  ['intending', 2.0],
  ['must', 2.0],
  ['shall', 2.0],
  ['ought', 2.0],
  ['aspire', 2.0],
  ['aspires', 2.0],
  ['aim', 1.5],
  ['aims', 1.5],
  ['goal', 1.5],
  ['objective', 1.5],
  ['plan', 1.5],
  ['plans', 1.5],
  ['planning', 1.5],
  ['propose', 1.5],
  ['proposes', 1.5],
  ['will', 1.5],
  ['should', 1.5],
  ['need', 1.0],
  ['needs', 1.0],
  ['target', 1.0],
  ['want', 1.0],
  ['wants', 1.0],
];

const SPECULATION_KEYWORDS: WeightedEntry[] = [
  ['might', 2.0],
  ['possibly', 2.0],
  ['perhaps', 2.0],
  ['uncertain', 2.0],
  ['unclear', 2.0],
  ['unsure', 2.0],
  ['speculate', 2.0],
  ['speculates', 2.0],
  ['speculated', 2.0],
  ['hypothesize', 2.0],
  ['hypothesizes', 2.0],
  ['unlikely', 2.0],
  ['probably', 2.0],
  ['suspect', 2.0],
  ['suspects', 2.0],
  ['likely', 1.5],
  ['assume', 1.5],
  ['assumes', 1.5],
  ['assuming', 1.5],
  ['estimate', 1.5],
  ['estimates', 1.5],
  ['seem', 1.5],
  ['seems', 1.5],
  ['allegedly', 1.5],
  ['supposedly', 1.5],
  ['may', 1.5],
  ['could', 1.0],
  ['appears', 1.0],
];

// Immediately preceding one of these suppresses a goal keyword hit.
const PAST_AUX = new Set(['was', 'were', 'had', 'has', 'have', 'been', 'did', 'got', 'is']);
const NEGATION = new Set(['not', 'never', 'no', 'neither', 'nor']);

const MIN_THRESHOLD = 0.05;

function tokenize(content: string): string[] {
  return content
    .toLowerCase()
    .split(/\s+/)
    .map(t => t.replace(/[^a-z0-9]/g, ''))
    .filter(t => t.length > 0);
}

// Returns true when a goal keyword at `index` should have its hit suppressed.
// Guard fires when:
//   - the preceding token is a past-tense auxiliary ("was goal") OR a negation ("not will")
//   - the following token is a past-tense auxiliary ("goal was"), indicating nominal/historical use
function isSuppressed(tokens: string[], index: number): boolean {
  const prev = index > 0 ? tokens[index - 1] : null;
  const next = index < tokens.length - 1 ? tokens[index + 1] : null;
  if (prev !== null && (PAST_AUX.has(prev) || NEGATION.has(prev))) return true;
  if (next !== null && PAST_AUX.has(next)) return true;
  return false;
}

function scoreTokens(
  tokens: string[],
  keywords: ReadonlyMap<string, number>,
  guard: boolean,
): number {
  let total = 0;
  for (let i = 0; i < tokens.length; i++) {
    const w = keywords.get(tokens[i]);
    if (w !== undefined) {
      if (!guard || !isSuppressed(tokens, i)) {
        total += w;
      }
    }
  }
  return total;
}

const FACT_MAP: ReadonlyMap<string, number> = new Map(FACT_KEYWORDS);
const GOAL_MAP: ReadonlyMap<string, number> = new Map(GOAL_KEYWORDS);
const SPEC_MAP: ReadonlyMap<string, number> = new Map(SPECULATION_KEYWORDS);

export function classifyRecords(records: MemoryRecord[]): ClassifyResult[] {
  return records.map(record => {
    const { content } = record;

    if (content.trim().length === 0) {
      return { id: record.id, kind: 'fact', confidence: 0 };
    }

    const tokens = tokenize(content);
    if (tokens.length === 0) {
      return { id: record.id, kind: 'fact', confidence: 0 };
    }

    const n = tokens.length;
    const factScore = scoreTokens(tokens, FACT_MAP, false) / n;
    const goalScore = scoreTokens(tokens, GOAL_MAP, true) / n;
    const specScore = scoreTokens(tokens, SPEC_MAP, false) / n;

    const maxScore = Math.max(factScore, goalScore, specScore);

    if (maxScore < MIN_THRESHOLD) {
      return { id: record.id, kind: 'fact', confidence: 0 };
    }

    let kind: RecordKind;
    if (goalScore >= factScore && goalScore >= specScore) {
      kind = 'goal';
    } else if (specScore >= factScore) {
      kind = 'speculation';
    } else {
      kind = 'fact';
    }

    const totalScore = factScore + goalScore + specScore;
    // maxScore <= totalScore always, so ratio is in [0, 1]
    const confidence = totalScore > 0 ? maxScore / totalScore : 0;

    return { id: record.id, kind, confidence };
  });
}
