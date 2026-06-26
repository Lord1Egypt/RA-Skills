#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');

const FILE_MODE = 0o600;
const DEFAULT_ENV_NAMES = ['OKKIGO_API_KEY', 'OKKI_GO_API_KEY', 'OKKIGO_SKILL_API_KEY'];

process.on('uncaughtException', (error) => {
  process.stderr.write(`${error.message}\n`);
  process.exit(error.exitCode || 1);
});

function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args.positionals[0];

  if (!command || args.options.help) {
    printUsage(command ? 0 : 2);
  }

  if (command === 'login') {
    handleLogin(args.options);
    return;
  }

  if (command === 'status') {
    handleStatus(args.options);
    return;
  }

  if (command === 'resolve') {
    handleResolve(args.options);
    return;
  }

  if (command === 'doctor') {
    handleStatus({ ...args.options, json: true, diagnostics: true });
    return;
  }

  throw userError(`Unknown command: ${command}`, 2);
}

function parseArgs(argv) {
  const options = {};
  const positionals = [];

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') {
      options.help = true;
    } else if (arg === '--json') {
      options.json = true;
    } else if (arg === '--with-api-key') {
      options.withApiKey = true;
    } else if (arg === '--check') {
      options.mode = 'check';
    } else if (arg === '--source') {
      options.mode = 'source';
    } else if (arg === '--print') {
      options.mode = 'print';
    } else if (arg === '--diagnostics') {
      options.diagnostics = true;
    } else if (arg.startsWith('--')) {
      throw userError(`Unknown option: ${arg}`, 2);
    } else {
      positionals.push(arg);
    }
  }

  return { options, positionals };
}

function printUsage(exitCode) {
  const output = [
    'Usage:',
    '  node scripts/okki-auth.js login --with-api-key [--json]',
    '  node scripts/okki-auth.js status [--json] [--diagnostics]',
    '  node scripts/okki-auth.js resolve [--check|--source|--print]',
    '  node scripts/okki-auth.js doctor [--json]',
    '',
    'API keys are read from stdin for login. Status and diagnostics are redacted.'
  ].join('\n');
  const stream = exitCode === 0 ? process.stdout : process.stderr;
  stream.write(`${output}\n`);
  process.exit(exitCode);
}

function handleLogin(options) {
  if (!options.withApiKey) {
    throw userError('login requires --with-api-key', 2);
  }

  const key = firstLine(fs.readFileSync(0, 'utf8'));
  if (!isValidApiKey(key)) {
    throw userError('Invalid OKKI Go API key format: expected a value starting with sk-', 2);
  }

  const dir = okkiConfigDir();
  const credentialsPath = path.join(dir, 'credentials.json');
  const sourcePath = path.join(dir, 'auth-source.json');

  ensureDirectory(dir);
  writeSecureJson(credentialsPath, { apiKey: key });
  writeSecureJson(sourcePath, {
    version: 1,
    preferred: {
      type: 'file',
      path: credentialsPath
    },
    fallbacks: DEFAULT_ENV_NAMES.map((name) => ({ type: 'env', name }))
  });

  writeJsonOrText(options, {
    ok: true,
    configured: true,
    source: `file:${credentialsPath}`,
    path: credentialsPath,
    redacted: true
  }, 'OKKI Go API key saved.');
}

function handleStatus(options) {
  const result = resolveCredential({ includeDiagnostics: Boolean(options.diagnostics || options.json) });

  if (options.json) {
    writeJson(statusPayload(result));
  } else if (result.key) {
    process.stdout.write(`KEY_SET ${result.source}\n`);
  } else {
    process.stdout.write(`NO_KEY ${result.reason}\n`);
  }

  process.exit(result.key ? 0 : 1);
}

