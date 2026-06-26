/**
 * Session persistence -- load/save sessions from ~/.agent-wallet/sessions.json.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { join } from "path";
import type { Session, Sessions } from "./types.js";

export const SESSIONS_DIR = join(process.env.HOME || "/tmp", ".agent-wallet");
export const SESSIONS_FILE = join(SESSIONS_DIR, "sessions.json");

export function loadSessions(): Sessions {
  if (!existsSync(SESSIONS_FILE)) return {};
  try {
    return JSON.parse(readFileSync(SESSIONS_FILE, "utf8")) as Sessions;
  } catch {
    return {};
  }
}

export function saveSessions(sessions: Sessions): void {
  mkdirSync(SESSIONS_DIR, { recursive: true });
  writeFileSync(SESSIONS_FILE, JSON.stringify(sessions, null, 2));
}

export function saveSession(topic: string, data: Omit<Session, "updatedAt">): void {
  const sessions = loadSessions();
  sessions[topic] = { ...data, updatedAt: new Date().toISOString() };
  saveSessions(sessions);
}
