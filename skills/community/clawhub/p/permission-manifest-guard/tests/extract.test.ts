import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {
  parseCommandString,
  detectChildProcessCalls,
  detectShebangs,
  detectKnownCLIPatterns,
  extractBinaries,
  extractDomains,
  extractUrlDomains,
  extractBareDomains,
  isLocalhostWithStandardPort,
  extractFilePaths,
  isFilePath,
  isImportOrRequirePath,
  classifyAccess,
  READ_APIS,
  WRITE_APIS,

  ABS_POSIX_RE,
  ABS_WIN_RE,
  HOME_RE,
  REL_FS_CONTEXT_RE,
  NETWORK_CONTEXT_PATTERNS,
  URI_REGEX,
  LOCALHOST_HOSTS,
  extractConfigFiles,
  extractPackageManagers,
} from '../src/extract.js';
import type { DiscoveredFile, ConfigFileEntry, PackageManagerEntry } from '../src/types.js';

function makeTmpDir(): string {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'extract-test-'));
}

function writeFile(base: string, relPath: string, content: string): void {
  const full = path.join(base, relPath);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content);
}

describe('parseCommandString', () => {
  it('extracts binaries from pipe chains', () => {
    const result = parseCommandString('cat /etc/passwd | grep root | wc -l');

    assert.deepEqual(result.binaries, ['cat', 'grep', 'wc']);
    assert.equal(result.confidence, 'high');
  });

  it('extracts binaries from && chains', () => {
    const result = parseCommandString('mkdir -p dist && cp -r src/* dist');

    assert.deepEqual(result.binaries, ['mkdir', 'cp']);
    assert.equal(result.confidence, 'high');
  });

  it('extracts binaries from semicolon chains', () => {
    const result = parseCommandString('echo start ; npm install ; echo done');

    assert.deepEqual(result.binaries, ['echo', 'npm', 'echo']);
    assert.equal(result.confidence, 'high');
  });

  it('strips quotes and extracts basename from quoted paths', () => {
    const result = parseCommandString("'/usr/local/bin/git' clone repo");

    assert.deepEqual(result.binaries, ['git']);
    assert.equal(result.confidence, 'high');
  });

  it('marks variable interpolation as low confidence', () => {
    const result = parseCommandString('${TOOL} --verbose');

    assert.equal(result.binaries.length, 1);
    assert.equal(result.confidence, 'low');
  });

  it('handles $VAR style interpolation as low confidence', () => {
    const result = parseCommandString('$CMD run --flag');

    assert.equal(result.confidence, 'low');
  });

  it('handles mixed chains and pipes', () => {
    const result = parseCommandString('ls -la | grep foo && rm -rf tmp ; echo done');

    assert.deepEqual(result.binaries, ['ls', 'grep', 'rm', 'echo']);
    assert.equal(result.confidence, 'high');
  });

  it('returns empty binaries for empty string', () => {
    const result = parseCommandString('');

    assert.deepEqual(result.binaries, []);
    assert.equal(result.confidence, 'high');
  });
});

describe('detectChildProcessCalls', () => {
  it('detects child_process.exec calls and extracts binary name', () => {
    const content = [
      "import { exec } from 'child_process';",
      "exec('git clone https://github.com/repo');",
    ].join('\n');

    const refs = detectChildProcessCalls(content, 'src/deploy.ts');

    const gitRef = refs.find(r => r.value === 'git');
    assert.ok(gitRef, 'should detect git binary from exec call');
    assert.equal(gitRef.source.filePath, 'src/deploy.ts');
    assert.equal(gitRef.source.line, 2);
    assert.equal(gitRef.confidence, 'high');
  });

  it('detects child_process.spawn calls and extracts binary name', () => {
    const content = "spawn('docker', ['run', '-it', 'ubuntu']);";

    const refs = detectChildProcessCalls(content, 'src/runner.ts');

    assert.equal(refs.length, 1);
    assert.equal(refs[0]!.value, 'docker');
    assert.equal(refs[0]!.source.filePath, 'src/runner.ts');
    assert.equal(refs[0]!.source.line, 1);
    assert.equal(refs[0]!.confidence, 'high');
  });

  it('detects execSync calls', () => {
    const content = "const output = execSync('npm install --production');";

    const refs = detectChildProcessCalls(content, 'src/setup.ts');

    assert.equal(refs.length, 1);
    assert.equal(refs[0]!.value, 'npm');
    assert.equal(refs[0]!.source.line, 1);
    assert.equal(refs[0]!.confidence, 'high');
  });

  it('extracts all commands from pipe chains', () => {
    const content = "exec('cat /etc/passwd | grep root | wc -l');";

    const refs = detectChildProcessCalls(content, 'src/scan.ts');

    const binaries = refs.map(r => r.value);
    assert.ok(binaries.includes('cat'), 'should extract cat');
    assert.ok(binaries.includes('grep'), 'should extract grep');
    assert.ok(binaries.includes('wc'), 'should extract wc');
    assert.equal(refs.length, 3);
  });

  it('extracts all commands from && chains', () => {
    const content = "exec('mkdir -p dist && cp -r src/* dist && echo done');";

    const refs = detectChildProcessCalls(content, 'src/build.ts');

    const binaries = refs.map(r => r.value);
    assert.ok(binaries.includes('mkdir'), 'should extract mkdir');
    assert.ok(binaries.includes('cp'), 'should extract cp');
    assert.ok(binaries.includes('echo'), 'should extract echo');
    assert.equal(refs.length, 3);
  });

  it('marks variable interpolation commands as low confidence', () => {
    const content = "execSync(`${command} --verbose`);";

    const refs = detectChildProcessCalls(content, 'src/dynamic.ts');

    assert.equal(refs.length, 1);
    assert.equal(refs[0]!.confidence, 'low');
  });

  it('returns empty array for content with no child_process calls', () => {
    const content = [
      'const x = 42;',
      'function add(a: number, b: number) { return a + b; }',
      '// just a comment about exec in prose',
    ].join('\n');

    const refs = detectChildProcessCalls(content, 'src/math.ts');

    assert.deepEqual(refs, []);
  });
});

describe('detectShebangs', () => {
  it('extracts binary from #!/usr/bin/env shebang', () => {
    const content = '#!/usr/bin/env node\nconsole.log("hello");';

    const refs = detectShebangs(content, 'scripts/run.sh');

    assert.equal(refs.length, 1);
    assert.equal(refs[0]!.value, 'node');
    assert.equal(refs[0]!.source.filePath, 'scripts/run.sh');
    assert.equal(refs[0]!.source.line, 1);
    assert.equal(refs[0]!.confidence, 'high');
  });

  it('extracts binary from direct path shebang (#!/bin/bash)', () => {
    const content = '#!/bin/bash\necho "hello"';

    const refs = detectShebangs(content, 'scripts/deploy.sh');

    assert.equal(refs.length, 1);
    assert.equal(refs[0]!.value, 'bash');
    assert.equal(refs[0]!.source.filePath, 'scripts/deploy.sh');
    assert.equal(refs[0]!.source.line, 1);
    assert.equal(refs[0]!.confidence, 'high');
  });

  it('returns empty array when no shebang is present', () => {
    const content = 'console.log("no shebang here");';

    const refs = detectShebangs(content, 'src/index.ts');

    assert.deepEqual(refs, []);
  });
});

describe('detectKnownCLIPatterns', () => {
  it('detects known CLI names in string literals with medium confidence', () => {
    const content = [
      "const tool = 'terraform';",
      'const cloud = "aws configure --profile dev";',
      'const deploy = `helm install my-chart`;',
    ].join('\n');

    const refs = detectKnownCLIPatterns(content, 'src/infra.ts');

    const terraformRef = refs.find(r => r.value === 'terraform');
    const awsRef = refs.find(r => r.value === 'aws');
    const helmRef = refs.find(r => r.value === 'helm');
    assert.ok(terraformRef, 'should detect terraform');
    assert.ok(awsRef, 'should detect aws');
    assert.ok(helmRef, 'should detect helm');
    assert.equal(terraformRef!.confidence, 'medium');
    assert.equal(awsRef!.confidence, 'medium');
    assert.equal(helmRef!.confidence, 'medium');
    assert.equal(terraformRef!.source.line, 1);
    assert.equal(awsRef!.source.line, 2);
    assert.equal(helmRef!.source.line, 3);
  });

  it('detects CLI names from path-like tokens', () => {
    const content = "const bin = '/usr/local/bin/git';";

    const refs = detectKnownCLIPatterns(content, 'src/paths.ts');

    const gitRef = refs.find(r => r.value === 'git');
    assert.ok(gitRef, 'should extract git from path');
    assert.equal(gitRef!.confidence, 'medium');
  });

  it('returns empty array when no known CLIs are found', () => {
    const content = "const x = 'hello world';";

    const refs = detectKnownCLIPatterns(content, 'src/app.ts');

    assert.deepEqual(refs, []);
  });
});

