// 小暖文字世界 v13 - 桌面壁纸版 流式输出 + 改进重连

const config = {
    apiUrl: 'http://127.0.0.1:8765/chat',
    streamUrl: 'http://127.0.0.1:8765/stream',
    healthUrl: 'http://127.0.0.1:8765/health',
    clearUrl: 'http://127.0.0.1:8765/clear',
    sessionKey: 'wallpaper-main',
    userName: 'User'
};

let state = {
    connected: false,
    typing: false,
    count: 0,
    achievements: new Set(),
    startTime: null,
    selectedImage: null,
    lastError: null,
    reconnectAttempts: 0
};

// 发光字符分类
const glowChars = {
    heart: ['心', '爱', '情', '暖', '温', '亲'],
    star: ['星', '光', '梦', '辉', '明', '亮'],
    nature: ['花', '树', '山', '风', '雨', '雪', '草', '叶'],
    water: ['水', '海', '河', '波', '浪', '泉'],
    sword: ['剑', '刀', '锋', '刃', '武'],
    dragon: ['龙', '麟', '爪', '鳞', '飞'],
    sun: ['日', '曦', '晨', '阳', '光'],
    moon: ['月', '夜', '影', '晚', '辉']
};

// 12个成就 - 每个用对应字组成清晰图案
const achievements = {
    meet: {
        name: '相遇',
        desc: '第一次对话',
        art: `
　　　相
　相相相相相
　　相　相
　　相　相
　相相相相相`
    },
    chat5: {
        name: '话匣子',
        desc: '对话5次',
        art: `
话话话话话话
话　　　　　话
话　　　　　话
话话话话话话
话`
    },
    chat10: {
        name: '谈天说地',
        desc: '对话10次',
        art: `
　谈谈谈谈谈
谈　　　　　谈
谈　　　　　谈
　谈谈谈谈谈
　　　谈`
    },
    chat20: {
        name: '知音',
        desc: '对话20次',
        art: `
知　　知
知　　知
知　　知
　知知知知`
    },
    star: {
        name: '星辰',
        desc: '提到星辰',
        art: `
　　　　　星
　　　　星星星
　　　　　星
　　　星星星星星
　　星星星星星星星`
    },
    heart: {
        name: '暖心',
        desc: '提到心意',
        art: `
　心　　　心
心心心　心心心
心心心心心心心
　心心心心心
　　心心心
　　　心`
    },
    sword: {
        name: '剑心',
        desc: '提到剑锋',
        art: `
　　　　　剑
　　　　　剑
　　　　　剑
　　　　　剑
　　　剑剑剑剑
　　剑剑剑剑剑`
    },
    dragon: {
        name: '龙魂',
        desc: '提到龙',
        art: `
　龙　　　　龙
　　龙　　龙
　　　龙龙
　龙　龙　龙
龙　　　　龙`
    },
    tree: {
        name: '树语',
        desc: '提到树木',
        art: `
　　　树树树
　　树树树树树
　树树树树树树树
　　　　　树
　　　　　树
　　　　　树`
    },
    water: {
        name: '流水',
        desc: '提到水海',
        art: `
水水　　水水　　水水
　水水　水水　水水
水水　　水水　　水水`
    },
    moon: {
        name: '月华',
        desc: '提到月亮',
        art: `
　　　月月月
　月月月月月
　月月
　月月
　月月月月月`
    },
    sun: {
        name: '晨曦',
        desc: '提到太阳',
        art: `
　　　曦曦曦
　曦曦曦曦曦曦曦
曦曦曦曦曦曦曦曦曦
　曦曦曦曦曦曦曦
　　　曦曦曦`
    }
};

// 聊天中的艺术图案
const chatPatterns = {
    heart: `
　心　　　心
心心心　心心心
心心心心心心心
　心心心心心
　　心心心
　　　心`,
    star: `
　　　　　星
　　　　星星星
　　　　　星
　　　星星星星星
　　星星星星星星星`,
    sword: `
　　　　　剑
　　　　　剑
　　　　　剑
　　　　　剑
　　　剑剑剑剑
　　剑剑剑剑剑`
};

const bgChars = '暖光星辰梦想思念陪伴故事时光心意灵魂风雨山水花月剑龙日曦晨阳夜影'.split('');

let el = {};

