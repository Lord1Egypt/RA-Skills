#!/usr/bin/env node
/**
 * JEP Guard v2.0.4 — Post-Install Hook (Security Hardened)
 * 
 * v2.0.4 HARDENING:
 * - REMOVED child_process.spawn/exec/execSync entirely
 * - REMOVED daemon auto-start during installation
 * - REMOVED all background process creation
 * - Pure Node.js fs/net APIs only
 * - User must explicitly start daemon: claw run jep-guard daemon
 * - Explicit interactive consent required for full mode
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');
const nacl = require('tweetnacl');

const CONFIG_DIR = path.join(os.homedir(), '.jep-guard');
const LOG_FILE = path.join(CONFIG_DIR, 'install.log');

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  gray: '\x1b[90m',
  red: '\x1b[31m'
};

function log(msg, level = 'info') {
  const timestamp = new Date().toISOString();
  const line = `[${timestamp}] ${msg}\n`;
  try {
    if (!fs.existsSync(CONFIG_DIR)) fs.mkdirSync(CONFIG_DIR, { recursive: true });
    fs.appendFileSync(LOG_FILE, line);
  } catch (e) {}

  if (level === 'success') console.log(`${colors.green}✓${colors.reset} ${msg}`);
  else if (level === 'warn') console.log(`${colors.yellow}⚠${colors.reset} ${msg}`);
  else if (level === 'error') console.log(`${colors.red}✗${colors.reset} ${msg}`);
  else console.log(`${colors.blue}ℹ${colors.reset} ${msg}`);
}

function ask(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => rl.question(question, ans => { rl.close(); resolve(ans.trim().toLowerCase()); }));
}

// v2.0.4: Pure Node.js sleep helper (retained for potential future use, not for daemon polling)
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// v2.0.4: Check if OpenClaw is available without shell command
function checkOpenClaw() {
  try {
    const paths = (process.env.PATH || '').split(path.delimiter);
    for (const p of paths) {
      if (fs.existsSync(path.join(p, 'claw')) || fs.existsSync(path.join(p, 'claw.exe'))) {
        return true;
      }
    }
    return false;
  } catch (e) {
    return false;
  }
}

// v2.0.4: Check Node.js version
function checkNode() {
  return typeof process !== 'undefined' && process.version;
}

async function main() {
  console.log(`\n${colors.blue}🛡️  JEP Guard v2.0.4 — Security Module Installation${colors.reset}\n`);

  // v2.0.4: Show declared dependencies
  console.log(`${colors.gray}Dependencies check:${colors.reset}`);
  console.log(`${colors.gray}  Node.js: ${checkNode() ? '✓' : '✗'} ${process.version}${colors.reset}`);
  console.log(`${colors.gray}  OpenClaw: ${checkOpenClaw() ? '✓' : '✗ (optional)'}${colors.reset}`);
  console.log('');

  // SECURITY: Always show privilege requirements upfront
  console.log(`${colors.yellow}REQUIRED PRIVILEGES:${colors.reset}`);
  console.log(`${colors.gray}  · Intercept skill executions (preExec hooks)${colors.reset}`);
  console.log(`${colors.gray}  · Write audit logs to ~/.jep-guard/${colors.reset}`);
  console.log(`${colors.gray}  · Run persistent background daemon (MANUAL START ONLY)${colors.reset}`);
  console.log(`${colors.gray}  · Modify OpenClaw runtime security settings${colors.reset}`);
  console.log('');

  // v2.0.4: Explicit security notice
  console.log(`${colors.yellow}SECURITY NOTICE (v2.0.4):${colors.reset}`);
  console.log(`${colors.gray}  · Installer will NEVER spawn background processes${colors.reset}`);
  console.log(`${colors.gray}  · Installer will NEVER execute shell commands${colors.reset}`);
  console.log(`${colors.gray}  · You must manually start the daemon after installation${colors.reset}`);
  console.log('');

  // Non-interactive environments default to passive mode
  if (process.env.CI || process.env.JEP_LITE || process.env.JEP_PASSIVE) {
    log('Non-interactive environment detected. Installing in PASSIVE mode.', 'info');
    installPassive();
    return;
  }

  // Explicit user consent required
  console.log(`${colors.yellow}INSTALLATION OPTIONS:${colors.reset}`);
  console.log(`${colors.gray}  [1] Full Protection — Enable daemon hooks + runtime interception${colors.reset}`);
  console.log(`${colors.gray}  [2] Passive Mode — SDK only, no interception, no daemon${colors.reset}`);
  console.log(`${colors.gray}  [3] Cancel installation${colors.reset}`);
  console.log('');

  const choice = await ask('Your choice [1/2/3]: ');

  switch (choice) {
    case '1':
    case 'full':
      await installFull();
      break;
    case '2':
    case 'passive':
      installPassive();
      break;
    case '3':
    case 'cancel':
      console.log(`\n${colors.yellow}Installation cancelled.${colors.reset}\n`);
      process.exit(0);
    default:
      console.log(`\n${colors.green}Defaulting to Passive Mode...${colors.reset}`);
      installPassive();
  }
}

function installPassive() {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true, mode: 0o700 });
  }

  const config = {
    version: '2.0.4',
    mode: 'passive',
    core: { 
      default_deny: false,
      auto_start: false,
      hooks_enabled: false
    },
    extensions: {
      cross_agent: { enabled: false },
      aegis: { enabled: false },
      cognitive: { enabled: false },
      tee: { enabled: false }
    },
    audit: { 
      stream: 'local',
      retention_days: 30,
      max_size_mb: 100
    },
    ui: { 
      notifications: 'silent',
      confirmation: 'never'
    }
  };

  fs.writeFileSync(path.join(CONFIG_DIR, 'config.json'), JSON.stringify(config, null, 2), { mode: 0o600 });
  generateKeypair();

  log('Passive mode installed successfully.', 'success');
  console.log(`\n${colors.gray}Features available:${colors.reset}`);
  console.log(`${colors.gray}  · SDK for voluntary event logging${colors.reset}`);
  console.log(`${colors.gray}  · Manual audit export${colors.reset}`);
  console.log(`${colors.gray}  · No automatic interception${colors.reset}`);
  console.log(`\n${colors.blue}To enable full protection later:${colors.reset}`);
  console.log(`${colors.gray}  claw run jep-guard init --mode full${colors.reset}`);
  console.log(`${colors.gray}  claw run jep-guard daemon${colors.reset}\n`);
}

async function installFull() {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true, mode: 0o700 });
  }

  // Record explicit consent
  const consentRecord = {
    timestamp: new Date().toISOString(),
    mode: 'full',
    consent: 'explicit',
    version: '2.0.4',
    privileges: [
      'skill_execution_intercept',
      'runtime_config_modification',
      'persistent_daemon_manual_start_only',
      'audit_log_write'
    ],
    security_note: 'Installer did not spawn any processes. Daemon must be started manually by user.'
  };
  fs.writeFileSync(path.join(CONFIG_DIR, 'install-consent.json'), JSON.stringify(consentRecord, null, 2), { mode: 0o600 });

  const config = {
    version: '2.0.4',
    mode: 'personal',
    core: { 
      default_deny: true,
      auto_start: false,        // v2.0.4: NEVER auto-start
      hooks_enabled: true
    },
    extensions: {
      cross_agent: { enabled: true },
      aegis: { enabled: false },
      cognitive: { enabled: false },
      tee: { enabled: false }
    },
    audit: { 
      stream: 'local',
      retention_days: 30,
      max_size_mb: 100
    },
    ui: { 
      notifications: 'minimal',
      confirmation: 'adaptive'
    }
  };

  fs.writeFileSync(path.join(CONFIG_DIR, 'config.json'), JSON.stringify(config, null, 2), { mode: 0o600 });
  generateKeypair();

  const auditPath = path.join(CONFIG_DIR, 'audit-stream.jep');
  if (!fs.existsSync(auditPath)) {
    fs.writeFileSync(auditPath, '', { mode: 0o600 });
  }

  // v2.0.4: Pure Node.js runtime registration check (no shell, no spawn)
  const hasOpenClaw = checkOpenClaw();
  if (hasOpenClaw) {
    log('OpenClaw runtime detected', 'info');
    log('To register as security module, run manually:', 'info');
    console.log(`${colors.gray}   claw config set security.module jep-guard${colors.reset}`);
  } else {
    log('OpenClaw runtime not detected (standalone mode)', 'warn');
  }

  // v2.0.4 SECURITY FIX: Removed all daemon auto-start logic.
  // Previous versions used child_process.spawn here; this has been completely removed.
  // The daemon must be started explicitly by the user after installation.
  log('Installation complete. Daemon auto-start disabled by design (v2.0.4).', 'success');
  log('To start the daemon manually:', 'info');
  console.log(`${colors.gray}   claw run jep-guard daemon --mode ${config.mode}${colors.reset}`);
  console.log(`${colors.gray}   # or after npm run build: node dist/daemon/server.js --mode ${config.mode}${colors.reset}`);

  console.log(`\n${colors.green}✅ JEP Guard v2.0.4 — Full Protection Configured${colors.reset}`);
  console.log(`${colors.gray}   Consent recorded: ${CONFIG_DIR}/install-consent.json${colors.reset}`);
  console.log(`${colors.gray}   Mode: ${config.mode}${colors.reset}`);
  console.log(`${colors.gray}   Config: ${CONFIG_DIR}/config.json${colors.reset}`);
  console.log(`${colors.gray}   Daemon: STOPPED (manual start required)${colors.reset}`);
  console.log(`\n${colors.blue}Quick commands:${colors.reset}`);
  console.log(`${colors.gray}   Start daemon: claw run jep-guard daemon${colors.reset}`);
  console.log(`${colors.gray}   View status:  claw run jep-guard status${colors.reset}`);
  console.log(`${colors.gray}   View logs:    claw run jep-guard log --last${colors.reset}`);
  console.log(`${colors.gray}   Dashboard:    claw run jep-guard dashboard${colors.reset}`);
  console.log(`\n${colors.yellow}💡 Tip: Most operations are silent. You'll only hear from us when something matters.${colors.reset}\n`);
}

function generateKeypair() {
  const keyPath = path.join(CONFIG_DIR, 'guard.key');
  if (!fs.existsSync(keyPath)) {
    const kp = nacl.sign.keyPair();

    const keyData = {
      pubkey: Buffer.from(kp.publicKey).toString('base64'),
      created_at: Date.now(),
      algorithm: 'Ed25519',
      _security_note: 'This key identifies JEP Guard. Keep safe.'
    };

    fs.writeFileSync(keyPath, JSON.stringify(keyData, null, 2), { mode: 0o600 });
    log('Generated Guard identity key (Ed25519)', 'success');
  }
}

main().catch(err => {
  log(`Setup error: ${err.message}`, 'error');
  process.exit(1);
});