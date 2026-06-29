// ----------------------------------------------------------------------------
// browser-state.js
//
// Persists the running Chromium's CDP endpoint to a state file so that
// subsequent CLI invocations can re-attach to the same browser. Without this
// every CLI call would spawn a fresh browser and lose its tab + cookies.
//
// State layout (~/.cache/pricewin-deal-finder/session-<id>.json):
//   {
//     "id": "<8-char id>",
//     "wsEndpoint": "ws://127.0.0.1:<port>/devtools/browser/<uuid>",
//     "pid": 12345,
//     "createdAt": "2026-05-18T10:00:00Z"
//   }
// ----------------------------------------------------------------------------

import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { existsSync, mkdirSync } from 'node:fs';

const STATE_DIR = path.join(os.homedir(), '.cache', 'pricewin-deal-finder');
const DEFAULT_SESSION = 'default';

function ensureDir() {
  if (!existsSync(STATE_DIR)) mkdirSync(STATE_DIR, { recursive: true });
}

function statePath(sessionId = DEFAULT_SESSION) {
  return path.join(STATE_DIR, `session-${sessionId}.json`);
}

export async function saveState(state, sessionId = DEFAULT_SESSION) {
  ensureDir();
  await fs.writeFile(statePath(sessionId), JSON.stringify(state, null, 2));
}

export async function loadState(sessionId = DEFAULT_SESSION) {
  try {
    const raw = await fs.readFile(statePath(sessionId), 'utf8');
    return JSON.parse(raw);
  } catch (err) {
    if (err.code === 'ENOENT') return null;
    throw err;
  }
}

export async function clearState(sessionId = DEFAULT_SESSION) {
  await fs.unlink(statePath(sessionId)).catch(() => {});
}

export function isProcessAlive(pid) {
  if (!pid) return false;
  try {
    // Signal 0 = test without actually signalling. Throws if process gone.
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}
