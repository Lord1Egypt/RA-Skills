import assert from 'node:assert/strict';
import { chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';

const skillRoot = resolve(import.meta.dirname, '..');

test('ASC exporter downloads compressed reports once and reuses the daily cache', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'openclaw-asc-cache-test-'));
  try {
    const binDir = join(tmp, 'bin');
    mkdirSync(binDir, { recursive: true });
    const fakeAsc = join(binDir, 'asc');
    writeFileSync(
      fakeAsc,
      `#!/usr/bin/env node
const { writeFileSync, appendFileSync } = require('node:fs');
const { gzipSync } = require('node:zlib');

const args = process.argv.slice(2);
const logPath = process.env.FAKE_ASC_LOG;
if (logPath) appendFileSync(logPath, args.join(' ') + '\\n');
const outputIndex = args.indexOf('--output');
const outputPath = outputIndex >= 0 ? args[outputIndex + 1] : '';
const command = args.join(' ');

if (command.startsWith('apps list')) {
  console.log(JSON.stringify({ data: [{ id: '123456789', type: 'apps', attributes: { name: 'Test App' } }] }));
} else if (command.startsWith('status ')) {
  console.log(JSON.stringify({ appstore: { status: 'READY_FOR_SALE' } }));
} else if (command.startsWith('reviews ratings')) {
  console.log(JSON.stringify({ averageRating: 4.8, ratingCount: 120 }));
} else if (command.startsWith('reviews summarizations')) {
  console.log(JSON.stringify({ data: [] }));
} else if (command.startsWith('feedback ')) {
  console.log(JSON.stringify({ data: [] }));
} else if (command.startsWith('analytics requests')) {
  console.log(JSON.stringify({ data: [{ id: 'req_1', type: 'analyticsReportRequests' }] }));
} else if (command.startsWith('analytics view')) {
  console.log(JSON.stringify({ data: [{ id: 'inst_1', type: 'analyticsReportInstances', attributes: { name: 'App Store Downloads Instance' } }] }));
} else if (command.startsWith('analytics download')) {
  if (process.env.FAKE_ASC_FAIL_DOWNLOAD === '1') {
    process.stderr.write('download disabled for cache hit test\\n');
    process.exit(42);
  }
  const report = [
    'Date\\tApp Apple Identifier\\tSource Type\\tImpressions\\tProduct Page Views\\tFirst-Time Downloads\\tPurchases\\tDeveloper Proceeds\\tSessions\\tCrashes\\tApp Version',
    '2026-06-09\\t123456789\\tApp Store Search\\t1000\\t200\\t40\\t6\\t36.50\\t300\\t2\\t2.0.0',
    '2026-06-09\\t123456789\\tWeb Referrer\\t200\\t40\\t8\\t1\\t6.00\\t10\\t0\\t2.0.0',
  ].join('\\n') + '\\n';
  writeFileSync(outputPath, gzipSync(report));
  console.log(JSON.stringify({ output: outputPath }));
} else {
  console.log(JSON.stringify({}));
}
`,
      'utf8',
    );
    chmodSync(fakeAsc, 0o755);

    const cacheDir = join(tmp, 'cache');
    const logPath = join(tmp, 'asc.log');
    const env = {
      ...process.env,
      PATH: `${binDir}:${process.env.PATH || ''}`,
      FAKE_ASC_LOG: logPath,
    };
    const args = [
      join(skillRoot, 'scripts/export-asc-summary.mjs'),
      '--cache-dir',
      cacheDir,
      '--end',
      '2026-06-09',
      '--analytics-instance-limit',
      '1',
      '--max-signals',
      '8',
    ];

    const first = spawnSync(process.execPath, args, { cwd: tmp, env, encoding: 'utf8' });
    assert.equal(first.status, 0, first.stderr);
    const firstPayload = JSON.parse(first.stdout);
    assert.equal(firstPayload.meta.analytics.units.total, 48);
    assert.equal(firstPayload.meta.analytics.impressions.total, 1200);
    assert.equal(firstPayload.meta.analytics.purchases.total, 7);
    assert.equal(firstPayload.meta.analytics.totalCrashes, 2);
    assert.equal(firstPayload.meta.batchReports[0].cacheStatus, 'downloaded');

    const second = spawnSync(process.execPath, args, {
      cwd: tmp,
      env: { ...env, FAKE_ASC_FAIL_DOWNLOAD: '1' },
      encoding: 'utf8',
    });
    assert.equal(second.status, 0, second.stderr);
    const secondPayload = JSON.parse(second.stdout);
    assert.equal(secondPayload.meta.analytics.units.total, 48);
    assert.equal(secondPayload.meta.batchReports[0].cacheStatus, 'hit');

    const commandLog = readFileSync(logPath, 'utf8');
    assert.equal((commandLog.match(/analytics download/g) || []).length, 1);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

test('ASC exporter keeps app-specific queries usable when App Analytics request access is blocked', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'openclaw-asc-auth-blocked-test-'));
  try {
    const binDir = join(tmp, 'bin');
    mkdirSync(binDir, { recursive: true });
    const fakeAsc = join(binDir, 'asc');
    writeFileSync(
      fakeAsc,
      `#!/usr/bin/env node
const { writeFileSync, appendFileSync } = require('node:fs');
const { gzipSync } = require('node:zlib');

const args = process.argv.slice(2);
const logPath = process.env.FAKE_ASC_LOG;
if (logPath) appendFileSync(logPath, args.join(' ') + '\\n');
const outputIndex = args.indexOf('--output');
const outputPath = outputIndex >= 0 ? args[outputIndex + 1] : '';
const command = args.join(' ');

if (command.startsWith('status ')) {
  console.log(JSON.stringify({ appstore: { version: '2.1.13', state: 'READY_FOR_SALE' } }));
} else if (command.startsWith('reviews ratings')) {
  console.log(JSON.stringify({ averageRating: 4.6, ratingCount: 42 }));
} else if (command.startsWith('reviews summarizations')) {
  console.log(JSON.stringify({ data: [] }));
} else if (command.startsWith('testflight feedback list')) {
  console.log(JSON.stringify({ data: [] }));
} else if (command.startsWith('analytics sales')) {
  const report = [
    'Date\\tApp Apple Identifier\\tSource Type\\tUnits\\tDeveloper Proceeds',
    '2026-06-09\\t6475738569\\tApp Store Search\\t9\\t18.00',
  ].join('\\n') + '\\n';
  writeFileSync(outputPath, gzipSync(report));
  console.log(JSON.stringify({ output: outputPath }));
} else if (command.startsWith('analytics requests')) {
  process.stderr.write('Error: analytics requests: failed to fetch: This request is forbidden for security reasons: The API key in use does not allow this request\\n');
  process.exit(13);
} else if (command.startsWith('analytics request ')) {
  process.stderr.write('should not create when request listing is auth-blocked\\n');
  process.exit(42);
} else {
  console.log(JSON.stringify({}));
}
`,
      'utf8',
    );
    chmodSync(fakeAsc, 0o755);

    const cacheDir = join(tmp, 'cache');
    const logPath = join(tmp, 'asc.log');
    const result = spawnSync(
      process.execPath,
      [
        join(skillRoot, 'scripts/export-asc-summary.mjs'),
        '--app',
        '6475738569',
        '--cache-dir',
        cacheDir,
        '--end',
        '2026-06-09',
        '--analytics-instance-limit',
        '1',
        '--max-signals',
        '8',
      ],
      {
        cwd: tmp,
        env: {
          ...process.env,
          PATH: `${binDir}:${process.env.PATH || ''}`,
          FAKE_ASC_LOG: logPath,
          ASC_VENDOR_NUMBER: '93770984',
        },
        encoding: 'utf8',
      },
    );

    assert.equal(result.status, 0, result.stderr);
    const payload = JSON.parse(result.stdout);
    assert.equal(payload.meta.appId, '6475738569');
    assert.equal(payload.meta.analyticsAvailability, 'partial_auth_blocked');
    assert.equal(payload.meta.analytics.units.total, 9);
    assert.match(payload.meta.analyticsWarnings.join('\n'), /cannot read App Analytics report requests/);

    const commandLog = readFileSync(logPath, 'utf8');
    assert.match(commandLog, /testflight feedback list --app 6475738569/);
    assert.match(commandLog, /analytics requests --app 6475738569/);
    assert.doesNotMatch(commandLog, /analytics request --app 6475738569/);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

test('ASC exporter retries blocked analytics calls with the Admin p8 fallback env', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'openclaw-asc-admin-fallback-test-'));
  try {
    const binDir = join(tmp, 'bin');
    mkdirSync(binDir, { recursive: true });
    const fakeAsc = join(binDir, 'asc');
    writeFileSync(
      fakeAsc,
      `#!/usr/bin/env node
const { writeFileSync, appendFileSync } = require('node:fs');
const { gzipSync } = require('node:zlib');
const args = process.argv.slice(2);
const logPath = process.env.FAKE_ASC_LOG;
if (logPath) appendFileSync(logPath, args.join(' ') + ' key=' + (process.env.ASC_KEY_ID || '') + '\\n');
const outputIndex = args.indexOf('--output');
const outputPath = outputIndex >= 0 ? args[outputIndex + 1] : '';
const command = args.join(' ');
const isAdmin = process.env.ASC_KEY_ID === 'ADMINKEY';
function forbidden() {
  process.stderr.write('Error: request failed: This request is forbidden for security reasons: The API key in use does not allow this request\\n');
  process.exit(13);
}
if (command.startsWith('reviews ratings')) {
  console.log(JSON.stringify({ averageRating: 4.6, ratingCount: 42 }));
} else if (command.startsWith('analytics sales')) {
  if (!isAdmin) forbidden();
  const report = [
    'Date\\tApp Apple Identifier\\tSource Type\\tUnits\\tDeveloper Proceeds',
    '2026-06-09\\t6475738569\\tApp Store Search\\t11\\t22.00',
  ].join('\\n') + '\\n';
  writeFileSync(outputPath, gzipSync(report));
  console.log(JSON.stringify({ output: outputPath }));
} else if (command.startsWith('analytics requests')) {
  if (!isAdmin) forbidden();
  console.log(JSON.stringify({ data: [{ id: 'req_admin', type: 'analyticsReportRequests' }] }));
} else if (command.startsWith('analytics view')) {
  if (!isAdmin) forbidden();
  console.log(JSON.stringify({ data: [] }));
} else {
  console.log(JSON.stringify({}));
}
`,
      'utf8',
    );
    chmodSync(fakeAsc, 0o755);

    const logPath = join(tmp, 'asc.log');
    const result = spawnSync(
      process.execPath,
      [
        join(skillRoot, 'scripts/export-asc-summary.mjs'),
        '--app',
        '6475738569',
        '--cache-dir',
        join(tmp, 'cache'),
        '--end',
        '2026-06-09',
        '--command-timeout-ms',
        '5000',
      ],
      {
        cwd: tmp,
        env: {
          ...process.env,
          PATH: `${binDir}:${process.env.PATH || ''}`,
          FAKE_ASC_LOG: logPath,
          ASC_VENDOR_NUMBER: '93770984',
          ASC_ADMIN_KEY_ID: 'ADMINKEY',
          ASC_ADMIN_ISSUER_ID: 'issuer',
          ASC_ADMIN_PRIVATE_KEY_PATH: join(tmp, 'AuthKey_ADMINKEY.p8'),
        },
        encoding: 'utf8',
      },
    );

    assert.equal(result.status, 0, result.stderr);
    const payload = JSON.parse(result.stdout);
    assert.equal(payload.meta.analyticsAvailability, 'available');
    assert.ok(payload.meta.analytics.units.total >= 11);
    assert.match(payload.meta.analyticsWarnings.join('\n'), /retried with ASC_ADMIN key/);

    const commandLog = readFileSync(logPath, 'utf8');
    assert.match(commandLog, /analytics sales .* key=/);
    assert.match(commandLog, /analytics sales .* key=ADMINKEY/);
    assert.match(commandLog, /analytics requests .* key=ADMINKEY/);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

test('ASC exporter does not create analytics requests after request-list timeouts', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'openclaw-asc-timeout-test-'));
  try {
    const binDir = join(tmp, 'bin');
    mkdirSync(binDir, { recursive: true });
    const fakeAsc = join(binDir, 'asc');
    writeFileSync(
      fakeAsc,
      `#!/usr/bin/env node
const { appendFileSync } = require('node:fs');
const args = process.argv.slice(2);
const logPath = process.env.FAKE_ASC_LOG;
if (logPath) appendFileSync(logPath, args.join(' ') + '\\n');
const command = args.join(' ');
if (command.startsWith('reviews ratings')) {
  console.log(JSON.stringify({ averageRating: 4.6, ratingCount: 42 }));
} else if (command.startsWith('analytics requests')) {
  setTimeout(() => {}, 60_000);
} else if (command.startsWith('analytics request ')) {
  process.stderr.write('should not create after request-list timeout\\n');
  process.exit(42);
} else {
  console.log(JSON.stringify({}));
}
`,
      'utf8',
    );
    chmodSync(fakeAsc, 0o755);

    const logPath = join(tmp, 'asc.log');
    const result = spawnSync(
      process.execPath,
      [
        join(skillRoot, 'scripts/export-asc-summary.mjs'),
        '--app',
        '6475738569',
        '--cache-dir',
        join(tmp, 'cache'),
        '--end',
        '2026-06-09',
        '--command-timeout-ms',
        '1000',
      ],
      {
        cwd: tmp,
        env: {
          ...process.env,
          PATH: `${binDir}:${process.env.PATH || ''}`,
          FAKE_ASC_LOG: logPath,
        },
        encoding: 'utf8',
      },
    );

    assert.equal(result.status, 0, result.stderr);
    const payload = JSON.parse(result.stdout);
    assert.equal(payload.meta.analyticsAvailability, 'temporarily_unavailable');
    assert.match(payload.meta.analyticsWarnings.join('\n'), /skipped request creation/);

    const commandLog = existsSync(logPath) ? readFileSync(logPath, 'utf8') : '';
    if (commandLog) {
      assert.match(commandLog, /analytics requests --app 6475738569/);
      assert.doesNotMatch(commandLog, /analytics request --app 6475738569/);
    }
    assert.doesNotMatch(`${result.stdout}\n${result.stderr}`, /should not create after request-list timeout/);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});
