/**
 * RTK Exec Compression — Domain-Aware Output Truncation
 * =====================================================
 *
 * Pure string-processing truncation for OpenClaw exec tool output.
 * Zero external dependencies. Fail-safe on any error → returns raw output.
 *
 * ## Wire-in (if OpenClaw core were modifiable)
 * Applied in buildExecForegroundResult() — after outcome.aggregated is
 * populated, before it is wrapped into the tool result:
 *   outcome.aggregated = truncateExecOutput(command, outcome.aggregated);
 *
 * ## Phase Roadmap
 *   Phase 1 ✓  Domain-aware head+tail truncation (this file)
 *   Phase 2    Command-aware filter registry with fail-safe fallback
 *   Phase 3    Config flag + oversized-output logging
 */

// ─── Constants ────────────────────────────────────────────────────────────────

const DIFF_HEAD_LINES = 100;
const DIFF_TAIL_LINES = 20;
const DIFF_TOTAL_THRESHOLD = 120;
const GREP_MAX_MATCHES = 50;
const LS_MAX_ENTRIES = 100;
const BUILD_FOCUS_THRESHOLD = 200;

// ─── Fail-Safe Wrapper ───────────────────────────────────────────────────────

/**
 * Wraps any truncation function with panic recovery.
 * On ANY error (TypeError, RangeError, regex crash) returns raw output.
 */
export function truncateWithFailSafe(
  fn: () => string,
  raw: string
): string {
  try {
    return fn();
  } catch (err) {
    console.error("[exec-truncate] truncation error, returning raw:", err);
    return raw;
  }
}

// ─── git diff ────────────────────────────────────────────────────────────────

/**
 * Truncates `git diff` output: first 100 + last 20 lines.
 * Strips headers, hunk markers, unchanged context.
 * Keeps only additions (`+`). Returns unchanged if < 120 lines.
 */
export function truncateGitDiff(output: string): string {
  return truncateWithFailSafe(() => {
    const lines = output.split("\n");
    if (lines.length <= DIFF_TOTAL_THRESHOLD) return output;

    const head = lines.slice(0, DIFF_HEAD_LINES);
    const tail = lines.slice(-DIFF_TAIL_LINES);
    const middleCount = lines.length - DIFF_HEAD_LINES - DIFF_TAIL_LINES;

    const kept: string[] = [];
    let additions = 0;
    const totalAdditions = lines.filter(l => l.startsWith("+") && !l.startsWith("+++")).length;

    for (const line of head) {
      if (line.startsWith("+") && !line.startsWith("+++")) { kept.push(line); additions++; }
      else if (kept.length === 0 && (line.startsWith("diff --git") || line.startsWith("--- "))) {
        kept.push(line);
      }
    }

    for (const line of tail) {
      if (line.startsWith("+") && !line.startsWith("+++")) { kept.push(line); additions++; }
    }

    if (middleCount > 0) {
      kept.push(`\n[... ${middleCount} lines truncated, ${totalAdditions} total additions ...]`);
    } else if (kept.length === 0 || (kept.length === 1 && kept[0]!.startsWith("diff --git"))) {
      return `[diff: ${lines.length} lines, ${totalAdditions} additions — no additions in head/tail window]`;
    }

    return kept.join("\n");
  }, output);
}

// ─── git log ────────────────────────────────────────────────────────────────

/**
 * Truncates `git log` to condensed one-liners.
 * Strips: ASCII graph, full hashes, timestamps.
 * Keeps: short hash (7 chars), subject, branches, error/fail tags.
 * Max 50 entries.
 */
export function truncateGitLog(output: string): string {
  return truncateWithFailSafe(() => {
    const lines = output.split("\n");
    const result: string[] = [];

    for (const raw of lines) {
      if (result.length >= 50) break;

      // Strip leading graph characters
      const stripped = raw.replace(/^[*|/\\ ]+/, "").trim();
      if (!stripped) continue;

      const hasError = /\b(error|fail|fatal)\b/i.test(stripped);
      const hashMatch = stripped.match(/^([a-f0-9]{7})\s+(.*)$/i);

      if (hashMatch) {
        const [, hash, rest] = hashMatch;
        const branchMatch = rest.match(/^(.*?)\s*\(([^)]+)\)\s*$/);
        const branches = branchMatch ? ` (${branchMatch[2]})` : "";
        const subject = branchMatch ? branchMatch[1] : rest;
        result.push(`${hash} ${subject.trim()}${branches}${hasError ? " ⚠" : ""}`);
      } else if (hasError) {
        result.push(`⚠ ${stripped}`);
      }
    }

    return result.join("\n") || output;
  }, output);
}

