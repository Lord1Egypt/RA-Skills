#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const {
  runtimeHome,
  registryPath,
  stateDir,
  logsDir,
  systemdDir,
  launchdDir,
  windowsDir,
  configFile,
  serviceName,
  unitDir,
  unitPath,
  launchAgentsDir,
  plistPath,
  openclawBin,
  nowIso,
  ensureDir,
  ensureRuntimeDirs,
  writeJson,
  ensureRegistry,
  isValidSessionUuid,
  ensureConfigFile,
  commandExists,
  shellQuote,
  mergeConfig,
  readState,
} = require('./common');

const skillHome = path.resolve(__dirname, '..');
const watcherScript = path.join(skillHome, 'scripts', 'watch-registered-sessions.js');

function usage() {
  console.log(`Usage:
  node scripts/inspector.js register --session-id <id> --session-key <key> --reply-channel <channel> --reply-account <id> --to <target>
                                    [--agent <name>] [--workspace <path>]
                                    [--profile <name>] [--inactive <sec>] [--cooldown <sec>]
                                    [--running-cooldown <sec>] [--blocked-cooldown <sec>] [--notes <text>]
  node scripts/inspector.js unregister --session-id <id> [--mode disable|remove]
  node scripts/inspector.js list
  node scripts/inspector.js status --session-id <id>
  node scripts/inspector.js install
  node scripts/inspector.js doctor

Compatibility wrappers on Unix-like systems:
  scripts/inspector.js ...`);
}

function fail(message, code = 1) {
  console.error(`ERROR: ${message}`);
  process.exit(code);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith('--')) fail(`unknown arg: ${key}`);
    const name = key.slice(2);
    const value = argv[i + 1];
    if (value === undefined || value.startsWith('--')) fail(`missing value for ${key}`);
    args[name] = value;
    i += 1;
  }
  return args;
}

function maybeNumber(value, flagName) {
  if (value === undefined || value === '') return undefined;
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < 0) {
    fail(`${flagName} must be a non-negative number`, 2);
  }
  return parsed;
}

function loadRegistry() {
  return ensureRegistry();
}

function saveRegistry(registry) {
  writeJson(registryPath, registry);
}

function hasCompleteDeliveryTriple(entry) {
  return Boolean(entry.delivery_channel && entry.delivery_account_id && entry.delivery_target);
}

function cmdRegister(argv) {
  const args = parseArgs(argv);
  const sessionId = args['session-id'];
  if (!sessionId) fail('--session-id is required', 2);
  if (['current', 'this', 'latest'].includes(sessionId)) {
    fail(`session_id must be an actual OpenClaw session UUID, not a placeholder like '${sessionId}'`, 2);
  }
  if (!isValidSessionUuid(sessionId)) {
    fail('session_id must be an OpenClaw session UUID like a13ec701-e0ef-4eac-b8cc-6159b3ff830c', 2);
  }
  if (!args['session-key']) fail('--session-key is required', 2);
  if (!args['reply-channel']) fail('--reply-channel is required', 2);
  if (!args['reply-account']) fail('--reply-account is required', 2);
  if (!args.to) fail('--to is required', 2);

  const registry = loadRegistry();
  const entry = {
    session_id: sessionId,
    registered_at: nowIso(),
    enabled: true,
    profile: args.profile || 'default',
  };

  entry.session_key = args['session-key'];
  if (args.agent) entry.agent = args.agent;
  if (args.workspace) entry.workspace = args.workspace;
  if (args.notes) entry.notes = args.notes;
  entry.delivery_channel = args['reply-channel'];
  entry.delivery_account_id = args['reply-account'];
  entry.delivery_target = args.to;

  const numericFields = [
    ['inactive', 'inactive_threshold_seconds'],
    ['cooldown', 'cooldown_seconds'],
    ['running-cooldown', 'running_cooldown_seconds'],
    ['blocked-cooldown', 'blocked_cooldown_seconds'],
  ];
  for (const [flag, field] of numericFields) {
    const value = maybeNumber(args[flag], `--${flag}`);
    if (value !== undefined) entry[field] = value;
  }

  if (!entry.session_key) {
    fail('registration requires --session-key from the agent current session metadata', 2);
  }
  if (!hasCompleteDeliveryTriple(entry)) {
    fail('registration requires complete delivery metadata from the agent current session context: --reply-channel, --reply-account, and --to', 2);
  }

  registry.sessions = registry.sessions.filter((item) => item.session_id !== sessionId);
  registry.sessions.push(entry);
  saveRegistry(registry);
  console.log(`OK: registered session ${sessionId}`);
}

