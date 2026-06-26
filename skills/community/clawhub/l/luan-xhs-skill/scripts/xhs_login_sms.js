const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { chromium } = require('playwright');
const disableProxy = require('./disable_proxy');

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args[key] = true;
    else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

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

async function promptCode() {
  if (!process.stdin.isTTY) {
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    const merged = Buffer.concat(chunks.map(x => Buffer.isBuffer(x) ? x : Buffer.from(String(x)))).toString('utf8');
    const match = merged.match(/(\d{4,8})/);
    return match ? match[1] : null;
  }
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const answer = await new Promise(resolve => rl.question('请输入短信验证码: ', resolve));
  rl.close();
  const match = String(answer).match(/(\d{4,8})/);
  return match ? match[1] : null;
}

(async () => {
  const args = parseArgs(process.argv);
  const phone = String(args.phone || '').trim();
  if (!/^1\d{10}$/.test(phone)) {
    console.error('Usage: node xhs_login_sms.js --phone 13xxxxxxxxx [--code 123456]');
    process.exit(2);
  }

  const config = loadConfig();
  disableProxy.apply(config.useProxy !== true ? false : true);

  const workspace = path.join(process.env.HOME, '.openclaw', 'workspace');
  const sessionPath = path.join(workspace, 'xhs_user_info.json');
  const shotPath = path.join(workspace, 'xhs_sms_login_result.png');

  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    viewport: { width: 1400, height: 900 }
  });
  await context.addInitScript(() => {
    try { Object.defineProperty(navigator, 'webdriver', { get: () => false }); } catch {}
  });
  const page = await context.newPage();

  const visibleText = async () => page.evaluate(() => (document.body?.innerText || '').slice(0, 3000)).catch(() => '');
  const takeShot = async () => page.screenshot({ path: shotPath, fullPage: false }).catch(() => {});

  try {
    await page.goto('https://creator.xiaohongshu.com/login', { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
    await sleep(2500);

    const initialText = await visibleText();
    if (/APP扫一扫登录|扫码登录|请使用已登录该账号的小红书APP扫码登录身份|为保护账号安全/.test(initialText)) {
      throw new Error('QR_REQUIRED: creator platform switched to QR verification; use xhs_login_qr.js');
    }

    const phoneCandidates = [
      page.locator('input[placeholder*="手机号"]').first(),
      page.locator('input[placeholder*="手机号码"]').first(),
      page.locator('input[type="tel"]').first(),
      page.locator('input').first(),
    ];
    let phoneFilled = false;
    for (const loc of phoneCandidates) {
      if (await loc.isVisible().catch(() => false)) {
        try {
          await loc.fill('');
          await loc.type(phone, { delay: 40 });
          phoneFilled = true;
          break;
        } catch {}
      }
    }
    if (!phoneFilled) throw new Error('PHONE_INPUT_NOT_FOUND');

    const sendButtons = [
      page.getByText('发送验证码', { exact: true }).first(),
      page.getByText('获取验证码', { exact: true }).first(),
      page.locator('button:has-text("发送验证码")').first(),
      page.locator('button:has-text("获取验证码")').first(),
    ];
    let requested = false;
    for (const loc of sendButtons) {
      if (await loc.isVisible().catch(() => false)) {
        try {
          await loc.click({ timeout: 3000 });
          requested = true;
          break;
        } catch {}
      }
    }
    if (!requested) throw new Error('SEND_CODE_BUTTON_NOT_FOUND');

    await sleep(2000);
    console.log('XHS_SMS_CODE_REQUESTED');

    const afterRequestText = await visibleText();
    if (/APP扫一扫登录|扫码登录|请使用已登录该账号的小红书APP扫码登录身份|为保护账号安全/.test(afterRequestText)) {
      throw new Error('QR_REQUIRED: SMS request path switched to QR verification; use xhs_login_qr.js');
    }

    let code = String(args.code || '').trim();
    if (!/^[0-9]{4,8}$/.test(code)) {
      console.log('WAITING_FOR_CODE');
      code = await promptCode();
    }
    if (!/^[0-9]{4,8}$/.test(code || '')) throw new Error('INVALID_CODE');

    const codeCandidates = [
      page.locator('input[placeholder*="验证码"]').first(),
      page.locator('input[maxlength="6"]').first(),
      page.locator('input[inputmode="numeric"]').nth(1),
      page.locator('input').nth(1),
    ];
    let codeFilled = false;
    for (const loc of codeCandidates) {
      if (await loc.isVisible().catch(() => false)) {
        try {
          const current = await loc.inputValue().catch(() => '');
          if (current && current.replace(/\D/g, '') === phone) continue;
          await loc.fill('');
          await loc.type(code, { delay: 40 });
          codeFilled = true;
          break;
        } catch {}
      }
    }
    if (!codeFilled) throw new Error('CODE_INPUT_NOT_FOUND');

    const loginButtons = [
      page.getByText('登 录', { exact: true }).first(),
      page.getByText('登录', { exact: true }).first(),
      page.locator('button:has-text("登录")').first(),
      page.locator('[role="button"]:has-text("登录")').first(),
    ];
    let clicked = false;
    for (const loc of loginButtons) {
      if (await loc.isVisible().catch(() => false)) {
        try {
          await loc.click({ timeout: 3000 });
          clicked = true;
          break;
        } catch {}
      }
    }
    if (!clicked) throw new Error('LOGIN_BUTTON_NOT_FOUND');

    await sleep(6000);
    await takeShot();

    const result = {
      url: page.url(),
      title: await page.title().catch(() => ''),
      text: await visibleText(),
    };
    const ok = (/creator/.test(result.url) && !/login/.test(result.url)) ||
      (/发布笔记|笔记管理|数据看板|内容管理/.test(result.text) && !/发送验证码|短信登录|收不到验证码/.test(result.text));

    if (!ok) {
      console.error(JSON.stringify({ ok: false, result, screenshot: shotPath }, null, 2));
      process.exit(1);
    }

    const cookies = await context.cookies().catch(() => []);
    const localStorageObj = await page.evaluate(() => {
      const out = {};
      try {
        for (let i = 0; i < localStorage.length; i++) {
          const k = localStorage.key(i);
          out[k] = localStorage.getItem(k);
        }
      } catch {}
      return out;
    }).catch(() => ({}));
    const sessionStorageObj = await page.evaluate(() => {
      const out = {};
      try {
        for (let i = 0; i < sessionStorage.length; i++) {
          const k = sessionStorage.key(i);
          out[k] = sessionStorage.getItem(k);
        }
      } catch {}
      return out;
    }).catch(() => ({}));

    fs.writeFileSync(sessionPath, JSON.stringify({
      localStorage: localStorageObj,
      sessionStorage: sessionStorageObj,
      cookies,
      capturedAt: new Date().toISOString(),
      url: result.url,
      title: result.title,
      via: 'sms_login'
    }, null, 2));

    console.log('XHS_SMS_LOGIN_OK');
    console.log(JSON.stringify({ ok: true, url: result.url, title: result.title, cookieCount: cookies.length, sessionPath, screenshot: shotPath }, null, 2));
  } catch (error) {
    await takeShot();
    console.error('XHS_SMS_LOGIN_FAILED');
    console.error(String(error && error.stack || error));
    console.error('DEBUG_SCREENSHOT:' + shotPath);
    process.exit(1);
  } finally {
    await browser.close().catch(() => {});
  }
})();
