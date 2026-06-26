/**
 * Fortune history I/O — reads/writes ~/.lucky-lobster/fortune-history.json
 * Tracks past readings, streak counting, weekly lookup.
 */
import os from "node:os";
import path from "node:path";
import fs from "node:fs";

const DATA_DIR = path.join(os.homedir(), ".lucky-lobster");
const HISTORY_FILE = path.join(DATA_DIR, "fortune-history.json");

function ensureDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

export function loadHistory() {
  try {
    if (fs.existsSync(HISTORY_FILE)) {
      return JSON.parse(fs.readFileSync(HISTORY_FILE, "utf-8"));
    }
  } catch (_) { /* corrupt — start fresh */ }
  return { entries: [], streak: 0, last_date: null };
}

export function saveHistory(history) {
  ensureDir();
  fs.writeFileSync(HISTORY_FILE, JSON.stringify(history, null, 2));
}

/** Add a fortune entry and update streak */
export function addEntry(entry) {
  const history = loadHistory();
  const today = new Date().toISOString().slice(0, 10);

  // Update streak
  if (history.last_date) {
    const lastDate = new Date(history.last_date);
    const todayDate = new Date(today);
    const diffDays = Math.round((todayDate - lastDate) / 86400000);
    if (diffDays === 1) {
      history.streak += 1;
    } else if (diffDays > 1) {
      history.streak = 1; // streak broken
    }
    // diffDays === 0 means same day — streak unchanged
  } else {
    history.streak = 1;
  }

  history.last_date = today;
  history.entries.push({
    date: today,
    label: entry.label || entry.dimensions?.type_name || null,
    dimensions: entry.dimensions || null,
    scene: entry.scene || null,
    rating: entry.rating || null,
  });

  // Keep only last 365 entries
  if (history.entries.length > 365) {
    history.entries = history.entries.slice(-365);
  }

  saveHistory(history);
  return history;
}

/** Get current streak count */
export function getStreak() {
  const history = loadHistory();
  return history.streak;
}

/** Get entries for the current week (Monday-Sunday) */
export function getWeekEntries() {
  const history = loadHistory();
  const now = new Date();
  const dayOfWeek = now.getDay(); // 0=Sun
  const monday = new Date(now);
  monday.setDate(now.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1));
  const mondayStr = monday.toISOString().slice(0, 10);

  return history.entries.filter(e => e.date >= mondayStr);
}

/** Check if today is Sunday (weekly review trigger) */
export function isSunday() {
  return new Date().getDay() === 0;
}

/** Check if user already had a reading today */
export function hasTodayReading() {
  const history = loadHistory();
  const today = new Date().toISOString().slice(0, 10);
  return history.entries.some(e => e.date === today);
}

// ── Story Rotation ──

/**
 * Get story IDs used in the last N days.
 * Used by filter-stories to exclude recently-used stories from candidates.
 */
export function getRecentStoryIds(days = 14) {
  const history = loadHistory();
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);
  const cutoffStr = cutoff.toISOString().slice(0, 10);

  const ids = new Set();
  for (const e of history.entries) {
    if (e.date >= cutoffStr && e.story_id) {
      ids.add(e.story_id);
    }
  }
  return ids;
}

/**
 * Record which classic story the LLM used as the narrative shadow.
 * Called by the LLM via --action record-story after Step 3.
 * Always appends a new entry — multiple calls per day accumulate.
 */
export function recordStoryUsage(storyId) {
  const history = loadHistory();
  const today = new Date().toISOString().slice(0, 10);

  history.entries.push({ date: today, story_id: storyId });
  if (history.entries.length > 365) history.entries = history.entries.slice(-365);
  saveHistory(history);
  return true;
}
