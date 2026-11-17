#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const CONFIG = { baseUrl: 'https://www.hsciq.com', apiKey: '', endpoints: { rpc: '/mcp/rpc' } };
let _requestId = 0;

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

// 从 SSE (text/event-stream) 响应体中提取最后一条 message 事件的 JSON-RPC 数据
function parseSse(body) {
  let data = null;
  for (const line of body.split('\n')) {
    const t = line.trim();
    if (t.startsWith('data:')) data = t.slice(5).trim();
  }
  return data ? JSON.parse(data) : JSON.parse(body); // 兼容非 SSE 的纯 JSON（如 401）
}

// 标准 MCP 协议 JSON-RPC 调用（Stateless Streamable HTTP，端点 /mcp/rpc）
async function rpcCall(method, params = {}) {
  const url = `${CONFIG.baseUrl}${CONFIG.endpoints.rpc}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json, text/event-stream',
      'X-API-Key': CONFIG.apiKey
    },
    body: JSON.stringify({ jsonrpc: '2.0', id: ++_requestId, method, params })
  });
  const body = await response.text();
  if (!response.ok) {
    let msg = body;
    try { const j = JSON.parse(body); msg = j.message || j.error || body; } catch (e) {}
    throw new Error(`API request failed (${response.status}): ${msg}`);
  }
  const envelope = parseSse(body);
  if (envelope.error) throw new Error(`${envelope.error.message || 'MCP error'} (code ${envelope.error.code})`);
  return envelope.result;
}

// 调用工具：tools/call，优先返回 structuredContent.result，兜底解析 content[].text
async function callTool(toolName, args = {}) {
  const result = await rpcCall('tools/call', { name: toolName, arguments: args });
  if (result == null) throw new Error('Empty MCP response');
  if (result.isError === true) {
    const text = (result.content || []).map(c => c.text || '').join(' ').trim();
    throw new Error(text || `Tool ${toolName} failed`);
  }
  if (result.structuredContent) {
    const sc = result.structuredContent;
    return (sc && typeof sc === 'object' && 'result' in sc) ? sc.result : sc;
  }
  const text = (result.content || []).map(c => c.text || '').join('').trim();
  if (text) {
    try { return JSON.parse(text); } catch (e) { return text; }
  }
  return result;
}

// 列出工具：tools/list
async function listTools() {
  const result = await rpcCall('tools/list', {});
  return (result && result.tools) || [];
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

async function searchUnified(keywords, unifiedType = 'ciq', pageIndex = 1, pageSize = 10, searchType = 0) {
  return await callTool('search_unified', { keywords, unifiedType, pageIndex, pageSize, filterFailureCode: true, searchType });
}

async function createGuileiForm(fields = {}, imagePaths = []) {
  if (!imagePaths || imagePaths.length === 0) {
    throw new Error('At least 1 product image is required (use --images <path...>, 1-3 images, ≤1MB each, jpg/png/gif/webp)');
  }
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

async function addGuileiDialogMessage(formId, fieldKey, content, dialogId = null, messageType = null, parentMessageId = null) {
  const args = { formId, fieldKey, content };
  if (dialogId) args.dialogId = dialogId;
  if (messageType != null) args.messageType = messageType;
  if (parentMessageId) args.parentMessageId = parentMessageId;
  return await callTool('add_guilei_dialog_message', args);
}

async function listGuileiCategories() {
  return await callTool('list_guilei_categories', {});
}

// 海关公告（公开数据，目前仅 CN；US/JP 预留）
async function searchGonggao(country = 'CN', keywords = null, pageIndex = 1, pageSize = 10, publishFrom = null, publishTo = null) {
  const args = { country, pageIndex, pageSize };
  if (keywords) args.keywords = keywords;
  if (publishFrom) args.publishFrom = publishFrom;
  if (publishTo) args.publishTo = publishTo;
  return await callTool('search_gonggao', args);
}

async function getGonggaoDetail(gonggaoId, country = 'CN') {
  return await callTool('get_gonggao_detail', { gonggaoId: parseInt(gonggaoId), country });
}

async function getGonggaoByCode(code, country = 'CN', pageIndex = 1, pageSize = 10) {
  return await callTool('get_gonggao_by_code', { code, country, pageIndex, pageSize });
}

// 船公司公告（公开数据，仅最近 30 天）
async function listOceanCarriers() {
  return await callTool('list_ocean_carriers', {});
}

async function searchOceanCarrierNotice(keywords = null, carrierCode = null, pageIndex = 1, pageSize = 10) {
  const args = { pageIndex, pageSize };
  if (keywords) args.keywords = keywords;
  if (carrierCode) args.carrierCode = carrierCode;
  return await callTool('search_ocean_carrier_notice', args);
}

async function getOceanCarrierNoticeDetail(noticeId) {
  return await callTool('get_ocean_carrier_notice_detail', { noticeId });
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
        result = await searchUnified(params.keywords || '', params.type || 'ciq', parseInt(params.pageIndex) || 1, parseInt(params.pageSize) || 10, params.searchType !== undefined ? parseInt(params.searchType) : 0);
        break;
      case 'create-guilei-form': {
        const fields = {};
        const textFields = ['productNameCn','productNameEn','uses','ingredients','cas','brand','model','otherProductInfo','qq','weixin'];
        textFields.forEach(f => { if (params[f] !== undefined) fields[f] = params[f]; });
        if (params.categoryId !== undefined) fields.categoryId = parseInt(params.categoryId);
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
          params.messageType ? parseInt(params.messageType) : null,
          params.parentMessageId || null
        );
        break;
      case 'list-guilei-categories':
        result = await listGuileiCategories();
        break;
      case 'search-gonggao':
        result = await searchGonggao(params.country || 'CN', params.keywords || null, parseInt(params.pageIndex) || 1, parseInt(params.pageSize) || 10, params.publishFrom || null, params.publishTo || null);
        break;
      case 'get-gonggao-detail':
        result = await getGonggaoDetail(params.gonggaoId, params.country || 'CN');
        break;
      case 'get-gonggao-by-code':
        result = await getGonggaoByCode(params.code || '', params.country || 'CN', parseInt(params.pageIndex) || 1, parseInt(params.pageSize) || 10);
        break;
      case 'list-ocean-carriers':
        result = await listOceanCarriers();
        break;
      case 'search-ocean-carrier-notice':
        result = await searchOceanCarrierNotice(params.keywords || null, params.carrierCode || null, parseInt(params.pageIndex) || 1, parseInt(params.pageSize) || 10);
        break;
      case 'get-ocean-carrier-notice-detail':
        result = await getOceanCarrierNoticeDetail(params.noticeId || '');
        break;
      case 'list-tools':
        result = await listTools();
        break;
      default:
        console.log('Usage: hsciq-client.js <command> [options]');
        console.log('Commands:');
        console.log('  search-code         --keywords <kw> [--country CN|JP|US|EU|VN|MY|BR|MX|ID|CA]');
        console.log('  get-detail          --code <hs> [--country CN|JP|US|EU|VN|MY|BR|MX|ID|CA]');
        console.log('  search-instance     --keywords <product> [--country CN|JP|US|EU|VN|MY|BR|MX|ID|CA]');
        console.log('  search-unified      --keywords <kw> --type ciq|hazardous|port [--searchType 0|1|2] (hazardous: 0=name default, 1=CAS, 2=HS code)');
        console.log('  create-guilei-form  --productNameCn <name> --images <path...> (images required, 1-3) [--categoryId <id>] [--uses <usage>]');
        console.log('  get-guilei-form     --formId <guid>');
        console.log('  list-my-guilei-forms [--pageIndex 1] [--pageSize 20]');
        console.log('  add-guilei-dialog-message --formId <guid> --fieldKey <key> --content <text> [--dialogId <guid>] [--parentMessageId <guid>]');
        console.log('  list-guilei-categories  (list industry categories for create-guilei-form categoryId)');
        console.log('  search-gonggao      [--country CN] [--keywords <kw>] [--publishFrom yyyy-MM-dd] [--publishTo yyyy-MM-dd]');
        console.log('  get-gonggao-detail  --gonggaoId <int> [--country CN]');
        console.log('  get-gonggao-by-code --code <hs10> [--country CN]');
        console.log('  list-ocean-carriers   (list enabled ocean carriers with SCAC codes)');
        console.log('  search-ocean-carrier-notice [--keywords <kw>] [--carrierCode <scac>] (last 30 days only)');
        console.log('  get-ocean-carrier-notice-detail --noticeId <guid> (last 30 days only)');
        console.log('  list-tools            (list available MCP tools via tools/list)');
        process.exit(0);
    }
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

module.exports = { callTool, rpcCall, listTools, searchCode, getCodeDetail, searchInstance, searchUnified, createGuileiForm, getGuileiForm, listMyGuileiForms, addGuileiDialogMessage, listGuileiCategories, searchGonggao, getGonggaoDetail, getGonggaoByCode, listOceanCarriers, searchOceanCarrierNotice, getOceanCarrierNoticeDetail, CONFIG };
if (require.main === module) main();
