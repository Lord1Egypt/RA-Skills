// kepu-quickcut 帧采集：确定性 seek(t) → Chromium 逐帧截图
// 用法: node capture.js <anim.html> <frames_dir> [fps] [duration_sec]
// 要求 HTML 暴露 window.seek(t)；可选暴露 window.FPS / window.DUR 作为默认值
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');
const os = require('os');

const HTML_FILE = process.argv[2];
const OUT = process.argv[3] || 'frames';
let FPS = parseInt(process.argv[4]) || null;
let DUR = parseFloat(process.argv[5]) || null;

if (!HTML_FILE) { console.error('usage: node capture.js <anim.html> <frames_dir> [fps] [dur]'); process.exit(1); }

// 自动发现 Playwright 缓存的 headless chromium（缺缓存时兜底用系统 Chrome）
function findHeadless() {
  const cache = path.join(os.homedir(), 'Library/Caches/ms-playwright');
  if (fs.existsSync(cache)) {
    const dirs = fs.readdirSync(cache).filter(d => d.startsWith('chromium_headless_shell-')).sort();
    for (const d of dirs.reverse()) {
      const base = path.join(cache, d);
      for (const sub of ['chrome-headless-shell-mac-arm64/chrome-headless-shell',
                         'chrome-headless-shell-mac/chrome-headless-shell']) {
        const p = path.join(base, sub);
        if (fs.existsSync(p)) return p;
      }
    }
  }
  const chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  if (fs.existsSync(chrome)) return chrome;
  throw new Error('no chrome found: run `playwright install chromium-headless-shell`, or install Google Chrome');
}

(async () => {
  const HEADLESS = findHeadless();
  const HTML = 'file://' + path.resolve(HTML_FILE);
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: HEADLESS, headless: true, args: ['--no-sandbox', '--force-device-scale-factor=1'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto(HTML);
  await page.waitForTimeout(800); // 字体加载

  // 页面可声明 FPS/DUR，命令行参数优先
  const meta = await page.evaluate(() => ({
    fps: window.FPS || 30,
    dur: window.DUR || 10,
    hasSeek: typeof window.seek === 'function'
  }));
  if (!meta.hasSeek) { console.error('ERROR: window.seek(t) not defined'); process.exit(1); }
  if (!FPS) FPS = meta.fps;
  if (!DUR) DUR = meta.dur;

  const total = Math.round(FPS * DUR);
  for (let i = 0; i < total; i++) {
    const t = i / FPS;
    await page.evaluate((t) => window.seek(t), t);
    await page.screenshot({ path: path.join(OUT, `f_${String(i).padStart(4, '0')}.png`) });
    if (i % 60 === 0) console.log(`frame ${i}/${total}`);
  }
  await browser.close();
  console.log('DONE', total, `frames @${FPS}fps x${DUR}s`);
})();
