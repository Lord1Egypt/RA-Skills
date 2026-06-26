// ── 聊天面板（REST + SSE 連接 JARVIS 後端） ──

import { addOrbMessage } from './orb-messages.js';
import { updateSystemData } from './system-monitor.js';
import { getConfig } from '../config/config-loader.js';
import { renderMarkdown } from './markdown.js';

const terminalContent = document.getElementById('terminal-content');
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');

// Model Status 面板 DOM
const modelNameEl = document.getElementById('model-name');
const tokensInEl = document.getElementById('tokens-in');
const tokensOutEl = document.getElementById('tokens-out');
const contextValueEl = document.getElementById('context-value');
const contextBarEl = document.getElementById('context-bar');
const contextBarLabelEl = document.getElementById('context-bar-label');
// 單次對話 token 使用量
let lastTokensIn = 0;
let lastTokensOut = 0;
let contextWindow = 128000;  // 會從 API 更新

// ── 里程表數字滾動效果 ──

const isMobileView = window.matchMedia('(max-width: 768px)').matches;

function createOdometer(el) {
  if (!el || el.dataset.odometer === 'ready') return;
  el.dataset.odometer = 'ready';
  el.style.cssText += `
    display: inline-flex;
    overflow: hidden;
    height: 1.2em;
    line-height: 1.2em;
    vertical-align: bottom;
  `;
}

function setOdometerValue(el, value, duration = 800) {
  if (!el) return;

  // 手機版直接顯示文字（odometer 排版會壞）
  if (isMobileView) {
    const formatted = typeof value === 'string' ? value : value.toLocaleString();
    el.textContent = formatted;
    return;
  }

  createOdometer(el);

  const formatted = typeof value === 'string' ? value : value.toLocaleString();
  const chars = formatted.split('');

  // 第一次使用時清空原始文字內容
  if (!el.querySelector('.odo-col')) {
    el.textContent = '';
  }

  // 確保有足夠的 columns（移除多餘的）
  while (el.children.length > chars.length) {
    el.removeChild(el.lastChild);
  }

  chars.forEach((char, i) => {
    let col = el.children[i];

    if (!col) {
      col = document.createElement('span');
      col.className = 'odo-col';
      el.appendChild(col);
    }

    // 非數字字元（逗號、%）直接顯示
    if (!/\d/.test(char)) {
      col.style.cssText = `
        display: inline-block;
        width: auto;
        height: 1.2em;
        line-height: 1.2em;
        overflow: hidden;
      `;
      col.innerHTML = '';
      col.textContent = char;
      col.className = 'odo-col odo-sep';
      return;
    }

    const digit = parseInt(char);
    col.className = 'odo-col';
    col.style.cssText = `
      display: inline-block;
      width: 0.65em;
      height: 1.2em;
      overflow: hidden;
      position: relative;
      text-align: center;
    `;

    // 建立數字捲軸（0-9 + 再一個 0 用於循環）
    let strip = col.querySelector('.odo-strip');
    if (!strip) {
      strip = document.createElement('span');
      strip.className = 'odo-strip';
      strip.style.cssText = `
        display: block;
        transition: transform ${duration}ms cubic-bezier(0.23, 1, 0.32, 1);
        will-change: transform;
      `;
      strip.innerHTML = '0<br>1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9';
      col.innerHTML = '';
      col.appendChild(strip);
    }

    // 更新動畫時長
    strip.style.transitionDuration = duration + 'ms';

    // 滾動到目標數字
    requestAnimationFrame(() => {
      strip.style.transform = `translateY(-${digit * 1.2}em)`;
    });
  });
}

// 進度條平滑動畫
function animateBar(barEl, toPct, duration = 800) {
  if (!barEl) return;
  barEl.style.transition = `width ${duration}ms cubic-bezier(0.23, 1, 0.32, 1)`;
  barEl.style.width = toPct + '%';
}

