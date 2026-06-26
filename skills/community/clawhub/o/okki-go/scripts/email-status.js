#!/usr/bin/env node
'use strict';

const {
  getJson,
  parseJson,
  readJsonFile,
  writeJsonFile
} = require('./lib/okki-api');
const {
  budgetedItems,
  defaultRawPath,
  outputBudgetMetadata,
  applyDebugMetadata,
  responseList,
  responseTotal,
  truncateText
} = require('./lib/compact-output');

const DEFAULT_PAGE_SIZE = 20;
const HARD_CAP = 100;

function usage() {
  console.error([
    'Usage:',
    '  node scripts/email-status.js tasks --json \'{"page":1,"page_size":20}\' --compact [--debug-metadata]',
    '  node scripts/email-status.js task --task-id 1001 --compact [--save-raw PATH] [--debug-metadata]',
    '  node scripts/email-status.js mails --json \'{"statuses":"failed"}\' --compact [--debug-metadata]',
    '  node scripts/email-status.js mail --mail-id 2001 --compact [--include-body] [--debug-metadata]'
  ].join('\n'));
}

function parseArgs(argv) {
  if (argv.length === 0 || argv[0] === '--help' || argv[0] === '-h') {
    usage();
    process.exit(0);
  }
  const args = {
    command: argv[0],
    json: null,
    file: null,
    compact: false,
    taskId: null,
    mailId: null,
    saveRaw: null,
    includeBody: false,
    debugMetadata: false
  };
  for (let i = 1; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--json') {
      args.json = argv[++i];
    } else if (arg === '--file') {
      args.file = argv[++i];
    } else if (arg === '--task-id') {
      args.taskId = positiveInt(argv[++i], '--task-id');
    } else if (arg === '--mail-id') {
      args.mailId = positiveInt(argv[++i], '--mail-id');
    } else if (arg === '--compact') {
      args.compact = true;
    } else if (arg === '--save-raw') {
      args.saveRaw = argv[++i];
    } else if (arg === '--include-body') {
      args.includeBody = true;
    } else if (arg === '--debug-metadata') {
      args.debugMetadata = true;
    } else if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if (!['tasks', 'task', 'mails', 'mail'].includes(args.command)) {
    throw new Error('Command must be one of tasks, task, mails, or mail.');
  }
  return args;
}

function positiveInt(value, label) {
  const number = Number(value);
  if (!Number.isInteger(number) || number < 1) throw new Error(`${label} must be a positive integer.`);
  return number;
}

function readQuery(args) {
  const query = args.file ? readJsonFile(args.file) : args.json ? parseJson(args.json, '--json') : {};
  if (!query || typeof query !== 'object' || Array.isArray(query)) {
    throw new Error('Query must be a JSON object.');
  }
  const page = positiveInt(query.page || 1, 'page');
  const pageSize = Math.min(positiveInt(query.page_size || query.pageSize || DEFAULT_PAGE_SIZE, 'page_size'), 100);
  return { ...query, page, page_size: pageSize };
}

function queryString(query) {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(query)) {
    if (value !== null && value !== undefined && value !== '') params.set(key, String(value));
  }
  return params.toString();
}

function compactTaskRow(row) {
  return {
    task_id: row.taskId ?? row.task_id,
    status: row.status || null,
    total: row.totalCount ?? row.total ?? null,
    sent: row.sentCount ?? row.sent ?? null,
    failed: row.failedCount ?? row.failed ?? null,
    created_at: row.createdAt ?? row.created_at ?? null,
    completed_at: row.completedAt ?? row.completed_at ?? null
  };
}

function compactMailRow(row) {
  return {
    mail_id: row.mailId ?? row.mail_id,
    task_id: row.taskId ?? row.task_id,
    recipient_email: row.recipientEmail ?? row.recipient_email,
    subject: row.subject || null,
    status: row.status || null,
    sent_at: row.sentAt ?? row.sent_at ?? null,
    callback_received_at: row.callbackReceivedAt ?? row.callback_received_at ?? null,
    failure_reason: row.failureReason ?? row.failure_reason ?? null
  };
}

