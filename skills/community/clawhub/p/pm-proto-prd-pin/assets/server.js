/**
 * pm-proto-prd-pin 本地零依赖服务。
 * 启动：node server.js
 * 地址：http://localhost:3000
 *
 * 接口：
 *   GET  /api/get-all-prd  返回全量注册表
 *   POST /api/save-prd     写入页面专属数据文件（双常量结构）
 *
 * 本文件不读取、不保存任何密钥。写入操作仅限本地磁盘。
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const BASE_DIR = __dirname;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf'
};

function sendJson(res, status, payload) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(payload));
}

function safeName(name) {
  return String(name).replace(/\.html$/i, '').replace(/^prd-data-/, '').replace(/[^a-zA-Z0-9_-]/g, '_');
}

function buildDataFile(htmlName, pins, versionRegistry) {
  const arr = JSON.stringify(pins || [], null, 2);
  const registry = versionRegistry && typeof versionRegistry === 'object'
    ? JSON.stringify(versionRegistry, null, 2)
    : JSON.stringify({ activeVersion: 'v1.0.0', versions: { 'v1.0.0': pins || [] } }, null, 2);
  return `/**
 * ${htmlName} 专属 PRD 规格数据。
 * 本地持久化写入。PAGE_PRD_DATA 与 PRD_VERSION_REGISTRY 双常量同源。
 */
window.PAGE_PRD_DATA = window.PAGE_PRD_DATA || {};
window.PAGE_PRD_DATA["${htmlName}"] = ${arr};
window.INITIAL_PRD_DATA = window.PAGE_PRD_DATA["${htmlName}"];
window.PRD_VERSION_REGISTRY = ${registry};
`;
}

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const parsed = new URL(req.url, `http://${req.headers.host}`);
  const pathname = decodeURIComponent(parsed.pathname);

  if (pathname === '/api/save-prd' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const payload = JSON.parse(body);
        if (!payload.page) {
          sendJson(res, 400, { success: false, error: '缺少 page 标识' });
          return;
        }
        const jsDir = path.join(BASE_DIR, 'assets', 'js');
        fs.mkdirSync(jsDir, { recursive: true });
        const clean = safeName(payload.page);
        const htmlName = clean + '.html';
        const file = path.join(jsDir, `prd-data-${clean}.js`);
        fs.writeFileSync(file, buildDataFile(htmlName, payload.data, payload.versionRegistry), 'utf-8');

        if (payload.allData && typeof payload.allData === 'object') {
          fs.writeFileSync(path.join(jsDir, 'prd-data-all.json'), JSON.stringify(payload.allData, null, 2), 'utf-8');
        }
        console.log(`[PRD] 已写入 assets/js/prd-data-${clean}.js`);
        sendJson(res, 200, { success: true, timestamp: Date.now() });
      } catch (err) {
        console.error('[PRD] 保存失败', err);
        sendJson(res, 500, { success: false, error: err.message });
      }
    });
    return;
  }

  if (pathname === '/api/get-all-prd' && req.method === 'GET') {
    const all = path.join(BASE_DIR, 'assets', 'js', 'prd-data-all.json');
    if (fs.existsSync(all)) {
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      fs.createReadStream(all).pipe(res);
    } else {
      sendJson(res, 200, {});
    }
    return;
  }

  let relative = pathname === '/' || pathname === '' ? '/index.html' : pathname;
  const filePath = path.join(BASE_DIR, relative);
  if (!filePath.startsWith(BASE_DIR)) {
    res.writeHead(403);
    res.end('Access Denied');
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found: ' + pathname);
      return;
    }
    res.writeHead(200, { 'Content-Type': MIME_TYPES[path.extname(filePath).toLowerCase()] || 'application/octet-stream' });
    fs.createReadStream(filePath).pipe(res);
  });
});

server.listen(PORT, () => {
  console.log('====================================================');
  console.log(`PRD 本地服务已启动: http://localhost:${PORT}`);
  console.log(`静态根目录: ${BASE_DIR}`);
  console.log('本服务不处理任何密钥。');
  console.log('====================================================');
});