describe('extractBinaries', () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = makeTmpDir();
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('detects child_process.exec calls and extracts binary name', async () => {
    writeFile(tmpDir, 'src/deploy.ts', [
      "import { exec } from 'child_process';",
      "exec('git clone https://github.com/repo');",
    ].join('\n'));

    const refs = await extractBinaries(['src/deploy.ts'], tmpDir);

    const gitRef = refs.find(r => r.value === 'git');
    assert.ok(gitRef, 'should detect git binary from exec call');
    assert.equal(gitRef.source.filePath, 'src/deploy.ts');
    assert.equal(gitRef.source.line, 2);
    assert.equal(gitRef.confidence, 'high');
  });

  it('detects child_process.spawn calls and extracts binary name', async () => {
    writeFile(tmpDir, 'src/runner.ts', "spawn('docker', ['run', '-it', 'ubuntu']);");

    const refs = await extractBinaries(['src/runner.ts'], tmpDir);

    const dockerRef = refs.find(r => r.value === 'docker');
    assert.ok(dockerRef, 'should detect docker binary from spawn call');
    assert.equal(dockerRef.source.filePath, 'src/runner.ts');
    assert.equal(dockerRef.confidence, 'high');
  });

  it('detects execSync calls and extracts binary name', async () => {
    writeFile(tmpDir, 'src/setup.ts', "const out = execSync('npm install --production');");

    const refs = await extractBinaries(['src/setup.ts'], tmpDir);

    const npmRef = refs.find(r => r.value === 'npm');
    assert.ok(npmRef, 'should detect npm binary from execSync call');
    assert.equal(npmRef.source.line, 1);
    assert.equal(npmRef.confidence, 'high');
  });

  it('detects shebang lines and extracts interpreter binary', async () => {
    writeFile(tmpDir, 'scripts/run.sh', '#!/usr/bin/env node\nconsole.log("hello");');

    const refs = await extractBinaries(['scripts/run.sh'], tmpDir);

    const nodeRef = refs.find(r => r.value === 'node');
    assert.ok(nodeRef, 'should detect node binary from shebang');
    assert.equal(nodeRef.source.filePath, 'scripts/run.sh');
    assert.equal(nodeRef.source.line, 1);
    assert.equal(nodeRef.confidence, 'high');
  });

  it('detects known CLI names in string literals with medium confidence', async () => {
    writeFile(tmpDir, 'src/tools.ts', "const endpoint = 'curl https://api.example.com';");

    const refs = await extractBinaries(['src/tools.ts'], tmpDir);

    const curlRef = refs.find(r => r.value === 'curl');
    assert.ok(curlRef, 'should detect curl in string literal');
    assert.equal(curlRef.confidence, 'medium');
  });

  it('extracts all commands from pipe chains', async () => {
    writeFile(tmpDir, 'src/scan.ts', "exec('cat /etc/passwd | grep root | wc -l');");

    const refs = await extractBinaries(['src/scan.ts'], tmpDir);

    const binaries = refs.map(r => r.value);
    assert.ok(binaries.includes('cat'), 'should extract cat from pipe chain');
    assert.ok(binaries.includes('grep'), 'should extract grep from pipe chain');
    assert.ok(binaries.includes('wc'), 'should extract wc from pipe chain');
  });

  it('extracts all commands from && chains', async () => {
    writeFile(tmpDir, 'src/build.ts', "exec('mkdir -p dist && cp -r src/* dist && echo done');");

    const refs = await extractBinaries(['src/build.ts'], tmpDir);

    const binaries = refs.map(r => r.value);
    assert.ok(binaries.includes('mkdir'), 'should extract mkdir from && chain');
    assert.ok(binaries.includes('cp'), 'should extract cp from && chain');
    assert.ok(binaries.includes('echo'), 'should extract echo from && chain');
  });

  it('marks variable interpolation commands as low confidence', async () => {
    writeFile(tmpDir, 'src/dynamic.ts', "execSync(`${command} --verbose`);");

    const refs = await extractBinaries(['src/dynamic.ts'], tmpDir);

    assert.ok(refs.length >= 1, 'should detect at least one ref');
    assert.equal(refs[0]!.confidence, 'low');
  });

  it('deduplicates same binary at same file and line keeping highest confidence', async () => {
    // exec('git clone repo') triggers both child_process detection (high)
    // and known CLI detection (medium) for 'git' at the same line.
    writeFile(tmpDir, 'src/deploy.ts', "exec('git clone repo');");

    const refs = await extractBinaries(['src/deploy.ts'], tmpDir);

    const gitRefs = refs.filter(r => r.value === 'git');
    assert.equal(gitRefs.length, 1, 'should have exactly one git ref after dedup');
    assert.equal(gitRefs[0]!.confidence, 'high', 'should keep highest confidence');
  });

  it('returns empty array for file with no binary references', async () => {
    writeFile(tmpDir, 'src/math.ts', [
      'const x = 42;',
      'function add(a: number, b: number) { return a + b; }',
      "const msg = 'hello world';",
    ].join('\n'));

    const refs = await extractBinaries(['src/math.ts'], tmpDir);

    assert.deepEqual(refs, []);
  });
});

// ---------------------------------------------------------------------------
// Domain extraction (T010)
// ---------------------------------------------------------------------------

describe('URI_REGEX', () => {
  it('matches valid http/https/ws/wss URLs', () => {
    const urls = [
      'http://example.com',
      'https://api.example.com/v1/users',
      'ws://socket.example.com:8080',
      'wss://secure.example.com/ws',
      'https://sub.domain.example.com:443/path',
    ];
    for (const url of urls) {
      const matches = url.match(new RegExp(URI_REGEX.source, URI_REGEX.flags));
      assert.ok(matches, `should match ${url}`);
    }
  });

  it('rejects file paths and file:// URIs', () => {
    const nonUrls = [
      '/usr/local/bin/node',
      'file:///home/user/file.txt',
      './relative/path',
      '../parent/path',
      '/var/run/docker.sock',
    ];
    for (const str of nonUrls) {
      const matches = str.match(new RegExp(URI_REGEX.source, URI_REGEX.flags));
      assert.equal(matches, null, `should not match ${str}`);
    }
  });

  it('captures named groups correctly', () => {
    const regex = new RegExp(URI_REGEX.source, URI_REGEX.flags);
    const [match] = 'https://api.example.com:8080/v1/users'.matchAll(regex);
    assert.ok(match);
    assert.equal(match.groups!.scheme, 'https');
    assert.equal(match.groups!.host, 'api.example.com');
    assert.equal(match.groups!.port, '8080');
    assert.equal(match.groups!.path, '/v1/users');
  });
});

describe('isLocalhostWithStandardPort', () => {
  it('returns true for localhost with no port', () => {
    assert.ok(isLocalhostWithStandardPort('localhost', undefined));
  });

  it('returns true for 127.0.0.1 with port 80', () => {
    assert.ok(isLocalhostWithStandardPort('127.0.0.1', 80));
  });

  it('returns true for ::1 with port 443', () => {
    assert.ok(isLocalhostWithStandardPort('::1', 443));
  });

  it('returns false for localhost with non-standard port', () => {
    assert.ok(!isLocalhostWithStandardPort('localhost', 8080));
  });

  it('returns false for non-localhost hostname', () => {
    assert.ok(!isLocalhostWithStandardPort('example.com', undefined));
  });
});

