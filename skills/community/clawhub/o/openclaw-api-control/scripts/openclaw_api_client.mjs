#!/usr/bin/env node

import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const DEFAULT_BASE_URL = 'https://openclaw-as-a-service.com/api';
const MAX_UPLOAD_BYTES = 5 * 1024 * 1024;

function normalizeBaseUrl(rawValue) {
  const trimmed = String(rawValue || '').trim();
  if (!trimmed) {
    return DEFAULT_BASE_URL;
  }

  const withoutTrailing = trimmed.replace(/\/+$/, '');
  return withoutTrailing.endsWith('/api') ? withoutTrailing : `${withoutTrailing}/api`;
}

const API_BASE_URL = normalizeBaseUrl(process.env.OPENCLAW_API_BASE_URL);
const API_KEY = String(process.env.OPENCLAW_API_KEY || '').trim();
const DEFAULT_INSTANCE_ID = String(process.env.OPENCLAW_INSTANCE_ID || '').trim();

function usage() {
  console.error(`Usage:
  openclaw_api_client.mjs root
  openclaw_api_client.mjs instances list
  openclaw_api_client.mjs instances create [--invite-code CODE]
  openclaw_api_client.mjs chat sessions [--instance ID]
  openclaw_api_client.mjs chat send [--instance ID] [--session ID] --message TEXT [--stream]
  openclaw_api_client.mjs chat tail [--instance ID] [--session ID] [--limit N]
  openclaw_api_client.mjs files read [--instance ID] --path PATH
  openclaw_api_client.mjs files write [--instance ID] --path PATH --content TEXT
  openclaw_api_client.mjs files mkdir [--instance ID] --path PATH
  openclaw_api_client.mjs files upload-tree [--instance ID] --src DIR [--dest /workspace/target]
  openclaw_api_client.mjs terminal exec [--instance ID] --command CMD [--timeout-ms N]
`);
}

function parseArgs(argv) {
  const positional = [];
  const flags = {};

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith('--')) {
      positional.push(token);
      continue;
    }

    const key = token.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith('--')) {
      flags[key] = true;
      continue;
    }

    flags[key] = next;
    index += 1;
  }

  return { positional, flags };
}

function ensureApiKey() {
  if (!API_KEY) {
    throw new Error('OPENCLAW_API_KEY is required.');
  }
}

async function apiRequest(method, pathname, { query = null, body = undefined, expect = 'json' } = {}) {
  ensureApiKey();

  const url = new URL(pathname.replace(/^\//, ''), `${API_BASE_URL.replace(/\/+$/, '')}/`);
  if (query && typeof query === 'object') {
    for (const [key, value] of Object.entries(query)) {
      if (value === undefined || value === null || value === '') {
        continue;
      }
      url.searchParams.set(key, String(value));
    }
  }

  const response = await fetch(url, {
    method,
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      ...(body !== undefined ? { 'Content-Type': 'application/json' } : {})
    },
    body: body !== undefined ? JSON.stringify(body) : undefined
  });

  if (expect === 'stream') {
    if (!response.ok) {
      const text = await response.text().catch(() => '');
      throw new Error(`HTTP ${response.status}: ${text || response.statusText}`);
    }
    return response;
  }

  const text = await response.text();
  let payload = null;
  try {
    payload = text ? JSON.parse(text) : null;
  } catch (_error) {
    payload = text;
  }

  if (!response.ok) {
    const message = typeof payload === 'object' && payload && payload.message
      ? payload.message
      : typeof payload === 'string' && payload
        ? payload
        : response.statusText;
    throw new Error(`HTTP ${response.status}: ${message}`);
  }

  return payload;
}

async function resolveInstanceId(explicitInstanceId) {
  const candidate = String(explicitInstanceId || '').trim() || DEFAULT_INSTANCE_ID;
  if (candidate) {
    return candidate;
  }

  const instances = await apiRequest('GET', '/instances');
  if (!Array.isArray(instances) || instances.length === 0) {
    throw new Error('No OpenClaw instances found. Create one first.');
  }

  const ready = instances.find((instance) => instance && instance.status === 'ready');
  return ready?.id || instances[0]?.id || null;
}

async function resolveChatSessionId(instanceId, explicitSessionId) {
  const candidate = String(explicitSessionId || '').trim();
  if (candidate) {
    return candidate;
  }

  const sessions = await apiRequest('GET', `/instances/${encodeURIComponent(instanceId)}/chat/sessions`);
  if (Array.isArray(sessions) && sessions.length > 0) {
    return sessions[0].id;
  }

  const created = await apiRequest('POST', `/instances/${encodeURIComponent(instanceId)}/chat/sessions`, {
    body: { title: 'API client session' }
  });
  return created?.id || null;
}

function isLikelyTextFile(buffer) {
  if (!Buffer.isBuffer(buffer)) {
    return false;
  }

  if (buffer.length === 0) {
    return true;
  }

  const sample = buffer.subarray(0, Math.min(buffer.length, 4096));
  for (const byte of sample) {
    if (byte === 0) {
      return false;
    }
  }

  const decoded = sample.toString('utf8');
  const replacementCount = decoded.split('\uFFFD').length - 1;
  return replacementCount <= Math.max(2, Math.floor(decoded.length * 0.02));
}

async function walkDirectory(rootDir) {
  const directories = [];
  const files = [];

  async function visit(currentDir) {
    directories.push(currentDir);
    const entries = await fs.readdir(currentDir, { withFileTypes: true });
    entries.sort((left, right) => left.name.localeCompare(right.name));

    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        await visit(fullPath);
        continue;
      }
      if (entry.isFile()) {
        files.push(fullPath);
      }
    }
  }

  await visit(rootDir);
  return { directories, files };
}

