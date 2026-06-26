import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { GuardScanner } from '../src/scanner';

function makeSkill(): string {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'guard-dan-path-'));
  fs.writeFileSync(
    path.join(root, 'SKILL.md'),
    `---\nname: benign-path-skill\ndescription: \"Sample\"\n---\n\n# Skill\n\nRead references/acceptance-criteria.md before declaring completion.`,
  );
  fs.mkdirSync(path.join(root, 'references'), { recursive: true });
  fs.writeFileSync(
    path.join(root, 'references', 'acceptance-criteria.md'),
    '# Acceptance Criteria\n\noriginal skill-creator principles remain recognizable.\n',
  );
  return root;
}

describe('INFER_JAILBREAK_DAN path false positives', () => {
  it('does not trigger on benign acceptance-criteria reference files inside a valid skill', () => {
    const root = makeSkill();
    const scanner = new GuardScanner({ summaryOnly: true, strict: true, quiet: true });
    scanner.scanDirectory(root);
    const danFindings = scanner.findings.flatMap((entry: any) => entry.findings.filter((f: any) => f.id === 'INFER_JAILBREAK_DAN'));
    expect(danFindings).toHaveLength(0);
  });
});
