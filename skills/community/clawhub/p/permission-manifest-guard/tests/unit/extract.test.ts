import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { extractShellCommands, SHELL_PATTERNS, classifySecret, SAFE_ENV_VARS, extractEnvVars, extractJsEnvVars, extractPyEnvVars, extractShellEnvVars } from '../../src/extract.js';
import type { DiscoveredFile } from '../../src/types.js';
import type { EnvVar } from '../../src/extract.js';

describe('SHELL_PATTERNS', () => {
  it('exports a non-empty array of pattern objects with pattern and method', () => {
    assert.ok(SHELL_PATTERNS.length > 0);
    for (const entry of SHELL_PATTERNS) {
      assert.ok(entry.pattern instanceof RegExp);
      assert.ok(typeof entry.method === 'string');
    }
  });
});

describe('extractShellCommands', () => {
  it('detects subprocess APIs across JS, Python, and shell files', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/deploy.ts',
        content: [
          "import { exec, spawn, fork } from 'child_process';",
          "exec('git clone repo');",
          "spawn('docker', ['run']);",
          "execFile('/usr/bin/node', ['app.js']);",
          "fork('./worker.js');",
        ].join('\n'),
      },
      {
        path: 'scripts/build.py',
        content: [
          'import os, subprocess',
          "os.system('make clean')",
          "subprocess.run('pytest')",
          "subprocess.Popen('gunicorn app:app')",
        ].join('\n'),
      },
      {
        path: 'scripts/setup.sh',
        content: [
          '#!/bin/bash',
          'RESULT=`ls -la`',
          'FILES=$(find . -name "*.ts")',
        ].join('\n'),
      },
    ];

    const results = extractShellCommands(files);

    // JS detections
    const jsResults = results.filter(r => r.sourceFile === 'src/deploy.ts');
    const execResult = jsResults.find(r => r.invocationMethod === 'child_process.exec');
    assert.ok(execResult, 'should detect exec');
    assert.equal(execResult.command, 'git clone repo');
    assert.equal(execResult.lineNumber, 2);

    const spawnResult = jsResults.find(r => r.invocationMethod === 'child_process.spawn');
    assert.ok(spawnResult, 'should detect spawn');
    assert.equal(spawnResult.command, 'docker');

    const execFileResult = jsResults.find(r => r.invocationMethod === 'child_process.execFile');
    assert.ok(execFileResult, 'should detect execFile');
    assert.equal(execFileResult.command, 'node');

    const forkResult = jsResults.find(r => r.invocationMethod === 'child_process.fork');
    assert.ok(forkResult, 'should detect fork');
    assert.equal(forkResult.command, 'worker.js');

    // Python detections
    const pyResults = results.filter(r => r.sourceFile === 'scripts/build.py');
    const systemResult = pyResults.find(r => r.invocationMethod === 'os.system');
    assert.ok(systemResult, 'should detect os.system');
    assert.equal(systemResult.command, 'make clean');

    const subprocRun = pyResults.find(r => r.invocationMethod === 'subprocess.run');
    assert.ok(subprocRun, 'should detect subprocess.run');
    assert.equal(subprocRun.command, 'pytest');

    const popenResult = pyResults.find(r => r.invocationMethod === 'subprocess.Popen');
    assert.ok(popenResult, 'should detect subprocess.Popen');

    // Shell detections
    const shResults = results.filter(r => r.sourceFile === 'scripts/setup.sh');
    const backtickResult = shResults.find(r => r.invocationMethod === 'backtick_subshell');
    assert.ok(backtickResult, 'should detect backtick subshell');
    assert.equal(backtickResult.command, 'ls -la');
    assert.equal(backtickResult.lineNumber, 2);

    const dollarResult = shResults.find(r => r.invocationMethod === 'dollar_paren_subshell');
    assert.ok(dollarResult, 'should detect $() subshell');
    assert.ok(dollarResult.command.startsWith('find'));
  });

  it('does not match exec or spawn inside single-line comments', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/safe.ts',
        content: [
          "// exec('this should not match');",
          "// spawn('also ignored');",
          "  // execSync('indented comment');",
          "const x = 1; // exec('inline comment');",
        ].join('\n'),
      },
      {
        path: 'scripts/safe.py',
        content: [
          "# system('should not match')",
          "# subprocess.run('also ignored')",
        ].join('\n'),
      },
      {
        path: 'scripts/safe.sh',
        content: [
          '# `should not match`',
          '# $(also ignored)',
        ].join('\n'),
      },
    ];

    const results = extractShellCommands(files);
    assert.deepEqual(results, [], 'no matches should be found inside comments');
  });

  it('returns empty array for files with no subprocess usage', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/math.ts',
        content: [
          'const x = 42;',
          'function add(a: number, b: number) { return a + b; }',
          "const msg = 'hello world';",
        ].join('\n'),
      },
      {
        path: 'lib/utils.py',
        content: [
          'def greet(name):',
          '    return f"Hello {name}"',
        ].join('\n'),
      },
      {
        path: 'data/readme.txt',
        content: 'This file has an unsupported extension.',
      },
    ];

    const results = extractShellCommands(files);
    assert.deepEqual(results, []);
  });

  it('detects multiple matches per file across different lines', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/pipeline.ts',
        content: [
          "import { exec, execSync, spawn } from 'child_process';",
          "exec('npm install');",
          "execSync('npm run build');",
          "spawn('node', ['server.js']);",
          "exec('rm -rf dist');",
        ].join('\n'),
      },
    ];

    const results = extractShellCommands(files);

    assert.equal(results.length, 4, 'should find all four subprocess calls');
    assert.equal(results[0]!.command, 'npm install');
    assert.equal(results[0]!.lineNumber, 2);
    assert.equal(results[0]!.invocationMethod, 'child_process.exec');
    assert.equal(results[1]!.command, 'npm run build');
    assert.equal(results[1]!.lineNumber, 3);
    assert.equal(results[1]!.invocationMethod, 'child_process.execSync');
    assert.equal(results[2]!.command, 'node');
    assert.equal(results[2]!.lineNumber, 4);
    assert.equal(results[2]!.invocationMethod, 'child_process.spawn');
    assert.equal(results[3]!.command, 'rm -rf dist');
    assert.equal(results[3]!.lineNumber, 5);
    assert.equal(results[3]!.invocationMethod, 'child_process.exec');

    // Verify all results point to the same source file
    for (const r of results) {
      assert.equal(r.sourceFile, 'src/pipeline.ts');
    }
  });

  it('does not match subprocess calls inside block comments or docstrings', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/documented.ts',
        content: [
          '/*',
          " * This module uses exec('rm -rf /') internally",
          ' * and also calls spawn("node")',
          ' */',
          "exec('npm install');",
        ].join('\n'),
      },
      {
        path: 'scripts/documented.py',
        content: [
          'def build():',
          '    """',
          "    This uses spawn('node') for building",
          '    and calls system("make") internally',
          '    """',
          "    system('make clean')",
        ].join('\n'),
      },
    ];

    const results = extractShellCommands(files);

    // Only the real calls outside block comments should match
    assert.equal(results.length, 2);
    assert.equal(results[0]!.command, 'npm install');
    assert.equal(results[0]!.sourceFile, 'src/documented.ts');
    assert.equal(results[0]!.lineNumber, 5);
    assert.equal(results[1]!.command, 'make clean');
    assert.equal(results[1]!.sourceFile, 'scripts/documented.py');
    assert.equal(results[1]!.lineNumber, 6);
  });

  it('does not match subprocess calls inside logging/console function strings', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/logger.ts',
        content: [
          'console.log(\'exec("npm install") is dangerous\');',
          'console.warn(\'spawn("node") for child processes\');',
          "exec('real-command');",
        ].join('\n'),
      },
    ];

    const results = extractShellCommands(files);

    // Only the real exec call should match, not the ones inside console strings
    assert.equal(results.length, 1);
    assert.equal(results[0]!.command, 'real-command');
    assert.equal(results[0]!.lineNumber, 3);
    assert.equal(results[0]!.invocationMethod, 'child_process.exec');
  });

  it('real call-sites match alongside comments, docstrings, and logging', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/mixed.ts',
        content: [
          "// exec('commented out');",
          '/*',
          " * spawn('in block comment')",
          ' */',
          'console.log(\'exec("fake") output\');',
          "exec('git pull');",
          "spawn('docker', ['build']);",
        ].join('\n'),
      },
    ];

    const results = extractShellCommands(files);

    assert.equal(results.length, 2);
    assert.equal(results[0]!.command, 'git pull');
    assert.equal(results[0]!.lineNumber, 6);
    assert.equal(results[0]!.invocationMethod, 'child_process.exec');
    assert.equal(results[1]!.command, 'docker');
    assert.equal(results[1]!.lineNumber, 7);
    assert.equal(results[1]!.invocationMethod, 'child_process.spawn');
  });

  it('handles template literal arguments, returning raw template without interpolation', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/dynamic.ts',
        content: [
          "const dir = '/tmp';",
          'exec(`ls ${dir}`);',
          'execSync(`npm run build`);',
          'spawn(`node`, [`script.js`]);',
          'execFile(`/usr/local/bin/python3`, [`-m`, `pytest`]);',
        ].join('\n'),
      },
    ];

    const results = extractShellCommands(files);

    assert.equal(results.length, 4);

    // exec with template literal — raw template content preserved (exec-style keeps full command)
    assert.equal(results[0]!.command, 'ls ${dir}');
    assert.equal(results[0]!.invocationMethod, 'child_process.exec');

    // execSync with template literal — no interpolation, plain command preserved
    assert.equal(results[1]!.command, 'npm run build');
    assert.equal(results[1]!.invocationMethod, 'child_process.execSync');

    // spawn with template literal — spawn-style extracts binary basename
    assert.equal(results[2]!.command, 'node');
    assert.equal(results[2]!.invocationMethod, 'child_process.spawn');

    // execFile with template literal path — spawn-style extracts basename via parseCommandString
    assert.equal(results[3]!.command, 'python3');
    assert.equal(results[3]!.invocationMethod, 'child_process.execFile');
  });
});

