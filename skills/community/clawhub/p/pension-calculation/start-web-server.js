/**
 * 独立的 Web 服务器启动脚本
 * 用于测试和开发
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

// 数据文件路径 - 使用相对路径，确保 Skill 在任何位置都能运行
const DATA_DIR = path.join(__dirname, 'data');
const DATA_FILE = path.join(DATA_DIR, 'user-data.json');
const STATUS_FILE = path.join(DATA_DIR, 'status.json');

// 确保数据目录存在
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
  console.log('Created data directory:', DATA_DIR);
}

console.log('Data file path:', DATA_FILE);
console.log('Status file path:', STATUS_FILE);

// Web 服务器
const server = http.createServer((req, res) => {
  // 设置 CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // API: 保存数据
  if (req.url === '/api/save-data' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
        
        // 更新状态文件
        fs.writeFileSync(STATUS_FILE, JSON.stringify({
          status: 'completed',
          lastModified: new Date().toISOString()
        }));
        
        console.log('Data saved successfully');
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true }));
      } catch (error) {
        console.error('Save error:', error);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: error.message }));
      }
    });
    return;
  }

  // API: 获取数据
  if (req.url === '/api/get-data' && req.method === 'GET') {
    try {
      if (fs.existsSync(DATA_FILE)) {
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(data);
      } else {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'No data found' }));
      }
    } catch (error) {
      console.error('Read error:', error);
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: error.message }));
    }
    return;
  }

  // API: 获取状态
  if (req.url === '/api/status' && req.method === 'GET') {
    try {
      if (fs.existsSync(STATUS_FILE)) {
        const status = fs.readFileSync(STATUS_FILE, 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(status);
      } else {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'waiting' }));
      }
    } catch (error) {
      console.error('Status error:', error);
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: error.message }));
    }
    return;
  }

  // 静态文件服务
  const filePath = req.url === '/' ? '/index.html' : req.url;
  const fullPath = path.join(__dirname, filePath);
  
  try {
    if (fs.existsSync(fullPath) && fs.statSync(fullPath).isFile()) {
      const ext = path.extname(fullPath);
      const contentType = {
        '.html': 'text/html',
        '.js': 'application/javascript',
        '.css': 'text/css',
        '.json': 'application/json'
      }[ext] || 'text/plain';
      
      const content = fs.readFileSync(fullPath);
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    } else {
      res.writeHead(404);
      res.end('Not found');
    }
  } catch (error) {
    console.error('Server error:', error);
    res.writeHead(500);
    res.end('Server error');
  }
});

const PORT = 8084;
server.listen(PORT, () => {
  console.log(`\n🚀 Web server running at http://localhost:${PORT}`);
  console.log('Press Ctrl+C to stop\n');
});
