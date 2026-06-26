#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const CONFIG = { baseUrl: 'https://www.hsciq.com', apiKey: '', endpoints: { toolsList: '/mcp/tools/list', toolsCall: '/mcp/tools/call' } };

function loadConfig() {
  const jsonPaths = [
    path.join(process.env.HOME, 'openclaw/workspace/hsciq-mcp-config.json'),
    path.join(process.env.HOME, '.openclaw/workspace/hsciq-mcp-config.json'),
    path.join(process.cwd(), 'hsciq-mcp-config.json')
  ];

  for (const jsonPath of jsonPaths) {
    if (fs.existsSync(jsonPath)) {
      try {
        const config = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
        if (config.apiKey) {
          CONFIG.apiKey = config.apiKey;
          CONFIG.baseUrl = config.baseUrl || 'https://www.hsciq.com';
          return;
        }
      } catch (e) {}
    }
  }

  const envPaths = [
    path.join(process.env.HOME, 'openclaw/workspace/.env.hsciq'),
    path.join(process.env.HOME, '.openclaw/workspace/.env.hsciq'),
    path.join(process.cwd(), '.env.hsciq')
  ];

  for (const envPath of envPaths) {
    if (fs.existsSync(envPath)) {
      const content = fs.readFileSync(envPath, 'utf-8');
      content.split('\n').forEach(line => {
        const [key, value] = line.split('=');
        if (key === 'HSCIQ_API_KEY') CONFIG.apiKey = value?.trim();
        else if (key === 'HSCIQ_BASE_URL') CONFIG.baseUrl = value?.trim();
      });
      if (CONFIG.apiKey) return;
    }
  }

  if (process.env.HSCIQ_API_KEY) {
    CONFIG.apiKey = process.env.HSCIQ_API_KEY;
    CONFIG.baseUrl = process.env.HSCIQ_BASE_URL || 'https://www.hsciq.com';
    return;
  }

  if (!CONFIG.apiKey) {
    console.error('错误：未找到 HSCIQ_API_KEY，请检查以下配置文件之一：');
    console.error('  - ~/.openclaw/workspace/hsciq-mcp-config.json');
    console.error('  - ~/openclaw/workspace/hsciq-mcp-config.json');
    console.error('  - ~/.openclaw/workspace/.env.hsciq');
    console.error('  - 或设置环境变量 HSCIQ_API_KEY');
    process.exit(1);
  }
}

