#!/usr/bin/env node
// md-preview.js — 本地 live preview server
//
// 起一个 http 服务,文件改动自动 reload(轻量轮询,不依赖 watch)。
// 适合写作时另开窗口看效果——比 Typora 的 WYSIWYG 慢半拍但同等保真。
//
// 用法:
//   node md-preview.js <input.md> [--port 7777] [--theme typora-newsprint]

const fs = require('fs');
const http = require('http');
const path = require('path');
const { buildHtml, AVAILABLE_THEMES } = require('./lib/render.js');

function parseArgs(argv) {
  const out = { positional: [], opts: {} };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const k = a.slice(2); const n = argv[i + 1];
      if (n === undefined || n.startsWith('--')) out.opts[k] = true;
      else { out.opts[k] = n; i++; }
    } else out.positional.push(a);
  }
  return out;
}

const args = parseArgs(process.argv.slice(2));
const [inputPath] = args.positional;
if (!inputPath) {
  console.error('用法: md-preview.js <input.md> [--port 7777] [--theme typora-newsprint]');
  console.error('主题: ' + AVAILABLE_THEMES.join(' / '));
  process.exit(1);
}
if (!fs.existsSync(inputPath)) { console.error(`找不到: ${inputPath}`); process.exit(1); }

const port = parseInt(args.opts.port || '7777', 10);
let theme = args.opts.theme || 'typora-newsprint';
const absInput = path.resolve(inputPath);

const RELOAD_SCRIPT = `
<script>
(function() {
  let lastSig = '';
  setInterval(async () => {
    try {
      const r = await fetch('/__sig');
      const sig = await r.text();
      if (lastSig && sig !== lastSig) location.reload();
      lastSig = sig;
    } catch (_) {}
  }, 800);
})();
</script>
`;

function readSig() {
  const stat = fs.statSync(absInput);
  return `${stat.mtimeMs}-${stat.size}-${theme}`;
}

const server = http.createServer((req, res) => {
  if (req.url === '/__sig') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end(readSig());
    return;
  }
  if (req.url.startsWith('/__theme/')) {
    const t = req.url.slice('/__theme/'.length);
    if (AVAILABLE_THEMES.includes(t)) theme = t;
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('ok');
    return;
  }
  try {
    const md = fs.readFileSync(absInput, 'utf8');
    const html = buildHtml({
      markdown: md,
      theme,
      title: path.basename(absInput, '.md'),
      includePrint: false,
      includeMermaid: true,
    });
    const themeNav = AVAILABLE_THEMES.map(t =>
      `<a href="javascript:fetch('/__theme/${t}').then(()=>location.reload())" style="margin-right:8px;color:${t === theme ? '#c0392b' : '#888'}">${t}</a>`
    ).join(' · ');
    const banner = `<div style="position:fixed;top:0;left:0;right:0;background:#fff;border-bottom:1px solid #eee;padding:6px 12px;font-size:12px;font-family:sans-serif;z-index:9999">huo15-md-preview · ${path.basename(absInput)} · ${themeNav}</div><div style="height:36px"></div>`;
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(html.replace('<body', '<body').replace('</body>', `${banner}${RELOAD_SCRIPT}</body>`));
  } catch (e) {
    res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end(String(e));
  }
});

server.listen(port, () => {
  console.error(`✓ live preview: http://127.0.0.1:${port}/  watching ${absInput}`);
  console.error(`  改动文件自动刷新;切主题点顶栏`);
});
