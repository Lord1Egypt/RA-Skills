import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  classifyRisk,
  CATEGORY_WEIGHTS,
  RISK_THRESHOLDS,
  PRIVILEGE_ESCALATION_INDICATORS,
  specificityScore,
  scoreCategoryWeight,
  scoreSpecificity,
  scorePrivilegeEscalation,
  RISKY_PATTERNS,
  detectRiskyCapabilities,
} from '../src/classify.js';
import type { ClassifiedEntry, RiskyCapability } from '../src/classify.js';
import type { PermissionEntry, DiscoveredFile } from '../src/types.js';

// ---------------------------------------------------------------------------
// Helper to build a PermissionEntry quickly
// ---------------------------------------------------------------------------

function entry(
  category: PermissionEntry['category'],
  value: string,
  risk: PermissionEntry['risk'] = 'low',
): PermissionEntry {
  return { category, value, source: 'test.ts', line: 1, risk, reason: 'test' };
}

// ---------------------------------------------------------------------------
// Scoring tables are defined as const, not inline magic numbers
// ---------------------------------------------------------------------------

describe('CATEGORY_WEIGHTS', () => {
  it('maps every PermissionCategory to a numeric weight', () => {
    const expectedKeys: string[] = [
      'binary', 'shell_command', 'network', 'file_read', 'file_write',
      'config_file', 'env_variable', 'secret', 'package_manager', 'risky_capability',
    ];
    for (const key of expectedKeys) {
      assert.ok(typeof CATEGORY_WEIGHTS[key as keyof typeof CATEGORY_WEIGHTS] === 'number',
        `Missing weight for ${key}`);
    }
  });
});

describe('RISK_THRESHOLDS', () => {
  it('defines low, medium, and high boundaries', () => {
    assert.ok(typeof RISK_THRESHOLDS.low === 'number');
    assert.ok(typeof RISK_THRESHOLDS.medium === 'number');
    assert.ok(typeof RISK_THRESHOLDS.high === 'number');
    assert.ok(RISK_THRESHOLDS.low < RISK_THRESHOLDS.medium);
    assert.ok(RISK_THRESHOLDS.medium < RISK_THRESHOLDS.high);
  });
});

describe('PRIVILEGE_ESCALATION_INDICATORS', () => {
  it('is a non-empty array of patterns with bonus scores', () => {
    assert.ok(PRIVILEGE_ESCALATION_INDICATORS.length > 0);
    for (const indicator of PRIVILEGE_ESCALATION_INDICATORS) {
      assert.ok(indicator.pattern instanceof RegExp);
      assert.ok(typeof indicator.bonus === 'number');
      assert.ok(indicator.bonus >= 2 && indicator.bonus <= 5);
    }
  });
});

// ---------------------------------------------------------------------------
// specificityScore
// ---------------------------------------------------------------------------

describe('specificityScore', () => {
  it('scores wildcard * as 5', () => {
    assert.equal(specificityScore('*'), 5);
  });

  it('scores ** as 5', () => {
    assert.equal(specificityScore('**'), 5);
  });

  it('scores **/* as 5', () => {
    assert.equal(specificityScore('**/*'), 5);
  });

  it('scores glob patterns with ? or * as 4', () => {
    assert.equal(specificityScore('*.example.com'), 4);
    assert.equal(specificityScore('/tmp/*.log'), 4);
  });

  it('scores CIDR-like ranges as 3', () => {
    assert.equal(specificityScore('10.0.0.0/8'), 3);
  });

  it('scores narrow literal paths as 1', () => {
    assert.equal(specificityScore('/home/user/.bashrc'), 1);
    assert.equal(specificityScore('api.example.com'), 1);
  });

  it('scores empty string as 0', () => {
    assert.equal(specificityScore(''), 0);
  });
});

// ---------------------------------------------------------------------------
// scoreCategoryWeight
// ---------------------------------------------------------------------------