function cmdUnregister(argv) {
  const args = parseArgs(argv);
  const sessionId = args['session-id'];
  const mode = args.mode || 'disable';
  if (!sessionId) fail('--session-id is required', 2);
  if (!['disable', 'remove'].includes(mode)) fail('--mode must be disable or remove', 2);

  const registry = loadRegistry();
  const existing = registry.sessions.find((item) => item.session_id === sessionId);
  if (!existing) fail(`session not registered: ${sessionId}`, 5);

  if (mode === 'remove') {
    registry.sessions = registry.sessions.filter((item) => item.session_id !== sessionId);
  } else {
    registry.sessions = registry.sessions.map((item) => (
      item.session_id === sessionId ? { ...item, enabled: false } : item
    ));
  }
  saveRegistry(registry);
  console.log(`OK: ${mode} session ${sessionId}`);
}

function cmdList() {
  const registry = loadRegistry();
  const rows = [...registry.sessions].sort((a, b) => String(b.registered_at || '').localeCompare(String(a.registered_at || '')));
  if (rows.length === 0) {
    console.log(`INFO: no registered sessions in ${registryPath}`);
    return;
  }
  for (const item of rows) {
    const state = item.enabled === false ? 'disabled' : 'enabled';
    console.log(`session=${item.session_id}\tstate=${state}\tprofile=${item.profile || 'default'}\tagent=${item.agent || ''}\tworkspace=${item.workspace || ''}\tdelivery=${item.delivery_channel || ''}:${item.delivery_target || ''}\taccount=${item.delivery_account_id || ''}`);
  }
}

function cmdStatus(argv) {
  const args = parseArgs(argv);
  const sessionId = args['session-id'];
  if (!sessionId) fail('--session-id is required', 2);
  const registry = loadRegistry();
  const existing = registry.sessions.find((item) => item.session_id === sessionId);
  if (!existing) fail(`session not registered: ${sessionId}`, 5);
  console.log(JSON.stringify(existing, null, 2));
  const state = readState(sessionId);
  if (Object.keys(state).length === 0) {
    console.log('INFO: no runtime state file yet');
  } else {
    console.log('--- state ---');
    console.log(JSON.stringify(state, null, 2));
  }
}

function createSystemdUnit() {
  ensureDir(unitDir);
  const nodeBin = process.execPath;
  const content = `[Unit]\nDescription=OpenClaw Inspector\nAfter=default.target\n\n[Service]\nType=simple\nEnvironment=PATH=${process.env.PATH || ''}\nEnvironment=SESSION_INSPECTOR_HOME=${runtimeHome}\nEnvironment=SESSION_INSPACTOR_HOME=${runtimeHome}\nEnvironmentFile=-${configFile}\nExecStart=${nodeBin} ${watcherScript}\nRestart=always\nRestartSec=60\n\n[Install]\nWantedBy=default.target\n`;
  fs.writeFileSync(unitPath, content, 'utf8');
  fs.writeFileSync(path.join(systemdDir, `${serviceName}.service`), content, 'utf8');
  return {
    manager: 'systemd',
    unit: unitPath,
    next_steps: [
      'systemctl --user daemon-reload',
      `systemctl --user enable --now ${serviceName}.service`,
    ],
  };
}

function createLaunchdPlist() {
  ensureDir(launchAgentsDir);
  const nodeBin = process.execPath;
  const plist = `<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n  <dict>\n    <key>Label</key><string>${serviceName}</string>\n    <key>ProgramArguments</key>\n    <array>\n      <string>${nodeBin}</string>\n      <string>${watcherScript}</string>\n    </array>\n    <key>EnvironmentVariables</key>\n    <dict>\n      <key>SESSION_INSPECTOR_HOME</key><string>${runtimeHome}</string>\n      <key>SESSION_INSPACTOR_HOME</key><string>${runtimeHome}</string>\n      <key>PATH</key><string>${process.env.PATH || ''}</string>\n    </dict>\n    <key>RunAtLoad</key><true/>\n    <key>KeepAlive</key><true/>\n    <key>WorkingDirectory</key><string>${runtimeHome}</string>\n    <key>StandardOutPath</key><string>${path.join(logsDir, 'launchd.stdout.log')}</string>\n    <key>StandardErrorPath</key><string>${path.join(logsDir, 'launchd.stderr.log')}</string>\n  </dict>\n</plist>\n`;
  fs.writeFileSync(plistPath, plist, 'utf8');
  fs.writeFileSync(path.join(launchdDir, `${serviceName}.plist`), plist, 'utf8');
  return {
    manager: 'launchd',
    unit: plistPath,
    next_steps: [
      `launchctl unload ${shellQuote(plistPath)} 2>/dev/null || true`,
      `launchctl load ${shellQuote(plistPath)}`,
    ],
  };
}

