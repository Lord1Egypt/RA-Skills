/**
 * Version Checker — Checks current vs latest OpenClaw version.
 * Used by the ham radio update indicator.
 */

import { execSync } from 'child_process';

export interface VersionInfo {
  current: string;
  latest: string;
  updateAvailable: boolean;
  lastChecked: number;
}

let cachedVersion: VersionInfo | null = null;
let lastCheckMs = 0;
const CACHE_TTL_MS = 5 * 60_000; // Cache for 5 minutes

export function getVersionInfo(): VersionInfo {
  const now = Date.now();
  if (cachedVersion && now - lastCheckMs < CACHE_TTL_MS) {
    return cachedVersion;
  }

  let current = 'unknown';
  let latest = 'unknown';

  try {
    current = execSync('openclaw --version', { timeout: 5000, encoding: 'utf-8' }).trim();
  } catch {
    try {
      const list = execSync('npm list -g openclaw --json', { timeout: 5000, encoding: 'utf-8' });
      const parsed = JSON.parse(list);
      current = parsed?.dependencies?.openclaw?.version || 'unknown';
    } catch { /* ignore */ }
  }

  try {
    latest = execSync('npm view openclaw version', { timeout: 10_000, encoding: 'utf-8' }).trim();
  } catch { /* ignore */ }

  cachedVersion = {
    current,
    latest,
    updateAvailable: current !== 'unknown' && latest !== 'unknown' && current !== latest,
    lastChecked: now,
  };
  lastCheckMs = now;
  return cachedVersion;
}

export function runUpdate(): { success: boolean; output: string } {
  try {
    const output = execSync('npm update -g openclaw', {
      timeout: 120_000,
      encoding: 'utf-8',
      env: { ...process.env, NODE_ENV: undefined },
    });
    // Clear cache so next check gets fresh data
    cachedVersion = null;
    lastCheckMs = 0;
    return { success: true, output: output.trim() };
  } catch (err) {
    const error = err as { stderr?: string; message?: string };
    return { success: false, output: error.stderr || error.message || 'Update failed' };
  }
}

// ── Solara remote version checks ──────────────────────────

import { REMOTE_AGENTS } from './config.js';

let solaraCachedVersion: VersionInfo | null = null;
let solaraLastCheckMs = 0;

function remoteSsh(agentId: string, cmd: string, timeout = 10_000): string {
  const remote = REMOTE_AGENTS.find(r => r.id === agentId);
  if (!remote) throw new Error(`No remote config for agent: ${agentId}`);

  const sshCmd = remote.password
    ? `sshpass -p '${remote.password}' ssh -o ConnectTimeout=4 -o StrictHostKeyChecking=no -o LogLevel=ERROR ${remote.user}@${remote.host} '${cmd}'`
    : `ssh -o ConnectTimeout=4 -o StrictHostKeyChecking=no -o LogLevel=ERROR ${remote.user}@${remote.host} '${cmd}'`;

  return execSync(sshCmd, { timeout, encoding: 'utf-8' }).trim();
}

/** Legacy alias — uses first remote agent */
function solaraSsh(cmd: string, timeout = 10_000): string {
  const first = REMOTE_AGENTS[0];
  if (!first) throw new Error('No remote agents configured');
  return remoteSsh(first.id, cmd, timeout);
}

export function getSolaraVersionInfo(): VersionInfo & { online: boolean } {
  const now = Date.now();
  if (solaraCachedVersion && now - solaraLastCheckMs < CACHE_TTL_MS) {
    return { ...solaraCachedVersion, online: true };
  }

  try {
    let current = 'unknown';
    try {
      current = solaraSsh('openclaw --version');
    } catch {
      try {
        const json = solaraSsh('npm list -g openclaw --json 2>/dev/null');
        const parsed = JSON.parse(json);
        current = parsed?.dependencies?.openclaw?.version || 'unknown';
      } catch { /* ignore */ }
    }

    let latest = 'unknown';
    try {
      latest = solaraSsh('npm view openclaw version');
    } catch { /* ignore */ }

    solaraCachedVersion = {
      current,
      latest,
      updateAvailable: current !== 'unknown' && latest !== 'unknown' && current !== latest,
      lastChecked: now,
    };
    solaraLastCheckMs = now;
    return { ...solaraCachedVersion, online: true };
  } catch {
    return { current: 'unknown', latest: 'unknown', updateAvailable: false, lastChecked: now, online: false };
  }
}

export function runSolaraUpdate(): { success: boolean; output: string } {
  try {
    const output = solaraSsh('npm update -g openclaw 2>&1', 120_000);
    solaraCachedVersion = null;
    solaraLastCheckMs = 0;
    return { success: true, output };
  } catch (err) {
    const error = err as { stderr?: string; message?: string };
    return { success: false, output: error.stderr || error.message || 'Remote update failed' };
  }
}
