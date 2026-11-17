#!/usr/bin/env node
/* Locale: zh-CN (documented in SKILL.md metadata) — "Lan Folder Share" is a LAN
 * knowledge-base tool built for Chinese-speaking users; its messages and
 * comments are Chinese by design. 语言声明：本文件面向中文用户，提示与注释默认中文。
 * ---------------------------------------------------------------------------
 * lan-knowledge-share —— 一键将本地文件目录部署为局域网可访问的知识库
 *
 * 用法：
 *   node deploy.js [内容目录] [选项]
 *
 * 选项：
 *   -p, --port <n>      监听端口（默认 8089；被占用时自动 +1 重试）
 *   -n, --name <名>     站点名称（默认取内容目录名）
 *   -h, --host <ip>     监听地址（默认 0.0.0.0，局域网可访问）
 *   -r, --runtime <dir> 前端运行时目录（默认技能包内置 assets/runtime）
 *       --no-readme     关闭「内置默认首页」：内容目录始终零写入、不生成任何
 *                       站点文件；根目录无 README.md 时首页显示目录索引页
 *       --open          启动成功后自动打开浏览器
 *       --exclude <a,b> 额外排除的目录名（逗号分隔，不出现在目录树/搜索）
 *   -v, --version       输出版本号
 *       --help          显示帮助
 *
 * 两种部署形态：
 *   1) 任意纯内容目录（md/表格/图片/网页报告…）→ 自动注入内置前端运行时，
 *      内容目录本身不落任何站点文件，目录长什么样页面就什么样；
 *   2) 自包含知识库目录（根目录已有 index.html + assets，如本仓库形态）→
 *      完全按原逻辑托管，内置运行时仅作缺失资源兜底。
 *
 * 目录/文件改动实时生效（每次请求实时扫描文件系统）；全站搜索支持 md 正文
 * 与表格（xlsx/csv 等）单元格，服务端用内置 SheetJS 解析。
 */
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const VERSION = '1.0.12';

/* ───────────────────────── 参数解析 ───────────────────────── */
function parseArgs(argv) {
  const cfg = { dir: '.', port: 8089, host: '0.0.0.0', name: null, runtime: null,
                noReadme: false, open: false, excludes: [] };
  const args = argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    const next = () => args[++i];
    switch (a) {
      case '-p': case '--port': cfg.port = parseInt(next(), 10) || 8089; break;
      case '-n': case '--name': cfg.name = next(); break;
      case '-h': case '--host': cfg.host = next(); break;
      case '-r': case '--runtime': cfg.runtime = next(); break;
      case '--no-readme': cfg.noReadme = true; break;
      case '--open': cfg.open = true; break;
      case '--exclude':
        (next() || '').split(',').map(s => s.trim()).filter(Boolean).forEach(x => cfg.excludes.push(x));
        break;
      case '-v': case '--version': console.log('lan-knowledge-share ' + VERSION); process.exit(0); break;
      case '--help':
        fs.readFileSync(__filename, 'utf8').split('\n').slice(1, 18).forEach(l => console.log(l.replace(/^ \* ?/, '')));
        process.exit(0);
        break;
      default:
        if (a.startsWith('-')) { console.error('未知参数: ' + a + '\n运行 node deploy.js --help 查看用法'); process.exit(2); }
        cfg.dir = a;
    }
  }
  return cfg;
}

/* ───────────────────────── 常量 ───────────────────────── */
const MIME = {
  '.md': 'text/markdown; charset=utf-8',
  '.html': 'text/html; charset=utf-8',
  '.htm': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.gif': 'image/gif', '.svg': 'image/svg+xml', '.webp': 'image/webp',
  '.bmp': 'image/bmp', '.ico': 'image/x-icon',
  '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  '.xls': 'application/vnd.ms-excel', '.csv': 'text/csv; charset=utf-8',
  '.tsv': 'text/tab-separated-values; charset=utf-8',
  '.pdf': 'application/pdf', '.zip': 'application/zip',
  '.mp4': 'video/mp4', '.webm': 'video/webm', '.mov': 'video/quicktime',
  '.mp3': 'audio/mpeg', '.wav': 'audio/wav', '.ogg': 'audio/ogg',
  '.doc': 'application/msword',
  '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  '.ppt': 'application/vnd.ms-powerpoint',
  '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  '.txt': 'text/plain; charset=utf-8',
  // 字体文件（设计资源）：按标准字体 MIME 返回，浏览器可直接下载或引用
  '.ttf': 'font/ttf',
  '.otf': 'font/otf',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.eot': 'application/vnd.ms-fontobject',
};
// 通用技术噪音目录（任何部署形态都排除）
const NOISE_DIRS = new Set(['.git', '.svn', '.hg', 'node_modules', '__pycache__', '.idea',
  '.vscode', '.codebuddy', 'venv', '.venv', '.tox', '.pytest_cache']);
