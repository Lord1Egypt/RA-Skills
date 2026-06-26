import { readDailyMemoryFile } from "../sources/daily-memory-file.js";
import { readLcmDayContext } from "../sources/lcm-source.js";
import { cleanLosslessLines } from "./clean-lossless-lines.js";

export async function collectDayContext({
  date,
  briefMode = "hybrid",
  memoryFile = null,
  lcm = null,
} = {}) {
  const sources = [];

  if (briefMode !== "lossless-only" && memoryFile) {
    sources.push(await readDailyMemoryFile(memoryFile));
  }

  if (lcm?.enabled) {
    const lcmSource = await readLcmDayContext({
      date,
      dbPath: lcm.dbPath,
      sessionKey: lcm.sessionKey,
      includeTools: lcm.includeTools,
      limit: lcm.limit,
      conversationLimit: lcm.conversationLimit,
      rawConversationLimit: lcm.rawConversationLimit,
      messageTail: lcm.messageTail,
      summaryLimit: lcm.summaryLimit,
      includeSummaries: lcm.includeSummaries,
    });

    sources.push({
      ...lcmSource,
      lines: cleanLosslessLines(lcmSource.lines),
    });
  }

  return sources;
}
