// @ts-nocheck
import { describe, it, assert, beforeEach, afterEach, vi } from 'vitest';

import { PATTERNS  } from '../src/patterns';

describe('P1: Rule Explainability Verification', () => {
    it('All static patterns must have remediation metadata', () => {
        const failures = [];
        for (const p of PATTERNS) {
            if (!p.rationale || !p.remediationHint || !p.exploitPrecondition) {
                failures.push(p.id);
            }
        }
        
        if (failures.length > 0) {
            console.log('Failing patterns:', failures);
        }
        
        assert.ok(failures.length === 0, `Missing explanation metadata in ${failures.length} patterns.`);
    });
});
