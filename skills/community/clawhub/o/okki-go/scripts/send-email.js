#!/usr/bin/env node
'use strict';

const {
  parseJson,
  postJson,
  readJsonFile,
  writeJsonFile
} = require('./lib/okki-api');
const {
  defaultRawPath,
  nowIso,
  outputBudgetMetadata,
  applyDebugMetadata
} = require('./lib/compact-output');

function usage() {
  console.error([
    'Usage:',
    '  node scripts/send-email.js batch --json \'<payload>\' --compact [--mapping-file PATH] [--debug-metadata]',
    '  node scripts/send-email.js personalized --file payload.json --compact [--debug-metadata]'
  ].join('\n'));
}

function parseArgs(argv) {
  if (argv.length === 0 || argv[0] === '--help' || argv[0] === '-h') {
    usage();
    process.exit(0);
  }
  const args = { mode: argv[0], json: null, file: null, compact: false, mappingFile: null, debugMetadata: false };
  for (let i = 1; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--json') {
      args.json = argv[++i];
    } else if (arg === '--file') {
      args.file = argv[++i];
    } else if (arg === '--compact') {
      args.compact = true;
    } else if (arg === '--mapping-file') {
      args.mappingFile = argv[++i];
    } else if (arg === '--debug-metadata') {
      args.debugMetadata = true;
    } else if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if (!['batch', 'personalized'].includes(args.mode)) {
    throw new Error('Mode must be batch or personalized.');
  }
  if ((args.json ? 1 : 0) + (args.file ? 1 : 0) !== 1) {
    throw new Error('Provide exactly one of --json or --file.');
  }
  return args;
}

function readPayload(args) {
  return args.file ? readJsonFile(args.file) : parseJson(args.json, '--json');
}

function validatePayload(payload, mode) {
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    throw new Error('Payload must be a JSON object.');
  }
  const listKey = mode === 'batch' ? 'recipients' : 'emails';
  if (!Array.isArray(payload[listKey]) || payload[listKey].length === 0) {
    throw new Error(`Payload for ${mode} mode must include ${listKey}[].`);
  }
  if (payload[listKey].length > 100) {
    throw new Error(`Payload ${listKey}[] must not exceed 100.`);
  }
}

function taskIds(response) {
  if (!response || typeof response !== 'object') return [];
  if (response.task_id) return [response.task_id];
  if (Array.isArray(response.task_ids)) return response.task_ids;
  if (Array.isArray(response.tasks)) {
    return Array.from(new Set(response.tasks.map((task) => task.task_id || task.taskId).filter(Boolean)));
  }
  return [];
}

function totalSubmitted(response, payload) {
  if (response && Number.isFinite(Number(response.total))) return Number(response.total);
  if (Array.isArray(payload.recipients)) return payload.recipients.length;
  if (Array.isArray(payload.emails)) return payload.emails.length;
  return 0;
}

function acceptedCount(response, payload) {
  if (response && Number.isFinite(Number(response.accepted_count))) return Number(response.accepted_count);
  if (response && Number.isFinite(Number(response.acceptedCount))) return Number(response.acceptedCount);
  if (response && Number.isFinite(Number(response.accepted))) return Number(response.accepted);
  return totalSubmitted(response, payload) - rejectedCount(response);
}

function rejectedCount(response) {
  if (response && Number.isFinite(Number(response.rejected_count))) return Number(response.rejected_count);
  if (response && Number.isFinite(Number(response.rejectedCount))) return Number(response.rejectedCount);
  if (response && Number.isFinite(Number(response.rejected))) return Number(response.rejected);
  if (response && Array.isArray(response.rejected_recipients)) return response.rejected_recipients.length;
  if (response && Array.isArray(response.rejectedRecipients)) return response.rejectedRecipients.length;
  return 0;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const payload = readPayload(args);
  validatePayload(payload, args.mode);
  const endpoint = args.mode === 'batch'
    ? '/api/v1/emails/send/batch'
    : '/api/v1/emails/send/personalized';
  const response = await postJson(endpoint, payload);
  const mappingPath = args.mappingFile || defaultRawPath(`email-send-${args.mode}`);
  writeJsonFile(mappingPath, {
    version: '1.0',
    created_at: nowIso(),
    mode: args.mode,
    request: payload,
    response
  });
  const output = {
    submitted: true,
    mode: args.mode,
    status: response && response.status ? response.status : 'submitted',
    total: totalSubmitted(response, payload),
    accepted_count: acceptedCount(response, payload),
    rejected_count: rejectedCount(response),
    task_ids: taskIds(response),
    next_status_command: 'node scripts/email-status.js tasks --json \'{"page":1,"page_size":20}\' --compact',
    mapping_saved: mappingPath
  };
  Object.assign(output, outputBudgetMetadata({
    defaultCap: 20,
    hardCap: 100,
    returned: output.task_ids.length,
    available: output.total
  }));

  if (args.compact) {
    process.stdout.write(`${JSON.stringify(sendEmailNormalOutput(output, args.debugMetadata), null, 2)}\n`);
    return;
  }
  process.stdout.write(`${JSON.stringify(response, null, 2)}\n`);
}

function sendEmailNormalOutput(output, debugMetadata) {
  return applyDebugMetadata(output, [
    'mapping_saved',
    'output_budget'
  ], debugMetadata);
}

main().catch((error) => {
  console.error(error.message);
  usage();
  process.exit(2);
});
