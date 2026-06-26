#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

function usage() {
  console.log(`Usage:
  node scripts/install-global-skill.js --slug <skill-slug> [--agent <agent>] [--keep-staging] [--skip-backup] [--version <version>] [--openclaw-home <path>]

Behavior:
  1. Resolve the OpenClaw home from flags or env, then derive the agent workspace as <openclaw-home>/workspaces/<agent>
  2. Try 'openclaw skills update <slug> --agent <agent>'
  3. If update says the skill is not tracked, run 'openclaw skills install <slug> --agent <agent> --force'
  4. Verify staged .clawhub/origin.json
  5. Backup existing global copy unless --skip-backup
  6. Promote staged copy into <openclaw-home>/skills/<slug>
  7. Remove staging copy unless --keep-staging

Environment overrides:
  OPENCLAW_HOME              OpenClaw home directory that contains skills/
  OPENCLAW_AGENT             Agent name used for install/update, default: lan
`);
}

function parseArgs(argv) {
  const args = {
    agent: process.env.OPENCLAW_AGENT || 'lan',
    keepStaging: false,
    openclawHome: process.env.OPENCLAW_HOME || '',
    skipBackup: false,
    slug: '',
    version: '',
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--slug') args.slug = argv[++i] || '';
    else if (a === '--agent') args.agent = argv[++i] || '';
    else if (a === '--keep-staging') args.keepStaging = true;
    else if (a === '--openclaw-home') args.openclawHome = argv[++i] || '';
    else if (a === '--skip-backup') args.skipBackup = true;
    else if (a === '--version') args.version = argv[++i] || '';
    else if (a === '-h' || a === '--help') args.help = true;
    else throw new Error(`Unknown argument: ${a}`);
  }
  return args;
}

function run(cmd, args, opts = {}) {
  return execFileSync(cmd, args, {
    cwd: opts.cwd,
    encoding: 'utf8',
    stdio: opts.capture ? ['ignore', 'pipe', 'pipe'] : 'inherit',
  });
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function exists(p) {
  return fs.existsSync(p);
}

function resolveOpenClawHome(args) {
  if (args.openclawHome) {
    return path.resolve(args.openclawHome);
  }

  return path.resolve(process.env.OPENCLAW_HOME || path.join(os.homedir(), '.openclaw'));
}

function resolveWorkspaceRoot(args, openclawHome) {
  const resolved = path.resolve(path.join(openclawHome, 'workspaces', args.agent));

  if (!exists(resolved)) {
    throw new Error(
      `Workspace root does not exist: ${resolved}. ` +
      `This skill requires the workspace layout <openclaw-home>/workspaces/<agent>.`,
    );
  }

  return resolved;
}

function resolveLayout(args) {
  const openclawHome = resolveOpenClawHome(args);
  const workspaceRoot = resolveWorkspaceRoot(args, openclawHome);
  return {
    agent: args.agent,
    fileOutput: path.join(workspaceRoot, 'file_output'),
    globalRoot: path.join(openclawHome, 'skills'),
    openclawHome,
    stagingRoot: path.join(workspaceRoot, 'skills'),
    workspaceRoot,
  };
}

function timestamp() {
  return new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}Z$/, 'Z');
}

function backupGlobal(slug, globalDir, fileOutputDir, cwd) {
  ensureDir(fileOutputDir);
  const out = path.join(fileOutputDir, `${slug}-global-backup-${timestamp()}.tar.gz`);
  const py = [
    'import tarfile, sys',
    'src = sys.argv[1]',
    'dst = sys.argv[2]',
    'arc = sys.argv[3]',
    "with tarfile.open(dst, 'w:gz') as tf:",
    '    tf.add(src, arcname=arc, recursive=True)',
    'print(dst)',
  ].join('\n');
  run('python3', ['-c', py, globalDir, out, slug], { capture: true, cwd });
  return out;
}

function copyDir(src, dst) {
  fs.cpSync(src, dst, { recursive: true, force: true });
}

function removeDir(p) {
  fs.rmSync(p, { recursive: true, force: true });
}

function installOrUpdate(slug, version, layout) {
  try {
    const out = run('openclaw', ['skills', 'update', slug, '--agent', layout.agent], {
      capture: true,
      cwd: layout.workspaceRoot,
    });
    return { method: 'update', output: out };
  } catch (err) {
    const stdout = err.stdout ? String(err.stdout) : '';
    const stderr = err.stderr ? String(err.stderr) : '';
    const merged = `${stdout}\n${stderr}`;
    if (/not tracked as a ClawHub install/i.test(merged)) {
      const args = ['skills', 'install', slug, '--agent', layout.agent, '--force'];
      if (version) args.push('--version', version);
      const out = run('openclaw', args, { capture: true, cwd: layout.workspaceRoot });
      return { method: 'install', output: out };
    }
    throw new Error(`Skill update failed:\n${merged || err.message}`);
  }
}

function main() {
  const args = parseArgs(process.argv);
  if (args.help || !args.slug) {
    usage();
    process.exit(args.help ? 0 : 1);
  }

  if (!args.agent) {
    throw new Error('Agent name is required. Use --agent <name> or set OPENCLAW_AGENT.');
  }

  const layout = resolveLayout(args);
  const slug = args.slug;
  const stagedDir = path.join(layout.stagingRoot, slug);
  const globalDir = path.join(layout.globalRoot, slug);
  const tempGlobalDir = `${globalDir}.tmp`;

  const result = installOrUpdate(slug, args.version, layout);

  const stagedOrigin = path.join(stagedDir, '.clawhub', 'origin.json');
  if (!exists(stagedOrigin)) {
    throw new Error(`Staged skill missing origin file: ${stagedOrigin}`);
  }
  const stagedMeta = readJson(stagedOrigin);

  let backupPath = null;
  if (exists(globalDir) && !args.skipBackup) {
    backupPath = backupGlobal(slug, globalDir, layout.fileOutput, layout.workspaceRoot);
  }

  ensureDir(layout.globalRoot);
  removeDir(tempGlobalDir);
  copyDir(stagedDir, tempGlobalDir);
  removeDir(globalDir);
  fs.renameSync(tempGlobalDir, globalDir);

  const globalOrigin = path.join(globalDir, '.clawhub', 'origin.json');
  if (!exists(globalOrigin)) {
    throw new Error(`Global skill missing origin file after promotion: ${globalOrigin}`);
  }
  const globalMeta = readJson(globalOrigin);
  if (globalMeta.installedVersion !== stagedMeta.installedVersion) {
    throw new Error(`Version mismatch after promotion: staged=${stagedMeta.installedVersion}, global=${globalMeta.installedVersion}`);
  }

  if (!args.keepStaging) {
    removeDir(stagedDir);
  }

  const summary = {
    agent: layout.agent,
    slug,
    method: result.method,
    installedVersion: globalMeta.installedVersion || null,
    openclawHome: layout.openclawHome,
    globalPath: globalDir,
    workspaceRoot: layout.workspaceRoot,
    backupPath,
    stagingRemoved: !args.keepStaging,
  };
  console.log(JSON.stringify(summary, null, 2));
}

main();