describe('extractDomains', () => {
  it('extracts standard http/https/ws/wss URLs', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/api.ts',
      content: [
        'const api = "https://api.example.com/v1";',
        'const ws = "wss://ws.example.com:9090/live";',
        'const plain = "http://cdn.example.com/assets";',
        'const sock = "ws://stream.example.com/feed";',
      ].join('\n'),
    }];

    const domains = extractDomains(files);

    assert.equal(domains.length, 4);
    const api = domains.find(d => d.hostname === 'api.example.com');
    const ws = domains.find(d => d.hostname === 'ws.example.com');
    const cdn = domains.find(d => d.hostname === 'cdn.example.com');
    const stream = domains.find(d => d.hostname === 'stream.example.com');
    assert.ok(api);
    assert.equal(api.scheme, 'https');
    assert.equal(api.port, undefined);
    assert.ok(ws);
    assert.equal(ws.scheme, 'wss');
    assert.equal(ws.port, 9090);
    assert.ok(cdn);
    assert.equal(cdn.scheme, 'http');
    assert.ok(stream);
    assert.equal(stream.scheme, 'ws');
  });

  it('extracts bare hostnames from fetch/axios/http.get/new URL calls', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/client.ts',
      content: [
        "fetch('api.github.com/users');",
        "axios('data.service.io:3000/query');",
        "http.get('metrics.internal.net/health');",
        "new URL('cdn.assets.org/images');",
      ].join('\n'),
    }];

    const domains = extractDomains(files);

    const github = domains.find(d => d.hostname === 'api.github.com');
    const service = domains.find(d => d.hostname === 'data.service.io');
    const metrics = domains.find(d => d.hostname === 'metrics.internal.net');
    const cdn = domains.find(d => d.hostname === 'cdn.assets.org');
    assert.ok(github, 'should extract api.github.com from fetch');
    assert.ok(service, 'should extract data.service.io from axios');
    assert.equal(service!.port, 3000);
    assert.ok(metrics, 'should extract metrics.internal.net from http.get');
    assert.ok(cdn, 'should extract cdn.assets.org from new URL');
  });

  it('deduplicates by hostname+port keeping first occurrence', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/a.ts',
      content: 'const x = "https://api.example.com/v1";',
    }, {
      path: 'src/b.ts',
      content: 'const y = "https://api.example.com/v2";',
    }];

    const domains = extractDomains(files);

    const exampleDomains = domains.filter(d => d.hostname === 'api.example.com');
    assert.equal(exampleDomains.length, 1, 'should deduplicate same hostname');
    assert.equal(exampleDomains[0]!.sourceFile, 'src/a.ts', 'should keep first occurrence');
  });

  it('excludes localhost with standard ports but includes non-standard', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/dev.ts',
      content: [
        'const a = "http://localhost/api";',
        'const b = "http://localhost:80/api";',
        'const c = "https://127.0.0.1:443/api";',
        'const d = "http://localhost:8080/api";',
        'const e = "http://127.0.0.1:3000/api";',
      ].join('\n'),
    }];

    const domains = extractDomains(files);

    const keys = domains.map(d => d.port !== undefined ? `${d.hostname}:${d.port}` : d.hostname);
    assert.ok(!keys.includes('localhost'), 'should exclude localhost with no port');
    assert.ok(!keys.includes('localhost:80'), 'should exclude localhost:80');
    assert.ok(!keys.includes('127.0.0.1:443'), 'should exclude 127.0.0.1:443');
    assert.ok(keys.includes('localhost:8080'), 'should include localhost:8080');
    assert.ok(keys.includes('127.0.0.1:3000'), 'should include 127.0.0.1:3000');
    assert.equal(domains.length, 2);
  });

  it('does not extract file:// URIs or unix socket paths', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/files.ts',
      content: [
        'const a = "file:///home/user/data.json";',
        'const b = "/var/run/docker.sock";',
        'const c = "https://real.example.com/api";',
      ].join('\n'),
    }];

    const domains = extractDomains(files);

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'real.example.com');
  });

  it('scans .json, .yaml, .yml, and .env config files', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'config/api.json',
        content: '{ "endpoint": "https://json.example.com/api" }',
      },
      {
        path: 'config/settings.yaml',
        content: 'api_url: https://yaml.example.com/v1',
      },
      {
        path: 'config/prod.yml',
        content: 'host: https://yml.example.com/prod',
      },
      {
        path: '.env',
        content: 'API_URL=https://env.example.com/v2',
      },
      {
        path: 'config/skip.toml',
        content: 'url = "https://toml.example.com"',
      },
    ];

    const domains = extractDomains(files);

    const hostnames = domains.map(d => d.hostname);
    assert.ok(hostnames.includes('json.example.com'), 'should scan .json');
    assert.ok(hostnames.includes('yaml.example.com'), 'should scan .yaml');
    assert.ok(hostnames.includes('yml.example.com'), 'should scan .yml');
    assert.ok(hostnames.includes('env.example.com'), 'should scan .env');
    assert.ok(!hostnames.includes('toml.example.com'), 'should not scan .toml');
  });
});

// ---------------------------------------------------------------------------
// extractUrlDomains (T010.b)
// ---------------------------------------------------------------------------

describe('extractUrlDomains', () => {
  it('extracts multiple URLs on one line', () => {
    const content = 'const a = "https://one.example.com/api" + "http://two.example.com/v2";';
    const domains = extractUrlDomains(content, 'src/app.ts');

    assert.equal(domains.length, 2);
    assert.equal(domains[0]!.hostname, 'one.example.com');
    assert.equal(domains[0]!.scheme, 'https');
    assert.equal(domains[1]!.hostname, 'two.example.com');
    assert.equal(domains[1]!.scheme, 'http');
    // Both on line 1
    assert.equal(domains[0]!.line, 1);
    assert.equal(domains[1]!.line, 1);
    assert.equal(domains[0]!.sourceFile, 'src/app.ts');
  });

  it('extracts URLs with explicit ports', () => {
    const content = [
      'const api = "https://api.example.com:8443/v1";',
      'const ws = "ws://stream.example.com:9090/feed";',
    ].join('\n');
    const domains = extractUrlDomains(content, 'src/config.ts');

    const api = domains.find(d => d.hostname === 'api.example.com');
    const ws = domains.find(d => d.hostname === 'stream.example.com');
    assert.ok(api);
    assert.equal(api.port, 8443);
    assert.equal(api.line, 1);
    assert.ok(ws);
    assert.equal(ws.port, 9090);
    assert.equal(ws.line, 2);
  });

  it('extracts URLs with paths without stripping them from the match', () => {
    const content = 'const url = "https://api.example.com/v1/users/search?q=test";';
    const domains = extractUrlDomains(content, 'src/api.ts');

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'api.example.com');
    // Path is not stripped — the context snippet should include the path
    assert.ok(domains[0]!.context.includes('/v1/users/search'));
  });

  it('extracts ws:// and wss:// schemes', () => {
    const content = [
      'const ws = "ws://realtime.example.com/events";',
      'const wss = "wss://secure.example.com:4443/stream";',
    ].join('\n');
    const domains = extractUrlDomains(content, 'src/ws.ts');

    assert.equal(domains.length, 2);
    const ws = domains.find(d => d.scheme === 'ws');
    const wss = domains.find(d => d.scheme === 'wss');
    assert.ok(ws);
    assert.equal(ws.hostname, 'realtime.example.com');
    assert.ok(wss);
    assert.equal(wss.hostname, 'secure.example.com');
    assert.equal(wss.port, 4443);
  });

  it('includes localhost:3000 but excludes localhost:80', () => {
    const content = [
      'const dev = "http://localhost:3000/api";',
      'const standard = "http://localhost:80/api";',
      'const plain = "http://localhost/api";',
      'const secure = "https://127.0.0.1:443/api";',
      'const custom = "http://127.0.0.1:5000/api";',
    ].join('\n');
    const domains = extractUrlDomains(content, 'src/dev.ts');

    const hostKeys = domains.map(d => d.port !== undefined ? `${d.hostname}:${d.port}` : d.hostname);
    assert.ok(hostKeys.includes('localhost:3000'), 'should include localhost:3000');
    assert.ok(hostKeys.includes('127.0.0.1:5000'), 'should include 127.0.0.1:5000');
    assert.ok(!hostKeys.includes('localhost:80'), 'should exclude localhost:80');
    assert.ok(!hostKeys.includes('localhost'), 'should exclude plain localhost');
    assert.ok(!hostKeys.includes('127.0.0.1:443'), 'should exclude 127.0.0.1:443');
    assert.equal(domains.length, 2);
  });

  it('does not match file:// URIs', () => {
    const content = [
      'const f = "file:///home/user/data.json";',
      'const g = "file:///var/log/app.log";',
      'const h = "https://real.example.com/api";',
    ].join('\n');
    const domains = extractUrlDomains(content, 'src/files.ts');

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'real.example.com');
  });

  it('produces correct context snippets at line boundaries', () => {
    // URL at very start of line — no left context to clip
    const startLine = 'https://start.example.com/path and more text after';
    const domains1 = extractUrlDomains(startLine, 'test.ts');
    assert.equal(domains1.length, 1);
    assert.ok(domains1[0]!.context.startsWith('https://'));

    // URL at very end of line — no right context to clip
    const endLine = 'some prefix text before https://end.example.com';
    const domains2 = extractUrlDomains(endLine, 'test.ts');
    assert.equal(domains2.length, 1);
    assert.ok(domains2[0]!.context.endsWith('end.example.com'));

    // Short line where entire line is the context
    const shortLine = 'https://x.co';
    const domains3 = extractUrlDomains(shortLine, 'test.ts');
    assert.equal(domains3.length, 1);
    assert.equal(domains3[0]!.context, 'https://x.co');
  });
});

