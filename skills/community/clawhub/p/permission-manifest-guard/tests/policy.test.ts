import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  compareMetadataToObserved,
  computeCategoryMismatches,
  computeSeverityScore,
  CATEGORY_WEIGHTS,
  THRESHOLDS,
  recommendDisposition,
} from '../src/policy.js';
import type { ObservedPermissions, MismatchReport, Disposition } from '../src/policy.js';
import type { SkillMetadata } from '../src/types.js';

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

// ---------------------------------------------------------------------------
// computeCategoryMismatches
// ---------------------------------------------------------------------------

describe('computeCategoryMismatches', () => {
  it('returns empty array when both declared and observed are empty', () => {
    const result = computeCategoryMismatches('binaries', [], []);
    assert.deepEqual(result, []);
  });

  it('returns empty array when all observed match declared', () => {
    const result = computeCategoryMismatches('binaries', ['curl', 'git'], ['curl', 'git']);
    assert.deepEqual(result, []);
  });

  it('detects undeclared and phantom values in a mixed scenario', () => {
    const result = computeCategoryMismatches(
      'binaries',
      ['curl', 'node'],
      ['curl', 'wget'],
    );
    const undeclared = result.filter(m => m.type === 'undeclared');
    const phantom = result.filter(m => m.type === 'phantom');

    assert.equal(undeclared.length, 1);
    assert.equal(undeclared[0]!.value, 'wget');
    assert.equal(undeclared[0]!.category, 'binaries');

    assert.equal(phantom.length, 1);
    assert.equal(phantom[0]!.value, 'node');
    assert.equal(phantom[0]!.category, 'binaries');
  });
});

// ---------------------------------------------------------------------------
// compareMetadataToObserved
// ---------------------------------------------------------------------------