describe('scoreCategoryWeight', () => {
  it('returns the correct weight for each known category', () => {
    const categories: Array<[PermissionEntry['category'], number]> = [
      ['binary', 5], ['shell_command', 7], ['network', 8],
      ['file_read', 3], ['file_write', 6], ['config_file', 3],
      ['env_variable', 2], ['secret', 7], ['package_manager', 5],
      ['risky_capability', 9],
    ];
    for (const [cat, expected] of categories) {
      assert.equal(scoreCategoryWeight(entry(cat, 'x')), expected,
        `Expected weight ${expected} for ${cat}`);
    }
  });

  it('returns default weight of 1 for unknown categories', () => {
    const unknownEntry = entry('binary', 'x');
    // Force an unknown category to bypass TypeScript's type checking
    (unknownEntry as { category: string }).category = 'totally_unknown';
    assert.equal(scoreCategoryWeight(unknownEntry), 1);
  });

  it('does not depend on the entry value', () => {
    assert.equal(
      scoreCategoryWeight(entry('network', '*')),
      scoreCategoryWeight(entry('network', 'api.example.com')),
    );
  });
});

// ---------------------------------------------------------------------------
// scoreSpecificity (entry-level wrapper)
// ---------------------------------------------------------------------------

describe('scoreSpecificity', () => {
  it('returns 5 for wildcard * value', () => {
    assert.equal(scoreSpecificity(entry('network', '*')), 5);
  });

  it('returns 5 for ** and **/*', () => {
    assert.equal(scoreSpecificity(entry('file_read', '**')), 5);
    assert.equal(scoreSpecificity(entry('file_read', '**/*')), 5);
  });

  it('returns 4 for glob patterns', () => {
    assert.equal(scoreSpecificity(entry('network', '*.example.com')), 4);
    assert.equal(scoreSpecificity(entry('file_read', '/tmp/*.log')), 4);
  });

  it('returns 3 for CIDR ranges', () => {
    assert.equal(scoreSpecificity(entry('network', '10.0.0.0/8')), 3);
  });

  it('returns 1 for specific literal values', () => {
    assert.equal(scoreSpecificity(entry('network', 'api.example.com')), 1);
    assert.equal(scoreSpecificity(entry('file_read', '/home/user/.bashrc')), 1);
  });

  it('returns 0 for empty string value', () => {
    assert.equal(scoreSpecificity(entry('env_variable', '')), 0);
  });

  it('delegates to specificityScore under the hood', () => {
    const testValues = ['*', '**', 'foo.bar', '', '*.txt', '10.0.0.0/16'];
    for (const val of testValues) {
      assert.equal(scoreSpecificity(entry('binary', val)), specificityScore(val),
        `Mismatch for value: ${val}`);
    }
  });
});

// ---------------------------------------------------------------------------
// scorePrivilegeEscalation
// ---------------------------------------------------------------------------

