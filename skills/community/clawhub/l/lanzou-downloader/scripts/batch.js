#!/usr/bin/env node
/**
 * lanzou-downloader 批量下载路由（纯 Node.js，零依赖）
 *
 * 用法:
 *   node scripts/batch.js --urls "<url1>" "<url2>" ...
 *   node scripts/batch.js --file links.txt|links.md|links.json
 *   node scripts/batch.js --file links.txt --select 1,3,5
 *   node scripts/batch.js --file links.txt --select all
 *   node scripts/batch.js --manifest /path/.lanzou_manifest.json --select 2
 *   node scripts/batch.js --urls "<url>" --list        # 只解析，不下载
 *   node scripts/batch.js --file links.txt --json      # 机器可读清单（stdout 仅 JSON）
 *
 * 支持在一个参数里用空格/换行分隔多个链接；txt/md 行内可直接写
 * 「密码:xxxx / 提取码:xxxx / pwd:xxxx」，会自动作为该链接的密码。
 * --password 可指定所有链接的统一密码。
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const HERE = __dirname;
const DOWNLOAD_JS = path.join(HERE, 'download.js');
const LIST_PREFIX = '__LANZOU_LIST__';
const URL_RE = /https?:\/\/[^\s"'<>)\]]+/g;
const PWD_RE = /(?:密码|提取码|访问码|pwd|password)\s*[:：=]?\s*([A-Za-z0-9]{3,12})/i;
const MANIFEST_NAME = '.lanzou_manifest.json';

function log(...a) { console.error(...a); }

function parseArgs(argv) {
  const o = { urls: [], files: [], select: null, outDir: null, manifest: null, listOnly: false, json: false, password: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--urls') { while (argv[i + 1] && !argv[i + 1].startsWith('--')) o.urls.push(argv[++i]); }
    else if (a === '--file') { while (argv[i + 1] && !argv[i + 1].startsWith('--')) o.files.push(argv[++i]); }
    else if (a === '--select') { o.select = argv[++i] || ''; }
    else if (a === '--out-dir') { o.outDir = argv[++i] || null; }
    else if (a === '--manifest') { o.manifest = argv[++i] || null; }
    else if (a === '--password') { o.password = argv[++i] || null; }
    else if (a === '--list') { o.listOnly = true; }
    else if (a === '--json') { o.json = true; o.listOnly = true; }
    else if (!a.startsWith('--')) { o.urls.push(a); }
  }
  return o;
}

function urlsFromText(text) {
  const out = [], seen = new Set();
  for (const m of (text || '').match(URL_RE) || []) {
    const u = m.replace(/[.,;]+$/, '');
    if (!seen.has(u)) { seen.add(u); out.push(u); }
  }
  return out;
}

function buildPairs(o) {
  const pairs = [], seen = new Set();
  const add = (u, pwd) => {
    u = (u || '').trim();
    if (!u || seen.has(u)) return;
    seen.add(u);
    pairs.push([u, pwd || o.password || null]);
  };
  for (const chunk of o.urls) for (const u of urlsFromText(chunk)) add(u);
  for (const f of o.files) {
    if (!fs.existsSync(f)) { log(`⚠ 文件不存在，跳过: ${f}`); continue; }
    if (path.extname(f).toLowerCase() === '.json') {
      let data; try { data = JSON.parse(fs.readFileSync(f, 'utf8')); } catch (e) { continue; }
      const walk = (x) => {
        if (typeof x === 'string') urlsFromText(x).forEach((u) => add(u));
        else if (Array.isArray(x)) x.forEach(walk);
        else if (x && typeof x === 'object') Object.values(x).forEach(walk);
      };
      walk(data); continue;
    }
    let text = '';
    try { text = fs.readFileSync(f, 'utf8'); } catch (e) { log(`⚠ 读取失败 ${f}: ${e.message}`); continue; }
    for (const line of text.split(/\r?\n/)) {
      const us = urlsFromText(line);
      if (!us.length) continue;
      const pm = line.match(PWD_RE);
      const pwd = pm ? pm[1] : null;
      for (const u of us) add(u, pwd);
    }
  }
  return pairs;
}

function probe(url, pwd) {
  const r = spawnSync(process.execPath, [DOWNLOAD_JS, url, '', pwd || '', '--list'],
    { encoding: 'utf8', maxBuffer: 32 * 1024 * 1024, timeout: 180000 });
  const out = (r.stdout || '') + '\n' + (r.stderr || '');
  const idx = out.lastIndexOf(LIST_PREFIX);
  if (idx >= 0) {
    const jsonStr = out.slice(idx + LIST_PREFIX.length).trim();
    try {
      const arr = JSON.parse(jsonStr);
      if (Array.isArray(arr)) return arr.map((it) => ({ name: it.name, folder: !!it.folder, relDir: it.relDir || '' }));
    } catch (e) { /* fallthrough */ }
  }
  const tail = out.trim().split('\n').filter(Boolean).slice(-3).join(' / ');
  return { error: (tail || '解析失败').slice(0, 220) };
}

function buildManifest(pairs) {
  const items = [];
  let idx = 0;
  for (const [url, pwd] of pairs) {
    const res = probe(url, pwd);
    if (Array.isArray(res) && res.length) {
      for (const it of res) {
        idx += 1;
        items.push({ index: idx, url, pwd: pwd || null, title: it.name, folder: it.folder, relDir: it.relDir, status: 'ready', note: it.folder ? '文件夹分享' : '单文件' });
      }
    } else {
      idx += 1;
      items.push({ index: idx, url, pwd: pwd || null, title: '（无法解析）', folder: false, relDir: '', status: 'error', note: (res && res.error) || '解析失败' });
    }
  }
  return items;
}

