#!/usr/bin/env node
// OpenClaw Emergency Rollback — restore-if-armed.mjs
// Called by watchdog timer and native OpenClaw startup hook.
// Checks if watchdog is armed and timer has expired. Fires restore if so.

import { existsSync } from 'fs';
import { execSync } from 'child_process';
import { join } from 'path';
import { ROLLBACK_DIR, WATCHDOG_FILE, RESTORE_LOG, getWatchdog, appendLog } from './utils.mjs';

appendLog(RESTORE_LOG, `RESTORE-IF-ARMED — entered pid=${process.pid} ppid=${process.ppid} source=${process.env.WATCHDOG_SOURCE || 'direct'} triggeredByTimer=${process.env.WATCHDOG_TRIGGERED === '1'} triggeredByStartup=${process.env.RESTART_TRIGGERED === '1'}`);

if (!existsSync(WATCHDOG_FILE)) {
  appendLog(RESTORE_LOG, 'RESTORE-IF-ARMED — watchdog.json missing, exiting');
  process.exit(0);
}

const watchdog = getWatchdog();

if (!watchdog.armed) {
  appendLog(RESTORE_LOG, 'RESTORE-IF-ARMED — watchdog not armed, exiting');
  process.exit(0);
}

const now = Math.floor(Date.now() / 1000);
const expiry = watchdog.expiryEpoch || 0;
appendLog(RESTORE_LOG, `RESTORE-IF-ARMED — watchdog armed, now=${now}, expiry=${expiry}, remaining=${expiry - now}s`);

if (now >= expiry) {
  appendLog(RESTORE_LOG, 'RESTORE-IF-ARMED — watchdog armed and expired, triggering restore');
  process.env.RESTART_TRIGGERED = '1';
  const restoreScript = join(ROLLBACK_DIR, 'scripts', 'restore.mjs');
  try {
    execSync(`node "${restoreScript}"`, { stdio: 'inherit', env: { ...process.env, RESTART_TRIGGERED: '1' } });
  } catch (e) {
    appendLog(RESTORE_LOG, `RESTORE-IF-ARMED ERROR — restore.mjs failed: ${e?.status || 'unknown'} ${e?.message || e}`);
    process.exit(1);
  }
} else {
  const remaining = expiry - now;
  appendLog(RESTORE_LOG, `RESTORE-IF-ARMED — watchdog not expired, respawning timer for ${remaining}s`);
  const timerScript = join(ROLLBACK_DIR, 'scripts', 'watchdog-timer.mjs');
  if (existsSync(timerScript)) {
    const { spawn } = await import('child_process');
    const child = spawn(process.execPath, [timerScript, '0', String(remaining)], {
      detached: true,
      stdio: 'ignore',
      env: { ...process.env, WATCHDOG_SOURCE: 'restore-if-armed' }
    });
    child.unref();
    appendLog(RESTORE_LOG, `RESTORE-IF-ARMED — respawned watchdog timer pid=${child.pid || 'unknown'} remaining=${remaining}s`);
  } else {
    appendLog(RESTORE_LOG, 'RESTORE-IF-ARMED ERROR — watchdog-timer.mjs missing, cannot respawn timer');
  }
}

process.exit(0);