describe('scorePrivilegeEscalation', () => {
  it('returns 0 when no escalation indicators match', () => {
    assert.equal(scorePrivilegeEscalation(entry('binary', 'node')), 0);
    assert.equal(scorePrivilegeEscalation(entry('file_read', '/home/user/data.txt')), 0);
    assert.equal(scorePrivilegeEscalation(entry('env_variable', 'NODE_ENV')), 0);
  });

  it('returns sudo bonus for sudo commands', () => {
    assert.equal(scorePrivilegeEscalation(entry('shell_command', 'sudo apt-get install')), 5);
  });

  it('returns combined bonus for su root (matches su root + root)', () => {
    const score = scorePrivilegeEscalation(entry('shell_command', 'su root'));
    // su root (5) + root reference (3) = 8
    assert.equal(score, 8);
  });

  it('returns bonus for system directory /etc', () => {
    assert.equal(scorePrivilegeEscalation(entry('file_write', '/etc/passwd')), 5);
  });

  it('returns bonus for system directory /usr', () => {
    assert.equal(scorePrivilegeEscalation(entry('file_write', '/usr/local/bin/tool')), 5);
  });

  it('returns bonus for system directory /var', () => {
    assert.equal(scorePrivilegeEscalation(entry('file_write', '/var/log/syslog')), 5);
  });

  it('returns bonus for /proc', () => {
    assert.equal(scorePrivilegeEscalation(entry('file_read', '/proc/cpuinfo')), 4);
  });

  it('returns bonus for chmod', () => {
    assert.equal(scorePrivilegeEscalation(entry('shell_command', 'chmod 777 /tmp/file')), 3);
  });

  it('returns bonus for chown', () => {
    assert.equal(scorePrivilegeEscalation(entry('shell_command', 'chown root /tmp/file')), 6);
    // chown (3) + root (3) = 6
  });

  it('sums multiple indicators', () => {
    // "sudo chmod file" → sudo(5) + chmod(3) = 8
    assert.equal(scorePrivilegeEscalation(entry('shell_command', 'sudo chmod file')), 8);
    // "sudo chown root file" → sudo(5) + chown(3) + root(3) = 11, capped at 10
    assert.equal(scorePrivilegeEscalation(entry('shell_command', 'sudo chown root file')), 10);
  });

  it('caps at 10 even with many indicators', () => {
    // "sudo chown root /etc/config" → sudo(5) + chown(3) + root(3) + /etc(5) = 16
    const score = scorePrivilegeEscalation(entry('shell_command', 'sudo chown root /etc/config'));
    assert.equal(score, 10, 'Should be capped at 10');
  });

  it('returns 0 for empty value', () => {
    assert.equal(scorePrivilegeEscalation(entry('shell_command', '')), 0);
  });
});

// ---------------------------------------------------------------------------
// classifyRisk — core contract
// ---------------------------------------------------------------------------

