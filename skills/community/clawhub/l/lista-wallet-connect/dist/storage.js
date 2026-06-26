/**
 * Session persistence -- load/save sessions from ~/.agent-wallet/sessions.json.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { join } from "path";
export const SESSIONS_DIR = join(process.env.HOME || "/tmp", ".agent-wallet");
export const SESSIONS_FILE = join(SESSIONS_DIR, "sessions.json");
export function loadSessions() {
    if (!existsSync(SESSIONS_FILE))
        return {};
    try {
        return JSON.parse(readFileSync(SESSIONS_FILE, "utf8"));
    }
    catch {
        return {};
    }
}
export function saveSessions(sessions) {
    mkdirSync(SESSIONS_DIR, { recursive: true });
    writeFileSync(SESSIONS_FILE, JSON.stringify(sessions, null, 2));
}
export function saveSession(topic, data) {
    const sessions = loadSessions();
    sessions[topic] = { ...data, updatedAt: new Date().toISOString() };
    saveSessions(sessions);
}
