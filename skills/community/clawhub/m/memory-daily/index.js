'use strict';

const fs = require('fs');
const path = require('path');

const DEFAULT_MEMORY_DIR = path.join(__dirname, '..', '..', 'memory');

function todayStr() {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function dateFilePath(date, memoryDir) {
  const dir = memoryDir || DEFAULT_MEMORY_DIR;
  return path.join(dir, `${date}.md`);
}

function timeStr() {
  const now = new Date();
  const h = String(now.getHours()).padStart(2, '0');
  const m = String(now.getMinutes()).padStart(2, '0');
  return `${h}:${m}`;
}

/**
 * Ensure today's daily memory file exists.
 * Creates the memory directory and file with a header if missing.
 * @param {string} [memoryDir] - Override memory directory path
 * @returns {string} Path to today's file
 */
function ensureToday(memoryDir) {
  const dir = memoryDir || DEFAULT_MEMORY_DIR;
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const date = todayStr();
  const filePath = dateFilePath(date, dir);
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, `# ${date} Daily Notes\n\n`, 'utf8');
  }
  return filePath;
}

/**
 * Append a timestamped entry to today's daily memory file.
 * @param {string} entry - Content to append
 * @param {string} [memoryDir] - Override memory directory path
 * @returns {string} Path to the file
 */
function append(entry, memoryDir) {
  const filePath = ensureToday(memoryDir);
  const timestamp = timeStr();
  const block = `\n[${timestamp}] ${entry}\n`;
  fs.appendFileSync(filePath, block, 'utf8');
  return filePath;
}

/**
 * Read a daily memory file.
 * @param {string} [date] - Date string YYYY-MM-DD, defaults to today
 * @param {string} [memoryDir] - Override memory directory path
 * @returns {string|null} File content or null if not found
 */
function read(date, memoryDir) {
  const d = date || todayStr();
  const filePath = dateFilePath(d, memoryDir);
  if (!fs.existsSync(filePath)) return null;
  return fs.readFileSync(filePath, 'utf8');
}

/**
 * Read recent daily memory files.
 * @param {number} [days=2] - Number of days to look back
 * @param {string} [memoryDir] - Override memory directory path
 * @returns {Array<{date: string, content: string}>} Array of daily entries
 */
function recent(days, memoryDir) {
  const n = days || 2;
  const results = [];
  for (let i = 0; i < n; i++) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    const dateStr = `${y}-${m}-${dd}`;
    const content = read(dateStr, memoryDir);
    if (content) {
      results.push({ date: dateStr, content });
    }
  }
  return results;
}

module.exports = { ensureToday, append, read, recent };