function handleResolve(options) {
  const mode = options.mode || 'check';
  if (!['check', 'source', 'print'].includes(mode)) {
    throw userError('resolve mode must be --check, --source, or --print', 2);
  }

  const result = resolveCredential({ includeDiagnostics: true });
  if (result.key) {
    if (mode === 'check') {
      process.stdout.write('KEY_SET\n');
    } else if (mode === 'source') {
      process.stdout.write(`${result.source}\n`);
    } else {
      process.stdout.write(`${result.key}\n`);
    }
    return;
  }

  for (const diagnostic of result.diagnostics) {
    if (diagnostic.severity === 'error' || diagnostic.severity === 'warning') {
      process.stderr.write(`${diagnostic.message}\n`);
    }
  }
  process.stdout.write('NO_KEY\n');
  process.exit(1);
}

function resolveCredential(options = {}) {
  const diagnostics = [];
  const sources = credentialSources(diagnostics);
  const seen = new Set();

  for (const source of sources) {
    const id = sourceId(source);
    if (seen.has(id)) continue;
    seen.add(id);

    const result = readSource(source);
    if (result.key) {
      return {
        key: result.key,
        source: result.source,
        diagnostics
      };
    }
    if (result.diagnostic) diagnostics.push(result.diagnostic);
  }

  return {
    key: '',
    source: '',
    reason: diagnostics.length > 0 ? diagnostics[0].reason : 'no_auth_source',
    diagnostics: options.includeDiagnostics ? diagnostics : []
  };
}

function credentialSources(diagnostics) {
  const sources = [];
  const registered = readRegisteredSources(diagnostics);
  sources.push(...registered);
  for (const name of DEFAULT_ENV_NAMES) {
    sources.push({ type: 'env', name });
  }
  sources.push({ type: 'file', path: path.join(okkiConfigDir(), 'credentials.json'), strictMode: true });
  return sources;
}

function readRegisteredSources(diagnostics) {
  const sourcePath = path.join(okkiConfigDir(), 'auth-source.json');
  if (!fs.existsSync(sourcePath)) return [];

  const validation = validateReadableFile(sourcePath, { allowedModes: ['600'], label: sourcePath });
  if (!validation.ok) {
    diagnostics.push(validation.diagnostic);
    return [];
  }

  try {
    const data = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));
    const sources = [];
    if (data && typeof data === 'object') {
      if (data.preferred) sources.push(normalizeRegisteredSource(data.preferred));
      if (Array.isArray(data.fallbacks)) {
        for (const source of data.fallbacks) sources.push(normalizeRegisteredSource(source));
      }
    }
    return sources.filter(Boolean);
  } catch (error) {
    diagnostics.push(diagnostic('invalid_json', `Ignoring ${sourcePath}: invalid JSON`, 'warning'));
    return [];
  }
}

function normalizeRegisteredSource(source) {
  if (!source || typeof source !== 'object') return null;
  if (source.type === 'file' && typeof source.path === 'string' && source.path) {
    return { type: 'file', path: source.path, strictMode: true };
  }
  if (source.type === 'env' && typeof source.name === 'string' && source.name) {
    return { type: 'env', name: source.name };
  }
  return null;
}

function readSource(source) {
  if (source.type === 'env') {
    const value = process.env[source.name] || '';
    if (!value) return {};
    if (!isValidApiKey(value)) {
      return {
        diagnostic: diagnostic('invalid_api_key', `Ignoring env:${source.name}: invalid API key format`, 'warning')
      };
    }
    return { key: value, source: `env:${source.name}` };
  }

  if (source.type === 'file') {
    return readCredentialFile(source.path, source);
  }

  return {};
}

