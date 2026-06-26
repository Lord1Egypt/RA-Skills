import { clip, unique } from "../utils/text.js";

const DECISION_RE = /\b(decid|accepted|approved|final|preferred|merged|chosen|numele final|recomandarea mea)\b/i;
const OPEN_LOOP_RE = /\b(open loop|rămas|ramas|pending|blocked|follow-up|follow up|de făcut|de facut|todo|later|următorul pas|next step|needs|lipsește|lipseste)\b/i;
const RECOMMEND_RE = /\b(recommendation|recommend|recomand|merită|merita|next step|mâine|maine)\b/i;
const PRODUCT_SIGNAL_RE = /\b(mindkeeper|lossless|lcm|memory|repo|branch|cron|email|brief|summary|clarity|signal|owner|product|skill|readme|brand|prompt-to-pr|nexlink|release|merge)\b/i;
const HOUSEKEEPING_RE = /(let me|hai să|hai sa|vezi:|see:|starting task|adjacent:|diagnostics:|context budget|full session log|todo\.md|tasks\/todo\.md|tests\/|diff-ul|diff stat|verify|planific|what feature vrei|ce feature vrei|îți trimit|iti trimit|dacă vrei|daca vrei|ai dreptate|confirmă-mi|confirma-mi|retrimit|trimis|mail de transport|email de test|pot — dar|pot - dar|^perfect\.|^bun[,!.]?|^gata[,!.]?|^corect[,!.]?|^da[,!.]?|first real send|progress brief for|corrected real memory brief)/i;
const NOISE_PATTERNS = [
  /^(sender\b|session key|session id|source|conversation summary)/i,
  /^\{\s*$/,
  /^\}\s*$/,
  /^```/,
  /^"?(label|id|schema|provider|surface|chat_type|channel)"?\s*:/i,
  /^context:\s*\d/i,
  /^diagnostics:/i,
  /^tap version /i,
  /^# subtest:/i,
  /^(ok|not ok)\s+\d+\s+-/i,
  /^command exited with code/i,
  /^\[FAZA .*CONTEXT:/i,
  /^\|.*\|$/,
  /^\d+\.\s+\*\*/,
  /^\[\d+\]/,
];

function isMeaningful(line) {
  if (line.length < 12) return false;
  if (/:$/.test(line.trim()) && line.length < 80) return false;
  return !NOISE_PATTERNS.some((pattern) => pattern.test(line));
}

function isQuestion(line) {
  return /\?$/.test(line.trim());
}

function scoreLine(line) {
  let score = 0;

  if (PRODUCT_SIGNAL_RE.test(line)) score += 4;
  if (DECISION_RE.test(line)) score += 3;
  if (OPEN_LOOP_RE.test(line)) score += 2;
  if (RECOMMEND_RE.test(line)) score += 2;
  if (/\b(implement|build|use|keep|separate|final product name|convention)\b/i.test(line)) score += 1;
  if (HOUSEKEEPING_RE.test(line)) score -= 4;
  if (isQuestion(line)) score -= 2;

  return score;
}

function rankLines(lines) {
  return [...lines].sort((left, right) => scoreLine(right) - scoreLine(left));
}

function isUsefulHighlight(line) {
  return !HOUSEKEEPING_RE.test(line) && !isQuestion(line) && scoreLine(line) > 0;
}

export function extractSignals(lines, { briefMode = "hybrid" } = {}) {
  const meaningful = lines.filter(isMeaningful);
  const limits = briefMode === "lossless-only"
    ? { highlights: 3, decisions: 2, openLoops: 3, recommendations: 3 }
    : { highlights: 5, decisions: 5, openLoops: 5, recommendations: 4 };

  const decisions = rankLines(unique(meaningful.filter((line) => DECISION_RE.test(line) && !HOUSEKEEPING_RE.test(line))));
  const openLoops = rankLines(unique(meaningful.filter((line) => OPEN_LOOP_RE.test(line) && !HOUSEKEEPING_RE.test(line))));
  const recommendations = rankLines(unique(meaningful.filter((line) => RECOMMEND_RE.test(line) && !HOUSEKEEPING_RE.test(line))));

  const reserved = new Set([...decisions, ...openLoops, ...recommendations]);
  const highlights = clip(
    rankLines(meaningful.filter((line) => !reserved.has(line) && isUsefulHighlight(line))),
    limits.highlights,
  );

  return {
    highlights,
    decisions: clip(decisions, limits.decisions),
    openLoops: clip(openLoops, limits.openLoops),
    recommendations: clip(recommendations, limits.recommendations),
    sourceLineCount: meaningful.length,
  };
}
