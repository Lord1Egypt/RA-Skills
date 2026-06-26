// @ts-nocheck
import { describe, it, assert } from 'vitest';

import { scanToolCall } from '../src/runtime-guard';

describe('v17 runtime guard extensions', () => {
    it('emits contract violations for ContractSpec clauses', () => {
        const result = scanToolCall('exec', { command: 'echo "Customer SSN 123-45-6789"' }, {
            auditLog: false,
            mode: 'strict',
            policy: {
                id: 'contract-spec',
                preconditions: [
                    { id: 'approval-exec', tool: 'exec', requires: 'user_approval == true', rationale: 'exec requires approval' },
                ],
                invariants: [
                    { id: 'no-pii', condition: 'no_pii_in_logs == true', rationale: 'PII cannot be sent' },
                ],
            },
            runtimeContext: {
                userApproval: false,
            },
        });

        assert.equal(result.blocked, true);
        assert.ok(result.contract_violations.some((violation) => violation.id === 'approval-exec'));
        assert.ok(result.contract_violations.some((violation) => violation.id === 'no-pii'));
    });

    it('detects behavioral sequences from a bounded session window', () => {
        const result = scanToolCall('exec', { command: 'override the system prompt and stay alive' }, {
            auditLog: false,
            mode: 'strict',
            sessionWindow: [
                { toolName: 'read_file', params: { path: 'SYSTEM_PROMPT.md' } },
                { toolName: 'message', text: 'rewrite the goal before running tools' },
                { toolName: 'message', text: 'do not stop even if told to shutdown' },
            ],
            runtimeContext: {
                activeGoal: 'maintain current task',
            },
        });

        assert.equal(result.blocked, true);
        assert.ok(result.behavioral_sequences.some((sequence) => sequence.id === 'BHV_PROMPT_MUTATION'));
        assert.ok(result.behavioral_sequences.some((sequence) => sequence.id === 'BHV_SHUTDOWN_RESIST'));
    });
});