// 自包含知识库形态下额外排除的站点内部目录
const SITE_DIRS = new Set(['assets', 'sync', 'tests', 'vendor', '.workbuddy']);
const INDEX_FILES = new Set(['_sidebar.md', '_footer.md', '_side.md', 'index.html']);
const SHEET_EXTS = new Set(['.xlsx', '.xls', '.csv', '.tsv']);
const CONTENT_EXTS = new Set([
  '.md', '.xlsx', '.xls', '.csv', '.tsv',
  '.html', '.htm',
  '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.txt',
  '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp',
  '.mp4', '.mov', '.webm',
  '.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac', '.wma',
  // 字体文件（设计资源）：收录后侧边栏/目录页可见并可下载
  '.ttf', '.otf', '.woff', '.woff2', '.eot',
]);
const CACHEABLE_EXTS = new Set(['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp', '.ico', '.xlsx', '.xls']);

/* ── 文本类文件（.txt / .html）全文检索 ─────────────────────────
 * 与 md / 表格同一套实时缓存规则：mtime + size 未变则复用解析结果，
 * 文件内容更新后下一次搜索自动生效，无需重启。
 * 其余内容文件（图片/音视频/PDF/Office…）不做正文解析，按文件名即可搜索定位。
 */
const TEXT_EXTS = new Set(['.txt', '.html', '.htm']);
const FILE_TAGS = {
  '.txt': '文本', '.html': 'HTML 报告', '.htm': 'HTML 报告',
  '.ttf': '字体', '.otf': '字体', '.woff': '字体', '.woff2': '字体', '.eot': '字体',
  '.pdf': 'PDF', '.doc': 'Word', '.docx': 'Word', '.ppt': 'PPT', '.pptx': 'PPT',
  '.jpg': '图片', '.jpeg': '图片', '.png': '图片', '.gif': '图片', '.svg': '图片', '.webp': '图片', '.bmp': '图片',
  '.mp4': '视频', '.mov': '视频', '.webm': '视频',
  '.mp3': '音频', '.wav': '音频', '.ogg': '音频', '.m4a': '音频', '.aac': '音频', '.flac': '音频', '.wma': '音频',
};

function htmlToPlain(h) {
  return String(h)
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<!--[\s\S]*?-->/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/gi, ' ').replace(/&amp;/gi, '&').replace(/&lt;/gi, '<').replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"').replace(/&#39;/gi, "'")
    .replace(/\s+/g, ' ').trim();
}

function fileTag(ext) {
  return FILE_TAGS[ext] || '文件';
}

function collectSearchFiles(root, isExcludedDir) {
  // 搜索候选文件清单（实时扫描磁盘）：md 全量（含根 README）+ 表格 + 其余可展示文件。
  // 与 makeManifest 的分工：makeManifest 供目录展示/静态首页引用，这里专供全文搜索，
  // 确保目录里任何内容文件的新增/删除/修改都在下一次搜索立即生效。
  const md = [], sheets = [], others = [];
  (function walk(dir, relDir) {
    for (const it of readDirSafe(dir)) {
      if (it.isDirectory()) {
        if (isExcludedDir(it.name) || it.name.startsWith('.')) continue;
        walk(path.join(dir, it.name), relDir ? relDir + '/' + it.name : it.name);
      } else if (it.isFile()) {
        const low = it.name.toLowerCase();
        if (INDEX_FILES.has(low) || low.includes('_conflict.md')) continue;
        const ext = path.extname(it.name).toLowerCase();
        if (!CONTENT_EXTS.has(ext)) continue;
        const rel = relDir ? relDir + '/' + it.name : it.name;
        if (ext === '.md') md.push(rel);
        else if (SHEET_EXTS.has(ext)) sheets.push(rel);
        else others.push({ rel, ext });
      }
    }
  })(root, '');
  md.sort();
  sheets.sort();
  others.sort((a, b) => a.rel.localeCompare(b.rel));
  return { md, sheets, others };
}