async function uploadTree(instanceId, sourceDir, destinationDir) {
  const sourceStat = await fs.stat(sourceDir);
  if (!sourceStat.isDirectory()) {
    throw new Error(`Source is not a directory: ${sourceDir}`);
  }

  const absoluteSource = path.resolve(sourceDir);
  const remoteRoot = String(destinationDir || '/workspace').trim() || '/workspace';
  const { directories, files } = await walkDirectory(absoluteSource);
  const uploaded = [];
  const skipped = [];

  for (const directory of directories) {
    const relativeDir = path.relative(absoluteSource, directory);
    const remoteDir = relativeDir
      ? path.posix.join(remoteRoot, relativeDir.split(path.sep).join('/'))
      : remoteRoot;

    if (remoteDir !== '/workspace') {
      await apiRequest('POST', `/instances/${encodeURIComponent(instanceId)}/files/mkdir`, {
        body: { path: remoteDir }
      });
    }
  }

  for (const filePath of files) {
    const relativeFile = path.relative(absoluteSource, filePath);
    const buffer = await fs.readFile(filePath);
    if (buffer.length > MAX_UPLOAD_BYTES) {
      skipped.push({ path: filePath, reason: 'too_large' });
      continue;
    }
    if (!isLikelyTextFile(buffer)) {
      skipped.push({ path: filePath, reason: 'binary_or_unsupported' });
      continue;
    }

    const remoteDir = path.posix.join(
      remoteRoot,
      path.dirname(relativeFile).split(path.sep).join('/')
    ).replace(/\/\.$/, '');
    const fileName = path.basename(relativeFile);

    await apiRequest('POST', `/instances/${encodeURIComponent(instanceId)}/files/upload`, {
      body: {
        targetDir: remoteDir === '/workspace/.' ? '/workspace' : remoteDir,
        fileName,
        content: buffer.toString('utf8')
      }
    });
    uploaded.push({
      local_path: filePath,
      remote_path: path.posix.join(remoteDir === '/workspace/.' ? '/workspace' : remoteDir, fileName)
    });
  }

  return {
    instance_id: instanceId,
    source: absoluteSource,
    destination: remoteRoot,
    uploaded_count: uploaded.length,
    skipped_count: skipped.length,
    uploaded,
    skipped
  };
}

async function streamChat(instanceId, payload) {
  const response = await apiRequest('POST', `/instances/${encodeURIComponent(instanceId)}/chat/stream`, {
    body: payload,
    expect: 'stream'
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      break;
    }
    process.stdout.write(decoder.decode(value, { stream: true }));
  }
}

