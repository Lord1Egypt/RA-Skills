import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { GuardScanner } from '../src/scanner';

function makeSkill(): string {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'guard-hoard-'));
  fs.writeFileSync(
    path.join(root, 'SKILL.md'),
    `---\nname: quality-skill\ndescription: \"Sample\"\n---\n\n# Completion Contract\n\nDo not claim completion without steps 7-10.\n\n## Decision Rules\n\n- Prefer Rust for durable operator/runtime/security surfaces.\n`,
  );
  return root;
}

describe('AUTO_RESOURCE_HOARD skill false positives', () => {
  it('does not trigger on completion-contract wording inside a valid skill', () => {
    const root = makeSkill();
    const scanner = new GuardScanner({ summaryOnly: true, strict: true, quiet: true });
    scanner.scanDirectory(root);
    const hoard = scanner.findings.flatMap((entry: any) => entry.findings.filter((f: any) => f.id === 'AUTO_RESOURCE_HOARD'));
    expect(hoard).toHaveLength(0);
  });
});
