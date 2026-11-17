#!/usr/bin/env node
/**
 * Resume PDF Generator (generic)
 *
 * Uses Chrome CDP Page.printToPDF with displayHeaderFooter: false.
 * This is the only reliable way to produce a clean resume PDF.
 *
 * Usage:
 *   node scripts/generate-pdf.js <html-path> [output-path]
 *
 * Examples:
 *   node scripts/generate-pdf.js ./resume.html ./resume.pdf
 *   node scripts/generate-pdf.js /path/to/resume.html
 *   node scripts/generate-pdf.js ./resume.html  (output defaults to ./resume.pdf)
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const CDP_PORT = 9225;
const HTTP_PORT = 18772;

// Parse args
const htmlPath = process.argv[2];
if (!htmlPath) {
  console.error('Usage: node generate-pdf.js <html-path> [output-path]');
  process.exit(1);
}

const absHtmlPath = path.resolve(htmlPath);
if (!fs.existsSync(absHtmlPath)) {
  console.error(`File not found: ${absHtmlPath}`);
  process.exit(1);
}

const pdfPath = process.argv[3]
  ? path.resolve(process.argv[3])
  : path.join(path.dirname(absHtmlPath), path.basename(absHtmlPath, '.html') + '.pdf');

// Resolve chrome binary
function findChrome() {
  const candidates = [
    '/usr/bin/google-chrome-stable',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium-browser',
    '/usr/bin/chromium'
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return 'google-chrome-stable'; // fallback, let OS resolve
}

console.log(`📄 HTML: ${absHtmlPath}`);
console.log(`📄 PDF:  ${pdfPath}`);

const chrome = spawn(findChrome(), [
  '--headless', '--disable-gpu', '--no-sandbox',
  `--remote-debugging-port=${CDP_PORT}`,
  '--disable-extensions', '--disable-background-networking',
  '--disable-sync', '--no-first-run'
], { detached: true, stdio: 'ignore' });

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)); } catch (e) { reject(e); } });
    }).on('error', reject);
  });
}

async function waitForChrome(maxTry) {
  for (let i = 0; i < maxTry; i++) {
    try {
      const v = await fetchJson(`http://127.0.0.1:${CDP_PORT}/json/version`);
      return v.webSocketDebuggerUrl;
    } catch (e) {
      await new Promise(r => setTimeout(r, 1000));
    }
  }
  throw new Error('Chrome failed to start');
}

(async () => {
  const html = fs.readFileSync(absHtmlPath, 'utf-8');

  const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(html);
  });
  server.listen(HTTP_PORT);

  try {
    const browserWsUrl = await waitForChrome(10);
    const WebSocket = require('ws');

    // Connect to browser WS, create blank tab
    const bws = new WebSocket(browserWsUrl);
    await new Promise((resolve, reject) => {
      bws.on('open', resolve);
      bws.on('error', reject);
    });

    let msgId = 1;
    function bsend(method, params = {}) {
      return new Promise((resolve) => {
        const id = msgId++;
        bws.send(JSON.stringify({ id, method, params }));
        bws.on('message', function handler(raw) {
          const resp = JSON.parse(raw.toString());
          if (resp.id === id) { bws.removeListener('message', handler); resolve(resp); }
        });
      });
    }

    const createResp = await bsend('Target.createTarget', { url: 'about:blank' });
    if (!createResp.result) throw new Error('Failed to create target');
    const targetId = createResp.result.targetId;
    await new Promise(r => setTimeout(r, 2000));
    bws.close();

    // Get target's own WS URL
    const targets = await fetchJson(`http://127.0.0.1:${CDP_PORT}/json`);
    const ourTarget = targets.find(t => t.id === targetId);
    if (!ourTarget) throw new Error('Target not found');

    const tws = new WebSocket(ourTarget.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => {
      tws.on('open', resolve);
      tws.on('error', reject);
    });

    let msgId2 = 1;
    function tsend(method, params = {}) {
      return new Promise((resolve) => {
        const id = msgId2++;
        tws.send(JSON.stringify({ id, method, params }));
        tws.on('message', function handler(raw) {
          const resp = JSON.parse(raw.toString());
          if (resp.id === id) { tws.removeListener('message', handler); resolve(resp); }
        });
      });
    }

    await tsend('Page.enable');
    await tsend('Page.navigate', { url: `http://127.0.0.1:${HTTP_PORT}` });
    await new Promise(r => setTimeout(r, 5000));

    const pdfResp = await tsend('Page.printToPDF', {
      displayHeaderFooter: false,
      printBackground: true,
      marginTop: 0.4,
      marginBottom: 0.4,
      marginLeft: 0.6,
      marginRight: 0.6,
      paperWidth: 8.27,
      paperHeight: 11.69
    });

    if (!pdfResp.result || !pdfResp.result.data) {
      throw new Error('printToPDF failed: ' + JSON.stringify(pdfResp));
    }

    fs.writeFileSync(pdfPath, Buffer.from(pdfResp.result.data, 'base64'));
    const size = fs.statSync(pdfPath).size;

    console.log(`✅ PDF_OK ${(size / 1024).toFixed(0)}KB`);
    tws.close();
  } catch (err) {
    console.error('❌ ERROR', err.message || err);
    process.exitCode = 1;
  }

  server.close();
  chrome.kill('SIGKILL');
  setTimeout(() => process.exit(process.exitCode || 0), 200);
})();
