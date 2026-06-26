const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { chromium } = require('playwright');
const disableProxy = require('./disable_proxy');
const { normalizeTitle, normalizeBody } = require('./normalize_copy');

function parseArgs(argv) {
  const args = { image: [] };
  for (let i = 2; i < argv.length; i++) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args[key] = true;
    else {
      if (key === 'image') args.image.push(next);
      else args[key] = next;
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

function ensureImages(args, workspace) {
  if (args.image.length > 0) return args.image;
  const out = path.join(workspace, 'xhs_auto_cover.png');
  const subtitle = normalizeBody(args.body).split('\n').map(s => s.trim()).find(Boolean) || '先发一条，看看今天运气站不站我这边。';
  const footer = '#测试笔记';
  const res = spawnSync('python3', [
    path.join(__dirname, 'xhs_make_text_cover.py'),
    '--title', args.title,
    '--subtitle', subtitle.slice(0, 26),
    '--tag', '随手发发',
    '--footer', footer,
    '--output', out,
  ], { encoding: 'utf8' });
  if (res.status !== 0) {
    throw new Error(`AUTO_COVER_FAILED: ${res.stderr || res.stdout}`);
  }
  return [out];
}

function normalizeVisibility(raw) {
  const value = String(raw || 'public').trim().toLowerCase();
  if (['public', '公开', '公开可见'].includes(value)) return { key: 'public', text: '公开可见' };
  if (['private', 'self', '仅自己可见', '私密', '私有'].includes(value)) return { key: 'private', text: '仅自己可见' };
  if (['mutual', 'friends', '互关', '仅互关好友可见'].includes(value)) return { key: 'mutual', text: '仅互关好友可见' };
  throw new Error(`UNSUPPORTED_VISIBILITY: ${raw}`);
}

function parseScheduleAt(input) {
  const value = String(input || '').trim();
  if (!value) return null;
  const m = value.match(/^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})$/);
  if (!m) throw new Error(`INVALID_SCHEDULE_AT_FORMAT: ${input}. Expected YYYY-MM-DD HH:mm`);
  const dt = new Date(`${m[1]}-${m[2]}-${m[3]}T${m[4]}:${m[5]}:00+08:00`);
  if (Number.isNaN(dt.getTime())) throw new Error(`INVALID_SCHEDULE_AT_VALUE: ${input}`);
  const now = Date.now();
  const delta = dt.getTime() - now;
  if (delta < 60 * 60 * 1000) throw new Error('SCHEDULE_TOO_SOON: Xiaohongshu requires at least 1 hour later');
  if (delta > 14 * 24 * 60 * 60 * 1000) throw new Error('SCHEDULE_TOO_LATE: Xiaohongshu allows at most 14 days later');
  return value;
}

async function ensureCreatorSession(page, shotPath) {
  const home = await page.evaluate(() => ({
    url: location.href,
    title: document.title,
    text: (document.body?.innerText || '').slice(0, 4000)
  }));
  const loginInvalid = /短信登录|发送验证码|收不到验证码|解锁创作者专属功能/.test(home.text) || /\/login/.test(home.url);
  const creatorReady = /发布笔记|笔记管理|数据看板|创作服务平台/.test(home.text);
  if (loginInvalid || !creatorReady) {
    await page.screenshot({ path: shotPath, fullPage: false }).catch(() => {});
    throw new Error(`SESSION_INVALID:${JSON.stringify(home)}`);
  }
}

