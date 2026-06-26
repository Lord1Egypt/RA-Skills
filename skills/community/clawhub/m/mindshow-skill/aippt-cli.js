#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const DEFAULT_API_DOC = path.join(__dirname, 'apidoc.json');
const DEFAULT_ENV_FILE = path.join(__dirname, '.env');

function printUsage() {
  console.log(`Usage:
  node aippt-cli.js list
  node aippt-cli.js schema <path>
  node aippt-cli.js call <path> [options]

Options:
  --token <token>         Bearer token. Defaults to AIPPT_TOKEN env var.
  --base-url <url>       Override server URL from apidoc.json.
  --apidoc <file>        OpenAPI json file. Defaults to ./apidoc.json.
  --env <file>           Env file with AIPPT_TOKEN. Defaults to ./.env.
  --data <json>          JSON request body, for example '{"id":"xxx"}'.
  --data-file <file>     Read JSON request body from file.
  --file <file>          File path for multipart/form-data upload.
  --field key=value      Extra multipart field. Can be repeated.
  --method <method>      Override HTTP method. Defaults to method in apidoc.json.
  --timeout <ms>         Request timeout. Defaults to 120000.
  --pretty               Pretty-print JSON output.
  --help                 Show this help.

Environment:
  AIPPT_TOKEN            Bearer token used when --token is omitted. Can be set in .env.
  AIPPT_BASE_URL         Server URL used when --base-url is omitted. Can be set in .env.

Examples:
  AIPPT_TOKEN=xxx node aippt-cli.js call /v1/account/info
  AIPPT_TOKEN=xxx node aippt-cli.js call /v1/job/get --data '{"id":"job_id"}'
  AIPPT_TOKEN=xxx node aippt-cli.js call /v1/resource/upload --file ./demo.pptx
`);
}

function fail(message, extra) {
  const payload = { ok: false, error: message };
  if (extra !== undefined) payload.detail = extra;
  console.error(JSON.stringify(payload, null, 2));
  process.exit(1);
}

function parseArgs(argv) {
  const result = { _: [] };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) {
      result._.push(arg);
      continue;
    }

    const eqIndex = arg.indexOf('=');
    const key = arg.slice(2, eqIndex === -1 ? undefined : eqIndex);
    const inlineValue = eqIndex === -1 ? undefined : arg.slice(eqIndex + 1);

    if (key === 'help' || key === 'pretty') {
      result[key] = true;
      continue;
    }

    const value = inlineValue !== undefined ? inlineValue : argv[++i];
    if (value === undefined) fail(`Missing value for --${key}`);

    if (key === 'field') {
      if (!result.field) result.field = [];
      result.field.push(value);
    } else {
      result[key] = value;
    }
  }

  return result;
}

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (error) {
    fail(`Failed to read JSON file: ${file}`, error.message);
  }
}

function parseEnvValue(value) {
  const trimmed = value.trim();
  if (
    (trimmed.startsWith('"') && trimmed.endsWith('"')) ||
    (trimmed.startsWith("'") && trimmed.endsWith("'"))
  ) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

function loadEnvFile(file) {
  if (!fs.existsSync(file)) return;

  const text = fs.readFileSync(file, 'utf8');
  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;

    const normalized = line.startsWith('export ') ? line.slice(7).trim() : line;
    const eqIndex = normalized.indexOf('=');
    if (eqIndex === -1) continue;

    const key = normalized.slice(0, eqIndex).trim();
    if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(key)) continue;
    if (process.env[key] !== undefined && process.env[key] !== '') continue;

    process.env[key] = parseEnvValue(normalized.slice(eqIndex + 1));
  }
}

function findOperation(apiDoc, requestedPath, requestedMethod) {
  const pathItem = apiDoc.paths && apiDoc.paths[requestedPath];
  if (!pathItem) {
    fail(`API path not found in apidoc.json: ${requestedPath}`);
  }

  const method = (requestedMethod || Object.keys(pathItem)[0] || 'post').toLowerCase();
  const operation = pathItem[method];
  if (!operation) {
    fail(`HTTP method not found for ${requestedPath}: ${method.toUpperCase()}`);
  }

  return { method, operation };
}

function getRequestContent(operation) {
  return operation.requestBody && operation.requestBody.content
    ? operation.requestBody.content
    : {};
}

function parseRequestBody(args) {
  if (args.data && args['data-file']) {
    fail('Use either --data or --data-file, not both');
  }

  if (args.data) {
    try {
      return JSON.parse(args.data);
    } catch (error) {
      fail('Invalid JSON passed to --data', error.message);
    }
  }

  if (args['data-file']) {
    return readJson(path.resolve(args['data-file']));
  }

  return {};
}

