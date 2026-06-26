const fs = require('fs');
const path = require('path');

function getEnv(name, fallback) {
  return process.env[name] || fallback;
}

function requiredEnv(name) {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required env var: ${name}`);
  return value;
}

function apiBase() {
  return requiredEnv('AZURE_SPEECH_ENDPOINT').replace(/\/$/, '');
}

function apiVersion() {
  return getEnv('AZURE_SPEECH_API_VERSION', '2025-10-15');
}

function apiKey() {
  return requiredEnv('AZURE_SPEECH_KEY');
}

function parseArgs(argv) {
  const args = { _: [], __unknown: [] };
  for (let i = 0; i < argv.length; i++) {
    const cur = argv[i];
    if (!cur.startsWith('--')) {
      args._.push(cur);
      continue;
    }

    const eq = cur.indexOf('=');
    if (eq !== -1) {
      args[cur.slice(2, eq)] = cur.slice(eq + 1);
      continue;
    }

    const key = cur.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }

    args[key] = next;
    i++;
  }
  return args;
}

function resolveAudioFile(input) {
  if (!input) throw new Error('Missing audio file path. Use --help for usage.');
  const filePath = path.resolve(input);
  if (!fs.existsSync(filePath)) throw new Error(`Audio file not found: ${filePath}`);
  const stat = fs.statSync(filePath);
  if (!stat.isFile()) throw new Error(`Audio path is not a file: ${filePath}`);
  return { filePath, stat };
}

function ensureParentDir(targetPath) {
  const dir = path.dirname(targetPath);
  fs.mkdirSync(dir, { recursive: true });
}

function extractTranscript(data) {
  const combined = Array.isArray(data?.combinedPhrases)
    ? data.combinedPhrases.map(x => x?.text).filter(Boolean).join('\n')
    : '';
  if (combined) return combined;

  const phrases = Array.isArray(data?.phrases)
    ? data.phrases.map(x => x?.text).filter(Boolean).join('\n')
    : '';
  if (phrases) return phrases;

  if (typeof data?.text === 'string' && data.text.trim()) return data.text;
  if (typeof data?.transcript === 'string' && data.transcript.trim()) return data.transcript;
  return '';
}

function formatApiError(res, data, url) {
  const code = data?.error?.code || data?.code || String(res.status);
  const message = data?.error?.message || data?.message || res.statusText;

  let hint = '';
  if (res.status === 401 || res.status === 403) {
    hint = 'Check AZURE_SPEECH_KEY and confirm the endpoint matches the Speech resource.';
  } else if (res.status === 404) {
    hint = 'The endpoint path or resource is wrong, or the resource does not support this API/version.';
  } else if (res.status === 429) {
    hint = 'Rate limited by Azure. Retry later or add backoff.';
  } else if (res.status >= 500) {
    hint = 'Azure had a server-side wobble. Retry may succeed.';
  }

  return new Error(
    [
      `Azure Speech transcription failed: HTTP ${res.status} ${res.statusText}`,
      `Code: ${code}`,
      `Message: ${message}`,
      hint && `Hint: ${hint}`,
      `URL: ${url}`,
    ].filter(Boolean).join('\n')
  );
}

module.exports = {
  apiBase,
  apiKey,
  apiVersion,
  ensureParentDir,
  extractTranscript,
  formatApiError,
  parseArgs,
  resolveAudioFile,
};