async function openImagePublish(page) {
  await page.goto('https://creator.xiaohongshu.com/publish/publish', { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
  await sleep(2500);
  const imageTab = page.getByText('上传图文', { exact: true }).last();
  if (await imageTab.isVisible().catch(() => false)) {
    await imageTab.click().catch(() => {});
    await sleep(1500);
  }
}

async function configureVisibility(page, visibility) {
  try {
    let row = page.locator('.post-time-wrapper').locator('xpath=preceding-sibling::*[1]');
    if (!(await row.isVisible().catch(() => false))) {
      row = page.locator('.wrapper').last();
    }
    if (!(await row.isVisible().catch(() => false))) return { requested: visibility.text, applied: null, warning: 'row_not_visible' };
    await row.scrollIntoViewIfNeeded().catch(() => {});
    await sleep(200);
    const trigger = row.locator('.d-select-main').first();
    if (await trigger.isVisible().catch(() => false)) await trigger.click().catch(() => {});
    else await row.click().catch(() => {});
    await sleep(600);
    // Try to click the option; be tolerant if not visible
    let option = page.getByText(visibility.text, { exact: true }).last();
    if (!(await option.isVisible().catch(() => false))) {
      // try alternative dropdown content
      try {
        const alt = page.locator('.d-dropdown-content').getByText(visibility.text).first();
        if (await alt.isVisible().catch(() => false)) {
          await alt.click().catch(() => {});
          option = alt;
        }
      } catch (e) {}
    }
    if (option && (await option.isVisible().catch(() => false))) {
      await option.click().catch(() => {});
    } else {
      const applied = await row.innerText().then(x => x.trim()).catch(() => null);
      return { requested: visibility.text, applied, warning: 'option_not_found' };
    }
    await sleep(700);
    const applied = await row.innerText().then(x => x.trim()).catch(() => null);
    return { requested: visibility.text, applied };
  } catch (e) {
    return { requested: visibility.text, applied: null, warning: 'exception', error: String(e) };
  }
}

async function configureSchedule(page, scheduleAt) {
  const row = page.locator('.post-time-wrapper').first();
  if (!(await row.isVisible().catch(() => false))) return { enabled: false, applied: null };
  await row.scrollIntoViewIfNeeded().catch(() => {});
  await sleep(200);
  const checkbox = row.locator('input[type="checkbox"]').first();
  const checked = async () => await checkbox.isChecked().catch(() => false);
  if (!(await checked())) {
    await row.locator('.d-switch').click().catch(() => {});
    await sleep(800);
  }
  if (!(await checked())) {
    throw new Error('SCHEDULE_TOGGLE_FAILED');
  }
  const input = row.locator('input.d-text').first();
  if (!(await input.isVisible().catch(() => false))) {
    return { enabled: true, applied: null };
  }
  const defaultValue = await input.inputValue().catch(() => null);
  if (!scheduleAt) {
    return { enabled: true, applied: defaultValue, defaulted: true };
  }

  await input.click().catch(() => {});
  await sleep(300);
  await page.evaluate((value) => {
    const inputEl = document.querySelector('.post-time-wrapper input.d-text');
    if (!inputEl) return;
    inputEl.focus();
    inputEl.value = value;
    inputEl.dispatchEvent(new Event('input', { bubbles: true }));
    inputEl.dispatchEvent(new Event('change', { bubbles: true }));
    inputEl.blur();
  }, scheduleAt).catch(() => {});
  await sleep(800);
  await page.mouse.click(50, 50).catch(() => {});
  await sleep(1200);

  const applied = await input.inputValue().catch(() => null);
  if (applied !== scheduleAt) {
    throw new Error(`SCHEDULE_NOT_APPLIED:${scheduleAt}:${applied}`);
  }
  return { enabled: true, applied, defaulted: false };
}

(async () => {
  const args = parseArgs(process.argv);
  if (!args.title || !args.body) {
    console.error('Usage: node xhs_publish_with_saved_session.js --title "标题" --body "正文" [--image /path/a.png] [--visibility public|private|mutual] [--schedule] [--schedule-at "YYYY-MM-DD HH:mm"] [--dry-run]');
    process.exit(2);
  }

  args.title = normalizeTitle(args.title);
  args.body = normalizeBody(args.body);

  const visibility = normalizeVisibility(args.visibility || 'public');
  const scheduleAt = parseScheduleAt(args['schedule-at']);
  const scheduleEnabled = !!args.schedule || !!scheduleAt;

  const config = loadConfig();
  disableProxy.apply(config.useProxy !== true ? false : true);

  const workspace = path.join(process.env.HOME, '.openclaw', 'workspace');
  const sessionPath = path.join(workspace, 'xhs_user_info.json');
  const shotPath = path.join(workspace, 'xhs_publish_result.png');
  if (!fs.existsSync(sessionPath)) {
    console.error('SESSION_FILE_MISSING:' + sessionPath);
    process.exit(2);
  }

  const session = JSON.parse(fs.readFileSync(sessionPath, 'utf8'));
  const images = ensureImages(args, workspace);
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    viewport: { width: 1440, height: 960 }
  });
  await context.addInitScript(() => {
    try { Object.defineProperty(navigator, 'webdriver', { get: () => false }); } catch {}
  });
  const page = await context.newPage();

  try {
    if (Array.isArray(session.cookies) && session.cookies.length) {
      await context.addCookies(session.cookies).catch(() => {});
    }

    await page.goto('https://creator.xiaohongshu.com/new/home', { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
    await sleep(2500);

    if (session.localStorage && Object.keys(session.localStorage).length) {
      await page.evaluate(storage => {
        try {
          Object.entries(storage).forEach(([k, v]) => localStorage.setItem(k, v));
        } catch {}
      }, session.localStorage).catch(() => {});
      await page.reload({ waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
      await sleep(2000);
    }

    await ensureCreatorSession(page, shotPath);
    await openImagePublish(page);

    const fileInputs = page.locator('input[type=file]');
    const count = await fileInputs.count().catch(() => 0);
    let uploaded = false;
    for (let i = 0; i < count; i++) {
      try {
        await fileInputs.nth(i).setInputFiles(images);
        uploaded = true;
        break;
      } catch {}
    }
    if (!uploaded) throw new Error('IMAGE_UPLOAD_INPUT_NOT_FOUND');

    await page.waitForSelector('input[placeholder*="填写标题"]', { timeout: 30000 });
    await sleep(3500);

    const titleInput = page.locator('input[placeholder*="填写标题"]').first();
    await titleInput.fill(args.title.slice(0, 20)).catch(() => {});
    await sleep(300);

    const editor = page.locator('.tiptap.ProseMirror').first();
    await editor.click({ timeout: 5000 }).catch(() => {});
    await sleep(200);
    await page.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A').catch(() => {});
    await page.keyboard.press('Backspace').catch(() => {});
    await page.keyboard.insertText(args.body).catch(() => {});
    await sleep(800);
    await page.mouse.click(1200, 200).catch(() => {});
    await sleep(1000);

    const visibilityResult = await configureVisibility(page, visibility);
    const scheduleResult = scheduleEnabled ? await configureSchedule(page, scheduleAt) : { enabled: false, applied: null };

    const before = await page.evaluate(() => ({
      url: location.href,
      title: document.title,
      text: (document.body?.innerText || '').slice(0, 5000)
    }));

    if (!args['dry-run']) {
      const publishButtons = [
        page.getByText(scheduleEnabled ? '定时发布' : '发布', { exact: true }).last(),
        page.locator(`button:has-text("${scheduleEnabled ? '定时发布' : '发布'}")`).last(),
        page.locator(`[role="button"]:has-text("${scheduleEnabled ? '定时发布' : '发布'}")`).last(),
      ];
      let clicked = false;
      for (const loc of publishButtons) {
        if (await loc.isVisible().catch(() => false)) {
          try {
            await loc.click({ timeout: 5000 });
            clicked = true;
            break;
          } catch {}
        }
      }
      if (!clicked) throw new Error('PUBLISH_BUTTON_NOT_FOUND');
      await sleep(7000);
    }

    await page.goto('https://creator.xiaohongshu.com/new/home', { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
    await sleep(2500);
    const noteManager = page.getByText('笔记管理', { exact: true }).first();
    if (await noteManager.isVisible().catch(() => false)) {
      await noteManager.click().catch(() => {});
      await sleep(4000);
    }

    const after = await page.evaluate(() => ({
      url: location.href,
      title: document.title,
      text: (document.body?.innerText || '').slice(0, 5000)
    }));
    await page.screenshot({ path: shotPath, fullPage: false }).catch(() => {});

    const foundTitle = after.text.includes(args.title.slice(0, 20));
    const success = args['dry-run'] ? /图片编辑|笔记预览|内容设置|更多设置/.test(before.text) : foundTitle;
    console.log(JSON.stringify({
      ok: success,
      dryRun: !!args['dry-run'],
      title: args.title.slice(0, 20),
      visibility: visibilityResult,
      schedule: scheduleResult,
      images,
      before,
      after,
      screenshot: shotPath
    }, null, 2));
    process.exit(success ? 0 : 1);
  } catch (error) {
    await page.screenshot({ path: shotPath, fullPage: false }).catch(() => {});
    console.error('XHS_PUBLISH_FAILED');
    console.error(String(error && error.stack || error));
    console.error('DEBUG_SCREENSHOT:' + shotPath);
    process.exit(1);
  } finally {
    await browser.close().catch(() => {});
  }
})();