// ---------------------------------------------------------------------------
// Integration test — imports extractShellCommands via barrel (src/index.ts)
// ---------------------------------------------------------------------------
import { extractShellCommands as barrelExtractShellCommands } from '../../src/index.js';

describe('extractShellCommands (barrel export integration)', () => {
  it('processes mixed JS/Python/bash DiscoveredFile[] and returns correct ShellCommand[] fields', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'lib/runner.js',
        content: [
          "const { exec, spawn } = require('child_process');",
          "exec('npm test');",
          "spawn('node', ['index.js']);",
          "// exec('commented out');",
          "execSync('eslint .');",
        ].join('\n'),
      },
      {
        path: 'tools/deploy.py',
        content: [
          'import os, subprocess',
          "os.system('docker build .')",
          "# popen('should be ignored')",
          "subprocess.run('pytest --cov')",
        ].join('\n'),
      },
      {
        path: 'scripts/init.sh',
        content: [
          '#!/bin/bash',
          'echo "starting"',
          'HASH=`git rev-parse HEAD`',
          'COUNT=$(wc -l < file.txt)',
          '# $(ignored subshell)',
        ].join('\n'),
      },
      {
        path: 'src/clean.ts',
        content: [
          'const x = 42;',
          "const msg = 'hello';",
        ].join('\n'),
      },
    ];

    const results = barrelExtractShellCommands(files);

    // --- JS detections (lib/runner.js) ---
    const jsResults = results.filter(r => r.sourceFile === 'lib/runner.js');
    assert.equal(jsResults.length, 3, 'JS file should yield 3 matches (comment excluded)');

    const jsExec = jsResults.find(r => r.invocationMethod === 'child_process.exec');
    assert.ok(jsExec);
    assert.equal(jsExec.command, 'npm test');
    assert.equal(jsExec.sourceFile, 'lib/runner.js');
    assert.equal(jsExec.lineNumber, 2);

    const jsSpawn = jsResults.find(r => r.invocationMethod === 'child_process.spawn');
    assert.ok(jsSpawn);
    assert.equal(jsSpawn.command, 'node');
    assert.equal(jsSpawn.lineNumber, 3);

    const jsExecSync = jsResults.find(r => r.invocationMethod === 'child_process.execSync');
    assert.ok(jsExecSync);
    assert.equal(jsExecSync.command, 'eslint .');
    assert.equal(jsExecSync.lineNumber, 5);

    // --- Python detections (tools/deploy.py) ---
    const pyResults = results.filter(r => r.sourceFile === 'tools/deploy.py');
    assert.equal(pyResults.length, 2, 'Python file should yield 2 matches (comment excluded)');

    const pySystem = pyResults.find(r => r.invocationMethod === 'os.system');
    assert.ok(pySystem);
    assert.equal(pySystem.command, 'docker build .');
    assert.equal(pySystem.lineNumber, 2);

    const pySubproc = pyResults.find(r => r.invocationMethod === 'subprocess.run');
    assert.ok(pySubproc);
    assert.equal(pySubproc.command, 'pytest --cov');
    assert.equal(pySubproc.lineNumber, 4);

    // --- Shell detections (scripts/init.sh) ---
    const shResults = results.filter(r => r.sourceFile === 'scripts/init.sh');
    assert.equal(shResults.length, 2, 'Shell file should yield 2 matches (comment excluded)');

    const shBacktick = shResults.find(r => r.invocationMethod === 'backtick_subshell');
    assert.ok(shBacktick);
    assert.equal(shBacktick.command, 'git rev-parse HEAD');
    assert.equal(shBacktick.lineNumber, 3);

    const shDollar = shResults.find(r => r.invocationMethod === 'dollar_paren_subshell');
    assert.ok(shDollar);
    assert.ok(shDollar.command.startsWith('wc'));
    assert.equal(shDollar.lineNumber, 4);

    // --- No matches for clean .ts file ---
    const tsResults = results.filter(r => r.sourceFile === 'src/clean.ts');
    assert.equal(tsResults.length, 0, 'Clean TS file should produce no matches');

    // --- Total count ---
    assert.equal(results.length, 7, 'Total: 3 JS + 2 Python + 2 Shell');
  });
});

