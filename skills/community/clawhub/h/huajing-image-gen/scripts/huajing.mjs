#!/usr/bin/env node
// huajing.mjs — Huajing (AI Image Studio) local-server client for agent skills.
// Zero-dependency (Node 18+). Subcommands: health | generate | polish | gallery.

import process from 'node:process';

const BASE_URL = (process.env.HUAJING_BASE_URL || 'http://127.0.0.1:4173').replace(/\/+$/, '');
const DATA_DIR = process.env.HUAJING_DATA_DIR || '';

const EXIT_OK = 0;
const EXIT_FAILED = 1;
const EXIT_UNREACHABLE = 2;
const EXIT_USAGE = 3;

function usage(code = EXIT_USAGE) {
  process.stderr.write(`Usage:
  huajing.mjs health
  huajing.mjs generate --prompt <text> [--size 1024x1024] [--count 1-4]
                       [--provider <id|name>] [--model <id>] [--negative <text>]
                       [--timeout 300] [--plain]
  huajing.mjs polish   --prompt <text> [--provider <id|name>]
  huajing.mjs gallery  [--limit 5] [--query <text>] [--plain]
Environment:
  HUAJING_BASE_URL   server base URL (default ${BASE_URL})
  HUAJING_DATA_DIR   huajing data/ dir; when set, results carry absolute file paths
`);
  return code;
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token.startsWith('--')) {
      const key = token.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = next;
        i += 1;
      }
    } else {
      args._.push(token);
    }
  }
  return args;
}

function fail(exitCode, message) {
  process.stderr.write(`huajing: ${message}\n`);
  process.exit(exitCode);
}