function readCredentialFile(file, options = {}) {
  if (!fs.existsSync(file)) {
    return {
      diagnostic: diagnostic('file_missing', `Ignoring ${file}: file does not exist`, 'info')
    };
  }

  const validation = validateReadableFile(file, {
    allowedModes: options.strictMode ? ['600'] : ['600', '640', '644'],
    label: file
  });
  if (!validation.ok) {
    return { diagnostic: validation.diagnostic };
  }

  let data;
  try {
    data = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (error) {
    return {
      diagnostic: diagnostic('invalid_json', `Ignoring ${file}: invalid JSON`, 'warning')
    };
  }

  const key = data && typeof data === 'object'
    ? [data.apiKey, data.OKKIGO_API_KEY].find((value) => typeof value === 'string' && isValidApiKey(value))
    : '';
  if (!key) {
    return {
      diagnostic: diagnostic('invalid_api_key', `Ignoring ${file}: no valid API key found`, 'warning')
    };
  }

  return { key, source: `file:${file}` };
}

function validateReadableFile(file, options) {
  let stat;
  try {
    stat = fs.lstatSync(file);
  } catch (error) {
    return {
      ok: false,
      diagnostic: diagnostic('stat_failed', `Ignoring ${file}: cannot inspect file`, 'warning')
    };
  }

  if (stat.isSymbolicLink()) {
    return {
      ok: false,
      diagnostic: diagnostic('symlink_not_allowed', `Ignoring ${file}: symlinks are not allowed for credentials`, 'warning')
    };
  }

  if (!stat.isFile()) {
    return {
      ok: false,
      diagnostic: diagnostic('not_file', `Ignoring ${file}: not a regular file`, 'warning')
    };
  }

  const mode = (stat.mode & 0o777).toString(8);
  if (!options.allowedModes.includes(mode)) {
    return {
      ok: false,
      diagnostic: diagnostic(
        'insecure_permissions',
        `Ignoring ${file}: permissions must be ${options.allowedModes.join(', ')}`,
        'warning',
        { mode }
      )
    };
  }

  try {
    fs.accessSync(file, fs.constants.R_OK);
  } catch (error) {
    return {
      ok: false,
      diagnostic: diagnostic(
        'not_readable',
        `Ignoring ${file}: not readable by the current user`,
        'warning',
        currentUserDetails(stat)
      )
    };
  }

  return { ok: true };
}

function statusPayload(result) {
  return {
    configured: Boolean(result.key),
    source: result.source || null,
    reason: result.key ? null : result.reason || 'no_auth_source',
    redacted: true,
    diagnostics: result.diagnostics || []
  };
}

function writeSecureJson(file, value) {
  const temp = `${file}.tmp-${process.pid}-${Date.now()}`;
  const body = `${JSON.stringify(value, null, 2)}\n`;
  try {
    fs.writeFileSync(temp, body, { mode: FILE_MODE });
    fs.renameSync(temp, file);
    fs.chmodSync(file, FILE_MODE);
  } catch (error) {
    removeIfExists(temp);
    throw error;
  }
}

function ensureDirectory(dir) {
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
}

function okkiConfigDir() {
  const configHome = process.env.XDG_CONFIG_HOME || path.join(process.env.HOME || os.homedir(), '.config');
  return path.join(configHome, 'okki-go');
}

function isValidApiKey(value) {
  return typeof value === 'string' && value.trim() === value && value.startsWith('sk-') && value.length > 3;
}

function firstLine(value) {
  return String(value || '').trim().split(/\r?\n/)[0];
}

function sourceId(source) {
  if (source.type === 'env') return `env:${source.name}`;
  if (source.type === 'file') return `file:${source.path}`;
  return JSON.stringify(source);
}

function diagnostic(reason, message, severity, extra = {}) {
  return { reason, severity, message, ...extra };
}

function currentUserDetails(stat) {
  return {
    ownerUid: stat.uid,
    currentUid: typeof process.getuid === 'function' ? process.getuid() : null,
    currentUser: os.userInfo().username
  };
}

function writeJson(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

function writeJsonOrText(options, value, text) {
  if (options.json) {
    writeJson(value);
  } else {
    process.stdout.write(`${text}\n`);
  }
}

function removeIfExists(file) {
  try {
    fs.unlinkSync(file);
  } catch (error) {
    if (error && error.code !== 'ENOENT') throw error;
  }
}

function userError(message, exitCode) {
  const error = new Error(message);
  error.exitCode = exitCode;
  return error;
}

main();
