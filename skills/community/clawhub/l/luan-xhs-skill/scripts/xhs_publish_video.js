const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const disableProxy = require('./disable_proxy');
const { normalizeTitle, normalizeBody } = require('./normalize_copy');

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

function normalizeVisibility(raw) {
  const value = String(raw || 'public').trim().toLowerCase();
  if (['public', '公开', '公开可见'].includes(value)) return '公开可见';
  if (['private', 'self', '仅自己可见', '私密', '私有'].includes(value)) return '仅自己可见';
  if (['mutual', 'friends', '互关', '仅互关好友可见'].includes(value)) return '仅互关好友可见';
  return '公开可见';
}

async function setVisibility(page, visText) {
  try {
    const row = page.locator('.permission-card-wrapper, .wrapper').filter({ hasText: '公开可见' }).first();
    if (!(await row.isVisible().catch(() => false))) return { requested: visText, applied: null, warning: 'row_not_visible' };
    const trigger = row.locator('.d-select-main').first();
    if (await trigger.isVisible().catch(() => false)) {
      await trigger.click().catch(() => {});
      await sleep(500);
      const opt = page.getByText(visText, { exact: true }).last();
      if (await opt.isVisible().catch(() => false)) {
        await opt.click().catch(() => {});
        await sleep(500);
      }
    }
    const applied = await row.innerText().then(x => x.trim()).catch(() => null);
    return { requested: visText, applied };
  } catch (e) {
    return { requested: visText, applied: null, warning: String(e) };
  }
}

(async () => {
  const args = parseArgs(process.argv);
  const video = String(args.video || '').trim();
  const title = normalizeTitle(args.title || '小视频');
  const body = normalizeBody(args.body || '');
  const visibility = normalizeVisibility(args.visibility || 'public');

  if (!video) {
    console.error('USAGE: node xhs_publish_video.js --video /path/to/video.mp4 --title "标题" --body "正文" [--visibility public|private|mutual]');
    process.exit(2);
  }

  const config = loadConfig();
  disableProxy.apply(config.useProxy !== true ? false : true);

  const workspace = path.join(process.env.HOME, '.openclaw', 'workspace');
  const sessionPath = path.join(workspace, 'xhs_user_info.json');
  const shot = path.join(workspace, 'xhs_video_publish_result.png');
  if (!fs.existsSync(sessionPath)) {
    console.error('NO_SESSION');
    process.exit(3);
  }
  if (!fs.existsSync(video)) {
    console.error('VIDEO_NOT_FOUND:' + video);
    process.exit(4);
  }

  const session = JSON.parse(fs.readFileSync(sessionPath, 'utf8'));
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const context = await browser.newContext({ viewport: { width: 1440, height: 960 } });

  try {
    if (Array.isArray(session.cookies) && session.cookies.length) {
      await context.addCookies(session.cookies).catch(() => {});
    }
    const page = await context.newPage();

    await page.goto('https://creator.xiaohongshu.com/publish/publish', { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
    await sleep(2000);

    // The working flow is: open publish page -> keep/default on 上传视频 -> set hidden input.upload-input directly.
    const uploadInput = page.locator('input.upload-input').first();
    await uploadInput.setInputFiles(video).catch(async () => {
      const fallback = page.locator('input[type=file]').first();
      await fallback.setInputFiles(video).catch(() => {});
    });

    // Wait until the page really enters the video editor, not just the upload page.
    const start = Date.now();
    const timeout = 180000;
    let editorReady = false;
    while (Date.now() - start < timeout) {
      const state = await page.evaluate(() => {
        const text = document.body?.innerText || '';
        const hasVideoEditorSignals = /视频文件|重新上传|设置封面|智能标题|暂存离开|公开可见/.test(text);
        const titleInput = !!document.querySelector('input[placeholder*="填写标题"]');
        const editor = !!document.querySelector('.tiptap.ProseMirror');
        const publishBtn = [...document.querySelectorAll('button')].find(b => (b.innerText || '').trim() === '发布');
        return {
          hasVideoEditorSignals,
          titleInput,
          editor,
          publishBtnText: publishBtn ? publishBtn.innerText : null,
        };
      }).catch(() => ({ hasVideoEditorSignals: false, titleInput: false, editor: false }));
      if (state.hasVideoEditorSignals && state.titleInput && state.editor) {
        editorReady = true;
        break;
      }
      await sleep(1000);
    }

    if (!editorReady) {
      await page.screenshot({ path: shot }).catch(() => {});
      console.error('VIDEO_UPLOAD_NOT_ENTER_EDITOR');
      process.exit(5);
    }

    const titleInput = page.locator('input[placeholder*="填写标题"]').first();
    await titleInput.fill(title).catch(() => {});
    await sleep(300);

    const editor = page.locator('.tiptap.ProseMirror').first();
    await editor.click().catch(() => {});
    await sleep(200);
    await page.keyboard.insertText(body).catch(() => {});
    await sleep(500);

    await page.mouse.click(1200, 200).catch(() => {});
    await sleep(1000);

    const visibilityResult = await setVisibility(page, visibility);

    // Publish button is present early but disabled until title/body are filled.
    let publishEnabled = false;
    for (let i = 0; i < 20; i++) {
      publishEnabled = await page.evaluate(() => {
        const btn = [...document.querySelectorAll('button')].find(b => (b.innerText || '').trim() === '发布');
        return !!btn && !btn.disabled && !/disabled/.test(btn.className);
      }).catch(() => false);
      if (publishEnabled) break;
      await sleep(1000);
    }

    if (!publishEnabled) {
      const state = await page.evaluate(() => {
        const btn = [...document.querySelectorAll('button')].find(b => (b.innerText || '').trim() === '发布');
        return {
          disabled: btn ? btn.disabled : null,
          className: btn ? btn.className : null,
          text: (document.body?.innerText || '').slice(0, 3000)
        };
      }).catch(() => ({}));
      await page.screenshot({ path: shot }).catch(() => {});
      console.error(JSON.stringify({ ok: false, error: 'PUBLISH_STILL_DISABLED', state, screenshot: shot }, null, 2));
      process.exit(6);
    }

    const publishBtn = page.getByText('发布', { exact: true }).last();
    await publishBtn.click().catch(() => {});
    await sleep(8000);

    await page.goto('https://creator.xiaohongshu.com/new/note-manager', { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
    await sleep(3000);
    const found = await page.evaluate((t) => [...document.querySelectorAll('*')].some(el => (el.innerText || '').includes(t)), title);
    await page.screenshot({ path: shot }).catch(() => {});

    if (found) {
      console.log(JSON.stringify({ ok: true, title, visibility: visibilityResult, screenshot: shot }, null, 2));
      process.exit(0);
    }

    console.error(JSON.stringify({ ok: false, error: 'PUBLISH_VERIFY_FAILED', screenshot: shot }, null, 2));
    process.exit(7);
  } catch (error) {
    console.error('SCRIPT_EXCEPTION', String(error));
    process.exit(99);
  } finally {
    await browser.close().catch(() => {});
  }
})();
