/**
 * Local profile I/O — reads/writes ~/.lucky-lobster/profile.json
 * Stores 5-dim behavioral classification. Never leaves device.
 */
import os from "node:os";
import path from "node:path";
import fs from "node:fs";

const DATA_DIR = path.join(os.homedir(), ".lucky-lobster");
const PROFILE_FILE = path.join(DATA_DIR, "profile.json");

function ensureDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

export function loadProfile() {
  try {
    if (fs.existsSync(PROFILE_FILE)) {
      return JSON.parse(fs.readFileSync(PROFILE_FILE, "utf-8"));
    }
  } catch (_) { /* corrupt — return null */ }
  return null;
}

export function saveProfile(data) {
  ensureDir();
  fs.writeFileSync(PROFILE_FILE, JSON.stringify({ ...data, updated_at: new Date().toISOString() }, null, 2));
}

// ── Dimension storage (5-dimension behavioral classification) ──

export function saveDimensions(data) {
  const profile = loadProfile() || {};
  profile.dimensions = {
    code: data.code,
    type_name: data.type_name,
    confidence: data.confidence,
    last_evaluated: new Date().toISOString().slice(0, 10),
  };
  saveProfile(profile);
}

export function getDimensions() {
  const profile = loadProfile();
  return profile?.dimensions || null;
}

export function hasDimensions() {
  return !!getDimensions();
}

export function getProfilePath() {
  return PROFILE_FILE;
}