function createWindowsHints() {
  const cmdPath = path.join(windowsDir, 'watch-registered-sessions.cmd');
  const psPath = path.join(windowsDir, 'install-task.ps1');
  const nodeBin = process.execPath.replace(/\\/g, '/');
  const scriptPath = watcherScript.replace(/\\/g, '/');
  const cmd = `@echo off\r\nset SESSION_INSPECTOR_HOME=${runtimeHome.replace(/\\/g, '/')}\r\nset SESSION_INSPACTOR_HOME=${runtimeHome.replace(/\\/g, '/')}\r\n"${nodeBin}" "${scriptPath}" %*\r\n`;
  fs.writeFileSync(cmdPath, cmd, 'utf8');
  const ps = `$taskName = '${serviceName}'\n$action = New-ScheduledTaskAction -Execute '${nodeBin}' -Argument '${scriptPath}'\n$trigger = New-ScheduledTaskTrigger -AtLogOn\nRegister-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Description 'OpenClaw Inspector' -Force\n`;
  fs.writeFileSync(psPath, ps, 'utf8');
  return {
    manager: 'windows-task-scheduler',
    runner: cmdPath,
    helper: psPath,
    next_steps: [
      `powershell -ExecutionPolicy Bypass -File "${psPath}"`,
    ],
  };
}

function cmdInstall() {
  ensureRuntimeDirs();
  ensureConfigFile();
  ensureRegistry();

  let service;
  if (process.platform === 'linux' && commandExists('systemctl', ['--user', '--version'])) {
    service = createSystemdUnit();
  } else if (process.platform === 'darwin') {
    service = createLaunchdPlist();
  } else if (process.platform === 'win32') {
    service = createWindowsHints();
  } else {
    service = {
      manager: 'manual',
      next_steps: [`SESSION_INSPECTOR_HOME=${runtimeHome} ${process.execPath} ${watcherScript}`],
    };
  }

  console.log('OK: created runtime files');
  console.log(`runtime_home=${runtimeHome}`);
  console.log(`registry=${registryPath}`);
  console.log(`config=${configFile}`);
  console.log(`watcher=${watcherScript}`);
  console.log(`service_manager=${service.manager}`);
  if (service.unit) console.log(`unit=${service.unit}`);
  if (service.runner) console.log(`runner=${service.runner}`);
  if (service.helper) console.log(`helper=${service.helper}`);
  console.log('service not started');
  console.log('next steps (only if user explicitly requests):');
  for (const step of service.next_steps || []) {
    console.log(`  ${step}`);
  }
}

function safeExec(command, args) {
  const { spawnSync } = require('child_process');
  return spawnSync(command, args, { encoding: 'utf8' });
}

function cmdDoctor() {
  ensureRuntimeDirs();
  const registryExists = fs.existsSync(registryPath);
  let registryValid = false;
  try {
    if (registryExists) {
      ensureRegistry();
      registryValid = true;
    }
  } catch {
    registryValid = false;
  }
  const configExists = fs.existsSync(configFile);
  const openclawAvailable = commandExists(openclawBin, ['--help']);
  const info = {
    platform: process.platform,
    node: process.version,
    runtime_home: runtimeHome,
    registry: registryExists ? 'present' : 'missing',
    registry_json: registryExists ? (registryValid ? 'valid' : 'invalid') : 'n/a',
    config: configExists ? 'present' : 'missing',
    state_dir: fs.existsSync(stateDir) ? 'present' : 'missing',
    logs_dir: fs.existsSync(logsDir) ? 'present' : 'missing',
    openclaw: openclawAvailable ? 'available' : 'missing',
  };

  if (process.platform === 'linux' && commandExists('systemctl', ['--user', '--version'])) {
    info.service_manager = 'systemd';
    info.service_unit = unitPath;
    const result = safeExec('systemctl', ['--user', 'is-active', `${serviceName}.service`]);
    info.service_status = (result.stdout || result.stderr || '').trim() || 'inactive';
  } else if (process.platform === 'darwin') {
    info.service_manager = 'launchd';
    info.service_unit = plistPath;
    info.service_status = fs.existsSync(plistPath) ? 'installed' : 'not-installed';
  } else if (process.platform === 'win32') {
    info.service_manager = 'windows-task-scheduler';
    info.service_status = fs.existsSync(path.join(windowsDir, 'install-task.ps1')) ? 'helper-created' : 'not-installed';
  } else {
    info.service_manager = 'manual';
    info.service_status = 'manual';
  }

  const config = mergeConfig();
  info.scan_interval_seconds = Number(config.SCAN_INTERVAL_SECONDS || 30);
  console.log(JSON.stringify(info, null, 2));
}

function main() {
  const [, , command, ...rest] = process.argv;
  if (!command || ['-h', '--help', 'help'].includes(command)) {
    usage();
    return;
  }

  switch (command) {
    case 'register':
      cmdRegister(rest);
      return;
    case 'unregister':
      cmdUnregister(rest);
      return;
    case 'list':
      cmdList();
      return;
    case 'status':
      cmdStatus(rest);
      return;
    case 'install':
      cmdInstall();
      return;
    case 'doctor':
      cmdDoctor();
      return;
    default:
      fail(`unknown subcommand: ${command}`);
  }
}

main();
