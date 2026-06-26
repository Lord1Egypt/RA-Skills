import { readFile } from "node:fs/promises";
import { toLines } from "../utils/text.js";

export async function readDailyMemoryFile(path) {
  const content = await readFile(path, "utf8");
  return {
    source: "daily-memory-file",
    path,
    content,
    lines: toLines(content),
  };
}