// ============ 初始化 ============
document.addEventListener('DOMContentLoaded', () => {
    el = {
        clock: document.getElementById('clock'),
        statusDot: document.getElementById('statusDot'),
        statusText: document.getElementById('statusText'),
        count: document.getElementById('count'),
        messages: document.getElementById('messages'),
        chatScroll: document.getElementById('chatScroll'),
        userInput: document.getElementById('userInput'),
        sendBtn: document.getElementById('sendBtn'),
        thinking: document.getElementById('thinking'),
        wallGrid: document.getElementById('wallGrid'),
        achModal: document.getElementById('achModal'),
        achBadge: document.getElementById('achBadge'),
        achTitle: document.getElementById('achTitle'),
        floatChars: document.getElementById('floatChars')
    };
    
    updateClock();
    setInterval(updateClock, 1000);
    
    checkConnection();
    setInterval(checkConnection, 5000);  // 每5秒检测一次
    
    initFloatChars();
    
    loadData();
    renderAchievements();
    
    el.userInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') { e.preventDefault(); sendMessage(); }
    });
    
    el.sendBtn.addEventListener('click', sendMessage);
    el.refreshBtn = document.getElementById('refreshBtn');
    el.refreshBtn.addEventListener('click', resetState);
    
    // 图片上传
    el.imageInput = document.getElementById('imageInput');
    el.imageBtn = document.getElementById('imageBtn');
    el.imagePreview = document.getElementById('imagePreview');
    el.previewImg = document.getElementById('previewImg');
    el.removeImg = document.getElementById('removeImg');
    state.selectedImage = null;
    
    el.imageBtn.addEventListener('click', () => el.imageInput.click());
    el.imageInput.addEventListener('change', handleImageSelect);
    el.removeImg.addEventListener('click', clearSelectedImage);
    
    // 粘贴图片支持
    document.addEventListener('paste', handlePasteImage);
    
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') clearChat();
    });
    
    // 欢迎消息
    setTimeout(() => addMsg('你好，我是小暖。', 'assistant'), 400);
    setTimeout(() => addMsg('有什么想聊的吗？', 'assistant'), 800);
});

// ============ 图片处理 ============
function handleImageSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (event) => {
        state.selectedImage = {
            base64: event.target.result,
            name: file.name,
            type: file.type
        };
        el.previewImg.src = event.target.result;
        el.imagePreview.style.display = 'flex';
    };
    reader.readAsDataURL(file);
}

function clearSelectedImage() {
    state.selectedImage = null;
    el.imageInput.value = '';
    el.imagePreview.style.display = 'none';
}

// 处理粘贴图片
function handlePasteImage(e) {
    const items = e.clipboardData?.items;
    if (!items) return;
    
    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        
        // 检查是否是图片
        if (item.type.indexOf('image') !== -1) {
            const file = item.getAsFile();
            if (!file) continue;
            
            const reader = new FileReader();
            reader.onload = (event) => {
                state.selectedImage = {
                    base64: event.target.result,
                    name: 'pasted-image.png',
                    type: file.type || 'image/png'
                };
                el.previewImg.src = event.target.result;
                el.imagePreview.style.display = 'flex';
                
                // 聚焦到输入框
                el.userInput.focus();
            };
            reader.readAsDataURL(file);
            
            // 阻止默认行为
            e.preventDefault();
            break;
        }
    }
}

// ============ 重置状态并重连 ============
async function resetState() {
    // 强制重置状态
    state.typing = false;
    
    // 隐藏思考中
    el.thinking.classList.remove('show');
    
    // 恢复输入
    el.userInput.disabled = false;
    el.sendBtn.disabled = false;
    el.userInput.focus();
    
    // 清除图片
    clearSelectedImage();
    
    // 尝试重新连接
    await reconnect();
}

// ============ 时钟 ============
function updateClock() {
    const now = new Date();
    el.clock.textContent = 
        now.getHours().toString().padStart(2,'0') + ':' +
        now.getMinutes().toString().padStart(2,'0');
}

// ============ 连接状态 ============
async function checkConnection() {
    try {
        const res = await fetch(config.healthUrl, { 
            signal: AbortSignal.timeout(3000)
        });
        const wasOffline = !state.connected;
        state.connected = res.ok;
        state.reconnectAttempts = 0;
        state.lastError = null;
        
        if (state.connected) {
            el.statusDot.parentElement.classList.remove('offline');
            el.statusText.textContent = '在线';
            el.refreshBtn.textContent = '🔄';
            
            // 如果之前是离线状态，现在恢复了
            if (wasOffline) {
                console.log('连接已恢复');
            }
        }
    } catch (e) {
        state.connected = false;
        state.lastError = e.message;
        el.statusDot.parentElement.classList.add('offline');
        el.statusText.textContent = '无法连接';
        el.refreshBtn.textContent = '🔄';
    }
}

