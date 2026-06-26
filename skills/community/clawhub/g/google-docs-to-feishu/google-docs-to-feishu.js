#!/usr/bin/env node
/**
 * Google Docs → 飞书文档 同步工具
 * 
 * 功能：
 * 1. Google OAuth 2.0 授权
 * 2. 读取 Google Docs 内容
 * 3. 格式转换 (Google Docs blocks → Markdown)
 * 4. 创建飞书文档并写入
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const url = require('url');
const { execSync } = require('child_process');

// ============ 配置 ============
const CONFIG_DIR = path.join(process.env.HOME, '.config', 'google-docs-to-feishu');
const CREDENTIALS_PATH = path.join(CONFIG_DIR, 'credentials.json');
const TOKEN_PATH = path.join(CONFIG_DIR, 'token.json');

// Google OAuth 配置
const SCOPES = [
  'https://www.googleapis.com/auth/documents.readonly',
  'https://www.googleapis.com/auth/userinfo.profile',
  'https://www.googleapis.com/auth/userinfo.email'
];
const REDIRECT_URI = 'http://localhost:8765';
const TOKEN_DIR = path.join(CONFIG_DIR);

// ============ 工具函数 ============

/**
 * 确保配置目录存在
 */
function ensureConfigDir() {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }
}

/**
 * 读取 credentials 文件
 */
function loadCredentials() {
  ensureConfigDir();
  if (!fs.existsSync(CREDENTIALS_PATH)) {
    throw new Error(`凭证文件不存在: ${CREDENTIALS_PATH}\n请先下载 Google OAuth 客户端 JSON 文件并保存到该路径`);
  }
  const cred = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
  return {
    client_id: cred.client_id,
    client_secret: cred.client_secret,
    redirect_uris: cred.redirect_uris
  };
}

/**
 * 读取或刷新 token
 */
function loadToken() {
  if (fs.existsSync(TOKEN_PATH)) {
    return JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
  }
  return null;
}

/**
 * 保存 token
 */
function saveToken(token) {
  ensureConfigDir();
  fs.writeFileSync(TOKEN_PATH, JSON.stringify(token, null, 2));
}

/**
 * 发送 HTTP 请求
 */
function httpRequest(options, body = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve(data);
        }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

/**
 * 从 URL 中提取文档 ID
 */
function extractDocId(docUrl) {
  const match = docUrl.match(/\/document\/d\/([a-zA-Z0-9-_]+)/);
  if (!match) throw new Error('无效的 Google Docs URL');
  return match[1];
}

// ============ Google OAuth ============

/**
 * 生成授权 URL
 */
function generateAuthUrl(credentials) {
  const params = new url.URLSearchParams({
    client_id: credentials.client_id,
    redirect_uri: REDIRECT_URI,
    response_type: 'code',
    scope: SCOPES.join(' '),
    access_type: 'offline',
    prompt: 'consent'
  });
  return `https://accounts.google.com/o/oauth2/v2/auth?${params}`;
}

/**
 * 获取访问令牌
 */
async function getTokenFromCode(credentials, code) {
  return httpRequest({
    hostname: 'oauth2.googleapis.com',
    path: '/token',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  }, {
    client_id: credentials.client_id,
    client_secret: credentials.client_secret,
    code,
    redirect_uri: REDIRECT_URI,
    grant_type: 'authorization_code'
  });
}

/**
 * 刷新访问令牌
 */
async function refreshAccessToken(credentials, refresh_token) {
  return httpRequest({
    hostname: 'oauth2.googleapis.com',
    path: '/token',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  }, {
    client_id: credentials.client_id,
    client_secret: credentials.client_secret,
    refresh_token,
    grant_type: 'refresh_token'
  });
}

/**
 * 检查并刷新 token
 */
