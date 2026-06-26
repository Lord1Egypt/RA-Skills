import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { GuardScanner } from '../src/scanner';

function makeSkillFixture(): string {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'guard-skill-root-'));
  fs.writeFileSync(
    path.join(root, 'SKILL.md'),
    `---\nname: sample-skill\ndescription: \"Sample skill\"\n---\n\n# Sample Skill\n\nSee references/api_reference.md and scripts/example.py for details.`,
  );
  fs.mkdirSync(path.join(root, 'references'), { recursive: true });
  fs.writeFileSync(path.join(root, 'references', 'api_reference.md'), '# ref\n');
  fs.mkdirSync(path.join(root, 'scripts'), { recursive: true });
  fs.writeFileSync(path.join(root, 'scripts', 'example.py'), 'print("ok")\n');
  fs.mkdirSync(path.join(root, 'tests'), { recursive: true });
  fs.writeFileSync(path.join(root, 'tests', 'example.test.ts'), 'export {};\n');
  fs.mkdirSync(path.join(root, 'assets'), { recursive: true });
  fs.writeFileSync(path.join(root, 'assets', 'note.txt'), 'asset\n');
  fs.mkdirSync(path.join(root, 'tests', '__pycache__'), { recursive: true });
  fs.writeFileSync(path.join(root, 'tests', '__pycache__', 'temp.cpython-314.pyc'), 'x');
  return root;
}

describe('skill root structural noise', () => {
  it('does not emit STRUCT_NO_SKILLMD for child resource directories inside a valid skill root', () => {
    const skillRoot = makeSkillFixture();
    const scanner = new GuardScanner({ summaryOnly: true, strict: true });
    scanner.scanDirectory(skillRoot);
    const ids = scanner.findings.flatMap((entry: any) => entry.findings.map((f: any) => `${entry.skill}:${f.id}`));

    expect(ids).not.toContain('references:STRUCT_NO_SKILLMD');
    expect(ids).not.toContain('scripts:STRUCT_NO_SKILLMD');
    expect(ids).not.toContain('tests:STRUCT_NO_SKILLMD');
    expect(ids).not.toContain('assets:STRUCT_NO_SKILLMD');
    expect(ids).not.toContain('__pycache__:STRUCT_NO_SKILLMD');
  });
});