// ---------------------------------------------------------------------------
// Environment variable extraction tests (T012)
// ---------------------------------------------------------------------------

describe('extractEnvVars — process.env detection', () => {
  it('detects process.env.X and process.env["X"] in JS/TS files', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/config.ts',
        content: [
          "const env = process.env.NODE_ENV;",
          "const key = process.env['API_KEY'];",
          'const secret = process.env["DB_PASSWORD"];',
          "const port = process.env.PORT;",
        ].join('\n'),
      },
    ];

    const results = extractEnvVars(files);

    assert.equal(results.length, 4);

    const nodeEnv = results.find(r => r.name === 'NODE_ENV');
    assert.ok(nodeEnv);
    assert.equal(nodeEnv.sourceFile, 'src/config.ts');
    assert.equal(nodeEnv.line, 1);
    assert.equal(nodeEnv.accessMethod, 'process.env');
    assert.equal(nodeEnv.isSecret, false, 'NODE_ENV is safe');

    const apiKey = results.find(r => r.name === 'API_KEY');
    assert.ok(apiKey);
    assert.equal(apiKey.line, 2);
    assert.equal(apiKey.accessMethod, 'process.env');
    assert.equal(apiKey.isSecret, true, 'API_KEY is a secret');

    const dbPassword = results.find(r => r.name === 'DB_PASSWORD');
    assert.ok(dbPassword);
    assert.equal(dbPassword.line, 3);
    assert.equal(dbPassword.isSecret, true, 'DB_PASSWORD is a secret');

    const port = results.find(r => r.name === 'PORT');
    assert.ok(port);
    assert.equal(port.isSecret, false, 'PORT is safe');
  });
});

