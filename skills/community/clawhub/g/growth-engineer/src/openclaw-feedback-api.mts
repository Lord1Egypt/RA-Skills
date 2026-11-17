#!/usr/bin/env node

import { createServer } from 'node:http';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const DEFAULT_PORT = 4310;
const DEFAULT_HOST = '127.0.0.1';
const DEFAULT_DIR = 'data/openclaw-growth-engineer/feedback-api';
const FEEDBACK_HEADERS = ['x-feedback-token', 'x-feedback-key'];

function parseArgs(argv) {
  const args = {
    port: DEFAULT_PORT,
    host: DEFAULT_HOST,
    dir: DEFAULT_DIR,
    allowUnauthenticated: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    const next = argv[i + 1];
    if (token === '--') {
      continue;
    } else if (token === '--port') {
      args.port = Number.parseInt(next, 10) || DEFAULT_PORT;
      i += 1;
    } else if (token === '--host') {
      args.host = next || DEFAULT_HOST;
      i += 1;
    } else if (token === '--dir') {
      args.dir = next;
      i += 1;
    } else if (token === '--allow-unauthenticated') {
      args.allowUnauthenticated = true;
    } else if (token === '--help' || token === '-h') {
      printHelpAndExit(0);
    } else {
      printHelpAndExit(1, `Unknown argument: ${token}`);
    }
  }
  return args;
}

function printHelpAndExit(exitCode, reason = null) {
  if (reason) {
    process.stderr.write(`${reason}\n\n`);
  }
  process.stdout.write(`
OpenClaw Feedback API (MVP)

Usage:
  node scripts/openclaw-feedback-api.mjs [--host 127.0.0.1] [--port 4310] [--dir data/openclaw-growth-engineer/feedback-api]

Auth:
  Required env FEEDBACK_API_TOKEN.
  Clients must send header: x-feedback-token: <token>
  The API also accepts: x-feedback-key: <token>
  Local-only development can opt out with: --allow-unauthenticated
`);
  process.exit(exitCode);
}

async function ensureDir(dirPath) {
  await fs.mkdir(dirPath, { recursive: true });
}

function sendJson(res, statusCode, payload) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'Access-Control-Allow-Origin': '*',
  });
  res.end(JSON.stringify(payload));
}

async function readBody(req): Promise<string> {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', (chunk) => {
      raw += String(chunk);
      if (raw.length > 1_000_000) {
        reject(new Error('Payload too large'));
      }
    });
    req.on('end', () => resolve(raw));
    req.on('error', reject);
  });
}

function normalizeItem(input) {
  const now = new Date().toISOString();
  const metadata =
    input && typeof input.metadata === 'object' && !Array.isArray(input.metadata) ? input.metadata : {};
  const rawFeedback = String(input.feedback || input.message || input.comment || input.summary || '').trim();
  const locationId = String(input.locationId || input.location || metadata.locationId || '').trim();
  const surface = String(input.appSurface || input.surface || metadata.surface || '').trim();
  const originName = String(input.originName || metadata.originName || '').trim();
  const title =
    String(
      input.title ||
        input.summary ||
        metadata.title ||
        (rawFeedback ? rawFeedback.split(/[.!?]/)[0] : '') ||
        'User feedback',
    ).trim() || 'User feedback';
  return {
    id: String(input.id || `fb_${Date.now()}`),
    title,
    comment: rawFeedback,
    area: String(input.area || metadata.area || 'general').toLowerCase(),
    channel: String(input.channel || surface || 'unknown'),
    surface: surface || null,
    location_id: locationId || null,
    origin_name: originName || null,
    priority: String(input.priority || metadata.priority || 'medium').toLowerCase(),
    tags: Array.isArray(input.tags) ? input.tags.map(String) : [],
    metadata,
    app_id: input.appId ? String(input.appId) : null,
    user_id: input.userId ? String(input.userId) : null,
    created_at: String(input.created_at || now),
  };
}

async function appendEvent(filePath, item) {
  await fs.appendFile(filePath, `${JSON.stringify(item)}\n`, 'utf8');
}

async function readEvents(filePath) {
  try {
    const raw = await fs.readFile(filePath, 'utf8');
    return raw
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => JSON.parse(line));
  } catch {
    return [];
  }
}