async function ensureValidToken(credentials) {
  let token = loadToken();
  
  if (!token) {
    throw new Error('未授权，请先运行授权流程');
  }
  
  // 检查是否即将过期（提前5分钟）
  const expiresAt = token.expiry_date || (token.created_at + token.expires_in * 1000);
  if (Date.now() >= expiresAt - 5 * 60 * 1000) {
    console.log('Token 即将过期，刷新中...');
    const newToken = await refreshAccessToken(credentials, token.refresh_token);
    token = {
      ...token,
      ...newToken,
      created_at: Date.now()
    };
    saveToken(token);
    console.log('Token 刷新成功');
  }
  
  return token;
}

/**
 * 启动本地授权服务器
 */
function startAuthServer(credentials) {
  return new Promise((resolve, reject) => {
    const server = http.createServer(async (req, res) => {
      const query = new url.URL(req.url, REDIRECT_URI);
      
      if (query.pathname === '/favicon.ico') {
        res.writeHead(204);
        res.end();
        return;
      }
      
      const code = query.get('code');
      const error = query.get('error');
      
      if (error) {
        res.writeHead(400, { 'Content-Type': 'text/html' });
        res.end('<html><body><h1>授权失败</h1><p>请关闭此窗口并重试。</p></body></html>');
        server.close();
        reject(new Error(`授权被拒绝: ${error}`));
        return;
      }
      
      if (code) {
        try {
          console.log('正在获取访问令牌...');
          const token = await getTokenFromCode(credentials, code);
          token.created_at = Date.now();
          token.expiry_date = Date.now() + token.expires_in * 1000;
          saveToken(token);
          
          res.writeHead(200, { 'Content-Type': 'text/html' });
          res.end('<html><body><h1>授权成功！</h1><p>可以关闭此窗口了。</p></body></html>');
          server.close();
          resolve();
        } catch (e) {
          res.writeHead(500, { 'Content-Type': 'text/html' });
          res.end('<html><body><h1>错误</h1><p>获取令牌失败: ' + e.message + '</p></body></html>');
          server.close();
          reject(e);
        }
      }
    });
    
    server.listen(8765, () => {
      console.log('授权服务器已启动');
    });
    
    server.on('error', reject);
  });
}

// ============ Google Docs API ============

/**
 * 读取 Google 文档内容
 */
async function getGoogleDocContent(credentials, docId) {
  const token = await ensureValidToken(credentials);
  
  const docResponse = await httpRequest({
    hostname: 'docs.googleapis.com',
    path: `/v1/documents/${docId}`,
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token.access_token}` }
  });
  
  // 获取文档标题
  const title = docResponse.title || 'Untitled';
  
  // 转换内容为 Markdown
  const markdown = convertToMarkdown(docResponse);
  
  return { title, markdown, raw: docResponse };
}

/**
 * 将 Google Docs 结构转换为 Markdown
 */
function convertToMarkdown(doc) {
  const lines = [];
  
  if (!doc.body || !doc.body.content) {
    return '';
  }
  
  for (const block of doc.body.content) {
    const text = convertBlock(block);
    if (text) {
      lines.push(text);
    }
  }
  
  return lines.join('\n\n');
}

/**
 * 转换单个 block
 */
function convertBlock(block) {
  const type = block.type;
  
  switch (type) {
    case 'paragraph':
      return convertParagraph(block.paragraph);
    case 'heading1':
      return '# ' + getBlockText(block.heading1);
    case 'heading2':
      return '## ' + getBlockText(block.heading2);
    case 'heading3':
      return '### ' + getBlockText(block.heading3);
    case 'heading4':
      return '#### ' + getBlockText(block.heading4);
    case 'heading5':
      return '##### ' + getBlockText(block.heading5);
    case 'heading6':
      return '###### ' + getBlockText(block.heading6);
    case 'bulletList':
      return convertList(block.bulletList, '•');
    case 'orderedList':
      return convertList(block.orderedList, '1.');
    case 'table':
      return convertTable(block.table);
    case 'codeBlock':
      return '```\n' + getBlockText(block.codeBlock) + '\n```';
    case 'quote':
      return '> ' + getBlockText(block.quote);
    case 'image':
      return convertImage(block.image);
    case 'horizontalRule':
      return '---';
    default:
      // 未知类型，尝试提取文本
      if (block.paragraph) {
        return convertParagraph(block.paragraph);
      }
      return null;
  }
}

/**
 * 转换段落
 */
function convertParagraph(para) {
  if (!para || !para.elements) return null;
  
  const text = para.elements.map(elem => {
    const content = elem.textRun || elem.inlineObjectElement;
    if (!content) return '';
    
    let text = content.content || '';
    
    // 处理文本样式
    if (elem.textRun && elem.textRun.textStyle) {
      const style = elem.textRun.textStyle;
      if (style.bold) text = `**${text}**`;
      if (style.italic) text = `*${text}*`;
      if (style.underline) text = `<u>${text}</u>`;
      if (style.strikethrough) text = `~~${text}~~`;
      if (style.link) text = `[${text}](${style.link.url})`;
      if (style.code) text = `\`${text}\``;
    }
    
    return text;
  }).join('');
  
  return text.trim() || null;
}

