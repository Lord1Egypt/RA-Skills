import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = join(__dirname, "..", "..");

export function getDataDir() {
  return (process.env.NEWS_DIGEST_DATA_DIR ?? "").trim() || join(SKILL_ROOT, "data");
}

export function ensureDir(dirPath) {
  if (!existsSync(dirPath)) {
    mkdirSync(dirPath, { recursive: true });
  }
}

export function readJSON(filePath) {
  if (!existsSync(filePath)) return null;
  try {
    return JSON.parse(readFileSync(filePath, "utf-8"));
  } catch {
    return null;
  }
}

export function writeJSON(filePath, data) {
  ensureDir(dirname(filePath));
  writeFileSync(filePath, JSON.stringify(data, null, 2) + "\n", "utf-8");
}

export function todayStr() {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, "0");
  const d = String(now.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

export function nowISO() {
  return new Date().toISOString();
}

export function pushDir(date) {
  return join(getDataDir(), "pushes", date);
}

export function feedbackDir(date) {
  return join(getDataDir(), "feedback", date);
}

export function pushPath(date, slot) {
  return join(pushDir(date), `${slot}.json`);
}

export function feedbackPath(date, slot) {
  return join(feedbackDir(date), `${slot}.json`);
}

/**
 * List date directories under a given subdirectory of data (e.g. "pushes" or "feedback").
 * Returns sorted date strings descending (newest first).
 */
export function listDates(subDir) {
  const base = join(getDataDir(), subDir);
  if (!existsSync(base)) return [];
  return readdirSync(base, { withFileTypes: true })
    .filter((d) => d.isDirectory() && /^\d{4}-\d{2}-\d{2}$/.test(d.name))
    .map((d) => d.name)
    .sort()
    .reverse();
}

export function configPath() {
  return join(getDataDir(), "config.json");
}

export function loadConfig() {
  return readJSON(configPath());
}

export function saveConfig(config) {
  config.updated_at = nowISO();
  writeJSON(configPath(), config);
}

export function currentMonth() {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, "0");
  return `${y}-${m}`;
}

export function usagePath(yearMonth) {
  return join(getDataDir(), "usage", `${yearMonth}.json`);
}

/**
 * Generate a short ID: prefix-YYYYMMDD-NNN
 */
export function generateId(prefix) {
  const now = new Date();
  const dateStr =
    String(now.getFullYear()) +
    String(now.getMonth() + 1).padStart(2, "0") +
    String(now.getDate()).padStart(2, "0");
  const rand = String(Math.floor(Math.random() * 1000)).padStart(3, "0");
  return `${prefix}-${dateStr}-${rand}`;
}
