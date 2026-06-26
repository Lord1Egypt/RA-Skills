/**
 * OK Bridge - Background Service Worker
 *
 * 连接 Python bridge server（ws://localhost:9334），接收命令并执行：
 * - navigate / wait_for_load: chrome.tabs.update + onUpdated
 * - evaluate / has_element 等: chrome.scripting.executeScript (MAIN world)
 * - click / input 等 DOM 操作: chrome.tabs.sendMessage → content.js
 * - screenshot: chrome.tabs.captureVisibleTab
 * - get_cookies: chrome.cookies.getAll
 */

const BRIDGE_URL = "ws://localhost:9334";
let ws = null;

// 保持 service worker 存活
chrome.alarms.create("keepAlive", { periodInMinutes: 0.4 });
chrome.alarms.onAlarm.addListener(() => {
  if (!ws || ws.readyState !== WebSocket.OPEN) connect();
});

// ───────────────────────── WebSocket ─────────────────────────

function connect() {
  if (ws && (ws.readyState === WebSocket.CONNECTING || ws.readyState === WebSocket.OPEN)) return;

  ws = new WebSocket(BRIDGE_URL);

  ws.onopen = () => {
    console.log("[OK Bridge] 已连接到 bridge server");
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
    console.log("[OK Bridge] 连接断开，3s 后重连...");
    setTimeout(connect, 3000);
  };

  ws.onerror = (e) => {
    console.error("[OK Bridge] WS 错误", e);
  };
}

// ───────────────────────── 命令路由 ─────────────────────────

async function handleCommand(msg) {
  const { method, params = {} } = msg;

  switch (method) {
    case "navigate":
      return await cmdNavigate(params);

    case "wait_for_load":
      return await cmdWaitForLoad(params);

    case "screenshot_element":
      return await cmdScreenshot(params);

    case "set_file_input":
      return await cmdSetFileInputViaDebugger(params);

    case "get_cookies":
      return await cmdGetCookies(params);

    case "evaluate":
    case "wait_dom_stable":
    case "wait_for_selector":
    case "has_element":
    case "get_elements_count":
    case "get_element_text":
    case "get_element_attribute":
    case "get_scroll_top":
    case "get_viewport_height":
    case "get_url":
      return await cmdEvaluateInMainWorld(method, params);

    // DOM 操作（在页面 MAIN world 执行）
    default:
      return await cmdDomInMainWorld(method, params);
  }
}

// ───────────────────────── 导航 ─────────────────────────

async function cmdNavigate({ url }) {
  const tab = await getOrOpenOkTab();
  await chrome.tabs.update(tab.id, { url });
  await waitForTabComplete(tab.id, url, 60000);
  return null;
}

async function cmdWaitForLoad({ timeout = 60000 }) {
  const tab = await getOrOpenOkTab();
  await waitForTabComplete(tab.id, null, timeout);
  return null;
}

async function waitForTabComplete(tabId, expectedUrlPrefix, timeout) {
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

// ───────────────────────── 截图 ─────────────────────────

async function cmdScreenshot() {
  const tab = await getOrOpenOkTab();
  const dataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, { format: "png" });
  return { data: dataUrl.split(",")[1] };
}

// ───────────────────────── Cookies ─────────────────────────

async function cmdGetCookies({ domain = "ok.com" }) {
  return await chrome.cookies.getAll({ domain });
}

// ───────────────────────── MAIN world JS 执行 ─────────────────────────

async function cmdEvaluateInMainWorld(method, params) {
  const tab = await getOrOpenOkTab();
  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    world: "MAIN",
    func: mainWorldExecutor,
    args: [method, params],
  });
  const r = results?.[0]?.result;
  if (r && typeof r === "object" && "__ok_error" in r) {
    throw new Error(r.__ok_error);
  }
  return r;
}

function mainWorldExecutor(method, params) {
  function poll(check, interval, timeout) {
    return new Promise((resolve, reject) => {
      const start = Date.now();
      (function tick() {
        const result = check();
        if (result !== false && result !== null && result !== undefined) {
          resolve(result);
          return;
        }
        if (Date.now() - start >= timeout) {
          reject(new Error("超时"));
          return;
        }
        setTimeout(tick, interval);
      })();
    });
  }

  switch (method) {
    case "evaluate": {
      try {
        // eslint-disable-next-line no-new-func
        return Function(`"use strict"; return (${params.expression})`)();
      } catch (e) {
        return { __ok_error: `JS 执行错误: ${e.message}` };
      }
    }

    case "has_element":
      return document.querySelector(params.selector) !== null;

    case "get_elements_count":
      return document.querySelectorAll(params.selector).length;

    case "get_element_text": {
      const el = document.querySelector(params.selector);
      return el ? el.textContent : null;
    }

    case "get_element_attribute": {
      const el = document.querySelector(params.selector);
      return el ? el.getAttribute(params.attr) : null;
    }

    case "get_scroll_top":
      return window.pageYOffset || document.documentElement.scrollTop || 0;

    case "get_viewport_height":
      return window.innerHeight;

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
          if (size === last && size > 0) { resolve(null); return; }
          last = size;
          if (Date.now() - start >= timeout) { resolve(null); return; }
          setTimeout(tick, interval);
        })();
      });
    }

    case "wait_for_selector": {
      const timeout = params.timeout || 30000;
      return poll(
        () => document.querySelector(params.selector) ? true : false,
        200,
        timeout,
      ).catch(() => { throw new Error(`等待元素超时: ${params.selector}`); });
    }

    default:
      return { __ok_error: `未知 MAIN world 方法: ${method}` };
  }
}

// ───────────────────────── 文件上传（chrome.debugger + CDP） ─────────

