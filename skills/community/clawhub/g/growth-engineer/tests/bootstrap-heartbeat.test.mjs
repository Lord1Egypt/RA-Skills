import assert from 'node:assert/strict';
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';

const skillRoot = resolve(import.meta.dirname, '..');
const bootstrap = join(skillRoot, 'scripts', 'bootstrap-openclaw-workspace.sh');

function runBootstrap(workspace) {
  return spawnSync('bash', [bootstrap], {
    env: {
      ...process.env,
      OPENCLAW_GROWTH_WORKSPACE: workspace,
      OPENCLAW_GROWTH_BOOTSTRAP_SKIP_UPDATE: '1',
      OPENCLAW_GROWTH_SKIP_ANALYTICSCLI_UPDATE: '1',
    },
    encoding: 'utf8',
  });
}

test('bootstrap can refresh runtime and hand off to the local wizard in one command', () => {
  const workspace = mkdtempSync(join(tmpdir(), 'openclaw-bootstrap-wizard-'));

  try {
    const result = spawnSync('bash', [bootstrap, '--wizard', '--help'], {
      env: {
        ...process.env,
        OPENCLAW_GROWTH_WORKSPACE: workspace,
        OPENCLAW_GROWTH_BOOTSTRAP_SKIP_UPDATE: '1',
        OPENCLAW_GROWTH_SKIP_ANALYTICSCLI_UPDATE: '1',
      },
      encoding: 'utf8',
    });
    assert.equal(result.status, 0, `${result.stderr}\n${result.stdout}`);
    assert.match(result.stdout, /Copied openclaw-growth-engineer runtime into workspace/);
    assert.match(result.stdout, /Starting Growth Engineer wizard/);
    assert.match(result.stdout, /OpenClaw Growth Setup Wizard/);
    assert.match(result.stdout, /npx -y @analyticscli\/growth-engineer wizard --connectors/);
  } finally {
    rmSync(workspace, { recursive: true, force: true });
  }
});

test('bootstrap writes an actionable OpenClaw heartbeat task for empty workspaces', () => {
  const workspace = mkdtempSync(join(tmpdir(), 'openclaw-heartbeat-'));

  try {
    const result = runBootstrap(workspace);
    assert.equal(result.status, 0, `${result.stderr}\n${result.stdout}`);

    const heartbeat = readFileSync(join(workspace, 'HEARTBEAT.md'), 'utf8');
    assert.match(heartbeat, /tasks:/);
    assert.match(heartbeat, /name: openclaw-growth-engineer-run/);
    assert.match(heartbeat, /interval: 6h/);
    assert.match(heartbeat, /node scripts\/openclaw-growth-runner\.mjs --config data\/openclaw-growth-engineer\/config\.json/);
    assert.match(heartbeat, /--state data\/openclaw-growth-engineer\/state\.json/);
    assert.match(heartbeat, /ASC\/App Store Connect is a Growth Engineer local CLI connector, not a chat tool/);
    assert.match(heartbeat, /never answer no because no Apple tool is callable/);
    assert.match(heartbeat, /answer exactly: Yes\. ASC analytics is connected through Growth Engineer local asc CLI\/API-key setup/);
    assert.match(heartbeat, /openclaw-growth-status\.mjs --config data\/openclaw-growth-engineer\/config\.json --json --only-connectors asc/);
    assert.match(heartbeat, /HEARTBEAT_OK/);
  } finally {
    rmSync(workspace, { recursive: true, force: true });
  }
});

test('bootstrap repairs comment-only HEARTBEAT.md files', () => {
  const workspace = mkdtempSync(join(tmpdir(), 'openclaw-heartbeat-'));

  try {
    writeFileSync(join(workspace, 'HEARTBEAT.md'), '# Keep this file empty to skip heartbeat API calls.\n');

    const result = runBootstrap(workspace);
    assert.equal(result.status, 0, `${result.stderr}\n${result.stdout}`);

    const heartbeat = readFileSync(join(workspace, 'HEARTBEAT.md'), 'utf8');
    assert.match(heartbeat, /tasks:/);
    assert.match(heartbeat, /name: openclaw-growth-engineer-run/);
    assert.match(heartbeat, /interval: 6h/);
  } finally {
    rmSync(workspace, { recursive: true, force: true });
  }
});

test('bootstrap updates existing managed HEARTBEAT.md blocks to the current 6h cadence', () => {
  const workspace = mkdtempSync(join(tmpdir(), 'openclaw-heartbeat-'));

  try {
    writeFileSync(
      join(workspace, 'HEARTBEAT.md'),
      `# OpenClaw heartbeat checklist

<!-- openclaw-growth-engineer:start -->
tasks:

- name: openclaw-growth-engineer-run
  interval: 1d
  prompt: "old prompt"
<!-- openclaw-growth-engineer:end -->
`,
    );

    const result = runBootstrap(workspace);
    assert.equal(result.status, 0, `${result.stderr}\n${result.stdout}`);

    const heartbeat = readFileSync(join(workspace, 'HEARTBEAT.md'), 'utf8');
    assert.match(heartbeat, /interval: 6h/);
    assert.doesNotMatch(heartbeat, /interval: 1d/);
    assert.match(heartbeat, /connectorHealthCheckIntervalMinutes/);
  } finally {
    rmSync(workspace, { recursive: true, force: true });
  }
});