function buildSummary(events) {
  const grouped = new Map();
  for (const event of events) {
    const key = `${event.area}:${event.origin_name || 'unknown'}:${event.title.toLowerCase()}`;
    const current = grouped.get(key) || {
      id: key.replace(/[^a-z0-9:_-]/gi, '_'),
      title: event.title,
      area: event.area,
      origin_name: event.origin_name || null,
      priority: event.priority || 'medium',
      count: 0,
      channel: event.channel || 'mixed',
      surface: event.surface || null,
      comment: event.comment || '',
      keywords: [],
      locations: new Map(),
    };
    current.count += 1;
    current.comment = event.comment || current.comment;
    const tags = Array.isArray(event.tags) ? event.tags : [];
    current.keywords = [...new Set([...current.keywords, ...tags])];
    if (event.location_id) {
      current.locations.set(
        event.location_id,
        (current.locations.get(event.location_id) || 0) + 1,
      );
    }
    if (event.priority === 'high') {
      current.priority = 'high';
    }
    grouped.set(key, current);
  }
  const items = [...grouped.values()]
    .map((item) => ({
      ...item,
      locations: [...item.locations.entries()]
        .map(([location_id, count]) => ({ location_id, count }))
        .sort((a, b) => b.count - a.count || a.location_id.localeCompare(b.location_id)),
    }))
    .sort((a, b) => b.count - a.count || a.title.localeCompare(b.title));
  return {
    window: 'rolling',
    generated_at: new Date().toISOString(),
    items,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const storageDir = path.resolve(args.dir);
  const eventsFile = path.join(storageDir, 'events.ndjson');
  const summaryFile = path.join(storageDir, 'feedback_summary.json');
  const requiredToken = process.env.FEEDBACK_API_TOKEN || null;
  if (!requiredToken && !args.allowUnauthenticated) {
    throw new Error(
      'FEEDBACK_API_TOKEN is required. For local-only development, rerun with --allow-unauthenticated.',
    );
  }

  await ensureDir(storageDir);

  const server = createServer(async (req, res) => {
    try {
      if (req.method === 'OPTIONS') {
        res.writeHead(204, {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': `content-type,${FEEDBACK_HEADERS.join(',')}`,
          'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
        });
        res.end();
        return;
      }

      if (requiredToken) {
        const token = FEEDBACK_HEADERS.map((header) => req.headers[header]).find(Boolean);
        if (token !== requiredToken) {
          sendJson(res, 401, { ok: false, error: 'unauthorized' });
          return;
        }
      }

      if (req.method === 'GET' && req.url === '/health') {
        sendJson(res, 200, { ok: true, status: 'healthy' });
        return;
      }

      if (req.method === 'POST' && req.url === '/feedback') {
        const rawBody = await readBody(req);
        const payload = rawBody ? JSON.parse(rawBody) : {};
        const item = normalizeItem(payload);
        await appendEvent(eventsFile, item);

        const events = await readEvents(eventsFile);
        const summary = buildSummary(events);
        await fs.writeFile(summaryFile, JSON.stringify(summary, null, 2), 'utf8');

        sendJson(res, 200, { ok: true, item });
        return;
      }

      if (req.method === 'GET' && req.url === '/summary') {
        const summary = await fs
          .readFile(summaryFile, 'utf8')
          .then((raw) => JSON.parse(raw))
          .catch(async () => {
            const events = await readEvents(eventsFile);
            return buildSummary(events);
          });
        sendJson(res, 200, summary);
        return;
      }

      sendJson(res, 404, { ok: false, error: 'not_found' });
    } catch (error) {
      sendJson(res, 500, {
        ok: false,
        error: error instanceof Error ? error.message : String(error),
      });
    }
  });

  server.listen(args.port, args.host, () => {
    process.stdout.write(`Feedback API listening on http://${args.host}:${args.port}\n`);
    process.stdout.write(`Data dir: ${storageDir}\n`);
    if (requiredToken) {
      process.stdout.write('Auth: enabled (x-feedback-token or x-feedback-key required)\n');
    } else {
      process.stdout.write('Auth: disabled by explicit --allow-unauthenticated\n');
    }
  });
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
});
