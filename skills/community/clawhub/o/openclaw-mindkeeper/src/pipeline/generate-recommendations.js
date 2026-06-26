import { unique } from "../utils/text.js";

const HOUSEKEEPING_RE = /\b(todo\.md|tasks\/todo\.md|tests\/|full session log|starting task|adjacent:|final user request|user complained|assistant acknowledged|next turn likely)\b/i;

function hasTheme(lines, pattern) {
  return lines.some((line) => pattern.test(line));
}

function fromSeeds(lines) {
  const recommendations = [];

  if (hasTheme(lines, /\b(remaining open loop|open loop|blocked|pending|needs|implement|unfinished|still needs|follow-up|follow up)\b/i)) {
    recommendations.push("Close the highest-value unfinished thread before it expands into more work tomorrow.");
  }

  if (hasTheme(lines, /\b(template|branding|brand|digest|email)\b/i)) {
    recommendations.push("Keep the template, branding, and copy consistent across the next sends.");
  }

  if (hasTheme(lines, /\b(lossless|lcm|memory)\b/i)) {
    recommendations.push("Keep refining the lossless collector until the brief reads like memory, not a transcript.");
  }

  if (hasTheme(lines, /\b(repo|branch|product layer|separate product|owner-facing product)\b/i)) {
    recommendations.push("Keep product logic separate from memory-engine internals as the implementation grows.");
  }

  if (hasTheme(lines, /\b(prompt-to-pr|release|merged|merge|rollout|transport)\b/i)) {
    recommendations.push("Review the recent shipped work and capture any follow-up cleanup while context is still fresh.");
  }

  return recommendations;
}

function sanitizeSeed(line) {
  const value = String(line ?? "").trim();
  if (!value) return null;
  if (HOUSEKEEPING_RE.test(value)) return null;
  return value;
}

export function generateRecommendations(signals) {
  const seeds = [
    ...signals.openLoops,
    ...signals.recommendations,
    ...signals.decisions,
    ...signals.highlights,
  ]
    .map(sanitizeSeed)
    .filter(Boolean);

  const recommendations = unique(fromSeeds(seeds)).slice(0, 3);

  if (recommendations.length > 0) {
    return recommendations;
  }

  if (signals.highlights.length > 0 || signals.decisions.length > 0) {
    return ["Review the day’s strongest signal and choose the next concrete move before the next run."];
  }

  return [];
}