// ---------------------------------------------------------------------------
// NETWORK_CONTEXT_PATTERNS (T010.c)
// ---------------------------------------------------------------------------

describe('NETWORK_CONTEXT_PATTERNS', () => {
  it('has patterns for all required network APIs', () => {
    assert.ok(Array.isArray(NETWORK_CONTEXT_PATTERNS));
    assert.equal(NETWORK_CONTEXT_PATTERNS.length, 10);
  });

  it('matches fetch() calls', () => {
    const line = "fetch('api.example.com/users')";
    const matched = NETWORK_CONTEXT_PATTERNS.some(p => p.test(line));
    assert.ok(matched, 'should match fetch call');
  });

  it('matches axios.get() calls', () => {
    const line = "axios.get('api.example.com/data')";
    const matched = NETWORK_CONTEXT_PATTERNS.some(p => p.test(line));
    assert.ok(matched, 'should match axios.get call');
  });

  it('matches axios.post() calls', () => {
    const line = "axios.post('api.example.com/submit')";
    const matched = NETWORK_CONTEXT_PATTERNS.some(p => p.test(line));
    assert.ok(matched, 'should match axios.post call');
  });

  it('matches http.get() calls', () => {
    const line = "http.get('metrics.internal.net/health')";
    const matched = NETWORK_CONTEXT_PATTERNS.some(p => p.test(line));
    assert.ok(matched, 'should match http.get call');
  });

  it('matches http.request() calls', () => {
    const line = "http.request('api.service.io/rpc')";
    const matched = NETWORK_CONTEXT_PATTERNS.some(p => p.test(line));
    assert.ok(matched, 'should match http.request call');
  });

  it('matches new URL() calls', () => {
    const line = "new URL('cdn.assets.org/images')";
    const matched = NETWORK_CONTEXT_PATTERNS.some(p => p.test(line));
    assert.ok(matched, 'should match new URL call');
  });

  it('matches dns.resolve() calls', () => {
    const line = "dns.resolve('mail.example.com')";
    const matched = NETWORK_CONTEXT_PATTERNS.some(p => p.test(line));
    assert.ok(matched, 'should match dns.resolve call');
  });

  it('matches dns.lookup() calls', () => {
    const line = "dns.lookup('db.internal.net')";
    const matched = NETWORK_CONTEXT_PATTERNS.some(p => p.test(line));
    assert.ok(matched, 'should match dns.lookup call');
  });

  it('matches Host header in string literals', () => {
    const line = "headers: { 'Host': 'api.example.com' }";
    const matched = NETWORK_CONTEXT_PATTERNS.some(p => p.test(line));
    assert.ok(matched, 'should match Host header');
  });
});

// ---------------------------------------------------------------------------
// extractBareDomains (T010.c)
// ---------------------------------------------------------------------------

describe('extractBareDomains', () => {
  it('extracts bare domain from fetch() call', () => {
    const content = "fetch('api.github.com/users');";
    const domains = extractBareDomains(content, 'src/client.ts');

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'api.github.com');
    assert.equal(domains[0]!.scheme, 'https');
    assert.equal(domains[0]!.line, 1);
    assert.equal(domains[0]!.sourceFile, 'src/client.ts');
  });

  it('extracts bare domain from axios.get() call', () => {
    const content = "axios.get('data.service.io/query');";
    const domains = extractBareDomains(content, 'src/api.ts');

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'data.service.io');
  });

  it('extracts bare domain from axios.post() call', () => {
    const content = "axios.post('submit.example.com/form');";
    const domains = extractBareDomains(content, 'src/form.ts');

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'submit.example.com');
  });

  it('extracts bare domain from http.get() call', () => {
    const content = "http.get('metrics.internal.net/health');";
    const domains = extractBareDomains(content, 'src/health.ts');

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'metrics.internal.net');
  });

  it('extracts bare domain from http.request() call', () => {
    const content = "http.request('api.service.io/rpc');";
    const domains = extractBareDomains(content, 'src/rpc.ts');

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'api.service.io');
  });

  it('extracts bare domain from new URL() call', () => {
    const content = "new URL('cdn.assets.org/images');";
    const domains = extractBareDomains(content, 'src/cdn.ts');

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'cdn.assets.org');
  });

  it('extracts bare domain from dns.resolve() call', () => {
    const content = "dns.resolve('mail.example.com');";
    const domains = extractBareDomains(content, 'src/dns.ts');

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'mail.example.com');
  });

  it('extracts bare domain from dns.lookup() call', () => {
    const content = "dns.lookup('db.internal.net');";
    const domains = extractBareDomains(content, 'src/dns.ts');

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'db.internal.net');
  });

  it('extracts bare domain from Host header', () => {
    const content = "headers: { 'Host': 'api.example.com' }";
    const domains = extractBareDomains(content, 'src/req.ts');

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'api.example.com');
  });

  it('extracts bare domain with port', () => {
    const content = "fetch('api.example.com:8080/v1');";
    const domains = extractBareDomains(content, 'src/client.ts');

    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'api.example.com');
    assert.equal(domains[0]!.port, 8080);
  });

  it('rejects relative paths', () => {
    const content = [
      "fetch('/api/users');",
      "fetch('./local/resource');",
      "fetch('../parent/data');",
    ].join('\n');
    const domains = extractBareDomains(content, 'src/local.ts');

    assert.equal(domains.length, 0);
  });

  it('rejects template variable interpolation', () => {
    const content = [
      "fetch(`${baseUrl}/api`);",
      "fetch('$HOST/api');",
    ].join('\n');
    const domains = extractBareDomains(content, 'src/dynamic.ts');

    assert.equal(domains.length, 0);
  });

  it('skips URLs with schemes (defers to extractUrlDomains)', () => {
    const content = "fetch('https://api.example.com/v1');";
    const domains = extractBareDomains(content, 'src/api.ts');

    assert.equal(domains.length, 0);
  });

  it('filters localhost with standard ports but keeps non-standard', () => {
    const content = [
      "fetch('localhost.example.com/api');",
    ].join('\n');
    const domains = extractBareDomains(content, 'src/dev.ts');

    // localhost.example.com has a dot so it's a valid bare domain
    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'localhost.example.com');
  });

  it('includes context snippet for each match', () => {
    const content = "const res = fetch('api.github.com/users');";
    const domains = extractBareDomains(content, 'src/app.ts');

    assert.equal(domains.length, 1);
    assert.ok(domains[0]!.context.includes('api.github.com'));
    assert.ok(domains[0]!.context.length > 0);
  });

  it('extracts domains from multiple lines', () => {
    const content = [
      "fetch('api.github.com/users');",
      "dns.resolve('mail.example.com');",
      "http.get('metrics.internal.net/health');",
    ].join('\n');
    const domains = extractBareDomains(content, 'src/multi.ts');

    assert.equal(domains.length, 3);
    const hostnames = domains.map(d => d.hostname);
    assert.ok(hostnames.includes('api.github.com'));
    assert.ok(hostnames.includes('mail.example.com'));
    assert.ok(hostnames.includes('metrics.internal.net'));
    assert.equal(domains[0]!.line, 1);
    assert.equal(domains[1]!.line, 2);
    assert.equal(domains[2]!.line, 3);
  });
});