/**
 * 获取 block 中的纯文本
 */
function getBlockText(block) {
  if (!block || !block.elements) return '';
  
  return block.elements.map(elem => {
    const textRun = elem.textRun;
    return textRun ? textRun.content : '';
  }).join('').trim();
}

/**
 * 转换列表
 */
function convertList(list, marker) {
  if (!list || !list.listItems) return null;
  
  return list.listItems.map((item, idx) => {
    const prefix = marker === '1.' ? `${idx + 1}.` : marker;
    const text = getBlockText(item.paragraph || item);
    return `${prefix} ${text}`;
  }).join('\n');
}

/**
 * 转换表格
 */
function convertTable(table) {
  if (!table || !table.tableRows) return null;
  
  const rows = table.tableRows.map(row => {
    if (!row.tableCells) return '';
    const cells = row.tableCells.map(cell => {
      const text = getBlockText(cell.content?.[0]?.paragraph);
      return text || '';
    });
    return `| ${cells.join(' | ')} |`;
  });
  
  if (rows.length < 2) return rows.join('\n');
  
  // 添加表头分隔符
  const separator = '| ' + rows[0].split('|').slice(1, -1).map(() => '---').join(' | ') + ' |';
  
  return [rows[0], separator, ...rows.slice(1)].join('\n');
}

/**
 * 转换图片
 */
function convertImage(image) {
  // Google Docs API 返回的图片是 contentBlob URL
  const contentUrl = image.contentUri || image.uri;
  if (contentUrl) {
    return `![](${contentUrl})`;
  }
  return '';
}

// ============ 飞书文档写入 ============

/**
 * 调用飞书 API 创建文档
 */
async function createFeishuDoc(title, folderToken = null, ownerOpenId = null) {
  const feishuTool = 'feishu_doc';
  
  // 构建创建参数
  const params = { action: 'create', title };
  if (folderToken) params.folder_token = folderToken;
  if (ownerOpenId) params.owner_open_id = ownerOpenId;
  
  // 这里通过 OpenClaw 的 tool calling 机制调用
  // 实际实现需要通过 exec 或其他方式调用
  
  // 简化：直接通过 curl 调用飞书 API
  // 但更推荐使用 OpenClaw 内置的 feishu_doc tool
  
  // 使用 node 调用
  const createCmd = `
    openclaw tools call feishu_doc '{"action":"create","title":"${title}"${folderToken ? `,"folder_token":"${folderToken}"` : ''}${ownerOpenId ? `,"owner_open_id":"${ownerOpenId}"` : ''}}'
  `;
  
  try {
    const result = execSync(createCmd, { encoding: 'utf8' });
    return JSON.parse(result);
  } catch (e) {
    // 尝试直接调用
    return createFeishuDocByAPI(title, folderToken, ownerOpenId);
  }
}

/**
 * 直接通过飞书 API 创建文档
 */
