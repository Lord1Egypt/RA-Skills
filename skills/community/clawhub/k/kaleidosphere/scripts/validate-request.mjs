#!/usr/bin/env node
import {readFile} from 'node:fs/promises';

const denyKey = /(?:sql|query|token|secret|password|credential|url|uri|rows?|payload|apply|write|delete|deploy)/i;
const actions = new Set(['status', 'discovery', 'analyze', 'plan', 'preview', 'readback']);
const discoveryCommands = new Set(['start', 'resume', 'status', 'answer', 'revise', 'confirm', 'export']);

function fail(reason) {
  process.stdout.write(JSON.stringify({valid: false, reason}) + '\n');
  process.exitCode = 2;
}

function keysAre(value, allowed) {
  return value && typeof value === 'object' && !Array.isArray(value)
    && Object.keys(value).every((key) => allowed.has(key));
}

let request;
try {
  const raw = process.argv[2]
    ? await readFile(process.argv[2], 'utf8')
    : await new Promise((resolve) => {
        let data = '';
        process.stdin.setEncoding('utf8');
        process.stdin.on('data', (chunk) => { data += chunk; });
        process.stdin.on('end', () => resolve(data));
      });
  request = JSON.parse(raw);
} catch {
  fail('MALFORMED_JSON');
}

if (!process.exitCode) {
  if (!keysAre(request, new Set(['schemaVersion', 'requestId', 'action', 'input']))) fail('REQUEST_NOT_CLOSED');
  else if (request.schemaVersion !== 'superset-bi-agent.external/intent-request/v2') fail('STALE_OR_UNKNOWN_CONTRACT');
  else if (typeof request.requestId !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/.test(request.requestId)) fail('INVALID_REQUEST_ID');
  else if (!actions.has(request.action)) fail('ACTION_NOT_ALLOWED');
  else {
    const input = request.input ?? {};
    const deepKeys = JSON.stringify(input);
    if (denyKey.test(deepKeys)) fail('UNSAFE_FIELD');
    else if (['status', 'analyze', 'readback'].includes(request.action) && !keysAre(input, new Set())) fail('INPUT_NOT_EMPTY');
    else if (request.action === 'discovery') {
      if (!keysAre(input, new Set(['command', 'sessionId', 'field', 'value']))) fail('DISCOVERY_INPUT_NOT_CLOSED');
      else if (!discoveryCommands.has(input.command)) fail('DISCOVERY_COMMAND_NOT_ALLOWED');
      else if (typeof input.sessionId !== 'string' || !/^[a-z0-9][a-z0-9_-]{2,63}$/.test(input.sessionId)) fail('INVALID_SESSION_ID');
      else process.stdout.write(JSON.stringify({valid: true, action: request.action, authority: 'authority-free'}) + '\n');
    } else if (['plan', 'preview'].includes(request.action)) {
      if (!keysAre(input, new Set(['objective', 'receiptId']))) fail('PROPOSAL_INPUT_NOT_CLOSED');
      else if (typeof input.objective !== 'string' || input.objective.length < 3 || input.objective.length > 500) fail('INVALID_OBJECTIVE');
      else process.stdout.write(JSON.stringify({valid: true, action: request.action, authority: 'proposal-only'}) + '\n');
    } else {
      process.stdout.write(JSON.stringify({valid: true, action: request.action, authority: 'read-only'}) + '\n');
    }
  }
}
