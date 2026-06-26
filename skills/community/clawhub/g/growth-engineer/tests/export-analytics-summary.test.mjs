import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';

const skillRoot = resolve(import.meta.dirname, '..');
const exporter = join(skillRoot, 'scripts', 'export-analytics-summary.mjs');

test('export-analytics-summary passes the wizard token to analyticscli commands', () => {
  const tempDir = mkdtempSync(join(tmpdir(), 'openclaw-analytics-export-'));
  const fakeBin = join(tempDir, 'bin');
  const fakeAnalyticsCli = join(fakeBin, 'analyticscli');
  mkdirSync(fakeBin, { recursive: true });
  writeFileSync(
    fakeAnalyticsCli,
    `#!/usr/bin/env bash
set -euo pipefail

if [[ "\${ANALYTICSCLI_ACCESS_TOKEN:-}" != "fresh-token" ]]; then
  echo '{"error":{"code":"UNAUTHORIZED","message":"Token has been revoked"}}' >&2
  exit 1
fi

if [[ "$*" == "projects list --format json" ]]; then
  cat <<'JSON'
{"projects":[{"id":"project-one","name":"Project One"},{"id":"project-two","name":"Project Two"}]}
JSON
  exit 0
fi

if [[ "$*" == *" get onboarding-journey "* ]]; then
  if [[ "$*" == *"--project project-one"* ]]; then
    echo 'project one has no onboarding data yet' >&2
    exit 1
  fi
  cat <<'JSON'
{"starters":100,"completedUsers":40,"completionRate":40,"paywallReachedUsers":50,"paywallSkippedUsers":30,"paywallSkipRateFromPaywall":60,"purchasedUsers":4,"purchaseRateFromPaywall":8}
JSON
  exit 0
fi

if [[ "$*" == *" retention "* ]]; then
  if [[ "$*" == *"--project project-one"* ]]; then
    echo 'project one has no retention data yet' >&2
    exit 1
  fi
  cat <<'JSON'
{"cohortSize":100,"days":[{"day":7,"retentionRate":0.05}]}
JSON
  exit 0
fi

echo "{}"
`,
    { mode: 0o755 },
  );

  try {
    const result = spawnSync('node', [exporter], {
      cwd: skillRoot,
      env: {
        ...process.env,
        PATH: `${fakeBin}:${process.env.PATH || ''}`,
        ANALYTICSCLI_ACCESS_TOKEN: 'fresh-token',
        OPENCLAW_GROWTH_SECRETS_FILE: join(tempDir, 'missing.env'),
      },
      encoding: 'utf8',
    });

    assert.equal(result.status, 0, `${result.stderr}\n${result.stdout}`);
    const payload = JSON.parse(result.stdout);
    assert.equal(payload.meta.source, 'analyticscli');
    assert.equal(payload.meta.projectScope, 'all_accessible_projects');
    assert.equal(payload.meta.projectsScanned, 2);
    assert.equal(payload.meta.projects[0].queryWarnings.length, 2);
    assert(payload.signals.length > 0);
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
});
