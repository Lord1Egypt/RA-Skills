/**
 * Push preferences management.
 * Reads/writes ~/.lucky-lobster/preferences.json
 */
import os from "node:os";
import path from "node:path";
import fs from "node:fs";

const DATA_DIR = path.join(os.homedir(), ".lucky-lobster");
const PREFS_FILE = path.join(DATA_DIR, "preferences.json");

const DEFAULTS = {
  push_enabled: true,
  push_frequency: {
    max_per_day: 1,
    quiet_hours: "22:00-08:00",
  },
};

function ensureDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

export function loadPreferences() {
  try {
    if (fs.existsSync(PREFS_FILE)) {
      return { ...DEFAULTS, ...JSON.parse(fs.readFileSync(PREFS_FILE, "utf-8")) };
    }
  } catch (_) { /* corrupt — use defaults */ }
  return { ...DEFAULTS };
}

export function savePreferences(prefs) {
  ensureDir();
  fs.writeFileSync(PREFS_FILE, JSON.stringify(prefs, null, 2));
}

export function initPreferences() {
  if (!fs.existsSync(PREFS_FILE)) {
    savePreferences(DEFAULTS);
  }
  return loadPreferences();
}

