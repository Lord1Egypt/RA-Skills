import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'fs';
import { join } from 'path';
import type { Goals, DayLog, FoodLibrary, Meal } from './types.ts';

const BASE_DIR = join(process.env.HOME ?? '~', '.nutrition-claw');
const LOGS_DIR = join(BASE_DIR, 'logs');
const VECTORS_DIR = join(BASE_DIR, 'vectors');
const GOALS_FILE = join(BASE_DIR, 'goals.json');
const FOODS_FILE = join(BASE_DIR, 'foods.json');
const EDUCATION_FILE = join(BASE_DIR, 'education.txt');
const EDUCATION_MAX_LINES = 20;

export function getVectorsDir(): string {
  return VECTORS_DIR;
}

export function ensureDirs(): void {
  for (const dir of [BASE_DIR, LOGS_DIR, VECTORS_DIR]) {
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  }
}

function readJson<T>(path: string, fallback: T): T {
  if (!existsSync(path)) return fallback;
  try {
    return JSON.parse(readFileSync(path, 'utf8')) as T;
  } catch {
    return fallback;
  }
}

function writeJson(path: string, data: unknown): void {
  writeFileSync(path, JSON.stringify(data, null, 2));
}

export function readGoals(): Goals {
  return readJson<Goals>(GOALS_FILE, {});
}

export function writeGoals(goals: Goals): void {
  writeJson(GOALS_FILE, goals);
}

function logPath(date: string): string {
  return join(LOGS_DIR, `${date}.json`);
}

export function readDayLog(date: string): DayLog {
  return readJson<DayLog>(logPath(date), []);
}

export function writeDayLog(date: string, log: DayLog): void {
  writeJson(logPath(date), log);
}

export function listLogDates(): string[] {
  if (!existsSync(LOGS_DIR)) return [];
  return readdirSync(LOGS_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => f.replace('.json', ''))
    .sort();
}

export function getMealById(id: string, date?: string): { meal: Meal; date: string } | null {
  const dates = date ? [date] : listLogDates();
  for (const d of dates) {
    const log = readDayLog(d);
    const meal = log.find(m => m.id === id);
    if (meal) return { meal, date: d };
  }
  return null;
}

export function readFoods(): FoodLibrary {
  return readJson<FoodLibrary>(FOODS_FILE, {});
}

export function writeFoods(foods: FoodLibrary): void {
  writeJson(FOODS_FILE, foods);
}

/**
 * Reads the education log — a plain text file with up to EDUCATION_MAX_LINES lines,
 * one food name per line (most recent at the bottom). Returns a Set of names.
 */
export function readEducationLog(): Set<string> {
  if (!existsSync(EDUCATION_FILE)) return new Set();
  const lines = readFileSync(EDUCATION_FILE, 'utf8')
    .split('\n')
    .map(l => l.trim())
    .filter(Boolean);
  return new Set(lines);
}

/**
 * Appends a food name to the education log. If the log already has
 * EDUCATION_MAX_LINES entries, the oldest line is dropped (FIFO rotation).
 */
export function appendEducationLog(foodName: string): void {
  const lines = existsSync(EDUCATION_FILE)
    ? readFileSync(EDUCATION_FILE, 'utf8').split('\n').map(l => l.trim()).filter(Boolean)
    : [];
  // Remove existing entry for this food if present (re-insertion at bottom = most recent)
  const filtered = lines.filter(l => l !== foodName);
  filtered.push(foodName);
  // Keep only the last EDUCATION_MAX_LINES
  const trimmed = filtered.slice(-EDUCATION_MAX_LINES);
  writeFileSync(EDUCATION_FILE, trimmed.join('\n') + '\n');
}
