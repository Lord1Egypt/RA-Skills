#!/usr/bin/env node
/**
 * OpenClaw Cross-Platform Backup & Restore v3.0
 * Works on Windows, macOS, and Linux. Archives are interchangeable across all platforms.
 *
 * Part of MyClaw.ai (https://myclaw.ai) open skills ecosystem.
 *
 * SECURITY:
 *   - Archives contain bot tokens, API keys, and session credentials
 *   - Permissions hardened on non-Windows (chmod 600 for archive, 700/600 for credentials)
 *   - Pre-restore snapshot always created before overwriting
 *   - Gateway token preserved by default (prevents Control UI mismatch)
 *   - Interactive confirmation required before destructive restore
 *
 * Usage:
 *   node backup-restore.js backup [--output-dir <dir>]
 *   node backup-restore.js restore <archive> [--dry-run] [--overwrite-gateway-token]
 *   node backup-restore.js list [--backup-dir <dir>]
 */

'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');
const readline = require('readline');

// ── Config ──────────────────────────────────────────────────────────────────
const HOME = os.homedir();
const OPENCLAW_DIR = path.join(HOME, '.openclaw');
const DEFAULT_BACKUP_DIR = path.join(HOME, 'openclaw-backups');
const VERSION = '3.0.0';
const MAX_BACKUPS = 7;
const IS_WIN = process.platform === 'win32';

// Parse CLI args
const args = process.argv.slice(2);
const action = args[0];
const flag = (name) => args.includes(name);
const flagVal = (name, def) => {
  const i = args.indexOf(name);
  return i !== -1 && args[i + 1] ? args[i + 1] : def;
};

// ── Exclude patterns ────────────────────────────────────────────────────────
const EXCLUDE_DIRS = new Set([
  'node_modules', '.git', 'logs', '.cache', 'canvas', 'tmp', 'media',
  'browser',      // browser automation data — ephemeral
  'completions',  // shell completions — regenerated
]);
const EXCLUDE_EXTS = new Set([
  '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg',
  '.mp4', '.mp3', '.wav', '.ogg', '.webm',
  '.skill', '.zip',
]);
const EXCLUDE_PATTERNS = [/\.tar\.gz$/, /\.lock$/, /\.deleted\./];

// Known channel directory names (auto-discovered, but these are the expected ones)
const KNOWN_CHANNELS = [
  'telegram', 'whatsapp', 'signal', 'discord', 'dingtalk',
  'wecom-app', 'feishu', 'slack', 'irc', 'googlechat', 'imessage',
];

// ── Colors ──────────────────────────────────────────────────────────────────
const c = {
  green: s => `\x1b[32m${s}\x1b[0m`,
  yellow: s => `\x1b[33m${s}\x1b[0m`,
  red: s => `\x1b[31m${s}\x1b[0m`,
  cyan: s => `\x1b[36m${s}\x1b[0m`,
  dim: s => `\x1b[2m${s}\x1b[0m`,
};
const info = (msg) => console.log(`${c.green('[✓]')} ${msg}`);
const warn = (msg) => console.log(`${c.yellow('[!]')} ${msg}`);
const error = (msg) => { console.error(`${c.red('[✗]')} ${msg}`); process.exit(1); };

// ── Helpers ─────────────────────────────────────────────────────────────────
function formatSize(bytes) {
  if (bytes > 1e9) return (bytes / 1e9).toFixed(2) + ' GB';
  if (bytes > 1e6) return (bytes / 1e6).toFixed(2) + ' MB';
  if (bytes > 1e3) return (bytes / 1e3).toFixed(2) + ' KB';
  return bytes + ' B';
}

function timestamp() {
  const d = new Date();
  return d.getFullYear().toString() +
    String(d.getMonth() + 1).padStart(2, '0') +
    String(d.getDate()).padStart(2, '0') + '_' +
    String(d.getHours()).padStart(2, '0') +
    String(d.getMinutes()).padStart(2, '0') +
    String(d.getSeconds()).padStart(2, '0');
}

function ask(question) {
  return new Promise(resolve => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question(question, ans => { rl.close(); resolve(ans.trim()); });
  });
}

function getAgentName() {
  try {
    const idFile = path.join(OPENCLAW_DIR, 'workspace', 'IDENTITY.md');
    if (fs.existsSync(idFile)) {
      const content = fs.readFileSync(idFile, 'utf8');
      const match = content.match(/\*\*Name:\*\*\s*(.+)/);
      if (match) {
        const name = match[1].trim().replace(/\s+/g, '-').toLowerCase();
        if (name && !name.startsWith('_') && name.length > 1) return name;
      }
    }
  } catch {}
  return os.hostname();
}

function getOpenClawVersion() {
  try {
    const cmd = IS_WIN ? 'cmd /c openclaw --version' : 'openclaw --version';
    return execSync(cmd, { encoding: 'utf8', timeout: 5000 }).trim().split('\n')[0];
  } catch { return 'unknown'; }
}

