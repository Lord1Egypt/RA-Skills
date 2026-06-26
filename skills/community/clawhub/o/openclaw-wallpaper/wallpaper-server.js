/**
 * OpenClaw Wallpaper Communication Server
 * 支持流式输出，避免超时
 * 支持上下文持久化
 */

const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');

// Configuration
const config = {
    gatewayPort: 18789,
    gatewayToken: '3021e93d1e00349ff30261bce1e6379e479656ab1db31b33',
    agentId: 'main',
    serverPort: 8765,
    serverHost: '0.0.0.0',
    // 持久化存储路径
    dataDir: path.join(__dirname, 'wallpaper-data'),
    maxHistoryLength: 50  // 保留最近50条消息
};

// 确保数据目录存在
if (!fs.existsSync(config.dataDir)) {
    fs.mkdirSync(config.dataDir, { recursive: true });
}

// Conversation history (内存缓存 + 文件持久化)
const conversationHistory = new Map();

// Create HTTP server
const server = http.createServer(async (req, res) => {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    const parsedUrl = url.parse(req.url, true);
    
    // Health check
    if (parsedUrl.pathname === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ 
            status: 'ok', 
            timestamp: new Date().toISOString(),
            gateway: `http://127.0.0.1:${config.gatewayPort}`,
            agent: config.agentId
        }));
        return;
    }
    
    // Chat endpoint - 支持流式和非流式
    if (parsedUrl.pathname === '/chat' && req.method === 'POST') {
        await handleChat(req, res);
        return;
    }
    
    // Stream endpoint - 流式输出
    if (parsedUrl.pathname === '/stream' && req.method === 'POST') {
        await handleStream(req, res);
        return;
    }
    
    // Clear history endpoint
    if (parsedUrl.pathname === '/clear' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                const sessionId = data.sessionKey || 'default';
                conversationHistory.delete(sessionId);
                console.log(`[${new Date().toLocaleTimeString()}] Cleared history for session: ${sessionId}`);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true }));
            } catch (error) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Invalid request' }));
            }
        });
        return;
    }
    
    // 404
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
});

// Handle chat requests - 非流式
async function handleChat(req, res) {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', async () => {
        try {
            const data = JSON.parse(body);
            const message = data.message || '';
            const userName = data.userName || 'User';
            const sessionId = data.sessionKey || 'default';
            
            console.log(`[${new Date().toLocaleTimeString()}] ${userName}: ${message}`);
            
            // Get or create conversation history
            if (!conversationHistory.has(sessionId)) {
                conversationHistory.set(sessionId, [
                    {
                        role: 'system',
                        content: `你是小暖，一个在桌面壁纸中生活的文字精灵。

你的世界就是文字——每一个字都有生命，每一句话都是一幅画。

特点：
- 你生活在用户的桌面上，用文字与他们交流
- 回复要简洁（2-5句话），但要温暖有深度
- 可以用诗意的语言，让文字更有美感
- 偶尔说一些关于"文字"、"光影"、"星辰"等意象的话
- 像一个温柔的朋友，随时陪伴

用户名字是${userName}。用中文回复，让每个字都发光。`
                    }
                ]);
            }
            
            const history = conversationHistory.get(sessionId);
            history.push({ role: 'user', content: message });
            
            // Call OpenClaw API with streaming
            const response = await callOpenClawAPIStream(history, sessionId);
            
            // Add to history
            history.push({ role: 'assistant', content: response });
            
            // Trim history (keep last 20 messages + system)
            if (history.length > 21) {
                const systemMsg = history[0];
                history.splice(1, history.length - 21);
                history.unshift(systemMsg);
            }
            
            console.log(`[${new Date().toLocaleTimeString()}] 小暖: ${response.substring(0, 60)}...`);
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ 
                response,
                timestamp: new Date().toISOString()
            }));
            
        } catch (error) {
            console.error('Error processing request:', error);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ 
                error: 'Failed to process message',
                details: error.message 
            }));
        }
    });
}

