#!/usr/bin/env node
'use strict';

const https = require('node:https');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const BASE_HOST = 'ima.qq.com';
const BASE_PATH = '/';

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const k = argv[i].replace(/^--/, '');
      if (k === 'json') {
        args.json = true;
        continue;
      }
      if (k === 'help' || k === 'h') {
        args.help = true;
        continue;
      }
      if (i + 1 >= argv.length || argv[i + 1].startsWith('--')) {
        args[k] = true;
      } else {
        args[k] = argv[++i];
      }
    }
  }
  return args;
}

function loadCreds() {
  const home = process.env.HOME || process.env.USERPROFILE || '';
  const confDir = path.join(home, '.config', 'ima');
  let clientId = (process.env.IMA_OPENAPI_CLIENTID || '').trim();
  let apiKey = (process.env.IMA_OPENAPI_APIKEY || '').trim();

  if (!clientId && fs.existsSync(path.join(confDir, 'client_id'))) {
    let content = fs.readFileSync(path.join(confDir, 'client_id'));
    // 检测UTF-16 BOM
    if (content[0] === 0xff && content[1] === 0xfe) {
      content = content.toString('utf16le');
    } else if (content[0] === 0xfe && content[1] === 0xff) {
      content = content.toString('utf16be');
    } else {
      content = content.toString('utf8');
    }
    clientId = content.replace(/^\uFEFF/, '').trim();
  }
  if (!apiKey && fs.existsSync(path.join(confDir, 'api_key'))) {
    let content = fs.readFileSync(path.join(confDir, 'api_key'));
    // 检测UTF-16 BOM
    if (content[0] === 0xff && content[1] === 0xfe) {
      content = content.toString('utf16le');
    } else if (content[0] === 0xfe && content[1] === 0xff) {
      content = content.toString('utf16be');
    } else {
      content = content.toString('utf8');
    }
    apiKey = content.replace(/^\uFEFF/, '').trim();
  }
  return { clientId, apiKey };
}

function buildQuery(body) {
  if (typeof body === 'string') return body;
  return JSON.stringify(body);
}

function parseResponse(res, raw) {
  return new Promise((resolve, reject) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
      try {
        const parsed = JSON.parse(data);
        resolve({ status: res.statusCode, data: parsed, raw });
      } catch {
        resolve({ status: res.statusCode, data: data, raw });
      }
    });
    res.on('error', reject);
  });
}

async function apiRequest(apiPath, body, creds, options = {}) {
  const { clientId, apiKey } = creds;
  if (!clientId || !apiKey) {
    throw new Error('Missing IMA credentials. Set IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY env vars, or configure ~/.config/ima/{client_id,api_key}');
  }

  const bodyStr = buildQuery(body);
  const headers = {
    'ima-openapi-clientid': clientId,
    'ima-openapi-apikey': apiKey,
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(bodyStr)
  };

  const urlObj = new URL(apiPath.startsWith('http') ? apiPath : `https://${BASE_HOST}/${apiPath.replace(/^\//, '')}`);

  const httpOpts = {
    hostname: urlObj.hostname || BASE_HOST,
    port: urlObj.port || 443,
    path: urlObj.pathname + urlObj.search,
    method: 'POST',
    headers
  };

  return new Promise((resolve, reject) => {
    const req = (httpOpts.port === 443 ? https : http).request(httpOpts, async res => {
      try {
        const result = await parseResponse(res);
        if (result.data && typeof result.data.code !== 'undefined') {
          if (result.data.code !== 0) {
            console.error(`IMA API Error [${result.data.code}]: ${result.data.msg}`);
            process.exit(result.data.code);
          }
        }
        resolve(result);
      } catch (e) {
        reject(e);
      }
    });
    req.on('error', reject);
    req.write(bodyStr);
    req.end();
  });
}

function printUsage() {
  console.log(`
ima-api.cjs - IMA OpenAPI 调用工具

用法:
  node ima-api.cjs --path <api路径> --body <json字符串> [选项]

必需参数:
  --path    API路径，如 openapi/note/v1/search_note_book
  --body    请求体JSON字符串

可选参数:
  --json    输出完整响应JSON（默认只输出data字段）

示例:
  node ima-api.cjs --path openapi/note/v1/search_note_book --body '{"search_type":0,"query_info":{"title":"工作"},"start":0,"end":20}'

  node ima-api.cjs --path openapi/wiki/v1/get_knowledge_base --body '{"knowledge_base_id":"xxx"}' --json
`);
}

async function main() {
  const args = parseArgs(process.argv);

  if (args.help) {
    printUsage();
    return;
  }

  if (!args.path || !args.body) {
    console.error('Error: --path and --body are required');
    printUsage();
    process.exit(1);
  }

  const creds = loadCreds();
  let body;
  try {
    body = JSON.parse(args.body);
  } catch {
    console.error('Error: --body must be valid JSON');
    process.exit(1);
  }

  const result = await apiRequest(args.path, body, creds);

  if (args.json) {
    console.log(JSON.stringify(result.data, null, 2));
  } else if (result.data && result.data.data) {
    console.log(JSON.stringify(result.data.data, null, 2));
  } else {
    console.log(JSON.stringify(result.data, null, 2));
  }
}

module.exports = { apiRequest, loadCreds };

if (require.main === module) {
  main().catch(e => {
    console.error(`Request failed: ${e.message}`);
    process.exit(1);
  });
}
