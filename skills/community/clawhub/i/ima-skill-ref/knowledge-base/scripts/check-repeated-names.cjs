#!/usr/bin/env node
'use strict';

const path = require('node:path');
const fs = require('node:fs');
const https = require('node:https');

const BASE_HOST = 'ima.qq.com';
const API_BASE = '/openapi/wiki/v1';

function loadCreds() {
  const home = process.env.HOME || process.env.USERPROFILE || '';
  const confDir = path.join(home, '.config', 'ima');
  let clientId = process.env.IMA_OPENAPI_CLIENTID || '';
  let apiKey = process.env.IMA_OPENAPI_APIKEY || '';
  if (!clientId && fs.existsSync(path.join(confDir, 'client_id'))) {
    clientId = fs.readFileSync(path.join(confDir, 'client_id'), 'utf8').trim();
  }
  if (!apiKey && fs.existsSync(path.join(confDir, 'api_key'))) {
    apiKey = fs.readFileSync(path.join(confDir, 'api_key'), 'utf8').trim();
  }
  return { clientId, apiKey };
}

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const k = argv[i].replace(/^--/, '');
      if (k === 'json' || k === 'h' || k === 'help') {
        args[k] = true;
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

async function apiRequest(apiPath, body, creds) {
  const { clientId, apiKey } = creds;
  if (!clientId || !apiKey) {
    throw new Error('Missing IMA credentials');
  }
  const bodyStr = JSON.stringify(body);
  const headers = {
    'ima-openapi-clientid': clientId,
    'ima-openapi-apikey': apiKey,
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(bodyStr)
  };
  return new Promise((resolve, reject) => {
    const req = https.request({ hostname: BASE_HOST, port: 443, path: API_BASE + apiPath, method: 'POST', headers }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed);
        } catch {
          resolve({ raw: data });
        }
      });
    });
    req.on('error', reject);
    req.write(bodyStr);
    req.end();
  });
}

function printUsage() {
  console.log(`
check-repeated-names.cjs - 检查文件名重复

用法:
  node check-repeated-names.cjs --kb-id <知识库ID> --names <name1:mediaType1,name2:mediaType2> [--folder-id <folderID>] [--json]

必需参数:
  --kb-id     知识库ID
  --names     文件名列表，格式: 文件名1:media_type1,文件名2:media_type2

可选参数:
  --folder-id 文件夹ID（根目录可省略）
  --json      输出完整响应JSON

示例:
  node check-repeated-names.cjs --kb-id "kb_xxx" --names "report.pdf:1,data.xlsx:5"
  node check-repeated-names.cjs --kb-id "kb_xxx" --names "logo.png:9" --folder-id "folder_xxx" --json
`);
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.h || args.help) {
    printUsage();
    return;
  }

  const kbId = args['kb-id'] || args['kb_id'];
  const namesStr = args.names;

  if (!kbId || !namesStr) {
    console.error('Error: --kb-id and --names are required');
    printUsage();
    process.exit(1);
  }

  const params = namesStr.split(',').map(pair => {
    const [name, mediaTypeStr] = pair.split(':');
    return { name: name.trim(), media_type: parseInt(mediaTypeStr.trim()) };
  });

  const body = {
    knowledge_base_id: kbId,
    params: params
  };

  if (args['folder-id'] || args.folder_id) {
    body.folder_id = args['folder-id'] || args.folder_id;
  }

  const creds = loadCreds();
  const result = await apiRequest('/check_repeated_names', body, creds);

  if (result.code === 0) {
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      const results = result.data?.results || [];
      console.log(`文件名重复检查结果：\n`);
      let hasRepeated = false;
      results.forEach(r => {
        if (r.is_repeated) {
          hasRepeated = true;
          console.log(`❌ ${r.name} - 文件名重复`);
        } else {
          console.log(`✅ ${r.name} - 可用`);
        }
      });
      if (hasRepeated) {
        console.log(`\n⚠️  存在重复文件名，请处理后继续`);
      }
    }
  } else {
    console.error(`检查失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

main().catch(e => {
  console.error(`Error: ${e.message}`);
  process.exit(1);
});
