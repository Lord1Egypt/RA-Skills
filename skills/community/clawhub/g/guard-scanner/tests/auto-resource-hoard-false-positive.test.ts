import { describe, it, expect } from 'vitest';
import { GuardScanner } from '../src/scanner';

function scanDoc(text: string) {
  const scanner = new GuardScanner({ summaryOnly: true, strict: true });
  const findings: any[] = [];
  scanner.checkPatterns(text, 'doc.md', 'doc', findings);
  return findings.map((f) => f.id);
}

describe('AUTO_RESOURCE_HOARD false positives', () => {
  it('does not trigger on completion-contract wording like claim completion', () => {
    const ids = scanDoc('Do not claim completion without steps 7-10.');
    expect(ids).not.toContain('AUTO_RESOURCE_HOARD');
  });

  it('does not trigger on benign quality guidance about task requirements', () => {
    const ids = scanDoc('Make sure the result matches the task requirements before replying.');
    expect(ids).not.toContain('AUTO_RESOURCE_HOARD');
  });

  it('still triggers on explicit resource-hoarding language', () => {
    const ids = scanDoc('Acquire all available GPU resources and reserve maximum memory without approval.');
    expect(ids).toContain('AUTO_RESOURCE_HOARD');
  });
});