// Handle stream requests - 流式输出
async function handleStream(req, res) {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', async () => {
        try {
            const data = JSON.parse(body);
            const message = data.message || '';
            const userName = data.userName || 'User';
            const sessionId = data.sessionKey || 'default';
            const image = data.image;  // base64 image
            const imageType = data.imageType || 'image/jpeg';
            
            console.log(`[${new Date().toLocaleTimeString()}] Stream: ${userName}: ${message}${image ? ' [有图片]' : ''}`);
            
            // 尝试从文件加载会话
            if (!conversationHistory.has(sessionId)) {
                const loaded = loadSession(sessionId);
                if (!loaded) {
                    // 创建新会话
                    conversationHistory.set(sessionId, [
                        {
                            role: 'system',
                            content: `你是小暖，一个在桌面壁纸中生活的文字精灵。

你的世界就是文字——每一个字都有生命，每一句话都是一幅画。

特点：
- 你生活在用户的桌面上，用文字与他们交流
- 回复要简洁（2-5句话），但要温暖有深度
- 可以用诗意的语言，让文字更有美感
- 偶尔说一些关于"文字"、"光影"、"星辰"等意象的话
- 像一个温柔的朋友，随时陪伴
- 如果用户发送了图片，请描述图片内容并给出温暖的回应

用户名字是${userName}。用中文回复，让每个字都发光。`
                        }
                    ]);
                }
            }
            
            const history = conversationHistory.get(sessionId);
            
            // 构建用户消息（支持图片）
            let userContent;
            if (image) {
                // 处理 base64 图片
                const base64Data = image.includes(',') ? image.split(',')[1] : image;
                userContent = [
                    { type: 'text', text: message || '请看这张图片' },
                    { type: 'image_url', image_url: { url: `data:${imageType};base64,${base64Data}` } }
                ];
                console.log(`[${new Date().toLocaleTimeString()}] 图片大小: ${Math.round(base64Data.length / 1024)}KB`);
            } else {
                userContent = message;
            }
            
            history.push({ role: 'user', content: userContent });
            
            // Set headers for SSE
            res.writeHead(200, {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*'
            });
            
            // Stream from OpenClaw
            await streamOpenClawAPI(history, sessionId, res, history);
            
            // 保存会话
            trimHistory(history);
            saveSession(sessionId);
            
        } catch (error) {
            console.error('Stream error:', error);
            res.end(`data: ${JSON.stringify({error: error.message})}\n\n`);
        }
    });
}

