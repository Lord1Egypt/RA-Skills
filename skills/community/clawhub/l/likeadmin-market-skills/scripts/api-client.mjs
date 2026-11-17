#!/usr/bin/env node

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const CONFIG_FILE_NAME = 'credentials.json';

export function credentialsDirectory(homeDirectory = os.homedir()) {
  return path.resolve(homeDirectory, '.likeadmin-market-skills');
}

export function credentialsPath(homeDirectory = os.homedir()) {
  return path.join(credentialsDirectory(homeDirectory), CONFIG_FILE_NAME);
}

export function normalizeBaseUrl(value) {
  const baseUrl = String(value || '').trim().replace(/\/+$/, '');
  if (!baseUrl) throw new Error('base_url is required. Configure credentials before calling the API.');
  let parsed;
  try {
    parsed = new URL(baseUrl);
  } catch {
    throw new Error('base_url must be an absolute http(s) URL.');
  }
  if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error('base_url must use http or https.');
  return baseUrl;
}

function readCredentials(homeDirectory = os.homedir()) {
  const file = credentialsPath(homeDirectory);
  if (!fs.existsSync(file)) return {};
  try {
    const parsed = JSON.parse(fs.readFileSync(file, 'utf8'));
    return parsed && typeof parsed === 'object' ? parsed : {};
  } catch {
    throw new Error(`Invalid JSON in ${file}. Replace it with an object containing base_url and api_key.`);
  }
}

export function loadConfiguration(homeDirectory = os.homedir()) {
  const stored = readCredentials(homeDirectory);
  const baseUrl = normalizeBaseUrl(stored.base_url);
  const apiKey = String(stored.api_key || '').trim();
  if (!apiKey) throw new Error('api_key is required. Configure credentials before calling the API.');
  return { baseUrl, apiKey, credentialsFile: credentialsPath(homeDirectory) };
}

function writeCredentials(values, homeDirectory = os.homedir()) {
  const directory = credentialsDirectory(homeDirectory);
  fs.mkdirSync(directory, { recursive: true, mode: 0o700 });
  fs.chmodSync(directory, 0o700);
  const file = credentialsPath(homeDirectory);
  const merged = { ...readCredentials(homeDirectory), ...values };
  if (merged.base_url) merged.base_url = normalizeBaseUrl(merged.base_url);
  fs.writeFileSync(file, `${JSON.stringify(merged, null, 2)}\n`, { mode: 0o600 });
  fs.chmodSync(file, 0o600);
  return file;
}

export function endpoint(relativePath, configuration = loadConfiguration()) {
  const normalized = String(relativePath).replace(/^\/api\/v1\/?|^\/+/, '');
  return `${configuration.baseUrl}/api/v1/${normalized}`;
}

export async function request(relativePath, options = {}, configuration = loadConfiguration()) {
  const response = await fetch(endpoint(relativePath, configuration), {
    ...options,
    headers: {
      Accept: 'application/json',
      Authorization: `Bearer ${configuration.apiKey}`,
      ...(options.headers || {}),
    },
  });
  const raw = await response.text();
  let body;
  try {
    body = raw ? JSON.parse(raw) : {};
  } catch {
    body = { raw };
  }
  if (!response.ok || body?.code === 0) {
    const message = body?.error?.message || body?.msg || `HTTP ${response.status}`;
    throw new Error(`API request failed: ${message}`);
  }
  return body;
}

export async function upload(file, configuration = loadConfiguration(), localUploadConfirmed = false) {
  if (!localUploadConfirmed) throw new Error('Local upload requires explicit confirmation from the user.');
  const absolute = path.resolve(file);
  if (!fs.existsSync(absolute) || !fs.statSync(absolute).isFile()) throw new Error(`Not a file: ${absolute}`);
  const blob = await fs.openAsBlob(absolute);
  const form = new FormData();
  form.append('file', blob, path.basename(absolute));
  const response = await request('upload', { method: 'POST', body: form }, configuration);
  if (!response?.data?.url || typeof response.data.url !== 'string') throw new Error('Upload response did not include data.url.');
  return response;
}

export function taskStatus(payload) {
  const data = payload?.data || {};
  return String(data.status || data?.result?.status || payload?.status || '').toLowerCase();
}