function shouldExcludeFile(name) {
  const ext = path.extname(name).toLowerCase();
  if (EXCLUDE_EXTS.has(ext)) return true;
  return EXCLUDE_PATTERNS.some(re => re.test(name));
}

/** Set restrictive permissions (non-Windows only) */
function harden(filePath, mode) {
  if (IS_WIN) return;
  try { fs.chmodSync(filePath, mode); } catch {}
}

/** Recursively harden all files in a directory */
function hardenDir(dirPath, dirMode, fileMode) {
  if (IS_WIN || !fs.existsSync(dirPath)) return;
  harden(dirPath, dirMode);
  try {
    for (const entry of fs.readdirSync(dirPath, { withFileTypes: true })) {
      const p = path.join(dirPath, entry.name);
      if (entry.isDirectory()) hardenDir(p, dirMode, fileMode);
      else harden(p, fileMode);
    }
  } catch {}
}

/** Copy directory recursively with filtering (workspace, agents) */
function copyDirFiltered(src, dest, stats = { files: 0, bytes: 0 }) {
  if (!fs.existsSync(src)) return stats;
  fs.mkdirSync(dest, { recursive: true });

  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      if (EXCLUDE_DIRS.has(entry.name)) continue;
      copyDirFiltered(srcPath, destPath, stats);
    } else if (entry.isFile()) {
      if (shouldExcludeFile(entry.name)) continue;
      try {
        fs.copyFileSync(srcPath, destPath);
        const stat = fs.statSync(destPath);
        stats.files++;
        stats.bytes += stat.size;
      } catch {}  // Skip locked/unreadable files
    }
  }
  return stats;
}

/** Copy directory without filtering (config dirs) */
function copyDirAll(src, dest) {
  if (!fs.existsSync(src)) return false;
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirAll(srcPath, destPath);
    } else if (entry.isFile()) {
      try { fs.copyFileSync(srcPath, destPath); } catch {}
    }
  }
  return true;
}

function countFiles(dir) {
  if (!fs.existsSync(dir)) return 0;
  let count = 0;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) count += countFiles(path.join(dir, entry.name));
    else count++;
  }
  return count;
}

function rmrf(dir) {
  if (!fs.existsSync(dir)) return;
  fs.rmSync(dir, { recursive: true, force: true });
}

