import assert from 'node:assert/strict';
import os from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';
import { SKILL_ID } from '../lib/constants.js';
import { normalizeScope, validateScopeForRuntime } from '../lib/core/scope.js';
import { detectOS, formatDisplayPath } from '../lib/os.js';
import {
  resolveInstallLocation,
  resolveRuntimeIds,
  RUNTIME_IDS,
  RUNTIMES,
} from '../lib/runtime/index.js';

describe('resolveRuntimeIds', () => {
  it('returns all runtimes for all', () => {
    assert.deepEqual(resolveRuntimeIds('all'), ['claude', 'openclaw']);
  });

  it('parses comma separated runtimes', () => {
    assert.deepEqual(resolveRuntimeIds('claude,openclaw'), ['claude', 'openclaw']);
  });

  it('rejects abbreviated runtime names', () => {
    assert.throws(() => resolveRuntimeIds('c'), /Unknown runtime/);
  });
});

describe('resolveInstallLocation', () => {
  it('resolves global claude path ending with skill id', () => {
    const location = resolveInstallLocation('claude', 'global');
    assert.match(location.installDir, new RegExp(`[\\\\/]${SKILL_ID}$`));
  });

  it('resolves openclaw workspace skills path', () => {
    const location = resolveInstallLocation('openclaw', 'workspace', { cwd: process.cwd() });
    const expected = path.join(os.homedir(), '.openclaw', 'workspace', 'skills', SKILL_ID);
    assert.equal(location.installDir, expected);
    assert.equal(location.strategy, 'OpenClaw workspace skills directory (~/.openclaw/workspace/skills)');
  });
});

describe('normalizeScope', () => {
  it('accepts global, project and workspace', () => {
    assert.equal(normalizeScope('global'), 'global');
    assert.equal(normalizeScope('project'), 'project');
    assert.equal(normalizeScope('workspace'), 'workspace');
  });
});

describe('validateScopeForRuntime', () => {
  it('allows global and project for claude', () => {
    assert.equal(validateScopeForRuntime('claude', 'global'), 'global');
    assert.equal(validateScopeForRuntime('claude', 'project'), 'project');
  });

  it('rejects workspace for claude', () => {
    assert.throws(
      () => validateScopeForRuntime('claude', 'workspace'),
      /not supported for claude/,
    );
  });

  it('allows workspace for openclaw', () => {
    assert.equal(validateScopeForRuntime('openclaw', 'workspace'), 'workspace');
  });
});

describe('runtime registry', () => {
  it('only exposes claude and openclaw', () => {
    assert.deepEqual(RUNTIME_IDS, ['claude', 'openclaw']);
    assert.equal(RUNTIMES.claude.id, 'claude');
    assert.equal(RUNTIMES.openclaw.id, 'openclaw');
  });
});

describe('formatDisplayPath', () => {
  it('returns absolute path when outside home', () => {
    assert.equal(formatDisplayPath('D:/outside/path', 'windows'), 'D:/outside/path');
  });
});
