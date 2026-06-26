#!/usr/bin/env node
/**
 * Security tests for paperclip-resilience.
 *
 * Covers the hardened surfaces added for SUP-453:
 * - file path validation (including symlink handling)
 * - model + spawn argument validation
 * - task size / @file handling through dry-run mode
 * - config regex sanitization
 * - Paperclip issue-gate input sanitization helpers
 */

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');

const spawnModule = require('../src/spawn-with-fallback');
const issueGate = require('../src/lib/paperclip-issue-gate');

let passed = 0;
let failed = 0;

function pass(label) {
  console.log(`  ✅ ${label}`);
  passed += 1;
}

function fail(label, detail) {
  console.error(`  ❌ FAIL: ${label}${detail ? ` — ${detail}` : ''}`);
  failed += 1;
}

function assert(condition, label, detail) {
  if (condition) pass(label);
  else fail(label, detail);
}

function assertEq(actual, expected, label) {
  if (actual === expected) {
    pass(label);
    return;
  }
  fail(label, `expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
}

function assertThrowsSync(fn, expectedMessage, label) {
  try {
    fn();
    fail(label, 'expected error but none thrown');
  } catch (error) {
    if (!expectedMessage || String(error.message).includes(expectedMessage)) {
      pass(label);
    } else {
      fail(label, `expected error containing ${JSON.stringify(expectedMessage)}, got ${JSON.stringify(error.message)}`);
    }
  }
}

async function assertThrowsAsync(fn, expectedMessage, label) {
  try {
    await fn();
    fail(label, 'expected error but none thrown');
  } catch (error) {
    if (!expectedMessage || String(error.message).includes(expectedMessage)) {
      pass(label);
    } else {
      fail(label, `expected error containing ${JSON.stringify(expectedMessage)}, got ${JSON.stringify(error.message)}`);
    }
  }
}

async function run() {
  const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'paperclip-resilience-security-'));

  try {
    console.log('\n── Security: file path validation ──');

    assertThrowsSync(
      () => spawnModule.validateFilePath('../../../etc/passwd'),
      'Path traversal',
      'Blocks explicit ../ traversal',
    );

    assertThrowsSync(
      () => spawnModule.validateFilePath('/etc/passwd'),
      'system path',
      'Blocks direct system paths',
    );

    const regularFile = path.join(tmpRoot, 'task.txt');
    fs.writeFileSync(regularFile, 'safe task');
    assertEq(
      spawnModule.validateFilePath(regularFile),
      fs.realpathSync(regularFile),
      'Allows regular temp files and returns canonical path',
    );

    assertThrowsSync(
      () => spawnModule.validateFilePath(tmpRoot),
      'regular file',
      'Rejects directories',
    );

    const symlinkPath = path.join(tmpRoot, 'passwd-link');
    try {
      fs.symlinkSync('/etc/passwd', symlinkPath);
      assertThrowsSync(
        () => spawnModule.validateFilePath(symlinkPath),
        'system path',
        'Blocks temp symlinks that resolve into system paths',
      );
    } catch (error) {
      pass(`Symlink tunnel check skipped (${error.code || error.message})`);
    } finally {
      try { fs.unlinkSync(symlinkPath); } catch {}
    }

    console.log('\n── Security: model validation ──');

    assertEq(
      spawnModule.validateModelInput('openrouter/z-ai/glm-4.5-air:free'),
      'openrouter/z-ai/glm-4.5-air:free',
      'Allows valid provider/model strings with :free suffixes',
    );

    assertThrowsSync(
      () => spawnModule.validateModelInput('anthropic/../secrets'),
      'path traversal',
      'Blocks path traversal segments in model names',
    );

    assertThrowsSync(
      () => spawnModule.validateModelInput('anthropic//sonnet'),
      'path traversal',
      'Blocks empty model path segments',
    );

    assertThrowsSync(
      () => spawnModule.validateModelInput('bad model with spaces'),
      'invalid characters',
      'Blocks whitespace and other invalid model characters',
    );

    console.log('\n── Security: spawn argument validation ──');

    spawnModule.validateSpawnArgs('run', 'valid-label');
    pass('Allows valid spawn mode + label');

    spawnModule.validateSpawnArgs('session', 'another.label-123');
    pass('Allows session mode');

    assertThrowsSync(
      () => spawnModule.validateSpawnArgs('shell', null),
      'Invalid mode',
      'Rejects unexpected spawn modes',
    );

    assertThrowsSync(
      () => spawnModule.validateSpawnArgs(null, 'bad@label'),
      'invalid characters',
      'Rejects unsafe label characters',
    );

    console.log('\n── Security: task resolution via dry-run ──');

    const dryRunInline = await spawnModule.spawnWithFallback({
      model: 'sonnet',
      task: 'simple task',
      dryRun: true,
      config: spawnModule.loadConfig(),
    });
    assert(
      dryRunInline.task_preview.includes('simple task'),
      'Allows plain inline task strings',
    );

    const dryRunFile = await spawnModule.spawnWithFallback({
      model: 'sonnet',
      task: `@${regularFile}`,
      dryRun: true,
      config: spawnModule.loadConfig(),
    });
    assert(
      dryRunFile.task_preview.includes('safe task'),
      'Allows @file task loading from validated temp files',
    );

    const oversizedTask = 'x'.repeat(1024 * 1024 + 1);
    await assertThrowsAsync(
      () => spawnModule.spawnWithFallback({
        model: 'sonnet',
        task: oversizedTask,
        dryRun: true,
        config: spawnModule.loadConfig(),
      }),
      'maximum size',
      'Rejects oversized task payloads',
    );

    console.log('\n── Security: config regex sanitization ──');

    const configPath = path.join(tmpRoot, 'config.json');
    fs.writeFileSync(configPath, JSON.stringify({
      failurePatterns: {
        patterns: [
          'rate[\\s_-]?limit',
          '(',
          'x'.repeat(300),
        ],
      },
    }));

    const cfg = spawnModule.loadConfig(configPath);
    assertEq(cfg.failurePatterns.length, 1, 'Invalid or oversized regex patterns are filtered out');
    assert(cfg.failurePatterns[0].test('rate limit'), 'Remaining valid regex still works');

    console.log('\n── Security: Paperclip issue-gate sanitization ──');

    assertEq(
      issueGate.extractIssueIdentifier('Please handle SUP-453 before release'),
      'SUP-453',
      'Extracts valid Paperclip identifiers',
    );

    const sanitized = issueGate.sanitizeApiString('abc\u0000\u0007def', 5);
    assertEq(sanitized, 'abcde', 'Strips control characters and truncates API strings');

    assertEq(issueGate.validatePriority('HIGH'), 'high', 'Normalizes valid priorities');
    assertEq(issueGate.validatePriority('urgent'), 'medium', 'Falls back to medium for invalid priorities');

    console.log(`\n${'='.repeat(50)}`);
    console.log(`Security Results: ${passed} passed, ${failed} failed`);
    process.exit(failed > 0 ? 1 : 0);
  } finally {
    fs.rmSync(tmpRoot, { recursive: true, force: true });
  }
}

run().catch((error) => {
  console.error('Security test runner error:', error);
  process.exit(1);
});