async function cmdSetFileInputViaDebugger({ selector, files }) {
  const tab = await getOrOpenOkTab();
  const target = { tabId: tab.id };

  await chrome.debugger.attach(target, "1.3");
  try {
    const { root } = await chrome.debugger.sendCommand(target, "DOM.getDocument", {});
    const { nodeId } = await chrome.debugger.sendCommand(target, "DOM.querySelector", {
      nodeId: root.nodeId,
      selector,
    });
    if (!nodeId) throw new Error(`文件输入框不存在: ${selector}`);

    await chrome.debugger.sendCommand(target, "DOM.setFileInputFiles", {
      nodeId,
      files,
    });
  } finally {
    await chrome.debugger.detach(target).catch(() => {});
  }
  return null;
}

// ───────────────────────── DOM 操作转发 ─────────────────────────

async function cmdDomInMainWorld(method, params) {
  const tab = await getOrOpenOkTab();
  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    world: "MAIN",
    func: domExecutor,
    args: [method, params],
  });
  const r = results?.[0]?.result;
  if (r && typeof r === "object" && "__ok_error" in r) {
    throw new Error(r.__ok_error);
  }
  return r;
}

function domExecutor(method, params) {
  function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

  switch (method) {
    case "click_element": {
      const el = document.querySelector(params.selector);
      if (!el) return { __ok_error: `元素不存在: ${params.selector}` };
      el.scrollIntoView({ block: "center" });
      el.click();
      return null;
    }

    case "input_text": {
      const el = document.querySelector(params.selector);
      if (!el) return { __ok_error: `元素不存在: ${params.selector}` };
      el.focus();
      
      const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
      if (nativeInputValueSetter) {
        nativeInputValueSetter.call(el, params.text);
      } else {
        el.value = params.text;
      }
      
      el.dispatchEvent(new Event("input", { bubbles: true }));
      el.dispatchEvent(new Event("change", { bubbles: true }));
      return null;
    }

    case "input_content_editable": {
      const el = document.querySelector(params.selector);
      if (!el) return { __ok_error: `元素不存在: ${params.selector}` };
      el.focus();
      document.execCommand("selectAll", false, null);
      document.execCommand("delete", false, null);
      if (params.text) document.execCommand("insertText", false, params.text);
      return null;
    }

    case "scroll_by":
      window.scrollBy(params.x || 0, params.y || 0);
      return null;

    case "scroll_to":
      window.scrollTo(params.x || 0, params.y || 0);
      return null;

    case "scroll_to_bottom":
      window.scrollTo(0, document.body.scrollHeight);
      return null;

    case "scroll_element_into_view": {
      const el = document.querySelector(params.selector);
      if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
      return null;
    }

    case "hover_element": {
      const el = document.querySelector(params.selector);
      if (el) {
        const rect = el.getBoundingClientRect();
        const x = rect.left + rect.width / 2;
        const y = rect.top + rect.height / 2;
        el.dispatchEvent(new MouseEvent("mouseover", { clientX: x, clientY: y, bubbles: true }));
        el.dispatchEvent(new MouseEvent("mousemove", { clientX: x, clientY: y, bubbles: true }));
      }
      return null;
    }

    case "mouse_click": {
      const el = document.elementFromPoint(params.x, params.y);
      if (el) {
        el.dispatchEvent(new MouseEvent("mousedown", { clientX: params.x, clientY: params.y, bubbles: true }));
        el.dispatchEvent(new MouseEvent("mouseup", { clientX: params.x, clientY: params.y, bubbles: true }));
        el.dispatchEvent(new MouseEvent("click", { clientX: params.x, clientY: params.y, bubbles: true }));
      }
      return null;
    }

    case "press_key": {
      const keyMap = {
        Enter: { key: "Enter", code: "Enter", keyCode: 13 },
        ArrowDown: { key: "ArrowDown", code: "ArrowDown", keyCode: 40 },
        Tab: { key: "Tab", code: "Tab", keyCode: 9 },
        Backspace: { key: "Backspace", code: "Backspace", keyCode: 8 },
      };
      const info = keyMap[params.key] || { key: params.key, code: params.key, keyCode: 0 };
      const active = document.activeElement || document.body;
      active.dispatchEvent(new KeyboardEvent("keydown", { ...info, bubbles: true }));
      active.dispatchEvent(new KeyboardEvent("keyup", { ...info, bubbles: true }));
      return null;
    }

    case "remove_element": {
      const el = document.querySelector(params.selector);
      if (el) el.remove();
      return null;
    }

    case "select_all_text": {
      const el = document.querySelector(params.selector);
      if (el) {
        el.focus();
        if (el.select) el.select();
        else document.execCommand("selectAll");
      }
      return null;
    }

    default:
      return { __ok_error: `未知命令: ${method}` };
  }
}

// ───────────────────────── Tab 管理 ─────────────────────────

async function getOrOpenOkTab() {
  // 优先使用当前窗口的活动 ok.com 标签，确保用户能看到自动化过程
  const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (activeTab && activeTab.url && /^https:\/\/[^/]+\.ok\.com\//.test(activeTab.url)) {
    return activeTab;
  }

  const tabs = await chrome.tabs.query({ url: "https://*.ok.com/*" });
  if (tabs.length > 0) {
    await chrome.tabs.update(tabs[0].id, { active: true });
    return tabs[0];
  }
  const tab = await chrome.tabs.create({ url: "https://sg.ok.com/en/city-singapore/", active: true });
  await waitForTabComplete(tab.id, "https://sg.ok.com", 60000);
  return await chrome.tabs.get(tab.id);
}

// 启动连接
connect();
