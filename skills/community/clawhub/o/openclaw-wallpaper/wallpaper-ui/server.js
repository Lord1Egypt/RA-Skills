// 简单的测试服务器
const http = require('http');
const url = require('url');

const PORT = 8765;

const responses = [
    '收到！有什么想继续聊的吗？',
    '嗯，我在听。',
    '这个话题很有意思。',
    '你说得对，我也这么觉得。',
    '让我想想...嗯，这确实值得深思。',
    '感谢分享，我会记住的。',
    '这是一个很棒的想法！',
    '我们继续聊吧？',
    '有道理。',
    '我理解你的感受。'
];

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const path = parsedUrl.pathname;
    
    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    if (path === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ok' }));
        return;
    }
    
    if (path === '/chat' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                const response = responses[Math.floor(Math.random() * responses.length)];
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ response }));
            } catch (e) {
                res.writeHead(400);
                res.end('Bad request');
            }
        });
        return;
    }
    
    if (path === '/clear' && req.method === 'POST') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'cleared' }));
        return;
    }
    
    res.writeHead(404);
    res.end('Not found');
});

server.listen(PORT, () => {
    console.log(`测试服务器运行在 http://127.0.0.1:${PORT}`);
    console.log('接口: /health, /chat (POST), /clear (POST)');
});