// 從後端拉 Model Status
async function fetchModelStatus() {
  try {
    const res = await fetch('/api/model-status');
    if (!res.ok) return;
    const data = await res.json();

    // 模型名稱
    if (data.model && modelNameEl) {
      const display = data.provider
        ? `${data.provider}/${data.model}`.toUpperCase()
        : data.model.toUpperCase();
      modelNameEl.textContent = display;
    }
    if (data.contextWindow) contextWindow = data.contextWindow;

    // Token 使用量（單次對話的 input / output）
    if (data.usage) {
      lastTokensIn = data.usage.input || 0;
      lastTokensOut = data.usage.output || 0;
    }
    setOdometerValue(tokensInEl, lastTokensIn);
    setOdometerValue(tokensOutEl, lastTokensOut);

    // Context 使用率
    const total = data.totalTokens || (lastTokensIn + lastTokensOut);
    const pct = Math.min(100, Math.round((total / contextWindow) * 100));
    setOdometerValue(contextValueEl, pct + '%');
    animateBar(contextBarEl, pct);
    if (contextBarLabelEl) contextBarLabelEl.textContent = pct + '%';
  } catch {
    // ignore
  }
}

let isWaiting = false;
let currentReplyLine = null;
let replyBuffer = '';
let activeRunId = null;  // 追蹤我們送出的 runId

// TTS 語音播放（透過事件通知 audio.js → Orb + 頻譜 + 波形連動）
let ttsEnabled = true;

async function speakText(text) {
  if (!ttsEnabled || !text) return;
  try {
    // 限制長度，避免 macOS say 卡太久（超過 500 字截斷）
    const ttsText = text.length > 500 ? text.slice(0, 500) : text;

    const res = await fetch('/api/tts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: ttsText }),
    });
    if (!res.ok) return;

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    // 通知音頻系統播放（避免循環依賴）
    window.dispatchEvent(new CustomEvent('tts-play', { detail: { url, label: 'TTS_VOICE_OUTPUT' } }));
  } catch {
    // TTS 失敗不影響主流程
  }
}

// 串流速度追蹤
let lastStreamLen = 0;
let lastStreamTime = 0;
let streamSpeedTimer = null;

// ── SSE 串流 ──
// ── 載入 Gateway 歷史訊息 ──
async function loadHistory() {
  try {
    const displayLimit = parseInt(localStorage.getItem('jarvis-history-limit') || '50');
    // 多拉幾倍，因為 tool calls/heartbeat 會被過濾掉
    const fetchLimit = displayLimit * 4;
    const res = await fetch(`/api/history?limit=${fetchLimit}`);
    if (!res.ok) return;
    const data = await res.json();
    const messages = data.messages || [];

    // 過濾出 user/assistant 的文字訊息
    const chatMessages = [];
    for (const m of messages) {
      if (m.role !== 'user' && m.role !== 'assistant') continue;
      // 跳過包含 tool call 的 assistant 訊息（純工具呼叫不是對話）
      const hasToolCall = (m.content || []).some(c => c.type === 'toolCall');
      const texts = (m.content || [])
        .filter(c => c.type === 'text' && c.text?.trim())
        .map(c => {
          let t = c.text.trim();
          // 剝離 Conversation info metadata，保留使用者實際文字
          if (t.startsWith('Conversation info')) {
            const parts = t.split('\n```\n\n');
            t = parts.length > 1 ? parts.slice(1).join('\n```\n\n').trim() : '';
          }
          return t;
        })
        .filter(t => t && !t.startsWith('Read HEARTBEAT'))
        .filter(t => t !== 'HEARTBEAT_OK')
        .filter(t => t !== 'NO_REPLY')
        .filter(t => !t.startsWith('System:'))
        .filter(t => !t.startsWith('Pre-compaction'));
      if (!texts.length) continue;
      // assistant 有 tool call 但也有文字 → 保留文字（最終回覆）
      // assistant 只有 tool call → 跳過
      if (m.role === 'assistant' && hasToolCall && !m.stopReason?.includes('end_turn')) continue;
      chatMessages.push({
        role: m.role,
        text: texts.join('\n'),
        timestamp: m.timestamp,
      });
    }

    if (!chatMessages.length) return;

    // 只取最後 N 則實際對話
    const displayMessages = chatMessages.slice(-displayLimit);

    // 加一條分隔線
    addChatLine(`── HISTORY (${displayMessages.length}) ──`, 'system-line');

    for (const msg of displayMessages) {
      const className = msg.role === 'user' ? 'user-line' : 'jin-line';
      const line = addChatLine('', className);
      if (!line) continue;

      // 用時間戳覆蓋 timeStamp()
      if (msg.timestamp) {
        const timeEl = line.querySelector('.msg-time');
        if (timeEl) {
          const d = new Date(msg.timestamp);
          const hh = String(d.getHours()).padStart(2, '0');
          const mm = String(d.getMinutes()).padStart(2, '0');
          timeEl.textContent = `${d.getMonth() + 1}/${d.getDate()} ${hh}:${mm}`;
        }
      }

      // 渲染文字（assistant 用 markdown）
      const msgText = line.querySelector('.msg-text');
      if (msgText) {
        if (msg.role === 'assistant') {
          msgText.innerHTML = renderMarkdown(msg.text);
        } else {
          msgText.textContent = msg.text;
        }
      }
    }

    addChatLine('── END HISTORY ──', 'system-line');
    if (terminalContent) terminalContent.scrollTop = terminalContent.scrollHeight;
  } catch {
    // 靜默失敗，不影響正常使用
  }
}