describe('extractJsEnvVars — multiple vars on one line', () => {
  it('extracts all unique variables from a single line', () => {
    const content = "const x = process.env.NODE_ENV || process.env.API_KEY || process.env['DB_PASSWORD'];";
    const results = extractJsEnvVars(content, 'src/config.ts');

    assert.equal(results.length, 3);
    assert.ok(results.find(r => r.name === 'NODE_ENV'));
    assert.ok(results.find(r => r.name === 'API_KEY'));
    assert.ok(results.find(r => r.name === 'DB_PASSWORD'));
    for (const r of results) {
      assert.equal(r.line, 1, 'all should be on line 1');
      assert.equal(r.accessMethod, 'process.env');
    }
  });
});

describe('extractJsEnvVars — template literals containing process.env', () => {
  it('detects process.env inside template literal expressions', () => {
    const content = [
      'const url = `http://${process.env.HOST}:${process.env.PORT}/api`;',
      "const msg = `Running in ${process.env.NODE_ENV} mode`;",
    ].join('\n');
    const results = extractJsEnvVars(content, 'src/server.ts');

    assert.equal(results.length, 3);

    const host = results.find(r => r.name === 'HOST');
    assert.ok(host);
    assert.equal(host.line, 1);
    assert.equal(host.accessMethod, 'process.env');

    const port = results.find(r => r.name === 'PORT');
    assert.ok(port);
    assert.equal(port.line, 1);

    const nodeEnv = results.find(r => r.name === 'NODE_ENV');
    assert.ok(nodeEnv);
    assert.equal(nodeEnv.line, 2);
  });
});

describe('extractJsEnvVars — line numbers are correct', () => {
  it('reports accurate 1-based line numbers', () => {
    const content = [
      '// line 1 comment',
      '',
      "const a = process.env.FIRST_VAR;",
      '',
      '',
      "const b = process.env['SECOND_VAR'];",
    ].join('\n');
    const results = extractJsEnvVars(content, 'src/app.ts');

    assert.equal(results.length, 2);
    assert.equal(results[0]!.name, 'FIRST_VAR');
    assert.equal(results[0]!.line, 3);
    assert.equal(results[1]!.name, 'SECOND_VAR');
    assert.equal(results[1]!.line, 6);
  });
});

describe('extractJsEnvVars — .jsx/.tsx/.cjs extensions', () => {
  it('works with JSX, TSX, and CJS file extensions via extractEnvVars', () => {
    const files: DiscoveredFile[] = [
      { path: 'src/App.jsx', content: "const env = process.env.REACT_APP_KEY;" },
      { path: 'src/App.tsx', content: "const env = process.env.NEXT_PUBLIC_URL;" },
      { path: 'lib/config.cjs', content: "const env = process.env.CJS_VAR;" },
    ];
    const results = extractEnvVars(files);

    assert.equal(results.length, 3);
    assert.ok(results.find(r => r.name === 'REACT_APP_KEY' && r.sourceFile === 'src/App.jsx'));
    assert.ok(results.find(r => r.name === 'NEXT_PUBLIC_URL' && r.sourceFile === 'src/App.tsx'));
    assert.ok(results.find(r => r.name === 'CJS_VAR' && r.sourceFile === 'lib/config.cjs'));
  });
});

// ---------------------------------------------------------------------------
// extractPyEnvVars unit tests (T012.c)
// ---------------------------------------------------------------------------

describe('extractPyEnvVars — os.environ bracket access', () => {
  it('detects os.environ with single and double quotes', () => {
    const content = [
      "import os",
      "home = os.environ['HOME']",
      'key = os.environ["API_KEY"]',
    ].join('\n');
    const results = extractPyEnvVars(content, 'config.py');

    assert.equal(results.length, 2);

    const home = results.find(r => r.name === 'HOME');
    assert.ok(home);
    assert.equal(home.accessMethod, 'os.environ');
    assert.equal(home.line, 2);
    assert.equal(home.sourceFile, 'config.py');
    assert.equal(home.isSecret, false, 'HOME is safe');

    const apiKey = results.find(r => r.name === 'API_KEY');
    assert.ok(apiKey);
    assert.equal(apiKey.accessMethod, 'os.environ');
    assert.equal(apiKey.line, 3);
    assert.equal(apiKey.isSecret, true, 'API_KEY is a secret');
  });
});

describe('extractPyEnvVars — os.getenv calls', () => {
  it('detects os.getenv with single and double quotes', () => {
    const content = [
      "import os",
      "lang = os.getenv('LANG')",
      'token = os.getenv("GITHUB_TOKEN")',
    ].join('\n');
    const results = extractPyEnvVars(content, 'app.py');

    assert.equal(results.length, 2);

    const lang = results.find(r => r.name === 'LANG');
    assert.ok(lang);
    assert.equal(lang.accessMethod, 'os.getenv');
    assert.equal(lang.isSecret, false, 'LANG is safe');

    const token = results.find(r => r.name === 'GITHUB_TOKEN');
    assert.ok(token);
    assert.equal(token.accessMethod, 'os.getenv');
    assert.equal(token.isSecret, true, 'GITHUB_TOKEN is a secret');
  });
});

