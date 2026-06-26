import { readFileSync, existsSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";
import { parse } from "yaml";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = join(__dirname, "..", "..");

export function skillRoot() {
  return SKILL_ROOT;
}

/**
 * Load recipe yaml from path, or return defaults if missing / parse error.
 */
export function loadRecipe(fileName, defaults) {
  const path = join(SKILL_ROOT, "recipes", fileName);
  if (!existsSync(path)) return { ...defaults };
  const raw = readFileSync(path, "utf8");
  try {
    return { ...defaults, ...parse(raw) };
  } catch {
    return { ...defaults };
  }
}
