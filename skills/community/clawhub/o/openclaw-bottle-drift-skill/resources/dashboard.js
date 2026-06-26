const BASE_URL = window.location.origin;
const STORAGE_KEY = "bottle-drift-dashboard-profile-v2";
const HEARTBEAT_MS = 30 * 1000;

const els = {
  baseUrl: document.getElementById("baseUrl"),
  userId: document.getElementById("userId"),
  displayName: document.getElementById("displayName"),
  callbackUrl: document.getElementById("callbackUrl"),
  acceptBottles: document.getElementById("acceptBottles"),
  saveIdentityBtn: document.getElementById("saveIdentityBtn"),
  heartbeatBtn: document.getElementById("heartbeatBtn"),
  identityStatus: document.getElementById("identityStatus"),
  messageText: document.getElementById("messageText"),
  messageCounter: document.getElementById("messageCounter"),
  fanout: document.getElementById("fanout"),
  ttlHours: document.getElementById("ttlHours"),
  sendBtn: document.getElementById("sendBtn"),
  sendStatus: document.getElementById("sendStatus"),
  refreshAllBtn: document.getElementById("refreshAllBtn"),
  refreshInboxBtn: document.getElementById("refreshInboxBtn"),
  onlineCount: document.getElementById("onlineCount"),
  onlineList: document.getElementById("onlineList"),
  receivedList: document.getElementById("receivedList"),
  repliesList: document.getElementById("repliesList"),
  sentList: document.getElementById("sentList"),
};

let heartbeatTimer = null;
let refreshTimer = null;

function showStatus(element, type, message) {
  element.className = `status show ${type}`;
  element.textContent = message;
}

function clearStatus(element) {
  element.className = "status";
  element.textContent = "";
}

function saveProfile() {
  const profile = {
    userId: els.userId.value.trim(),
    displayName: els.displayName.value.trim(),
    callbackUrl: els.callbackUrl.value.trim(),
    acceptBottles: !!els.acceptBottles.checked,
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(profile));
  return profile;
}

function loadProfile() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function applyProfile(profile) {
  if (!profile) return;
  els.userId.value = profile.userId || "";
  els.displayName.value = profile.displayName || "";
  els.callbackUrl.value = profile.callbackUrl || "";
  els.acceptBottles.checked = profile.acceptBottles !== false;
}

function requireProfile() {
  const profile = saveProfile();
  if (!profile.userId || !profile.displayName) {
    showStatus(els.identityStatus, "err", "请先填写用户 ID 和展示昵称。");
    return null;
  }
  clearStatus(els.identityStatus);
  return profile;
}

async function api(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json; charset=utf-8" },
    cache: "no-store",
    ...options,
  });
  const data = await res.json().catch(() => ({ ok: false, error: "invalid server response" }));
  if (!res.ok || data.ok === false) {
    throw new Error(data.error || `request failed (${res.status})`);
  }
  return data;
}

function renderEmpty(container, text) {
  container.innerHTML = `<div class="empty">${text}</div>`;
}