function compactTaskDetail(body) {
  const mails = Array.isArray(body.mails) ? body.mails : [];
  const failed = [];
  const successful = [];
  for (const mail of mails) {
    if (String(mail.status || '').toLowerCase() === 'failed' || mail.failureReason || mail.failure_reason) {
      failed.push(mail);
    } else {
      successful.push(mail);
    }
  }
  const visibleSuccessful = budgetedItems(successful, {
    defaultCap: DEFAULT_PAGE_SIZE,
    hardCap: HARD_CAP,
    available: successful.length
  });
  return {
    task_id: body.taskId ?? body.task_id,
    status: body.status || null,
    total: body.totalCount ?? body.total ?? mails.length,
    sent: body.sentCount ?? body.sent ?? null,
    failed: body.failedCount ?? body.failed ?? failed.length,
    created_at: body.createdAt ?? body.created_at ?? null,
    completed_at: body.completedAt ?? body.completed_at ?? null,
    failed_mails: failed.slice(0, 20).map(compactMailRow),
    successful_mails: visibleSuccessful.items.map(compactMailRow),
    content_omitted: Boolean(body.content),
    ...outputBudgetMetadata({
      defaultCap: DEFAULT_PAGE_SIZE,
      hardCap: HARD_CAP,
      returned: failed.slice(0, 20).length + visibleSuccessful.items.length,
      available: mails.length
    })
  };
}

function compactMailDetail(body, includeBody) {
  const output = compactMailRow(body);
  output.recipient_nickname = body.recipientNickname ?? body.recipient_nickname ?? null;
  output.content_omitted = Boolean(body.content) && !includeBody;
  if (includeBody && body.content) {
    output.content_preview = truncateText(body.content, 500);
    output.email_body_explicitly_requested = true;
  }
  Object.assign(output, outputBudgetMetadata({
    defaultCap: DEFAULT_PAGE_SIZE,
    hardCap: HARD_CAP,
    returned: 1,
    available: 1
  }));
  return output;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  let body;
  let output;
  if (args.command === 'tasks') {
    const query = readQuery(args);
    body = await getJson(`/api/v1/emails/tasks?${queryString(query)}`);
    const allRows = responseList(body);
    const total = responseTotal(body, allRows.length);
    const budgeted = budgetedItems(allRows, {
      defaultCap: DEFAULT_PAGE_SIZE,
      hardCap: HARD_CAP,
      requestedLimit: query.page_size,
      available: total
    });
    const rows = budgeted.items;
    output = {
      total,
      page: body.page || query.page,
      page_size: body.page_size || query.page_size,
      tasks: rows.map(compactTaskRow),
      ...budgeted.metadata
    };
  } else if (args.command === 'task') {
    if (!args.taskId) throw new Error('Missing --task-id');
    body = await getJson(`/api/v1/emails/tasks/${args.taskId}`);
    output = compactTaskDetail(body);
  } else if (args.command === 'mails') {
    const query = readQuery(args);
    body = await getJson(`/api/v1/emails/mails?${queryString(query)}`);
    const allRows = responseList(body);
    const total = responseTotal(body, allRows.length);
    const budgeted = budgetedItems(allRows, {
      defaultCap: DEFAULT_PAGE_SIZE,
      hardCap: HARD_CAP,
      requestedLimit: query.page_size,
      available: total
    });
    const rows = budgeted.items;
    output = {
      total,
      page: body.page || query.page,
      page_size: body.page_size || query.page_size,
      mails: rows.map(compactMailRow),
      ...budgeted.metadata
    };
  } else {
    if (!args.mailId) throw new Error('Missing --mail-id');
    body = await getJson(`/api/v1/emails/mails/${args.mailId}`);
    output = compactMailDetail(body, args.includeBody);
  }

  const rawPath = args.saveRaw || null;
  if (rawPath) {
    writeJsonFile(rawPath, body);
    output.raw_saved = true;
    output.raw_path = rawPath;
  } else if (args.command === 'task' || args.command === 'mail') {
    const defaultPath = defaultRawPath(`email-${args.command}`);
    writeJsonFile(defaultPath, body);
    output.raw_saved = true;
    output.raw_path = defaultPath;
  }

  if (args.compact) {
    process.stdout.write(`${JSON.stringify(emailStatusNormalOutput(output, args.debugMetadata), null, 2)}\n`);
    return;
  }
  process.stdout.write(`${JSON.stringify(body, null, 2)}\n`);
}

function emailStatusNormalOutput(output, debugMetadata) {
  return applyDebugMetadata(output, [
    'raw_path',
    'output_budget'
  ], debugMetadata);
}

main().catch((error) => {
  console.error(error.message);
  usage();
  process.exit(2);
});