// 强制重新连接
async function reconnect() {
    el.refreshBtn.textContent = '⏳';
    el.statusText.textContent = '连接中...';
    
    state.reconnectAttempts++;
    console.log(`尝试重连 (${state.reconnectAttempts})...`);
    
    try {
        // 尝试连接
        const res = await fetch(config.healthUrl, { 
            signal: AbortSignal.timeout(5000)
        });
        
        if (res.ok) {
            state.connected = true;
            state.reconnectAttempts = 0;
            state.lastError = null;
            
            el.statusDot.parentElement.classList.remove('offline');
            el.statusText.textContent = '在线';
            el.refreshBtn.textContent = '🔄';
            
            // 如果有之前未发送的消息，提示用户
            if (el.userInput.value.trim()) {
                addMsg('连接已恢复，可以发送消息了。', 'assistant');
            } else {
                addMsg('已重新连接。', 'assistant');
            }
            return true;
        }
    } catch (e) {
        state.lastError = e.message;
        console.error('重连失败:', e.message);
    }
    
    // 重连失败
    state.connected = false;
    el.statusDot.parentElement.classList.add('offline');
    el.statusText.textContent = '无法连接';
    el.refreshBtn.textContent = '🔄';
    
    // 显示错误信息
    addMsg(`连接失败: ${state.lastError || '桥接服务器未运行'}。请确保 wallpaper-server.js 已启动。`, 'assistant');
    return false;
}

// ============ 漂浮文字 ============
function initFloatChars() {
    for (let i = 0; i < 6; i++) setTimeout(createFloatChar, i * 800);
    setInterval(createFloatChar, 4000);
}

function createFloatChar() {
    if (el.floatChars.children.length > 12) return;
    const div = document.createElement('div');
    div.className = 'float-char';
    div.textContent = bgChars[Math.floor(Math.random() * bgChars.length)];
    div.style.left = Math.random() * 100 + '%';
    div.style.animationDuration = (45 + Math.random() * 30) + 's';
    el.floatChars.appendChild(div);
    setTimeout(() => div.remove(), 80000);
}

// ============ 数据 ============
function loadData() {
    state.count = parseInt(localStorage.getItem('warm_count')) || 0;
    try {
        state.achievements = new Set(JSON.parse(localStorage.getItem('warm_ach') || '[]'));
    } catch { state.achievements = new Set(); }
    updateCount();
}

function saveData() {
    localStorage.setItem('warm_count', state.count);
    localStorage.setItem('warm_ach', JSON.stringify([...state.achievements]));
}

// ============ 成就墙 ============
function renderAchievements() {
    el.wallGrid.innerHTML = '';
    
    const allIds = Object.keys(achievements);
    
    allIds.forEach((id, idx) => {
        const ach = achievements[id];
        const unlocked = state.achievements.has(id);
        
        const div = document.createElement('div');
        div.className = `ach-item ${unlocked ? '' : 'locked'}`;
        
        const artDiv = document.createElement('div');
        artDiv.className = 'ach-art';
        artDiv.textContent = ach.art;
        div.appendChild(artDiv);
        
        div.title = unlocked ? `${ach.name}: ${ach.desc}` : '???';
        div.style.animationDelay = `${idx * 0.08}s`;
        
        el.wallGrid.appendChild(div);
    });
}

