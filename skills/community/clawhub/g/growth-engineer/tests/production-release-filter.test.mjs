import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import test from 'node:test';

const skillRoot = join(fileURLToPath(new URL('.', import.meta.url)), '..');

function writeJson(filePath, value) {
  writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function runAnalyzer({ sentryVersion, productionVersions }) {
  const dir = mkdtempSync(join(tmpdir(), 'openclaw-production-release-filter-'));
  try {
    mkdirSync(join(dir, 'apps'), { recursive: true });
    writeFileSync(join(dir, 'apps', 'app.ts'), 'export const app = true;\n', 'utf8');

    const analyticsPath = join(dir, 'analytics.json');
    const sentryPath = join(dir, 'sentry.json');
    const ascPath = join(dir, 'asc.json');
    const cadencePath = join(dir, 'cadence.json');
    const outPath = join(dir, 'out.json');

    writeJson(analyticsPath, { project: 'test-app', window: 'last_24h', signals: [] });
    writeJson(sentryPath, {
      project: 'sentry:test/test-app',
      window: 'last_24h',
      signals: [
        {
          id: 'sentry_test',
          title: `Crash in version ${sentryVersion}`,
          area: 'crash',
          priority: 'high',
          metric: 'sentry_unresolved_issues',
          current_value: 12,
          releaseVersions: [sentryVersion],
          evidence: [`Release/app version: ${sentryVersion}`, 'Events: 12'],
          keywords: ['fatal', sentryVersion],
        },
      ],
    });
    writeJson(ascPath, {
      project: 'app-store-connect:test-app',
      signals: [],
      meta: {
        source: 'asc',
        productionVersions,
      },
    });
    writeJson(cadencePath, {
      cadences: [
        {
          key: 'healthcheck',
          title: '90-minute production error healthcheck',
          criticalOnly: true,
          objective: 'Check Sentry/GlitchTip production errors',
          instructions: 'Ignore non-production app versions after ASC comparison.',
        },
      ],
    });

    const result = spawnSync(
      process.execPath,
      [
        join(skillRoot, 'scripts/openclaw-growth-engineer.mjs'),
        '--analytics',
        analyticsPath,
        '--sentry',
        sentryPath,
        '--source',
        `asc_cli=${ascPath}`,
        '--repo-root',
        dir,
        '--out',
        outPath,
        '--cadence-plan',
        cadencePath,
      ],
      { encoding: 'utf8' },
    );

    assert.equal(result.status, 0, result.stderr || result.stdout);
    return JSON.parse(readFileSync(outPath, 'utf8'));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

test('Sentry healthcheck ignores crashes from non-production ASC versions', () => {
  const output = runAnalyzer({ sentryVersion: '2.0.0', productionVersions: ['1.0.0'] });
  assert.equal(output.issue_count, 0);
  assert.equal(output.ignored_signals.length, 1);
  assert.equal(output.ignored_signals[0].reason, 'Sentry/GlitchTip issue release is not an ASC production version');
});

test('Sentry healthcheck keeps crashes from ASC production versions', () => {
  const output = runAnalyzer({ sentryVersion: '1.0.0', productionVersions: ['1.0.0'] });
  assert.equal(output.issue_count, 1);
  assert.equal(output.ignored_signals.length, 0);
  assert.match(output.issues[0].body, /ASC production version check passed/);
});
