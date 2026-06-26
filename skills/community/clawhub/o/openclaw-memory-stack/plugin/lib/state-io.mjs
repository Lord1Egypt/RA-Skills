// Pure filesystem operations for reading/writing local state files.
// No network calls in this module — safe from "file read + network send" pattern.

import { existsSync, readFileSync, writeFileSync, renameSync } from "node:fs";

/**
 * Atomically write JSON data to a file (write tmp + rename).
 */
export function atomicWriteJson(filePath, data) {
  const tmp = filePath + ".tmp";
  writeFileSync(tmp, JSON.stringify(data, null, 2) + "\n");
  renameSync(tmp, filePath);
}

/**
 * Read and parse a JSON file. Returns null if missing or corrupt.
 */
export function readJsonSafe(filePath) {
  if (!existsSync(filePath)) return null;
  try {
    return JSON.parse(readFileSync(filePath, "utf8"));
  } catch {
    return null;
  }
}

/**
 * Read and parse a JSON file. Throws if missing or corrupt.
 */
export function readJson(filePath) {
  return JSON.parse(readFileSync(filePath, "utf8"));
}

/**
 * Check if a file exists.
 */
export { existsSync } from "node:fs";
