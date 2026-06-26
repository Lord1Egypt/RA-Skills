import { collectDayContext } from "./collect-day-context.js";
import { mergeSources } from "./merge-sources.js";
import { extractSignals } from "./extract-signals.js";
import { generateBrief } from "./generate-brief.js";
import { filterFocusedLines } from "./filter-focused-lines.js";
import { extractFocusTerms } from "./extract-focus-terms.js";

export async function runDailyBrief({ date, title, focusTitle = null, prompt = "", briefMode = "hybrid", memoryFile = null, focusTerms = [], lcm = null }) {
  const sources = await collectDayContext({ date, briefMode, memoryFile, lcm });

  if (briefMode === "lossless-only" && !lcm?.enabled) {
    throw new Error("Mindkeeper lossless-only mode requires --use-lcm.");
  }

  if (sources.length === 0) {
    throw new Error("Mindkeeper needs at least one source: --memory-file or --use-lcm.");
  }

  const merged = mergeSources(sources);
  const baseLines = merged.lines;
  const resolvedFocusTerms = extractFocusTerms({ explicitTerms: focusTerms, title: focusTitle ?? title, prompt });
  const focusedLines = filterFocusedLines(baseLines, resolvedFocusTerms);
  const workingLines = focusedLines.length > 0 ? focusedLines : baseLines;
  const signals = extractSignals(workingLines, { briefMode });

  return {
    brief: generateBrief({ date, title, signals }),
    diagnostics: {
      briefMode,
      sources: merged.sources,
      lineCount: baseLines.length,
      focusedLineCount: focusedLines.length,
      signalCount: signals.sourceLineCount,
      focusTerms: resolvedFocusTerms,
      usedFallbackFocus: resolvedFocusTerms.length > 0 && focusedLines.length === 0,
    },
  };
}