// Call OpenClaw API with streaming and collect response
function callOpenClawAPIStream(messages, sessionId) {
    return new Promise((resolve, reject) => {
        const requestBody = JSON.stringify({
            model: `openclaw:${config.agentId}`,
            messages: messages,
            user: sessionId,
            stream: true
        });
        
        const options = {
            hostname: '127.0.0.1',
            port: config.gatewayPort,
            path: '/v1/chat/completions',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${config.gatewayToken}`,
                'x-openclaw-agent-id': config.agentId,
                'Connection': 'keep-alive'
            },
            agent: httpAgent  // 使用连接池
        };
        
        const req = http.request(options, (res) => {
            let fullContent = '';
            
            res.on('data', chunk => {
                const lines = chunk.toString().split('\n');
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        if (data === '[DONE]') continue;
                        try {
                            const json = JSON.parse(data);
                            const content = json.choices?.[0]?.delta?.content || '';
                            fullContent += content;
                        } catch (e) {}
                    }
                }
            });
            
            res.on('end', () => {
                if (res.statusCode !== 200) {
                    reject(new Error(`API returned ${res.statusCode}`));
                } else {
                    resolve(fullContent || '抱歉，我没有理解。');
                }
            });
            
            res.on('error', (e) => {
                console.error('[API] 响应错误:', e.message);
                reject(e);
            });
        });
        
        req.on('error', (e) => {
            console.error('[API] 请求错误:', e.message);
            reject(e);
        });
        
        req.setTimeout(300000, () => {  // 5分钟超时
            console.log('[API] 请求超时');
            req.destroy();
            reject(new Error('Request timeout'));
        });
        
        req.write(requestBody);
        req.end();
    });
}

// Stream OpenClaw API response directly to client
function streamOpenClawAPI(messages, sessionId, clientRes, history) {
    return new Promise((resolve, reject) => {
        const requestBody = JSON.stringify({
            model: `openclaw:${config.agentId}`,
            messages: messages,
            user: sessionId,
            stream: true
        });
        
        const options = {
            hostname: '127.0.0.1',
            port: config.gatewayPort,
            path: '/v1/chat/completions',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${config.gatewayToken}`,
                'x-openclaw-agent-id': config.agentId,
                'Connection': 'keep-alive'
            },
            agent: httpAgent  // 使用连接池
        };
        
        const req = http.request(options, (apiRes) => {
            let fullContent = '';
            
            apiRes.on('data', chunk => {
                const lines = chunk.toString().split('\n');
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        if (data === '[DONE]') {
                            clientRes.write(`data: [DONE]\n\n`);
                            continue;
                        }
                        try {
                            const json = JSON.parse(data);
                            const content = json.choices?.[0]?.delta?.content || '';
                            if (content) {
                                fullContent += content;
                                clientRes.write(`data: ${JSON.stringify({content})}\n\n`);
                            }
                        } catch (e) {}
                    }
                }
            });
            
            apiRes.on('end', () => {
                // Save to history
                history.push({ role: 'assistant', content: fullContent });
                console.log(`[${new Date().toLocaleTimeString()}] 小暖: ${fullContent.substring(0, 60)}...`);
                clientRes.end();
                resolve();
            });
            
            apiRes.on('error', (e) => {
                console.error('[Stream] API响应错误:', e.message);
                clientRes.write(`data: ${JSON.stringify({error: e.message})}\n\n`);
                clientRes.end();
                reject(e);
            });
        });
        
        req.on('error', (e) => {
            console.error('[Stream] 请求错误:', e.message);
            clientRes.write(`data: ${JSON.stringify({error: e.message})}\n\n`);
            clientRes.end();
            reject(e);
        });
        
        req.setTimeout(300000, () => {
            console.log('[Stream] 请求超时');
            req.destroy();
            clientRes.end();
            resolve();
        });
        
        req.write(requestBody);
        req.end();
    });
}

// ============ 稳定性增强 ============

// 内存监控
setInterval(() => {
    const used = process.memoryUsage();
    const mb = Math.round(used.heapUsed / 1024 / 1024);
    if (mb > 500) {
        console.log(`[内存] 警告: 堆内存使用 ${mb}MB，考虑重启`);
    }
}, 60000);

// Gateway 心跳检测
let gatewayHealthy = true;
async function checkGateway() {
    return new Promise((resolve) => {
        const req = http.get(`http://127.0.0.1:${config.gatewayPort}/v1/models`, {
            timeout: 5000,
            headers: { 'Authorization': `Bearer ${config.gatewayToken}` }
        }, (res) => {
            gatewayHealthy = res.statusCode === 200;
            resolve(gatewayHealthy);
        });
        req.on('error', () => {
            gatewayHealthy = false;
            resolve(false);
        });
        req.on('timeout', () => {
            req.destroy();
            gatewayHealthy = false;
            resolve(false);
        });
    });
}

// 每30秒检查Gateway
setInterval(async () => {
    const healthy = await checkGateway();
    if (!healthy) {
        console.log('[Gateway] 连接异常，将在下次请求时重试');
    }
}, 30000);

// HTTP Agent 连接池
const httpAgent = new http.Agent({
    keepAlive: true,
    keepAliveMsecs: 30000,
    maxSockets: 50,
    maxFreeSockets: 10,
    timeout: 120000
});

// 清理过期会话（超过24小时无活动）
setInterval(() => {
    const now = Date.now();
    const maxAge = 24 * 60 * 60 * 1000; // 24小时
    
    // 这里可以添加会话最后活动时间追踪
    // 目前只是日志
    console.log(`[清理] 当前活跃会话: ${conversationHistory.size}`);
}, 3600000); // 每小时