describe('extractPyEnvVars — os.environ.get calls', () => {
  it('detects os.environ.get and classifies secrets correctly', () => {
    const content = [
      "import os",
      "secret = os.environ.get('AWS_SECRET_KEY')",
      "env = os.environ.get('NODE_ENV')",
    ].join('\n');
    const results = extractPyEnvVars(content, 'settings.py');

    assert.equal(results.length, 2);

    const awsKey = results.find(r => r.name === 'AWS_SECRET_KEY');
    assert.ok(awsKey);
    assert.equal(awsKey.accessMethod, 'os.environ');
    assert.equal(awsKey.isSecret, true, 'AWS_SECRET_KEY is a secret');

    const nodeEnv = results.find(r => r.name === 'NODE_ENV');
    assert.ok(nodeEnv);
    assert.equal(nodeEnv.accessMethod, 'os.environ');
    assert.equal(nodeEnv.isSecret, false, 'NODE_ENV is safe');
  });
});

describe('extractPyEnvVars — default values in getenv are ignored', () => {
  it('extracts only the variable name, not default arguments', () => {
    const content = [
      "import os",
      "env = os.getenv('NODE_ENV', 'production')",
      "host = os.environ.get('HOST', 'localhost')",
      "key = os.getenv('DB_PASSWORD', '')",
    ].join('\n');
    const results = extractPyEnvVars(content, 'defaults.py');

    assert.equal(results.length, 3);
    assert.ok(results.find(r => r.name === 'NODE_ENV'));
    assert.ok(results.find(r => r.name === 'HOST'));
    assert.ok(results.find(r => r.name === 'DB_PASSWORD'));

    // Ensure no result contains 'production', 'localhost', or empty string as name
    for (const r of results) {
      assert.notEqual(r.name, 'production');
      assert.notEqual(r.name, 'localhost');
      assert.notEqual(r.name, '');
    }
  });
});

describe('extractPyEnvVars — line numbers are correct', () => {
  it('reports accurate 1-based line numbers across blank lines and comments', () => {
    const content = [
      '# Python config',
      '',
      "import os",
      '',
      "first = os.environ['FIRST_VAR']",
      '# comment',
      '',
      "second = os.getenv('SECOND_VAR')",
      '',
      '',
      "third = os.environ.get('THIRD_VAR')",
    ].join('\n');
    const results = extractPyEnvVars(content, 'lines.py');

    assert.equal(results.length, 3);
    assert.equal(results[0]!.name, 'FIRST_VAR');
    assert.equal(results[0]!.line, 5);
    assert.equal(results[1]!.name, 'SECOND_VAR');
    assert.equal(results[1]!.line, 8);
    assert.equal(results[2]!.name, 'THIRD_VAR');
    assert.equal(results[2]!.line, 11);
  });
});

describe('extractEnvVars — Python env detection', () => {
  it('detects os.environ, os.environ.get, and os.getenv in .py files', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'scripts/config.py',
        content: [
          "import os",
          "home = os.environ['HOME']",
          "key = os.environ.get('AWS_SECRET_KEY')",
          "lang = os.getenv('LANG')",
          "token = os.getenv('GITHUB_TOKEN')",
        ].join('\n'),
      },
    ];

    const results = extractEnvVars(files);

    assert.equal(results.length, 4);

    const home = results.find(r => r.name === 'HOME');
    assert.ok(home);
    assert.equal(home.accessMethod, 'os.environ');
    assert.equal(home.isSecret, false, 'HOME is safe');

    const awsKey = results.find(r => r.name === 'AWS_SECRET_KEY');
    assert.ok(awsKey);
    assert.equal(awsKey.accessMethod, 'os.environ');
    assert.equal(awsKey.isSecret, true, 'AWS_SECRET_KEY is a secret');

    const lang = results.find(r => r.name === 'LANG');
    assert.ok(lang);
    assert.equal(lang.accessMethod, 'os.getenv');
    assert.equal(lang.isSecret, false, 'LANG is safe');

    const token = results.find(r => r.name === 'GITHUB_TOKEN');
    assert.ok(token);
    assert.equal(token.accessMethod, 'os.getenv');
    assert.equal(token.isSecret, true, 'GITHUB_TOKEN is a secret');
  });
});

describe('extractEnvVars — shell/Dockerfile variable detection', () => {
  it('detects $VAR and ${VAR} in .sh, .env, and Dockerfile files', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'deploy.sh',
        content: [
          '#!/bin/bash',
          'echo $HOME',
          'echo ${API_SECRET}',
          'export PATH=$PATH:/usr/local/bin',
        ].join('\n'),
      },
      {
        path: '.env',
        content: [
          'NODE_ENV=production',
          'DB_PASSWORD=${DB_PASSWORD}',
          'PORT=3000',
        ].join('\n'),
      },
      {
        path: 'Dockerfile',
        content: [
          'FROM node:18',
          'ENV APP_TOKEN=$APP_TOKEN',
          'RUN echo ${HOME}',
        ].join('\n'),
      },
    ];

    const results = extractEnvVars(files);

    // Shell file
    const shResults = results.filter(r => r.sourceFile === 'deploy.sh');
    assert.ok(shResults.find(r => r.name === 'HOME'));
    assert.ok(shResults.find(r => r.name === 'API_SECRET'));
    assert.ok(shResults.find(r => r.name === 'PATH'));
    for (const r of shResults) {
      assert.equal(r.accessMethod, 'shell_expansion');
    }

    // .env file
    const envResults = results.filter(r => r.sourceFile === '.env');
    const dbPw = envResults.find(r => r.name === 'DB_PASSWORD');
    assert.ok(dbPw);
    assert.equal(dbPw.isSecret, true);

    // Dockerfile
    const dockerResults = results.filter(r => r.sourceFile === 'Dockerfile');
    const appToken = dockerResults.find(r => r.name === 'APP_TOKEN');
    assert.ok(appToken);
    assert.equal(appToken.isSecret, true, 'APP_TOKEN matches _TOKEN suffix');
    assert.equal(appToken.accessMethod, 'shell_expansion');
  });
});

