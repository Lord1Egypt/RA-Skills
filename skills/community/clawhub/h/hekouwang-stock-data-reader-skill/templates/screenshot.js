// 贴图截图器 1080×1350 @2x —— 扫描目标目录 NN-*.html，截到 output/。
// 用法：node screenshot.js [贴图目录] [--clean]
//   默认保留 HTML；加 --clean 才在截图成功后删除对应 HTML。
//   Chrome 路径可用环境变量 CHROME_PATH 覆盖。
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const CHROME_DEFAULTS = {
  darwin: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  linux: 'google-chrome',
  win32: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
};
const chrome = process.env.CHROME_PATH || CHROME_DEFAULTS[process.platform] || 'google-chrome';
const W = 1080, H = 1350;

const args = process.argv.slice(2);
const clean = args.includes('--clean');
const dir = path.resolve(args.find(a => !a.startsWith('--')) || '.');
if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) {
  console.error('✗ 不是目录:', dir);
  process.exit(1);
}
const outDir = path.join(dir, 'output');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const files = fs.readdirSync(dir).filter(f => /^\d{2}-[a-z0-9-]+\.html$/.test(f)).sort();
for (const file of files) {
  const htmlPath = path.join(dir, file);
  const outPath = path.join(outDir, file.replace(/\.html$/, '.png'));
  const chromeArgs = [
    '--headless=new',
    '--disable-gpu',
    `--window-size=${W},${H}`,
    '--hide-scrollbars',
    '--force-device-scale-factor=2',
    `--screenshot=${outPath}`,
    '--virtual-time-budget=6000',
    'file://' + htmlPath,
  ];
  try {
    execFileSync(chrome, chromeArgs, { stdio: 'pipe', timeout: 45000 });
    if (clean) fs.unlinkSync(htmlPath);
    console.log('✓', file);
  } catch (e) {
    console.error('✗', file, '(截图失败，保留 HTML 供排查)');
  }
}
console.log('done:', files.length, 'shots →', outDir, clean ? '（已删除源 HTML）' : '（源 HTML 已保留）');
