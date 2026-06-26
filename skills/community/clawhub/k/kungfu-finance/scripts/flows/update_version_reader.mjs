// Reads the local skill version from package.json.
// This file ONLY reads a local file — no network, no secrets, no subprocesses.
import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

export function getLocalSkillVersion() {
  try {
    const selfDir = dirname(fileURLToPath(import.meta.url));
    const pkgPath = join(selfDir, "../../package.json");
    const pkg = JSON.parse(readFileSync(pkgPath, "utf-8"));
    return pkg.version || null;
  } catch {
    return null;
  }
}