describe('classifySecret — secret classification accuracy', () => {
  it('identifies secret patterns correctly', () => {
    // Suffix patterns
    assert.equal(classifySecret('MY_API_KEY'), true);
    assert.equal(classifySecret('AWS_SECRET'), true);
    assert.equal(classifySecret('GITHUB_TOKEN'), true);
    assert.equal(classifySecret('DB_PASSWORD'), true);
    assert.equal(classifySecret('SERVICE_CREDENTIAL'), true);

    // Prefix patterns
    assert.equal(classifySecret('API_ENDPOINT'), true);
    assert.equal(classifySecret('AUTH_HEADER'), true);

    // Substring patterns (case-insensitive)
    assert.equal(classifySecret('my_secret_value'), true);
    assert.equal(classifySecret('MyPassword'), true);
    assert.equal(classifySecret('accessToken'), true);
    assert.equal(classifySecret('userCredential'), true);

    // Non-secrets
    assert.equal(classifySecret('DATABASE_URL'), false);
    assert.equal(classifySecret('LOG_FORMAT'), false);
    assert.equal(classifySecret('MAX_RETRIES'), false);
    assert.equal(classifySecret('FEATURE_FLAG'), false);
  });
});

describe('classifySecret — safe-variable allowlist verification', () => {
  it('does not flag any SAFE_ENV_VARS as secrets', () => {
    for (const name of SAFE_ENV_VARS) {
      assert.equal(
        classifySecret(name),
        false,
        `${name} should not be classified as secret`,
      );
    }
  });

  it('safe vars that would match patterns are still not flagged', () => {
    // HOST could match AUTH_ prefix if checked wrong; PATH contains no secret markers
    assert.equal(classifySecret('HOST'), false);
    assert.equal(classifySecret('HOSTNAME'), false);
    assert.equal(classifySecret('PORT'), false);
    assert.equal(classifySecret('NODE_ENV'), false);
  });
});

describe('extractEnvVars — deduplication behaviour', () => {
  it('deduplicates by variable name per file, keeping first occurrence', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/app.ts',
        content: [
          "const a = process.env.NODE_ENV;",
          "const b = process.env.NODE_ENV;",
          "const c = process.env['NODE_ENV'];",
          "const d = process.env.API_KEY;",
          "const e = process.env.API_KEY;",
        ].join('\n'),
      },
    ];

    const results = extractEnvVars(files);

    // Should have exactly 2 unique vars: NODE_ENV and API_KEY
    assert.equal(results.length, 2);

    const nodeEnv = results.find(r => r.name === 'NODE_ENV');
    assert.ok(nodeEnv);
    assert.equal(nodeEnv.line, 1, 'should keep first occurrence of NODE_ENV');

    const apiKey = results.find(r => r.name === 'API_KEY');
    assert.ok(apiKey);
    assert.equal(apiKey.line, 4, 'should keep first occurrence of API_KEY');
  });

  it('same variable in different files is NOT deduplicated', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/a.ts',
        content: "const x = process.env.NODE_ENV;",
      },
      {
        path: 'src/b.ts',
        content: "const y = process.env.NODE_ENV;",
      },
    ];

    const results = extractEnvVars(files);
    assert.equal(results.length, 2, 'same var in different files should appear twice');
  });
});

// ---------------------------------------------------------------------------
// extractShellEnvVars unit tests (T012.d)
// ---------------------------------------------------------------------------

describe('extractShellEnvVars — braced and unbraced vars', () => {
  it('detects ${VAR} braced and $VAR unbraced expansions', () => {
    const content = [
      '#!/bin/bash',
      'echo $HOME',
      'echo ${API_SECRET}',
      'export PATH=$PATH:/usr/local/bin',
      'curl -H "Authorization: Bearer ${AUTH_TOKEN}"',
    ].join('\n');
    const results = extractShellEnvVars(content, 'deploy.sh');

    assert.ok(results.find(r => r.name === 'HOME'), 'should detect unbraced $HOME');
    assert.ok(results.find(r => r.name === 'API_SECRET'), 'should detect braced ${API_SECRET}');
    assert.ok(results.find(r => r.name === 'PATH'), 'should detect unbraced $PATH');
    assert.ok(results.find(r => r.name === 'AUTH_TOKEN'), 'should detect braced ${AUTH_TOKEN}');

    for (const r of results) {
      assert.equal(r.accessMethod, 'shell_expansion');
      assert.equal(r.sourceFile, 'deploy.sh');
    }
  });
});