function connectSSE() {
  const evtSource = new EventSource('/api/events');
  window.__jarvisSSE = evtSource;  // 共用給 tasks.js, schedule.js 等

  evtSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);

      if (data.type === 'connected') {
        addChatLine('GATEWAY STREAM CONNECTED ✓', 'system-line');
        return;
      }

      if (data.type === 'system') {
        updateSystemData(data);
        return;
      }

      // chat 事件串流
      handleChatEvent(data);
    } catch {
      // ignore
    }
  };

  evtSource.onerror = () => {
    // SSE 自動重連
  };
}

function handleChatEvent(data) {
  const text = data.text || '';
  const done = data.done || false;

  // 只處理我們送出的 runId，或是沒指定 runId 的通用事件
  if (data.runId && activeRunId && data.runId !== activeRunId) return;

  // 有文字 → 更新回覆行
  if (text) {
    if (!currentReplyLine) {
      currentReplyLine = addChatLine('', 'jin-line');
      replyBuffer = '';
      lastStreamLen = 0;
      lastStreamTime = performance.now();
      window.dispatchEvent(new CustomEvent('agent-state', { detail: 'responding' }));

      // 定期計算串流速度
      if (streamSpeedTimer) clearInterval(streamSpeedTimer);
      streamSpeedTimer = setInterval(() => {
        const now = performance.now();
        const dt = (now - lastStreamTime) / 1000;
        if (dt > 0) {
          const charsPerSec = (replyBuffer.length - lastStreamLen) / dt;
          // 正規化：~50 chars/sec = 1.0 強度
          const intensity = Math.min(1, charsPerSec / 50);
          window.dispatchEvent(new CustomEvent('agent-stream', { detail: intensity }));
          lastStreamLen = replyBuffer.length;
          lastStreamTime = now;
        }
      }, 200);
    }
    // delta 是累積的完整文字
    replyBuffer = text;
    if (currentReplyLine) {
      const msgSpan = currentReplyLine.querySelector('.msg-text');
      if (msgSpan) msgSpan.textContent = replyBuffer;
      terminalContent.scrollTop = terminalContent.scrollHeight;
    }
  }

  if (done) {
    // 清理串流追蹤
    if (streamSpeedTimer) { clearInterval(streamSpeedTimer); streamSpeedTimer = null; }
    window.dispatchEvent(new CustomEvent('agent-stream', { detail: 0 }));

    // 回覆完成 → 更新 Model Status（streaming 不帶 usage，需另外拉）
    fetchModelStatus();

    // 回覆完成 → Orb 通知
    if (replyBuffer) {
      const cfg = getConfig();
      const agentName = cfg?.agent?.name || 'JARVIS';
      addOrbMessage(`${agentName}: ${replyBuffer}`);
      speakText(replyBuffer);

      // 串流完成 → Markdown 渲染
      if (currentReplyLine) {
        const msgBody = currentReplyLine.querySelector('.msg-body');
        if (msgBody) {
          const timeEl = msgBody.querySelector('.msg-time');
          msgBody.innerHTML = renderMarkdown(replyBuffer);
          if (timeEl) msgBody.appendChild(timeEl);
        }
        currentReplyLine.classList.add('markdown-rendered');
        terminalContent.scrollTop = terminalContent.scrollHeight;
      }
    }
    currentReplyLine = null;
    replyBuffer = '';
    activeRunId = null;
    isWaiting = false;
    window.dispatchEvent(new CustomEvent('agent-state', { detail: 'idle' }));
    if (chatSend) chatSend.textContent = 'SEND';
  }
}

