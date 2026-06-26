#!/usr/bin/env node
import { existsSync } from 'fs';
import { join } from 'path';
import { execSync } from 'child_process';
import { getWatchdog, WATCHDOG_FILE, ROLLBACK_DIR, RESTORE_LOG, appendLog } from './utils.mjs';

const minutesArgs = parseInt(process.argv[2], 10) || 0;
const explicitSeconds = parseInt(process.argv[3], 10) || 0;

let timeoutMs = 0;
if (explicitSeconds > 0) {
  timeoutMs = explicitSeconds * 1000;
} else if (minutesArgs > 0) {
  timeoutMs = minutesArgs * 60 * 1000;
}

appendLog(RESTORE_LOG, `WATCHDOG TIMER — started pid=${process.pid} ppid=${process.ppid} timeoutMs=${timeoutMs}`);

if (timeoutMs <= 0) {
  appendLog(RESTORE_LOG, 'WATCHDOG TIMER — exiting immediately because timeoutMs <= 0');
  process.exit(0);
}

setTimeout(() => {
  appendLog(RESTORE_LOG, `WATCHDOG TIMER — fired pid=${process.pid}`);
  if (!existsSync(WATCHDOG_FILE)) {
    appendLog(RESTORE_LOG, 'WATCHDOG TIMER — watchdog.json missing at fire time, exiting');
    process.exit(0);
  }

  const watchdog = getWatchdog();
  appendLog(RESTORE_LOG, `WATCHDOG TIMER — armed=${Boolean(watchdog.armed)} expiry=${watchdog.expiryEpoch || 'null'}`);

  if (watchdog.armed) {
    const restoreIfArmed = join(ROLLBACK_DIR, 'scripts', 'restore-if-armed.mjs');
    try {
      appendLog(RESTORE_LOG, `WATCHDOG TIMER — invoking restore-if-armed.mjs via ${restoreIfArmed}`);
      execSync(`node "${restoreIfArmed}"`, {
        stdio: 'ignore',
        env: { ...process.env, WATCHDOG_TRIGGERED: '1' }
      });
      appendLog(RESTORE_LOG, 'WATCHDOG TIMER — restore-if-armed.mjs returned without throwing');
    } catch (e) {
      appendLog(RESTORE_LOG, `WATCHDOG TIMER ERROR — restore-if-armed.mjs failed: ${e?.message || e}`);
    }
  } else {
    appendLog(RESTORE_LOG, 'WATCHDOG TIMER — watchdog not armed at fire time, exiting');
  }
  process.exit(0);
}, timeoutMs);
