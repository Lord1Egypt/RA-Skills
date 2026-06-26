import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  compareMetadataToObserved,
  computeSeverityScore,
  CATEGORY_WEIGHTS,
} from '../src/policy.js';
import type { ObservedPermissions, Mismatch } from '../src/policy.js';
import type { SkillMetadata } from '../src/types.js';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function emptyObserved(): ObservedPermissions {
  return {
    binaries: [],
    network: [],
    filePaths: [],
    envVars: [],
    shellCommands: [],
    configFiles: [],
    packageManagers: [],
    riskyCapabilities: [],
  };
}

function emptyMetadata(): SkillMetadata {
  return {
    name: 'test-skill',
    version: '0.1.0',
    declaredPermissions: [],
    declaredDependencies: {},
  };
}

function undeclaredOf(mismatches: Mismatch[], category: string): Mismatch[] {
  return mismatches.filter(m => m.type === 'undeclared' && m.category === category);
}

function phantomOf(mismatches: Mismatch[], category: string): Mismatch[] {
  return mismatches.filter(m => m.type === 'phantom' && m.category === category);
}

// ---------------------------------------------------------------------------
// Undeclared network access (5 tests)
// ---------------------------------------------------------------------------

describe('metadata mismatch: undeclared network access', () => {
  it('detects fetch to undeclared domain', () => {
    // Simulates: fetch('https://api.example.com/data')
    const observed = emptyObserved();
    observed.network = ['api.example.com'];

    const report = compareMetadataToObserved(emptyMetadata(), observed);
    const findings = undeclaredOf(report.mismatches, 'network');

    assert.equal(findings.length, 1);
    assert.equal(findings[0]!.value, 'api.example.com');
    assert.equal(findings[0]!.type, 'undeclared');
    const { score } = computeSeverityScore(report);
    assert.equal(score, CATEGORY_WEIGHTS.networkDomains);
  });

  it('detects axios.get to undeclared domain', () => {
    // Simulates: axios.get('https://data.service.io/v2/records')
    const observed = emptyObserved();
    observed.network = ['data.service.io'];

    const report = compareMetadataToObserved(emptyMetadata(), observed);
    const findings = undeclaredOf(report.mismatches, 'network');

    assert.equal(findings.length, 1);
    assert.equal(findings[0]!.value, 'data.service.io');
    assert.equal(findings[0]!.type, 'undeclared');
    assert.equal(report.summary.undeclared, 1);
  });

  it('detects http.get to undeclared domain', () => {
    // Simulates: http.get('http://metrics.internal:9090/push')
    const observed = emptyObserved();
    observed.network = ['metrics.internal'];

    const report = compareMetadataToObserved(emptyMetadata(), observed);
    const findings = undeclaredOf(report.mismatches, 'network');

    assert.equal(findings.length, 1);
    assert.equal(findings[0]!.value, 'metrics.internal');
    assert.equal(findings[0]!.type, 'undeclared');
    const { score } = computeSeverityScore(report);
    assert.equal(score, CATEGORY_WEIGHTS.networkDomains);
  });

  it('detects WS protocol connection to undeclared domain', () => {
    // Simulates: wss://ws.live-feed.com/stream via WS protocol
    const observed = emptyObserved();
    observed.network = ['ws.live-feed.com'];

    const report = compareMetadataToObserved(emptyMetadata(), observed);
    const findings = undeclaredOf(report.mismatches, 'network');

    assert.equal(findings.length, 1);
    assert.equal(findings[0]!.value, 'ws.live-feed.com');
    assert.equal(findings[0]!.type, 'undeclared');
    assert.equal(report.summary.undeclared, 1);
    assert.equal(report.summary.phantom, 0);
  });

  it('detects dns.lookup of undeclared domain', () => {
    // Simulates: dns.lookup('telemetry.tracker.io', callback)
    const observed = emptyObserved();
    observed.network = ['telemetry.tracker.io'];

    const report = compareMetadataToObserved(emptyMetadata(), observed);
    const findings = undeclaredOf(report.mismatches, 'network');

    assert.equal(findings.length, 1);
    assert.equal(findings[0]!.value, 'telemetry.tracker.io');
    assert.equal(findings[0]!.type, 'undeclared');
    const { score } = computeSeverityScore(report);
    assert.equal(score, CATEGORY_WEIGHTS.networkDomains);
  });
});

// ---------------------------------------------------------------------------
// Undeclared binaries (3 tests)
// ---------------------------------------------------------------------------

describe('metadata mismatch: undeclared binaries', () => {
  it('detects child_process.exec calling undeclared binary', () => {
    // Simulates: exec('ffmpeg -i input.mp4 output.webm')
    const metadata: SkillMetadata = {
      ...emptyMetadata(),
      declaredPermissions: ['node'],
    };
    const observed = emptyObserved();
    observed.binaries = ['node', 'ffmpeg'];

    const report = compareMetadataToObserved(metadata, observed);
    const findings = undeclaredOf(report.mismatches, 'binaries');

    assert.equal(findings.length, 1);
    assert.equal(findings[0]!.value, 'ffmpeg');
    assert.equal(findings[0]!.type, 'undeclared');
    const { score } = computeSeverityScore(report);
    assert.equal(score, CATEGORY_WEIGHTS.binaries);
  });

  it('detects shebang referencing undeclared interpreter', () => {
    // Simulates: #!/usr/bin/env python3
    const observed = emptyObserved();
    observed.binaries = ['python3'];

    const report = compareMetadataToObserved(emptyMetadata(), observed);
    const findings = undeclaredOf(report.mismatches, 'binaries');

    assert.equal(findings.length, 1);
    assert.equal(findings[0]!.value, 'python3');
    assert.equal(findings[0]!.type, 'undeclared');
    assert.equal(report.summary.undeclared, 1);
  });

  it('detects npx invocation of undeclared package', () => {
    // Simulates: exec('npx prettier --write .')
    const metadata: SkillMetadata = {
      ...emptyMetadata(),
      declaredPermissions: ['node'],
    };
    const observed = emptyObserved();
    observed.binaries = ['node', 'npx', 'prettier'];

    const report = compareMetadataToObserved(metadata, observed);
    const findings = undeclaredOf(report.mismatches, 'binaries');

    assert.equal(findings.length, 2);
    assert.ok(findings.some(m => m.value === 'npx'));
    assert.ok(findings.some(m => m.value === 'prettier'));
    findings.forEach(f => assert.equal(f.type, 'undeclared'));
    const { score } = computeSeverityScore(report);
    assert.equal(score, 2 * CATEGORY_WEIGHTS.binaries);
  });
});

// ---------------------------------------------------------------------------
// Over-permissioned manifest (1 test)
// ---------------------------------------------------------------------------

describe('metadata mismatch: over-permissioned manifest', () => {
  it('reports phantom finding when network is declared but unused', () => {
    // Declares network permission but code never makes network calls
    const metadata: SkillMetadata = {
      ...emptyMetadata(),
      declaredPermissions: ['api.example.com'],
    };
    const observed = emptyObserved();

    const report = compareMetadataToObserved(metadata, observed);
    const findings = phantomOf(report.mismatches, 'network');

    assert.equal(findings.length, 1);
    assert.equal(findings[0]!.value, 'api.example.com');
    assert.equal(findings[0]!.type, 'phantom');
    assert.equal(report.summary.phantom, 1);
    assert.equal(report.summary.undeclared, 0);
    const { score } = computeSeverityScore(report);
    assert.equal(score, CATEGORY_WEIGHTS.phantomDeclarations);
  });
});