/* ───────────────────────── 文件系统扫描（实时） ───────────────────────── */
function readDirSafe(dir) {
  try { return fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return []; }
}

function makeTree(root, isExcludedDir) {
  const tree = {};
  (function walk(dir, relKey) {
    const entries = [];
    const items = readDirSafe(dir);
    const dirs = items.filter(i => i.isDirectory() && !isExcludedDir(i.name) && !i.name.startsWith('.'));
    const files = items.filter(i => i.isFile());
    dirs.sort((a, b) => a.name.localeCompare(b.name));
    files.sort((a, b) => a.name.localeCompare(b.name));
    for (const d of dirs) entries.push({ name: d.name, type: 'dir' });
    for (const f of files) {
      const low = f.name.toLowerCase();
      if (INDEX_FILES.has(low) || low.includes('_conflict.md')) continue;
      const ext = path.extname(f.name).toLowerCase().replace(/^\./, '');
      if (!CONTENT_EXTS.has('.' + ext)) continue;
      entries.push({ name: f.name, type: 'file', ext });
    }
    tree[relKey] = entries;
    for (const d of dirs) walk(path.join(dir, d.name), relKey ? relKey + '/' + d.name : d.name);
  })(root, '');
  return tree;
}

function makeManifest(root, isExcludedDir) {
  const md = [], sheets = [];
  (function walk(dir) {
    const items = readDirSafe(dir);
    for (const it of items) {
      const full = path.join(dir, it.name);
      if (it.isDirectory()) {
        if (isExcludedDir(it.name) || it.name.startsWith('.')) continue;
        walk(full);
      } else if (it.isFile()) {
        const ext = path.extname(it.name).toLowerCase();
        const rel = path.relative(root, full).split(path.sep).join('/');
        if (ext === '.md') {
          if (dir === root && (it.name.toLowerCase() === 'readme.md' || it.name.toLowerCase() === '_sidebar.md')) continue;
          md.push(rel);
        } else if (SHEET_EXTS.has(ext)) {
          sheets.push(rel);
        }
      }
    }
  })(root);
  md.sort(); sheets.sort();
  return { md, sheets };
}

/* ───────────────────────── 全文搜索（服务端） ───────────────────────── */
const mdCache = new Map();
const sheetCache = new Map();
const textCache = new Map();  // 文本文件(.txt/.html)全文解析缓存，按 mtime+size 实时失效
let refMap = null, refMapStamp = null;

function fileStamp(full) {
  try { const s = fs.statSync(full); return { mtimeMs: s.mtimeMs, size: s.size }; } catch (e) { return null; }
}

function fileTextData(root, rel) {
  const full = path.join(root, rel);
  const st = fileStamp(full);
  if (!st) return null;
  const hit = textCache.get(full);
  if (hit && hit.mtimeMs === st.mtimeMs && hit.size === st.size) return hit;
  // 超大文件跳过正文解析（>2MB），仅保留文件名可搜
  if (st.size > 2 * 1024 * 1024) {
    const big = { mtimeMs: st.mtimeMs, size: st.size, text: '', low: '', oversized: true };
    textCache.set(full, big);
    return big;
  }
  let buf;
  try { buf = fs.readFileSync(full); } catch (e) { return null; }
  // 常见纯文本编码解码：UTF-8 / UTF-16 LE、BE（带 BOM），无 BOM 时按 UTF-16LE 特征启发式判断
  let raw = '';
  const n = buf.length;
  if (n >= 2 && buf[0] === 0xFF && buf[1] === 0xFE) {
    raw = buf.slice(2).toString('utf16le');
  } else if (n >= 2 && buf[0] === 0xFE && buf[1] === 0xFF) {
    raw = buf.slice(2).swap16().toString('utf16le');
  } else if (n >= 3 && buf[0] === 0xEF && buf[1] === 0xBB && buf[2] === 0xBF) {
    raw = buf.slice(3).toString('utf8');
  } else if (n > 4 && (n % 2 === 0)) {
    let zeroOdd = 0;
    for (let i = 1; i < n; i += 2) if (buf[i] === 0) zeroOdd++;
    raw = (zeroOdd >= (n / 2) * 0.6) ? buf.toString('utf16le') : buf.toString('utf8');
  } else {
    raw = buf.toString('utf8');
  }
  const ext = path.extname(rel).toLowerCase();
  const text = (ext === '.html' || ext === '.htm') ? htmlToPlain(raw) : raw;
  const c = { mtimeMs: st.mtimeMs, size: st.size, text, low: text.toLowerCase(), oversized: false };
  textCache.set(full, c);
  return c;
}

