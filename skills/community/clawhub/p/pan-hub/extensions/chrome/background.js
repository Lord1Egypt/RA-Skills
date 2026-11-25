// 后台 service worker：右键菜单 + 桥接到本机 pan serve（127.0.0.1:17890）
const BASE = "http://127.0.0.1:17890";
const MENU_ID = "pan-dl-send";

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.removeAll(() => {
    chrome.contextMenus.create({
      id: MENU_ID,
      title: "发送 网盘链接 到 pan 下载",
      contexts: ["selection", "page", "link", "editable"]
    });
  });
});

async function loadDefaults() {
  const stored = await chrome.storage.local.get(["pwd", "to", "engine", "tier", "path"]);
  return {
    pwd: stored.pwd || "",
    to: stored.to || "",
    engine: stored.engine || "",
    tier: stored.tier || "",
    path: stored.path || ""
  };
}

function pickUrl(text) {
  const items = String(text || "").split(/\s+/).filter((s) => /^https?:\/\//i.test(s));
  return items[0] || "";
}

async function sendToPan(url, opts) {
  const body = { url: (url || "").trim() };
  if (opts.pwd) body.pwd = opts.pwd;
  if (opts.to) body.to = opts.to;
  if (opts.engine) body.engine = opts.engine;
  if (opts.tier) body.tier = opts.tier;
  if (opts.path) body.path = opts.path;
  const resp = await fetch(BASE + "/api/download", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  return await resp.json();
}

function notify(title, message) {
  try {
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icons/icon128.png",
      title: title,
      message: message
    });
  } catch (e) {
    console.log("notify failed", e);
  }
}

async function downloadFromText(text) {
  const url = pickUrl(text);
  if (!url) {
    notify("pan 下载", "未找到可用链接");
    return { ok: false, error: "no url" };
  }
  const opts = await loadDefaults();
  const data = await sendToPan(url, opts);
  notify("pan 下载", data.ok ? "已开始：" + url : "失败：" + (data.error || "未知错误"));
  return data;
}

chrome.contextMenus.onClicked.addListener(async (info) => {
  const text = info.linkUrl || info.selectionText || (info.menuItemId === MENU_ID ? (info.pageUrl || "") : "");
  await downloadFromText(text);
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg && msg.type === "PAN_DOWNLOAD_URL") {
    (async () => {
      const data = await downloadFromText(msg.url || "");
      sendResponse(data);
    })();
    return true;
  }
  return false;
});
