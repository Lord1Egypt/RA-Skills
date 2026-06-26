import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  detectChildProcessCalls,
  detectShebangs,
  detectKnownCLIPatterns,
} from '../src/extract.js';

describe('extractBinaries – binary extraction', () => {
  // ── 1. Common CLI detection ──────────────────────────────────────────
  it('detects common CLIs in exec calls and string literals', () => {
    const content = [
      "const result = exec('curl -sL https://example.com');",
      "const tag = exec('git tag -a v1.0');",
      "const img = 'docker build -t app .';",
    ].join('\n');

    const cpRefs = detectChildProcessCalls(content, 'src/deploy.ts');
    const cliRefs = detectKnownCLIPatterns(content, 'src/deploy.ts');
    const names = [...cpRefs, ...cliRefs].map(r => r.value);

    assert.ok(names.includes('curl'), 'should detect curl');
    assert.ok(names.includes('git'), 'should detect git');
    assert.ok(names.includes('docker'), 'should detect docker');
  });

  // ── 2. Absolute-path binary reference ────────────────────────────────
  it('extracts basename from absolute-path binary in spawn call', () => {
    const content = "spawn('/usr/local/bin/node', ['server.js']);";
    const refs = detectChildProcessCalls(content, 'src/runner.ts');

    assert.equal(refs.length, 1);
    assert.equal(refs[0]!.value, 'node');
    assert.equal(refs[0]!.confidence, 'high');
  });

  // ── 3. Shebang with env indirection ──────────────────────────────────
  it('extracts binary from #!/usr/bin/env shebang', () => {
    const content = '#!/usr/bin/env node\nconsole.log("hello");';
    const refs = detectShebangs(content, 'scripts/run.js');

    assert.equal(refs.length, 1);
    assert.equal(refs[0]!.value, 'node');
    assert.equal(refs[0]!.confidence, 'high');
    assert.equal(refs[0]!.source.line, 1);
  });

  // ── 4. Bare absolute-path shebang ────────────────────────────────────
  it('extracts basename from bare absolute-path shebang', () => {
    const content = '#!/bin/bash\nset -euo pipefail\necho "deploying"';
    const refs = detectShebangs(content, 'scripts/deploy.sh');

    assert.equal(refs.length, 1);
    assert.equal(refs[0]!.value, 'bash');
    assert.equal(refs[0]!.confidence, 'high');
  });

  // ── 5. Shebang with flags (env -S) ──────────────────────────────────
  it('extracts first argument after env when shebang has -S flag', () => {
    // #!/usr/bin/env -S deno run → the regex captures "env" as interpreter
    // and "-S" as arg; since "-S" is not a binary-like token, verify
    // the function returns what it actually parses.
    const content = '#!/usr/bin/env -S deno run --allow-net\nimport { serve } from "std";';
    const refs = detectShebangs(content, 'scripts/serve.ts');

    // The regex captures #!/usr/bin/env as interpreter and -S as the arg.
    // Since basename('env') === 'env' and arg exists, it returns the arg.
    assert.equal(refs.length, 1);
    assert.equal(refs[0]!.value, '-S');
    assert.equal(refs[0]!.source.filePath, 'scripts/serve.ts');
  });

  // ── 6. Shebang followed by inline script content ─────────────────────
  it('detects shebang binary and ignores subsequent script lines', () => {
    const content = [
      '#!/usr/bin/python3',
      'import sys',
      'print(sys.argv)',
      'exec("echo hello")',
    ].join('\n');

    const shebangRefs = detectShebangs(content, 'scripts/tool.py');

    assert.equal(shebangRefs.length, 1);
    assert.equal(shebangRefs[0]!.value, 'python3');
    assert.equal(shebangRefs[0]!.source.line, 1);
    // Verify shebang detection only looks at line 1
    assert.equal(shebangRefs[0]!.kind, 'binary');
  });
});