// ---------------------------------------------------------------------------
// isFilePath (T011.b)
// ---------------------------------------------------------------------------

describe('isFilePath', () => {
  it('accepts absolute POSIX, Windows, home-relative, and relative paths', () => {
    assert.ok(isFilePath('/etc/hosts'));
    assert.ok(isFilePath('/tmp/foo'));
    assert.ok(isFilePath('C:\\Users\\foo'));
    assert.ok(isFilePath('D:/data/file.txt'));
    assert.ok(isFilePath('~/config'));
    assert.ok(isFilePath('~/.ssh/id_rsa'));
    assert.ok(isFilePath('./data/input.json'));
    assert.ok(isFilePath('../config/settings.yaml'));
  });

  it('rejects URLs, bare module specifiers, and scoped packages', () => {
    assert.ok(!isFilePath('https://example.com/path'));
    assert.ok(!isFilePath('http://cdn.example.com'));
    assert.ok(!isFilePath('wss://socket.example.com'));
    assert.ok(!isFilePath('lodash'));
    assert.ok(!isFilePath('express'));
    assert.ok(!isFilePath('@types/node'));
    assert.ok(!isFilePath('@scope/pkg'));
  });

  it('rejects protocol-relative URLs and bare slash', () => {
    assert.ok(!isFilePath('//cdn.example.com'));
    assert.ok(!isFilePath('/'));
  });
});

// ---------------------------------------------------------------------------
// classifyAccess (T011.c)
// ---------------------------------------------------------------------------

describe('classifyAccess', () => {
  it('classifies read and write APIs correctly', () => {
    // Read APIs
    assert.equal(classifyAccess('fs.readFile'), 'read');
    assert.equal(classifyAccess('fs.readFileSync'), 'read');
    assert.equal(classifyAccess('fs.createReadStream'), 'read');
    assert.equal(classifyAccess('readFile'), 'read');
    assert.equal(classifyAccess('readFileSync'), 'read');
    assert.equal(classifyAccess('createReadStream'), 'read');

    // Write APIs
    assert.equal(classifyAccess('fs.writeFile'), 'write');
    assert.equal(classifyAccess('fs.writeFileSync'), 'write');
    assert.equal(classifyAccess('fs.appendFile'), 'write');
    assert.equal(classifyAccess('fs.appendFileSync'), 'write');
    assert.equal(classifyAccess('fs.createWriteStream'), 'write');
    assert.equal(classifyAccess('fs.mkdir'), 'write');
    assert.equal(classifyAccess('fs.mkdirSync'), 'write');
    assert.equal(classifyAccess('writeFile'), 'write');
    assert.equal(classifyAccess('writeFileSync'), 'write');
    assert.equal(classifyAccess('appendFile'), 'write');
    assert.equal(classifyAccess('appendFileSync'), 'write');
    assert.equal(classifyAccess('createWriteStream'), 'write');
    assert.equal(classifyAccess('mkdir'), 'write');
    assert.equal(classifyAccess('mkdirSync'), 'write');

    // Unknown API
    assert.equal(classifyAccess('fs.stat'), 'unknown');
    assert.equal(classifyAccess('console.log'), 'unknown');
  });

  it('inspects flag argument for fs.open and fs.openSync', () => {
    // 'r' flag → read
    assert.equal(classifyAccess('fs.open', 'r'), 'read');
    assert.equal(classifyAccess('fs.openSync', 'r'), 'read');
    assert.equal(classifyAccess('open', 'r'), 'read');
    assert.equal(classifyAccess('openSync', 'r'), 'read');

    // Write flags → write
    assert.equal(classifyAccess('fs.open', 'w'), 'write');
    assert.equal(classifyAccess('fs.openSync', 'a'), 'write');
    assert.equal(classifyAccess('fs.open', 'w+'), 'write');
    assert.equal(classifyAccess('fs.openSync', 'a+'), 'write');

    // Missing or unrecognised flag → unknown
    assert.equal(classifyAccess('fs.open'), 'unknown');
    assert.equal(classifyAccess('fs.openSync', 'rs'), 'unknown');
    assert.equal(classifyAccess('openSync'), 'unknown');
  });

  it('READ_APIS and WRITE_APIS do not overlap', () => {
    for (const api of READ_APIS) {
      assert.ok(!WRITE_APIS.has(api), `${api} should not be in both READ_APIS and WRITE_APIS`);
    }
  });
});

// ---------------------------------------------------------------------------
// isImportOrRequirePath (T011.d)
// ---------------------------------------------------------------------------

describe('isImportOrRequirePath', () => {
  it('returns true for require() calls with single and double quotes', () => {
    assert.ok(isImportOrRequirePath("const fs = require('./utils/fs.js');", './utils/fs.js'));
    assert.ok(isImportOrRequirePath('const mod = require("./config.js");', './config.js'));
    assert.ok(isImportOrRequirePath("const x = require( './spaced.js' );", './spaced.js'));
  });

  it('returns true for import ... from statements', () => {
    assert.ok(isImportOrRequirePath("import fs from './utils/fs.js';", './utils/fs.js'));
    assert.ok(isImportOrRequirePath('import { helper } from "../lib/helper.js";', '../lib/helper.js'));
    assert.ok(isImportOrRequirePath("export { foo } from './bar.js';", './bar.js'));
  });

  it('returns true for dynamic import() expressions', () => {
    assert.ok(isImportOrRequirePath("const mod = await import('./lazy.js');", './lazy.js'));
    assert.ok(isImportOrRequirePath('const m = import("./dynamic.js");', './dynamic.js'));
    assert.ok(isImportOrRequirePath("import( './spaced.js' ).then(m => m);", './spaced.js'));
  });

  it('returns true for side-effect import statements', () => {
    assert.ok(isImportOrRequirePath("import './polyfill.js';", './polyfill.js'));
    assert.ok(isImportOrRequirePath('import "./setup.js";', './setup.js'));
  });

  it('returns false for non-import/require contexts', () => {
    assert.ok(!isImportOrRequirePath("readFileSync('/etc/hosts');", '/etc/hosts'));
    assert.ok(!isImportOrRequirePath("const p = '/tmp/foo';", '/tmp/foo'));
    assert.ok(!isImportOrRequirePath("writeFile('~/config', data);", '~/config'));
  });

  it('returns false when literal does not match the import path', () => {
    assert.ok(!isImportOrRequirePath("import fs from './utils/fs.js';", './other.js'));
    assert.ok(!isImportOrRequirePath("const mod = require('./config.js');", './different.js'));
  });
});

// ---------------------------------------------------------------------------
// extractFilePaths (T011.b)
// ---------------------------------------------------------------------------