// 時間戳格式
function timeStamp() {
  const now = new Date();
  return now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
}

// ── 公開 API ──
export function addChatLine(text, className, images = []) {
  if (!terminalContent) return null;

  const line = document.createElement('div');
  line.className = `terminal-line ${className}`;

  // 系統訊息不加時間戳和標籤
  if (className.includes('system-line') || className.includes('command-line')) {
    line.textContent = text;
  } else {
    // 發送者標籤
    const sender = document.createElement('span');
    sender.className = 'msg-sender';
    const cfg = getConfig();
    sender.textContent = className.includes('user-line') ? 'YOU' : (cfg?.agent?.name || 'JARVIS').toUpperCase();
    line.appendChild(sender);

    // 內容行（text + time）
    const msgBody = document.createElement('div');
    msgBody.className = 'msg-body';

    // 圖片預覽
    if (images.length) {
      const imgContainer = document.createElement('div');
      imgContainer.className = 'msg-images';
      images.forEach(src => {
        const img = document.createElement('img');
        img.src = src;
        img.className = 'msg-image';
        img.addEventListener('click', () => window.open(src, '_blank'));
        imgContainer.appendChild(img);
      });
      msgBody.appendChild(imgContainer);
    }

    const msgText = document.createElement('span');
    msgText.className = 'msg-text';
    msgText.textContent = text;
    msgBody.appendChild(msgText);

    const time = document.createElement('span');
    time.className = 'msg-time';
    time.textContent = timeStamp();
    msgBody.appendChild(time);

    line.appendChild(msgBody);
  }

  terminalContent.appendChild(line);

  // 限制 terminal 行數，避免 DOM 無限膨脹
  const MAX_LINES = 100;
  const lines = terminalContent.querySelectorAll('.terminal-line');
  if (lines.length > MAX_LINES) {
    const excess = lines.length - MAX_LINES;
    for (let i = 0; i < excess; i++) lines[i].remove();
  }

  terminalContent.scrollTop = terminalContent.scrollHeight;
  return line;
}

export function addTerminalMessage(message, isCommand = false) {
  if (!terminalContent) return;
  const newLine = document.createElement('div');
  newLine.className = isCommand ? 'terminal-line command-line' : 'terminal-line system-line';
  newLine.textContent = message;
  terminalContent.appendChild(newLine);
  terminalContent.scrollTop = terminalContent.scrollHeight;
}

// ── 送出 ──
const chatAttach = document.getElementById('chat-attach');
const chatFileInput = document.getElementById('chat-file-input');
let pendingFiles = [];  // 待發送的附件

const ATTACH_SVG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48"/></svg>';

function updateAttachBtn(count) {
  if (!chatAttach) return;
  chatAttach.classList.toggle('has-files', count > 0);
  chatAttach.innerHTML = count > 0 ? `${ATTACH_SVG}<span class="attach-badge">${count}</span>` : ATTACH_SVG;
}

// 附件按鈕
if (chatAttach && chatFileInput) {
  chatAttach.addEventListener('click', () => chatFileInput.click());
  chatFileInput.addEventListener('change', () => {
    pendingFiles = Array.from(chatFileInput.files || []);
    updateAttachBtn(pendingFiles.length);
  });
}

