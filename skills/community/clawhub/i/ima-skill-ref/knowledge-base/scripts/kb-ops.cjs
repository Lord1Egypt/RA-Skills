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

function parseArgs(argv) {
  const args = { _: [] };
  let i = 2;
  while (i < argv.length) {
    if (argv[i].startsWith('--')) {
      const k = argv[i].replace(/^--/, '');
      if (k === 'json' || k === 'h' || k === 'help') {
        args[k] = true;
        i++;
        continue;
      }
      if (i + 1 >= argv.length || argv[i + 1].startsWith('--')) {
        args[k] = true;
        i++;
      } else {
        args[k] = argv[i + 1];
        i += 2;
      }
    } else {
      args._.push(argv[i]);
      i++;
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

function printUsage(cmd) {
  const cmds = {
    'list': `Usage: node kb-ops.cjs list [--query <搜索词>] [--cursor ""] [--limit 50] [--json]

Examples:
  node kb-ops.cjs list
  node kb-ops.cjs list --query "产品"
  node kb-ops.cjs list --limit 100 --json`,
    'search': `Usage: node kb-ops.cjs search --kb-id <知识库ID> --query <搜索词> [--cursor ""] [--limit 20] [--json]

Examples:
  node kb-ops.cjs search --kb-id "kb_xxx" --query "文档"
  node kb-ops.cjs search --kb-id "kb_xxx" --query "设计" --json`,
    'get-kb': `Usage: node kb-ops.cjs get-kb --kb-id <知识库ID> [--json]

Examples:
  node kb-ops.cjs get-kb --kb-id "kb_xxx"
  node kb-ops.cjs get-kb --kb-id "kb_xxx" --json`,
    'list-kbs': `Usage: node kb-ops.cjs list-kbs [--query <搜索词>] [--json]

Examples:
  node kb-ops.cjs list-kbs
  node kb-ops.cjs list-kbs --query "产品"
  node kb-ops.cjs list-kbs --json`,
    'add-urls': `Usage: node kb-ops.cjs add-urls --kb-id <知识库ID> --urls <url1,url2> [--folder-id <folderID>] [--json]

Examples:
  node kb-ops.cjs add-urls --kb-id "kb_xxx" --urls "https://example.com/article"
  node kb-ops.cjs add-urls --kb-id "kb_xxx" --urls "url1,url2" --folder-id "folder_xxx" --json`,
    'add-note': `Usage: node kb-ops.cjs add-note --kb-id <知识库ID> --doc-id <笔记ID> --title <标题> [--folder-id <folderID>] [--json]

Examples:
  node kb-ops.cjs add-note --kb-id "kb_xxx" --doc-id "doc_xxx" --title "工作日志"
  node kb-ops.cjs add-note --kb-id "kb_xxx" --doc-id "doc_xxx" --title "日志" --json`
  };
  console.log('\n' + (cmds[cmd] || 'Unknown command. Use: list|search|get-kb|list-kbs|add-urls|add-note'));
  console.log('\nGlobal options: --json (output full response)');
}

async function cmdList(args) {
  const creds = loadCreds();
  const kbId = args['kb-id'] || args['kb_id'];
  if (!kbId) {
    console.error('Error: --kb-id is required');
    process.exit(1);
  }
  const body = {
    knowledge_base_id: kbId,
    cursor: args.cursor || "",
    limit: parseInt(args.limit) || 50
  };
  if (args.query) {
    body.query = args.query;
  }
  const result = await apiRequest('/get_knowledge_list', body, creds);
  if (result.code === 0) {
    const items = result.data?.knowledge_list || [];
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      console.log(`知识库内容（共 ${items.length} 项）：\n`);
      items.forEach((item, i) => {
        const isFolder = item.title?.startsWith('📁') || item.media_id?.startsWith('folder_');
        console.log(`${i + 1}. ${item.title || '未命名'} ${isFolder ? '(文件夹)' : ''}`);
        console.log(`   ID: ${item.media_id}`);
        if (item.highlight_content) console.log(`   摘要: ${item.highlight_content.substring(0, 100)}...`);
        console.log('');
      });
    }
  } else {
    console.error(`获取失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

async function cmdSearch(args) {
  const creds = loadCreds();
  const kbId = args['kb-id'] || args['kb_id'];
  const query = args.query || args.q;
  if (!kbId || !query) {
    console.error('Error: --kb-id and --query are required');
    process.exit(1);
  }
  const body = {
    knowledge_base_id: kbId,
    query: query,
    cursor: args.cursor || "",
    limit: parseInt(args.limit) || 20
  };
  const result = await apiRequest('/search_knowledge', body, creds);
  if (result.code === 0) {
    const items = result.data?.info_list || [];
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      console.log(`搜索「${query}」找到 ${items.length} 项：\n`);
      items.forEach((item, i) => {
        console.log(`${i + 1}. ${item.title || '未命名'}`);
        console.log(`   ID: ${item.media_id}`);
        if (item.highlight_content) console.log(`   ${item.highlight_content}...`);
        console.log('');
      });
    }
  } else {
    console.error(`搜索失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

async function cmdGetKb(args) {
  const creds = loadCreds();
  const kbId = args['kb-id'] || args['kb_id'];
  if (!kbId) {
    console.error('Error: --kb-id is required');
    process.exit(1);
  }
  const body = { ids: [kbId] };
  const result = await apiRequest('/get_knowledge_base', body, creds);
  if (result.code === 0) {
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      const infos = result.data?.infos || {};
      const kb = infos[kbId];
      if (kb) {
        console.log(`📚 ${kb.name || '未命名'}`);
        if (kb.description) console.log(`   ${kb.description}`);
        console.log(`   ID: ${kb.id}`);
      }
    }
  } else {
    console.error(`获取失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

async function cmdListKbs(args) {
  const creds = loadCreds();
  const body = { limit: 50 };
  if (args.query) {
    body.query = args.query;
  }
  const result = await apiRequest('/search_knowledge_base', body, creds);
  if (result.code === 0) {
    const kbs = result.data?.info_list || [];
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      console.log(`知识库列表（共 ${kbs.length} 个）：\n`);
      kbs.forEach((kb, i) => {
        console.log(`${i + 1}. ${kb.name || '未命名'}`);
        if (kb.description) console.log(`   ${kb.description}`);
        console.log(`   ID: ${kb.id}`);
        console.log('');
      });
    }
  } else {
    console.error(`获取失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

async function cmdAddUrls(args) {
  const creds = loadCreds();
  const kbId = args['kb-id'] || args['kb_id'];
  const urls = args.urls;
  if (!kbId || !urls) {
    console.error('Error: --kb-id and --urls are required');
    process.exit(1);
  }
  const body = {
    knowledge_base_id: kbId,
    urls: urls.split(',').map(u => u.trim())
  };
  if (args['folder-id'] || args.folder_id) {
    body.folder_id = args['folder-id'] || args.folder_id;
  }
  const result = await apiRequest('/import_urls', body, creds);
  if (result.code === 0) {
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      const results = result.data?.results || {};
      let success = 0, failed = 0;
      for (const [url, info] of Object.entries(results)) {
        if (info.ret_code === 0) {
          success++;
          console.log(`✅ ${url}`);
        } else {
          failed++;
          console.log(`❌ ${url}: ${info.ret_msg || '失败'}`);
        }
      }
      console.log(`\n添加完成：${success} 成功，${failed} 失败`);
    }
  } else {
    console.error(`添加失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

async function cmdAddNote(args) {
  const creds = loadCreds();
  const kbId = args['kb-id'] || args['kb_id'];
  const docId = args['doc-id'] || args.doc_id;
  const title = args.title;
  if (!kbId || !docId || !title) {
    console.error('Error: --kb-id, --doc-id, and --title are required');
    process.exit(1);
  }
  const body = {
    media_type: 11,
    note_info: { content_id: docId },
    title: title,
    knowledge_base_id: kbId
  };
  if (args['folder-id'] || args.folder_id) {
    body.folder_id = args['folder-id'] || args.folder_id;
  }
  const result = await apiRequest('/add_knowledge', body, creds);
  if (result.code === 0) {
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      console.log(`✅ 笔记「${title}」已添加到知识库`);
      console.log(`   Media ID: ${result.data?.media_id || 'N/A'}`);
    }
  } else {
    console.error(`添加失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.h || args.help) {
    printUsage(args._?.[0] || 'list');
    return;
  }
  const cmd = args._?.[0];
  if (!cmd) {
    printUsage('list');
    return;
  }
  switch (cmd) {
    case 'list': await cmdList(args); break;
    case 'search': await cmdSearch(args); break;
    case 'get-kb': await cmdGetKb(args); break;
    case 'list-kbs': await cmdListKbs(args); break;
    case 'add-urls': await cmdAddUrls(args); break;
    case 'add-note': await cmdAddNote(args); break;
    default: printUsage('list');
  }
}

main().catch(e => {
  console.error(`Error: ${e.message}`);
  process.exit(1);
});
