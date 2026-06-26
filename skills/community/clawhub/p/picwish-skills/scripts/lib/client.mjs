import fs from 'fs';
import path from 'path';
import os from 'os';
import {
  REGION_CONFIG,
  DEFAULT_REGION,
  DEFAULT_POLL_INTERVAL_MS,
  DEFAULT_POLL_TIMEOUT_MS,
  TASK_STATE,
} from './constants.mjs';
import { buildHttpError, buildTaskStateError } from './errors.mjs';

export function resolveApiKey() {
  const envKey = process.env.PICWISH_API_KEY?.trim();
  if (envKey) return envKey;

  const openclawConfigPath = path.join(os.homedir(), '.openclaw', 'config.json');
  try {
    const config = JSON.parse(fs.readFileSync(openclawConfigPath, 'utf8'));
    const clawKey = config?.skills?.entries?.picwish?.apiKey?.trim();
    if (clawKey) return clawKey;
  } catch { /* ignore */ }

  console.error(
    `Error: Missing PicWish API Key.\n` +
    `Please set it using one of the following methods:\n` +
    `\n` +
    `  Option 1 (environment variable):\n` +
    `  export PICWISH_API_KEY="your_api_key_here"\n` +
    `\n` +
    `  Option 2 (OpenClaw config):\n` +
    `  openclaw config set skills.entries.picwish.apiKey "your_api_key_here"\n` +
    `\n` +
    `China mainland users should also set region (pick one):\n` +
    `  export PICWISH_REGION=cn\n` +
    `  openclaw config set skills.entries.picwish.region cn\n` +
    `\n` +
    `Get your API key here:\n` +
    `  Global: https://picwish.com/my-account?subRoute=api-key\n` +
    `  China:  https://picwish.cn/my-account?subRoute=api-key\n`
  );
  process.exit(1);
}

function resolveRegion() {
  const envRegion = process.env.PICWISH_REGION?.trim()?.toLowerCase();
  if (envRegion) return envRegion;

  const openclawConfigPath = path.join(os.homedir(), '.openclaw', 'config.json');
  try {
    const config = JSON.parse(fs.readFileSync(openclawConfigPath, 'utf8'));
    const clawRegion = config?.skills?.entries?.picwish?.region?.trim()?.toLowerCase();
    if (clawRegion) return clawRegion;
  } catch { /* ignore */ }

  return DEFAULT_REGION;
}

export function resolveBaseUrl() {
  const override = process.env.PICWISH_BASE_URL?.trim();
  if (override) return override.replace(/\/+$/, '');

  const region = resolveRegion();
  const cfg = REGION_CONFIG[region];
  if (!cfg) {
    console.error(
      `Error: Unsupported PICWISH_REGION="${region}".\n` +
      `Supported values: ${Object.keys(REGION_CONFIG).join(', ')} (default: ${DEFAULT_REGION})\n`
    );
    process.exit(1);
  }
  return cfg.baseUrl;
}

export async function createTask(endpoint, formFields, apiKey) {
  const baseUrl = resolveBaseUrl();
  const url = `${baseUrl}${endpoint}`;
  const form = new FormData();

  for (const [key, value] of Object.entries(formFields)) {
    if (value === undefined || value === null || value === '') continue;
    if (value && typeof value === 'object' && value.blob instanceof Blob) {
      form.append(key, value.blob, value.filename || 'file');
    } else if (value instanceof Blob) {
      form.append(key, value, 'file');
    } else {
      form.append(key, String(value));
    }
  }

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'X-API-KEY': apiKey },
    body: form,
  });

  if (res.status !== 200) {
    const text = await res.text().catch(() => '');
    const err = buildHttpError(res.status, text);
    console.log(JSON.stringify(err));
    process.exit(1);
  }

  const json = await res.json();
  if (json.status !== 200) {
    const err = buildHttpError(json.status, json.message);
    console.log(JSON.stringify(err));
    process.exit(1);
  }

  return json.data;
}

export async function pollResult(endpoint, taskId, apiKey, opts = {}) {
  const baseUrl = resolveBaseUrl();
  const interval = opts.interval || parseInt(process.env.PICWISH_POLL_INTERVAL_MS, 10) || DEFAULT_POLL_INTERVAL_MS;
  const timeout = opts.timeout || DEFAULT_POLL_TIMEOUT_MS;

  const url = `${baseUrl}${endpoint}/${taskId}`;
  const start = Date.now();

  while (Date.now() - start < timeout) {
    const res = await fetch(url, {
      method: 'GET',
      headers: { 'X-API-KEY': apiKey },
    });

    if (res.status !== 200) {
      const text = await res.text().catch(() => '');
      const err = buildHttpError(res.status, text);
      console.log(JSON.stringify(err));
      process.exit(1);
    }

    const json = await res.json();
    const data = json.data;

    if (data.state === TASK_STATE.COMPLETED) {
      return data;
    }

    if (data.state < 0) {
      const err = buildTaskStateError(data.state);
      console.log(JSON.stringify(err));
      process.exit(1);
    }

    await new Promise(r => setTimeout(r, interval));
  }

  const err = buildTaskStateError(TASK_STATE.TIMEOUT);
  err.user_hint = `Poll timed out (>${timeout / 1000}s). Please try a smaller or simpler image.`;
  console.log(JSON.stringify(err));
  process.exit(1);
}

export async function downloadFile(url, destPath) {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Download failed: HTTP ${res.status}`);
  }
  const buffer = Buffer.from(await res.arrayBuffer());
  fs.mkdirSync(path.dirname(destPath), { recursive: true });
  fs.writeFileSync(destPath, buffer);
  return destPath;
}