describe('extractFilePaths', () => {
  it('classifies read and write access types correctly', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/io.ts',
      content: [
        "const data = readFileSync('/etc/config.json');",
        "readFile('/var/data/input.csv', cb);",
        "createReadStream('/tmp/large.log');",
        "writeFileSync('/tmp/output.json', data);",
        "writeFile('/var/log/app.log', msg, cb);",
        "appendFile('/var/log/audit.log', entry);",
        "createWriteStream('/tmp/export.csv');",
        "mkdirSync('/tmp/build');",
      ].join('\n'),
    }];

    const paths = extractFilePaths(files);

    const reads = paths.filter(p => p.accessType === 'read');
    const writes = paths.filter(p => p.accessType === 'write');
    assert.equal(reads.length, 3, 'should detect 3 read accesses');
    assert.equal(writes.length, 5, 'should detect 5 write accesses');
    assert.ok(reads.some(p => p.path === '/etc/config.json'));
    assert.ok(reads.some(p => p.path === '/var/data/input.csv'));
    assert.ok(reads.some(p => p.path === '/tmp/large.log'));
    assert.ok(writes.some(p => p.path === '/tmp/output.json'));
    assert.ok(writes.some(p => p.path === '/var/log/app.log'));
    assert.ok(writes.some(p => p.path === '/var/log/audit.log'));
    assert.ok(writes.some(p => p.path === '/tmp/export.csv'));
    assert.ok(writes.some(p => p.path === '/tmp/build'));
  });

  it('excludes paths in import and require statements', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/app.ts',
      content: [
        "import fs from './utils/fs.js';",
        "export { helper } from '../lib/helper.js';",
        "const mod = require('./config.js');",
        "const data = readFileSync('/etc/hosts');",
      ].join('\n'),
    }];

    const paths = extractFilePaths(files);

    assert.equal(paths.length, 1, 'should only extract the readFileSync path');
    assert.equal(paths[0]!.path, '/etc/hosts');
    assert.equal(paths[0]!.accessType, 'read');
  });

  it('detects absolute and home-relative paths as unknown access', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/config.ts',
      content: [
        "const hosts = '/etc/hosts';",
        "const tmp = '/tmp/scratch';",
        "const home = '~/config/settings.yaml';",
        "const rel = 'lodash';",
      ].join('\n'),
    }];

    const paths = extractFilePaths(files);

    assert.equal(paths.length, 3, 'should detect 3 paths');
    const etc = paths.find(p => p.path === '/etc/hosts');
    const tmp = paths.find(p => p.path === '/tmp/scratch');
    const home = paths.find(p => p.path === '~/config/settings.yaml');
    assert.ok(etc, 'should detect /etc/hosts');
    assert.equal(etc!.accessType, 'unknown');
    assert.equal(etc!.line, 1);
    assert.ok(tmp, 'should detect /tmp/scratch');
    assert.equal(tmp!.accessType, 'unknown');
    assert.ok(home, 'should detect ~/config/settings.yaml');
    assert.equal(home!.accessType, 'unknown');
    // lodash is not a file path — should not be extracted
    assert.ok(!paths.some(p => p.path === 'lodash'));
  });

  it('detects Windows drive paths and relative paths in fs API contexts', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/platform.ts',
      content: [
        "const cfg = readFileSync('C:\\\\Users\\\\foo\\\\config.json');",
        "writeFileSync('D:/data/output.txt', data);",
        "const local = readFileSync('./data/input.json');",
        "const parent = readFileSync('../config/settings.yaml');",
        "const home = '~/myconfig';",
      ].join('\n'),
    }];

    const paths = extractFilePaths(files);

    assert.ok(paths.some(p => p.path === 'C:\\\\Users\\\\foo\\\\config.json' && p.accessType === 'read'),
      'should detect Windows backslash path as read');
    assert.ok(paths.some(p => p.path === 'D:/data/output.txt' && p.accessType === 'write'),
      'should detect Windows forward-slash path as write');
    assert.ok(paths.some(p => p.path === './data/input.json' && p.accessType === 'read'),
      'should detect relative ./ path in readFileSync as read');
    assert.ok(paths.some(p => p.path === '../config/settings.yaml' && p.accessType === 'read'),
      'should detect relative ../ path in readFileSync as read');
    assert.ok(paths.some(p => p.path === '~/myconfig' && p.accessType === 'unknown'),
      'should detect home path outside fs API as unknown');
  });

  it('infers access type from open() and openSync() flag arguments', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/fs-ops.ts',
      content: [
        "open('/tmp/read.txt', 'r', cb);",
        "openSync('/tmp/write.txt', 'w');",
        "fs.open('/tmp/append.txt', 'a', cb);",
        "fs.openSync('/tmp/no-flag.txt');",
      ].join('\n'),
    }];

    const paths = extractFilePaths(files);

    const readPath = paths.find(p => p.path === '/tmp/read.txt');
    assert.ok(readPath, 'should detect /tmp/read.txt');
    assert.equal(readPath!.accessType, 'read', "open with 'r' flag should be read");

    const writePath = paths.find(p => p.path === '/tmp/write.txt');
    assert.ok(writePath, 'should detect /tmp/write.txt');
    assert.equal(writePath!.accessType, 'write', "openSync with 'w' flag should be write");

    const appendPath = paths.find(p => p.path === '/tmp/append.txt');
    assert.ok(appendPath, 'should detect /tmp/append.txt');
    assert.equal(appendPath!.accessType, 'write', "fs.open with 'a' flag should be write");

    const noFlagPath = paths.find(p => p.path === '/tmp/no-flag.txt');
    assert.ok(noFlagPath, 'should detect /tmp/no-flag.txt');
    assert.equal(noFlagPath!.accessType, 'unknown', 'openSync without flag should be unknown');
  });
});

// ---------------------------------------------------------------------------
// extractConfigFiles (T013.c)
// ---------------------------------------------------------------------------

describe('extractConfigFiles', () => {
  it('returns entries for .env, .env.local, .env.production variants', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/config.ts',
      content: [
        'dotenv.config({ path: ".env" });',
        'dotenv.config({ path: ".env.local" });',
        'dotenv.config({ path: ".env.production" });',
      ].join('\n'),
    }];

    const entries = extractConfigFiles(files);
    const patterns = entries.map(e => e.matchedPattern);

    assert.ok(patterns.includes('.env'), 'should find .env');
    assert.ok(patterns.includes('.env.local'), 'should find .env.local');
    assert.ok(patterns.includes('.env.production'), 'should find .env.production');
    for (const entry of entries.filter(e => patterns.indexOf(e.matchedPattern) >= 0)) {
      assert.equal(entry.configCategory, 'dotenv');
    }
  });

  it('detects JSON config files with correct category', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/loader.ts',
      content: [
        'const tsconfig = require("./tsconfig.json");',
        'const pkg = readFileSync("package.json", "utf8");',
        'loadConfig("config.json");',
      ].join('\n'),
    }];

    const entries = extractConfigFiles(files);
    const jsonEntries = entries.filter(e => e.configCategory === 'json');
    const patterns = jsonEntries.map(e => e.matchedPattern);

    assert.ok(patterns.includes('tsconfig.json'));
    assert.ok(patterns.includes('package.json'));
    assert.ok(patterns.includes('config.json'));
  });

  it('detects YAML, TOML, INI, and RC config references', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/app.ts',
      content: [
        'readFile("config.yaml");',
        'readFile("pyproject.toml");',
        'readFile("database.ini");',
        'readFile(".eslintrc");',
      ].join('\n'),
    }];

    const entries = extractConfigFiles(files);
    const categories = new Set(entries.map(e => e.configCategory));

    assert.ok(categories.has('yaml'), 'should detect yaml');
    assert.ok(categories.has('toml'), 'should detect toml');
    assert.ok(categories.has('ini'), 'should detect ini');
    assert.ok(categories.has('rc-files'), 'should detect rc-files');
  });

  it('does NOT false-positive on MIME types', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/http.ts',
      content: [
        "headers['Content-Type'] = 'application/json';",
        "accept: 'text/yaml'",
        "contentType: 'application/yaml'",
        "res.type('text/html');",
      ].join('\n'),
    }];

    const entries = extractConfigFiles(files);
    assert.equal(entries.length, 0, `expected 0 entries but got: ${JSON.stringify(entries)}`);
  });

  it('does NOT false-positive on generic strings without path context', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/utils.ts',
      content: [
        "const msg = 'hello world';",
        "const num = '42';",
        "const ext = 'json';",
        "const fmt = 'yaml format';",
      ].join('\n'),
    }];

    const entries = extractConfigFiles(files);
    assert.equal(entries.length, 0, `expected 0 entries but got: ${JSON.stringify(entries)}`);
  });

  it('each entry includes sourceFile, matchedPattern, lineNumber, configCategory', () => {
    const files: DiscoveredFile[] = [{ path: 'src/loader.ts', content: 'load("tsconfig.json");\n' }];
    const entries = extractConfigFiles(files);

    assert.ok(entries.length > 0, 'should find at least one entry');
    const entry = entries[0]!;
    assert.equal(entry.sourceFile, 'src/loader.ts');
    assert.equal(entry.matchedPattern, 'tsconfig.json');
    assert.equal(entry.lineNumber, 1);
    assert.equal(entry.configCategory, 'json');
  });

  it('handles multi-file input', () => {
    const files: DiscoveredFile[] = [
      { path: 'a.ts', content: 'load(".env")' },
      { path: 'b.ts', content: 'load("config.yaml")' },
      { path: 'c.ts', content: 'load("settings.toml")' },
    ];

    const entries = extractConfigFiles(files);
    const sources = new Set(entries.map(e => e.sourceFile));

    assert.ok(sources.has('a.ts'), 'should include a.ts');
    assert.ok(sources.has('b.ts'), 'should include b.ts');
    assert.ok(sources.has('c.ts'), 'should include c.ts');
  });

  it('finds multiple matches on the same line', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/multi.ts',
      content: 'merge("config.yaml", "settings.toml");',
    }];

    const entries = extractConfigFiles(files);
    const patterns = entries.map(e => e.matchedPattern);

    assert.ok(patterns.includes('config.yaml'), 'should find config.yaml');
    assert.ok(patterns.includes('settings.toml'), 'should find settings.toml');
    assert.ok(entries.every(e => e.lineNumber === 1), 'all should be on line 1');
  });

  it('deduplicates entries with same sourceFile + matchedPattern + lineNumber', () => {
    // Both strategies could match .env on the same line; should produce only one entry
    const files: DiscoveredFile[] = [{
      path: 'src/dup.ts',
      content: 'load(".env");',
    }];

    const entries = extractConfigFiles(files);
    const envEntries = entries.filter(e => e.matchedPattern === '.env');
    assert.equal(envEntries.length, 1, 'should deduplicate to one .env entry');
  });

  it('returns empty for lines with no config references', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/math.ts',
      content: [
        'const x = 1 + 2;',
        'function add(a: number, b: number) { return a + b; }',
        '// just a regular comment',
      ].join('\n'),
    }];

    const entries = extractConfigFiles(files);
    assert.equal(entries.length, 0);
  });

  it('returns empty for empty input', () => {
    const entries = extractConfigFiles([]);
    assert.deepEqual(entries, []);
  });

  it('detects config paths via quoted string literals with path separators', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/deep.ts',
      content: [
        'readFile("./config/app.yaml");',
        'readFile("/etc/myapp/settings.toml");',
        'readFile("../secrets/.env.local");',
      ].join('\n'),
    }];

    const entries = extractConfigFiles(files);
    const patterns = entries.map(e => e.matchedPattern);

    assert.ok(patterns.includes('app.yaml'), 'should detect app.yaml from path');
    assert.ok(patterns.includes('settings.toml'), 'should detect settings.toml from path');
    assert.ok(patterns.includes('.env.local'), 'should detect .env.local from path');
  });

  it('accepts DiscoveredFile[] and returns ConfigFileEntry[]', () => {
    const files: DiscoveredFile[] = [{ path: 'a.ts', content: '"package.json"' }];
    const result: ConfigFileEntry[] = extractConfigFiles(files);
    assert.ok(Array.isArray(result));
    assert.ok(result.length > 0);
    assert.ok('sourceFile' in result[0]!);
    assert.ok('matchedPattern' in result[0]!);
    assert.ok('lineNumber' in result[0]!);
    assert.ok('configCategory' in result[0]!);
  });
});