/** Auto-discover channel directories under OPENCLAW_DIR */
function discoverChannelDirs() {
  const found = [];
  try {
    for (const entry of fs.readdirSync(OPENCLAW_DIR, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      if (KNOWN_CHANNELS.includes(entry.name)) {
        found.push(entry.name);
      }
    }
  } catch {}
  return found;
}

/** Auto-discover all workspace-* directories */
function discoverWorkspaceDirs() {
  const found = [];
  try {
    for (const entry of fs.readdirSync(OPENCLAW_DIR, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      // workspace is the main one; workspace-* are extra (team, dev, pm, etc.)
      if (entry.name.startsWith('workspace-')) {
        found.push(entry.name);
      }
    }
  } catch {}
  return found;
}

// ── Archive (tar.gz / ZIP cross-platform) ───────────────────────────────────
function hasTar() {
  try {
    execSync(IS_WIN ? 'where tar' : 'which tar', { stdio: 'ignore' });
    return true;
  } catch { return false; }
}

function createArchive(sourceDir, archivePath) {
  const dirName = path.basename(sourceDir);
  const parentDir = path.dirname(sourceDir);

  if (hasTar()) {
    execSync(`tar -czf "${archivePath}" -C "${parentDir}" "${dirName}"`, { stdio: 'ignore' });
  } else if (IS_WIN) {
    // Fallback: PowerShell Compress-Archive (creates zip)
    const zipPath = archivePath.replace(/\.tar\.gz$/, '.zip');
    execSync(
      `powershell -NoProfile -Command "Compress-Archive -Path '${sourceDir}' -DestinationPath '${zipPath}' -CompressionLevel Optimal -Force"`,
      { stdio: 'ignore' }
    );
    // Rename to .tar.gz so the naming is consistent (extractArchive handles both)
    fs.renameSync(zipPath, archivePath);
    warn('Used ZIP format (tar not available). Archive is still cross-platform compatible.');
  } else {
    error('tar is required but not found. Install it with your package manager.');
  }
}

function extractArchive(archivePath, destDir) {
  fs.mkdirSync(destDir, { recursive: true });

  // Try tar first (works on Win10+, macOS, Linux)
  if (hasTar()) {
    try {
      execSync(`tar -xzf "${archivePath}" -C "${destDir}"`, { stdio: 'ignore' });
      return;
    } catch {} // Might be a zip renamed as .tar.gz
  }

  // Fallback: try as zip
  if (IS_WIN) {
    try {
      execSync(
        `powershell -NoProfile -Command "Expand-Archive -Path '${archivePath}' -DestinationPath '${destDir}' -Force"`,
        { stdio: 'ignore' }
      );
      return;
    } catch {}
  } else {
    try {
      execSync(`unzip -o "${archivePath}" -d "${destDir}"`, { stdio: 'ignore' });
      return;
    } catch {}
  }

  error('Could not extract archive. Ensure tar or zip tools are available.');
}

// ── BACKUP ──────────────────────────────────────────────────────────────────
async function doBackup() {
  const outputDir = flagVal('--output-dir', DEFAULT_BACKUP_DIR);
  if (!fs.existsSync(OPENCLAW_DIR)) error(`OpenClaw directory not found: ${OPENCLAW_DIR}`);

  fs.mkdirSync(outputDir, { recursive: true });

  const ts = timestamp();
  const agentName = getAgentName();
  const backupName = `openclaw-backup_${agentName}_${ts}`;
  const stagingDir = path.join(os.tmpdir(), backupName);
  const archivePath = path.join(outputDir, `${backupName}.tar.gz`);

  console.log('');
  console.log('🦞 OpenClaw Backup');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`Platform:  ${process.platform} (${os.arch()})`);
  console.log(`Source:    ${OPENCLAW_DIR}`);
  console.log(`Output:    ${archivePath}`);
  console.log('');

  fs.mkdirSync(stagingDir, { recursive: true });

  try {
    // ── 1. Main workspace (filtered) ──────────────────────────────────────
    info('Backing up workspace...');
    const wsStats = copyDirFiltered(
      path.join(OPENCLAW_DIR, 'workspace'),
      path.join(stagingDir, 'workspace')
    );
    info(`  workspace → ${wsStats.files} files (${formatSize(wsStats.bytes)})`);

    // ── 2. Extra workspace-* directories (multi-agent teams, etc.) ────────
    const extraWorkspaces = discoverWorkspaceDirs();
    if (extraWorkspaces.length > 0) {
      info(`Backing up ${extraWorkspaces.length} extra workspace(s)...`);
      for (const ws of extraWorkspaces) {
        const st = copyDirFiltered(
          path.join(OPENCLAW_DIR, ws),
          path.join(stagingDir, ws)
        );
        info(`  ${ws} → ${st.files} files (${formatSize(st.bytes)})`);
      }
    }

    // ── 3. Gateway config (openclaw.json — contains bot tokens, API keys) ─
    info('Backing up Gateway config...');
    fs.mkdirSync(path.join(stagingDir, 'config'), { recursive: true });
    const configFile = path.join(OPENCLAW_DIR, 'openclaw.json');
    if (fs.existsSync(configFile)) {
      fs.copyFileSync(configFile, path.join(stagingDir, 'config', 'openclaw.json'));
      info(`  openclaw.json → ${formatSize(fs.statSync(configFile).size)}`);
    } else {
      warn('  openclaw.json not found, skipping');
    }
    const bakFile = configFile + '.bak';
    if (fs.existsSync(bakFile)) {
      fs.copyFileSync(bakFile, path.join(stagingDir, 'config', 'openclaw.json.bak'));
    }

    // ── 4. System skills ──────────────────────────────────────────────────
    info('Backing up system skills...');
    const skillsDir = path.join(OPENCLAW_DIR, 'skills');
    if (fs.existsSync(skillsDir)) {
      copyDirAll(skillsDir, path.join(stagingDir, 'skills'));
      info(`  skills → ${countFiles(path.join(stagingDir, 'skills'))} files`);
    } else {
      warn('  no system skills found');
    }

    // ── 5. Extensions (feishu, etc.) ──────────────────────────────────────
    info('Backing up extensions...');
    const extDir = path.join(OPENCLAW_DIR, 'extensions');
    if (fs.existsSync(extDir)) {
      copyDirAll(extDir, path.join(stagingDir, 'extensions'));
      info(`  extensions → ${countFiles(path.join(stagingDir, 'extensions'))} files`);
    }

    // ── 6. Credentials & channel pairing state ───────────────────────────
    info('Backing up credentials & channel state...');
    const credsDir = path.join(OPENCLAW_DIR, 'credentials');
    if (fs.existsSync(credsDir)) {
      copyDirAll(credsDir, path.join(stagingDir, 'credentials'));
      info('  credentials → backed up');
    }

    // Auto-discover channel directories
    const channels = discoverChannelDirs();
    for (const chan of channels) {
      copyDirAll(path.join(OPENCLAW_DIR, chan), path.join(stagingDir, 'channels', chan));
      info(`  channel state: ${chan}`);
    }

    // ── 7. Agents (config + session history, filtered) ────────────────────
    info('Backing up agent config & sessions...');
    const agentsDir = path.join(OPENCLAW_DIR, 'agents');
    if (fs.existsSync(agentsDir)) {
      copyDirFiltered(agentsDir, path.join(stagingDir, 'agents'));
      info('  agents → backed up');
    }

    // ── 8. Devices (paired nodes/phones) ──────────────────────────────────
    info('Backing up devices...');
    const devicesDir = path.join(OPENCLAW_DIR, 'devices');
    if (fs.existsSync(devicesDir)) {
      copyDirAll(devicesDir, path.join(stagingDir, 'devices'));
      info('  devices → backed up');
    }

    // ── 9. Identity ──────────────────────────────────────────────────────
    info('Backing up identity...');
    const identityDir = path.join(OPENCLAW_DIR, 'identity');
    if (fs.existsSync(identityDir)) {
      copyDirAll(identityDir, path.join(stagingDir, 'identity'));
      info('  identity → backed up');
    }

    // ── 10. Scripts (guardian.sh, gw-watchdog.sh — Linux/Mac portability) ─
    info('Backing up scripts...');
    fs.mkdirSync(path.join(stagingDir, 'scripts'), { recursive: true });
    for (const f of ['guardian.sh', 'gw-watchdog.sh', 'start-gateway.sh']) {
      const fp = path.join(OPENCLAW_DIR, f);
      if (fs.existsSync(fp)) fs.copyFileSync(fp, path.join(stagingDir, 'scripts', f));
    }

    // ── 11. Cron jobs ────────────────────────────────────────────────────
    info('Backing up cron jobs...');
    const cronDir = path.join(OPENCLAW_DIR, 'cron');
    if (fs.existsSync(cronDir)) {
      copyDirAll(cronDir, path.join(stagingDir, 'cron'));
      info('  cron → backed up');
    }

    // ── 12. ClawHub registry data ────────────────────────────────────────
    const clawhubDir = path.join(OPENCLAW_DIR, '.clawhub');
    if (fs.existsSync(clawhubDir)) {
      copyDirAll(clawhubDir, path.join(stagingDir, '.clawhub'));
      info('  .clawhub → backed up');
    }

    // ── 13. Delivery queue ───────────────────────────────────────────────
    const dqDir = path.join(OPENCLAW_DIR, 'delivery-queue');
    if (fs.existsSync(dqDir)) {
      copyDirAll(dqDir, path.join(stagingDir, 'delivery-queue'));
      info('  delivery-queue → backed up');
    }

    // ── 14. Memory (qmd index) ───────────────────────────────────────────
    const memDir = path.join(OPENCLAW_DIR, 'memory');
    if (fs.existsSync(memDir)) {
      copyDirAll(memDir, path.join(stagingDir, 'memory'));
      info('  memory index → backed up');
    }

    // ── 15. Manifest (metadata for restore inspection) ───────────────────
    const manifest = {
      backup_name: backupName,
      agent_name: agentName,
      timestamp: ts,
      created_at: new Date().toISOString(),
      hostname: os.hostname(),
      platform: process.platform,
      arch: os.arch(),
      node_version: process.version,
      openclaw_home: OPENCLAW_DIR,
      openclaw_version: getOpenClawVersion(),
      backup_tool_version: VERSION,
      created_by: `openclaw-backup cross-platform v${VERSION}`,
      extra_workspaces: extraWorkspaces,
      channels_backed_up: channels,
      contents: {
        workspace: fs.existsSync(path.join(stagingDir, 'workspace')),
        extra_workspaces: extraWorkspaces.length > 0,
        gateway_config: fs.existsSync(path.join(stagingDir, 'config', 'openclaw.json')),
        skills: fs.existsSync(path.join(stagingDir, 'skills')),
        extensions: fs.existsSync(path.join(stagingDir, 'extensions')),
        credentials: fs.existsSync(path.join(stagingDir, 'credentials')),
        channel_state: channels.length > 0,
        agents: fs.existsSync(path.join(stagingDir, 'agents')),
        devices: fs.existsSync(path.join(stagingDir, 'devices')),
        identity: fs.existsSync(path.join(stagingDir, 'identity')),
        guardian_scripts: true,
        cron_jobs: fs.existsSync(path.join(stagingDir, 'cron')),
        clawhub: fs.existsSync(path.join(stagingDir, '.clawhub')),
        delivery_queue: fs.existsSync(path.join(stagingDir, 'delivery-queue')),
        memory_index: fs.existsSync(path.join(stagingDir, 'memory')),
      },
      notes: 'Cross-platform backup. Compatible with Windows/macOS/Linux. Contains credentials and API keys — keep secure.',
    };
    fs.writeFileSync(path.join(stagingDir, 'MANIFEST.json'), JSON.stringify(manifest, null, 2));

    // ── 16. Package ──────────────────────────────────────────────────────
    console.log('');
    info('Packaging...');
    createArchive(stagingDir, archivePath);

    // Security: restrictive permissions on archive (contains secrets)
    harden(archivePath, 0o600);

    const archiveSize = fs.statSync(archivePath).size;
    const totalFiles = countFiles(stagingDir);

    console.log('');
    console.log(`${c.green('✅')} Backup complete!`);
    console.log(`   Archive:  ${archivePath}`);
    console.log(`   Size:     ${formatSize(archiveSize)}`);
    console.log(`   Files:    ${totalFiles}`);
    console.log(`   Platform: ${process.platform}/${os.arch()}`);
    if (extraWorkspaces.length > 0) {
      console.log(`   Extra workspaces: ${extraWorkspaces.join(', ')}`);
    }
    console.log('');
    console.log(c.cyan('To restore on any machine (Windows/macOS/Linux):'));
    console.log(c.dim(`   node backup-restore.js restore "${path.basename(archivePath)}" --dry-run`));
    console.log(c.dim(`   node backup-restore.js restore "${path.basename(archivePath)}"`));
    console.log('');
    warn('Archive contains credentials & API keys — store securely.');
    if (!IS_WIN) info('Permissions: chmod 600 applied to archive.');

    // ── 17. Prune old backups (keep last MAX_BACKUPS) ────────────────────
    const backups = fs.readdirSync(outputDir)
      .filter(f => f.startsWith('openclaw-backup_') && (f.endsWith('.tar.gz') || f.endsWith('.zip')))
      .sort().reverse();
    if (backups.length > MAX_BACKUPS) {
      const toRemove = backups.slice(MAX_BACKUPS);
      toRemove.forEach(f => {
        try { fs.unlinkSync(path.join(outputDir, f)); } catch {}
      });
      info(`Pruned ${toRemove.length} old backup(s) (keeping last ${MAX_BACKUPS})`);
    }

    return { archivePath, archiveSize, totalFiles, backupName };

  } finally {
    rmrf(stagingDir);
  }
}

// ── RESTORE ─────────────────────────────────────────────────────────────────
async function doRestore() {
  let archive = args[1];
  const isDryRun = flag('--dry-run');
  const overwriteToken = flag('--overwrite-gateway-token');

  if (!archive) error('Usage: node backup-restore.js restore <archive> [--dry-run] [--overwrite-gateway-token]');

  // Find archive file
  if (!fs.existsSync(archive)) {
    const tryPath = path.join(DEFAULT_BACKUP_DIR, archive);
    if (fs.existsSync(tryPath)) archive = tryPath;
    else error(`Archive not found: ${archive}`);
  }
  archive = path.resolve(archive);

  console.log('');
  console.log(`🦞 OpenClaw Restore ${isDryRun ? c.cyan('(DRY RUN)') : ''}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`Archive:   ${archive}`);
  console.log(`Target:    ${OPENCLAW_DIR}`);
  console.log(`Platform:  ${process.platform} (${os.arch()})`);
  console.log('');

  // Extract to temp
  const ts = timestamp();
  const extractDir = path.join(os.tmpdir(), `openclaw-restore-${ts}`);

  try {
    info('Extracting archive...');
    extractArchive(archive, extractDir);

    // Find backup dir inside — supports multiple archive structures
    let backupDir = null;

    // Standard: openclaw-backup_xxx/ at top level
    for (const entry of fs.readdirSync(extractDir, { withFileTypes: true })) {
      if (entry.isDirectory() && entry.name.startsWith('openclaw-backup_')) {
        backupDir = path.join(extractDir, entry.name);
        break;
      }
    }
    // Direct: MANIFEST.json at top level
    if (!backupDir && fs.existsSync(path.join(extractDir, 'MANIFEST.json'))) {
      backupDir = extractDir;
    }
    // Legacy: .openclaw/ at top level (v1 bash backups)
    if (!backupDir) {
      const ocDir = path.join(extractDir, '.openclaw');
      if (fs.existsSync(ocDir)) {
        backupDir = extractDir;
        if (!fs.existsSync(path.join(extractDir, 'workspace')) && fs.existsSync(path.join(ocDir, 'workspace'))) {
          for (const entry of fs.readdirSync(ocDir, { withFileTypes: true })) {
            const src = path.join(ocDir, entry.name);
            const dest = path.join(extractDir, entry.name);
            try { fs.renameSync(src, dest); } catch {}
          }
        }
      }
    }
    if (!backupDir) error('Invalid archive: could not find backup data');

    // Show manifest
    const manifestFile = path.join(backupDir, 'MANIFEST.json');
    let manifest = {};
    if (fs.existsSync(manifestFile)) {
      manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'));
      console.log('📋 Manifest:');
      console.log(`  Backup:     ${manifest.backup_name || 'unknown'}`);
      console.log(`  Agent:      ${manifest.agent_name || 'unknown'}`);
      console.log(`  Created:    ${manifest.created_at || manifest.timestamp || 'unknown'}`);
      console.log(`  From:       ${manifest.hostname || 'unknown'} (${manifest.platform || 'unknown'}/${manifest.arch || 'unknown'})`);
      console.log(`  OC version: ${manifest.openclaw_version || 'unknown'}`);
      console.log(`  Tool ver:   ${manifest.backup_tool_version || 'v1.x (legacy)'}`);
      if (manifest.extra_workspaces && manifest.extra_workspaces.length > 0) {
        console.log(`  Extra WS:   ${manifest.extra_workspaces.join(', ')}`);
      }
      if (manifest.channels_backed_up && manifest.channels_backed_up.length > 0) {
        console.log(`  Channels:   ${manifest.channels_backed_up.join(', ')}`);
      }
      const hasCreds = manifest.contents?.credentials;
      console.log(`  Credentials: ${hasCreds ? 'included ✓' : 'NOT included (old backup)'}`);
      console.log('');
    }

    // Show contents
    const totalFiles = countFiles(backupDir);
    info(`Archive contains: ${totalFiles} files`);

    const dirs = fs.readdirSync(backupDir, { withFileTypes: true }).filter(e => e.isDirectory());
    console.log('');
    console.log('Contents:');
    for (const d of dirs) {
      const dc = countFiles(path.join(backupDir, d.name));
      console.log(`  📁 ${d.name}/ (${dc} files)`);
    }

    // Key files check
    console.log('');
    console.log('Key files:');
    const keyFiles = [
      ['workspace/MEMORY.md', 'Agent memory'],
      ['workspace/SOUL.md', 'Agent personality'],
      ['workspace/USER.md', 'User info'],
      ['config/openclaw.json', 'Gateway config'],
    ];
    for (const [kf, desc] of keyFiles) {
      const fp = path.join(backupDir, kf);
      if (fs.existsSync(fp)) {
        console.log(`  ${c.green('✓')} ${kf} (${desc}, ${formatSize(fs.statSync(fp).size)})`);
      } else {
        console.log(`  ${c.dim('✗')} ${kf} (${desc}) — not in backup`);
      }
    }

    // ── Gateway token strategy ──────────────────────────────────────────
    let currentToken = null;
    const currentConfig = path.join(OPENCLAW_DIR, 'openclaw.json');
    if (fs.existsSync(currentConfig)) {
      try {
        const cfg = JSON.parse(fs.readFileSync(currentConfig, 'utf8'));
        currentToken = cfg?.gateway?.auth?.token;
      } catch {}
    }

    console.log('');
    console.log('🔑 Gateway Token Strategy:');
    if (overwriteToken) {
      warn('  --overwrite-gateway-token: backup token will replace current');
      warn('  You may need to update Control UI / Dashboard with the restored token');
    } else if (currentToken) {
      info(`  Current server token preserved (${currentToken.substring(0, 8)}...${currentToken.slice(-4)})`);
      console.log('  Control UI / Dashboard will continue working without changes');
    } else {
      warn('  No current token — backup token will be used as-is');
    }

    // Existing data check
    if (fs.existsSync(OPENCLAW_DIR)) {
      const existingFiles = countFiles(OPENCLAW_DIR);
      console.log('');
      warn(`Existing ${OPENCLAW_DIR} has ${existingFiles} files — will be overwritten`);
    }

    if (isDryRun) {
      console.log('');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log(`${c.cyan('🔍')} DRY RUN — no changes made.`);
      console.log('   Review the above, then run without --dry-run to apply.');
      console.log(c.dim(`   node backup-restore.js restore "${path.basename(archive)}"`));
      return;
    }

    // ── Interactive confirmation ─────────────────────────────────────────
    console.log('');
    console.log(c.red('⚠️  WARNING: This will OVERWRITE ~/.openclaw/ with backup data.'));
    console.log(`   Backup:  ${path.basename(archive)}`);
    console.log(`   Target:  ${OPENCLAW_DIR}`);
    if (currentToken && !overwriteToken) {
      console.log(`   ${c.green('Gateway token: preserved (this server\'s token kept)')}`);
    }
    console.log('');
    const confirm = await ask("   Type 'yes' to confirm: ");
    if (confirm !== 'yes') { console.log('Cancelled.'); return; }
    console.log('');

    // ── Pre-restore snapshot (safety net) ────────────────────────────────
    let preArchive = null;
    if (fs.existsSync(OPENCLAW_DIR)) {
      const preBackupDir = DEFAULT_BACKUP_DIR;
      fs.mkdirSync(preBackupDir, { recursive: true });
      preArchive = path.join(preBackupDir, `pre-restore_${ts}.tar.gz`);
      warn('Saving pre-restore snapshot...');
      try {
        createArchive(OPENCLAW_DIR, preArchive);
        harden(preArchive, 0o600);
        info(`  Saved: ${preArchive}`);
      } catch (e) {
        warn(`  Pre-restore backup failed (continuing): ${e.message}`);
        preArchive = null;
      }
    }

    // ── Stop gateway before restore ──────────────────────────────────────
    warn('Stopping OpenClaw Gateway...');
    try {
      const stopCmd = IS_WIN ? 'cmd /c "openclaw gateway stop"' : 'openclaw gateway stop';
      execSync(stopCmd, { stdio: 'ignore', timeout: 10000 });
    } catch {} // May not be running

    // ── Restore helper ───────────────────────────────────────────────────
    const restoreDir = (src, dest) => {
      if (!fs.existsSync(src)) return false;
      fs.mkdirSync(dest, { recursive: true });
      copyDirAll(src, dest);
      return true;
    };

    // 1. Main workspace
    info('Restoring workspace...');
    restoreDir(path.join(backupDir, 'workspace'), path.join(OPENCLAW_DIR, 'workspace'));

    // 2. Extra workspace-* directories
    for (const entry of fs.readdirSync(backupDir, { withFileTypes: true })) {
      if (entry.isDirectory() && entry.name.startsWith('workspace-')) {
        info(`Restoring ${entry.name}...`);
        restoreDir(path.join(backupDir, entry.name), path.join(OPENCLAW_DIR, entry.name));
      }
    }

    // 3. Gateway config
    info('Restoring Gateway config...');
    const backupConfig = path.join(backupDir, 'config', 'openclaw.json');
    if (fs.existsSync(backupConfig)) {
      fs.mkdirSync(OPENCLAW_DIR, { recursive: true });
      fs.copyFileSync(backupConfig, path.join(OPENCLAW_DIR, 'openclaw.json'));

      // Preserve gateway token (prevents Control UI mismatch on migration)
      if (currentToken && !overwriteToken) {
        try {
          const cfgPath = path.join(OPENCLAW_DIR, 'openclaw.json');
          const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
          if (!cfg.gateway) cfg.gateway = {};
          if (!cfg.gateway.auth) cfg.gateway.auth = {};
          cfg.gateway.auth.token = currentToken;
          fs.writeFileSync(cfgPath, JSON.stringify(cfg, null, 2));
          info(`  Gateway token preserved (${currentToken.substring(0, 8)}...)`);
        } catch (e) {
          warn(`  Could not preserve gateway token: ${e.message}`);
        }
      } else {
        info('  openclaw.json restored (gateway token from backup)');
      }
    }
    const backupConfigBak = path.join(backupDir, 'config', 'openclaw.json.bak');
    if (fs.existsSync(backupConfigBak)) {
      fs.copyFileSync(backupConfigBak, path.join(OPENCLAW_DIR, 'openclaw.json.bak'));
    }

    // 4. Skills
    info('Restoring skills...');
    restoreDir(path.join(backupDir, 'skills'), path.join(OPENCLAW_DIR, 'skills'));
    // v2 legacy: skills were under skills/system/
    if (fs.existsSync(path.join(backupDir, 'skills', 'system'))) {
      restoreDir(path.join(backupDir, 'skills', 'system'), path.join(OPENCLAW_DIR, 'skills'));
    }

    // 5. Extensions
    info('Restoring extensions...');
    restoreDir(path.join(backupDir, 'extensions'), path.join(OPENCLAW_DIR, 'extensions'));

    // 6. Credentials (with hardened permissions on non-Windows)
    info('Restoring credentials...');
    const credsRestored = restoreDir(path.join(backupDir, 'credentials'), path.join(OPENCLAW_DIR, 'credentials'));
    if (credsRestored) {
      hardenDir(path.join(OPENCLAW_DIR, 'credentials'), 0o700, 0o600);
      if (!IS_WIN) info('  Credentials permissions hardened (700/600)');
    }

    // 7. Channel state
    info('Restoring channel state...');
    const chansDir = path.join(backupDir, 'channels');
    if (fs.existsSync(chansDir)) {
      for (const chan of fs.readdirSync(chansDir, { withFileTypes: true })) {
        if (chan.isDirectory()) {
          restoreDir(path.join(chansDir, chan.name), path.join(OPENCLAW_DIR, chan.name));
          info(`  channel: ${chan.name}`);
        }
      }
    }

    // 8. Agents
    info('Restoring agents...');
    restoreDir(path.join(backupDir, 'agents'), path.join(OPENCLAW_DIR, 'agents'));

    // 9. Devices
    info('Restoring devices...');
    restoreDir(path.join(backupDir, 'devices'), path.join(OPENCLAW_DIR, 'devices'));

    // 10. Identity
    info('Restoring identity...');
    restoreDir(path.join(backupDir, 'identity'), path.join(OPENCLAW_DIR, 'identity'));

    // 11. Scripts (guardian/watchdog — make executable on non-Windows)
    info('Restoring scripts...');
    const backupScripts = path.join(backupDir, 'scripts');
    if (fs.existsSync(backupScripts)) {
      for (const f of fs.readdirSync(backupScripts)) {
        const dest = path.join(OPENCLAW_DIR, f);
        fs.copyFileSync(path.join(backupScripts, f), dest);
        harden(dest, 0o755);
      }
    }

    // 12. Cron
    info('Restoring cron jobs...');
    restoreDir(path.join(backupDir, 'cron'), path.join(OPENCLAW_DIR, 'cron'));

    // 13. ClawHub
    restoreDir(path.join(backupDir, '.clawhub'), path.join(OPENCLAW_DIR, '.clawhub'));

    // 14. Delivery queue
    restoreDir(path.join(backupDir, 'delivery-queue'), path.join(OPENCLAW_DIR, 'delivery-queue'));

    // 15. Memory index
    restoreDir(path.join(backupDir, 'memory'), path.join(OPENCLAW_DIR, 'memory'));

    // ── Write restore-complete flag ──────────────────────────────────────
    const restoreFlag = {
      restored_at: new Date().toISOString(),
      backup_name: manifest.backup_name || path.basename(archive),
      agent_name: manifest.agent_name || 'unknown',
      source_platform: manifest.platform || 'unknown',
      restore_platform: process.platform,
      pre_restore_snapshot: preArchive || null,
    };
    try {
      const flagPath = path.join(OPENCLAW_DIR, 'workspace', '.restore-complete.json');
      fs.mkdirSync(path.dirname(flagPath), { recursive: true });
      fs.writeFileSync(flagPath, JSON.stringify(restoreFlag, null, 2));
    } catch {}

    // ── Restart gateway ──────────────────────────────────────────────────
    console.log('');
    info('Starting OpenClaw Gateway...');
    try {
      const startCmd = IS_WIN
        ? 'cmd /c "openclaw gateway start"'
        : (fs.existsSync(path.join(OPENCLAW_DIR, 'start-gateway.sh'))
          ? `bash "${path.join(OPENCLAW_DIR, 'start-gateway.sh')}" &`
          : 'openclaw gateway start');
      execSync(startCmd, { stdio: 'ignore', timeout: 15000 });
      info('  Gateway started');
    } catch {
      warn('  Could not auto-start gateway. Run manually: openclaw gateway start');
    }

    // ── Summary ──────────────────────────────────────────────────────────
    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`${c.green('✅')} Restore complete!`);
    if (preArchive) {
      console.log(`   Pre-restore snapshot: ${preArchive}`);
    }
    console.log('');

    if (currentToken && !overwriteToken) {
      console.log('🔑 Gateway token: preserved (this server\'s token kept)');
      console.log('   Control UI / Dashboard should connect without any changes.');
    } else {
      console.log('🔑 Gateway token: from backup');
      console.log('   ⚠️  If Control UI shows "token mismatch", check openclaw.json for the token.');
    }
    console.log('');
    console.log('📋 All channels should reconnect automatically.');
    console.log('   If Telegram is silent after 30s, send /start to your bot.');
    console.log(`   Verify: openclaw gateway status`);
    console.log('');

  } finally {
    rmrf(extractDir);
  }
}

// ── LIST ────────────────────────────────────────────────────────────────────
function doList() {
  const backupDir = flagVal('--backup-dir', DEFAULT_BACKUP_DIR);
  if (!fs.existsSync(backupDir)) { console.log(`No backups found at: ${backupDir}`); return; }

  const backups = fs.readdirSync(backupDir)
    .filter(f => f.startsWith('openclaw-backup_') || f.startsWith('pre-restore_'))
    .map(f => {
      try {
        const stat = fs.statSync(path.join(backupDir, f));
        return { name: f, size: stat.size, time: stat.mtime };
      } catch { return null; }
    })
    .filter(Boolean)
    .sort((a, b) => b.time - a.time);

  if (backups.length === 0) { console.log(`No backups in: ${backupDir}`); return; }

  console.log('');
  console.log('🦞 OpenClaw Backups');
  console.log(`Directory: ${backupDir}`);
  console.log('');
  for (const b of backups) {
    const age = Date.now() - b.time.getTime();
    const ageStr = age > 86400000 ? Math.floor(age / 86400000) + 'd ago'
                 : age > 3600000 ? Math.floor(age / 3600000) + 'h ago'
                 : Math.floor(age / 60000) + 'm ago';
    const icon = b.name.startsWith('pre-restore') ? '🔄' : '📦';
    console.log(`  ${icon} ${b.name}  ${formatSize(b.size)}  ${ageStr}`);
  }
  console.log('');
}

// ── MAIN ────────────────────────────────────────────────────────────────────
async function main() {
  switch (action) {
    case 'backup':  return doBackup();
    case 'restore': return doRestore();
    case 'list':    return doList();
    default:
      console.log(`
🦞 OpenClaw Backup & Restore v${VERSION}
   Cross-platform — Windows, macOS, and Linux

Usage:
  node backup-restore.js backup  [--output-dir <dir>]
  node backup-restore.js restore <archive> [--dry-run] [--overwrite-gateway-token]
  node backup-restore.js list    [--backup-dir <dir>]

Examples:
  node backup-restore.js backup
  node backup-restore.js restore openclaw-backup_mybot_20260307.tar.gz --dry-run
  node backup-restore.js restore openclaw-backup_mybot_20260307.tar.gz
  node backup-restore.js list

Default backup directory: ${DEFAULT_BACKUP_DIR}

Archive format: tar.gz (Win10+/macOS/Linux native), auto-fallback to ZIP on older Windows.
Backups created on any OS can be restored on any other OS.
`);
  }
}

// Export for programmatic use (server.js)
module.exports = { doBackup };

main().catch(e => { error(e.message); });
