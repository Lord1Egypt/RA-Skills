import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { analyzeSkill } from '../src/index.js';

const FIXTURE_DIR = path.resolve(import.meta.dirname, 'fixtures/sample-skill');

describe('Self-scan: analyzeSkill against committed fixture', () => {
  let result: Awaited<ReturnType<typeof analyzeSkill>>;
  let json: Record<string, unknown>;

  // Run the pipeline once; all 8 tests share the result.
  // node:test runs it() callbacks sequentially within a describe, so
  // lazy-init on first access is safe and avoids before() lifecycle noise.
  async function ensureResult(): Promise<void> {
    if (!result) {
      result = await analyzeSkill(FIXTURE_DIR);
      json = result.jsonManifest as Record<string, unknown>;
    }
  }

  it('markdownManifest is a non-empty string', async () => {
    await ensureResult();
    assert.equal(typeof result.markdownManifest, 'string');
    assert.ok(result.markdownManifest.length > 0, 'markdownManifest must not be empty');
  });

  it('jsonManifest has all 5 top-level keys', async () => {
    await ensureResult();
    const requiredKeys = ['skill_name', 'disposition', 'observed', 'mismatches', 'summary'];
    for (const key of requiredKeys) {
      assert.ok(key in json, `JSON manifest must have key: ${key}`);
    }
  });

  it('skill_name equals sample-skill', async () => {
    await ensureResult();
    assert.equal(json['skill_name'], 'sample-skill');
  });

  it('observed.network includes api.example.com', async () => {
    await ensureResult();
    const observed = json['observed'] as Record<string, string[]>;
    assert.ok(Array.isArray(observed['network']), 'observed.network must be an array');
    assert.ok(
      observed['network'].includes('api.example.com'),
      `expected api.example.com in observed.network, got: ${JSON.stringify(observed['network'])}`,
    );
  });

  it('observed.binaries is non-empty', async () => {
    await ensureResult();
    const observed = json['observed'] as Record<string, string[]>;
    assert.ok(Array.isArray(observed['binaries']), 'observed.binaries must be an array');
    assert.ok(observed['binaries'].length > 0, 'observed.binaries must not be empty');
  });

  it('observed.envVars includes API_KEY', async () => {
    await ensureResult();
    const observed = json['observed'] as Record<string, string[]>;
    assert.ok(Array.isArray(observed['envVars']), 'observed.envVars must be an array');
    assert.ok(
      observed['envVars'].includes('API_KEY'),
      `expected API_KEY in observed.envVars, got: ${JSON.stringify(observed['envVars'])}`,
    );
  });

  it('mismatches.undeclared is non-empty', async () => {
    await ensureResult();
    const mismatches = json['mismatches'] as Record<string, unknown[]>;
    assert.ok(Array.isArray(mismatches['undeclared']), 'mismatches.undeclared must be an array');
    assert.ok(mismatches['undeclared'].length > 0, 'must have at least one undeclared mismatch');
  });

  it('markdownManifest contains Network Domains and Summary headings', async () => {
    await ensureResult();
    assert.ok(
      result.markdownManifest.includes('## Network Domains'),
      'markdownManifest must contain "## Network Domains"',
    );
    assert.ok(
      result.markdownManifest.includes('## Summary'),
      'markdownManifest must contain "## Summary"',
    );
  });
});