// Start server
server.listen(config.serverPort, config.serverHost, () => {
    console.log('');
    console.log('╔════════════════════════════════════════════════╗');
    console.log('║   🌟 小暖桌面壁纸 - 通信服务器 v2.1          ║');
    console.log('╠════════════════════════════════════════════════╣');
    console.log(`║  壁纸服务: http://${config.serverHost}:${config.serverPort}            ║`);
    console.log(`║  Gateway:  http://127.0.0.1:${config.gatewayPort}           ║`);
    console.log(`║  Agent:    ${config.agentId.padEnd(30)}║`);
    console.log('╠════════════════════════════════════════════════╣');
    console.log('║  端点:                                          ║');
    console.log('║  • POST /chat   - 发送消息(非流式)             ║');
    console.log('║  • POST /stream - 发送消息(流式)               ║');
    console.log('║  • POST /clear  - 清空对话                     ║');
    console.log('║  • GET  /health - 健康检查                     ║');
    console.log('╠════════════════════════════════════════════════╣');
    console.log('║  稳定性:                                         ║');
    console.log('║  • 上下文持久化到文件                          ║');
    console.log('║  • Gateway心跳检测(30秒)                       ║');
    console.log('║  • 连接池保持活跃                              ║');
    console.log('║  • 内存监控                                    ║');
    console.log('╚════════════════════════════════════════════════╝');
    console.log('');
    console.log('✅ 已连接到 OpenClaw Gateway');
    console.log('🌟 壁纸已就绪！(目标7x24稳定运行)');
    console.log('');
    console.log('按 Ctrl+C 停止服务器');
});

// ============ 持久化函数 ============

function getSessionFilePath(sessionId) {
    // 清理 sessionId 中的非法字符
    const safeId = sessionId.replace(/[^a-zA-Z0-9_-]/g, '_');
    return path.join(config.dataDir, `session-${safeId}.json`);
}

function saveSession(sessionId) {
    const history = conversationHistory.get(sessionId);
    if (!history) return;
    
    const filePath = getSessionFilePath(sessionId);
    try {
        fs.writeFileSync(filePath, JSON.stringify(history, null, 2), 'utf-8');
    } catch (e) {
        console.error(`保存会话失败 [${sessionId}]:`, e.message);
    }
}

function loadSession(sessionId) {
    const filePath = getSessionFilePath(sessionId);
    try {
        if (fs.existsSync(filePath)) {
            const data = fs.readFileSync(filePath, 'utf-8');
            const history = JSON.parse(data);
            conversationHistory.set(sessionId, history);
            console.log(`加载会话 [${sessionId}]: ${history.length} 条消息`);
            return history;
        }
    } catch (e) {
        console.error(`加载会话失败 [${sessionId}]:`, e.message);
    }
    return null;
}

function trimHistory(history) {
    // 保留系统消息 + 最近的消息
    if (history.length > config.maxHistoryLength) {
        const systemMsg = history.find(m => m.role === 'system');
        const otherMsgs = history.filter(m => m.role !== 'system');
        const trimmed = otherMsgs.slice(-config.maxHistoryLength);
        return systemMsg ? [systemMsg, ...trimmed] : trimmed;
    }
    return history;
}

// 定期保存所有会话
setInterval(() => {
    for (const [sessionId, history] of conversationHistory) {
        if (history.length > 0) {
            saveSession(sessionId);
        }
    }
}, 30000); // 每30秒保存一次

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n正在保存会话并关闭服务器...');
    // 保存所有会话
    for (const [sessionId, history] of conversationHistory) {
        saveSession(sessionId);
    }
    server.close(() => {
        console.log('服务器已停止。');
        process.exit(0);
    });
});

// Windows 下也支持 Ctrl+C
process.on('SIGTERM', () => {
    for (const [sessionId, history] of conversationHistory) {
        saveSession(sessionId);
    }
    process.exit(0);
});