describe('compareMetadataToObserved', () => {
  it('detects a single undeclared binary', () => {
    const observed = emptyObserved();
    observed.binaries = ['curl'];

    const report = compareMetadataToObserved(emptyMetadata(), observed);

    assert.equal(report.mismatches.length, 1);
    assert.equal(report.mismatches[0]!.category, 'binaries');
    assert.equal(report.mismatches[0]!.value, 'curl');
    assert.equal(report.mismatches[0]!.type, 'undeclared');
    assert.equal(report.summary.undeclared, 1);
    assert.equal(report.summary.phantom, 0);
    assert.equal(report.summary.total, 1);
  });

  it('detects undeclared binaries while ignoring declared ones', () => {
    const metadata: SkillMetadata = { ...emptyMetadata(), declaredPermissions: ['curl'] };
    const observed = emptyObserved();
    observed.binaries = ['curl', 'wget', 'git'];

    const report = compareMetadataToObserved(metadata, observed);

    const undeclared = report.mismatches.filter(m => m.type === 'undeclared');
    assert.equal(undeclared.length, 2);
    assert.ok(undeclared.some(m => m.value === 'wget'));
    assert.ok(undeclared.some(m => m.value === 'git'));
    assert.ok(!undeclared.some(m => m.value === 'curl'));
  });

  it('domain suffix matching: *.example.com covers subdomains', () => {
    const metadata: SkillMetadata = {
      ...emptyMetadata(),
      declaredPermissions: ['*.example.com'],
    };
    const observed = emptyObserved();
    observed.network = ['api.example.com', 'deep.sub.example.com'];

    const report = compareMetadataToObserved(metadata, observed);

    const undeclaredNetwork = report.mismatches.filter(
      m => m.category === 'network' && m.type === 'undeclared',
    );
    assert.equal(undeclaredNetwork.length, 0, 'subdomains should be covered by wildcard');
  });

  it('domain suffix matching: *.example.com does not cover unrelated domains', () => {
    const metadata: SkillMetadata = {
      ...emptyMetadata(),
      declaredPermissions: ['*.example.com'],
    };
    const observed = emptyObserved();
    observed.network = ['api.other.com', 'example.com'];

    const report = compareMetadataToObserved(metadata, observed);

    const undeclaredNetwork = report.mismatches.filter(
      m => m.category === 'network' && m.type === 'undeclared',
    );
    assert.equal(undeclaredNetwork.length, 2);
    assert.ok(undeclaredNetwork.some(m => m.value === 'api.other.com'));
    assert.ok(undeclaredNetwork.some(m => m.value === 'example.com'));
  });

  it('path prefix matching: /tmp/ covers deeper paths', () => {
    const metadata: SkillMetadata = {
      ...emptyMetadata(),
      declaredPermissions: ['/tmp/'],
    };
    const observed = emptyObserved();
    observed.filePaths = ['/tmp/foo/bar.txt', '/etc/hosts'];

    const report = compareMetadataToObserved(metadata, observed);

    const undeclaredPaths = report.mismatches.filter(
      m => m.category === 'filePaths' && m.type === 'undeclared',
    );
    assert.equal(undeclaredPaths.length, 1);
    assert.equal(undeclaredPaths[0]!.value, '/etc/hosts');
  });

  it('env var matching is case-insensitive', () => {
    const metadata: SkillMetadata = {
      ...emptyMetadata(),
      declaredPermissions: ['API_KEY'],
    };
    const observed = emptyObserved();
    observed.envVars = ['api_key'];

    const report = compareMetadataToObserved(metadata, observed);

    const undeclaredEnv = report.mismatches.filter(
      m => m.category === 'envVars' && m.type === 'undeclared',
    );
    assert.equal(undeclaredEnv.length, 0, 'case-insensitive match should cover api_key');
    assert.equal(report.summary.phantom, 0, 'declared API_KEY observed as api_key — not phantom');
  });

  it('detects phantom declarations not observed in code', () => {
    const metadata: SkillMetadata = {
      ...emptyMetadata(),
      declaredPermissions: ['curl', '*.example.com', '/opt/data/'],
    };
    const observed = emptyObserved();

    const report = compareMetadataToObserved(metadata, observed);

    assert.equal(report.summary.phantom, 3);
    assert.equal(report.summary.undeclared, 0);
    const phantoms = report.mismatches.filter(m => m.type === 'phantom');
    assert.ok(phantoms.some(m => m.value === 'curl'));
    assert.ok(phantoms.some(m => m.value === '*.example.com'));
    assert.ok(phantoms.some(m => m.value === '/opt/data/'));
  });

  it('returns empty report when both inputs are empty', () => {
    const report = compareMetadataToObserved(emptyMetadata(), emptyObserved());

    assert.equal(report.mismatches.length, 0);
    assert.equal(report.summary.undeclared, 0);
    assert.equal(report.summary.phantom, 0);
    assert.equal(report.summary.total, 0);
  });

  it('returns zero mismatches when all observed permissions are declared', () => {
    const metadata: SkillMetadata = {
      ...emptyMetadata(),
      declaredPermissions: ['curl', 'api.example.com', '/tmp/', 'API_KEY'],
    };
    const observed = emptyObserved();
    observed.binaries = ['curl'];
    observed.network = ['api.example.com'];
    observed.filePaths = ['/tmp/cache.json'];
    observed.envVars = ['API_KEY'];

    const report = compareMetadataToObserved(metadata, observed);

    assert.equal(report.mismatches.length, 0);
    assert.equal(report.summary.total, 0);
  });
});

// ---------------------------------------------------------------------------
// CATEGORY_WEIGHTS & THRESHOLDS constants (T018)
// ---------------------------------------------------------------------------

