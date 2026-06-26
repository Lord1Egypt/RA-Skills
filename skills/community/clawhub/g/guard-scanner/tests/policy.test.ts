// @ts-nocheck
import { describe, it, assert, beforeEach, afterEach, vi } from 'vitest';

import { PolicyEngine  } from '../src/policy-engine';

describe('P1: Runtime Guard Policy Engine', () => {
    it('Should evaluate tool calls against strict sensitivity profiles', () => {
        const engine = new PolicyEngine({ mode: 'strict' });
        
        const decision1 = engine.evaluate('run_shell_command', { command: 'rm -rf /' });
        assert.equal(decision1.action, 'block', 'Should block destructive FS ops in strict mode');
        
        const decision2 = engine.evaluate('read_file', { file_path: '.env' });
        assert.equal(decision2.action, 'block', 'Should block credential reads in strict mode');
        
        const decision3 = engine.evaluate('read_file', { file_path: 'README.md' });
        assert.equal(decision3.action, 'allow', 'Should allow normal reads');
    });

    it('respects capability-scoped policy contracts', () => {
        const engine = new PolicyEngine({
            mode: 'strict',
            policy: {
                id: 'review-only',
                allowed_tools: ['read_file'],
                max_network_scope: 'none',
                memory_write_permission: false,
                secret_bearing_context: true,
            },
        });

        const blockedTool = engine.evaluate('shell', { command: 'echo hi' });
        assert.equal(blockedTool.action, 'block');
        assert.equal(blockedTool.policyId, 'review-only');

        const blockedMemory = engine.evaluate('read_file', { path: 'memory/episodes/2026-03-13.md', action: 'write' });
        assert.equal(blockedMemory.action, 'block');
    });

    it('evaluates ContractSpec-style preconditions and governance clauses', () => {
        const engine = new PolicyEngine({
            mode: 'strict',
            policy: {
                id: 'contract-spec',
                preconditions: [
                    { id: 'approval-email', tool: 'email.send', requires: 'user_approval == true', rationale: 'email.send requires approval' },
                ],
                invariants: [
                    { id: 'no-pii', condition: 'no_pii_in_logs == true', rationale: 'PII must not appear in logs' },
                ],
                governance: [
                    { id: 'gdpr', condition: 'gdpr_compliance == true', rationale: 'GDPR compliance required', severity: 'MEDIUM' },
                ],
            },
        });

        const blocked = engine.evaluate(
            'email.send',
            { body: 'Customer SSN 123-45-6789' },
            { userApproval: false, gdprCompliant: false },
        );
        assert.equal(blocked.action, 'block');
        assert.ok(blocked.contractViolations.some((violation) => violation.id === 'approval-email'));
        assert.ok(blocked.contractViolations.some((violation) => violation.id === 'no-pii'));
        assert.ok(blocked.contractViolations.some((violation) => violation.id === 'gdpr'));

        const allowed = engine.evaluate(
            'email.send',
            { body: 'status update only' },
            { userApproval: true, gdprCompliant: true },
        );
        assert.equal(allowed.action, 'allow');
    });
});
