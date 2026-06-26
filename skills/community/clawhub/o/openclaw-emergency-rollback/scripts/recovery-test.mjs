#!/usr/bin/env node
// OpenClaw Emergency Rollback — recovery-test.mjs
// Usage: node recovery-test.mjs <subcommand>
//
// Subcommands:
//   preflight      — check all dependencies and system readiness
//   save-recovery  — copy current openclaw.json to openclaw.recovery
//   sabotage       — deliberately break openclaw.json (makes it invalid JSON)
//   verify         — check if openclaw.json was restored (is valid JSON again)

import { existsSync, readFileSync, writeFileSync, copyFileSync, statSync } from 'fs';
import { execSync } from 'child_process';
import {
  ROLLBACK_DIR, RECOVERY_FILE, CHANGE_LOG, RESTORE_LOG,
  getConfig, getOpenclawJson, getManifest, getWatchdog,
  readJson, appendLog
} from './utils.mjs';

const subcommand = process.argv[2];
if (!subcommand) {
  console.error('Usage: node recovery-test.mjs <preflight|save-recovery|sabotage|verify>');
  process.exit(1);
}

const OC_JSON = getOpenclawJson();

switch (subcommand) {

  case 'preflight': {
    console.log('=== Recovery Test Pre-Flight Check ===');
    let pass = true;

    // Check node (we're running, so it's there)
    console.log(`  ✓ node found: ${process.execPath}`);

    // Check zip/unzip
    for (const tool of ['tar', 'gzip']) {
      try {
        execSync(`command -v ${tool}`, { stdio: 'ignore' });
        console.log(`  ✓ ${tool} found`);
      } catch {
        console.log(`  ✗ ${tool} NOT FOUND — install before proceeding`);
        pass = false;
      }
    }

    console.log('  ✓ no cron dependency — watchdog uses detached Node timers and startup checks');

    // Check rollback directory
    if (existsSync(ROLLBACK_DIR)) {
      console.log('  ✓ rollback directory exists');
    } else {
      console.log('  ✗ rollback directory missing — run setup first');
      pass = false;
    }

    // Check manifest
    const manifest = getManifest();
    console.log(`  ✓ manifest.json (${manifest.snapshots.length} snapshots)`);

    // Check scripts
    const scripts = ['snapshot.mjs', 'restore.mjs', 'restore-if-armed.mjs', 'watchdog-set.mjs', 'watchdog-clear.mjs'];
    for (const s of scripts) {
      const p = `${ROLLBACK_DIR}/scripts/${s}`;
      if (existsSync(p)) {
        console.log(`  ✓ ${s} exists`);
      } else {
        console.log(`  ✗ ${s} missing`);
        pass = false;
      }
    }

    // Check openclaw.json
    if (existsSync(OC_JSON)) {
      const verifyParsed = readJson(OC_JSON);
      if (readJson(OC_JSON)) {
        console.log('  ✓ openclaw.json exists and is valid JSON');
      } else {
        console.log('  ✗ openclaw.json exists but is NOT valid JSON');
        pass = false;
      }
    } else {
      console.log(`  ✗ openclaw.json not found at ${OC_JSON}`);
      pass = false;
    }

    // Check restart command
    const config = getConfig();
    if (config.restartCommand) {
      console.log(`  ✓ restart command: ${config.restartCommand}`);
    } else {
      console.log('  ✗ restart command not configured');
      pass = false;
    }

    console.log('');
    if (pass) {
      console.log('All checks passed. Ready to test.');
    } else {
      console.log('Some checks FAILED. Fix the issues above before testing.');
      process.exit(1);
    }
    break;
  }

  case 'save-recovery': {
    if (!existsSync(OC_JSON)) {
      console.error(`ERROR: openclaw.json not found at ${OC_JSON}`);
      process.exit(1);
    }

    copyFileSync(OC_JSON, RECOVERY_FILE);
    const config = getConfig();
    console.log(`Recovery copy saved: ${RECOVERY_FILE}`);
    console.log('');
    console.log('If the test fails, restore manually with:');
    console.log(`  cp ${RECOVERY_FILE} ${OC_JSON}`);
    console.log(`  ${config.restartCommand || 'kill -USR1 1'}`);

    appendLog(CHANGE_LOG,
      `RECOVERY TEST — MANUAL BACKUP SAVED\n  Source: ${OC_JSON}\n  Backup: ${RECOVERY_FILE}`
    );
    break;
  }

  case 'sabotage': {
    if (!existsSync(OC_JSON)) {
      console.error(`ERROR: openclaw.json not found at ${OC_JSON}`);
      process.exit(1);
    }

    if (!existsSync(RECOVERY_FILE)) {
      console.error(`ERROR: No recovery copy found at ${RECOVERY_FILE}`);
      console.error('Run "node recovery-test.mjs save-recovery" first.');
      process.exit(1);
    }

    const originalSize = statSync(OC_JSON).size;
    const parsed = readJson(OC_JSON);

    // 1. Poison the gateway auth token 
    if (parsed.gateway && parsed.gateway.auth) {
      parsed.gateway.auth.token = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff';
    }

    // 2. Poison the agent workspace paths to break routing logically
    if (parsed.agents && Array.isArray(parsed.agents.list)) {
      parsed.agents.list.forEach(agent => {
        if (agent.workspace) {
          agent.workspace += 'x';
        }
      });
    }

    // Safe write
    writeFileSync(OC_JSON, JSON.stringify(parsed, null, 2));

    console.log('Config sabotaged logically. openclaw.json is VALID JSON, but contains a poisoned token and modified agent workspaces.');
    console.log(`Original size: ${originalSize} bytes`);
    console.log('The watchdog should restore it automatically when the timer expires.');

    appendLog(CHANGE_LOG,
      `RECOVERY TEST — CONFIG SABOTAGED\n  File: ${OC_JSON}\n  Method: Changed gateway token to ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff and poisoned workspace paths\n  Original size: ${originalSize} bytes`
    );
    break;
  }

  case 'verify': {
    console.log('=== Recovery Test Verification ===');

    if (!existsSync(OC_JSON)) {
      console.log('  ✗ openclaw.json not found');
      console.log('RESULT: FAILED');
      process.exit(1);
    }

    const testParsed = readJson(OC_JSON);
    if (!testParsed) {
      console.log('  ✗ openclaw.json exists but is NOT valid JSON (this is unexpected)');
      process.exit(1);
    }
    
    if (testParsed.gateway?.auth?.token === 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' || testParsed.agents?.list?.[0]?.workspace?.endsWith('x')) {
      console.log('  ✗ ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff still present OR workspaces still poisoned');
      console.log('  The Dead Man\'s Switch has NOT restored the config yet.');
      console.log('');
      console.log('RESULT: NOT YET RESTORED — wait longer for background switch to fire');
      console.log('Debug:');
      console.log(`  cat ${RESTORE_LOG}       # restore attempts`);
      console.log(`  node ${ROLLBACK_DIR}/scripts/watchdog-status.mjs  # timer`);
      process.exit(1);
    }

    if (testParsed) {
      console.log('  ✓ openclaw.json is valid JSON');
    } else {
      console.log('  ✗ openclaw.json exists but is NOT valid JSON');
      console.log('RESULT: PARTIAL — file may have been partially restored');
      process.exit(1);
    }

    const watchdog = getWatchdog();
    console.log(`  Watchdog armed: ${watchdog.armed}`);

    if (existsSync(RESTORE_LOG)) {
      const log = readFileSync(RESTORE_LOG, 'utf8');
      const lastRestore = log.split('\n').filter(l => l.includes('RESTORE COMPLETE')).pop();
      if (lastRestore) console.log(`  Last restore: ${lastRestore.trim()}`);
    }

    console.log('');
    console.log('RESULT: PASSED — recovery test successful');

    appendLog(CHANGE_LOG,
      `RECOVERY TEST — VERIFIED PASSED\n  openclaw.json: valid JSON, marker removed\n  Watchdog armed: ${watchdog.armed}`
    );
    break;
}

  default:
    console.error(`Unknown subcommand: ${subcommand}`);
    console.error('Usage: node recovery-test.mjs <preflight|save-recovery|sabotage|verify>');
    process.exit(1);
}