// ---------------------------------------------------------------------------
// extractPackageManagers (T014.b)
// ---------------------------------------------------------------------------

describe('extractPackageManagers', () => {
  it('detects npm, yarn, and pnpm CLI invocations', () => {
    const files: DiscoveredFile[] = [{
      path: 'setup.sh',
      content: [
        'npm install express',
        'yarn add lodash',
        'pnpm install typescript',
      ].join('\n'),
    }];

    const results = extractPackageManagers(files);
    const managers = results.map(r => r.manager);

    assert.ok(managers.includes('npm'), 'should detect npm');
    assert.ok(managers.includes('yarn'), 'should detect yarn');
    assert.ok(managers.includes('pnpm'), 'should detect pnpm');
  });

  it('detects pip, cargo, apt-get, brew, gem, and go install invocations', () => {
    const files: DiscoveredFile[] = [{
      path: 'install.sh',
      content: [
        'pip install requests',
        'cargo install serde',
        'apt-get install curl',
        'brew install jq',
        'gem install rails',
        'go install golang.org/x/tools@latest',
      ].join('\n'),
    }];

    const results = extractPackageManagers(files);
    const managers = results.map(r => r.manager);

    assert.ok(managers.includes('pip'), 'should detect pip');
    assert.ok(managers.includes('cargo'), 'should detect cargo');
    assert.ok(managers.includes('apt'), 'should detect apt-get');
    assert.ok(managers.includes('brew'), 'should detect brew');
    assert.ok(managers.includes('gem'), 'should detect gem');
    assert.ok(managers.includes('go'), 'should detect go install');
  });

  it('detects subprocess-style invocations containing package manager commands', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/build.ts',
      content: [
        'execSync("npm ci");',
        'spawn("pip3 install flask");',
      ].join('\n'),
    }];

    const results = extractPackageManagers(files);
    const managers = results.map(r => r.manager);

    assert.ok(managers.includes('npm'), 'should detect npm inside execSync');
    assert.ok(managers.includes('pip'), 'should detect pip3 inside spawn');
  });

  it('identifies auto-install from postinstall script in package.json', () => {
    const files: DiscoveredFile[] = [{
      path: 'package.json',
      content: JSON.stringify({
        name: 'test-pkg',
        scripts: { postinstall: 'node setup.js' },
      }),
    }];

    const results = extractPackageManagers(files);
    const lifecycle = results.find(r => r.source === 'lifecycle-script');

    assert.ok(lifecycle, 'should detect postinstall lifecycle script');
    assert.equal(lifecycle!.manager, 'npm');
    assert.equal(lifecycle!.isAutoInstall, true);
  });

  it('identifies auto-install from preinstall script in package.json', () => {
    const files: DiscoveredFile[] = [{
      path: 'package.json',
      content: JSON.stringify({
        name: 'test-pkg',
        scripts: { preinstall: 'echo check' },
      }),
    }];

    const results = extractPackageManagers(files);
    const lifecycle = results.find(r => r.source === 'lifecycle-script');

    assert.ok(lifecycle, 'should detect preinstall lifecycle script');
    assert.equal(lifecycle!.manager, 'npm');
    assert.equal(lifecycle!.isAutoInstall, true);
  });

  it('infers package manager from lockfile presence', () => {
    const files: DiscoveredFile[] = [
      { path: 'package-lock.json', content: '{}' },
      { path: 'yarn.lock', content: '' },
      { path: 'Cargo.lock', content: '' },
      { path: 'go.sum', content: '' },
      { path: 'Gemfile.lock', content: '' },
    ];

    const results = extractPackageManagers(files);
    const managers = results.map(r => r.manager);

    assert.ok(managers.includes('npm'), 'package-lock.json → npm');
    assert.ok(managers.includes('yarn'), 'yarn.lock → yarn');
    assert.ok(managers.includes('cargo'), 'Cargo.lock → cargo');
    assert.ok(managers.includes('go'), 'go.sum → go');
    assert.ok(managers.includes('gem'), 'Gemfile.lock → gem');

    for (const r of results) {
      assert.equal(r.source, 'manifest');
      assert.equal(r.isAutoInstall, false);
    }
  });

  it('each entry includes required fields', () => {
    const files: DiscoveredFile[] = [{
      path: 'deploy.sh',
      content: 'npm install express',
    }];

    const results = extractPackageManagers(files);
    assert.ok(results.length > 0);
    const entry = results[0]!;

    assert.equal(typeof entry.manager, 'string');
    assert.equal(typeof entry.source, 'string');
    assert.equal(typeof entry.file, 'string');
    assert.equal(typeof entry.isAutoInstall, 'boolean');
    assert.equal(typeof entry.line, 'number');
    assert.equal(entry.file, 'deploy.sh');
    assert.equal(entry.line, 1);
  });

  it('deduplicates by manager + file', () => {
    const files: DiscoveredFile[] = [{
      path: 'setup.sh',
      content: [
        'npm install express',
        'npm run build',
        'npm ci',
      ].join('\n'),
    }];

    const results = extractPackageManagers(files);
    const npmEntries = results.filter(r => r.manager === 'npm' && r.file === 'setup.sh');

    assert.equal(npmEntries.length, 1, 'should deduplicate npm entries for same file');
  });

  it('returns empty for files with no package manager references', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/util.ts',
      content: 'const x = 1 + 2;\nfunction add(a: number, b: number) { return a + b; }',
    }];

    const results = extractPackageManagers(files);
    assert.deepEqual(results, []);
  });

  it('returns empty for empty input', () => {
    const results = extractPackageManagers([]);
    assert.deepEqual(results, []);
  });

  it('accepts DiscoveredFile[] and returns PackageManagerEntry[]', () => {
    const files: DiscoveredFile[] = [{ path: 'x.sh', content: 'cargo build' }];
    const results: PackageManagerEntry[] = extractPackageManagers(files);
    assert.ok(Array.isArray(results));
    assert.ok(results.length > 0);
    assert.ok('manager' in results[0]!);
    assert.ok('source' in results[0]!);
    assert.ok('file' in results[0]!);
    assert.ok('isAutoInstall' in results[0]!);
  });

  it('handles invalid JSON in package.json gracefully', () => {
    const files: DiscoveredFile[] = [{
      path: 'package.json',
      content: '{ not valid json !!!',
    }];

    const results = extractPackageManagers(files);
    // Should not throw, may still produce entries from command scanning
    assert.ok(Array.isArray(results));
  });

  it('lifecycle entry wins dedup over command scan for same manager+file', () => {
    const files: DiscoveredFile[] = [{
      path: 'package.json',
      content: JSON.stringify({
        name: 'test',
        scripts: {
          postinstall: 'node build.js',
          build: 'npm run compile',
        },
      }),
    }];

    const results = extractPackageManagers(files);
    const npmEntries = results.filter(r => r.manager === 'npm' && r.file === 'package.json');

    assert.equal(npmEntries.length, 1, 'should have exactly one npm entry');
    assert.equal(npmEntries[0]!.isAutoInstall, true, 'lifecycle entry should win dedup');
    assert.equal(npmEntries[0]!.source, 'lifecycle-script');
  });

  it('detects manifest files like Pipfile and composer.json', () => {
    const files: DiscoveredFile[] = [
      { path: 'Pipfile', content: '[packages]\nrequests = "*"' },
      { path: 'composer.json', content: '{}' },
    ];

    const results = extractPackageManagers(files);
    const managers = results.map(r => r.manager);

    assert.ok(managers.includes('pip'), 'Pipfile → pip');
    assert.ok(managers.includes('composer'), 'composer.json → composer');
  });

  it('normal npm scripts without lifecycle hooks have isAutoInstall=false', () => {
    const files: DiscoveredFile[] = [{
      path: 'package.json',
      content: JSON.stringify({
        name: 'normal-pkg',
        scripts: {
          build: 'npm run compile',
          test: 'npm run jest',
          start: 'node index.js',
        },
      }),
    }];

    const results = extractPackageManagers(files);
    assert.ok(results.length > 0, 'should detect npm from scripts');
    for (const entry of results) {
      assert.equal(entry.isAutoInstall, false, 'no lifecycle scripts means isAutoInstall=false');
    }
  });

  it('deduplicates when same manager found in both command and manifest', () => {
    const files: DiscoveredFile[] = [
      {
        path: 'setup.sh',
        content: 'npm install express',
      },
      {
        path: 'package-lock.json',
        content: '{}',
      },
    ];

    const results = extractPackageManagers(files);
    const npmEntries = results.filter(r => r.manager === 'npm');

    // npm appears from command scan (setup.sh) and manifest scan (package-lock.json)
    // They are in different files, so both should appear (dedup is per manager+file)
    assert.equal(npmEntries.length, 2, 'npm from different files should not be deduped');
    assert.ok(npmEntries.some(e => e.file === 'setup.sh'), 'should have command entry');
    assert.ok(npmEntries.some(e => e.file === 'package-lock.json'), 'should have manifest entry');
  });

  it('deduplicates command and manifest in the same file', () => {
    const files: DiscoveredFile[] = [{
      path: 'package-lock.json',
      content: '{\n  "npm install": "dummy"\n}',
    }];

    const results = extractPackageManagers(files);
    const npmEntries = results.filter(r => r.manager === 'npm');

    // Command scan finds "npm install" on line 2, manifest scan also detects package-lock.json
    // Both are the same manager+file, so dedup should keep only the first match
    assert.equal(npmEntries.length, 1, 'same manager+file should be deduped to one entry');
  });

  it('detects pnpm-lock.yaml and Cargo.toml as manifest files', () => {
    const files: DiscoveredFile[] = [
      { path: 'pnpm-lock.yaml', content: 'lockfileVersion: 5.4' },
      { path: 'Cargo.toml', content: '[package]\nname = "my-crate"' },
    ];

    const results = extractPackageManagers(files);
    const managers = results.map(r => r.manager);

    assert.ok(managers.includes('pnpm'), 'pnpm-lock.yaml → pnpm');
    assert.ok(managers.includes('cargo'), 'Cargo.toml → cargo');
    for (const r of results) {
      assert.equal(r.source, 'manifest');
      assert.equal(r.isAutoInstall, false);
    }
  });

  it('detects subprocess-style invocations via child_process.exec and cp.execSync', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/installer.ts',
      content: [
        'import { exec } from "child_process";',
        'exec("pip install boto3");',
        'const result = cp.execSync("cargo build --release");',
      ].join('\n'),
    }];

    const results = extractPackageManagers(files);
    const managers = results.map(r => r.manager);

    assert.ok(managers.includes('pip'), 'should detect pip inside exec()');
    assert.ok(managers.includes('cargo'), 'should detect cargo inside cp.execSync()');
  });

  it('detects package managers across multiple source files', () => {
    const files: DiscoveredFile[] = [
      { path: 'scripts/setup.sh', content: 'apt-get install build-essential' },
      { path: 'scripts/deps.sh', content: 'brew install libpq' },
      { path: 'Gemfile', content: 'source "https://rubygems.org"\ngem "rails"' },
      { path: 'go.sum', content: 'golang.org/x/text v0.3.0 h1:abc123=\n' },
    ];

    const results = extractPackageManagers(files);
    const managers = results.map(r => r.manager);

    assert.ok(managers.includes('apt'), 'should detect apt-get');
    assert.ok(managers.includes('brew'), 'should detect brew');
    assert.ok(managers.includes('gem'), 'should detect gem from Gemfile manifest');
    assert.ok(managers.includes('go'), 'should detect go from go.sum manifest');
    assert.equal(results.length, 4, 'should find exactly 4 entries');
  });

  it('nested package.json path detects lifecycle scripts', () => {
    const files: DiscoveredFile[] = [{
      path: 'packages/core/package.json',
      content: JSON.stringify({
        name: '@myorg/core',
        scripts: { postinstall: 'node scripts/patch.js' },
      }),
    }];

    const results = extractPackageManagers(files);
    assert.ok(results.length > 0);
    const lifecycle = results.find(r => r.source === 'lifecycle-script');

    assert.ok(lifecycle, 'should detect lifecycle script in nested package.json');
    assert.equal(lifecycle!.file, 'packages/core/package.json');
    assert.equal(lifecycle!.isAutoInstall, true);
  });

  it('both preinstall and postinstall in same file produce only one lifecycle entry', () => {
    const files: DiscoveredFile[] = [{
      path: 'package.json',
      content: JSON.stringify({
        name: 'dual-hooks',
        scripts: {
          preinstall: 'echo pre',
          postinstall: 'echo post',
        },
      }),
    }];

    const results = extractPackageManagers(files);
    const lifecycleEntries = results.filter(r => r.source === 'lifecycle-script');

    assert.equal(lifecycleEntries.length, 1, 'should deduplicate lifecycle entries for same file');
    assert.equal(lifecycleEntries[0]!.isAutoInstall, true);
  });

  it('reports correct line numbers for CLI invocations', () => {
    const files: DiscoveredFile[] = [{
      path: 'install.sh',
      content: [
        '#!/bin/bash',
        'echo "setting up"',
        '',
        'pip install numpy',
        'echo "done"',
        'gem install bundler',
      ].join('\n'),
    }];

    const results = extractPackageManagers(files);
    const pip = results.find(r => r.manager === 'pip');
    const gem = results.find(r => r.manager === 'gem');

    assert.ok(pip, 'should detect pip');
    assert.equal(pip!.line, 4, 'pip install should be on line 4');
    assert.ok(gem, 'should detect gem');
    assert.equal(gem!.line, 6, 'gem install should be on line 6');
  });
});