test('bootstrap supports canonical ClawHub growth-engineer install slug', () => {
  const workspace = mkdtempSync(join(tmpdir(), 'openclaw-heartbeat-'));
  const installedScriptDir = join(workspace, 'skills', 'growth-engineer', 'scripts');
  const installedBootstrap = join(installedScriptDir, 'bootstrap-openclaw-workspace.sh');

  try {
    mkdirSync(installedScriptDir, { recursive: true });
    copyFileSync(bootstrap, installedBootstrap);

    const result = spawnSync('bash', [installedBootstrap], {
      env: {
        ...process.env,
        OPENCLAW_GROWTH_BOOTSTRAP_SKIP_UPDATE: '1',
        OPENCLAW_GROWTH_SKIP_ANALYTICSCLI_UPDATE: '1',
      },
      encoding: 'utf8',
    });
    assert.equal(result.status, 0, `${result.stderr}\n${result.stdout}`);

    const heartbeat = readFileSync(join(workspace, 'HEARTBEAT.md'), 'utf8');
    assert.match(heartbeat, /tasks:/);
    assert.match(heartbeat, /name: openclaw-growth-engineer-run/);
    assert.match(heartbeat, /interval: 6h/);
    assert.match(heartbeat, /node scripts\/openclaw-growth-runner\.mjs --config data\/openclaw-growth-engineer\/config\.json/);
    assert.match(heartbeat, /--state data\/openclaw-growth-engineer\/state\.json/);
  } finally {
    rmSync(workspace, { recursive: true, force: true });
  }
});

test('bootstrap points heartbeat at legacy home config when workspace config is missing', () => {
  const workspace = mkdtempSync(join(tmpdir(), 'openclaw-heartbeat-'));
  const home = mkdtempSync(join(tmpdir(), 'openclaw-home-'));
  const legacyConfigDir = join(home, 'data', 'openclaw-growth-engineer');
  const legacyConfigPath = join(legacyConfigDir, 'config.json');

  try {
    mkdirSync(legacyConfigDir, { recursive: true });
    writeFileSync(legacyConfigPath, '{"version":1}\n');

    const result = spawnSync('bash', [bootstrap], {
      env: {
        ...process.env,
        HOME: home,
        OPENCLAW_GROWTH_WORKSPACE: workspace,
        OPENCLAW_GROWTH_BOOTSTRAP_SKIP_UPDATE: '1',
        OPENCLAW_GROWTH_SKIP_ANALYTICSCLI_UPDATE: '1',
      },
      encoding: 'utf8',
    });
    assert.equal(result.status, 0, `${result.stderr}\n${result.stdout}`);

    const heartbeat = readFileSync(join(workspace, 'HEARTBEAT.md'), 'utf8');
    assert.match(heartbeat, /name: openclaw-growth-engineer-run/);
    assert.match(heartbeat, new RegExp(`--config ${legacyConfigPath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
    assert.match(heartbeat, new RegExp(`--state ${join(legacyConfigDir, 'state.json').replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
  } finally {
    rmSync(workspace, { recursive: true, force: true });
    rmSync(home, { recursive: true, force: true });
  }
});

test('bootstrap prefers legacy home config with state over workspace config', () => {
  const workspace = mkdtempSync(join(tmpdir(), 'openclaw-heartbeat-'));
  const home = mkdtempSync(join(tmpdir(), 'openclaw-home-'));
  const workspaceConfigDir = join(workspace, 'data', 'openclaw-growth-engineer');
  const legacyConfigDir = join(home, 'data', 'openclaw-growth-engineer');
  const legacyConfigPath = join(legacyConfigDir, 'config.json');

  try {
    mkdirSync(workspaceConfigDir, { recursive: true });
    mkdirSync(legacyConfigDir, { recursive: true });
    writeFileSync(join(workspaceConfigDir, 'config.json'), '{"version":"workspace"}\n');
    writeFileSync(legacyConfigPath, '{"version":"legacy"}\n');
    writeFileSync(join(legacyConfigDir, 'state.json'), '{"lastRunAt":"2026-05-13T00:00:00.000Z"}\n');

    const result = spawnSync('bash', [bootstrap], {
      env: {
        ...process.env,
        HOME: home,
        OPENCLAW_GROWTH_WORKSPACE: workspace,
        OPENCLAW_GROWTH_BOOTSTRAP_SKIP_UPDATE: '1',
        OPENCLAW_GROWTH_SKIP_ANALYTICSCLI_UPDATE: '1',
      },
      encoding: 'utf8',
    });
    assert.equal(result.status, 0, `${result.stderr}\n${result.stdout}`);

    const heartbeat = readFileSync(join(workspace, 'HEARTBEAT.md'), 'utf8');
    assert.match(heartbeat, new RegExp(`--config ${legacyConfigPath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
    assert.match(heartbeat, new RegExp(`--state ${join(legacyConfigDir, 'state.json').replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
  } finally {
    rmSync(workspace, { recursive: true, force: true });
    rmSync(home, { recursive: true, force: true });
  }
});

test('bootstrap updates AnalyticsCLI when feedback summary support is missing', () => {
  const source = readFileSync(bootstrap, 'utf8');

  assert.match(source, /OPENCLAW_GROWTH_SKIP_ANALYTICSCLI_UPDATE/);
  assert.match(source, /analyticscli feedback summary --help/);
  assert.match(source, /install-analyticscli-cli\.sh/);
  assert.match(source, /Ensuring AnalyticsCLI CLI supports feedback summaries/);
});