// ─── grep / rg / find ───────────────────────────────────────────────────────

/**
 * Truncates `grep`, `rg`, `find` output.
 * Caps at 50 matches, strips absolute-path prefixes,
 * adds `[... N more matches]` if truncated.
 */
export function truncateGrepOutput(output: string, maxMatches = GREP_MAX_MATCHES): string {
  return truncateWithFailSafe(() => {
    const allLines = output.split("\n").filter((l) => l.trim());
    if (allLines.length <= maxMatches) return stripWorkingDirPrefix(allLines.join("\n"));

    const kept = allLines.slice(0, maxMatches);
    const truncated = allLines.length - maxMatches;
    return stripWorkingDirPrefix(kept.join("\n")) + `\n[... ${truncated} more matches ...]`;
  }, output);
}

/** Lazily cached cwd regex */
let cachedCwdRegex: RegExp | null = null;
let cachedCwd = "";

/** Strips cwd and home directory prefixes from paths */
function stripWorkingDirPrefix(text: string): string {
  if (cachedCwd !== process.cwd()) {
    const cwd = process.cwd().replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    cachedCwdRegex = new RegExp(cwd + "/", "g");
    cachedCwd = process.cwd();
  }
  const home = process.env.HOME ?? "";
  return text
    .replace(cachedCwdRegex!, "")
    .replace(new RegExp("^" + home.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "/", "g"), "");
}

// ─── ls -la / ls -l ─────────────────────────────────────────────────────────

/**
 * Truncates `ls -la` / `ls -l` output.
 * Max 100 entries, strips permissions/owner/timestamps,
 * keeps filename + abbreviated size (1.2K, 3.4M).
 */
export function truncateLsOutput(output: string): string {
  return truncateWithFailSafe(() => {
    const lines = output.split("\n");
    const totalLine = lines.find((l) => l.startsWith("total "));
    const otherLines = lines.filter((l) => !l.startsWith("total ") && l.trim());

    const result: string[] = totalLine ? [totalLine] : [];

    if (otherLines.length <= LS_MAX_ENTRIES) {
      for (const line of otherLines) result.push(formatLsLine(line));
    } else {
      for (let i = 0; i < LS_MAX_ENTRIES; i++) result.push(formatLsLine(otherLines[i]));
      result.push(`[... ${otherLines.length - LS_MAX_ENTRIES} more entries ...]`);
    }

    return result.join("\n");
  }, output);
}

/** Parses one ls -l line → "size  filename". Preserves error lines. */
function formatLsLine(line: string): string {
  if (line.includes("No such file") || line.includes("Permission denied") || line.includes("cannot access")) {
    return line;
  }
  const m = line.match(/^[dl-][rwxsStT-]{9}\s+\d+\s+\S+\s+\S+\s+(\d+)\s+\w+\s+\d+\s+[\d:]+\s+(.+)$/);
  if (m) return `${abbreviateSize(parseInt(m[1], 10))}  ${m[2]}`;
  const parts = line.trim().split(/\s+/);
  const name = parts[parts.length - 1] ?? "";
  const sizeField = parts.length > 4 ? parts[4] : "";
  return `${/^\d+$/.test(sizeField) ? abbreviateSize(parseInt(sizeField, 10)) : sizeField}  ${name}`;
}

/** Abbreviates bytes → 1.2K / 1.2M / 1.2G */
function abbreviateSize(bytes: number): string {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 ** 2) return `${(bytes / 1024).toFixed(1)}K`;
  if (bytes < 1024 ** 3) return `${(bytes / 1024 ** 2).toFixed(1)}M`;
  return `${(bytes / 1024 ** 3).toFixed(1)}G`;
}

// ─── Build Output ────────────────────────────────────────────────────────────

/**
 * Truncates build tool output (cargo, npm, go, ruff, tsc, gcc, cmake, make).
 *
 * Strip: ANSI codes, progress bars, "Compiling X", "Downloading N bytes".
 * Keep: `error:` and `warning:` lines.
 * If no errors/warnings: brief `[build OK — N warnings]`.
 * If > 200 lines: focus on first error or last 50 relevant lines.
 */