describe('CATEGORY_WEIGHTS', () => {
  it('has correct values for all categories', () => {
    assert.equal(CATEGORY_WEIGHTS.riskyCapabilities, 10);
    assert.equal(CATEGORY_WEIGHTS.shellCommands, 8);
    assert.equal(CATEGORY_WEIGHTS.networkDomains, 6);
    assert.equal(CATEGORY_WEIGHTS.binaries, 5);
    assert.equal(CATEGORY_WEIGHTS.fileWritePaths, 5);
    assert.equal(CATEGORY_WEIGHTS.envVars, 4);
    assert.equal(CATEGORY_WEIGHTS.packageManagers, 3);
    assert.equal(CATEGORY_WEIGHTS.fileReadPaths, 2);
    assert.equal(CATEGORY_WEIGHTS.configFiles, 2);
    assert.equal(CATEGORY_WEIGHTS.phantomDeclarations, 1);
  });
});

describe('THRESHOLDS', () => {
  it('has correct boundary values', () => {
    assert.equal(THRESHOLDS.allow, 0);
    assert.equal(THRESHOLDS.reviewMin, 1);
    assert.equal(THRESHOLDS.reviewMax, 7);
    assert.equal(THRESHOLDS.sandboxMin, 8);
    assert.equal(THRESHOLDS.sandboxMax, 19);
    assert.equal(THRESHOLDS.rejectMin, 20);
  });
});

// ---------------------------------------------------------------------------
// recommendDisposition (T018)
// ---------------------------------------------------------------------------

function makeReport(mismatches: MismatchReport['mismatches']): MismatchReport {
  const undeclared = mismatches.filter(m => m.type === 'undeclared').length;
  const phantom = mismatches.filter(m => m.type === 'phantom').length;
  return { mismatches, summary: { undeclared, phantom, total: undeclared + phantom } };
}

describe('computeSeverityScore', () => {
  it('returns score 0 and empty reasons for an empty report', () => {
    const { score, reasons } = computeSeverityScore(makeReport([]));
    assert.equal(score, 0);
    assert.deepEqual(reasons, []);
  });

  it('scores a single category with one undeclared mismatch', () => {
    const { score, reasons } = computeSeverityScore(makeReport([
      { category: 'envVars', value: 'SECRET', type: 'undeclared' },
    ]));
    assert.equal(score, CATEGORY_WEIGHTS.envVars); // 4
    assert.equal(reasons.length, 1);
    assert.ok(reasons[0]!.includes('1 undeclared envVars'));
    assert.ok(reasons[0]!.includes('(+4)'));
  });

  it('accumulates across multiple categories', () => {
    const { score, reasons } = computeSeverityScore(makeReport([
      { category: 'shellCommands', value: 'rm', type: 'undeclared' },       // 8
      { category: 'network', value: 'evil.com', type: 'undeclared' },       // 6
      { category: 'configFiles', value: '.env', type: 'phantom' },          // 1
    ]));
    assert.equal(score, 8 + 6 + 1);
    assert.equal(reasons.length, 3);
  });

  it('sorts reasons by contribution descending', () => {
    const { reasons } = computeSeverityScore(makeReport([
      { category: 'configFiles', value: '.npmrc', type: 'undeclared' },      // 2
      { category: 'riskyCapabilities', value: 'eval()', type: 'undeclared' },// 10
      { category: 'envVars', value: 'KEY', type: 'undeclared' },             // 4
    ]));
    assert.equal(reasons.length, 3);
    assert.ok(reasons[0]!.includes('riskyCapabilities'), 'highest weight first');
    assert.ok(reasons[1]!.includes('envVars'), 'middle weight second');
    assert.ok(reasons[2]!.includes('configFiles'), 'lowest weight last');
  });
});

