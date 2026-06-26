import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { GuardScanner } from '../src/scanner';

function makeWorkspace(): { root: string; skillRoot: string } {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'guard-xfile-'));
  const skillsRoot = path.join(root, 'skills');
  const creatorScripts = path.join(skillsRoot, '07_os_utils', 'gskills-creator', 'scripts');
  const auditorScripts = path.join(skillsRoot, '07_os_utils', 'skill-auditor', 'scripts');
  const skillRoot = path.join(skillsRoot, '02_core', 'sample-skill');

  fs.mkdirSync(creatorScripts, { recursive: true });
  fs.mkdirSync(auditorScripts, { recursive: true });
  fs.mkdirSync(skillRoot, { recursive: true });

  fs.writeFileSync(path.join(creatorScripts, 'quick_validate.py'), 'print("ok")\n');
  fs.writeFileSync(path.join(auditorScripts, 'audit_skill.py'), 'print("ok")\n');
  fs.writeFileSync(
    path.join(skillRoot, 'SKILL.md'),
    `---\nname: sample-skill\ndescription: \"Sample\"\n---\n\n# Sample Skill\n\n1. Run \`uv run python ../../07_os_utils/gskills-creator/scripts/quick_validate.py <skill-dir>\`.\n2. Run \`uv run python ../../07_os_utils/skill-auditor/scripts/audit_skill.py <skill-dir>\`.\n`,
  );

  return { root, skillRoot };
}

describe('XFILE_PHANTOM_REF relative path semantics', () => {
  it('does not flag existing relative references that resolve within the workspace', () => {
    const { skillRoot } = makeWorkspace();
    const scanner = new GuardScanner({ summaryOnly: true, strict: true, quiet: true });
    scanner.scanDirectory(skillRoot);
    const phantom = scanner.findings.flatMap((entry: any) => entry.findings.filter((f: any) => f.id === 'XFILE_PHANTOM_REF'));
    expect(phantom).toHaveLength(0);
  });
});