function mdData(root, rel) {
  const full = path.join(root, rel);
  const st = fileStamp(full);
  if (!st) return null;
  const hit = mdCache.get(full);
  if (hit && hit.mtimeMs === st.mtimeMs && hit.size === st.size) return hit;
  let raw;
  try { raw = fs.readFileSync(full, 'utf8'); } catch (e) { return null; }
  let body = raw;
  if (/^---\r?\n[\s\S]*?\r?\n---/.test(body)) body = body.replace(/^---\r?\n[\s\S]*?\r?\n---/, '');
  const c = { mtimeMs: st.mtimeMs, size: st.size, body, low: body.toLowerCase() };
  mdCache.set(full, c);
  return c;
}

function mdTitle(rel, body) {
  let title = rel.split('/').pop().replace(/\.md$/i, '');
  const m = body.match(/^#\s+(.+)$/m) || body.match(/^##\s+(.+)$/m);
  if (m) title = m[1].trim();
  return title;
}

function sheetData(root, rel, xlsxLib) {
  const full = path.join(root, rel);
  const st = fileStamp(full);
  if (!st) return null;
  const hit = sheetCache.get(full);
  if (hit && hit.mtimeMs === st.mtimeMs && hit.size === st.size) return hit;
  let buf;
  try { buf = fs.readFileSync(full); } catch (e) { return null; }
  const sheets = [];
  try {
    const wb = xlsxLib.read(buf, { type: 'buffer' });
    (wb.SheetNames || []).forEach((name) => {
      const ws = wb.Sheets[name];
      const rows = [];
      if (ws && ws['!ref']) {
        try {
          const raw = xlsxLib.utils.sheet_to_json(ws, { header: 1, defval: '', blankrows: false, raw: false });
          for (const r of raw) {
            const cells = [];
            let any = false;
            for (let j = 0; j < r.length; j++) {
              const v = r[j] == null ? '' : String(r[j]).replace(/\s+$/, '');
              if (v !== '') any = true;
              cells.push(v);
            }
            if (any) rows.push(cells);
          }
        } catch (e) { /* 单个 sheet 解析失败不影响整体 */ }
      }
      sheets.push({ name, rows, text: rows.map(r => r.join(' ')).join('\n') });
    });
  } catch (e) { /* 解析失败 → 空 */ }
  const all = sheets.map(s => s.text).join('\n');
  const c = { mtimeMs: st.mtimeMs, size: st.size, sheets, all, low: all.toLowerCase() };
  sheetCache.set(full, c);
  return c;
}

function buildRefMap(root, xlsxLib, isExcludedDir) {
  const { md, sheets } = makeManifest(root, isExcludedDir);
  const stamp = md.map(p => { const c = mdData(root, p); return c ? p + ':' + c.mtimeMs + ':' + c.size : p + ':0:0'; }).join('|');
  if (refMapStamp === stamp && refMap) return refMap;
  const map = {};
  for (const sp of sheets) {
    const fn = sp.split('/').pop();
    const enc = encodeURI(fn);
    for (const mp of md) {
      const c = mdData(root, mp);
      if (!c) continue;
      if (c.body.indexOf(fn) !== -1 || c.body.indexOf(enc) !== -1) { map[sp] = mp; break; }
    }
  }
  refMap = map; refMapStamp = stamp;
  return map;
}

function snippetOf(body, low, kws, width) {
  let first = -1;
  for (const kw of kws) {
    const p = low.indexOf(kw);
    if (p !== -1 && (first === -1 || p < first)) first = p;
  }
  if (first === -1) return '';
  const start = Math.max(0, first - 20);
  const cut = body.substr(start, width || 120).replace(/\s+/g, ' ').trim();
  return (start > 0 ? '…' : '') + cut;
}

function countHits(lowText, kw) {
  let cnt = 0, from = 0, idx;
  while ((idx = lowText.indexOf(kw, from)) !== -1 && cnt < 99) { cnt++; from = idx + kw.length; }
  return cnt;
}

function searchAll(root, q, xlsxLib, isExcludedDir) {
  const kws = q.toLowerCase().split(/\s+/).filter(Boolean);
  if (!kws.length) return [];
  const { md, sheets, others } = collectSearchFiles(root, isExcludedDir);
  const results = [];

  for (const p of md) {
    const c = mdData(root, p);
    if (!c) continue;
    let score = 0, ok = true;
    for (const kw of kws) {
      if (c.low.indexOf(kw) === -1) { ok = false; break; }
      score += countHits(c.low, kw);
    }
    if (!ok) continue;
    const title = mdTitle(p, c.body);
    for (const kw of kws) if (title.toLowerCase().indexOf(kw) !== -1) score += 8;
    results.push({ type: 'md', title, path: p, score, snippet: snippetOf(c.body, c.low, kws) });
  }

  if (xlsxLib) {
    let refs = null;
    for (const p of sheets) {
      const d = sheetData(root, p, xlsxLib);
      if (!d) continue;
      let score = 0, ok = true;
      for (const kw of kws) {
        if (d.low.indexOf(kw) === -1) { ok = false; break; }
        score += countHits(d.low, kw);
      }
      if (!ok) continue;
      const hitRows = [];
      for (const s of d.sheets) {
        const idxs = [];
        for (let i = 0; i < s.rows.length; i++) {
          const line = s.rows[i].join('\n').toLowerCase();
          if (kws.every(kw => line.indexOf(kw) !== -1)) idxs.push(i);
        }
        if (idxs.length) hitRows.push({ name: s.name, rows: idxs });
      }
      const hitSheets = hitRows.length
        ? hitRows.map(h => h.name)
        : d.sheets.filter(s => kws.every(kw => s.text.toLowerCase().indexOf(kw) !== -1)).map(s => s.name);
      let snippet;
      if (hitRows.length) {
        const sh = d.sheets.find(s => s.name === hitRows[0].name) || null;
        const rowText = sh && sh.rows[hitRows[0].rows[0]] ? sh.rows[hitRows[0].rows[0]].join('　') : '';
        snippet = rowText ? '命中第 ' + (hitRows[0].rows[0] + 1) + ' 行：' + rowText : snippetOf(d.all, d.low, kws);
      } else {
        snippet = snippetOf(d.all, d.low, kws);
      }
      if (!refs) refs = buildRefMap(root, xlsxLib, isExcludedDir);
      results.push({
        type: 'sheet', title: p.split('/').pop(), path: p, score,
        snippet, hitSheets, hitRows, refPage: refs[p] || null,
      });
    }
  }

  // 其余内容文件：.txt/.html 做正文全文搜索；媒体/PDF/Office 等至少按文件名搜索
  for (const o of others) {
    const rel = o.rel;
    const name = rel.split('/').pop();
    const title = name.replace(/\.[^.]+$/, '');
    const titleLow = title.toLowerCase();
    let score = 0;

    // 正文全文匹配（txt 直接全文；html 剥掉标签后检索）
    const td = TEXT_EXTS.has(o.ext) ? fileTextData(root, rel) : null;
    const contentOk = td && !td.oversized && td.low &&
      kws.every(kw => td.low.indexOf(kw) !== -1);
    if (contentOk) {
      for (const kw of kws) score += countHits(td.low, kw);
      for (const kw of kws) if (titleLow.indexOf(kw) !== -1) score += 8;
    }

    // 文件名/路径匹配：完整文件名（含扩展名）与相对路径都参与，
    // 保证任意类型文件新增后即使只记得文件名也能被搜出来
    const nameLow = rel.toLowerCase();
    const nameOk = kws.every(kw => nameLow.indexOf(kw) !== -1);
    if (nameOk) {
      score += 6;
      for (const kw of kws) if (titleLow.indexOf(kw) !== -1) score += 8;
    }

    if (!contentOk && !nameOk) continue;
    const snippet = contentOk ? snippetOf(td.text, td.low, kws) : '';
    results.push({ type: 'file', title, path: rel, score, snippet, tag: fileTag(o.ext) });
  }

  results.sort((a, b) => b.score - a.score);
  return results;
}

/* ───────────────────────── 工具 ───────────────────────── */
function sendJson(res, data) {
  const body = JSON.stringify(data);
  res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-cache' });
  res.end(body);
}

function safeJoin(base, decoded) {
  const abs = path.normalize(path.join(base, decoded));
  if (abs !== base && !abs.startsWith(base + path.sep)) return null;  // 防目录穿越
  return abs;
}

function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function lanIPv4s() {
  const out = [];
  const ifs = os.networkInterfaces();
  for (const name of Object.keys(ifs)) {
    for (const it of ifs[name] || []) {
      if (it.family === 'IPv4' && !it.internal) out.push(it.address);
    }
  }
  return out;
}

function openBrowser(url) {
  const cmd = process.platform === 'win32' ? 'start "" "' + url + '"'
    : process.platform === 'darwin' ? 'open "' + url + '"'
    : 'xdg-open "' + url + '"';
  try { require('child_process').exec(cmd); } catch (e) { /* 忽略 */ }
}

/* ───────────────────────── 主流程 ───────────────────────── */
function main() {
  const cfg = parseArgs(process.argv);
  const root = path.resolve(cfg.dir);

  if (!fs.existsSync(root) || !fs.statSync(root).isDirectory()) {
    console.error('内容目录不存在或不是目录: ' + root);
    process.exit(2);
  }

  const selfContained = fs.existsSync(path.join(root, 'index.html'));
  const runtimeDir = cfg.runtime
    ? path.resolve(cfg.runtime)
    : path.join(__dirname, '..', 'assets', 'runtime');
  const runtimeOk = fs.existsSync(path.join(runtimeDir, 'index.html'));

  if (!selfContained && !runtimeOk) {
    console.error('既不是自包含知识库目录，也找不到前端运行时目录: ' + runtimeDir);
    console.error('请通过 --runtime 指定运行时目录，或将 index.html + assets 放入内容目录。');
    process.exit(2);
  }

  const siteName = cfg.name || path.basename(root) || '知识库';
  const excludeSet = new Set(NOISE_DIRS);
  cfg.excludes.forEach(x => excludeSet.add(x));
  if (selfContained) SITE_DIRS.forEach(x => excludeSet.add(x));
  const isExcludedDir = (name) => excludeSet.has(name);

  // 纯内容目录保持「零写入」：不在共享目录里生成 README.md 或任何站点文件，
  // 目录里有什么文件、页面就只展示什么。根目录无 README.md 且未指定 --no-readme 时，
  // 由服务端在请求时于内存中渲染温和默认首页（见下方请求处理）；用户如需自定义首页，
  // 直接在内容目录自行创建 README.md 即可，服务端会优先返回真实文件。

  // 内置 SheetJS 定位（自包含目录优先用其自身 vendor，否则用 runtime vendor）
  let xlsxLib = null;
  const vendorCandidates = [
    path.join(root, 'assets', 'vendor', 'xlsx.full.min.js'),
    path.join(runtimeDir, 'assets', 'vendor', 'xlsx.full.min.js'),
  ];
  for (const v of vendorCandidates) {
    if (fs.existsSync(v)) {
      try { xlsxLib = require(v); break; } catch (e) { xlsxLib = null; }
    }
  }
  if (!xlsxLib) console.warn('[deploy] 警告: 未找到 xlsx.full.min.js，表格文件将无法参与全文搜索（页面内预览不受影响）');

  // ── HTTP 服务 ──
  const server = http.createServer((req, res) => {
    const urlPath = (req.url || '/').split('?')[0].split('#')[0];

    if (urlPath === '/api/tree' || urlPath.endsWith('/api/tree')) { sendJson(res, makeTree(root, isExcludedDir)); return; }
    if (urlPath === '/api/manifest' || urlPath.endsWith('/api/manifest')) { sendJson(res, makeManifest(root, isExcludedDir)); return; }
    if (urlPath === '/api/search' || urlPath.endsWith('/api/search')) {
      let q = '';
      try { q = (new URL(req.url, 'http://localhost').searchParams.get('q') || '').trim().slice(0, 200); } catch (e) { q = ''; }
      if (!q) { sendJson(res, { q, count: 0, results: [] }); return; }
      let results = [];
      try { results = searchAll(root, q, xlsxLib, isExcludedDir); } catch (e) { results = []; }
      sendJson(res, { q, count: results.length, results });
      return;
    }

    let decoded;
    try { decoded = decodeURIComponent(urlPath); } catch (e) { decoded = urlPath; }
    if (decoded === '/') decoded = '/index.html';

    const hit = resolveStatic(decoded);
    if (!hit) {
      // 纯内容目录的虚拟默认首页（内存渲染，零写入）：docsify 加载首页时会
      // 请求根 README.md，根目录没有该文件时此处返回温和占位首页而非 404。
      if (!selfContained && !cfg.noReadme && /^\/readme\.md$/i.test(decoded)) {
        const md = '# ' + siteName + '\n\n' +
          '> 本目录由 **lan-knowledge-share**（局域网知识库一键共享）提供服务，页面随文件实时更新。\n\n' +
          '- 支持 Markdown 文档、Excel/CSV 表格在线预览、HTML 网页报告、图片画廊、全文搜索\n' +
          '- 将文档放入子目录即可出现在左侧导航；本页为自动生成的占位首页（内容目录保持零写入），如需自定义首页请在内容目录自行创建 README.md\n';
        res.writeHead(200, { 'Content-Type': 'text/markdown; charset=utf-8', 'Cache-Control': 'no-cache' });
        res.end(md);
        return;
      }
      res.writeHead(404);
      res.end('Not Found');
      return;
    }

    // 运行时 index.html → 注入站点名
    if (hit.template) {
      try {
        const raw = fs.readFileSync(hit.abs, 'utf8');
        const html = raw
          .split('__KB_NAME_HTML__').join(escapeHtml(siteName))
          .split('__KB_NAME_JSON__').join(JSON.stringify(siteName));
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-cache' });
        res.end(html);
        return;
      } catch (e) { /* fallthrough */ }
    }

    serveStatic(res, hit.abs, req);
  });

  // 资源解析：内容目录优先 → 运行时兜底（自包含知识库即内容目录命中）
  function resolveStatic(decoded) {
    const rel = decoded.replace(/^\/+/, '');
    const p = safeJoin(root, rel);
    if (p) {
      const t = fileOrIndex(p);
      if (t) return { abs: t, template: false };
    }
    if (runtimeOk) {
      const pr = safeJoin(runtimeDir, rel);
      if (pr) {
        const t = fileOrIndex(pr);
        if (t) return { abs: t, template: rel === 'index.html' && !selfContained };
      }
    }
    return null;
  }

  function fileOrIndex(p) {
    try {
      const st = fs.statSync(p);
      if (st.isFile()) return p;
      if (st.isDirectory()) {
        const idx = safeJoin(p, 'index.html');
        if (idx && fs.existsSync(idx)) return idx;
      }
    } catch (e) { /* 不存在 */ }
    return null;
  }

  // 静态文件响应：支持标准 HTTP Range（视频/音频 seek 必需，Safari/iOS 强依赖）。
  //   - 带 Range → 206 Partial Content + Content-Range + Content-Length
  //   - bytes=start-end / bytes=start- / bytes=-N（后缀）三种写法
  //   - 越界 → 416 + Content-Range: bytes */size
  //   - 无 Range → 200 整段 + Accept-Ranges: bytes + Content-Length
  //   - HEAD → 只回状态与头，不传 body
  function serveStatic(res, abs, req) {
    let st;
    try { st = fs.statSync(abs); } catch (e) {
      res.writeHead(404);
      res.end('Not Found');
      return;
    }
    const size = st.size;
    const ext = path.extname(abs).toLowerCase();
    const headers = {
      'Content-Type': MIME[ext] || 'application/octet-stream',
      'Accept-Ranges': 'bytes',
      'Cache-Control': CACHEABLE_EXTS.has(ext) ? 'public, max-age=3600' : 'no-cache',
    };
    const isHead = req && req.method === 'HEAD';
    const range = req && req.headers && req.headers.range;

    if (range) {
      const m = /^bytes=(\d*)-(\d*)$/.exec(String(range).trim());
      if (m) {
        let start = m[1] === '' ? null : parseInt(m[1], 10);
        let end = m[2] === '' ? null : parseInt(m[2], 10);
        if (start === null) {
          // 后缀请求 bytes=-N：取文件末尾 N 字节
          const n = end;
          if (n == null || n <= 0 || size <= 0) {
            res.writeHead(416, { 'Content-Range': 'bytes */' + size });
            res.end();
            return;
          }
          start = Math.max(0, size - n);
          end = size - 1;
        } else {
          if (end === null) end = size - 1;
          end = Math.min(end, size - 1);
        }
        if (start >= size || start > end) {
          res.writeHead(416, { 'Content-Range': 'bytes */' + size });
          res.end();
          return;
        }
        headers['Content-Range'] = 'bytes ' + start + '-' + end + '/' + size;
        headers['Content-Length'] = String(end - start + 1);
        if (isHead) { res.writeHead(206, headers); res.end(); return; }
        res.writeHead(206, headers);
        const rs = fs.createReadStream(abs, { start, end });
        rs.on('error', () => { try { res.end(); } catch (err) { /* 已断开 */ } });
        rs.pipe(res);
        return;
      }
      // 无法解析的 Range 头：按 RFC 7233 忽略，回完整内容（下面 200 分支）
    }

    headers['Content-Length'] = String(size);
    if (isHead) { res.writeHead(200, headers); res.end(); return; }
    res.writeHead(200, headers);
    const stream = fs.createReadStream(abs);
    stream.on('error', () => {
      if (!res.headersSent) res.writeHead(500);
      res.end('Internal Server Error');
    });
    stream.pipe(res);
  }

  // 端口占用自动 +1 重试
  function tryListen(port) {
    server.listen(port, cfg.host, () => {
      const url = 'http://127.0.0.1:' + port;
      const lans = lanIPv4s();
      console.log('');
      console.log('  lan-knowledge-share v' + VERSION + '  站名: ' + siteName);
      console.log('  内容目录: ' + root + (selfContained ? '  （自包含知识库）' : ''));
      console.log('  本机访问: ' + url);
      if (lans.length) {
        console.log('  局域网分享:');
        for (const ip of lans) console.log('    http://' + ip + ':' + port);
      } else {
        console.log('  局域网分享: 未检测到局域网 IPv4（请确认网卡已联网）');
      }
      console.log('  提示: 目录文件增删改实时生效；内容目录零写入（不生成任何文件）；Ctrl+C 停止服务');
      console.log('  安全: 该服务无鉴权，局域网内任意可达设备均可浏览，请勿共享含敏感信息的目录');
      console.log('');
      if (cfg.open) openBrowser(url);
      // 预热 md / 表格解析缓存，避免首次搜索卡顿
      setTimeout(() => {
        try {
          const { md, sheets } = makeManifest(root, isExcludedDir);
          md.forEach(p => mdData(root, p));
          if (xlsxLib) sheets.forEach(p => sheetData(root, p, xlsxLib));
          console.log('[deploy] 搜索缓存预热完成：' + md.length + ' 篇 md / ' + sheets.length + ' 个表格');
        } catch (e) { /* 预热失败不影响搜索 */ }
      }, 1500);
    });
    server.on('error', (e) => {
      if (e.code === 'EADDRINUSE' && port < 65535) {
        server.removeAllListeners('error');
        tryListen(port + 1);
      } else {
        console.error('服务启动失败:', e.message);
        process.exit(1);
      }
    });
  }

  process.on('SIGINT', () => {
    console.log('\n[deploy] 已停止服务');
    server.close(() => process.exit(0));
    setTimeout(() => process.exit(0), 800);
  });

  tryListen(cfg.port);
}

main();
