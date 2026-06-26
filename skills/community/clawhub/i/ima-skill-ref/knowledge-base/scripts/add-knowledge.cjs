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
add-knowledge.cjs - 添加知识到知识库

用法（添加文件）:
  node add-knowledge.cjs --kb-id <知识库ID> --media-type <media_type> --title <标题> --media-id <media_id> --cos-key <cos_key> --file-size <字节数> --file-name <文件名> [--folder-id <folderID>] [--json]

用法（添加笔记）:
  node add-knowledge.cjs --kb-id <知识库ID> --media-type 11 --title <标题> --doc-id <笔记ID> [--folder-id <folderID>] [--json]

用法（添加网页）:
  node add-knowledge.cjs --kb-id <知识库ID> --media-type 2 --title <标题> --url <网页URL> [--folder-id <folderID>] [--json]

必需参数:
  --kb-id         知识库ID
  --media-type    media_type（1=PDF,3=Word,4=PPT,5=Excel,7=MD,9=图片,11=笔记,2=网页）
  --title         标题

文件特定参数:
  --media-id      create_media 返回的 media_id
  --cos-key       COS Key
  --file-size     文件大小（字节数）
  --file-name     文件名

笔记特定参数:
  --doc-id        笔记ID

网页特定参数:
  --url           网页URL

可选参数:
  --folder-id     文件夹ID（根目录可省略）
  --json          输出完整响应JSON

示例:
  node add-knowledge.cjs --kb-id "kb_xxx" --media-type 1 --title "报告" --media-id "media_xxx" --cos-key "xxx" --file-size 1048576 --file-name "report.pdf"
  node add-knowledge.cjs --kb-id "kb_xxx" --media-type 11 --title "工作笔记" --doc-id "doc_xxx" --folder-id "folder_xxx"
  node add-knowledge.cjs --kb-id "kb_xxx" --media-type 2 --title "文章" --url "https://example.com/article" --json
`);
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.h || args.help) {
    printUsage();
    return;
  }

  const kbId = args['kb-id'] || args['kb_id'];
  const mediaType = parseInt(args['media-type'] || args.media_type);
  const title = args.title;

  if (!kbId || isNaN(mediaType) || !title) {
    console.error('Error: --kb-id, --media-type, and --title are required');
    printUsage();
    process.exit(1);
  }

  const body = {
    knowledge_base_id: kbId,
    media_type: mediaType,
    title: title
  };

  if (mediaType === 11) {
    const docId = args['doc-id'] || args.doc_id;
    if (!docId) {
      console.error('Error: --doc-id is required when media-type=11');
      process.exit(1);
    }
    body.note_info = { content_id: docId };
  } else if (mediaType === 2) {
    const url = args.url;
    if (!url) {
      console.error('Error: --url is required when media-type=2');
      process.exit(1);
    }
    body.web_info = { content_id: url };
  } else {
    const mediaId = args['media-id'] || args.media_id;
    const cosKey = args['cos-key'] || args.cos_key;
    const fileSize = args['file-size'] || args.file_size;
    const fileName = args['file-name'] || args.file_name;
    if (!mediaId || !cosKey || !fileSize || !fileName) {
      console.error('Error: --media-id, --cos-key, --file-size, and --file-name are required for file types');
      process.exit(1);
    }
    body.media_id = mediaId;
    body.file_info = {
      cos_key: cosKey,
      file_size: parseInt(fileSize),
      file_name: fileName
    };
  }

  if (args['folder-id'] || args.folder_id) {
    body.folder_id = args['folder-id'] || args.folder_id;
  }

  const creds = loadCreds();
  const result = await apiRequest('/add_knowledge', body, creds);

  if (result.code === 0) {
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      const mediaId = result.data?.media_id;
      console.log(`✅ 知识已添加到知识库`);
      console.log(`   Media ID: ${mediaId}`);
    }
  } else {
    console.error(`添加失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

main().catch(e => {
  console.error(`Error: ${e.message}`);
  process.exit(1);
});