function htmlEscape(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function heartbeat(showOk = false) {
  const profile = requireProfile();
  if (!profile) return null;
  const data = await api(`${BASE_URL}/api/presence/heartbeat`, {
    method: "POST",
    body: JSON.stringify({
      user_id: profile.userId,
      display_name: profile.displayName,
      callback_url: profile.callbackUrl || null,
      accept_bottles: profile.acceptBottles,
    }),
  });
  if (showOk) {
    showStatus(
      els.identityStatus,
      "ok",
      `上线成功：${profile.displayName}（${profile.userId}）\n最近心跳已刷新。`
    );
  }
  return data;
}

async function refreshOnline() {
  const profile = loadProfile();
  const exclude = profile?.userId ? `?exclude=${encodeURIComponent(profile.userId)}` : "";
  const data = await api(`${BASE_URL}/api/users/online${exclude}`);
  const users = data.online_users || [];
  els.onlineCount.textContent = `${users.length} 人`;
  if (!users.length) {
    renderEmpty(els.onlineList, "目前还没有其他在线订阅者。");
    return;
  }
  els.onlineList.innerHTML = users.map((user) => `
    <div class="item">
      <div class="item-grid">
        <div>
          <h4>${htmlEscape(user.display_name || user.displayName || user.user_id)}</h4>
          <div class="meta">用户 ID：${htmlEscape(user.user_id)}</div>
        </div>
        <span class="pill">最近在线：${htmlEscape(user.last_seen_text)}</span>
      </div>
    </div>
  `).join("");
}

function receivedItemHtml(item, displayName) {
  const replyBoxId = `reply-${item.delivery_id}`;
  const replierName = htmlEscape(displayName || "");
  return `
    <div class="item">
      <div class="item-grid">
        <div>
          <h4>来自 ${htmlEscape(item.sender_name)}</h4>
          <div class="meta">瓶子 ID：${htmlEscape(item.bottle_id)} · 收到于 ${htmlEscape(item.delivered_at_text)}</div>
        </div>
        <span class="pill">${item.has_replied ? "已回信" : "待回信"}</span>
      </div>
      <div class="message">${htmlEscape(item.message)}</div>
      <div class="actions">
        <button class="secondary" type="button" data-toggle-reply="${htmlEscape(replyBoxId)}">${item.has_replied ? "查看回信状态" : "直接回信"}</button>
        <a class="button-link ghost" href="${htmlEscape(item.reply_url)}" target="_blank" rel="noopener">打开专属回信页</a>
      </div>
      <div class="reply-box ${item.has_replied ? "show" : ""}" id="${htmlEscape(replyBoxId)}">
        ${item.has_replied ? `<div class="status show ok">这个漂流瓶已经回信成功，默认不再接受第二次回信。</div>` : `
        <label>你的昵称
          <input class="reply-name" value="${replierName}" maxlength="40" placeholder="你的昵称">
        </label>
        <label>你的回信
          <textarea class="reply-text" maxlength="240" placeholder="写下你的回应"></textarea>
        </label>
        <div class="actions">
          <button class="primary" type="button" data-reply-token="${htmlEscape(item.reply_token)}">发送回信</button>
        </div>
        <div class="status" data-reply-status="${htmlEscape(item.delivery_id)}"></div>`}
      </div>
    </div>
  `;
}

function replyItemHtml(item) {
  return `
    <div class="item">
      <div class="item-grid">
        <div>
          <h4>${htmlEscape(item.replier_name)} 的回信</h4>
          <div class="meta">瓶子 ID：${htmlEscape(item.bottle_id)} · ${htmlEscape(item.created_at_text)}</div>
        </div>
        <span class="pill">来自 ${htmlEscape(item.recipient_id)}</span>
      </div>
      <div class="message">${htmlEscape(item.reply_text)}</div>
    </div>
  `;
}

function sentItemHtml(item) {
  const deliveries = (item.deliveries || []).map((delivery) => `
    <div class="item" style="margin-top:10px;">
      <div class="item-grid">
        <div>
          <h4>送达给 ${htmlEscape(delivery.recipient_name || delivery.recipient_id)}</h4>
          <div class="meta">送达时间：${htmlEscape(delivery.delivered_at_text)}</div>
        </div>
        <span class="pill">${delivery.has_reply ? "已收到回信" : "等待回信"}</span>
      </div>
      <div class="actions">
        <a class="button-link ghost" href="${htmlEscape(delivery.reply_url)}" target="_blank" rel="noopener">打开该条回信链接</a>
      </div>
    </div>
  `).join("");
  return `
    <div class="item">
      <div class="item-grid">
        <div>
          <h4>瓶子 ${htmlEscape(item.bottle_id)}</h4>
          <div class="meta">发出于 ${htmlEscape(item.created_at_text)} · 有效至 ${htmlEscape(item.expires_at_text)}</div>
        </div>
        <span class="pill">回信 ${item.reply_count || 0}/${(item.deliveries || []).length}</span>
      </div>
      <div class="message">${htmlEscape(item.message)}</div>
      ${deliveries || `<div class="empty">暂时还没有送达记录。</div>`}
    </div>
  `;
}

async function refreshInbox() {
  const profile = requireProfile();
  if (!profile) {
    renderEmpty(els.receivedList, "先保存身份，再查看收件箱。");
    renderEmpty(els.repliesList, "先保存身份，再查看回信。");
    renderEmpty(els.sentList, "先保存身份，再查看发件箱。");
    return;
  }
  const data = await api(`${BASE_URL}/api/inbox/${encodeURIComponent(profile.userId)}`);
  const received = data.received_bottles || [];
  const replies = data.replies_received || [];
  const sent = data.sent_bottles || [];

  els.receivedList.innerHTML = received.length
    ? received.map((item) => receivedItemHtml(item, profile.displayName)).join("")
    : `<div class="empty">你还没有收到新的漂流瓶。</div>`;

  els.repliesList.innerHTML = replies.length
    ? replies.map(replyItemHtml).join("")
    : `<div class="empty">你发出去的瓶子还没有收到回信。</div>`;

  els.sentList.innerHTML = sent.length
    ? sent.map(sentItemHtml).join("")
    : `<div class="empty">你还没有扔出任何漂流瓶。</div>`;
}

async function refreshAll(showStatusText = false) {
  try {
    await heartbeat(false);
    await Promise.all([refreshOnline(), refreshInbox()]);
    if (showStatusText) {
      showStatus(els.sendStatus, "info", "面板已刷新。");
    }
  } catch (error) {
    showStatus(els.sendStatus, "err", error.message);
  }
}

async function sendBottle() {
  const profile = requireProfile();
  if (!profile) return;

  const message = els.messageText.value.trim();
  if (!message) {
    showStatus(els.sendStatus, "err", "请先写下赠言。");
    return;
  }

  try {
    await heartbeat(false);
    const data = await api(`${BASE_URL}/api/bottles/send`, {
      method: "POST",
      body: JSON.stringify({
        sender_id: profile.userId,
        sender_name: profile.displayName,
        message,
        fanout: Number(els.fanout.value),
        ttl_seconds: Number(els.ttlHours.value) * 3600,
      }),
    });
    const recipients = (data.deliveries || []).map((d) => d.recipient_name || d.recipient_id).join("、");
    els.messageText.value = "";
    updateCounter();
    showStatus(
      els.sendStatus,
      "ok",
      `漂流瓶已送出。\n瓶子 ID：${data.bottle_id}\n本次送达：${recipients || "无"}`
    );
    await refreshInbox();
    await refreshOnline();
  } catch (error) {
    showStatus(els.sendStatus, "err", error.message);
  }
}

async function sendReply(button) {
  const box = button.closest(".reply-box");
  const nameInput = box.querySelector(".reply-name");
  const textInput = box.querySelector(".reply-text");
  const statusEl = box.querySelector(".status");
  const token = button.dataset.replyToken;

  const replierName = nameInput.value.trim();
  const replyText = textInput.value.trim();

  if (!replierName || !replyText) {
    showStatus(statusEl, "err", "请填写昵称和回信内容。");
    return;
  }

  try {
    await api(`${BASE_URL}/api/bottles/reply`, {
      method: "POST",
      body: JSON.stringify({
        token,
        replier_name: replierName,
        reply_text: replyText,
      }),
    });
    showStatus(statusEl, "ok", "回信已送达。这个漂流瓶默认不再接受第二次回信。");
    textInput.value = "";
    await refreshInbox();
  } catch (error) {
    showStatus(statusEl, "err", error.message);
  }
}

function updateCounter() {
  els.messageCounter.textContent = String(els.messageText.value.length);
}

function attachEvents() {
  els.saveIdentityBtn.addEventListener("click", async () => {
    try {
      saveProfile();
      await heartbeat(true);
      await refreshOnline();
      await refreshInbox();
      startLoops();
    } catch (error) {
      showStatus(els.identityStatus, "err", error.message);
    }
  });

  els.heartbeatBtn.addEventListener("click", async () => {
    try {
      saveProfile();
      await heartbeat(true);
      await refreshOnline();
    } catch (error) {
      showStatus(els.identityStatus, "err", error.message);
    }
  });

  els.sendBtn.addEventListener("click", sendBottle);
  els.refreshAllBtn.addEventListener("click", () => refreshAll(true));
  els.refreshInboxBtn.addEventListener("click", refreshInbox);
  els.messageText.addEventListener("input", updateCounter);

  document.addEventListener("click", (event) => {
    const toggle = event.target.closest("[data-toggle-reply]");
    if (toggle) {
      const box = document.getElementById(toggle.dataset.toggleReply);
      if (box) box.classList.toggle("show");
      return;
    }

    const replyBtn = event.target.closest("[data-reply-token]");
    if (replyBtn) {
      sendReply(replyBtn);
    }
  });
}

function startLoops() {
  if (heartbeatTimer) clearInterval(heartbeatTimer);
  if (refreshTimer) clearInterval(refreshTimer);

  heartbeatTimer = setInterval(() => {
    heartbeat(false).catch(() => {});
  }, HEARTBEAT_MS);

  refreshTimer = setInterval(() => {
    Promise.all([refreshOnline(), refreshInbox()]).catch(() => {});
  }, HEARTBEAT_MS);
}

function init() {
  els.baseUrl.textContent = BASE_URL;
  applyProfile(loadProfile());
  updateCounter();
  attachEvents();

  if (els.userId.value && els.displayName.value) {
    heartbeat(false)
      .then(() => Promise.all([refreshOnline(), refreshInbox()]))
      .then(() => startLoops())
      .catch(() => {
        renderEmpty(els.onlineList, "保存身份后将自动展示在线订阅者。");
        renderEmpty(els.receivedList, "保存身份后可查看收件箱。");
        renderEmpty(els.repliesList, "保存身份后可查看回信。");
        renderEmpty(els.sentList, "保存身份后可查看发件箱。");
      });
  } else {
    renderEmpty(els.onlineList, "保存身份后将自动展示在线订阅者。");
    renderEmpty(els.receivedList, "保存身份后可查看收件箱。");
    renderEmpty(els.repliesList, "保存身份后可查看回信。");
    renderEmpty(els.sentList, "保存身份后可查看发件箱。");
  }
}

init();