export function truncateBuildOutput(output: string): string {
  return truncateWithFailSafe(() => {
    const text = stripAnsiCodes(output);
    const lines = text.split("\n");
    const builder = detectBuilder(text);
    const cleaned = stripBuilderNoise(lines, builder);
    const relevant = cleaned.filter(isRelevantBuildLine);

    const errorCount = relevant.filter((l) => l.toLowerCase().includes("error")).length;
    const warnCount = relevant.filter((l) => l.toLowerCase().includes("warning")).length;

    if (relevant.length === 0) {
      return `[build OK — ${lines.length} lines output]`;
    }

    if (lines.length > BUILD_FOCUS_THRESHOLD) {
      const firstErrorIdx = relevant.findIndex((l) => l.toLowerCase().includes("error"));
      if (firstErrorIdx !== -1) return relevant.slice(firstErrorIdx, firstErrorIdx + 50).join("\n");
      return relevant.slice(-50).join("\n");
    }

    const hasErrors = relevant.some((l) => l.toLowerCase().includes("error"));
    const summary = hasErrors
      ? `[build FAILED — ${errorCount} error${errorCount !== 1 ? "s" : ""}, ${warnCount} warning${warnCount !== 1 ? "s" : ""}]`
      : `[build OK — ${warnCount} warning${warnCount !== 1 ? "s" : ""}]`;

    if (lines.length > BUILD_FOCUS_THRESHOLD) {
      const firstErrorIdx = relevant.findIndex((l) => l.toLowerCase().includes("error"));
      const focused = firstErrorIdx !== -1
        ? relevant.slice(firstErrorIdx, firstErrorIdx + 50)
        : relevant.slice(-50);
      return [...focused, summary].join("\n");
    }

    // For non-large builds: cap at 50 + append summary (no duplication)
    return [...relevant.slice(0, 50), summary].join("\n");
  }, output);
  }, output);
}

/** Strips ANSI escape sequences */
function stripAnsiCodes(text: string): string {
  // eslint-disable-next-line no-control-regex
  return text
    .replace(/\x1b\[[0-9;]*[a-zA-Z]/g, "")
    .replace(/\x1b\][^\x07]*\x07/g, "")
    .replace(/\x1b[()][AB012]/g, "");
}

/** Detects which build tool produced the output */
function detectBuilder(output: string): string {
  if (output.includes("cargo") || output.includes("Compiling")) return "cargo";
  if (output.includes("npm ") || output.includes("node_modules")) return "npm";
  if (output.includes("go build") || output.includes("go: ")) return "go";
  if (output.includes("ruff")) return "ruff";
  if (output.includes("tsc") || output.includes("TypeScript")) return "tsc";
  if (output.includes("gcc") || output.includes("cc ")) return "gcc";
  if (output.includes("cmake") || output.includes("CMake")) return "cmake";
  if (output.includes("make") || output.includes("Makefile")) return "make";
  return "generic";
}

/** Returns true for error/warning lines that should be preserved */
function isRelevantBuildLine(line: string): boolean {
  const l = line.toLowerCase();
  return l.includes("error") || l.includes("warning") || l.includes("failed");
}

/** Strips common build-tool noise lines */
function stripBuilderNoise(lines: string[], _builder?: string): string[] {
  return lines.filter((line) => {
    const t = line.trim();
    if (!t) return false;
    const noiseRe = /^(Downloading|Finished|Compiling|Building|Installing|Bundling)\s+|^\s*[|\\/—→]+$|^[\s.✓✅✔ done]+$|^(\d+%)([\s|][\s█░▓]+)?$|^warning: deprecated/i;
    return !noiseRe.test(t);
  });
}

// ─── Main Dispatcher ────────────────────────────────────────────────────────

/**
 * Routes command + output to the appropriate truncation handler.
 * Unknown commands → raw output unchanged (fail-safe default).
 */
export function truncateExecOutput(command: string, output: string): string {
  const cmd = command.trim();

  if (/^git diff/i.test(cmd)) return truncateGitDiff(output);
  if (/^git log/i.test(cmd)) return truncateGitLog(output);
  if (/^(grep|rg |find\b)/i.test(cmd)) {
    return truncateGrepOutput(output);
  }
  if (/ls\s+(-la|-l|)/i.test(cmd) || /^ls\s/i.test(cmd)) {
    return truncateLsOutput(output);
  }

  const buildPattern = /^(cargo|npm\s+run|go\s+build|ruff|tsc|gcc|cmake|make)/i;
  if (buildPattern.test(cmd)) return truncateBuildOutput(output);

  return output; // Unknown → pass through unchanged
}
