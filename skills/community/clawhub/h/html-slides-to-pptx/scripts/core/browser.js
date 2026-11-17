// core/browser.js — Playwright 生命周期
const { chromium } = require("playwright");

async function launchPage(config) {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: config.viewport.width, height: config.viewport.height },
    // 截图 DPI:capture.scale 提升位图密度(clip 坐标仍 CSS px,提取几何不受影响)
    deviceScaleFactor: (config.capture && config.capture.scale) || 1,
  });
  return { browser, page };
}

// 带容错的页面加载:优先 networkidle(等字体/图片稳定);
// 页面含挂起的第三方脚本(统计/追踪类)时,networkidle 可能永不触发 ——
// 封顶 timeoutMs 后降级继续(本地内容早已就绪,不影响提取),并警告提示。
async function gotoSettled(page, url, { timeoutMs = 10000 } = {}) {
  try {
    await page.goto(url, { waitUntil: "networkidle", timeout: timeoutMs });
  } catch (e) {
    if (e.name !== "TimeoutError") throw e;
    console.warn(`⚠️  networkidle ${timeoutMs / 1000}s 未达成(页面或含挂起的外部请求),继续处理: ${url.split("/").pop()}`);
  }
}

module.exports = { launchPage, gotoSettled };