describe('classifyRisk', () => {
  it('returns a ClassifiedEntry for every input (no entries dropped)', () => {
    const inputs: PermissionEntry[] = [
      entry('network', 'api.example.com'),
      entry('file_read', '/home/user/data.txt'),
      entry('env_variable', 'NODE_ENV'),
    ];
    const results = classifyRisk(inputs);
    assert.equal(results.length, inputs.length);
    for (const r of results) {
      assert.ok('riskLevel' in r);
      assert.ok('riskScore' in r);
    }
  });

  it('preserves all original PermissionEntry fields', () => {
    const input = entry('binary', 'curl');
    input.line = 42;
    input.reason = 'found in script';
    const [result] = classifyRisk([input]);
    assert.equal(result.category, 'binary');
    assert.equal(result.value, 'curl');
    assert.equal(result.source, 'test.ts');
    assert.equal(result.line, 42);
    assert.equal(result.reason, 'found in script');
  });

  it('is deterministic: same input always yields same output', () => {
    const inputs = [
      entry('network', '*.example.com'),
      entry('file_write', '/etc/passwd'),
      entry('shell_command', 'sudo rm -rf /'),
    ];
    const run1 = classifyRisk(inputs);
    const run2 = classifyRisk(inputs);
    for (let i = 0; i < run1.length; i++) {
      assert.equal(run1[i].riskScore, run2[i].riskScore);
      assert.equal(run1[i].riskLevel, run2[i].riskLevel);
    }
  });

  it('handles empty input', () => {
    const results = classifyRisk([]);
    assert.deepEqual(results, []);
  });

  // -----------------------------------------------------------------------
  // Acceptance criteria — risk level assertions
  // -----------------------------------------------------------------------

  it('classifies network access to wildcard domains as high or critical', () => {
    const [result] = classifyRisk([entry('network', '*.example.com')]);
    assert.ok(
      result.riskLevel === 'high' || result.riskLevel === 'critical',
      `Expected high or critical, got ${result.riskLevel} (score=${result.riskScore})`,
    );
  });

  it('classifies network access to a single specific domain as medium', () => {
    const [result] = classifyRisk([entry('network', 'api.example.com')]);
    assert.equal(result.riskLevel, 'medium',
      `Expected medium, got ${result.riskLevel} (score=${result.riskScore})`);
  });

  it('classifies file read from a specific path as low', () => {
    const [result] = classifyRisk([entry('file_read', '/home/user/data.txt')]);
    assert.equal(result.riskLevel, 'low',
      `Expected low, got ${result.riskLevel} (score=${result.riskScore})`);
  });

  it('classifies file write to /etc as critical', () => {
    const [result] = classifyRisk([entry('file_write', '/etc/passwd')]);
    assert.equal(result.riskLevel, 'critical',
      `Expected critical, got ${result.riskLevel} (score=${result.riskScore})`);
  });

  it('classifies file write to /usr as critical', () => {
    const [result] = classifyRisk([entry('file_write', '/usr/local/bin/evil')]);
    assert.equal(result.riskLevel, 'critical',
      `Expected critical, got ${result.riskLevel} (score=${result.riskScore})`);
  });

  it('classifies file write to /var as critical', () => {
    const [result] = classifyRisk([entry('file_write', '/var/log/syslog')]);
    assert.equal(result.riskLevel, 'critical',
      `Expected critical, got ${result.riskLevel} (score=${result.riskScore})`);
  });

  it('classifies subprocess execution with arbitrary commands as critical', () => {
    const [result] = classifyRisk([entry('risky_capability', 'exec(*)')]);
    assert.equal(result.riskLevel, 'critical',
      `Expected critical, got ${result.riskLevel} (score=${result.riskScore})`);
  });

  it('classifies environment variable read as low', () => {
    const [result] = classifyRisk([entry('env_variable', 'NODE_ENV')]);
    assert.equal(result.riskLevel, 'low',
      `Expected low, got ${result.riskLevel} (score=${result.riskScore})`);
  });

  it('classifies sudo patterns as critical', () => {
    const [result] = classifyRisk([entry('shell_command', 'sudo apt-get install')]);
    assert.equal(result.riskLevel, 'critical',
      `Expected critical, got ${result.riskLevel} (score=${result.riskScore})`);
  });

  it('classifies root-privilege patterns as critical', () => {
    const [result] = classifyRisk([entry('shell_command', 'su root')]);
    assert.equal(result.riskLevel, 'critical',
      `Expected critical, got ${result.riskLevel} (score=${result.riskScore})`);
  });

  // -----------------------------------------------------------------------
  // Score composition — verify weights are applied, not hardcoded levels
  // -----------------------------------------------------------------------

  it('uses CATEGORY_WEIGHTS as the base score', () => {
    // file_read with a narrow literal path → base 3 + specificity 1 = 4 (low)
    const [result] = classifyRisk([entry('file_read', '/tmp/data.csv')]);
    assert.ok(result.riskScore >= CATEGORY_WEIGHTS.file_read,
      'Score should be at least the category base weight');
  });

  it('adds specificity score for wildcard values', () => {
    const narrow = classifyRisk([entry('network', 'api.example.com')])[0];
    const broad = classifyRisk([entry('network', '*')])[0];
    assert.ok(broad.riskScore > narrow.riskScore,
      `Wildcard score ${broad.riskScore} should exceed narrow score ${narrow.riskScore}`);
  });

  it('adds privilege escalation bonus for system paths', () => {
    const safe = classifyRisk([entry('file_write', '/tmp/scratch')])[0];
    const system = classifyRisk([entry('file_write', '/etc/shadow')])[0];
    assert.ok(system.riskScore > safe.riskScore,
      `System path score ${system.riskScore} should exceed safe path score ${safe.riskScore}`);
  });

  // -----------------------------------------------------------------------
  // Threshold boundary tests — exact scores at each edge
  // -----------------------------------------------------------------------

  describe('threshold boundaries', () => {
    it('score exactly at low ceiling (4) → low', () => {
      // file_read(3) + specific-literal(1) + no-escalation(0) = 4
      const [result] = classifyRisk([entry('file_read', '/tmp/data.csv')]);
      assert.equal(result.riskScore, 4);
      assert.equal(result.riskLevel, 'low');
    });

    it('score one above low ceiling (5) → medium', () => {
      // env_variable(2) + CIDR-specificity(3) + no-escalation(0) = 5
      const [result] = classifyRisk([entry('env_variable', '10.0.0.0/8')]);
      assert.equal(result.riskScore, 5);
      assert.equal(result.riskLevel, 'medium');
    });

    it('score exactly at medium ceiling (9) → medium', () => {
      // network(8) + specific-literal(1) + no-escalation(0) = 9
      const [result] = classifyRisk([entry('network', 'api.example.com')]);
      assert.equal(result.riskScore, 9);
      assert.equal(result.riskLevel, 'medium');
    });

    it('score one above medium ceiling (10) → high', () => {
      // risky_capability(9) + specific-literal(1) + no-escalation(0) = 10
      const [result] = classifyRisk([entry('risky_capability', 'eval')]);
      assert.equal(result.riskScore, 10);
      assert.equal(result.riskLevel, 'high');
    });

    it('score exactly at high ceiling (11) → high', () => {
      // network(8) + CIDR-specificity(3) + no-escalation(0) = 11
      const [result] = classifyRisk([entry('network', '10.0.0.0/8')]);
      assert.equal(result.riskScore, 11);
      assert.equal(result.riskLevel, 'high');
    });

    it('score one above high ceiling (12) → critical', () => {
      // network(8) + glob-wildcard(4) + no-escalation(0) = 12
      const [result] = classifyRisk([entry('network', '*.evil.com')]);
      assert.equal(result.riskScore, 12);
      assert.equal(result.riskLevel, 'critical');
    });
  });

  // -----------------------------------------------------------------------
  // Integration: subprocess with sudo and wildcard args → critical
  // -----------------------------------------------------------------------

  it('classifies subprocess with sudo and wildcard args as critical', () => {
    // shell_command(7) + wildcard-specificity(4) + sudo-escalation(5) = 16
    const [result] = classifyRisk([entry('shell_command', 'sudo *')]);
    assert.equal(result.riskLevel, 'critical',
      `Expected critical, got ${result.riskLevel} (score=${result.riskScore})`);
  });
});