// Orb 拖放
const orbDropZone = document.getElementById('three-container') || document.body;
['dragenter', 'dragover'].forEach(evt => {
  orbDropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    e.stopPropagation();
    orbDropZone.classList.add('drag-over');
  });
});
['dragleave', 'drop'].forEach(evt => {
  orbDropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    e.stopPropagation();
    orbDropZone.classList.remove('drag-over');
  });
});
orbDropZone.addEventListener('drop', (e) => {
  const files = Array.from(e.dataTransfer?.files || []);
  if (!files.length) return;
  pendingFiles = files;
  updateAttachBtn(files.length);
  // 自動送出：分析這些檔案
  chatInput.value = chatInput.value || '請分析這些檔案';
  handleChatSend();
});

async function handleChatSend() {
  if (!chatInput || isWaiting) return;
  const msg = chatInput.value.trim();
  const hasFiles = pendingFiles.length > 0;
  if (!msg && !hasFiles) return;

  // 用戶互動時提前初始化 AudioContext（解決手機 autoplay 限制）
  window.dispatchEvent(new Event('user-interaction'));

  // 顯示附件資訊（含圖片預覽）
  if (hasFiles) {
    const imageUrls = [];
    const fileNames = [];
    pendingFiles.forEach(f => {
      fileNames.push(f.name);
      if (f.type.startsWith('image/')) {
        imageUrls.push(URL.createObjectURL(f));
      }
    });
    addChatLine(msg || `📎 ${fileNames.join(', ')}`, 'user-line', imageUrls);
  } else {
    addChatLine(msg, 'user-line');
  }
  chatInput.value = '';

  isWaiting = true;
  window.dispatchEvent(new CustomEvent('agent-state', { detail: 'thinking' }));
  if (chatSend) chatSend.textContent = '...';

  // 不預建回覆行，等 SSE 第一個 chunk 再建
  currentReplyLine = null;
  replyBuffer = '';

  try {
    let res;
    if (hasFiles) {
      // 帶檔案 → FormData
      const formData = new FormData();
      formData.append('message', msg);
      pendingFiles.forEach(f => formData.append('files', f));
      res = await fetch('/api/chat/upload', { method: 'POST', body: formData });
      // 清除附件
      pendingFiles = [];
      if (chatAttach) { updateAttachBtn(0); }
      if (chatFileInput) chatFileInput.value = '';
    } else {
      res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg }),
      });
    }

    const result = await res.json();

    if (!res.ok) {
      addChatLine(`ERROR: ${result.error || 'Unknown error'}`, 'system-line');
      currentReplyLine = null;
      activeRunId = null;
      isWaiting = false;
      window.dispatchEvent(new CustomEvent('agent-state', { detail: 'idle' }));
      if (chatSend) chatSend.textContent = 'SEND';
      return;
    }

    // 記錄 runId，等 SSE 串流
    activeRunId = result.runId || null;

    // 超時 fallback
    setTimeout(() => {
      if (isWaiting && activeRunId === result.runId) {
        if (!replyBuffer) {
          addChatLine('TIMEOUT — 等待回覆超時', 'system-line');
        }
        if (streamSpeedTimer) { clearInterval(streamSpeedTimer); streamSpeedTimer = null; }
        window.dispatchEvent(new CustomEvent('agent-stream', { detail: 0 }));
        currentReplyLine = null;
        activeRunId = null;
        isWaiting = false;
        window.dispatchEvent(new CustomEvent('agent-state', { detail: 'idle' }));
        if (chatSend) chatSend.textContent = 'SEND';
      }
    }, 60000);

  } catch (err) {
    addChatLine(`CONNECTION ERROR: ${err.message}`, 'system-line');
    if (streamSpeedTimer) { clearInterval(streamSpeedTimer); streamSpeedTimer = null; }
    window.dispatchEvent(new CustomEvent('agent-stream', { detail: 0 }));
    currentReplyLine = null;
    isWaiting = false;
    window.dispatchEvent(new CustomEvent('agent-state', { detail: 'idle' }));
    if (chatSend) chatSend.textContent = 'SEND';
  }
}

// ── 初始化打字動畫 ──
let lastUserActionTime = Date.now();
export function updateUserActivity() {
  lastUserActionTime = Date.now();
}