async function request(pathname, { method = 'GET', body, timeoutMs = 30_000 } = {}) {
  let response;
  try {
    response = await fetch(BASE_URL + pathname, {
      method,
      headers: body === undefined ? {} : { 'content-type': 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: AbortSignal.timeout(timeoutMs)
    });
  } catch (error) {
    fail(EXIT_UNREACHABLE, `cannot reach Huajing at ${BASE_URL} (${error.cause?.code || error.message}). ` +
      'Start it with start.bat (Windows) or `npm start` in the Huajing repo.');
  }
  const text = await response.text();
  let payload = null;
  try { payload = text ? JSON.parse(text) : null; } catch { payload = null; }
  if (!response.ok) {
    const detail = payload?.error?.message || payload?.message || text.slice(0, 300) || response.statusText;
    fail(response.status === 404 ? EXIT_USAGE : EXIT_FAILED, `HTTP ${response.status} ${pathname}: ${detail}`);
  }
  return payload;
}

function imageEntries(record) {
  return (record?.images || []).map((image) => {
    const entry = {
      url: image.url?.startsWith('http') ? image.url : BASE_URL + (image.url || `/media/generated/${image.file}`),
      mime: image.mime,
      width: image.width,
      height: image.height,
      bytes: image.size
    };
    if (DATA_DIR) entry.file = `${DATA_DIR.replace(/[\\/]+$/, '')}/generated/${image.file}`;
    return entry;
  });
}

function printResult(result, plain) {
  if (!plain) {
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
    return;
  }
  if (result.status === 'unreachable') return;
  if (result.images?.length) {
    for (const image of result.images) {
      process.stdout.write(`${image.file ? image.file + '\n' : ''}${image.url}\n`);
    }
    return;
  }
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}

async function requireHealthy() {
  const health = await request('/api/health', { timeoutMs: 5000 });
  if (!health?.ok) fail(EXIT_UNREACHABLE, `server at ${BASE_URL} answered but is not healthy`);
  return health;
}

async function resolveProvider(spec) {
  const { data } = await request('/api/providers');
  const providers = data || [];
  if (spec) {
    const byId = providers.find((p) => p.id === spec);
    const byName = providers.find((p) => p.name.toLowerCase() === spec.toLowerCase());
    const found = byId || byName;
    if (!found) fail(EXIT_USAGE, `provider "${spec}" not found; available: ${providers.map((p) => p.name).join(', ')}`);
    return found;
  }
  const usable = providers
    .filter((p) => p.enabled && p.imageModel)
    .sort((a, b) => Number(b.apiKeyConfigured || b.authConfigured || false) - Number(a.apiKeyConfigured || a.authConfigured || false));
  if (!usable.length) fail(EXIT_FAILED, 'no enabled provider with an image model; add one in the Huajing UI (Service & Models)');
  return usable[0];
}

async function pollGeneration(id, timeoutSeconds) {
  const deadline = Date.now() + timeoutSeconds * 1000;
  const delays = [1000, 2000, 3000];
  for (let attempt = 0; ; attempt += 1) {
    await new Promise((resolve) => setTimeout(resolve, delays[Math.min(attempt, delays.length - 1)]));
    const { data: record } = await request(`/api/generations/${id}`);
    if (record.status === 'completed') return record;
    if (record.status === 'failed') {
      fail(EXIT_FAILED, `generation failed: ${record.error || 'provider reported failure (see Huajing request logs)'}`);
    }
    if (Date.now() > deadline) {
      fail(EXIT_FAILED, `timed out after ${timeoutSeconds}s; the task may still finish — check the gallery later (record id: ${id})`);
    }
    process.stderr.write(`huajing: status ${record.status}, waiting...\n`);
  }
}

async function cmdHealth() {
  const health = await requireHealthy();
  printResult({
    ok: true,
    version: health.version,
    providers: health.providers,
    generations: health.generations,
    videos: health.videos,
    baseUrl: BASE_URL
  }, false);
  return EXIT_OK;
}

async function cmdGenerate(args) {
  const prompt = String(args.prompt || '').trim();
  if (!prompt) {
    process.stderr.write('huajing: --prompt is required\n');
    return usage();
  }
  await requireHealthy();
  const provider = await resolveProvider(args.provider);
  const payload = {
    prompt,
    providerId: provider.id,
    size: args.size || '1024x1024',
    count: Math.min(Math.max(Number.parseInt(args.count, 10) || 1, 1), 4)
  };
  if (args.model) payload.model = args.model;
  if (args.negative) payload.negativePrompt = args.negative;
  const queued = await request('/api/generations', { method: 'POST', body: payload });
  const ids = (queued.data || []).map((record) => record.id);
  process.stderr.write(`huajing: queued ${ids.length} task(s) on provider "${provider.name}" (${provider.imageModel})\n`);
  const records = [];
  for (const id of ids) {
    records.push(await pollGeneration(id, Number.parseInt(args.timeout, 10) || 300));
  }
  const images = records.flatMap((record) => imageEntries(record));
  printResult({
    status: 'completed',
    provider: provider.name,
    model: records[0]?.model || provider.imageModel,
    size: payload.size,
    taskIds: ids,
    images
  }, args.plain);
  return EXIT_OK;
}

async function cmdPolish(args) {
  const prompt = String(args.prompt || '').trim();
  if (!prompt) {
    process.stderr.write('huajing: --prompt is required\n');
    return usage();
  }
  await requireHealthy();
  const body = { prompt };
  if (args.provider) {
    const provider = await resolveProvider(args.provider);
    body.providerId = provider.id;
  }
  const result = await request('/api/prompts/polish', { method: 'POST', body, timeoutMs: 120_000 });
  printResult({ status: 'completed', data: result.data }, false);
  return EXIT_OK;
}

async function cmdGallery(args) {
  await requireHealthy();
  const params = new URLSearchParams();
  params.set('limit', String(Math.min(Math.max(Number.parseInt(args.limit, 10) || 5, 1), 200)));
  if (args.query) params.set('q', args.query);
  const { data } = await request(`/api/generations?${params.toString()}`);
  printResult({
    status: 'completed',
    count: (data || []).length,
    generations: (data || []).map((record) => ({
      id: record.id,
      title: record.title,
      status: record.status,
      provider: record.providerName,
      model: record.model,
      createdAt: record.createdAt,
      images: record.status === 'completed' ? imageEntries(record) : []
    }))
  }, args.plain);
  return EXIT_OK;
}

const [command, ...rest] = process.argv.slice(2);
const args = parseArgs(rest);
const commands = { health: cmdHealth, generate: cmdGenerate, polish: cmdPolish, gallery: cmdGallery };
const handler = commands[command];
if (!handler) process.exit(usage());
process.exit(await handler(args));
