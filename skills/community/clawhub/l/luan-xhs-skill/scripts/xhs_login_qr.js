const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const disableProxy = require('./disable_proxy');

function loadConfig() {
  try {
    return JSON.parse(fs.readFileSync(path.join(__dirname, '..', '_meta.json'), 'utf8')).config || {};
  } catch {
    return { useProxy: false };
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function ensureQrMode(page) {
  const text = await page.evaluate(() => document.body?.innerText || '').catch(() => '');
  if (/APP扫一扫登录|扫码登录|请使用已登录该账号的小红书APP扫码登录身份|为保护账号安全/.test(text)) return true;

  const attempts = [];

  // Preferred: click near the top-right corner of the login card.
  attempts.push(async () => {
    const box = await page.locator('.login-box-container').boundingBox().catch(() => null);
    if (!box) return false;
    const points = [
      { x: box.x + box.width - 36, y: box.y + 26 },
      { x: box.x + box.width - 22, y: box.y + 18 },
      { x: box.x + box.width - 48, y: box.y + 34 },
    ];
    for (const p of points) {
      await page.mouse.click(Math.round(p.x), Math.round(p.y)).catch(() => {});
      await sleep(1200);
      const t = await page.evaluate(() => document.body?.innerText || '').catch(() => '');
      if (/APP扫一扫登录|扫码登录|请使用已登录该账号的小红书APP扫码登录身份|为保护账号安全/.test(t)) return true;
    }
    return false;
  });

  // Fallback: click likely SVG/icon area inside the login card.
  attempts.push(async () => {
    const ok = await page.evaluate(() => {
      const box = document.querySelector('.login-box-container');
      if (!box) return false;
      const rect = box.getBoundingClientRect();
      const candidates = [...document.querySelectorAll('svg, div, span')].filter(el => {
        const r = el.getBoundingClientRect();
        return r.width > 0 && r.height > 0 && r.x > rect.right - 90 && r.x < rect.right + 10 && r.y > rect.y - 10 && r.y < rect.y + 90;
      });
      const el = candidates[0];
      if (!el) return false;
      el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
      return true;
    }).catch(() => false);
    if (!ok) return false;
    await sleep(1500);
    const t = await page.evaluate(() => document.body?.innerText || '').catch(() => '');
    return /APP扫一扫登录|扫码登录|请使用已登录该账号的小红书APP扫码登录身份|为保护账号安全/.test(t);
  });

  for (const fn of attempts) {
    try {
      if (await fn()) return true;
    } catch {}
  }
  return false;
}

async function saveQr(page, qrPath, qrFullPath) {
  let saved = false;
  const selectors = [
    'img[src*="qr"]',
    'img[class*="qr"]',
    '[class*="qrcode"] img',
    '[class*="qrcode"]',
    'canvas'
  ];
  for (const sel of selectors) {
    try {
      const loc = page.locator(sel).first();
      if (await loc.isVisible({ timeout: 1500 }).catch(() => false)) {
        await loc.screenshot({ path: qrPath });
        saved = true;
        break;
      }
    } catch {}
  }
  await page.screenshot({ path: qrFullPath, fullPage: false }).catch(() => {});
  if (!saved) {
    try { fs.copyFileSync(qrFullPath, qrPath); } catch {}
  }
  return saved;
}

(async () => {
  const config = loadConfig();
  disableProxy.apply(config.useProxy !== true ? false : true);

  const workspace = path.join(process.env.HOME, '.openclaw', 'workspace');
  const qrPath = path.join(workspace, 'xhs_qr.png');
  const qrFullPath = path.join(workspace, 'xhs_qr_full.png');
  const sessionPath = path.join(workspace, 'xhs_user_info.json');

  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    viewport: { width: 1400, height: 900 }
  });
  const page = await context.newPage();

  try {
    await page.goto('https://creator.xiaohongshu.com/login', { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
    await sleep(2500);

    const qrReady = await ensureQrMode(page);
    if (!qrReady) {
      await page.screenshot({ path: qrFullPath, fullPage: false }).catch(() => {});
      console.error('XHS_QR_LOGIN_FAILED');
      console.error('QR_TOGGLE_NOT_FOUND');
      console.error('DEBUG_SCREENSHOT:' + qrFullPath);
      process.exit(1);
    }

    await saveQr(page, qrPath, qrFullPath);
    console.log('QR_READY:' + qrPath);

    const start = Date.now();
    const timeoutMs = 10 * 60 * 1000;
    let loggedIn = false;
    while (Date.now() - start < timeoutMs) {
      try {
        const state = await page.evaluate(() => {
          const text = document.body ? document.body.innerText : '';
          const needsLogin = /APP扫一扫登录|扫码登录|短信登录|发送验证码|收不到验证码|请使用已登录该账号的小红书APP扫码登录身份|为保护账号安全/.test(text) || /\/login/.test(location.href);
          const creatorReady = /发布笔记|笔记管理|数据看板|创作服务平台/.test(text) && !/APP扫一扫登录|扫码登录|短信登录|发送验证码/.test(text);
          return { needsLogin, creatorReady, url: location.href, title: document.title };
        });
        if (!state.needsLogin && state.creatorReady) {
          loggedIn = true;
          break;
        }
      } catch {}
      await sleep(2000);
    }

    if (!loggedIn) {
      console.log('LOGIN_TIMEOUT');
      process.exit(0);
    }

    await page.goto('https://creator.xiaohongshu.com/new/home', { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
    await sleep(2500);

    const cookies = await context.cookies().catch(() => []);
    const storage = await page.evaluate(() => {
      const localStorageObj = {};
      const sessionStorageObj = {};
      try {
        for (let i = 0; i < localStorage.length; i++) {
          const k = localStorage.key(i);
          localStorageObj[k] = localStorage.getItem(k);
        }
      } catch {}
      try {
        for (let i = 0; i < sessionStorage.length; i++) {
          const k = sessionStorage.key(i);
          sessionStorageObj[k] = sessionStorage.getItem(k);
        }
      } catch {}
      return { localStorage: localStorageObj, sessionStorage: sessionStorageObj, url: location.href, title: document.title };
    }).catch(() => ({ localStorage: {}, sessionStorage: {}, url: '', title: '' }));

    fs.writeFileSync(sessionPath, JSON.stringify({
      localStorage: storage.localStorage,
      sessionStorage: storage.sessionStorage,
      cookies,
      capturedAt: new Date().toISOString(),
      url: storage.url,
      title: storage.title,
      via: 'creator_qr_login'
    }, null, 2));

    console.log('XHS_QR_LOGIN_OK');
    console.log(JSON.stringify({ ok: true, sessionPath, qrPath, title: storage.title, url: storage.url, cookieCount: cookies.length }, null, 2));
  } catch (error) {
    await page.screenshot({ path: qrFullPath, fullPage: false }).catch(() => {});
    console.error('XHS_QR_LOGIN_FAILED');
    console.error(String(error && error.stack || error));
    console.error('DEBUG_SCREENSHOT:' + qrFullPath);
    process.exit(1);
  } finally {
    await browser.close().catch(() => {});
  }
})();
