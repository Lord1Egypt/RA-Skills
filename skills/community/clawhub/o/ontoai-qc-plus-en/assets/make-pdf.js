#!/usr/bin/env node
/* ============================================================
   ontoAI 质检官 · HTML → PDF 生成脚本
   用法：node assets/make-pdf.js <输入.html> [输出.pdf]
   示例：node assets/make-pdf.js evals/selftest-report.html
         node assets/make-pdf.js evals/selftest-report.html 报告.pdf

   原理：调用本机已安装的 Microsoft Edge / Google Chrome 的无头打印能力，
   使用 HTML 内已内置的 @page A4 与 print-color-adjust 规则，
   不引入任何第三方依赖（无 puppeteer、无 wkhtmltopdf），离线可用。
   ============================================================ */
"use strict";
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const CANDIDATES = [
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/microsoft-edge",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium"
];

function findBrowser() {
  for (const p of CANDIDATES) if (fs.existsSync(p)) return p;
  return null;
}

const [, , inArg, outArg] = process.argv;
if (!inArg) {
  console.error("用法：node assets/make-pdf.js <输入.html> [输出.pdf]");
  process.exit(1);
}
const inPath = path.resolve(inArg);
if (!fs.existsSync(inPath)) {
  console.error("找不到输入文件：" + inPath);
  process.exit(1);
}
const outPath = path.resolve(outArg || inPath.replace(/\.html?$/i, ".pdf"));

const browser = findBrowser();
if (!browser) {
  console.error("未找到 Edge / Chrome。请安装其一，或直接用浏览器打开 HTML 后按 Ctrl+P 另存为 PDF。");
  process.exit(2);
}

// file:// URL 按 RFC 3986 逐段编码：encodeURIComponent 会转义 # ? % 等危险字符
// （encodeURI 不转义 #/?，路径含这些字符时 file URL 被截断、打印失败）
// Windows 盘符（如 C:）保留冒号不编码
const fileUrl = "file:///" + inPath.replace(/\\/g, "/").split("/")
  .map((seg, i) => (i === 1 && /^[A-Za-z]:$/.test(seg)) ? seg : encodeURIComponent(seg))
  .join("/");

// Edge/Chrome 无头打印为异步落盘，轮询等待最长 20 秒。
// 关键：必须等「本次新写入」的文件（mtime >= 启动时刻），否则会误判到上一次的旧 PDF。
const wait = ms => { const t = Date.now(); while (Date.now() - t < ms); };

function attempt(flag) {
  const tmpProfile = fs.mkdtempSync(path.join(os.tmpdir(), "ontoai-pdf-"));
  const args = [
    flag,
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--disable-extensions",
    "--user-data-dir=" + tmpProfile,
    "--print-to-pdf=" + outPath,
    fileUrl
  ];
  const t0 = Date.now();
  const r = spawnSync(browser, args, { windowsHide: true, timeout: 120000 });
  const deadline = Date.now() + 20000;
  let ok = false;
  while (Date.now() < deadline) {
    if (fs.existsSync(outPath)) {
      const st = fs.statSync(outPath);
      if (st.size > 1024 && st.mtimeMs >= t0 - 1500) { ok = true; break; }
    }
    wait(300);
  }
  return { ok, r };
}

console.log("浏览器：" + browser);
console.log("输入　：" + inPath);
// 新无头模式优先（Chromium 109+ 标准路径，旧模式已在新版被移除）；失败回退旧模式（兼容老浏览器）
let res = attempt("--headless=new");
if (!res.ok) {
  console.log("模式　：--headless=new 未产出，回退 --headless=old");
  res = attempt("--headless=old");
} else {
  console.log("模式　：--headless=new");
}

if (res.ok) {
  console.log("输出　：" + outPath);
  console.log("大小　：" + Math.round(fs.statSync(outPath).size / 1024) + " KB");
  console.log("完成。");
} else {
  console.error("生成失败（exit=" + (res.r.status == null ? "null" : res.r.status) + "）。");
  if (res.r.stderr) console.error(String(res.r.stderr).slice(0, 800));
  console.error("备用方案：用浏览器打开该 HTML，按 Ctrl+P → 目标选「另存为 PDF」→ 勾选「背景图形」。");
  process.exit(3);
}