// ============ 发送消息 ============
async function sendMessage() {
    const text = el.userInput.value.trim();
    const hasImage = state.selectedImage !== null;
    
    if ((!text && !hasImage) || state.typing) return;
    
    // 如果有图片，显示图片消息
    if (hasImage) {
        addImageMsg(state.selectedImage.base64, text, 'user');
    } else {
        addMsg(text, 'user');
    }
    
    // 保存当前图片并清除
    const currentImage = state.selectedImage;
    clearSelectedImage();
    el.userInput.value = '';
    
    state.count++;
    saveData();
    updateCount();
    
    checkAchievements(text);
    
    el.userInput.disabled = true;
    el.sendBtn.disabled = true;
    state.typing = true;
    state.startTime = Date.now();
    el.thinking.classList.add('show');
    
    try {
        // 先检测连接状态
        if (!state.connected) {
            await checkConnection();
        }
        
        await sendMessageStream(text, currentImage);
    } catch (e) {
        el.thinking.classList.remove('show');
        addMsg('连接失败: ' + e.message, 'assistant');
        
        // 立即更新离线状态
        state.connected = false;
        state.lastError = e.message;
        el.statusDot.parentElement.classList.add('offline');
        el.statusText.textContent = '离线';
        el.refreshBtn.textContent = '🔄';
        
        // 立即检测一次
        checkConnection();
    }
    
    el.userInput.disabled = false;
    el.sendBtn.disabled = false;
    el.userInput.focus();
    state.typing = false;
}

// 添加图片消息
function addImageMsg(imageSrc, text, sender) {
    const msg = document.createElement('div');
    msg.className = `message ${sender}`;
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const img = document.createElement('img');
    img.src = imageSrc;
    img.style.maxWidth = '200px';
    img.style.maxHeight = '150px';
    img.style.borderRadius = '10px';
    img.style.marginBottom = '8px';
    img.style.display = 'block';
    content.appendChild(img);
    
    if (text) {
        const textSpan = document.createElement('span');
        textSpan.textContent = text;
        content.appendChild(textSpan);
    }
    
    const time = document.createElement('div');
    time.className = 'msg-time';
    time.textContent = new Date().toTimeString().slice(0,5);
    
    msg.appendChild(content);
    msg.appendChild(time);
    el.messages.appendChild(msg);
    
    scrollDown();
}

// 流式发送消息
async function sendMessageStream(text, image) {
    const body = {
        message: text || '请看这张图片',
        userName: config.userName,
        sessionKey: config.sessionKey
    };
    
    if (image) {
        body.image = image.base64;
        body.imageType = image.type;
    }
    
    let response;
    try {
        response = await fetch(config.streamUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
            signal: AbortSignal.timeout(120000) // 2分钟超时
        });
    } catch (e) {
        // 网络错误
        state.connected = false;
        el.statusDot.parentElement.classList.add('offline');
        el.statusText.textContent = '无法连接';
        throw new Error('无法连接到桥接服务器，请点击刷新按钮重试');
    }
    
    if (!response.ok) {
        state.connected = false;
        throw new Error('HTTP error: ' + response.status);
    }
    
    el.thinking.classList.remove('show');
    
    // 创建消息容器
    const msg = document.createElement('div');
    msg.className = 'message assistant';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.id = 'streaming-content';
    
    const time = document.createElement('div');
    time.className = 'msg-time';
    
    const elapsed = document.createElement('span');
    elapsed.className = 'elapsed-time';
    
    msg.appendChild(content);
    msg.appendChild(time);
    el.messages.appendChild(msg);
    
    // 读取流式响应
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullContent = '';
    
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = line.slice(6);
                if (data === '[DONE]') continue;
                
                try {
                    const json = JSON.parse(data);
                    if (json.error) {
                        // 服务器返回错误
                        fullContent = '错误: ' + json.error;
                        content.textContent = fullContent;
                        content.style.color = '#f88';
                        break;
                    }
                    if (json.content) {
                        fullContent += json.content;
                        content.textContent = fullContent;
                        scrollDown();
                        
                        // 更新耗时
                        const elapsedMs = Date.now() - state.startTime;
                        elapsed.textContent = `${(elapsedMs / 1000).toFixed(1)}s`;
                    }
                } catch (e) {}
            }
        }
    }
    
    // 完成后处理
    time.textContent = new Date().toTimeString().slice(0,5) + ' · ' + elapsed.textContent;
    
    // 应用发光效果
    applyGlowEffects(content, fullContent);
    
    // 更新状态
    state.connected = true;
    state.reconnectAttempts = 0;
    el.statusDot.parentElement.classList.remove('offline');
    el.statusText.textContent = '在线';
    
    showPattern(text, fullContent);
}

// 应用发光效果
function applyGlowEffects(container, text) {
    container.innerHTML = '';
    
    for (let i = 0; i < text.length; i++) {
        const char = text[i];
        const span = document.createElement('span');
        span.className = 'char';
        
        if (char === '\n') {
            span.classList.add('newline');
        } else if (char !== ' ') {
            for (const [type, chars] of Object.entries(glowChars)) {
                if (chars.includes(char)) {
                    span.classList.add(`glow-${type}`);
                    break;
                }
            }
            span.textContent = char;
        }
        
        container.appendChild(span);
    }
}

