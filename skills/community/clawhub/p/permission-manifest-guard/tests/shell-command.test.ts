import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { extractShellCommands } from '../src/extract.js';
import type { DiscoveredFile } from '../src/types.js';

/** Creates a DiscoveredFile from an inline source string. */
function source(content: string, path = 'src/deploy.ts'): DiscoveredFile {
  return { path, content };
}

describe('extractShellCommands — shell command extraction', () => {
  // ── 1. exec with string literal ─────────────────────────────────────────
  it('extracts full command from exec() with a string literal', () => {
    const file = source([
      "import { exec } from 'child_process';",
      "exec('ls -la /tmp');",
    ].join('\n'));

    const cmds = extractShellCommands([file]);

    assert.equal(cmds.length, 1);
    assert.equal(cmds[0]!.command, 'ls -la /tmp');
    assert.equal(cmds[0]!.invocationMethod, 'child_process.exec');
    assert.equal(cmds[0]!.lineNumber, 2);
    assert.equal(cmds[0]!.sourceFile, 'src/deploy.ts');
  });

  // ── 2. exec with template literal containing interpolation ──────────────
  it('extracts full command from exec() with a template literal', () => {
    const file = source([
      "import { exec } from 'child_process';",
      "const cmd = 'docker';",
      "exec(`${cmd} build --tag myapp .`);",
    ].join('\n'));

    const cmds = extractShellCommands([file]);

    assert.equal(cmds.length, 1);
    assert.equal(cmds[0]!.command, '${cmd} build --tag myapp .');
    assert.equal(cmds[0]!.invocationMethod, 'child_process.exec');
    assert.equal(cmds[0]!.lineNumber, 3);
  });

  // ── 3. execSync variant ─────────────────────────────────────────────────
  it('extracts full command from execSync() call', () => {
    const file = source([
      "import { execSync } from 'child_process';",
      "execSync('rm -rf /tmp/x');",
    ].join('\n'));

    const cmds = extractShellCommands([file]);

    assert.equal(cmds.length, 1);
    assert.equal(cmds[0]!.command, 'rm -rf /tmp/x');
    assert.equal(cmds[0]!.invocationMethod, 'child_process.execSync');
    assert.equal(cmds[0]!.lineNumber, 2);
  });

  // ── 4. spawn with argument array ────────────────────────────────────────
  it('extracts binary name from spawn() with argument array', () => {
    const file = source([
      "import { spawn } from 'child_process';",
      "spawn('git', ['clone', 'https://github.com/user/repo.git']);",
    ].join('\n'));

    const cmds = extractShellCommands([file]);

    assert.equal(cmds.length, 1);
    assert.equal(cmds[0]!.command, 'git');
    assert.equal(cmds[0]!.invocationMethod, 'child_process.spawn');
    assert.equal(cmds[0]!.lineNumber, 2);
  });

  // ── 5. spawn with shell:true option ─────────────────────────────────────
  it('extracts binary name from spawn() with shell option', () => {
    const file = source([
      "import { spawn } from 'child_process';",
      "spawn('bash', ['-c', 'echo hi'], { shell: true });",
    ].join('\n'));

    const cmds = extractShellCommands([file]);

    assert.equal(cmds.length, 1);
    assert.equal(cmds[0]!.command, 'bash');
    assert.equal(cmds[0]!.invocationMethod, 'child_process.spawn');
    assert.equal(cmds[0]!.lineNumber, 2);
  });

  // ── 6. backtick / $() subshell in a shell script ───────────────────────
  it('extracts command from $() subshell pattern in a shell source', () => {
    const file = source([
      '#!/bin/bash',
      'RESULT=$(date +%Y-%m-%d)',
      'echo "Today: $RESULT"',
    ].join('\n'), 'scripts/check.sh');

    const cmds = extractShellCommands([file]);

    assert.equal(cmds.length, 1);
    assert.equal(cmds[0]!.command, 'date +%Y-%m-%d');
    assert.equal(cmds[0]!.invocationMethod, 'dollar_paren_subshell');
    assert.equal(cmds[0]!.lineNumber, 2);
    assert.equal(cmds[0]!.sourceFile, 'scripts/check.sh');
  });
});