describe('recommendDisposition', () => {
  it('returns allow with score 0 for a clean report', () => {
    const result = recommendDisposition(makeReport([]));
    assert.equal(result.recommendation, 'allow');
    assert.equal(result.score, 0);
    assert.deepEqual(result.reasons, []);
  });

  it('returns review for a single low-severity mismatch', () => {
    const result = recommendDisposition(makeReport([
      { category: 'configFiles', value: '.eslintrc', type: 'undeclared' },
    ]));
    assert.equal(result.recommendation, 'review');
    assert.equal(result.score, CATEGORY_WEIGHTS.configFiles); // 2
    assert.ok(result.score >= THRESHOLDS.reviewMin && result.score <= THRESHOLDS.reviewMax);
  });

  it('returns sandbox at the review/sandbox boundary (score exactly 8)', () => {
    // networkDomains (6) + configFiles (2) = 8
    const result = recommendDisposition(makeReport([
      { category: 'network', value: 'api.evil.com', type: 'undeclared' },
      { category: 'configFiles', value: '.npmrc', type: 'undeclared' },
    ]));
    assert.equal(result.score, 8);
    assert.equal(result.recommendation, 'sandbox');
  });

  it('returns sandbox for an undeclared shell command', () => {
    const result = recommendDisposition(makeReport([
      { category: 'shellCommands', value: 'rm -rf /', type: 'undeclared' },
    ]));
    assert.equal(result.score, CATEGORY_WEIGHTS.shellCommands); // 8
    assert.equal(result.recommendation, 'sandbox');
  });

  it('returns reject at the sandbox/reject boundary (score exactly 20)', () => {
    // riskyCapabilities (10) + riskyCapabilities (10) = 20
    const result = recommendDisposition(makeReport([
      { category: 'riskyCapabilities', value: 'eval()', type: 'undeclared' },
      { category: 'riskyCapabilities', value: 'child_process', type: 'undeclared' },
    ]));
    assert.equal(result.score, 20);
    assert.equal(result.recommendation, 'reject');
  });

  it('returns reject for undeclared risky capability + network domains', () => {
    // FOCUS: one risky capability (10) + two undeclared network domains (6×2=12) = 22
    const result = recommendDisposition(makeReport([
      { category: 'riskyCapabilities', value: 'eval()', type: 'undeclared' },
      { category: 'network', value: 'evil.com', type: 'undeclared' },
      { category: 'network', value: 'malware.io', type: 'undeclared' },
    ]));
    assert.equal(result.score, 22);
    assert.ok(result.score >= THRESHOLDS.rejectMin);
    assert.equal(result.recommendation, 'reject');
  });

  it('returns review at most for phantom-only mismatches', () => {
    const result = recommendDisposition(makeReport([
      { category: 'binaries', value: 'curl', type: 'phantom' },
      { category: 'network', value: '*.example.com', type: 'phantom' },
      { category: 'configFiles', value: '.env', type: 'phantom' },
    ]));
    // 3 phantoms × 1 = 3
    assert.equal(result.score, 3);
    assert.ok(
      result.recommendation === 'allow' || result.recommendation === 'review',
      `expected allow or review, got ${result.recommendation}`,
    );
  });

  it('produces reasons identifying each contributing category and count', () => {
    const result = recommendDisposition(makeReport([
      { category: 'shellCommands', value: 'curl http://evil.com', type: 'undeclared' },
      { category: 'shellCommands', value: 'wget http://evil.com', type: 'undeclared' },
      { category: 'binaries', value: 'nmap', type: 'phantom' },
    ]));
    assert.ok(result.reasons.some(r => r.includes('2') && r.includes('undeclared') && r.includes('shellCommands')));
    assert.ok(result.reasons.some(r => r.includes('1') && r.includes('phantom')));
  });

  it('computes correct combined multi-category score', () => {
    const result = recommendDisposition(makeReport([
      { category: 'riskyCapabilities', value: 'eval()', type: 'undeclared' },     // 10
      { category: 'shellCommands', value: 'rm -rf', type: 'undeclared' },          // 8
      { category: 'network', value: 'evil.com', type: 'undeclared' },              // 6
      { category: 'envVars', value: 'SECRET_KEY', type: 'undeclared' },            // 4
      { category: 'binaries', value: 'nmap', type: 'phantom' },                    // 1
    ]));
    assert.equal(result.score, 10 + 8 + 6 + 4 + 1);  // 29
    assert.equal(result.recommendation, 'reject');
    assert.equal(result.reasons.length, 5); // 4 undeclared categories + 1 phantom
  });
});
