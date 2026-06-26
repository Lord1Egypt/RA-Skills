// Background update checker.
// File reads are delegated to state-io.mjs.
// This module only handles network update-check logic.
// Only sends { key, current_version } — no user data or memory content.

import { resolve } from "node:path";
import { readJsonSafe, atomicWriteJson, existsSync } from "./state-io.mjs";

/**
 * Fire-and-forget, never blocks startup. Checks at most once every 24 hours.
 * Silent on any error.
 * @param {string} home - User home directory
 */
export function checkForUpdates(home) {
  (async () => {
    try {
      const stateDir = resolve(home, ".openclaw/memory-stack");
      const statePath = resolve(stateDir, "update-state.json");

      // Throttle: 24hr
      const state = readJsonSafe(statePath) || {};
      if (Date.now() - (state.last_check || 0) < 86_400_000) return;

      // Read local version
      const versionFile = resolve(stateDir, "version.json");
      if (!existsSync(versionFile)) return;

      const version = readJsonSafe(versionFile);
      if (!version) return;

      // Check update (5s timeout)
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 5000);
      const res = await fetch("https://openclaw-api.apptah.com/api/check-update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ current: version.version }),
        signal: controller.signal,
      });
      clearTimeout(timer);

      if (!res.ok) {
        atomicWriteJson(statePath, { last_check: Date.now(), latest: null });
        return;
      }

      const data = await res.json();

      atomicWriteJson(statePath, {
        last_check: Date.now(),
        latest: data.latest || null,
        update_available: !!data.update_available,
      });
    } catch {
      // Silent — never block normal startup
    }
  })();
}

/**
 * Check if an auto-update just happened and return a notification message.
 * Clears the flag after reading.
 * @param {string} home
 * @returns {string|null}
 */
export function checkPostUpdateNotification(home) {
  const updateState = resolve(home, ".openclaw/memory-stack/update-state.json");
  const us = readJsonSafe(updateState);
  if (!us || us.auto_updated !== true) return null;
  us.auto_updated = false;
  atomicWriteJson(updateState, us);
  return `\u{2705} Memory Stack auto-updated to v${us.latest}`;
}

/**
 * Check if an update is available and return a notification message.
 * @param {string} home
 * @returns {string|null}
 */
export function getUpdateAvailableNotice(home) {
  const statePath = resolve(home, ".openclaw/memory-stack/update-state.json");
  const state = readJsonSafe(statePath);
  if (!state || !state.update_available || !state.latest) return null;
  return `Memory Stack v${state.latest} is available. Run: openclaw-memory upgrade`;
}