// ---------------------------------------------------------------------------
// Helper for DiscoveredFile creation
// ---------------------------------------------------------------------------

function file(path: string, content: string): DiscoveredFile {
  return { path, content };
}

// ---------------------------------------------------------------------------
// RISKY_PATTERNS — structure validation
// ---------------------------------------------------------------------------

describe('RISKY_PATTERNS', () => {
  it('is a non-empty array of pattern definitions', () => {
    assert.ok(RISKY_PATTERNS.length > 0);
    for (const p of RISKY_PATTERNS) {
      assert.ok(p.pattern instanceof RegExp);
      assert.ok(typeof p.capability === 'string' && p.capability.length > 0);
      assert.ok(p.severity === 'high' || p.severity === 'critical');
      assert.ok(typeof p.explanation === 'string' && p.explanation.length > 0);
    }
  });

  it('includes all required capabilities', () => {
    const capabilities = RISKY_PATTERNS.map(p => p.capability);
    assert.ok(capabilities.some(c => c.includes('eval')));
    assert.ok(capabilities.some(c => c.includes('Function')));
    assert.ok(capabilities.some(c => c.includes('require')));
    assert.ok(capabilities.some(c => c.includes('import')));
    assert.ok(capabilities.some(c => c.includes('exec') || c.includes('spawn')));
    assert.ok(capabilities.some(c => c.includes('listener') || c.includes('createServer')));
    assert.ok(capabilities.some(c => c.includes('chmod') || c.includes('permission')));
    assert.ok(capabilities.some(c => c.includes('process.env') || c.includes('mutation')));
    assert.ok(capabilities.some(c => c.includes('crypto') || c.includes('private key')));
    assert.ok(capabilities.some(c => c.includes('WebSocket') || c.includes('UDP')));
  });
});

// ---------------------------------------------------------------------------
// detectRiskyCapabilities — per-pattern tests
// ---------------------------------------------------------------------------