async function main() {
  const { positional, flags } = parseArgs(process.argv.slice(2));
  const [group, command] = positional;

  if (!group) {
    usage();
    process.exit(1);
  }

  if (group === 'root') {
    const root = await apiRequest('GET', '');
    console.log(JSON.stringify(root, null, 2));
    return;
  }

  if (group === 'instances' && command === 'list') {
    const instances = await apiRequest('GET', '/instances');
    console.log(JSON.stringify(instances, null, 2));
    return;
  }

  if (group === 'instances' && command === 'create') {
    const created = await apiRequest('POST', '/instances', {
      body: flags['invite-code'] ? { invite_code: String(flags['invite-code']) } : {}
    });
    console.log(JSON.stringify(created, null, 2));
    return;
  }

  if (group === 'chat' && command === 'sessions') {
    const instanceId = await resolveInstanceId(flags.instance);
    const sessions = await apiRequest('GET', `/instances/${encodeURIComponent(instanceId)}/chat/sessions`);
    console.log(JSON.stringify({ instance_id: instanceId, sessions }, null, 2));
    return;
  }

  if (group === 'chat' && command === 'send') {
    const message = String(flags.message || '').trim();
    if (!message) {
      throw new Error('--message is required.');
    }

    const instanceId = await resolveInstanceId(flags.instance);
    const payload = {
      message
    };
    const sessionId = String(flags.session || '').trim();
    if (sessionId) {
      payload.session_id = sessionId;
    }

    if (flags.stream) {
      await streamChat(instanceId, payload);
      return;
    }

    const response = await apiRequest('POST', `/instances/${encodeURIComponent(instanceId)}/chat`, {
      body: payload
    });
    console.log(JSON.stringify(response, null, 2));
    return;
  }

  if (group === 'chat' && command === 'tail') {
    const instanceId = await resolveInstanceId(flags.instance);
    const sessionId = await resolveChatSessionId(instanceId, flags.session);
    const payload = await apiRequest('GET', `/instances/${encodeURIComponent(instanceId)}/chat/messages`, {
      query: {
        session_id: sessionId,
        tail: true,
        limit: flags.limit || 20
      }
    });
    console.log(JSON.stringify({ instance_id: instanceId, session_id: sessionId, messages: payload }, null, 2));
    return;
  }

  if (group === 'files' && command === 'read') {
    const targetPath = String(flags.path || '').trim();
    if (!targetPath) {
      throw new Error('--path is required.');
    }
    const instanceId = await resolveInstanceId(flags.instance);
    const payload = await apiRequest('GET', `/instances/${encodeURIComponent(instanceId)}/files/read`, {
      query: { path: targetPath }
    });
    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  if (group === 'files' && command === 'write') {
    const targetPath = String(flags.path || '').trim();
    if (!targetPath) {
      throw new Error('--path is required.');
    }
    if (typeof flags.content !== 'string') {
      throw new Error('--content is required.');
    }
    const instanceId = await resolveInstanceId(flags.instance);
    const payload = await apiRequest('POST', `/instances/${encodeURIComponent(instanceId)}/files/write`, {
      body: {
        path: targetPath,
        content: String(flags.content)
      }
    });
    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  if (group === 'files' && command === 'mkdir') {
    const targetPath = String(flags.path || '').trim();
    if (!targetPath) {
      throw new Error('--path is required.');
    }
    const instanceId = await resolveInstanceId(flags.instance);
    const payload = await apiRequest('POST', `/instances/${encodeURIComponent(instanceId)}/files/mkdir`, {
      body: { path: targetPath }
    });
    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  if (group === 'files' && command === 'upload-tree') {
    const sourceDir = String(flags.src || '').trim();
    if (!sourceDir) {
      throw new Error('--src is required.');
    }
    const instanceId = await resolveInstanceId(flags.instance);
    const report = await uploadTree(
      instanceId,
      sourceDir,
      String(flags.dest || '/workspace')
    );
    console.log(JSON.stringify(report, null, 2));
    return;
  }

  if (group === 'terminal' && command === 'exec') {
    const rawCommand = String(flags.command || '').trim();
    if (!rawCommand) {
      throw new Error('--command is required.');
    }
    const instanceId = await resolveInstanceId(flags.instance);
    const timeoutMs = Number.parseInt(flags['timeout-ms'], 10);
    const payload = await apiRequest('POST', `/instances/${encodeURIComponent(instanceId)}/terminal/exec`, {
      body: {
        command: rawCommand,
        ...(Number.isFinite(timeoutMs) ? { timeout_ms: timeoutMs } : {})
      }
    });
    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  usage();
  process.exit(1);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