export async function poll(taskId, intervalSeconds = 3, maxSeconds = 600, configuration = loadConfiguration()) {
  const deadline = Date.now() + Number(maxSeconds) * 1000;
  while (true) {
    const payload = await request(`tasks/${encodeURIComponent(taskId)}`, {}, configuration);
    const status = taskStatus(payload);
    if (['completed', 'failed', 'cancelled', 'canceled'].includes(status)) return payload;
    if (Date.now() >= deadline) throw new Error(`Polling timed out after ${maxSeconds} seconds.`);
    await new Promise((resolve) => setTimeout(resolve, Math.max(1, Number(intervalSeconds)) * 1000));
  }
}

function parseJson(value, label) {
  try {
    return JSON.parse(value);
  } catch {
    throw new Error(`${label} must be valid JSON.`);
  }
}

function maskBaseUrl(value) {
  try {
    return new URL(value).origin;
  } catch {
    return 'invalid';
  }
}

function parseConfigArguments(args) {
  const values = {};
  for (let index = 0; index < args.length; index += 2) {
    const flag = args[index];
    const value = args[index + 1];
    if (!value || !['--base-url', '--api-key'].includes(flag)) throw new Error('Usage: config set --base-url <url> --api-key <key>');
    values[flag === '--base-url' ? 'base_url' : 'api_key'] = value;
  }
  if (!values.base_url || !values.api_key) throw new Error('Both --base-url and --api-key are required.');
  return values;
}

export function parseCredentialLines(value) {
  const lines = String(value || '').split(/\r?\n/);
  const baseUrl = String(lines.shift() || '').trim();
  const apiKey = String(lines.shift() || '').trim();
  if (!baseUrl || !apiKey || lines.some((line) => line.trim())) {
    throw new Error('Credential import requires exactly two non-empty lines: base_url, then api_key.');
  }
  return { base_url: baseUrl, api_key: apiKey };
}

async function main() {
  const [command, ...args] = process.argv.slice(2);
  let result;
  switch (command) {
    case 'config': {
      const [subcommand, ...configArgs] = args;
      if (subcommand === 'path') result = { credentials_file: credentialsPath() };
      else if (subcommand === 'set') result = { credentials_file: writeCredentials(parseConfigArguments(configArgs)), configured: true };
      else if (subcommand === 'import-lines') {
        if (configArgs.length) throw new Error('Usage: printf "<base_url>\\n<api_key>\\n" | api-client.mjs config import-lines');
        result = { credentials_file: writeCredentials(parseCredentialLines(fs.readFileSync(0, 'utf8'))), configured: true };
      }
      else if (subcommand === 'status') {
        const stored = readCredentials();
        result = {
          credentials_file: credentialsPath(),
          base_url: stored.base_url ? maskBaseUrl(stored.base_url) : null,
          api_key_configured: Boolean(stored.api_key),
        };
      } else throw new Error('Commands: config path, config status, config set --base-url <url> --api-key <key>, config import-lines');
      break;
    }
    case 'discover':
      result = { models: await request('models?detail=1'), apps: await request('apps') };
      break;
    case 'upload':
      if (!args[0] || args[1] !== '--confirm-local-upload') throw new Error('Usage: api-client.mjs upload <local-file> --confirm-local-upload');
      result = await upload(args[0], loadConfiguration(), true);
      break;
    case 'request': {
      const [method, relativePath, body = ''] = args;
      if (!method || !relativePath) throw new Error('Usage: api-client.mjs request <METHOD> <path> [json-body]');
      const hasJsonBody = body !== '' && !['GET', 'HEAD'].includes(method.toUpperCase());
      result = await request(relativePath, {
        method: method.toUpperCase(),
        ...(hasJsonBody ? { headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(parseJson(body, 'json-body')) } : {}),
      });
      break;
    }
    case 'poll': {
      const [taskId, interval = '3', timeout = '600'] = args;
      if (!taskId) throw new Error('Usage: api-client.mjs poll <task-id> [interval-seconds] [max-seconds]');
      result = await poll(taskId, interval, timeout);
      break;
    }
    default:
      throw new Error('Commands: config, discover, upload, request, poll');
  }
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exit(1);
  });
}