// ============ 消息 ============
function addMsg(text, sender) {
    const msg = document.createElement('div');
    msg.className = `message ${sender}`;
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;
    
    const time = document.createElement('div');
    time.className = 'msg-time';
    time.textContent = new Date().toTimeString().slice(0,5);
    
    msg.appendChild(content);
    msg.appendChild(time);
    el.messages.appendChild(msg);
    
    scrollDown();
}

// 流式输出
async function typeMsg(text, sender) {
    const msg = document.createElement('div');
    msg.className = `message ${sender}`;
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const time = document.createElement('div');
    time.className = 'msg-time';
    time.textContent = new Date().toTimeString().slice(0,5);
    
    msg.appendChild(content);
    msg.appendChild(time);
    el.messages.appendChild(msg);
    
    for (let i = 0; i < text.length; i++) {
        const char = text[i];
        const span = document.createElement('span');
        span.className = 'char';
        
        if (char === '\n') {
            span.classList.add('newline');
        } else if (char !== ' ') {
            // 检查是否是发光字符
            for (const [type, chars] of Object.entries(glowChars)) {
                if (chars.includes(char)) {
                    span.classList.add(`glow-${type}`);
                    break;
                }
            }
            span.textContent = char;
        }
        
        span.style.animationDelay = `${i * 0.02}s`;
        content.appendChild(span);
        scrollDown();
        
        await sleep(char === '\n' ? 60 : 25);
    }
}

function scrollDown() {
    el.chatScroll.scrollTop = el.chatScroll.scrollHeight;
}

// ============ 图案 ============
function showPattern(user, resp) {
    const all = user + resp;
    let key = null;
    
    if (all.includes('心') || all.includes('爱')) key = 'heart';
    else if (all.includes('星') || all.includes('梦')) key = 'star';
    else if (all.includes('剑') || all.includes('锋')) key = 'sword';
    
    if (key && Math.random() > 0.4) {
        const art = document.createElement('div');
        art.className = 'pattern-art';
        art.textContent = chatPatterns[key];
        el.messages.appendChild(art);
        scrollDown();
    }
}

// ============ 成就检查 ============
function checkAchievements(msg) {
    const checks = {
        meet: () => state.count >= 1,
        chat5: () => state.count >= 5,
        chat10: () => state.count >= 10,
        chat20: () => state.count >= 20,
        star: () => msg.includes('星') || msg.includes('光') || msg.includes('梦'),
        heart: () => msg.includes('心') || msg.includes('爱') || msg.includes('情'),
        sword: () => msg.includes('剑') || msg.includes('刀') || msg.includes('锋'),
        dragon: () => msg.includes('龙') || msg.includes('麟'),
        tree: () => msg.includes('树') || msg.includes('木') || msg.includes('林'),
        water: () => msg.includes('水') || msg.includes('海') || msg.includes('河'),
        moon: () => msg.includes('月') || msg.includes('夜'),
        sun: () => msg.includes('日') || msg.includes('曦') || msg.includes('晨') || msg.includes('阳')
    };
    
    for (const [id, check] of Object.entries(checks)) {
        if (!state.achievements.has(id) && check()) {
            unlockAch(id);
            break;
        }
    }
}

function unlockAch(id) {
    const ach = achievements[id];
    if (!ach) return;
    
    state.achievements.add(id);
    saveData();
    renderAchievements();
    
    el.achBadge.textContent = ach.art;
    el.achTitle.textContent = `解锁: ${ach.name}`;
    el.achModal.classList.add('show');
    
    setTimeout(() => el.achModal.classList.remove('show'), 3000);
}

// ============ 计数 ============
function updateCount() {
    el.count.textContent = `对话: ${state.count}`;
}

// ============ 清空 ============
async function clearChat() {
    el.messages.innerHTML = '';
    try {
        await fetch(config.clearUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sessionKey: config.sessionKey })
        });
    } catch {}
    setTimeout(() => addMsg('对话已清空。', 'assistant'), 200);
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// Lively壁纸支持
function livelyPropertyListener(name, val) {
    if (name === 'apiUrl') config.apiUrl = val;
    else if (name === 'sessionKey') config.sessionKey = val;
    else if (name === 'userName') config.userName = val;
}