#!/usr/bin/env node
'use strict';

const path = require('node:path');
const fs = require('node:fs');
const https = require('node:https');

const BASE_HOST = 'ima.qq.com';
const API_BASE = '/openapi/note/v1';

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
    'search': `Usage: node notes-ops.cjs search --query <关键词> [--type title|content] [--start 0] [--end 20] [--json]

Examples:
  node notes-ops.cjs search --query "工作日志"
  node notes-ops.cjs search --query "会议" --type content --json`,
    'list-folders': `Usage: node notes-ops.cjs list-folders [--cursor "0"] [--limit 20] [--json]

Examples:
  node notes-ops.cjs list-folders
  node notes-ops.cjs list-folders --limit 50 --json`,
    'list-notes': `Usage: node notes-ops.cjs list-notes [--folder-id <id>] [--cursor ""] [--limit 20] [--json]

Examples:
  node notes-ops.cjs list-notes
  node notes-ops.cjs list-notes --folder-id "folder_xxx" --json`,
    'read': `Usage: node notes-ops.cjs read --doc-id <id> [--format 0] [--json]

Examples:
  node notes-ops.cjs read --doc-id "doc_xxx"
  node notes-ops.cjs read --doc-id "doc_xxx" --format 0 --json`,
    'create': `Usage: node notes-ops.cjs create --content <markdown内容> [--title <标题>] [--json]

Examples:
  node notes-ops.cjs create --content "# 今天的工作\\n\\n完成了..."
  node notes-ops.cjs create --title "工作日志" --content "# 今天..." --json`,
    'append': `Usage: node notes-ops.cjs append --doc-id <id> --content <追加内容> [--json]

Examples:
  node notes-ops.cjs append --doc-id "doc_xxx" --content "\\n\\n## 补充\\n新内容"
  node notes-ops.cjs append --doc-id "doc_xxx" --content "追加内容" --json`
  };
  console.log('\n' + (cmds[cmd] || 'Unknown command. Use: search|list-folders|list-notes|read|create|append'));
  console.log('\nGlobal options: --json (output full response)');
}

async function cmdSearch(args) {
  const creds = loadCreds();
  const query = args.query || args.q;
  if (!query) {
    console.error('Error: --query is required');
    process.exit(1);
  }
  const searchType = args.type === 'content' ? 1 : 0;
  const body = {
    search_type: searchType,
    query_info: { title: query, content: query },
    start: parseInt(args.start) || 0,
    end: parseInt(args.end) || 20
  };
  if (searchType === 0) {
    body.query_info = { title: query };
  } else {
    body.query_info = { content: query };
  }
  const result = await apiRequest('/search_note_book', body, creds);
  if (result.code === 0) {
    const docs = result.data?.docs || [];
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      console.log(`找到 ${docs.length} 篇笔记：\n`);
      docs.forEach((d, i) => {
        const info = d.doc?.basic_info || {};
        console.log(`${i + 1}. ${info.title || '无标题'}`);
        console.log(`   ID: ${info.docid}`);
        if (info.summary) console.log(`   摘要: ${info.summary.substring(0, 100)}...`);
        console.log('');
      });
    }
  } else {
    console.error(`搜索失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

async function cmdListFolders(args) {
  const creds = loadCreds();
  const body = { cursor: args.cursor || "0", limit: parseInt(args.limit) || 20 };
  const result = await apiRequest('/list_note_folder_by_cursor', body, creds);
  if (result.code === 0) {
    const folders = result.data?.note_book_folders || [];
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      console.log(`笔记本列表（共 ${folders.length} 个）：\n`);
      folders.forEach((f, i) => {
        const info = f.folder?.basic_info || {};
        console.log(`${i + 1}. ${info.name || '未命名'} (${info.folder_type})`);
        console.log(`   ID: ${info.folder_id}`);
        console.log('');
      });
    }
  } else {
    console.error(`获取失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

async function cmdListNotes(args) {
  const creds = loadCreds();
  const body = {
    folder_id: args['folder-id'] || "",
    cursor: args.cursor || "",
    limit: parseInt(args.limit) || 20
  };
  const result = await apiRequest('/list_note_by_folder_id', body, creds);
  if (result.code === 0) {
    const notes = result.data?.note_book_list || [];
    const isEnd = result.data?.is_end;
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      console.log(`笔记列表（共 ${notes.length} 篇）：\n`);
      notes.forEach((n, i) => {
        const info = n.basic_info?.basic_info || {};
        console.log(`${i + 1}. ${info.title || '无标题'}`);
        console.log(`   ID: ${info.docid}`);
        if (info.summary) console.log(`   摘要: ${info.summary.substring(0, 80)}...`);
        console.log('');
      });
      if (!isEnd) console.log('(还有更多，使用 --cursor ' + (result.data?.next_cursor || '') + ' 获取)');
    }
  } else {
    console.error(`获取失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

async function cmdRead(args) {
  const creds = loadCreds();
  const docId = args['doc-id'] || args.doc_id;
  if (!docId) {
    console.error('Error: --doc-id is required');
    process.exit(1);
  }
  const body = { doc_id: docId, target_content_format: parseInt(args.format) || 0 };
  const result = await apiRequest('/get_doc_content', body, creds);
  if (result.code === 0) {
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      const content = result.data?.content || '';
      console.log(content);
    }
  } else {
    console.error(`读取失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

async function cmdCreate(args) {
  const creds = loadCreds();
  const content = args.content;
  if (!content) {
    console.error('Error: --content is required');
    process.exit(1);
  }
  const finalContent = args.title ? `# ${args.title}\n\n${content}` : content;
  const body = { content_format: 1, content: finalContent };
  const result = await apiRequest('/import_doc', body, creds);
  if (result.code === 0) {
    const docId = result.data?.doc_id;
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      console.log(`✅ 笔记创建成功`);
      console.log(`   ID: ${docId}`);
    }
  } else {
    console.error(`创建失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

async function cmdAppend(args) {
  const creds = loadCreds();
  const docId = args['doc-id'] || args.doc_id;
  const content = args.content;
  if (!docId || !content) {
    console.error('Error: --doc-id and --content are required');
    process.exit(1);
  }
  const body = { doc_id: docId, content_format: 1, content: content };
  const result = await apiRequest('/append_doc', body, creds);
  if (result.code === 0) {
    if (args.json) {
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      console.log(`✅ 内容已追加到笔记 ${docId}`);
    }
  } else {
    console.error(`追加失败 [${result.code}]: ${result.msg}`);
    process.exit(result.code);
  }
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.h || args.help) {
    printUsage(args._?.[0] || 'search');
    return;
  }
  const cmd = args._?.[0] || (Object.keys(args).length === 0 ? 'help' : 'search');
  switch (cmd) {
    case 'search': await cmdSearch(args); break;
    case 'list-folders': await cmdListFolders(args); break;
    case 'list-notes': await cmdListNotes(args); break;
    case 'read': await cmdRead(args); break;
    case 'create': await cmdCreate(args); break;
    case 'append': await cmdAppend(args); break;
    default: printUsage('search');
  }
}

main().catch(e => {
  console.error(`Error: ${e.message}`);
  process.exit(1);
});
