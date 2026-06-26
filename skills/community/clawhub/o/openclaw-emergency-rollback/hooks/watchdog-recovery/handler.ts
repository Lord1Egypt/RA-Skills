import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { spawn, execSync } from 'child_process';

function appendLog(logFile: string, entry: string) {
  mkdirSync(dirname(logFile), { recursive: true });
  const ts = new Date().toISOString().replace('T', ' ').replace(/\.\d+Z$/, '');
  const existing = existsSync(logFile) ? readFileSync(logFile, 'utf8') : '';
  writeFileSync(logFile, existing + `[${ts}] ${entry}\n---\n`);
}

const handler = async (event: any) => {
  if (event?.type !== 'gateway' || event?.action !== 'startup') return;

  const home = process.env.OPENCLAW_HOME || join(process.env.HOME || '/home/node', '.openclaw');
  const rollbackDir = join(home, 'rollback');
  const watchdogFile = join(rollbackDir, 'watchdog.json');
  const restoreLog = join(rollbackDir, 'logs', 'restore.log');
  const restoreScript = join(rollbackDir, 'scripts', 'restore-if-armed.mjs');
  const timerScript = join(rollbackDir, 'scripts', 'watchdog-timer.mjs');

  appendLog(restoreLog, 'HOOK gateway:startup — entered watchdog recovery hook');

  if (!existsSync(watchdogFile)) {
    appendLog(restoreLog, 'HOOK gateway:startup — watchdog.json missing, nothing to do');
    return;
  }
  if (!existsSync(restoreScript)) {
    appendLog(restoreLog, 'HOOK gateway:startup — restore-if-armed.mjs missing, nothing to do');
    return;
  }

  let watchdog: any = null;
  try {
    watchdog = JSON.parse(readFileSync(watchdogFile, 'utf8'));
  } catch (e: any) {
    appendLog(restoreLog, `HOOK gateway:startup — failed to parse watchdog.json: ${e?.message || e}`);
    return;
  }

  if (!watchdog?.armed) {
    appendLog(restoreLog, 'HOOK gateway:startup — watchdog not armed, nothing to do');
    return;
  }

  const now = Math.floor(Date.now() / 1000);
  const expiry = watchdog.expiryEpoch || 0;
  const remaining = expiry - now;

  appendLog(restoreLog, `HOOK gateway:startup — watchdog armed, expiry=${expiry}, now=${now}, remaining=${remaining}s`);

  if (now >= expiry) {
    appendLog(restoreLog, 'HOOK gateway:startup — watchdog expired, invoking restore-if-armed.mjs');
    try {
      execSync(`node "${restoreScript}"`, {
        stdio: 'ignore',
        env: { ...process.env, WATCHDOG_TRIGGERED: '1', WATCHDOG_SOURCE: 'gateway:startup-hook' }
      });
      appendLog(restoreLog, 'HOOK gateway:startup — restore-if-armed.mjs returned');
    } catch (e: any) {
      appendLog(restoreLog, `HOOK gateway:startup — restore-if-armed.mjs failed: ${e?.message || e}`);
    }
    return;
  }

  if (!existsSync(timerScript)) {
    appendLog(restoreLog, 'HOOK gateway:startup — watchdog-timer.mjs missing, cannot respawn timer');
    return;
  }

  try {
    const child = spawn(process.execPath, [timerScript, '0', String(remaining)], {
      detached: true,
      stdio: 'ignore',
      env: { ...process.env, WATCHDOG_SOURCE: 'gateway:startup-hook' }
    });
    child.unref();
    appendLog(restoreLog, `HOOK gateway:startup — respawned watchdog timer pid=${child.pid || 'unknown'} remaining=${remaining}s`);
  } catch (e: any) {
    appendLog(restoreLog, `HOOK gateway:startup — failed to respawn watchdog timer: ${e?.message || e}`);
  }
};

export default handler;
