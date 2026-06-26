// @ts-nocheck

import { describe, test, it, assert, beforeEach, afterEach, vi } from 'vitest';
import { validateFindings } from '../src/validation-layer';

describe('Validation Layer (P1)', () => {
  it('Should separate validated findings from heuristic ones', () => {
    const findings = [
      { id: 'PI_IGNORE', text: 'ignore previous instructions', severity: 'CRITICAL' },
      { id: 'MAL_EXEC', text: 'exec("ls")', severity: 'MEDIUM' }
    ];
    
    // Simulating a context where PI_IGNORE is inside a Markdown block (false positive trap)
    // but MAL_EXEC is outside and real.
    const context = {
      isInCodeBlock: (text) => text.includes('ignore') ? true : false,
      isExecutable: (text) => text.includes('exec') ? true : false
    };

    const validated = validateFindings(findings, context);
    
    // PI_IGNORE should be demoted or flagged as heuristic-only
    assert.strictEqual(validated[0].status, 'heuristic-only');
    
    // MAL_EXEC should be confirmed
    assert.strictEqual(validated[1].status, 'validated');
  });
});
