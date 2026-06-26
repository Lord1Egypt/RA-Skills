const BRIDGE_URL = "ws://localhost:9335";
let ws = null;

chrome.alarms.create("keepAlive", { periodInMinutes: 0.4 });
chrome.alarms.onAlarm.addListener(() => {
  if (!ws || ws.readyState !== WebSocket.OPEN) connect();
});

function connect() {
  if (ws && (ws.readyState === WebSocket.CONNECTING || ws.readyState === WebSocket.OPEN)) return;

  ws = new WebSocket(BRIDGE_URL);

  ws.onopen = () => {
    console.log("[Gumtree Bridge] 已连接到 bridge server");
    ws.send(JSON.stringify({ role: "extension" }));
  };

  ws.onmessage = async (event) => {
    let msg;
    try {
      msg = JSON.parse(event.data);
    } catch {
      return;
    }

    try {
      const result = await handleCommand(msg);
      ws.send(JSON.stringify({ id: msg.id, result: result ?? null }));
    } catch (err) {
      ws.send(JSON.stringify({ id: msg.id, error: String(err.message || err) }));
    }
  };

  ws.onclose = () => {
    console.log("[Gumtree Bridge] 连接断开，3s 后重连...");
    setTimeout(connect, 3000);
  };

  ws.onerror = (event) => {
    console.error("[Gumtree Bridge] WS 错误", event);
  };
}

async function handleCommand(msg) {
  const { method, params = {} } = msg;

  switch (method) {
    case "navigate":
      return await cmdNavigate(params);
    case "wait_for_load":
      return await cmdWaitForLoad(params);
    case "evaluate":
    case "wait_dom_stable":
    case "get_url":
      return await cmdEvaluateInMainWorld(method, params);
    default:
      throw new Error(`未知命令: ${method}`);
  }
}

async function cmdNavigate({ url }) {
  const tab = await getOrOpenGumtreeTab();
  await chrome.tabs.update(tab.id, { url, active: true });
  await waitForTabComplete(tab.id, url, 60000);
  return null;
}

async function cmdWaitForLoad({ timeout = 60000 }) {
  const tab = await getOrOpenGumtreeTab();
  await waitForTabComplete(tab.id, null, timeout);
  return null;
}

function waitForTabComplete(tabId, expectedUrlPrefix, timeout) {
  return new Promise((resolve, reject) => {
    const deadline = Date.now() + timeout;

    function listener(id, info, updatedTab) {
      if (id !== tabId) return;
      if (info.status !== "complete") return;
      if (expectedUrlPrefix && !updatedTab.url?.startsWith(expectedUrlPrefix.slice(0, 20))) return;
      chrome.tabs.onUpdated.removeListener(listener);
      resolve();
    }

    chrome.tabs.onUpdated.addListener(listener);

    const poll = async () => {
      if (Date.now() > deadline) {
        chrome.tabs.onUpdated.removeListener(listener);
        reject(new Error("页面加载超时"));
        return;
      }
      const tab = await chrome.tabs.get(tabId).catch(() => null);
      if (tab && tab.status === "complete") {
        chrome.tabs.onUpdated.removeListener(listener);
        resolve();
        return;
      }
      setTimeout(poll, 400);
    };

    setTimeout(poll, 600);
  });
}

async function cmdEvaluateInMainWorld(method, params) {
  const tab = await getOrOpenGumtreeTab();
  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    world: "MAIN",
    func: mainWorldExecutor,
    args: [method, params],
  });
  const result = results?.[0]?.result;
  if (result && typeof result === "object" && "__gumtree_error" in result) {
    throw new Error(result.__gumtree_error);
  }
  return result ?? null;
}

async function mainWorldExecutor(method, params) {
  switch (method) {
    case "evaluate": {
      try {
        return await Promise.resolve(
          Function(`"use strict"; return (${params.expression})`)()
        );
      } catch (err) {
        return { __gumtree_error: `JS 执行错误: ${err.message}` };
      }
    }
    case "get_url":
      return window.location.href;
    case "wait_dom_stable": {
      const timeout = params.timeout || 10000;
      const interval = params.interval || 500;
      return new Promise((resolve) => {
        let last = -1;
        const start = Date.now();
        (function tick() {
          const size = document.body ? document.body.innerHTML.length : 0;
          if (size === last && size > 0) {
            resolve(null);
            return;
          }
          last = size;
          if (Date.now() - start >= timeout) {
            resolve(null);
            return;
          }
          setTimeout(tick, interval);
        })();
      });
    }
    default:
      return { __gumtree_error: `未知 MAIN world 方法: ${method}` };
  }
}

async function getOrOpenGumtreeTab() {
  const tabs = await chrome.tabs.query({
    url: [
      "https://www.gumtree.com/*",
      "https://gumtree.com/*"
    ]
  });
  if (tabs.length > 0) return tabs[0];
  const tab = await chrome.tabs.create({ url: "https://www.gumtree.com/" });
  await waitForTabComplete(tab.id, null, 30000);
  return tab;
}

connect();
