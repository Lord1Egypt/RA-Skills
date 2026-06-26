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
create-media.cjs - 创建媒体并获取COS上传凭证

用法:
  node create-media.cjs --kb-id <知识库ID> --file-name <文件名> --file-size <字节数> --content-type <MIME类型> --file-ext <扩展名> [--json]

必需参数:
  --kb-id         知识库ID
  --file-name     文件名（如report.pdf）
  --file-size     文件大小（字节数，如1048576）
  --content-type  MIME类型（如application/pdf）
  --file-ext      文件扩展名（无点号，如pdf）

可选参数:
  --json          输出完整响应JSON

示例:
  node create-media.cjs --kb-id "kb_xxx" --file-name "report.pdf" --file-size 1048576 --content-type "application/pdf" --file-ext "pdf"
  node create-media.cjs --kb-id "kb_xxx" --file-name "data.xlsx" --file-size 2097152 --content-type "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" --file-ext "xlsx" --json
`);
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.h || args.help) {
    printUsage();
    return;
  }

  const kbId = args['kb-id'] || args['kb_id'];
  const fileName = args['file-name'] || args.file_name;
  const fileSize = args['file-size'] || args.file_size;
  const contentType = args['content-type'] || args.content_type;
  const fileExt = args['file-ext'] || args.file_ext;

  if (!kbId || !fileName || !fileSize || !contentType || !fileExt) {
    console.error('Error: --kb-id, --file-name, --file-size, --content-type, and --file-ext are required');
    printUsage();
    process.exit(1);
  }

  const body = {
    knowledge_base_id: kbId,
    file_name: fileName,
    file_size: parseInt(fileSize),
    content_type: contentType,
    file_ext: fileExt
  };

  const creds = loadCreds();
  const result = await apiRequest('/create_media', body, creds);

  if (result.code === 0) {
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      const data = result.data || {};
      const mediaId = data.media_id;
      const cosCred = data.cos_credential || {};

      console.log(`✅ 媒体创建成功`);
      console.log(`   Media ID: ${mediaId}`);
      console.log(``);
      console.log(`COS凭证：`);
      console.log(`   Bucket: ${cosCred.bucket_name}`);
      console.log(`   Region: ${cosCred.region}`);
      console.log(`   COS Key: ${cosCred.cos_key}`);
      console.log(``);
      console.log(`COS上传命令示例：`);
      console.log(`   node cos-upload.cjs \\`);
      console.log(`     --file <本地文件路径> \\`);
      // 为安全起见，不打印敏感凭证到stdout
      // 凭证信息可通过安全方式传递给后续脚本
      console.log(`     --bucket "${cosCred.bucket_name}" \\`);
      console.log(`     --region "${cosCred.region}" \\`);
      console.log(`     --cos-key "${cosCred.cos_key}" \\`);
      console.log(`     --content-type "${contentType}"`);
      
      // 将敏感凭证写入临时文件，供后续脚本安全读取
      const tempDir = process.env.TMPDIR || process.env.TEMP || '/tmp';
      const credFile = path.join(tempDir, `ima-cos-cred-${Date.now()}.json`);
      try {
        fs.writeFileSync(credFile, JSON.stringify({
          secret_id: cosCred.secret_id,
          secret_key: cosCred.secret_key,
          token: cosCred.token
        }, null, 2));
        console.log(`     --cred-file "${credFile}"`);
      } catch (e) {
        // 如果写入临时文件失败，回退到环境变量方式
        console.error(`警告: 无法写入临时凭证文件: ${e.message}`);
      }
    }
  } else {
    console.error(`创建失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

main().catch(e => {
  console.error(`Error: ${e.message}`);
  process.exit(1);
});
