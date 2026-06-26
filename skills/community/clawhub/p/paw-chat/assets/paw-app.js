(() => {
  const $ = s => document.querySelector(s);
  const msgBox = $('#messages');
  const empty = $('#empty');
  const input = $('#input');
  const sendBtn = $('#send-btn');
  const stopBtn = $('#stop-btn');
  const uploadBtn = $('#upload-btn');
  const fileInput = $('#file-input');
  const previewArea = $('#preview-area');
  const statusEl = $('#status');
  const typing = $('#typing');
  const settingsOverlay = $('#settings-overlay');
  const settingsPanel = $('#settings');
  const sessionPanel = $('#session-dropdown');
  const sessionListEl = $('#session-list');
  const newSessionDialog = $('#new-session-dialog');
  const newSessionKeyInput = $('#new-session-key');
  const cfgUrl = $('#cfg-url');
  const cfgToken = $('#cfg-token');
  const cfgSession = $('#cfg-session');
  const agentBtn = $('#agent-btn');
  const appLogo = $('#app-logo');

  const PROTOCOL_VERSION = 3;
  const CLIENT_INFO = {
    id: 'openclaw-control-ui',
    displayName: 'Web Chat',
    version: '1.0.0',
    platform: navigator.platform || 'web',
    mode: 'webchat',
  };
  const TOOL_ICONS = {
    read:'📄', write:'✏️', edit:'🔧', exec:'⚡', process:'⚙️',
    web_search:'🔍', web_fetch:'🌐', browser:'🖥️',
    memory_search:'🧠', memory_get:'🧠',
    message:'💬', tts:'🔊', cron:'⏰', gateway:'🔌', canvas:'🎨',
    nodes:'📡', sessions_spawn:'🚀', sessions_send:'📨',
    sessions_list:'📋', sessions_history:'📜', session_status:'📊', agents_list:'🤖',
  };

  let ws = null;
  let sessionKey = 'main';
  let canonicalKey = '';
  let isRunning = false;
  let streamingEl = null;
  let streamBuf = '';
  let reqId = 0;
  const pending = new Map();
  const toolCallElements = new Map();
  let agentsList = [];
  let currentAgentId = '';
  let pendingImages = [];

  // Reconnect state
  let reconnectTimer = null;
  let reconnectAttempt = 0;
  let pingInterval = null;
  let manualDisconnect = false;
  const RECONNECT_BASE_MS = 1000;    // 1s
  const RECONNECT_MAX_MS = 60000;    // 60s
  const RECONNECT_MAX_ATTEMPTS = 10;

  function getReconnectDelay() {
    // Exponential backoff with jitter: 1s, 2s, 4s, 8s, 16s, 32s, 60s...
    const delay = Math.min(RECONNECT_BASE_MS * Math.pow(2, reconnectAttempt), RECONNECT_MAX_MS);
    const jitter = delay * 0.2 * Math.random();
    return Math.floor(delay + jitter);
  }

  function scheduleReconnect() {
    if (manualDisconnect || reconnectAttempt >= RECONNECT_MAX_ATTEMPTS) {
      if (reconnectAttempt >= RECONNECT_MAX_ATTEMPTS) {
        setStatus('重连失败，请手动连接', 'error');
      }
      return;
    }
    const delay = getReconnectDelay();
    const secs = (delay / 1000).toFixed(1);
    setStatus(`${secs}s 后重连 (${reconnectAttempt + 1}/${RECONNECT_MAX_ATTEMPTS})...`, 'error');
    reconnectTimer = setTimeout(() => {
      reconnectAttempt++;
      connect(true);
    }, delay);
  }

  function cancelReconnect() {
    if (reconnectTimer) { clearTimeout(reconnectTimer); reconnectTimer = null; }
  }

  // ── Config ──
  function saveConfig() {
    try { localStorage.setItem('oc-chat-cfg', JSON.stringify({
      url: cfgUrl.value, token: cfgToken.value, session: cfgSession.value
    })); } catch {}
  }
  function autoWsUrl() {
    if (location.protocol === 'file:') return ''; // local file — user must fill in manually
    return `${location.protocol === 'https:' ? 'wss:' : 'ws:'}//${location.host}`;
  }
  function loadConfig() {
    try {
      const cfg = JSON.parse(localStorage.getItem('oc-chat-cfg') || '{}');
      cfgUrl.value = cfg.url || autoWsUrl();
      cfgToken.value = cfg.token || '';
      cfgSession.value = cfg.session || 'main';
    } catch { cfgUrl.value = autoWsUrl(); }
  }

  // ── UI ──
  function setStatus(t, c) { statusEl.textContent = t; statusEl.className = c || ''; }
  function autoResize() { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 150) + 'px'; }
  function isNearBottom() {
    // User is "near bottom" if within 150px of the bottom edge
    return msgBox.scrollHeight - msgBox.scrollTop - msgBox.clientHeight < 150;
  }

  function scrollBottom(force) {
    if (!force && !isNearBottom()) return; // don't hijack user's scroll position
    requestAnimationFrame(() => {
      msgBox.scrollTop = msgBox.scrollHeight;
      setTimeout(() => { msgBox.scrollTop = msgBox.scrollHeight; }, 100);
    });
  }
  function escHtml(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  // Lazy image loading
  const lazyObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src && !img.src) {
          img.src = img.dataset.src;
        }
        lazyObserver.unobserve(img);
      }
    }
  }, { rootMargin: '200px' });

  // Also handle markdown-rendered lazy images after addMessage
  function activateLazyImages(container) {
    if (!container) return;
    const imgs = container.querySelectorAll('img.lazy-img:not([src])');
    for (const img of imgs) {
      if (img.dataset.src) {
        // 立即加载图片，不使用懒加载（消息中的图片通常已经在视口内）
        img.src = img.dataset.src;
        img.classList.remove('lazy-img');
      }
    }
  }

  // Image lightbox
  function showImageLightbox(src) {
    const overlay = document.createElement('div');
    overlay.className = 'img-lightbox';
    overlay.innerHTML = `<button class="img-lightbox-close">✕</button><img src="${src}">`;
    overlay.onclick = () => overlay.remove();
    document.body.appendChild(overlay);
    // ESC to close
    const handler = (e) => { if (e.key === 'Escape') { overlay.remove(); document.removeEventListener('keydown', handler); } };
    document.addEventListener('keydown', handler);
  }

  // Configure marked with highlight.js for code blocks
  (() => {
    if (typeof hljs !== 'undefined') {
      // Register additional language aliases
      hljs.registerAliases(['sh'], { languageName: 'bash' });
      hljs.registerAliases(['ts'], { languageName: 'typescript' });
      hljs.registerAliases(['js'], { languageName: 'javascript' });
      hljs.registerAliases(['py'], { languageName: 'python' });
      hljs.registerAliases(['yml'], { languageName: 'yaml' });
      hljs.registerAliases(['html'], { languageName: 'xml' });
    }
    if (typeof marked !== 'undefined') {
      marked.setOptions({
        breaks: true, // \n → <br> (chat-style line breaks)
        gfm: true,    // GitHub Flavored Markdown (tables, strikethrough, etc.)
        highlight: (code, lang) => {
          if (typeof hljs === 'undefined') return escHtml(code);
          if (lang && hljs.getLanguage(lang)) {
            try { return hljs.highlight(code, { language: lang }).value; } catch {}
          }
          try { return hljs.highlightAuto(code).value; } catch {}
          return escHtml(code);
        },
      });
      // Custom renderer for images and links
      const renderer = new marked.Renderer();
      renderer.image = function(token) {
        const href = token.href || '';
        const alt = token.text || '';
        return `<img loading="lazy" data-src="${href}" alt="${escHtml(alt)}" class="chat-img lazy-img" onclick="showImageLightbox(this.src)">`;
      };
      renderer.link = function(token) {
        const href = token.href || '';
        const text = token.text || href;
        return `<a href="${href}" target="_blank" rel="noopener">${text}</a>`;
      };
      marked.setOptions({ renderer });
    }
  })();

  function renderMarkdown(text) {
    try {
      if (typeof marked !== 'undefined') {
        return marked.parse(text);
      }
      // Fallback: basic escaping if marked didn't load
      return escHtml(text).replace(/\n/g, '<br>');
    } catch (e) {
      console.warn('[renderMarkdown error]', e);
      return escHtml(text).replace(/\n/g, '<br>');
    }
  }

  // ── Tool Cards ──
  function summarizeToolArgs(name, args) {
    if (!args) return '';
    try {
      const a = typeof args === 'string' ? JSON.parse(args) : args;
      if (name === 'read' || name === 'write' || name === 'edit') return a.path || a.file_path || '';
      if (name === 'exec') return (a.command || '').substring(0, 60);
      if (name === 'web_search') return a.query || '';
      if (name === 'web_fetch') return (a.url || '').substring(0, 60);
      if (name === 'memory_search') return a.query || '';
      if (name === 'message') return `${a.action||''} → ${a.target||a.to||''}`;
      if (name === 'browser') return a.action || '';
      for (const v of Object.values(a)) { if (typeof v === 'string' && v) return v.substring(0, 50); }
    } catch {}
    return '';
  }

  function createToolCard(tc) {
    const name = tc.name || 'unknown';
    const icon = TOOL_ICONS[name] || '🔧';
    const summary = summarizeToolArgs(name, tc.arguments || tc.input);
    const argsStr = typeof tc.arguments === 'string' ? tc.arguments : JSON.stringify(tc.arguments || tc.input || {}, null, 2);
    const group = document.createElement('div');
    group.className = 'tool-group';
    group.innerHTML = `
      <div class="tool-header" onclick="this.parentElement.classList.toggle('open')">
        <span class="tool-chevron">▶</span>
        <span style="flex-shrink:0">${icon}</span>
        <span class="tool-name">${escHtml(name)}</span>
        <span class="tool-summary">${escHtml(summary)}</span>
      </div>
      <div class="tool-body">
        <div class="tool-label">参数</div>
        <pre>${escHtml(argsStr)}</pre>
        <div class="tool-result" style="display:none">
          <div class="tool-label">结果</div>
          <pre class="tool-result-text"></pre>
        </div>
      </div>`;
    if (tc.id) toolCallElements.set(tc.id, group);
    return group;
  }

  function attachToolResult(id, text) {
    const group = toolCallElements.get(id);
    if (!group) return;
    const rd = group.querySelector('.tool-result');
    const rp = group.querySelector('.tool-result-text');
    if (rd && rp) {
      const maxLen = 2000;
      rp.textContent = text.length > maxLen ? text.substring(0, maxLen) + `\n... (${text.length - maxLen} chars truncated)` : text;
      rd.style.display = '';
    }
  }

  // ── Content Extraction ──
  function extractText(content) {
    if (typeof content === 'string') return content;
    if (Array.isArray(content)) return content.filter(c => c.type === 'text' || c.type === 'output_text').map(c => c.text || '').join('');
    return '';
  }

  // Strip OpenClaw envelope metadata from user messages
  function stripUserEnvelope(text) {
    // Remove "Conversation info (untrusted metadata):\n```json\n{...}\n```\n\n"
    // Use greedy match for the entire ```json...``` block (handles nested braces)
    text = text.replace(/^Conversation info \(untrusted metadata\):\s*```json\s*[\s\S]*?```\s*/m, '');
    // Remove timestamp prefix like "[Wed 2026-03-04 21:10 GMT+8] "
    text = text.replace(/^\[(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s+GMT[+-]\d+\]\s*/m, '');
    return text.trim();
  }

  // ── Message Rendering ──
  function createAvatar(role) {
    const av = document.createElement('div');
    av.className = `avatar ${role === 'user' ? 'user-avatar' : 'bot-avatar'}`;
    if (role === 'user') {
      av.textContent = '👤';
    } else {
      // 获取当前 agent 的 identity
      const curAgent = agentsList.find(a => a.id === currentAgentId);
      const identity = curAgent?.identity || {};
      
      // 优先级: agent avatar > agent emoji > 默认 emoji
      if (identity.avatar) {
        // 使用 agent 的 avatar 图片
        const img = document.createElement('img');
        img.src = identity.avatar;
        img.alt = identity.name || 'Assistant';
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';
        img.style.borderRadius = '50%';
        img.onerror = () => {
          img.style.display = 'none';
          av.textContent = identity.emoji || '🤖';
        };
        av.appendChild(img);
      } else if (identity.emoji) {
        // 使用 agent 的 emoji
        av.textContent = identity.emoji;
      } else {
        // 使用默认 emoji（不是 Paw logo）
        av.textContent = '🤖';
      }
    }
    return av;
  }

  function wrapInRow(role, msgEl) {
    if (role === 'system') {
      const row = document.createElement('div');
      row.className = 'msg-row system';
      row.appendChild(msgEl);
      return row;
    }
    const row = document.createElement('div');
    row.className = `msg-row ${role}`;
    row.appendChild(createAvatar(role));
    row.appendChild(msgEl);
    return row;
  }

  function addMessage(role, content, cls) {
    empty.classList.add('hidden');
    msgBox.style.display = 'flex';

    if (typeof content === 'string' || !Array.isArray(content)) {
      const text = typeof content === 'string' ? content : extractText(content);
      if (!text.trim()) return null;
      const el = document.createElement('div');
      el.className = `msg ${role} ${cls || ''}`;
      if (role === 'assistant' || role === 'system') el.innerHTML = renderMarkdown(text);
      else el.textContent = text;
      msgBox.appendChild(wrapInRow(role, el));
      activateLazyImages(el);
      scrollBottom();
      return el;
    }

    // Rich content with tool calls
    const textStr = content.filter(c => c.type === 'text' || c.type === 'output_text').map(c => c.text || '').join('').trim();
    const toolCalls = content.filter(c => c.type === 'toolCall' || c.type === 'tool_use');
    if (!textStr && !toolCalls.length) return null;

    const wrapper = document.createElement('div');
    wrapper.className = `msg ${role} ${cls || ''}`;
    if (textStr) {
      const d = document.createElement('div');
      d.innerHTML = renderMarkdown(textStr);
      wrapper.appendChild(d);
    }
    for (const tc of toolCalls) wrapper.appendChild(createToolCard(tc));
    msgBox.appendChild(wrapInRow(role, wrapper));
    activateLazyImages(wrapper);
    scrollBottom();
    return wrapper;
  }

  // ── WebSocket ──
  function connect(isReconnect) {
    if (ws) { ws.onclose = null; ws.close(); ws = null; }
    if (!isReconnect) {
      manualDisconnect = false;
      reconnectAttempt = 0;
      cancelReconnect();
    }
    const url = cfgUrl.value.trim() || 'ws://127.0.0.1:18789';
    sessionKey = cfgSession.value.trim() || 'main';
    if (!isReconnect) canonicalKey = '';
    saveConfig();
    setStatus(isReconnect ? `重连中 (${reconnectAttempt}/${RECONNECT_MAX_ATTEMPTS})...` : '连接中...', '');
    try { ws = new WebSocket(url); } catch {
      setStatus('连接失败', 'error');
      if (!manualDisconnect) scheduleReconnect();
      return;
    }

    ws.onopen = () => setStatus('等待握手...', '');

    ws.onmessage = (event) => {
      let frame;
      try { frame = JSON.parse(event.data); } catch { return; }

      if (frame.type === 'event') {
        if (frame.event === 'connect.challenge') {
          const token = cfgToken.value.trim();
          sendRpc('connect', {
            minProtocol: PROTOCOL_VERSION, maxProtocol: PROTOCOL_VERSION,
            client: CLIENT_INFO,
            role: 'operator',
            scopes: ['operator.read', 'operator.write'],
            caps: ['tool-events'],
            auth: token ? { token } : undefined,
          }).then(() => {
            reconnectAttempt = 0;
            cancelReconnect();
            setStatus('已连接', 'connected');
            input.disabled = false; sendBtn.disabled = false; uploadBtn.disabled = false; agentBtn.disabled = false;
            settingsPanel.classList.remove('show');
            // Enable tool event streaming by setting verbose level
            sendRpc('sessions.patch', { key: sessionKey, verboseLevel: 'on' }).catch(() => {});
            // Keepalive ping every 30s to prevent idle disconnection
            if (pingInterval) clearInterval(pingInterval);
            pingInterval = setInterval(() => {
              if (ws && ws.readyState === WebSocket.OPEN) {
                sendRpc('ping', {}).catch(() => {});
              }
            }, 30000);
            loadHistory();
            initSidebar();
          }).catch(err => {
            setStatus('认证失败', 'error');
            addMessage('system', '认证失败: ' + (err.message || err));
          });
          return;
        }
        if (frame.event === 'chat') { handleChatEvent(frame.payload); return; }
        if (frame.event === 'agent') { handleAgentEvent(frame.payload); return; }
        return;
      }

      if (frame.type === 'res' && frame.id && pending.has(frame.id)) {
        const p = pending.get(frame.id);
        pending.delete(frame.id);
        if (frame.ok === false) p.reject(frame.error || { message: 'unknown error' });
        else p.resolve(frame.payload);
        return;
      }
    };

    ws.onclose = (e) => {
      const r = e.reason || '';
      input.disabled = true; sendBtn.disabled = true; uploadBtn.disabled = true; agentBtn.disabled = true;
      ws = null;
      if (pingInterval) { clearInterval(pingInterval); pingInterval = null; }
      resetRunState();
      if (manualDisconnect) {
        setStatus('已断开', '');
      } else {
        setStatus('已断开' + (e.code !== 1000 ? ` (${e.code}${r ? ': '+r : ''})` : ''), 'error');
        scheduleReconnect();
      }
    };

    ws.onerror = () => setStatus('连接错误', 'error');
  }

  function disconnect() {
    manualDisconnect = true;
    cancelReconnect();
    if (ws) { ws.close(); ws = null; }
    setStatus('未连接', '');
    input.disabled = true; sendBtn.disabled = true; uploadBtn.disabled = true; agentBtn.disabled = true;
    resetRunState();
  }

  function sendRpc(method, params) {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      return Promise.reject({ message: 'not connected' });
    }
    const id = String(++reqId);
    return new Promise((resolve, reject) => {
      pending.set(id, { resolve, reject });
      const payload = JSON.stringify({ type: 'req', id, method, params });
      console.log('[ws →]', method, params);
      ws.send(payload);
      setTimeout(() => { if (pending.has(id)) { pending.delete(id); reject({ message: 'timeout' }); } }, 60000);
    });
  }

  // ── History ──
  // ── Pagination ──
  // ── Two-stage history loading ──
  // Stage 1: load last 50 messages for fast initial render
  // Stage 2: user pulls to top → fetch 200 messages, prepend the difference
  const INITIAL_LIMIT = 20;
  const FULL_LIMIT = 200;
  let allMessages = []; // current message cache (from last chat.history call)
  let hasLoadedFull = false; // whether we've done the full (200) fetch
  let isLoadingMore = false;
  let loadMoreEl = null;

  function renderMessageEl(msg) {
    const role = msg.role || '';
    if (role === 'system') return;
    if (role === 'user') {
      const t = stripUserEnvelope(extractText(msg.content));
      const el = t.trim() ? addMessage('user', t) : null;
      if (el && Array.isArray(msg.content)) {
        for (const c of msg.content) {
          if (c.type === 'image') {
            const imgEl = document.createElement('img');
            imgEl.className = 'chat-img';
            let imgSrc = '';
            if (c.source && c.source.data) {
              const mime = c.source.media_type || c.source.mimeType || 'image/png';
              imgSrc = c.source.data.startsWith('data:') ? c.source.data : `data:${mime};base64,${c.source.data}`;
            } else if (c.data) {
              const mime = c.mimeType || c.media_type || 'image/png';
              imgSrc = c.data.startsWith('data:') ? c.data : `data:${mime};base64,${c.data}`;
            } else if (c.url) {
              imgSrc = c.url;
            } else if (c.source && c.source.url) {
              imgSrc = c.source.url;
            }
            if (imgSrc) {
              imgEl.src = imgSrc;
              imgEl.onclick = () => showImageLightbox(imgEl.src);
              el.appendChild(imgEl);
            }
          }
        }
      }
      return;
    }
    if (role === 'assistant') {
      if (Array.isArray(msg.content)) {
        // Check if this message has any tool calls
        const hasToolCalls = msg.content.some(c => c.type === 'toolCall' || c.type === 'tool_use');
        for (const c of msg.content) { if ((c.type === 'toolCall' || c.type === 'tool_use') && c.id) toolCallElements.set(c.id, null); }
        addMessage('assistant', msg.content);
      } else {
        const t = extractText(msg.content);
        if (!t.trim()) return;
        // Skip short "narration" lines that are just tool call introductions
        // (e.g. "Now update the CSS:", "Deploy:", "Let me check:")
        // These are internal thinking that clutter the chat for users
        if (t.trim().length < 80 && /:\s*$/.test(t.trim())) return;
        addMessage('assistant', t);
      }
      return;
    }
    if (role === 'toolResult' || role === 'tool') {
      const tid = msg.tool_use_id || msg.toolCallId;
      const t = extractText(msg.content);
      if (tid) {
        const existing = toolCallElements.get(tid);
        if (existing) {
          // Attach result to existing tool card
          attachToolResult(tid, t);
        } else {
          // No matching tool card found (e.g. truncated history) — render standalone
          const toolName = msg.toolName || msg.name || 'tool';
          const card = createToolCard({ name: toolName, id: tid, arguments: '' });
          // Auto-attach the result
          const rd = card.querySelector('.tool-result');
          const rp = card.querySelector('.tool-result-text');
          if (rd && rp) {
            const maxLen = 2000;
            rp.textContent = t.length > maxLen ? t.substring(0, maxLen) + `\n... (${t.length - maxLen} chars truncated)` : t;
            rd.style.display = '';
          }
          const wrapper = document.createElement('div');
          wrapper.className = 'msg assistant';
          wrapper.style.padding = '4px 8px';
          wrapper.appendChild(card);
          msgBox.appendChild(wrapInRow('assistant', wrapper));
        }
      }
      return;
    }
  }

  function updateLoadMoreBanner() {
    if (!hasLoadedFull) {
      if (!loadMoreEl) {
        loadMoreEl = document.createElement('div');
        loadMoreEl.className = 'msg system';
        loadMoreEl.style.cssText = 'cursor:pointer;text-align:center;padding:10px;color:var(--accent);font-size:12px;user-select:none;';
        loadMoreEl.onclick = () => loadOlderMessages();
      }
      if (!isLoadingMore) {
        loadMoreEl.textContent = '↑ 向上滑动加载更多';
      }
      if (loadMoreEl.parentNode !== msgBox) {
        msgBox.insertBefore(loadMoreEl, msgBox.firstChild);
      }
    } else if (loadMoreEl && loadMoreEl.parentNode) {
      loadMoreEl.parentNode.removeChild(loadMoreEl);
      loadMoreEl = null;
    }
  }

  // Build a simple fingerprint for a message to match across fetches
  function msgFingerprint(msg) {
    const role = msg.role || '';
    const text = extractText(msg.content) || '';
    // Use role + first 80 chars of text content for matching
    return role + ':' + text.substring(0, 80);
  }

  async function loadOlderMessages() {
    if (isLoadingMore || hasLoadedFull) return;
    isLoadingMore = true;
    if (loadMoreEl) {
      loadMoreEl.textContent = '⏳ 加载历史消息中...';
      loadMoreEl.style.color = 'var(--text-dim)';
    }

    try {
      const res = await sendRpc('chat.history', { sessionKey, limit: FULL_LIMIT });
      if (!res || !res.messages) { isLoadingMore = false; return; }

      const fullMessages = res.messages.filter(m => m.role !== 'system');
      hasLoadedFull = true;

      // Find how many new (older) messages we got compared to what's already rendered
      // Strategy: the currently rendered messages should be a suffix of fullMessages
      // Find the offset in fullMessages where our current allMessages start
      const currentFirstFp = allMessages.length > 0 ? msgFingerprint(allMessages[0]) : null;
      let matchIdx = -1;
      if (currentFirstFp) {
        // Search from the end backwards for efficiency
        for (let i = fullMessages.length - allMessages.length; i >= 0; i--) {
          if (msgFingerprint(fullMessages[i]) === currentFirstFp) {
            matchIdx = i;
            break;
          }
        }
      }

      if (matchIdx <= 0) {
        // No older messages to prepend, or can't match
        updateLoadMoreBanner();
        isLoadingMore = false;
        return;
      }

      // Prepend messages [0..matchIdx) to the top of the chat
      const olderMessages = fullMessages.slice(0, matchIdx);
      allMessages = [...olderMessages, ...allMessages];

      // Hide msgBox during prepend to prevent visual flash/scroll jump
      const prevScrollHeight = msgBox.scrollHeight;
      const prevScrollTop = msgBox.scrollTop;
      msgBox.style.overflow = 'hidden'; // freeze scroll rendering

      // Render older messages and collect DOM elements
      const refNode = loadMoreEl && loadMoreEl.parentNode === msgBox
        ? loadMoreEl.nextSibling : msgBox.firstChild;
      const insertedEls = [];
      for (const msg of olderMessages) {
        const beforeLen = msgBox.childElementCount;
        renderMessageEl(msg);
        while (msgBox.childElementCount > beforeLen) {
          const last = msgBox.lastElementChild;
          insertedEls.push(last);
          msgBox.removeChild(last);
        }
      }
      for (const el of insertedEls) {
        msgBox.insertBefore(el, refNode);
      }

      isLoadingMore = false;
      updateLoadMoreBanner();

      // Fix scroll position synchronously — disable smooth scroll to prevent animation
      msgBox.style.scrollBehavior = 'auto';
      const newScrollHeight = msgBox.scrollHeight;
      msgBox.scrollTop = prevScrollTop + (newScrollHeight - prevScrollHeight);
      msgBox.style.overflow = ''; // restore scrolling
      // Restore smooth scroll on next frame
      requestAnimationFrame(() => { msgBox.style.scrollBehavior = ''; });
    } catch (err) {
      console.error('loadOlderMessages failed:', err);
      if (loadMoreEl) {
        loadMoreEl.textContent = '⚠ 加载失败，点击重试';
        loadMoreEl.style.color = 'var(--error)';
      }
      isLoadingMore = false;
    }
  }

  // Scroll-to-top detection: trigger load-more when user pulls to top
  let historyJustLoaded = false;
  msgBox.addEventListener('scroll', () => {
    if (historyJustLoaded) return;
    if (msgBox.scrollTop < 60 && !hasLoadedFull && !isLoadingMore) {
      loadOlderMessages();
    }
  });

  async function loadHistory() {
    try {
      historyJustLoaded = true;
      // Stage 1: fast initial load with small limit
      const res = await sendRpc('chat.history', { sessionKey, limit: INITIAL_LIMIT });
      if (res && res.sessionKey) canonicalKey = res.sessionKey;
      msgBox.innerHTML = '';
      toolCallElements.clear();
      loadMoreEl = null;
      allMessages = [];
      hasLoadedFull = false;

      if (res && res.messages && res.messages.length > 0) {
        empty.classList.add('hidden');
        msgBox.style.display = 'flex';

        allMessages = res.messages.filter(m => m.role !== 'system');
        // If we got fewer than INITIAL_LIMIT, there's nothing older to load
        if (res.messages.length < INITIAL_LIMIT) hasLoadedFull = true;

        for (const msg of allMessages) {
          renderMessageEl(msg);
        }

        updateLoadMoreBanner();
      }
      scrollBottom(true);
      setTimeout(() => { historyJustLoaded = false; }, 300);
    } catch (err) {
      addMessage('system', '加载历史失败: ' + (err.message || err), 'error');
    }
  }

  // ── Image Handling ──
  function genUUID() {
    if (typeof crypto.randomUUID === 'function') return crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
      const r = Math.random() * 16 | 0;
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
  }

  function readFileAsDataUrl(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  async function handleFileSelect(files) {
    for (const file of files) {
      if (!file.type.startsWith('image/')) continue;
      if (file.size > 10 * 1024 * 1024) {
        addMessage('system', `图片 ${file.name} 太大（最大 10MB）`, 'error');
        continue;
      }
      const dataUrl = await readFileAsDataUrl(file);
      const base64 = dataUrl.split(',')[1];
      pendingImages.push({ file, dataUrl, base64, mimeType: file.type, fileName: file.name });
    }
    renderPreviews();
  }

  function renderPreviews() {
    // Keep the label span, remove old previews
    while (previewArea.children.length > 1) previewArea.removeChild(previewArea.lastChild);
    if (pendingImages.length === 0) {
      previewArea.classList.remove('show');
      return;
    }
    previewArea.classList.add('show');
    pendingImages.forEach((img, idx) => {
      const item = document.createElement('div');
      item.className = 'preview-item';
      const imgEl = document.createElement('img');
      imgEl.src = img.dataUrl;
      item.appendChild(imgEl);
      const btn = document.createElement('button');
      btn.className = 'preview-remove';
      btn.textContent = '×';
      btn.onclick = () => { pendingImages.splice(idx, 1); renderPreviews(); };
      item.appendChild(btn);
      previewArea.appendChild(item);
    });
  }

  // ── Send ──
  async function sendMessage() {
    const text = input.value.trim();
    const hasImages = pendingImages.length > 0;
    if (!text && !hasImages) return;
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      addMessage('system', '未连接，请先连接 Gateway', 'error');
      return;
    }

    // Show user message with inline images
    const userEl = addMessage('user', text || '(图片)');
    const imagesToSend = [...pendingImages];
    if (userEl && hasImages) {
      for (const img of imagesToSend) {
        const imgEl = document.createElement('img');
        imgEl.src = img.dataUrl;
        imgEl.className = 'chat-img';
        userEl.appendChild(imgEl);
      }
    }

    input.value = '';
    autoResize();
    pendingImages = [];
    renderPreviews();
    scrollBottom(true); // user just sent a message, force scroll to bottom
    setRunning(true);

    try {
      // Build attachments from pending images (base64, sent via Gateway)
      const attachments = hasImages
        ? imagesToSend.map(img => {
            const base64 = img.dataUrl.split(',')[1];
            return { type: 'image', mimeType: img.mimeType, content: base64 };
          }).filter(a => a.content)
        : undefined;

      const idempotencyKey = genUUID();
      sendRpc('chat.send', {
        sessionKey,
        message: text || '',
        idempotencyKey,
        attachments,
      })
        .then(res => { console.log('[chat.send ack]', res); })
        .catch(err => {
          addMessage('system', '发送失败: ' + (err.message || err), 'error');
          setRunning(false);
        });
    } catch (err) {
      addMessage('system', '发送失败: ' + (err.message || err), 'error');
      setRunning(false);
    }
  }

  function stopGeneration() {
    if (!ws) return;
    sendRpc('chat.abort', { sessionKey }).catch(() => {});
    setRunning(false);
  }

  // ── Run State ──
  function setRunning(v) {
    isRunning = v;
    if (v) {
      typing.classList.add('show');
      sendBtn.style.display = 'none';
      stopBtn.classList.add('show');
      input.disabled = true;
      sendBtn.disabled = true;
      uploadBtn.disabled = true;
    } else {
      streamingEl = null;
      streamBuf = '';
      typing.classList.remove('show');
      sendBtn.style.display = '';
      stopBtn.classList.remove('show');
      input.disabled = !ws;
      sendBtn.disabled = !ws;
      uploadBtn.disabled = !ws;
      input.focus();
    }
  }

  function resetRunState() {
    isRunning = false;
    joinedMidRun = false;
    midRunHistoryLoading = false;
    midRunEventQueue = [];
    if (midRunBannerEl && midRunBannerEl.parentNode) {
      midRunBannerEl.parentNode.removeChild(midRunBannerEl);
      midRunBannerEl = null;
    }
    streamingEl = null;
    streamBuf = '';
    resetTurnState();
    typing.classList.remove('show');
    sendBtn.style.display = '';
    stopBtn.classList.remove('show');
  }

  // ── Chat Event Stream ──
  function matchSession(evtKey) {
    return evtKey === sessionKey || (canonicalKey && evtKey === canonicalKey);
  }

  // Track active tool calls and multi-turn rendering state
  let activeToolCalls = new Map(); // toolCallId -> { el, name, phase }
  let toolContainerEl = null; // current tool group container
  let turnIndex = 0; // tracks the current agent turn (text→tools→text→tools...)
  let lastStreamBufByTurn = new Map(); // turnIndex -> last streamBuf for that turn
  let streamElByTurn = new Map(); // turnIndex -> DOM element for that turn's text

  // Queue for agent events that arrive during mid-run history reload
  let midRunHistoryLoading = false;
  let midRunEventQueue = [];

  function getOrCreateToolContainer() {
    if (!toolContainerEl) {
      toolContainerEl = document.createElement('div');
      toolContainerEl.className = 'msg assistant';
      toolContainerEl.style.padding = '4px 8px';
      msgBox.appendChild(wrapInRow('assistant', toolContainerEl));
      empty.classList.add('hidden');
      msgBox.style.display = 'flex';
    }
    return toolContainerEl;
  }

  // Finalize the current streaming text element (make it permanent)
  function finalizeStreamingEl() {
    if (streamingEl) {
      streamingEl.classList.remove('streaming');
      if (streamBuf) {
        streamingEl.innerHTML = renderMarkdown(streamBuf);
      }
      streamElByTurn.set(turnIndex, streamingEl);
      lastStreamBufByTurn.set(turnIndex, streamBuf);
      streamingEl = null;
      streamBuf = '';
    }
  }

  // Start a new turn: finalize previous text, bump turn counter
  function startNewTurn() {
    finalizeStreamingEl();
    toolContainerEl = null;
    turnIndex++;
  }

  function resetTurnState() {
    activeToolCalls.clear();
    toolContainerEl = null;
    turnIndex = 0;
    lastStreamBufByTurn.clear();
    streamElByTurn.clear();
  }

  function handleAgentEvent(payload) {
    if (!payload) return;
    const evtSession = payload.sessionKey || '';
    if (evtSession && !matchSession(evtSession)) return;

    // Mark that we have agent-level events — chat deltas will be suppressed
    hasAgentEvents = true;

    // Detect mid-run reconnection: receiving agent events without user having sent a message
    if (!isRunning && !joinedMidRun) {
      joinedMidRun = true;
      setRunning(true);
      midRunHistoryLoading = true;
      midRunEventQueue = [];
      // Queue this triggering event too (don't discard it)
      midRunEventQueue.push(payload);
      // Reload history to show completed turns from transcript, then replay queued events
      loadHistory().then(() => {
        midRunHistoryLoading = false;
        // Show reconnect banner
        if (!midRunBannerEl) {
          midRunBannerEl = document.createElement('div');
          midRunBannerEl.className = 'msg system';
          midRunBannerEl.style.cssText = 'text-align:center;padding:6px;font-size:12px;color:var(--text-dim);';
          midRunBannerEl.textContent = '🔄 已重新连接，当前轮次的工具调用将实时显示';
          msgBox.appendChild(midRunBannerEl);
          scrollBottom();
        }
        // Replay queued events that arrived during history load
        const queued = midRunEventQueue;
        midRunEventQueue = [];
        for (const evt of queued) {
          handleAgentEvent(evt);
        }
      });
      return; // Already queued — will be replayed after history loads
    }

    // Queue events while history is reloading during mid-run reconnect
    if (midRunHistoryLoading) {
      midRunEventQueue.push(payload);
      return;
    }

    const stream = payload.stream;
    const data = payload.data || {};

    // Handle assistant text stream from agent events
    if (stream === 'assistant') {
      const text = typeof data.text === 'string' ? data.text : '';
      if (text) {
        streamBuf = text;
        if (!streamingEl) {
          typing.classList.remove('show');
          streamingEl = document.createElement('div');
          streamingEl.className = 'msg assistant streaming';
          msgBox.appendChild(wrapInRow('assistant', streamingEl));
          empty.classList.add('hidden');
          msgBox.style.display = 'flex';
        }
        streamingEl.innerHTML = renderMarkdown(streamBuf);
        scrollBottom();
      }
      return;
    }

    if (stream !== 'tool') return;

    const toolCallId = data.toolCallId || '';
    if (!toolCallId) return;
    const name = data.name || 'tool';
    const phase = data.phase || '';

    if (phase === 'start') {
      // Tool call starting: finalize any current text, then show tool card
      finalizeStreamingEl();

      typing.classList.remove('show');
      const tc = { name, id: toolCallId, arguments: data.args };
      const card = createToolCard(tc);
      const container = getOrCreateToolContainer();
      container.appendChild(card);
      activeToolCalls.set(toolCallId, { el: card, name, phase: 'start' });
      scrollBottom();
    }

    else if (phase === 'update' || phase === 'result') {
      const entry = activeToolCalls.get(toolCallId);
      if (!entry) return;
      const resultText = data.partialResult != null ? formatToolResult(data.partialResult)
                       : data.result != null ? formatToolResult(data.result) : '';
      if (resultText) attachToolResult(toolCallId, resultText);
      if (phase === 'result') {
        entry.phase = 'result';
        // After tool result, prepare for next turn of text
        startNewTurn();
      }
      scrollBottom();
    }
  }

  function formatToolResult(value) {
    if (value === null || value === undefined) return '';
    if (typeof value === 'string') return value;
    if (typeof value === 'number' || typeof value === 'boolean') return String(value);
    if (typeof value === 'object') {
      if (typeof value.text === 'string') return value.text;
      if (Array.isArray(value.content)) {
        return value.content
          .filter(c => c && c.type === 'text' && typeof c.text === 'string')
          .map(c => c.text).join('\n');
      }
    }
    try { return JSON.stringify(value, null, 2); } catch { return String(value); }
  }

  // Track whether we've received any agent-level events for this run.
  // When agent events are active, we ignore chat-level deltas to avoid conflicts.
  let hasAgentEvents = false;
  // Track whether this run was already active when we connected (mid-run reconnect).
  // In that case, tool events before our connection are lost.
  let joinedMidRun = false;
  let midRunBannerEl = null;

  function handleChatEvent(payload) {
    if (!payload) return;
    if (!matchSession(payload.sessionKey || '')) return;
    console.log('[chat event]', payload.state, payload);

    if (payload.state === 'delta') {
      // Detect mid-run reconnection via chat events
      if (!isRunning && !joinedMidRun) {
        joinedMidRun = true;
        setRunning(true);
      }
      // Skip chat deltas when agent events are handling the stream.
      // Agent events provide per-turn text + tool cards; chat deltas are
      // a single accumulated blob that overwrites the multi-turn layout.
      if (hasAgentEvents) return;

      if (payload.message) {
        try {
          const text = extractText(payload.message.content || payload.message);
          if (text) {
            streamBuf = text;
            if (!streamingEl) {
              typing.classList.remove('show');
              streamingEl = document.createElement('div');
              streamingEl.className = 'msg assistant streaming';
              msgBox.appendChild(wrapInRow('assistant', streamingEl));
              empty.classList.add('hidden');
              msgBox.style.display = 'flex';
            }
            streamingEl.innerHTML = renderMarkdown(streamBuf);
            scrollBottom();
          }
        } catch (e) {
          console.error('[delta render error]', e);
        }
      }
    }

    else if (payload.state === 'final') {
      typing.classList.remove('show');
      streamingEl = null;
      streamBuf = '';
      hasAgentEvents = false;
      resetTurnState();
      setRunning(false);
      // Remove mid-run banner if present (history reload will show complete messages)
      if (midRunBannerEl && midRunBannerEl.parentNode) {
        midRunBannerEl.parentNode.removeChild(midRunBannerEl);
        midRunBannerEl = null;
      }
      joinedMidRun = false;
      // Reload full history to get the complete, properly formatted message
      loadHistory();
    }

    else if (payload.state === 'aborted') {
      hasAgentEvents = false;
      if (streamingEl && streamBuf) {
        streamingEl.classList.remove('streaming');
        streamingEl.innerHTML = renderMarkdown(streamBuf + '\n\n⏹ 已停止');
      } else {
        addMessage('system', '⏹ 已停止');
      }
      streamingEl = null;
      streamBuf = '';
      resetTurnState();
      setRunning(false);
    }

    else if (payload.state === 'error') {
      addMessage('system', '❌ ' + (payload.errorMessage || '未知错误'), 'error');
      streamingEl = null;
      streamBuf = '';
      resetTurnState();
      setRunning(false);
    }
  }

  // ── Session Management ──
  let sessionsList = [];

  async function loadSessionsList() {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    try {
      const res = await sendRpc('sessions.list', { includeGlobal: false, includeUnknown: false, includeDerivedTitles: true, includeLastMessage: true });
      if (res && res.sessions) {
        sessionsList = res.sessions;
        renderSessionList();
      }
    } catch (err) {
      console.error('[sessions.list error]', err);
    }
  }

  // Extract agent id from a session key
  function extractAgentId(key) {
    const m = (key || '').match(/^agent:([^:]+):/);
    return m ? m[1] : 'main';
  }

  // Update app logo based on agent info
  function updateAppLogo(agent) {
    // 顶部 logo 始终显示 Paw logo，不随 agent 变化
    // 这个函数现在只用于缓存 agent 信息，不修改 UI
    if (!appLogo) return;
    
    // 缓存 agent 信息供其他地方使用
    if (agent?.identity?.avatar) {
      localStorage.setItem('paw:agent:icon', agent.identity.avatar);
    }
    if (agent?.identity?.emoji) {
      localStorage.setItem('paw:agent:emoji', agent.identity.emoji);
    }
    
    // 始终显示 Paw logo，不替换为 agent 的 emoji/avatar
    appLogo.innerHTML = `<img src="logo.jpg?v=${Date.now()}" style="height:32px;vertical-align:middle;border-radius:4px">`;
  }

  // Clean up a derived title: strip envelope metadata, timestamps, etc.
  function cleanTitle(title) {
    if (!title) return '';
    let t = title;
    // Strip "Conversation info (untrusted metadata)..." blob
    t = t.replace(/^Conversation info \(untrusted[\s\S]*$/i, '');
    // Strip "[Fri 2026-03-06 10:59 GMT+8]" timestamp prefix
    t = t.replace(/^\[(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s+GMT[+-]?\d*\]\s*/i, '');
    // Strip "A new session was started via..."
    t = t.replace(/^A new session was started via\s*/i, '');
    return t.trim();
  }

  // Detect session "kind" for icon and fallback name
  function sessionKindInfo(s) {
    const key = s.key || '';
    const channel = s.channel || s.lastChannel || s.surface || '';
    const chatType = s.chatType || s.origin?.chatType || '';
    const isCron = key.includes(':cron:') || /^cron:/i.test(s.label || '');
    const isDm = chatType === 'direct';
    const isGroup = chatType === 'group';

    if (isCron) return { icon: '⏰', fallbackName: '定时任务' };
    if (isGroup) return { icon: '👥', fallbackName: channel ? `${channel} 群聊` : '群聊' };
    if (isDm && channel === 'telegram') return { icon: '💬', fallbackName: 'Telegram' };
    if (channel === 'webchat') return { icon: '🌐', fallbackName: '网页对话' };
    if (channel) return { icon: '💬', fallbackName: channel };
    return { icon: '💬', fallbackName: '对话' };
  }

  // Check if a string looks like a machine-generated ID (hex, UUID, etc.)
  function looksLikeMachineId(str) {
    if (!str) return true;
    // Strip date suffix like " (2026-03-06)" or " (2026-03-06 14:30)"
    const stripped = str.replace(/\s*\(\d{4}-\d{2}-\d{2}[^)]*\)\s*$/, '').trim();
    if (!stripped) return true;
    // Pure hex (8+ chars), UUID, or hex-prefix patterns
    if (/^[0-9a-f-]{8,}$/i.test(stripped)) return true;
    // Session key fragments like "agent:xiaodai:webchat:..."
    if (/^agent:/.test(stripped)) return true;
    // Channel-prefixed machine IDs like "telegram:g-cidllp1nbe-ntawglsyiqfvyg"
    if (/^(telegram|discord|slack|signal|whatsapp|qqbot|wecom|imessage|googlechat):/i.test(stripped)) return true;
    // Base64-ish strings (mostly lowercase/digits with == suffix)
    if (/^[a-z0-9/+=]{16,}$/i.test(stripped)) return true;
    // Webchat auto-generated names like "webchat:0306-1527"
    if (/^webchat:\d{4}-\d{4}$/.test(stripped)) return true;
    // Cron run IDs like "62fd86a2-3bbf-41fa-a83d-710aade2cdba"
    if (/^[0-9a-f]{8}-[0-9a-f]{4}-/i.test(stripped)) return true;
    return false;
  }

  // Get a friendly display name for a session
  function sessionDisplayName(s) {
    // 1. Clean derivedTitle (from first user message)
    const cleaned = cleanTitle(s.derivedTitle);
    if (cleaned && cleaned.length > 2 && !looksLikeMachineId(cleaned)) {
      return cleaned.length > 30 ? cleaned.substring(0, 30) + '…' : cleaned;
    }
    // 2. Origin label (e.g. "openclaw报告群 - 李智")
    if (s.origin?.label && !looksLikeMachineId(s.origin.label)) return s.origin.label;
    // 3. displayName / label (skip machine IDs)
    if (s.displayName && !looksLikeMachineId(s.displayName)) return s.displayName;
    if (s.label && !looksLikeMachineId(s.label) && !/^cron:/i.test(s.label)) return s.label;
    // 4. For cron sessions, show a more readable name
    if (s.label && /^cron:/i.test(s.label)) {
      // label can be "cron:UUID" or "Cron: 持续工作" or "cron:UUID:run:UUID"
      const cronName = s.label.replace(/^cron:\s*/i, '').replace(/:run:.*/, '').trim();
      if (cronName && !looksLikeMachineId(cronName)) return '⏰ ' + cronName;
    }
    // 5. Generate a friendly name from channel + date
    const kind = sessionKindInfo(s);
    if (s.updatedAt) {
      const d = new Date(s.updatedAt);
      const dateStr = `${d.getMonth()+1}/${d.getDate()} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
      return `${kind.fallbackName} ${dateStr}`;
    }
    return kind.fallbackName;
  }

  // Get subtitle: channel + last message preview (cleaned)
  function sessionSubtitle(s) {
    const channel = s.channel || s.lastChannel || '';
    let preview = s.lastMessagePreview || '';
    // Clean preview too
    preview = cleanTitle(preview);
    if (preview.length > 40) preview = preview.substring(0, 40) + '…';
    const parts = [channel, preview].filter(Boolean);
    return parts.join(' · ');
  }

  const SESSIONS_INITIAL_SHOW = 5; // per agent group, show this many initially
  const expandedGroups = new Set(); // track which agent groups are expanded (show all)
  const collapsedGroups = new Set(); // track which agent groups are collapsed (hidden)

  function createSessionItem(s) {
    const li = document.createElement('li');
    const isActive = s.key === sessionKey || s.key === canonicalKey;
    li.className = 'session-item' + (isActive ? ' active' : '');

    const kind = sessionKindInfo(s);
    const iconEl = document.createElement('span');
    iconEl.className = 'session-item-icon';
    iconEl.textContent = kind.icon;
    li.appendChild(iconEl);

    const info = document.createElement('div');
    info.className = 'session-item-info';

    const keyEl = document.createElement('div');
    keyEl.className = 'session-item-key';
    keyEl.textContent = sessionDisplayName(s);
    info.appendChild(keyEl);

    const sub = sessionSubtitle(s);
    if (sub) {
      const labelEl = document.createElement('div');
      labelEl.className = 'session-item-label';
      labelEl.textContent = sub;
      info.appendChild(labelEl);
    }

    li.appendChild(info);

    const meta = document.createElement('div');
    meta.className = 'session-item-meta';
    if (s.updatedAt) meta.textContent = formatTimeAgo(s.updatedAt);
    li.appendChild(meta);

    if (!isActive) {
      const delBtn = document.createElement('button');
      delBtn.className = 'session-item-delete';
      delBtn.textContent = '×';
      delBtn.title = '删除';
      delBtn.onclick = (e) => { e.stopPropagation(); deleteSessionByKey(s.key); };
      li.appendChild(delBtn);
    }

    li.onclick = () => { switchSession(s.key); };
    return li;
  }

  function renderSessionList() {
    sessionListEl.innerHTML = '';
    const sorted = [...sessionsList].sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0));

    // Group by agent
    const groups = new Map();
    for (const s of sorted) {
      const agentId = extractAgentId(s.key);
      if (!groups.has(agentId)) groups.set(agentId, []);
      groups.get(agentId).push(s);
    }

    function agentLabel(id) {
      const agent = agentsList.find(a => a.id === id);
      const emoji = agent?.identity?.emoji || '🤖';
      const name = agent?.identity?.name || agent?.name || id;
      return `${emoji} ${name}`;
    }

    for (const [agentId, sessions] of groups) {
      const isCollapsed = collapsedGroups.has(agentId);
      const isExpanded = expandedGroups.has(agentId);
      const hasMore = sessions.length > SESSIONS_INITIAL_SHOW;

      // Agent group header (always show when multiple groups)
      if (groups.size > 1) {
        const header = document.createElement('li');
        header.className = 'session-agent-group' + (isCollapsed ? ' collapsed' : '');
        const countBadge = sessions.length > 1 ? `<span class="group-count">${sessions.length}</span>` : '';
        header.innerHTML = `<span>${agentLabel(agentId)}${countBadge}</span><span class="group-toggle">▼</span>`;
        header.onclick = () => {
          if (collapsedGroups.has(agentId)) collapsedGroups.delete(agentId);
          else collapsedGroups.add(agentId);
          renderSessionList();
        };
        sessionListEl.appendChild(header);
      }

      if (isCollapsed) continue;

      // Show limited sessions, with "show more" option
      const limit = isExpanded ? sessions.length : SESSIONS_INITIAL_SHOW;
      const visible = sessions.slice(0, limit);

      for (const s of visible) {
        sessionListEl.appendChild(createSessionItem(s));
      }

      if (hasMore) {
        const toggle = document.createElement('li');
        toggle.className = 'session-show-more';
        if (isExpanded) {
          toggle.textContent = `收起 ↑`;
          toggle.onclick = () => { expandedGroups.delete(agentId); renderSessionList(); };
        } else {
          toggle.textContent = `展开全部 (还有 ${sessions.length - limit} 个) ↓`;
          toggle.onclick = () => { expandedGroups.add(agentId); renderSessionList(); };
        }
        sessionListEl.appendChild(toggle);
      }
    }
  }

  function formatTimeAgo(ts) {
    const diff = Date.now() - ts;
    if (diff < 60000) return '刚刚';
    if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前';
    if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前';
    return Math.floor(diff / 86400000) + '天前';
  }

  function switchSession(newKey) {
    // Don't abort the running task — just reset UI state
    // The task continues running on the server
    if (isRunning) {
      setRunning(false);
    }
    sessionKey = newKey;
    canonicalKey = '';
    cfgSession.value = newKey;
    saveConfig();
    newSessionDialog.classList.remove('show');
    closeSessionDropdown();
    // Reset state
    streamingEl = null;
    streamBuf = '';
    resetTurnState();
    toolCallElements.clear();
    loadHistory();
    renderSessionList();
  }

  function generateSessionName() {
    const now = new Date();
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const dd = String(now.getDate()).padStart(2, '0');
    const hh = String(now.getHours()).padStart(2, '0');
    const mi = String(now.getMinutes()).padStart(2, '0');
    return `webchat:${mm}${dd}-${hh}${mi}`;
  }

  function createNewSession() {
    const name = newSessionKeyInput.value.trim() || generateSessionName();
    const agentId = $('#new-session-agent').value || 'main';
    const key = `agent:${agentId}:${name}`;
    newSessionKeyInput.value = '';
    newSessionDialog.classList.remove('show');
    switchSession(key);
  }

  async function deleteSessionByKey(key) {
    if (!confirm(`确定删除会话 "${key}" 吗？`)) return;
    try {
      await sendRpc('sessions.delete', { key, deleteTranscript: true });
      await loadSessionsList();
    } catch (err) {
      addMessage('system', '删除失败: ' + (err.message || err), 'error');
    }
  }

  // ── Events ──
  $('#clear-btn').onclick = async () => {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    if (!confirm('确定要清除当前会话的上下文吗？会话设置会保留，但所有消息历史将被清空。')) return;
    try {
      await sendRpc('sessions.reset', { key: sessionKey });
      addMessage('system', '✅ 上下文已清除');
      msgBox.innerHTML = '';
      toolCallElements.clear();
      allMessages = [];
      hasLoadedFull = false;
      loadMoreEl = null;
      empty.classList.add('hidden');
      msgBox.style.display = 'flex';
      addMessage('system', '上下文已清除，可以开始新对话');
    } catch (err) {
      addMessage('system', '清除失败: ' + (err.message || err), 'error');
    }
  };
  function closeSettings() { settingsOverlay.classList.remove('show'); }
  function toggleSettings() {
    if (settingsOverlay.classList.contains('show')) {
      closeSettings();
    } else {
      closeSessionDropdown();
      settingsOverlay.classList.add('show');
    }
  }
  $('#settings-btn').onclick = toggleSettings;
  settingsOverlay.onclick = (e) => { if (e.target === settingsOverlay) closeSettings(); };

  // Session dropdown toggle
  const sessionDropdownOverlay = $('#session-dropdown-overlay');
  function closeSessionDropdown() {
    sessionDropdownOverlay.classList.remove('show');
    newSessionDialog.classList.remove('show');
  }
  function toggleSessionDropdown() {
    if (sessionDropdownOverlay.classList.contains('show')) {
      closeSessionDropdown();
    } else {
      closeSettings();
      sessionDropdownOverlay.classList.add('show');
      loadSessionsList();
    }
  }
  $('#sessions-btn').onclick = toggleSessionDropdown;
  // Click overlay background to close
  sessionDropdownOverlay.onclick = (e) => {
    if (e.target === sessionDropdownOverlay) closeSessionDropdown();
  };

  // Load sessions on connect
  function initSidebar() {
    loadSessionsList();
    if (agentsList.length === 0) {
      sendRpc('agents.list', {}).then(res => {
        if (res && res.agents) {
          agentsList = res.agents;
          // Update logo with current agent info
          const curAgentId = agentIdFromSessionKey();
          const curAgent = agentsList.find(a => a.id === curAgentId);
          if (curAgent) updateAppLogo(curAgent);
        }
      }).catch(() => {});
    }
  }
  $('#new-session-btn').onclick = () => {
    const dialog = newSessionDialog;
    dialog.classList.toggle('show');
    if (dialog.classList.contains('show')) {
      const sel = $('#new-session-agent');
      sel.innerHTML = '';
      for (const agent of agentsList) {
        const opt = document.createElement('option');
        opt.value = agent.id;
        const emoji = agent.identity?.emoji || '🤖';
        const name = agent.identity?.name || agent.name || agent.id;
        opt.textContent = `${emoji} ${name}`;
        sel.appendChild(opt);
      }
      const curAgent = agentIdFromSessionKey();
      if (curAgent) sel.value = curAgent;
      setTimeout(() => newSessionKeyInput.focus(), 50);
    }
  };
  $('#create-session-btn').onclick = createNewSession;
  $('#cancel-session-btn').onclick = () => { newSessionDialog.classList.remove('show'); newSessionKeyInput.value = ''; };
  $('#new-session-key').addEventListener('keydown', e => { if (e.key === 'Enter') createNewSession(); });
  $('#connect-btn').onclick = connect;
  $('#disconnect-btn').onclick = disconnect;
  sendBtn.onclick = sendMessage;
  stopBtn.onclick = stopGeneration;
  uploadBtn.onclick = () => fileInput.click();
  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) handleFileSelect(Array.from(fileInput.files));
    fileInput.value = '';
  });
  input.addEventListener('input', autoResize);
  // IME composition guard: ignore Enter during IME input (e.g. Chinese pinyin confirming raw English)
  let isComposing = false;
  input.addEventListener('compositionstart', () => { isComposing = true; });
  input.addEventListener('compositionend', () => { isComposing = false; });
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing && !isComposing) { e.preventDefault(); sendMessage(); }
  });
  // Paste image from clipboard
  input.addEventListener('paste', (e) => {
    const items = e.clipboardData?.items;
    if (!items) return;
    const imageFiles = [];
    for (const item of items) {
      if (item.type.startsWith('image/')) {
        const file = item.getAsFile();
        if (file) imageFiles.push(file);
      }
    }
    if (imageFiles.length > 0) {
      e.preventDefault();
      handleFileSelect(imageFiles);
    }
  });
  // Drag & drop
  const app = $('#app');
  app.addEventListener('dragover', e => { e.preventDefault(); e.dataTransfer.dropEffect = 'copy'; });
  app.addEventListener('drop', e => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
    if (files.length > 0) handleFileSelect(files);
  });

  // ── Theme ──
  const themeBtn = $('#theme-btn');
  function getTheme() {
    return localStorage.getItem('oc-chat-theme') || 'dark';
  }
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    themeBtn.textContent = theme === 'dark' ? '☀️' : '🌙';
    themeBtn.title = theme === 'dark' ? '切换浅色模式' : '切换深色模式';
    localStorage.setItem('oc-chat-theme', theme);
  }
  themeBtn.onclick = () => {
    applyTheme(getTheme() === 'dark' ? 'light' : 'dark');
  };
  applyTheme(getTheme());

  // Load cached agent icon on startup
  // 注意：顶部 logo 始终显示 Paw logo，不随 agent 变化
  // 缓存只用于消息头像，不用于顶部 logo
  (function loadCachedAgentIcon() {
    // 顶部 logo 保持默认 Paw logo，不需要从缓存恢复
    // 缓存的 agent icon/emoji 会在 createAvatar 中使用
  })();

  // ── Agent Management Modal ──
  const agentModal = $('#agent-modal');
  const agentSelect = $('#agent-select');
  const agentModalClose = $('#agent-modal-close');
  const agentSaveBtn = $('#agent-save');
  const agentRevertBtn = $('#agent-revert');
  const agentSaveStatus = $('#agent-save-status');
  const agentFooter = $('#agent-footer');
  const cronRefreshBtn = $('#cron-refresh');
  const cronListContainer = $('#cron-list-container');

  // State
  let agentOriginalData = {}; // snapshot for revert
  let activeTab = 'identity';

  // Tab switching
  document.querySelectorAll('.modal-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.modal-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      activeTab = tab.dataset.tab;
      document.getElementById('tab-' + activeTab).classList.add('active');
      // Show/hide footer (hide for cron tab)
      agentFooter.style.display = activeTab === 'cron' ? 'none' : 'flex';
      // Load cron data if switching to cron tab
      if (activeTab === 'cron') loadCronList();
    });
  });

  // Open modal
  agentBtn.onclick = async () => {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    agentSaveStatus.textContent = '';
    agentSaveStatus.className = 'save-status';
    agentModal.classList.add('show');
    await loadAgentsList();
  };

  // Close modal
  agentModalClose.onclick = () => agentModal.classList.remove('show');
  agentModal.addEventListener('click', e => {
    if (e.target === agentModal) agentModal.classList.remove('show');
  });

  // Extract agentId from session key (format: agent:<agentId>:...)
  function agentIdFromSessionKey() {
    const key = canonicalKey || sessionKey || '';
    const m = key.match(/^agent:([^:]+):/);
    return m ? m[1] : '';
  }

  // Load agents list
  async function loadAgentsList() {
    try {
      const res = await sendRpc('agents.list', {});
      if (!res || !res.agents) return;
      agentsList = res.agents;
      renderAgentSelect();
      // Prioritize: current session's agent > previous selection > default
      const sessionAgent = agentIdFromSessionKey();
      const defaultId = res.defaultId || (agentsList[0] && agentsList[0].id) || 'main';
      const preferred = sessionAgent && agentsList.find(a => a.id === sessionAgent) ? sessionAgent
        : currentAgentId && agentsList.find(a => a.id === currentAgentId) ? currentAgentId
        : defaultId;
      currentAgentId = preferred;
      agentSelect.value = currentAgentId;
      await loadAgentData(currentAgentId);
    } catch (err) {
      console.error('[agents.list error]', err);
    }
  }

  function renderAgentSelect() {
    agentSelect.innerHTML = '';
    for (const agent of agentsList) {
      const opt = document.createElement('option');
      opt.value = agent.id;
      const label = agent.identity?.name || agent.name || agent.id;
      const emoji = agent.identity?.emoji || '';
      opt.textContent = `${emoji} ${label} (${agent.id})`.trim();
      agentSelect.appendChild(opt);
    }
  }

  agentSelect.addEventListener('change', async () => {
    currentAgentId = agentSelect.value;
    agentSaveStatus.textContent = '';
    agentSaveStatus.className = 'save-status';
    await loadAgentData(currentAgentId);
    if (activeTab === 'cron') loadCronList();
  });

  // ── MD Parsers & Builders ──

  // Parse key-value list from markdown (supports **Key:** val and Key: val)
  function parseMdKv(content) {
    const result = {};
    if (!content) return result;
    for (const line of content.split('\n')) {
      // Match "- **Key:** value" (bold wraps key+colon) or "- Key: value"
      const m = line.match(/^-\s+[*][*](.+?):[*][*]\s*(.*)/) || line.match(/^-\s+([^:*]+?):\s*(.*)/);
      if (m) {
        const key = m[1].trim().toLowerCase().replace(/\s+/g, '_');
        const val = m[2].replace(/^_\(.*?\)_$/, '').trim(); // strip _(hint)_ placeholders
        result[key] = val;
      }
    }
    return result;
  }

  // Parse IDENTITY.md
  function parseIdentityMd(content) {
    const kv = parseMdKv(content);
    return {
      name: kv.name || '',
      creature: kv.creature || '',
      vibe: kv.vibe || '',
      emoji: kv.emoji || '',
      avatar: kv.avatar || '',
    };
  }

  function buildIdentityMd(data) {
    const lines = ['# IDENTITY.md', ''];
    if (data.name) lines.push(`- **Name:** ${data.name}`);
    if (data.creature) lines.push(`- **Creature:** ${data.creature}`);
    if (data.vibe) lines.push(`- **Vibe:** ${data.vibe}`);
    if (data.emoji) lines.push(`- **Emoji:** ${data.emoji}`);
    if (data.avatar) lines.push(`- **Avatar:** ${data.avatar}`);
    lines.push('');
    return lines.join('\n');
  }

  // Parse USER.md into structured fields
  function parseUserMd(content) {
    const result = { name: '', callme: '', pronouns: '', timezone: '', notes: '', context: '' };
    if (!content) return result;
    const kv = parseMdKv(content);
    result.name = kv.name || '';
    result.callme = kv.what_to_call_them || '';
    result.pronouns = kv.pronouns || '';
    result.timezone = kv.timezone || '';
    result.notes = kv.notes || '';
    // Extract Context section
    const ctxMatch = content.match(/##\s*Context\s*\n([\s\S]*?)(?=\n##|\n---|\s*$)/i);
    if (ctxMatch) {
      result.context = ctxMatch[1].replace(/^_.*_\s*\n?/gm, '').replace(/^\s*\n/, '').trim();
    }
    return result;
  }

  function buildUserMd(data) {
    const lines = ['# USER.md', ''];
    lines.push(`- **Name:** ${data.name || ''}`);
    lines.push(`- **What to call them:** ${data.callme || ''}`);
    lines.push(`- **Pronouns:** ${data.pronouns || ''}`);
    lines.push(`- **Timezone:** ${data.timezone || ''}`);
    lines.push(`- **Notes:** ${data.notes || ''}`);
    lines.push('');
    lines.push('## Context');
    if (data.context) {
      lines.push('');
      lines.push(data.context);
    }
    lines.push('');
    return lines.join('\n');
  }

  // Parse SOUL.md into structured sections
  function parseSoulMd(content) {
    const result = { core: '', style: '', boundaries: '', skills: '', extra: '' };
    if (!content) return result;

    // Try to extract structured sections
    const sections = {};
    let currentSection = '_header';
    let currentLines = [];

    for (const line of content.split('\n')) {
      const headerMatch = line.match(/^##\s+(.+)/);
      if (headerMatch) {
        sections[currentSection] = currentLines.join('\n').trim();
        currentSection = headerMatch[1].trim().toLowerCase();
        currentLines = [];
      } else {
        currentLines.push(line);
      }
    }
    sections[currentSection] = currentLines.join('\n').trim();

    // Map sections to fields with flexible key matching
    const sectionMap = {
      core: ['核心定位', '你是谁', 'core', 'core truths', 'who you are', '定位', '简介', '角色'],
      style: ['工作风格', '风格', 'style', 'vibe', 'work style', '沟通风格'],
      boundaries: ['边界', '行为边界', 'boundaries', '限制', '规则'],
      skills: ['技术栈', '擅长', 'skills', '能力', '专长', '擅长领域'],
      extra: [],
    };

    const usedSections = new Set(['_header']);

    for (const [field, keys] of Object.entries(sectionMap)) {
      for (const key of keys) {
        for (const [sectionKey, sectionContent] of Object.entries(sections)) {
          if (sectionKey.includes(key) && sectionContent && !usedSections.has(sectionKey)) {
            result[field] = cleanSectionContent(sectionContent);
            usedSections.add(sectionKey);
            break;
          }
        }
        if (result[field]) break;
      }
    }

    // Header text becomes core if core is empty
    if (!result.core && sections['_header']) {
      // Remove the title line (# SOUL.md ...)
      result.core = sections['_header'].replace(/^#\s+.*\n*/m, '').trim();
    }

    // Remaining sections go to extra
    const extraParts = [];
    for (const [key, val] of Object.entries(sections)) {
      if (!usedSections.has(key) && val && key !== '_header') {
        extraParts.push(val);
      }
    }
    if (extraParts.length && !result.extra) {
      result.extra = extraParts.join('\n\n');
    }

    // For skills field, try to extract a comma-separated list from bullet points
    if (result.skills) {
      const bullets = result.skills.match(/^[-*]\s+.+/gm);
      if (bullets) {
        result.skills = bullets.map(b => b.replace(/^[-*]\s+\*\*?/, '').replace(/\*\*.*/, '').replace(/[（(].*/,'')).join('、');
      }
    }

    return result;
  }

  function cleanSectionContent(text) {
    // Remove markdown bold wrappers and leading bullets for display as plain text
    return text.replace(/\*\*(.+?)\*\*/g, '$1').replace(/^[-*]\s+/gm, '• ').trim();
  }

  function buildSoulMd(data, agentName) {
    const title = agentName ? `# SOUL.md - ${agentName}` : '# SOUL.md';
    const lines = [title, ''];

    if (data.core) {
      lines.push(data.core, '');
    }

    if (data.style) {
      lines.push('## 工作风格', '', data.style, '');
    }

    if (data.boundaries) {
      lines.push('## 边界', '', data.boundaries, '');
    }

    if (data.skills) {
      lines.push('## 擅长领域', '');
      // Convert comma/、-separated list to bullet points
      const items = data.skills.split(/[,，、;；]/).map(s => s.trim()).filter(Boolean);
      for (const item of items) lines.push(`- ${item}`);
      lines.push('');
    }

    if (data.extra) {
      lines.push(data.extra, '');
    }

    return lines.join('\n');
  }

  // Fill form from parsed data
  function fillIdentityForm(identity) {
    $('#agent-name').value = identity.name;
    $('#agent-creature').value = identity.creature;
    $('#agent-vibe').value = identity.vibe;
    $('#agent-emoji').value = identity.emoji;
    $('#agent-avatar').value = identity.avatar;
  }

  function fillSoulForm(soul) {
    $('#soul-core').value = soul.core;
    $('#soul-style').value = soul.style;
    $('#soul-boundaries').value = soul.boundaries;
    $('#soul-skills').value = soul.skills;
    $('#soul-extra').value = soul.extra;
  }

  function fillUserForm(user) {
    $('#user-name').value = user.name;
    $('#user-callme').value = user.callme;
    $('#user-pronouns').value = user.pronouns;
    $('#user-timezone').value = user.timezone;
    $('#user-notes').value = user.notes;
    $('#user-context').value = user.context;
  }

  function readIdentityForm() {
    return {
      name: $('#agent-name').value.trim(),
      creature: $('#agent-creature').value.trim(),
      vibe: $('#agent-vibe').value.trim(),
      emoji: $('#agent-emoji').value.trim(),
      avatar: $('#agent-avatar').value.trim(),
    };
  }

  function readSoulForm() {
    return {
      core: $('#soul-core').value.trim(),
      style: $('#soul-style').value.trim(),
      boundaries: $('#soul-boundaries').value.trim(),
      skills: $('#soul-skills').value.trim(),
      extra: $('#soul-extra').value.trim(),
    };
  }

  function readUserForm() {
    return {
      name: $('#user-name').value.trim(),
      callme: $('#user-callme').value.trim(),
      pronouns: $('#user-pronouns').value.trim(),
      timezone: $('#user-timezone').value.trim(),
      notes: $('#user-notes').value.trim(),
      context: $('#user-context').value.trim(),
    };
  }

  // Load a specific agent's data
  async function loadAgentData(agentId) {
    try {
      const [identityRes, soulRes, userRes] = await Promise.all([
        sendRpc('agents.files.get', { agentId, name: 'IDENTITY.md' }),
        sendRpc('agents.files.get', { agentId, name: 'SOUL.md' }),
        sendRpc('agents.files.get', { agentId, name: 'USER.md' }),
      ]);

      const identityContent = identityRes?.file?.content || '';
      const soulContent = soulRes?.file?.content || '';
      const userContent = userRes?.file?.content || '';

      const identity = parseIdentityMd(identityContent);
      const soul = parseSoulMd(soulContent);
      const user = parseUserMd(userContent);

      fillIdentityForm(identity);
      fillSoulForm(soul);
      fillUserForm(user);

      agentOriginalData = {
        identity: { ...identity },
        soul: { ...soul },
        user: { ...user },
        rawIdentity: identityContent,
        rawSoul: soulContent,
        rawUser: userContent,
      };
    } catch (err) {
      console.error('[loadAgentData error]', err);
      agentSaveStatus.textContent = '加载失败: ' + (err.message || err);
      agentSaveStatus.className = 'save-status error';
    }
  }

  // Save
  agentSaveBtn.onclick = async () => {
    if (!currentAgentId) return;
    agentSaveBtn.disabled = true;
    agentSaveStatus.textContent = '保存中...';
    agentSaveStatus.className = 'save-status';

    try {
      const identity = readIdentityForm();
      const soul = readSoulForm();
      const user = readUserForm();

      const identityMd = buildIdentityMd(identity);
      const soulMd = buildSoulMd(soul, identity.name);
      const userMd = buildUserMd(user);

      const saves = [];
      if (identityMd !== agentOriginalData.rawIdentity) {
        saves.push(sendRpc('agents.files.set', { agentId: currentAgentId, name: 'IDENTITY.md', content: identityMd }));
      }
      if (soulMd !== agentOriginalData.rawSoul) {
        saves.push(sendRpc('agents.files.set', { agentId: currentAgentId, name: 'SOUL.md', content: soulMd }));
      }
      if (userMd !== agentOriginalData.rawUser) {
        saves.push(sendRpc('agents.files.set', { agentId: currentAgentId, name: 'USER.md', content: userMd }));
      }

      if (saves.length === 0) {
        agentSaveStatus.textContent = '没有变更';
        agentSaveStatus.className = 'save-status';
        agentSaveBtn.disabled = false;
        return;
      }

      await Promise.all(saves);

      // Update snapshot
      agentOriginalData = {
        identity: { ...identity },
        soul: { ...soul },
        user: { ...user },
        rawIdentity: identityMd,
        rawSoul: soulMd,
        rawUser: userMd,
      };

      agentSaveStatus.textContent = '✅ 已保存';
      agentSaveStatus.className = 'save-status success';
      setTimeout(() => {
        agentSaveStatus.textContent = '';
        agentSaveStatus.className = 'save-status';
      }, 3000);
    } catch (err) {
      agentSaveStatus.textContent = '保存失败: ' + (err.message || err);
      agentSaveStatus.className = 'save-status error';
    } finally {
      agentSaveBtn.disabled = false;
    }
  };

  // Revert
  agentRevertBtn.onclick = () => {
    if (!agentOriginalData.identity) return;
    fillIdentityForm(agentOriginalData.identity);
    fillSoulForm(agentOriginalData.soul);
    fillUserForm(agentOriginalData.user);
    agentSaveStatus.textContent = '已还原';
    agentSaveStatus.className = 'save-status';
    setTimeout(() => { agentSaveStatus.textContent = ''; }, 2000);
  };

  // ── Cron Management ──
  let cronJobs = [];

  async function loadCronList() {
    cronListContainer.innerHTML = '<div class="loading-text">加载中...</div>';
    try {
      const res = await sendRpc('cron.list', { includeDisabled: true });
      cronJobs = (res && res.jobs) || [];
      renderCronList();
    } catch (err) {
      cronListContainer.innerHTML = `<div class="cron-empty">加载失败: ${escHtml(err.message || String(err))}</div>`;
    }
  }

  function formatSchedule(schedule) {
    if (!schedule) return '未知';
    if (schedule.kind === 'cron') return `cron: ${schedule.expr || '?'}${schedule.tz ? ` (${schedule.tz})` : ''}`;
    if (schedule.kind === 'every') {
      const ms = schedule.everyMs || 0;
      if (ms >= 86400000) return `每 ${Math.round(ms/86400000)} 天`;
      if (ms >= 3600000) return `每 ${Math.round(ms/3600000)} 小时`;
      if (ms >= 60000) return `每 ${Math.round(ms/60000)} 分钟`;
      return `每 ${Math.round(ms/1000)} 秒`;
    }
    if (schedule.kind === 'at') {
      try { return `一次性: ${new Date(schedule.at).toLocaleString('zh-CN')}`; } catch {}
      return `一次性: ${schedule.at}`;
    }
    return JSON.stringify(schedule);
  }

  function renderCronList() {
    // Filter jobs by current agent
    const filtered = currentAgentId
      ? cronJobs.filter(j => (j.agentId || 'main') === currentAgentId)
      : cronJobs;
    if (filtered.length === 0) {
      cronListContainer.innerHTML = '<div class="cron-empty">暂无定时任务</div>';
      return;
    }
    const ul = document.createElement('ul');
    ul.className = 'cron-list';
    for (const job of filtered) {
      const li = document.createElement('li');
      li.className = 'cron-item';

      const info = document.createElement('div');
      info.className = 'cron-item-info';
      const nameEl = document.createElement('div');
      nameEl.className = 'cron-item-name';
      nameEl.textContent = job.name || job.id || job.jobId || '未命名任务';
      info.appendChild(nameEl);
      const schedEl = document.createElement('div');
      schedEl.className = 'cron-item-schedule';
      const agentLabel = job.agentId ? `[${job.agentId}] ` : '';
      schedEl.textContent = agentLabel + formatSchedule(job.schedule);
      info.appendChild(schedEl);
      li.appendChild(info);

      const statusEl = document.createElement('span');
      statusEl.className = 'cron-item-status ' + (job.enabled !== false ? 'enabled' : 'disabled');
      statusEl.textContent = job.enabled !== false ? '启用' : '停用';
      li.appendChild(statusEl);

      const actions = document.createElement('div');
      actions.className = 'cron-item-actions';

      // Toggle enable/disable
      const toggleBtn = document.createElement('button');
      toggleBtn.textContent = job.enabled !== false ? '⏸' : '▶';
      toggleBtn.title = job.enabled !== false ? '停用' : '启用';
      toggleBtn.onclick = async () => {
        try {
          await sendRpc('cron.update', { jobId: job.id || job.jobId, patch: { enabled: job.enabled === false } });
          await loadCronList();
        } catch (err) { console.error('[cron.update error]', err); }
      };
      actions.appendChild(toggleBtn);

      // Run now
      const runBtn = document.createElement('button');
      runBtn.textContent = '▶️';
      runBtn.title = '立即执行';
      runBtn.onclick = async () => {
        try {
          await sendRpc('cron.run', { jobId: job.id || job.jobId, mode: 'force' });
          runBtn.textContent = '✅';
          setTimeout(() => { runBtn.textContent = '▶️'; }, 2000);
        } catch (err) { console.error('[cron.run error]', err); }
      };
      actions.appendChild(runBtn);

      // Delete
      const delBtn = document.createElement('button');
      delBtn.className = 'danger';
      delBtn.textContent = '🗑';
      delBtn.title = '删除';
      delBtn.onclick = async () => {
        if (!confirm(`确定删除任务 "${job.name || job.id}" 吗？`)) return;
        try {
          await sendRpc('cron.remove', { jobId: job.id || job.jobId });
          await loadCronList();
        } catch (err) { console.error('[cron.remove error]', err); }
      };
      actions.appendChild(delBtn);

      li.appendChild(actions);
      ul.appendChild(li);
    }
    cronListContainer.innerHTML = '';
    cronListContainer.appendChild(ul);
  }

  cronRefreshBtn.onclick = loadCronList;

  // Cron create form logic
  const cronCreateForm = $('#cron-create-form');
  const cronAddToggle = $('#cron-add-toggle');
  const cronCreateBtn = $('#cron-create-btn');
  const cronCancelBtn = $('#cron-cancel-btn');

  cronAddToggle.onclick = () => {
    cronCreateForm.classList.toggle('show');
    if (cronCreateForm.classList.contains('show')) {
      // Set default datetime to now + 1 hour
      const d = new Date(Date.now() + 3600000);
      const local = new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
      $('#cron-once-time').value = local;
    }
  };

  cronCancelBtn.onclick = () => {
    cronCreateForm.classList.remove('show');
  };

  // Type radio switching
  document.querySelectorAll('input[name="cron-type"]').forEach(radio => {
    radio.addEventListener('change', () => {
      document.querySelectorAll('.cron-type-panel').forEach(p => p.style.display = 'none');
      const panel = document.getElementById('cron-panel-' + radio.value);
      if (panel) panel.style.display = '';
    });
  });

  // Create cron job
  cronCreateBtn.onclick = async () => {
    const name = $('#cron-new-name').value.trim();
    const message = $('#cron-new-message').value.trim();
    if (!message) {
      alert('请填写执行内容');
      return;
    }

    const type = document.querySelector('input[name="cron-type"]:checked')?.value || 'once';
    let schedule;

    if (type === 'once') {
      const timeVal = $('#cron-once-time').value;
      if (!timeVal) { alert('请选择执行时间'); return; }
      schedule = { kind: 'at', at: new Date(timeVal).toISOString() };
    } else if (type === 'every') {
      const val = parseInt($('#cron-every-val').value) || 1;
      const unit = parseInt($('#cron-every-unit').value) || 86400000;
      schedule = { kind: 'every', everyMs: val * unit };
    } else if (type === 'cron') {
      const expr = $('#cron-expr').value.trim();
      if (!expr) { alert('请填写 Cron 表达式'); return; }
      schedule = { kind: 'cron', expr, tz: Intl.DateTimeFormat().resolvedOptions().timeZone };
    }

    cronCreateBtn.disabled = true;
    cronCreateBtn.textContent = '创建中...';

    try {
      await sendRpc('cron.add', {
        name: name || undefined,
        agentId: currentAgentId || undefined,
        schedule,
        payload: { kind: 'agentTurn', message },
        sessionTarget: 'isolated',
        enabled: true,
      });
      cronCreateForm.classList.remove('show');
      // Reset form
      $('#cron-new-name').value = '';
      $('#cron-new-message').value = '';
      await loadCronList();
    } catch (err) {
      alert('创建失败: ' + (err.message || err));
    } finally {
      cronCreateBtn.disabled = false;
      cronCreateBtn.textContent = '创建';
    }
  };

  // ── Download offline package ──
  const downloadBtn = $('#download-btn');
  if (downloadBtn) {
    downloadBtn.addEventListener('click', async () => {
      downloadBtn.disabled = true;
      downloadBtn.textContent = '打包中...';
      try {
        await downloadOfflineZip();
      } catch (err) {
        alert('下载失败: ' + (err.message || err));
      } finally {
        downloadBtn.disabled = false;
        downloadBtn.textContent = '📦 下载离线版';
      }
    });
  }

  async function downloadOfflineZip() {
    // Resolve the current HTML filename from the URL path
    const pathParts = location.pathname.split('/');
    const htmlFile = pathParts[pathParts.length - 1] || 'index.html';

    // All files to pack — fetch raw source files (not DOM snapshots)
    const files = [
      { name: 'paw/index.html', url: htmlFile },
      { name: 'paw/paw-app.js', url: 'paw-app.js' },
      { name: 'paw/marked.min.js', url: 'marked.min.js' },
      { name: 'paw/highlight.min.js', url: 'highlight.min.js' },
      { name: 'paw/github-dark.min.css', url: 'github-dark.min.css' },
      { name: 'paw/start.sh', url: 'start.sh' },
      { name: 'paw/start.bat', url: 'start.bat' },
    ];

    // Fetch all files in parallel (raw source, no runtime state)
    const fetched = await Promise.all(files.map(async (f) => {
      const resp = await fetch(f.url, { cache: 'reload' });
      if (!resp.ok) throw new Error(`Failed to fetch ${f.name}: ${resp.status}`);
      return { name: f.name, data: new Uint8Array(await resp.arrayBuffer()) };
    }));

    // Generate README.md for the offline package
    const readmeText = generateReadme();
    fetched.push({ name: 'paw/README.md', data: new TextEncoder().encode(readmeText) });

    // Generate LICENSE
    const licenseText = generateLicense();
    fetched.push({ name: 'paw/LICENSE', data: new TextEncoder().encode(licenseText) });

    // Build zip using store (no compression) — simple and fast
    const zipBlob = buildZip(fetched);

    // Trigger download
    const a = document.createElement('a');
    a.href = URL.createObjectURL(zipBlob);
    a.download = 'paw.zip';
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  function generateReadme() {
    return `# 🐾 Paw

A standalone web chat frontend for [OpenClaw](https://github.com/openclaw/openclaw).
Zero build tools, zero backend — just static files that connect to any OpenClaw Gateway via WebSocket.

## Quick Start

### macOS / Linux

\`\`\`bash
cd paw
chmod +x start.sh
./start.sh
\`\`\`

### Windows

Double-click \`start.bat\` (requires [Python](https://www.python.org/downloads/)).

### Manual

\`\`\`bash
cd paw
python3 -m http.server 8080
# Open http://localhost:8080
\`\`\`

> ⚠️ **Do not open index.html directly** (double-click). The \`file://\` protocol
> is blocked by the Gateway. Always use a local HTTP server.

## First-Time Setup

1. Start the local server (see above)
2. Open the URL shown in your terminal (default: http://localhost:8080)
3. Click ⚙ **Settings** in the top-right corner
4. Fill in:
   - **Gateway URL**: \`wss://<your-gateway-host>:<port>\` (e.g. \`wss://192.168.1.100:30100\`)
   - **Token**: your Gateway authentication token
5. Click **Connect**

### Where to find your Gateway URL and Token

On the machine running OpenClaw:

\`\`\`bash
# Show Gateway status (includes URL)
openclaw status

# Show current config (includes token)
openclaw config get gateway.auth.token
\`\`\`

Or check your \`~/.openclaw/config.yaml\`:

\`\`\`yaml
gateway:
  bind: "0.0.0.0"
  port: 30100          # → wss://<host>:30100
  auth:
    mode: token
    token: "your-token" # ← paste this into Paw
\`\`\`

### Device Pairing

On first connection from a new device, you may need to approve it:

\`\`\`bash
openclaw devices list      # list pending requests
openclaw devices approve <id>  # approve
\`\`\`

Connections from localhost are auto-approved.

## Files

| File | Description |
|------|-------------|
| \`index.html\` | Main application |
| \`paw-app.js\` | Core logic (WebSocket, UI, offline packaging) |
| \`marked.min.js\` | Markdown parser ([marked](https://github.com/markedjs/marked) v15) |
| \`highlight.min.js\` | Syntax highlighting ([highlight.js](https://highlightjs.org/) v11) |
| \`github-dark.min.css\` | Code block dark theme |
| \`start.sh\` | Quick-start script for macOS/Linux |
| \`start.bat\` | Quick-start script for Windows |

## Deploy to Gateway (optional)

Instead of running a separate server, you can serve Paw directly from your Gateway:

\`\`\`bash
UIROOT="$(openclaw config get gateway.controlUi.root 2>/dev/null || echo ~/.openclaw/control-ui-static)"
cp index.html "$UIROOT/chat.html"
cp paw-app.js marked.min.js highlight.min.js github-dark.min.css "$UIROOT/"
\`\`\`

Then access at \`https://<gateway-host>:<port>/<basePath>/chat.html\`.

## Links

- OpenClaw: https://github.com/openclaw/openclaw
- Docs: https://docs.openclaw.ai
- Community: https://discord.com/invite/clawd

## License

MIT — see LICENSE file.
`;
  }

  function generateLicense() {
    const year = new Date().getFullYear();
    return `MIT License

Copyright (c) ${year} OpenClaw Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
`;
  }

  // Minimal ZIP builder (store mode, no compression)
  function buildZip(files) {
    const entries = [];
    let offset = 0;

    // Build local file entries
    for (const f of files) {
      const nameBytes = new TextEncoder().encode(f.name);
      const crc = crc32(f.data);

      // Local file header (30 + name + data)
      const header = new ArrayBuffer(30 + nameBytes.length);
      const hv = new DataView(header);
      hv.setUint32(0, 0x04034b50, true);  // signature
      hv.setUint16(4, 20, true);           // version needed
      hv.setUint16(6, 0, true);            // flags
      hv.setUint16(8, 0, true);            // compression: store
      hv.setUint16(10, 0, true);           // mod time
      hv.setUint16(12, 0, true);           // mod date
      hv.setUint32(14, crc, true);         // crc32
      hv.setUint32(18, f.data.length, true); // compressed size
      hv.setUint32(22, f.data.length, true); // uncompressed size
      hv.setUint16(26, nameBytes.length, true); // name length
      hv.setUint16(28, 0, true);           // extra length
      new Uint8Array(header).set(nameBytes, 30);

      entries.push({ nameBytes, crc, size: f.data.length, headerOffset: offset, header: new Uint8Array(header), data: f.data });
      offset += header.byteLength + f.data.length;
    }

    // Build central directory
    const cdParts = [];
    let cdSize = 0;
    for (const e of entries) {
      const cd = new ArrayBuffer(46 + e.nameBytes.length);
      const cv = new DataView(cd);
      cv.setUint32(0, 0x02014b50, true);  // signature
      cv.setUint16(4, 20, true);           // version made by
      cv.setUint16(6, 20, true);           // version needed
      cv.setUint16(8, 0, true);            // flags
      cv.setUint16(10, 0, true);           // compression: store
      cv.setUint16(12, 0, true);           // mod time
      cv.setUint16(14, 0, true);           // mod date
      cv.setUint32(16, e.crc, true);       // crc32
      cv.setUint32(20, e.size, true);      // compressed size
      cv.setUint32(24, e.size, true);      // uncompressed size
      cv.setUint16(28, e.nameBytes.length, true); // name length
      cv.setUint16(30, 0, true);           // extra length
      cv.setUint16(32, 0, true);           // comment length
      cv.setUint16(34, 0, true);           // disk number
      cv.setUint16(36, 0, true);           // internal attrs
      cv.setUint32(38, 0, true);           // external attrs
      cv.setUint32(42, e.headerOffset, true); // local header offset
      new Uint8Array(cd).set(e.nameBytes, 46);
      cdParts.push(new Uint8Array(cd));
      cdSize += cd.byteLength;
    }

    // End of central directory
    const eocd = new ArrayBuffer(22);
    const ev = new DataView(eocd);
    ev.setUint32(0, 0x06054b50, true);    // signature
    ev.setUint16(4, 0, true);             // disk number
    ev.setUint16(6, 0, true);             // cd start disk
    ev.setUint16(8, entries.length, true); // entries on disk
    ev.setUint16(10, entries.length, true);// total entries
    ev.setUint32(12, cdSize, true);        // cd size
    ev.setUint32(16, offset, true);        // cd offset
    ev.setUint16(20, 0, true);            // comment length

    // Combine all parts
    const parts = [];
    for (const e of entries) { parts.push(e.header, e.data); }
    for (const cd of cdParts) { parts.push(cd); }
    parts.push(new Uint8Array(eocd));

    return new Blob(parts, { type: 'application/zip' });
  }

  // CRC32 (standard polynomial)
  function crc32(data) {
    let crc = 0xFFFFFFFF;
    // Build table on first use
    if (!crc32.table) {
      crc32.table = new Uint32Array(256);
      for (let i = 0; i < 256; i++) {
        let c = i;
        for (let j = 0; j < 8; j++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
        crc32.table[i] = c;
      }
    }
    const t = crc32.table;
    for (let i = 0; i < data.length; i++) {
      crc = t[(crc ^ data[i]) & 0xFF] ^ (crc >>> 8);
    }
    return (crc ^ 0xFFFFFFFF) >>> 0;
  }

  // ── Init ──
  loadConfig();
  if (cfgUrl.value && cfgToken.value) connect();
  else settingsPanel.classList.add('show');
})();