describe('extractShellEnvVars — excludes special shell variables', () => {
  it('ignores $$, $?, $0-$9, $@, and $*', () => {
    const content = [
      'echo $$',
      'echo $?',
      'echo $0 $1 $2 $9',
      'echo $@ $*',
      'echo $REAL_VAR',
    ].join('\n');
    const results = extractShellEnvVars(content, 'test.sh');

    // Only REAL_VAR should be detected — special vars are excluded
    assert.equal(results.length, 1);
    assert.equal(results[0]!.name, 'REAL_VAR');
  });
});

describe('extractShellEnvVars — Dockerfile ENV and ARG lines', () => {
  it('detects $VAR and ${VAR} in Dockerfile ENV and ARG instructions', () => {
    const content = [
      'FROM node:18',
      'ARG BUILD_ENV=production',
      'ENV APP_TOKEN=$APP_TOKEN',
      'ENV CONFIG_PATH=${CONFIG_DIR}/app.conf',
      'RUN echo ${HOME}',
      'COPY . /app',
    ].join('\n');
    const results = extractShellEnvVars(content, 'Dockerfile');

    const appToken = results.find(r => r.name === 'APP_TOKEN');
    assert.ok(appToken, 'should detect $APP_TOKEN');
    assert.equal(appToken.line, 3);
    assert.equal(appToken.isSecret, true, 'APP_TOKEN matches _TOKEN suffix');

    const configDir = results.find(r => r.name === 'CONFIG_DIR');
    assert.ok(configDir, 'should detect ${CONFIG_DIR}');
    assert.equal(configDir.line, 4);

    const home = results.find(r => r.name === 'HOME');
    assert.ok(home, 'should detect ${HOME}');
    assert.equal(home.line, 5);
    assert.equal(home.isSecret, false, 'HOME is safe');
  });
});

describe('extractShellEnvVars — .env KEY=value with $KEY on right side', () => {
  it('detects $VAR references on the right side of assignments', () => {
    const content = [
      'NODE_ENV=production',
      'DB_HOST=localhost',
      'DB_URL=postgres://${DB_HOST}:5432/mydb',
      'SECRET_KEY=${API_SECRET_KEY}',
      'FALLBACK=$DEFAULT_VALUE',
    ].join('\n');
    const results = extractShellEnvVars(content, '.env');

    // NODE_ENV=production has no $, should not be detected
    assert.ok(!results.find(r => r.name === 'NODE_ENV'), 'bare assignment LHS should not match');

    // DB_HOST appears as ${DB_HOST} on line 3, so it IS detected via braced expansion
    const dbHost = results.find(r => r.name === 'DB_HOST');
    assert.ok(dbHost, 'should detect ${DB_HOST} from RHS of DB_URL assignment');
    assert.equal(dbHost.line, 3);

    // API_SECRET_KEY should be detected and flagged as secret
    const apiSecretKey = results.find(r => r.name === 'API_SECRET_KEY');
    assert.ok(apiSecretKey, 'should detect ${API_SECRET_KEY}');
    assert.equal(apiSecretKey.isSecret, true, 'API_SECRET_KEY matches _KEY suffix');
    assert.equal(apiSecretKey.line, 4);

    // DEFAULT_VALUE should be detected from unbraced $DEFAULT_VALUE
    const defaultVal = results.find(r => r.name === 'DEFAULT_VALUE');
    assert.ok(defaultVal, 'should detect $DEFAULT_VALUE');
    assert.equal(defaultVal.line, 5);
  });
});

describe('extractShellEnvVars — line numbers are correct', () => {
  it('reports accurate 1-based line numbers across blank lines and comments', () => {
    const content = [
      '#!/bin/bash',
      '',
      '# Configuration',
      'export DB_USER=$DB_USER',
      '',
      '',
      'echo ${API_KEY}',
      '# end of script',
      '',
      'curl -u $SERVICE_TOKEN',
    ].join('\n');
    const results = extractShellEnvVars(content, 'setup.sh');

    assert.equal(results.length, 3);

    const dbUser = results.find(r => r.name === 'DB_USER');
    assert.ok(dbUser);
    assert.equal(dbUser.line, 4, 'DB_USER should be on line 4');

    const apiKey = results.find(r => r.name === 'API_KEY');
    assert.ok(apiKey);
    assert.equal(apiKey.line, 7, 'API_KEY should be on line 7');

    const serviceToken = results.find(r => r.name === 'SERVICE_TOKEN');
    assert.ok(serviceToken);
    assert.equal(serviceToken.line, 10, 'SERVICE_TOKEN should be on line 10');
  });
});

describe('extractShellEnvVars — deduplication keeps first occurrence', () => {
  it('deduplicates by variable name, keeping the first occurrence', () => {
    const content = [
      'echo $HOME',
      'echo $PATH',
      'echo ${HOME}',
      'cd $HOME',
      'echo ${PATH}:/extra',
    ].join('\n');
    const results = extractShellEnvVars(content, 'dup.sh');

    assert.equal(results.length, 2, 'should have 2 unique vars');

    const home = results.find(r => r.name === 'HOME');
    assert.ok(home);
    assert.equal(home.line, 1, 'HOME should be from first occurrence on line 1');

    const pathVar = results.find(r => r.name === 'PATH');
    assert.ok(pathVar);
    assert.equal(pathVar.line, 2, 'PATH should be from first occurrence on line 2');
  });
});

