/**
 * 雅思复盘笔记 PDF 生成脚本
 * 用法：node generate-pdf.js <HTML文件路径>
 * 示例：node generate-pdf.js 剑5-Test1-Passage1-XXX复盘.html
 * 
 * 匿名统计：生成 PDF 成功后会上报一次匿名事件（仅版本号+时间戳，不含任何个人信息）
 * 关闭统计：设置环境变量 SKILL_NO_TELEMETRY=1
 */
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const SKILL_VERSION = '1.3.0';
const STATS_ENDPOINT = 'https://ielts-skill-stats.dengjiawei.workers.dev/ping';

const htmlFile = process.argv[2];
if (!htmlFile) {
  console.error('❌ 请提供 HTML 文件路径，例如：node generate-pdf.js 复盘笔记.html');
  process.exit(1);
}

const absPath = path.resolve(htmlFile);
if (!fs.existsSync(absPath)) {
  console.error(`❌ 文件不存在：${absPath}`);
  process.exit(1);
}

const pdfPath = absPath.replace(/\.html$/, '.pdf');

/**
 * 匿名统计上报 — 非阻塞，失败静默，不影响主流程
 * 仅发送：事件类型 + Skill 版本号 + 时间戳
 * 不发送：IP、用户名、文件名、文件内容等任何个人信息
 */
function reportAnonymousUsage(event) {
  if (process.env.SKILL_NO_TELEMETRY === '1') return;

  const https = require('https');
  const url = new URL(STATS_ENDPOINT);
  const payload = JSON.stringify({
    event,
    version: SKILL_VERSION,
    ts: Date.now(),
  });

  const req = https.request({
    hostname: url.hostname,
    path: url.pathname,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload),
    },
    timeout: 3000,
  });

  req.on('error', () => {}); // 静默失败
  req.on('timeout', () => req.destroy());
  req.write(payload);
  req.end();
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true
  });
  const page = await browser.newPage();
  await page.goto('file://' + absPath, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    margin: { top: '2cm', right: '2cm', bottom: '2cm', left: '2cm' },
    printBackground: true,
    displayHeaderFooter: false
  });
  await browser.close();
  console.log(`✅ PDF 已生成：${pdfPath}`);

  // 匿名上报 PDF 生成事件
  reportAnonymousUsage('pdf_generated');
})();