function appendMultipartFields(form, fields) {
  for (const item of fields || []) {
    const eqIndex = item.indexOf('=');
    if (eqIndex === -1) fail(`Invalid --field value, expected key=value: ${item}`);
    const key = item.slice(0, eqIndex);
    const value = item.slice(eqIndex + 1);
    form.append(key, value);
  }
}

async function buildFetchOptions(args, method, operation, requestBody) {
  const token = args.token || process.env.AIPPT_TOKEN;
  const headers = { Accept: 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;

  const content = getRequestContent(operation);
  const contentTypes = Object.keys(content);
  const wantsMultipart = contentTypes.includes('multipart/form-data') || Boolean(args.file);

  if (wantsMultipart) {
    if (!args.file) fail('This endpoint requires --file for multipart/form-data');
    const filePath = path.resolve(args.file);
    const fileBytes = fs.readFileSync(filePath);
    const form = new FormData();
    form.append('file', new Blob([fileBytes]), path.basename(filePath));
    appendMultipartFields(form, args.field);
    return { method: method.toUpperCase(), headers, body: form };
  }

  headers['Content-Type'] = 'application/json';
  return {
    method: method.toUpperCase(),
    headers,
    body: JSON.stringify(requestBody === undefined ? parseRequestBody(args) : requestBody),
  };
}

async function writeStreamToStdout(response) {
  if (!response.body) return;

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    process.stdout.write(decoder.decode(value, { stream: true }));
  }

  const rest = decoder.decode();
  if (rest) process.stdout.write(rest);
}

async function callApi(apiDoc, apiPath, args) {
  const { method, operation } = findOperation(apiDoc, apiPath, args.method);
  const baseUrl = (args['base-url'] || process.env.AIPPT_BASE_URL || apiDoc.servers?.[0]?.url || '').replace(/\/+$/, '');
  if (!baseUrl) fail('No base URL found. Pass --base-url or add servers[0].url to apidoc.json');

  const timeoutMs = Number(args.timeout || 120000);
  if (!Number.isFinite(timeoutMs) || timeoutMs <= 0) fail('--timeout must be a positive number');

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const requestBody = args.file ? undefined : parseRequestBody(args);
    const shouldStreamRawSse = requestBody && requestBody.stream === true;
    const response = await fetch(`${baseUrl}${apiPath}`, {
      ...(await buildFetchOptions(args, method, operation, requestBody)),
      signal: controller.signal,
    });

    if (shouldStreamRawSse) {
      await writeStreamToStdout(response);
      return null;
    }

    const text = await response.text();
    let body;

    try {
      body = text ? JSON.parse(text) : null;
    } catch {
      body = text;
    }

    return {
      ok: response.ok,
      status: response.status,
      statusText: response.statusText,
      path: apiPath,
      method: method.toUpperCase(),
      data: body,
    };
  } catch (error) {
    fail('Request failed', error.name === 'AbortError' ? `Timeout after ${timeoutMs}ms` : error.message);
  } finally {
    clearTimeout(timer);
  }
}

function listApis(apiDoc) {
  const rows = [];
  for (const [apiPath, pathItem] of Object.entries(apiDoc.paths || {})) {
    for (const [method, operation] of Object.entries(pathItem)) {
      rows.push({
        method: method.toUpperCase(),
        path: apiPath,
        summary: operation.summary || '',
        contentTypes: Object.keys(getRequestContent(operation)),
        required: Object.values(getRequestContent(operation))[0]?.schema?.required || [],
      });
    }
  }
  return rows;
}

function getSchema(apiDoc, apiPath, args) {
  const { method, operation } = findOperation(apiDoc, apiPath, args.method);
  const content = getRequestContent(operation);
  return {
    method: method.toUpperCase(),
    path: apiPath,
    summary: operation.summary || '',
    description: operation.description || '',
    tags: operation.tags || [],
    requestContent: content,
    responseContent: operation.responses?.['200']?.content || {},
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  loadEnvFile(path.resolve(args.env || DEFAULT_ENV_FILE));
  const command = args._[0];

  if (!command || args.help) {
    printUsage();
    return;
  }

  const apiDoc = readJson(path.resolve(args.apidoc || DEFAULT_API_DOC));
  let output;

  if (command === 'list') {
    output = listApis(apiDoc);
  } else if (command === 'schema') {
    const apiPath = args._[1];
    if (!apiPath) fail('Missing API path for schema command');
    output = getSchema(apiDoc, apiPath, args);
  } else if (command === 'call') {
    const apiPath = args._[1];
    if (!apiPath) fail('Missing API path for call command');
    output = await callApi(apiDoc, apiPath, args);
  } else {
    fail(`Unknown command: ${command}`);
  }

  if (output !== null) {
    console.log(JSON.stringify(output, null, args.pretty ? 2 : 0));
  }
}

main();