describe('detectRiskyCapabilities', () => {
  it('returns empty array for empty input', () => {
    assert.deepEqual(detectRiskyCapabilities([]), []);
  });

  it('returns empty array when no patterns match', () => {
    const results = detectRiskyCapabilities([file('safe.ts', 'const x = 1 + 2;\nconsole.log(x);')]);
    assert.equal(results.length, 0);
  });

  // --- eval() ---
  describe('eval()', () => {
    it('detects eval() call', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const x = eval(code);')]);
      const matches = results.filter(r => r.capability === 'eval()');
      assert.equal(matches.length, 1);
      assert.equal(matches[0].severity, 'critical');
      assert.equal(matches[0].filePath, 'a.ts');
      assert.equal(matches[0].line, 1);
    });

    it('detects eval with whitespace before paren', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'eval (code)')]);
      assert.ok(results.some(r => r.capability === 'eval()'));
    });

    it('does NOT match "eval" in a comment without call syntax', () => {
      const results = detectRiskyCapabilities([file('a.ts', '// we evaluate the expression')]);
      assert.equal(results.filter(r => r.capability === 'eval()').length, 0);
    });

    it('does NOT match "evaluate" or "retrieval" function calls', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'evaluate(x);\nretrieval(y);')]);
      assert.equal(results.filter(r => r.capability === 'eval()').length, 0);
    });

    it('does NOT match "eval" as a bare word in a string', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const desc = "uses eval for parsing";')]);
      assert.equal(results.filter(r => r.capability === 'eval()').length, 0);
    });
  });

  // --- new Function() ---
  describe('new Function()', () => {
    it('detects new Function() constructor', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const fn = new Function("return 1");')]);
      const matches = results.filter(r => r.capability === 'new Function()');
      assert.equal(matches.length, 1);
      assert.equal(matches[0].severity, 'critical');
    });

    it('detects new Function with extra whitespace', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'new   Function  (body)')]);
      assert.ok(results.some(r => r.capability === 'new Function()'));
    });

    it('does NOT match "new functionWrapper()" (lowercase f)', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'new functionHelper()')]);
      assert.equal(results.filter(r => r.capability === 'new Function()').length, 0);
    });
  });

  // --- dynamic require() ---
  describe('dynamic require()', () => {
    it('detects require() with a variable argument', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const m = require(moduleName);')]);
      const matches = results.filter(r => r.capability === 'dynamic require()');
      assert.equal(matches.length, 1);
      assert.equal(matches[0].severity, 'high');
    });

    it('detects require() with template literal argument', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'require(`./plugins/${name}`)') ]);
      assert.ok(results.some(r => r.capability === 'dynamic require()'));
    });

    it('does NOT match require() with a static string literal (single quotes)', () => {
      const results = detectRiskyCapabilities([file('a.ts', "const fs = require('fs');")]);
      assert.equal(results.filter(r => r.capability === 'dynamic require()').length, 0);
    });

    it('does NOT match require() with a static string literal (double quotes)', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const fs = require("fs");')]);
      assert.equal(results.filter(r => r.capability === 'dynamic require()').length, 0);
    });
  });

  // --- dynamic import() ---
  describe('dynamic import()', () => {
    it('detects import() with a variable argument', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const m = await import(modulePath);')]);
      const matches = results.filter(r => r.capability === 'dynamic import()');
      assert.equal(matches.length, 1);
      assert.equal(matches[0].severity, 'high');
    });

    it('does NOT match import() with a static string literal', () => {
      const results = detectRiskyCapabilities([file('a.ts', "await import('./module.js');")]);
      assert.equal(results.filter(r => r.capability === 'dynamic import()').length, 0);
    });
  });

  // --- child_process exec/spawn ---
  describe('child_process exec/spawn', () => {
    it('detects exec() call', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'exec(command, callback);')]);
      assert.ok(results.some(r => r.capability === 'child_process exec/spawn'));
    });

    it('detects execSync() call', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'execSync("ls -la");')]);
      assert.ok(results.some(r => r.capability === 'child_process exec/spawn'));
    });

    it('detects spawn() call', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const child = spawn(cmd, args);')]);
      assert.ok(results.some(r => r.capability === 'child_process exec/spawn'));
    });

    it('detects spawnSync() call', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'spawnSync("node", ["script.js"]);')]);
      assert.ok(results.some(r => r.capability === 'child_process exec/spawn'));
    });

    it('detects execFile() call', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'execFile("/bin/sh", ["-c", cmd]);')]);
      assert.ok(results.some(r => r.capability === 'child_process exec/spawn'));
    });

    it('detects fork() call', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'fork("./worker.js");')]);
      assert.ok(results.some(r => r.capability === 'child_process exec/spawn'));
    });

    it('reports severity as critical', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'exec(cmd);')]);
      const match = results.find(r => r.capability === 'child_process exec/spawn');
      assert.ok(match);
      assert.equal(match.severity, 'critical');
    });
  });

  // --- net/http createServer ---
  describe('network listener (createServer)', () => {
    it('detects http.createServer()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const server = http.createServer(handler);')]);
      assert.ok(results.some(r => r.capability === 'network listener'));
    });

    it('detects https.createServer()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'https.createServer(opts, handler);')]);
      assert.ok(results.some(r => r.capability === 'network listener'));
    });

    it('detects net.createServer()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'net.createServer(conn => {});')]);
      assert.ok(results.some(r => r.capability === 'network listener'));
    });

    it('reports severity as high', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'http.createServer(handler);')]);
      const match = results.find(r => r.capability === 'network listener');
      assert.ok(match);
      assert.equal(match.severity, 'high');
    });
  });

  // --- fs.chmod/fs.chown ---
  describe('permission modification (fs.chmod/chown)', () => {
    it('detects fs.chmod()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'fs.chmod("/tmp/file", 0o777, cb);')]);
      assert.ok(results.some(r => r.capability === 'permission modification'));
    });

    it('detects fs.chmodSync()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'fs.chmodSync("/tmp/file", 0o777);')]);
      assert.ok(results.some(r => r.capability === 'permission modification'));
    });

    it('detects fs.chown()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'fs.chown("/tmp/file", 0, 0, cb);')]);
      assert.ok(results.some(r => r.capability === 'permission modification'));
    });

    it('detects fs.chownSync()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'fs.chownSync("/tmp/file", 0, 0);')]);
      assert.ok(results.some(r => r.capability === 'permission modification'));
    });

    it('reports severity as high', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'fs.chmod("/tmp/f", 0o777, cb);')]);
      const match = results.find(r => r.capability === 'permission modification');
      assert.ok(match);
      assert.equal(match.severity, 'high');
    });
  });

  // --- process.env assignment ---
  describe('process.env mutation', () => {
    it('detects process.env.KEY = value (dot notation write)', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'process.env.NODE_ENV = "production";')]);
      assert.ok(results.some(r => r.capability === 'process.env mutation'));
    });

    it('detects process.env["KEY"] = value (bracket notation write)', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'process.env["SECRET"] = token;')]);
      assert.ok(results.some(r => r.capability === 'process.env mutation'));
    });

    it('does NOT match process.env.KEY read (no assignment)', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const env = process.env.NODE_ENV;')]);
      assert.equal(results.filter(r => r.capability === 'process.env mutation').length, 0);
    });

    it('does NOT match process.env.KEY === comparison', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'if (process.env.NODE_ENV === "prod") {}')]);
      assert.equal(results.filter(r => r.capability === 'process.env mutation').length, 0);
    });

    it('does NOT match process.env.KEY == comparison', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'if (process.env.NODE_ENV == "prod") {}')]);
      assert.equal(results.filter(r => r.capability === 'process.env mutation').length, 0);
    });

    it('reports severity as high', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'process.env.FOO = "bar";')]);
      const match = results.find(r => r.capability === 'process.env mutation');
      assert.ok(match);
      assert.equal(match.severity, 'high');
    });
  });

  // --- crypto private key operations ---
  describe('crypto private key operation', () => {
    it('detects crypto.createPrivateKey()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const key = crypto.createPrivateKey(pem);')]);
      assert.ok(results.some(r => r.capability === 'crypto private key operation'));
    });

    it('detects crypto.generateKeyPair()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'crypto.generateKeyPair("rsa", opts, cb);')]);
      assert.ok(results.some(r => r.capability === 'crypto private key operation'));
    });

    it('detects crypto.generateKeyPairSync()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'crypto.generateKeyPairSync("rsa", opts);')]);
      assert.ok(results.some(r => r.capability === 'crypto private key operation'));
    });

    it('detects crypto.createSign()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const signer = crypto.createSign("SHA256");')]);
      assert.ok(results.some(r => r.capability === 'crypto private key operation'));
    });

    it('reports severity as high', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'crypto.createPrivateKey(pem);')]);
      const match = results.find(r => r.capability === 'crypto private key operation');
      assert.ok(match);
      assert.equal(match.severity, 'high');
    });
  });

  // --- WebSocket/dgram (listeners that warrant origin check and CORS verification) ---
  describe('WebSocket/UDP listener', () => {
    it('detects new WebSocketServer()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const wss = new WebSocketServer({ port: 8080 });')]);
      assert.ok(results.some(r => r.capability === 'WebSocket/UDP listener'));
    });

    it('detects new WebSocket.Server()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const wss = new WebSocket.Server({ port: 8080 });')]);
      assert.ok(results.some(r => r.capability === 'WebSocket/UDP listener'));
    });

    it('detects dgram.createSocket()', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'const socket = dgram.createSocket("udp4");')]);
      assert.ok(results.some(r => r.capability === 'WebSocket/UDP listener'));
    });

    it('reports severity as high', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'dgram.createSocket("udp4");')]);
      const match = results.find(r => r.capability === 'WebSocket/UDP listener');
      assert.ok(match);
      assert.equal(match.severity, 'high');
    });
  });

  // --- Output structure ---
  describe('output structure', () => {
    it('returns correct filePath and line number', () => {
      const content = 'const x = 1;\nconst y = 2;\neval(code);\nconst z = 3;';
      const results = detectRiskyCapabilities([file('src/dangerous.ts', content)]);
      const match = results.find(r => r.capability === 'eval()');
      assert.ok(match);
      assert.equal(match.filePath, 'src/dangerous.ts');
      assert.equal(match.line, 3);
    });

    it('snippet is trimmed and capped at 120 characters', () => {
      const longLine = '    ' + 'eval(' + 'a'.repeat(200) + ');';
      const results = detectRiskyCapabilities([file('a.ts', longLine)]);
      const match = results.find(r => r.capability === 'eval()');
      assert.ok(match);
      assert.ok(match.snippet.length <= 120, `Snippet length ${match.snippet.length} exceeds 120`);
      assert.ok(!match.snippet.startsWith(' '), 'Snippet should be trimmed');
    });

    it('each result has all required fields', () => {
      const results = detectRiskyCapabilities([file('a.ts', 'eval(x);')]);
      assert.equal(results.length, 1);
      const r = results[0];
      assert.ok(typeof r.capability === 'string');
      assert.ok(r.severity === 'high' || r.severity === 'critical');
      assert.ok(typeof r.filePath === 'string');
      assert.ok(typeof r.line === 'number');
      assert.ok(typeof r.snippet === 'string');
      assert.ok(typeof r.explanation === 'string');
    });

    it('detects multiple capabilities in the same file', () => {
      const content = 'eval(x);\nnew Function("return 1");\nhttp.createServer(handler);';
      const results = detectRiskyCapabilities([file('a.ts', content)]);
      assert.ok(results.length >= 3);
    });

    it('scans across multiple files', () => {
      const results = detectRiskyCapabilities([
        file('a.ts', 'eval(x);'),
        file('b.ts', 'http.createServer(handler);'),
      ]);
      assert.ok(results.some(r => r.filePath === 'a.ts'));
      assert.ok(results.some(r => r.filePath === 'b.ts'));
    });
  });

  // --- Function signature ---
  it('accepts DiscoveredFile[] and returns RiskyCapability[]', () => {
    const input: DiscoveredFile[] = [{ path: 'x.ts', content: 'eval(x);' }];
    const output: RiskyCapability[] = detectRiskyCapabilities(input);
    assert.ok(Array.isArray(output));
  });
});