async function createFeishuDocByAPI(title, folderToken, ownerOpenId) {
  // 读取飞书 bot token
  const feishuConfigPath = path.join(process.env.HOME, '.openclaw', 'channels', 'feishu', 'config.json');
  let accessToken = '自动获取'; // OpenClaw 会自动管理 token
  
  // 构建请求体
  const body = {
    title: title
  };
  
  if (folderToken) {
    body.folder_token = folderToken;
  }
  
  // 这里需要通过 OpenClaw 的飞书集成来获取 token
  // 简化处理，返回一个提示
  console.log('请使用 feishu-doc skill 创建文档');
  return { title };
}

// ============ 主流程 ============

/**
 * 授权流程
 */
async function authorize() {
  console.log('开始 Google 授权流程...\n');
  
  const credentials = loadCredentials();
  const authUrl = generateAuthUrl(credentials);
  
  console.log('请在浏览器中打开以下链接完成授权:\n');
  console.log(authUrl);
  console.log();
  
  // 自动打开浏览器
  const openCmd = process.platform === 'darwin' ? 'open' : 'xdg-open';
  try {
    execSync(`${openCmd} "${authUrl}"`);
    console.log('已自动打开浏览器');
  } catch (e) {
    console.log('请手动复制链接到浏览器');
  }
  
  await startAuthServer(credentials);
  console.log('\n✅ 授权成功！Token 已保存。');
}

/**
 * 同步文档
 */
async function syncDoc(googleDocUrl, feishuFolderToken = null, feishuOwnerOpenId = null) {
  console.log('开始同步文档...\n');
  
  const credentials = loadCredentials();
  const docId = extractDocId(googleDocUrl);
  
  console.log(`📄 读取 Google Docs: ${docId}`);
  const { title, markdown } = await getGoogleDocContent(credentials, docId);
  console.log(`✅ 读取成功: ${title}\n`);
  
  console.log('📝 创建飞书文档...');
  // 调用 feishu-doc 创建文档
  const feishuResult = await createFeishuDoc(title, feishuFolderToken, feishuOwnerOpenId);
  
  if (feishuResult && feishuResult.doc_token) {
    console.log(`✅ 飞书文档已创建: ${feishuResult.doc_token}`);
    
    // 写入内容
    console.log('📤 写入内容...');
    const writeCmd = `openclaw tools call feishu_doc '{"action":"write","doc_token":"${feishuResult.doc_token}","content":${JSON.stringify(markdown)}}'`;
    execSync(writeCmd, { encoding: 'utf8' });
    
    console.log('✅ 同步完成！');
    return {
      success: true,
      feishu_doc_token: feishuResult.doc_token,
      title: title
    };
  }
  
  return { success: false, error: '创建飞书文档失败' };
}

// ============ CLI 入口 ============

const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'authorize':
    authorize().catch(e => {
      console.error('授权失败:', e.message);
      process.exit(1);
    });
    break;
    
  case 'sync':
    const docUrl = args[1];
    const folderToken = args[2] || null;
    const ownerOpenId = args[3] || null;
    
    if (!docUrl) {
      console.error('用法: sync <google-doc-url> [feishu-folder-token] [feishu-owner-open-id]');
      process.exit(1);
    }
    
    syncDoc(docUrl, folderToken, ownerOpenId)
      .then(result => {
        console.log('\n📋 结果:', JSON.stringify(result, null, 2));
      })
      .catch(e => {
        console.error('同步失败:', e.message);
        process.exit(1);
      });
    break;
    
  case 'help':
  default:
    console.log(`
Google Docs → 飞书文档 同步工具

用法:
  node google-docs-to-feishu.js authorize     授权 Google 账号
  node google-docs-to-feishu.js sync <url> [folder-token] [owner-open-id]  同步文档

示例:
  node google-docs-to-feishu.js authorize
  node google-docs-to-feishu.js sync "https://docs.google.com/document/d/XXX/edit"
  node google-docs-to-feishu.js sync "https://docs.google.com/document/d/XXX/edit" "fldcnXXX"
    `);
}