function renderTable(items) {
  const head = ['#', '类型', '状态', '标题 / 名称', '说明'];
  const rows = items.map((it) => [
    String(it.index),
    it.folder ? '文件夹' : '单文件',
    it.status === 'ready' ? '✓ 可下载' : '✗ 解析失败',
    it.title,
    it.note || '',
  ]);
  const dw = (s) => { let w = 0; for (const c of String(s)) w += c.codePointAt(0) > 0x2e7f ? 2 : 1; return w; };
  const widths = head.map((_, i) => Math.max(dw(head[i]), ...rows.map((r) => dw(r[i]))));
  const pad = (s, w) => s + ' '.repeat(Math.max(0, w - dw(s)));
  const fmt = (r) => r.map((c, i) => pad(c, widths[i])).join('  ');
  const lines = [fmt(head), '-'.repeat(widths.reduce((a, b) => a + b, 0) + 2 * (head.length - 1))];
  for (const r of rows) lines.push(fmt(r));
  return lines.join('\n');
}

function parseSelect(spec) {
  if (!spec) return null;
  spec = String(spec).trim().toLowerCase();
  if (spec === 'all' || spec === '*' || spec === '全部') return 'all';
  const picks = new Set();
  for (let part of spec.split(',')) {
    part = part.trim();
    if (!part) continue;
    const mm = part.match(/^(\d+)\s*-\s*(\d+)$/);
    if (mm) { for (let i = +mm[1]; i <= +mm[2]; i++) picks.add(i); continue; }
    if (/^\d+$/.test(part)) picks.add(+part);
  }
  return picks;
}

function sanitize(s) {
  return String(s).replace(/[\\/:*?"<>|\x00-\x1f]/g, '_').replace(/\s+/g, ' ').trim() || 'file';
}

function withExt(name, ext) {
  if (!ext) return name;
  return name.toLowerCase().endsWith(ext.toLowerCase()) ? name : name + ext;
}

function uniquePath(outDir, name) {
  const ext = path.extname(name);
  const stem = name.slice(0, name.length - ext.length);
  let cand = path.join(outDir, name);
  let i = 2;
  while (fs.existsSync(cand)) { cand = path.join(outDir, `${stem}-${i}${ext}`); i += 1; }
  return cand;
}

function runDownload(item, outDir) {
  log(`\n── [${item.index}] 蓝奏云 | ${item.title}`);
  const ext = path.extname(item.title) || '.zip';
  const base = withExt(sanitize(item.title), ext);
  const out = uniquePath(outDir, base);
  const args = [DOWNLOAD_JS, item.url, out, item.pwd || ''];
  if (item.folder) args.push('--select', item.relDir ? `${item.relDir}/${item.title}` : item.title);
  const r = spawnSync(process.execPath, args, { encoding: 'utf8', maxBuffer: 128 * 1024 * 1024, timeout: 3600000 });
  const outText = (r.stdout || '') + (r.stderr || '');
  const exists = fs.existsSync(out);
  if (r.status === 0 && exists) {
    let sizeInfo = '';
    try {
      const st = fs.statSync(out);
      sizeInfo = st.isDirectory() ? '目录' : `${(st.size / 1048576).toFixed(2)} MB`;
    } catch (e) { /* ignore */ }
    log(`   ✅ 完成: ${path.basename(out)} (${sizeInfo})`);
    return true;
  }
  const tail = outText.trim().split('\n').filter(Boolean).slice(-4).join(' / ');
  log(`   ❌ 失败: ${tail || '未知错误'}`);
  return false;
}

function main() {
  const o = parseArgs(process.argv.slice(2));
  let items;

  if (o.manifest) {
    if (!fs.existsSync(o.manifest)) { log(`⚠ 清单不存在: ${o.manifest}`); process.exit(1); }
    items = JSON.parse(fs.readFileSync(o.manifest, 'utf8'));
    log(`📄 复用清单：${o.manifest}（${items.length} 条）`);
  } else {
    const pairs = buildPairs(o);
    if (!pairs.length) {
      log('用法: node scripts/batch.js --urls "<url1>" "<url2>" | --file links.txt [--select 1,2|all] [--out-dir DIR] [--list|--json]');
      process.exit(1);
    }
    log(`🔎 解析识别 ${pairs.length} 个链接…\n`);
    items = buildManifest(pairs);
  }

  if (o.json) { process.stdout.write(JSON.stringify(items, null, 2) + '\n'); return; }

  process.stdout.write(renderTable(items) + '\n\n');

  const manifestPath = path.resolve(process.cwd(), MANIFEST_NAME);
  fs.writeFileSync(manifestPath, JSON.stringify(items, null, 2));
  log(`💾 清单已保存：${manifestPath}`);

  const sel = parseSelect(o.select);
  if (!sel) {
    log('\n下一步：用 --select 选择要下载的编号，例如：');
    log(`  node scripts/batch.js --manifest ${manifestPath} --select 1,2,3`);
    log('  （或 --select all 下载全部）');
    return;
  }

  const outDir = o.outDir || path.resolve(process.cwd(), 'downloads');
  fs.mkdirSync(outDir, { recursive: true });
  const picks = items.filter((it) => it.status === 'ready' && (sel === 'all' || sel.has(it.index)));
  if (!picks.length) { log('⚠ 没有可下载的选中项（编号无效或均不可下载）'); return; }

  log(`\n⬇️  开始下载 ${picks.length} 项 → ${outDir}`);
  let ok = 0, fail = 0;
  for (const it of picks) { runDownload(it, outDir) ? ok++ : fail++; }
  log(`\n===== 汇总：成功 ${ok} | 失败 ${fail} =====`);
  log(`输出目录：${outDir}`);
}

main();