// ── 初始化 ──
export function initChat() {
  // 監聽外部模組的 terminal 訊息（解耦用，避免循環依賴）
  window.addEventListener('terminal-message', (e) => {
    const { message, isCommand } = e.detail;
    addTerminalMessage(message, isCommand);
  });

  if (chatSend) chatSend.addEventListener('click', handleChatSend);
  if (chatInput) {
    // IME 輸入中（注音/日文等）按 Enter 是確認選字，不送出
    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.isComposing) handleChatSend();
    });

    // Ctrl+V / Cmd+V 貼圖支援
    chatInput.addEventListener('paste', (e) => {
      const items = Array.from(e.clipboardData?.items || []);
      const imageItems = items.filter(item => item.type.startsWith('image/'));
      if (!imageItems.length) return;

      e.preventDefault();
      const files = imageItems.map(item => item.getAsFile()).filter(Boolean);
      pendingFiles = [...pendingFiles, ...files];
      updateAttachBtn(pendingFiles.length);
      // 顯示通知
      addChatLine(`📋 已貼上 ${files.length} 張圖片，輸入訊息後送出`, 'system-line');
    });
  }

  // 初始化系統訊息（config 已載入）
  const cfg = getConfig();
  const agentName = cfg?.agent?.name || 'JARVIS';
  const agentEmoji = cfg?.agent?.emoji || '🤖';

  // 直接顯示系統訊息，不用打字動畫
  setTimeout(() => {
    addChatLine(`SYSTEM INITIALIZED. ${agentName.toUpperCase()} INTERFACE ONLINE.`, 'system-line');
  }, 1000);

  // 手機版：點 header 收合/展開聊天面板
  if (window.matchMedia('(max-width: 768px)').matches) {
    const chatHeader = document.querySelector('.terminal-panel.chat-panel .terminal-header');
    if (chatHeader) {
      let swiped = false;

      chatHeader.addEventListener('click', () => {
        if (swiped) { swiped = false; return; }
        const panel = document.querySelector('.terminal-panel.chat-panel');
        if (panel) {
          panel.classList.remove('chat-fullscreen');
          panel.classList.toggle('chat-collapsed');
        }
      });

      // 手機版：上滑 header 展開全螢幕，下滑縮回
      let touchStartY = 0;
      chatHeader.addEventListener('touchstart', (e) => {
        touchStartY = e.touches[0].clientY;
        swiped = false;
      }, { passive: true });
      chatHeader.addEventListener('touchend', (e) => {
        const deltaY = touchStartY - e.changedTouches[0].clientY;
        const panel = document.querySelector('.terminal-panel.chat-panel');
        if (!panel) return;
        if (deltaY > 50) {
          swiped = true;
          panel.classList.remove('chat-collapsed');
          panel.classList.add('chat-fullscreen');
        } else if (deltaY < -50) {
          swiped = true;
          panel.classList.remove('chat-fullscreen');
        }
      }, { passive: true });
    }
  }

  // 歷史訊息數量選擇器
  const historyLimit = document.getElementById('history-limit');
  if (historyLimit) {
    const saved = localStorage.getItem('jarvis-history-limit');
    if (saved) historyLimit.value = saved;
    historyLimit.addEventListener('change', () => {
      localStorage.setItem('jarvis-history-limit', historyLimit.value);
    });
  }

  // 載入歷史訊息，完成後再連 SSE
  loadHistory().then(() => {
    setTimeout(connectSSE, 500);
  });

  // 初始化 Model Status
  setTimeout(fetchModelStatus, 3500);

  // 檢查後端狀態
  setTimeout(async () => {
    try {
      const res = await fetch('/api/status');
      const data = await res.json();
      if (data.gateway) {
        addChatLine('OPENCLAW GATEWAY ONLINE ✓', 'system-line');
        addOrbMessage('GATEWAY ONLINE ✓');
      } else {
        addChatLine('GATEWAY CONNECTING...', 'system-line');
      }
    } catch {
      addChatLine('BACKEND NOT AVAILABLE — DEMO MODE', 'system-line');
      addOrbMessage('⚠ DEMO MODE');
    }
  }, 3000);
}
