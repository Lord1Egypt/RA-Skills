const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;
const DIR = 'C:\\Users\\23622\\Documents\\Lively Wallpapers\\OpenClawChat';

const MIME = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json'
};

const server = http.createServer((req, res) => {
    let file = req.url === '/' ? '/index.html' : req.url;
    const filePath = DIR + file;
    const ext = path.extname(filePath);
    
    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404);
            res.end('Not found');
            return;
        }
        res.writeHead(200, { 'Content-Type': MIME[ext] || 'text/plain' });
        res.end(data);
    });
});

server.listen(PORT, () => console.log(`UI服务器: http://localhost:${PORT}`));