(function () {
  const CONFIG = window.GATEWAY_CONFIG || {
    openclawBase: "http://127.0.0.1:18789",
    tokenLoaded: false,
    defaultUser: "Alex",
    users: ["Alex", "Sam", "Family"],
    googleMapsEmbedApiKey: "",
  };

  const state = {
    activeUser: CONFIG.defaultUser,
    histories: {},
    thinking: false,
  };

  const shortcutPrompts = {
    agenda: "What are my events today?",
    home: "Give me a global status of the house.",
    weather: "What is the current weather and today's forecast?",
    diag: "Run a quick diagnostic of OpenClaw and the gateway.",
  };

  const dom = {
    body: document.body,
    messagesEl: document.getElementById("messages"),
    chatScroll: document.getElementById("chatScroll"),
    messageInput: document.getElementById("messageInput"),
    sendBtn: document.getElementById("sendBtn"),
    inputState: document.getElementById("inputState"),
    userPills: document.getElementById("userPills"),
    baseUrlLabel: document.getElementById("baseUrlLabel"),
    tokenLoadedLabel: document.getElementById("tokenLoadedLabel"),
    activeUserLabel: document.getElementById("activeUserLabel"),
    hudUserChip: document.getElementById("hudUserChip"),
    clearChatBtn: document.getElementById("clearChatBtn"),
    floatingWindows: document.getElementById("floatingWindows"),
  };

  let zCounter = 100;

  function hasCoreDom() {
    return !!(dom.messagesEl && dom.chatScroll && dom.messageInput && dom.sendBtn && dom.userPills && dom.baseUrlLabel && dom.tokenLoadedLabel && dom.activeUserLabel && dom.hudUserChip && dom.clearChatBtn && dom.floatingWindows);
  }

  function escapeHtml(text) {
    return String(text ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function ensureHistory(user) {
    if (!state.histories[user]) state.histories[user] = [];
    return state.histories[user];
  }

  function autoScroll() {
    if (!dom.chatScroll) return;
    requestAnimationFrame(() => {
      dom.chatScroll.scrollTop = 0;
    });
  }

  function autoResizeTextarea() {
    if (!dom.messageInput) return;
    dom.messageInput.style.height = "auto";
    dom.messageInput.style.height = `${Math.min(dom.messageInput.scrollHeight, 220)}px`;
  }

  function setThinking(flag) {
    state.thinking = !!flag;
    dom.body?.classList.toggle("thinking", state.thinking);
    if (dom.inputState) dom.inputState.textContent = state.thinking ? "Thinking..." : "Ready";
    if (dom.sendBtn) dom.sendBtn.disabled = state.thinking;
    autoScroll();
  }

  function renderMessages() {
    if (!dom.messagesEl) return;
    const history = [...ensureHistory(state.activeUser)].reverse();
    dom.messagesEl.innerHTML = history.map((msg) => `
      <div class="message-row ${msg.role === "user" ? "user" : "assistant"}">
        <div class="bubble">${escapeHtml(msg.content).replace(/\n/g, "<br>")}</div>
      </div>
    `).join("");

    if (dom.activeUserLabel) dom.activeUserLabel.textContent = state.activeUser;
    if (dom.hudUserChip) dom.hudUserChip.textContent = `USER: ${String(state.activeUser).toUpperCase()}`;
    autoScroll();
  }

  function setActiveUser(user) {
    state.activeUser = user;
    ensureHistory(user);
    renderUserPills();
    renderMessages();
    if (dom.messageInput) {
      dom.messageInput.value = "";
      autoResizeTextarea();
      dom.messageInput.focus();
    }
    persistState();
  }

  function renderUserPills() {
    if (!dom.userPills) return;
    dom.userPills.innerHTML = CONFIG.users.map((user) => `<button type="button" class="user-pill ${user === state.activeUser ? "active" : ""}" data-user="${escapeHtml(user)}">${escapeHtml(user)}</button>`).join("");
    dom.userPills.querySelectorAll(".user-pill").forEach((btn) => btn.addEventListener("click", () => setActiveUser(btn.dataset.user)));
  }

  async function persistState() {
    try {
      await fetch("/api/state", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ activeUser: state.activeUser, histories: state.histories }),
      });
    } catch (err) {
      console.warn("persist error", err);
    }
  }

  async function loadState() {
    try {
      const res = await fetch("/api/state");
      const data = await res.json();
      if (data && typeof data === "object") {
        state.activeUser = data.activeUser || CONFIG.defaultUser;
        state.histories = data.histories || {};
      }
    } catch (err) {
      console.warn("load state error", err);
    }
    ensureHistory(state.activeUser);
    renderUserPills();
    renderMessages();
  }

  function appendMessage(role, content, user = state.activeUser) {
    ensureHistory(user).push({ role, content });
    if (user === state.activeUser) renderMessages();
    persistState();
  }

  function initHeader() {
    if (dom.baseUrlLabel) dom.baseUrlLabel.textContent = CONFIG.openclawBase || "-";
    if (dom.tokenLoadedLabel) dom.tokenLoadedLabel.textContent = CONFIG.tokenLoaded ? "yes" : "no";
    if (dom.activeUserLabel) dom.activeUserLabel.textContent = state.activeUser;
    if (dom.hudUserChip) dom.hudUserChip.textContent = `USER: ${String(state.activeUser).toUpperCase()}`;
  }

  function bindShortcuts() {
    document.querySelectorAll("[data-shortcut]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const prompt = shortcutPrompts[btn.dataset.shortcut];
        if (prompt && dom.messageInput) {
          dom.messageInput.value = prompt;
          autoResizeTextarea();
          dom.messageInput.focus();
        }
      });
    });
  }

  function focusWindow(win) {
    win.style.zIndex = String(++zCounter);
  }

  function applyWindowSizing(win) {
    win.style.width = `${Math.min(window.innerWidth - 48, 920)}px`;
    win.style.height = `${Math.min(window.innerHeight - 48, 640)}px`;
  }

  function makeDraggable(win, handle) {
    let isDragging = false;
    let offsetX = 0;
    let offsetY = 0;

    handle?.addEventListener("mousedown", (event) => {
      isDragging = true;
      focusWindow(win);
      offsetX = event.clientX - win.offsetLeft;
      offsetY = event.clientY - win.offsetTop;
    });

    document.addEventListener("mousemove", (event) => {
      if (!isDragging) return;
      win.style.left = `${Math.max(12, event.clientX - offsetX)}px`;
      win.style.top = `${Math.max(12, event.clientY - offsetY)}px`;
    });

    document.addEventListener("mouseup", () => {
      isDragging = false;
    });
  }

  function buildFloatingWindow(id, title) {
    const existing = document.getElementById(id);
    if (existing) {
      focusWindow(existing);
      return existing;
    }

    const win = document.createElement("div");
    win.className = "floating-window active";
    win.id = id;
    win.style.left = `${Math.max(24, Math.round((window.innerWidth - 920) / 2))}px`;
    win.style.top = `${Math.max(24, Math.round((window.innerHeight - 640) / 2))}px`;
    win.style.zIndex = String(++zCounter);
    applyWindowSizing(win);
    win.innerHTML = `
      <div class="floating-window-header">
        <div class="floating-window-title">
          <span class="floating-window-dot"></span>
          <span>${escapeHtml(title)}</span>
        </div>
        <div class="floating-window-actions">
          <button type="button" class="floating-window-btn" data-action="reload">↻</button>
          <button type="button" class="floating-window-btn" data-action="close">✕</button>
        </div>
      </div>
      <div class="floating-window-body"></div>
    `;
    dom.floatingWindows.appendChild(win);

    const header = win.querySelector(".floating-window-header");
    makeDraggable(win, header);
    win.addEventListener("mousedown", () => focusWindow(win));
    win.querySelector('[data-action="close"]')?.addEventListener("click", () => win.remove());
    win.querySelector('[data-action="reload"]')?.addEventListener("click", () => {
      if (typeof win.__reloadHandler__ === "function") win.__reloadHandler__();
    });
    focusWindow(win);
    return win;
  }

  function setWindowHtml(win, html) {
    const body = win.querySelector(".floating-window-body");
    if (body) body.innerHTML = html;
  }

  function setWindowFallback(win, title, launchUrl, extraHtml = "") {
    setWindowHtml(win, `
      <div class="floating-window-fallback" style="padding:20px; height:100%; overflow:auto;">
        <h3 style="margin-top:0;">${escapeHtml(title)}</h3>
        <p>The integrated view is not available for this page.</p>
        ${extraHtml}
        <p style="margin-top:16px;"><a class="floating-window-link" href="${launchUrl}" target="_blank" rel="noreferrer">Open in Google Maps</a></p>
      </div>
    `);
  }

  function setWindowFrame(win, url, title, launchUrl, extraHtml = "") {
    setWindowHtml(win, `<iframe class="floating-window-frame" src="${url}" referrerpolicy="no-referrer-when-downgrade" loading="lazy" style="width:100%;height:100%;border:0;"></iframe>`);
    const iframe = win.querySelector("iframe");
    const timer = setTimeout(() => {
      try {
        const currentUrl = iframe?.contentWindow?.location?.href;
        if (!currentUrl || currentUrl === "about:blank") setWindowFallback(win, title, launchUrl, extraHtml);
      } catch (_err) {
      }
    }, 3000);
    iframe?.addEventListener("load", () => clearTimeout(timer));
  }

  function openIntegratedWindow({ id, title, url, launchUrl = "", extraHtml = "" }) {
    const win = buildFloatingWindow(id, title);
    setWindowFrame(win, url, title, launchUrl || url, extraHtml);
    win.__reloadHandler__ = () => setWindowFrame(win, url, title, launchUrl || url, extraHtml);
    return win;
  }

  function buildGoogleMapsLaunchUrl(origin = "", destination = "") {
    if (!String(origin).trim() || !String(destination).trim()) return "https://www.google.com/maps";
    return `https://www.google.com/maps/dir/?api=1&origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}`;
  }

  function buildGoogleMapsEmbedUrl(origin = "", destination = "", mode = "driving") {
    const key = String(CONFIG.googleMapsEmbedApiKey || "").trim();
    if (!key || !String(origin).trim() || !String(destination).trim()) return "";
    return `https://www.google.com/maps/embed/v1/directions?key=${encodeURIComponent(key)}&origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}&mode=${encodeURIComponent(mode)}`;
  }

  function openWebSearch(query = "") {
    const url = query ? `https://www.google.com/search?q=${encodeURIComponent(query)}` : "https://www.google.com";
    return openIntegratedWindow({ id: "gateway-window-web", title: query ? `Web · ${query}` : "Web", url, launchUrl: url });
  }

  function openMapSearch(query = "") {
    const launchUrl = query ? `https://www.google.com/maps?q=${encodeURIComponent(query)}` : "https://www.google.com/maps";
    const key = String(CONFIG.googleMapsEmbedApiKey || "").trim();
    const embedUrl = key && query ? `https://www.google.com/maps/embed/v1/search?key=${encodeURIComponent(key)}&q=${encodeURIComponent(query)}` : "";
    if (embedUrl) return openIntegratedWindow({ id: "gateway-window-map", title: query ? `Map · ${query}` : "Map", url: embedUrl, launchUrl });
    const win = buildFloatingWindow("gateway-window-map", query ? `Map · ${query}` : "Map");
    setWindowFallback(win, query ? `Map · ${query}` : "Map", launchUrl, query ? `<div style="margin-top:14px; padding:12px; border:1px solid rgba(255,255,255,0.12); border-radius:12px;"><strong>Search</strong><br>${escapeHtml(query)}</div>` : "");
    win.__reloadHandler__ = () => setWindowFallback(win, query ? `Map · ${query}` : "Map", launchUrl);
    return win;
  }

  function openRoute(origin = "", destination = "") {
    const launchUrl = buildGoogleMapsLaunchUrl(origin, destination);
    const embedUrl = buildGoogleMapsEmbedUrl(origin, destination);
    const hasRoute = String(origin).trim() && String(destination).trim();
    const title = hasRoute ? "Route" : "Map";
    const routeHtml = hasRoute ? `<div style="margin-top:14px; padding:12px; border:1px solid rgba(255,255,255,0.12); border-radius:12px;"><div style="margin-bottom:10px;"><strong>Origin</strong><br>${escapeHtml(origin)}</div><div><strong>Destination</strong><br>${escapeHtml(destination)}</div></div>` : "";
    if (embedUrl) return openIntegratedWindow({ id: "gateway-window-route", title, url: embedUrl, launchUrl, extraHtml: routeHtml });
    const win = buildFloatingWindow("gateway-window-route", title);
    setWindowFallback(win, title, launchUrl, `<p>Missing Google Maps Embed API key or incomplete route.</p>${routeHtml}`);
    win.__reloadHandler__ = () => setWindowFallback(win, title, launchUrl, `<p>Missing Google Maps Embed API key or incomplete route.</p>${routeHtml}`);
    return win;
  }

  function openRouteSearch(query = "") {
    const launchUrl = query ? `https://www.google.com/maps/dir/${encodeURIComponent(query)}` : "https://www.google.com/maps";
    const key = String(CONFIG.googleMapsEmbedApiKey || "").trim();
    if (key && query) {
      const embedUrl = `https://www.google.com/maps/embed/v1/search?key=${encodeURIComponent(key)}&q=${encodeURIComponent(query)}`;
      return openIntegratedWindow({ id: "gateway-window-route-search", title: `Route · ${query}`, url: embedUrl, launchUrl, extraHtml: `<div style="margin-top:14px; padding:12px; border:1px solid rgba(255,255,255,0.12); border-radius:12px;"><strong>Query</strong><br>${escapeHtml(query)}</div>` });
    }
    const win = buildFloatingWindow("gateway-window-route-search", query ? `Route · ${query}` : "Route");
    setWindowFallback(win, query ? `Route · ${query}` : "Route", launchUrl, query ? `<div style="margin-top:14px; padding:12px; border:1px solid rgba(255,255,255,0.12); border-radius:12px;"><strong>Query</strong><br>${escapeHtml(query)}</div>` : "");
    win.__reloadHandler__ = () => setWindowFallback(win, query ? `Route · ${query}` : "Route", launchUrl);
    return win;
  }

  function bindWindowButtons() {
    dom.clearChatBtn?.addEventListener("click", async () => {
      state.histories[state.activeUser] = [];
      renderMessages();
      await persistState();
    });
  }

  function bindTextarea() {
    dom.messageInput?.addEventListener("input", autoResizeTextarea);
  }

  if (!hasCoreDom()) {
    console.error("Incomplete DOM for GatewayUI", dom);
    return;
  }

  window.GatewayUI = { CONFIG, state, dom, escapeHtml, appendMessage, autoResizeTextarea, autoScroll, setThinking, loadState, persistState, renderMessages, renderUserPills, setActiveUser, openWebSearch, openMapSearch, openRouteSearch, openRoute };

  initHeader();
  bindShortcuts();
  bindWindowButtons();
  bindTextarea();
  loadState();
  autoResizeTextarea();
  dom.messageInput?.focus();
})();