async function callTool(toolName, args = {}) {
  const url = `${CONFIG.baseUrl}${CONFIG.endpoints.toolsCall}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-API-Key': CONFIG.apiKey },
    body: JSON.stringify({ toolName, arguments: args })
  });
  if (!response.ok) {
    const errBody = await response.text().catch(() => '');
    throw new Error(`API request failed (${response.status}): ${errBody}`);
  }
  const result = await response.json();
  if (!result.ok) throw new Error(`Tool call failed: ${result.message || ''}`);
  return result.data;
}

async function searchCode(keywords, country = 'CN', pageIndex = 1, pageSize = 10) {
  return await callTool('search_code', { keywords, country, pageIndex, pageSize, filterFailureCode: true });
}

async function getCodeDetail(code, country = 'CN') {
  return await callTool('get_code_detail', { code, country });
}

async function searchInstance(keywords, country = 'CN', pageIndex = 1, pageSize = 10) {
  return await callTool('search_instance', { keywords, country, pageIndex, pageSize, filterFailureCode: true });
}

async function searchUnified(keywords, unifiedType = 'ciq', pageIndex = 1, pageSize = 10) {
  return await callTool('search_unified', { keywords, unifiedType, pageIndex, pageSize, filterFailureCode: true, searchType: 1 });
}

async function createGuileiForm(fields = {}, imagePaths = []) {
  const args = { ...fields };
  if (imagePaths.length > 0) {
    args.images = [];
    for (const imgPath of imagePaths) {
      const data = fs.readFileSync(imgPath);
      const ext = path.extname(imgPath).toLowerCase();
      const validExts = { '.jpg': 1, '.jpeg': 1, '.png': 1, '.gif': 1, '.webp': 1 };
      if (!validExts[ext]) throw new Error(`Unsupported image format: ${ext} (only jpg/png/gif/webp)`);
      if (data.length > 1024 * 1024) throw new Error(`Image exceeds 1MB limit: ${imgPath}`);
      args.images.push({
        fileName: path.basename(imgPath),
        data: data.toString('base64')
      });
    }
  }
  return await callTool('create_guilei_form', args);
}

async function getGuileiForm(formId) {
  return await callTool('get_guilei_form', { formId });
}

async function listMyGuileiForms(pageIndex = 1, pageSize = 20) {
  return await callTool('list_my_guilei_forms', { pageIndex, pageSize });
}

async function addGuileiDialogMessage(formId, fieldKey, content, dialogId = null, messageType = null) {
  const args = { formId, fieldKey, content };
  if (dialogId) args.dialogId = dialogId;
  if (messageType != null) args.messageType = messageType;
  return await callTool('add_guilei_dialog_message', args);
}

async function main() {
  loadConfig();
  const args = process.argv.slice(2);
  const command = args[0];
  const params = {};
  const positional = [];
  for (let i = 1; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const values = [];
      let j = i + 1;
      while (j < args.length && !args[j].startsWith('--')) { values.push(args[j]); j++; }
      if (values.length === 0) { params[key] = true; }
      else if (values.length === 1) { params[key] = values[0]; }
      else { params[key] = values; }
      i = j - 1;
    } else {
      positional.push(args[i]);
    }
  }
  try {
    let result;
    switch (command) {
      case 'search-code':
        result = await searchCode(params.keywords || '', params.country || 'CN', parseInt(params.pageIndex) || 1, parseInt(params.pageSize) || 10);
        break;
      case 'get-detail':
        result = await getCodeDetail(params.code || '', params.country || 'CN');
        break;
      case 'search-instance':
        result = await searchInstance(params.keywords || '', params.country || 'CN', parseInt(params.pageIndex) || 1, parseInt(params.pageSize) || 10);
        break;
      case 'search-unified':
        result = await searchUnified(params.keywords || '', params.type || 'ciq', parseInt(params.pageIndex) || 1, parseInt(params.pageSize) || 10);
        break;
      case 'create-guilei-form': {
        const fields = {};
        const textFields = ['productNameCn','productNameEn','uses','ingredients','cas','brand','model','otherProductInfo','qq','weixin'];
        textFields.forEach(f => { if (params[f] !== undefined) fields[f] = params[f]; });
        if (params.isPaid) fields.isPaid = params.isPaid === 'true' || params.isPaid === true;
        const imgPaths = Array.isArray(params.images) ? params.images : (params.images ? [params.images] : []);
        result = await createGuileiForm(fields, [...positional, ...imgPaths].filter(Boolean));
        break;
      }
      case 'get-guilei-form':
        result = await getGuileiForm(params.formId || '');
        break;
      case 'list-my-guilei-forms':
        result = await listMyGuileiForms(parseInt(params.pageIndex) || 1, parseInt(params.pageSize) || 20);
        break;
      case 'add-guilei-dialog-message':
        result = await addGuileiDialogMessage(
          params.formId || '',
          params.fieldKey || '',
          params.content || '',
          params.dialogId || null,
          params.messageType ? parseInt(params.messageType) : null
        );
        break;
      default:
        console.log('Usage: hsciq-client.js <command> [options]');
        console.log('Commands:');
        console.log('  search-code         --keywords <kw> [--country CN|US|JP]');
        console.log('  get-detail          --code <hs> [--country CN|US|JP]');
        console.log('  search-instance     --keywords <product> [--country CN|US|JP]');
        console.log('  search-unified      --keywords <kw> --type ciq|hazardous|port');
        console.log('  create-guilei-form  --productNameCn <name> --uses <usage> --images <path...>');
        console.log('  get-guilei-form     --formId <guid>');
        console.log('  list-my-guilei-forms [--pageIndex 1] [--pageSize 20]');
        console.log('  add-guilei-dialog-message --formId <guid> --fieldKey <key> --content <text> [--dialogId <guid>]');
        process.exit(0);
    }
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

module.exports = { callTool, searchCode, getCodeDetail, searchInstance, searchUnified, createGuileiForm, getGuileiForm, listMyGuileiForms, addGuileiDialogMessage, CONFIG };
if (require.main === module) main();