// ---------------------------------------------------------------------------
// extractEnvVars integration tests (T012.e) — mixed file types in one call
// ---------------------------------------------------------------------------

describe('extractEnvVars — mixed JS/Python/Dockerfile integration', () => {
  it('combines results from all three extractors with correct fields and isSecret flags', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/config.ts',
        content: [
          "const env = process.env.NODE_ENV;",
          "const key = process.env['AWS_SECRET_KEY'];",
          "const port = process.env.PORT;",
        ].join('\n'),
      },
      {
        path: 'scripts/setup.py',
        content: [
          "import os",
          "home = os.environ['HOME']",
          "token = os.getenv('GITHUB_TOKEN')",
          "lang = os.environ.get('LANG')",
        ].join('\n'),
      },
      {
        path: 'Dockerfile',
        content: [
          'FROM node:18',
          'ENV APP_TOKEN=$APP_TOKEN',
          'RUN echo ${PATH}',
          'ENV DB_PASSWORD=${DB_PASSWORD}',
        ].join('\n'),
      },
    ];

    const results = extractEnvVars(files);

    // --- JS results ---
    const jsResults = results.filter(r => r.sourceFile === 'src/config.ts');
    assert.equal(jsResults.length, 3, 'JS file should yield 3 vars');
    for (const r of jsResults) {
      assert.equal(r.accessMethod, 'process.env');
    }
    const nodeEnv = jsResults.find(r => r.name === 'NODE_ENV');
    assert.ok(nodeEnv);
    assert.equal(nodeEnv.isSecret, false, 'NODE_ENV is safe');
    assert.equal(nodeEnv.line, 1);

    const awsKey = jsResults.find(r => r.name === 'AWS_SECRET_KEY');
    assert.ok(awsKey);
    assert.equal(awsKey.isSecret, true, 'AWS_SECRET_KEY matches _KEY suffix');
    assert.equal(awsKey.line, 2);

    const jsPort = jsResults.find(r => r.name === 'PORT');
    assert.ok(jsPort);
    assert.equal(jsPort.isSecret, false, 'PORT is safe');

    // --- Python results ---
    const pyResults = results.filter(r => r.sourceFile === 'scripts/setup.py');
    assert.equal(pyResults.length, 3, 'Python file should yield 3 vars');

    const pyHome = pyResults.find(r => r.name === 'HOME');
    assert.ok(pyHome);
    assert.equal(pyHome.accessMethod, 'os.environ');
    assert.equal(pyHome.isSecret, false, 'HOME is safe');

    const ghToken = pyResults.find(r => r.name === 'GITHUB_TOKEN');
    assert.ok(ghToken);
    assert.equal(ghToken.accessMethod, 'os.getenv');
    assert.equal(ghToken.isSecret, true, 'GITHUB_TOKEN matches _TOKEN suffix');

    const pyLang = pyResults.find(r => r.name === 'LANG');
    assert.ok(pyLang);
    assert.equal(pyLang.accessMethod, 'os.environ');
    assert.equal(pyLang.isSecret, false, 'LANG is safe');

    // --- Dockerfile results ---
    const dockerResults = results.filter(r => r.sourceFile === 'Dockerfile');
    assert.ok(dockerResults.length >= 3, 'Dockerfile should yield at least 3 vars');
    for (const r of dockerResults) {
      assert.equal(r.accessMethod, 'shell_expansion');
    }

    const appToken = dockerResults.find(r => r.name === 'APP_TOKEN');
    assert.ok(appToken);
    assert.equal(appToken.isSecret, true, 'APP_TOKEN matches _TOKEN suffix');

    const dockerPath = dockerResults.find(r => r.name === 'PATH');
    assert.ok(dockerPath);
    assert.equal(dockerPath.isSecret, false, 'PATH is safe');

    const dbPw = dockerResults.find(r => r.name === 'DB_PASSWORD');
    assert.ok(dbPw);
    assert.equal(dbPw.isSecret, true, 'DB_PASSWORD matches _PASSWORD suffix');

    // --- Total count: 3 JS + 3 Python + 3 Dockerfile = 9 ---
    assert.equal(results.length, 9, 'combined output should have 9 entries');
  });

  it('deduplicates within each file but keeps same var across files', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'src/a.ts',
        content: [
          "const a = process.env.NODE_ENV;",
          "const b = process.env.NODE_ENV;",
        ].join('\n'),
      },
      {
        path: 'scripts/b.py',
        content: [
          "import os",
          "x = os.environ['NODE_ENV']",
          "y = os.getenv('NODE_ENV')",
        ].join('\n'),
      },
      {
        path: 'deploy.sh',
        content: [
          'echo $NODE_ENV',
          'echo ${NODE_ENV}',
        ].join('\n'),
      },
    ];

    const results = extractEnvVars(files);

    // 1 from JS (deduped), 1 from Python (deduped), 1 from shell (deduped)
    assert.equal(results.length, 3, 'same var across files should NOT be deduped');
    assert.equal(
      results.filter(r => r.name === 'NODE_ENV').length,
      3,
      'NODE_ENV should appear once per file',
    );

    // Each should come from its own file
    assert.ok(results.find(r => r.sourceFile === 'src/a.ts'));
    assert.ok(results.find(r => r.sourceFile === 'scripts/b.py'));
    assert.ok(results.find(r => r.sourceFile === 'deploy.sh'));
  });
});
