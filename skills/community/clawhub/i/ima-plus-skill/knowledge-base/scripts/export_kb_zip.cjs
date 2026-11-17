#!/usr/bin/env node
'use strict';

/**
 * 知识库打包导出为 zip（IMA.plus 知识库模块附属功能）
 *
 * 支持三种范围：
 *   1. 整个知识库：            --path "我的知识库"  |  --kb-name <知识库名称>
 *   2. 指定文件夹（递归子内容）： 在上述基础上 + --folder-id <folder_id>
 *   3. 指定多个文件：           + --media-ids <id1,id2,id3>
 *
 * 行为：
 *   - 递归收集文件清单，按知识库原始目录结构落盘（保留文件夹层级）
 *   - 同名文件自动加序号（_1 / _2 …）避免互相覆盖
 *   - 逐个调用 export_media_for_ima_sandbox 导出并带 headers 下载
 *   - 全部下载完成后整体打包成 zip（UTF-8 文件名）
 *   - 导出失败的文件如实报告，不影响其余文件；全部失败则不生成 zip
 *
 * 凭证（与 ima_api.cjs 一致）：单一来源 = 环境变量 IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY，
 *   强制设置，不设置即报错（无 config.json / ~/.config/ima/ 降级）。
 *   凭证获取：在 ima app 的 copilot 对话索要环境变量 IMA_OPENAPI_CLIENTID/APIKEY 的凭证，
 *   在自建环境 export（可写入 ~/.bashrc 或 ~/.zshrc；完整 SOP 见 SKILL.md「Credential Check」）。
 *   注意：个人在 agent-interface 申请的 key 未开通导出权限（导出报 220030），
 *   ima.copilot 环境已自动注入已开通导出的凭证，直接可用。
 *
 * Usage:
 *   node export_kb_zip.cjs --kb-name "我的知识库"
 *   node export_kb_zip.cjs --path "我的知识库/目标文件夹"
 *   node export_kb_zip.cjs --path "我的知识库" --media-ids id1,id2
 *   node export_kb_zip.cjs --kb-name "我的知识库" --dry-run        # 只列清单不下载
 *   node export_kb_zip.cjs --kb-name "我的知识库" --estimate       # 统计+调用量预估
 *   node export_kb_zip.cjs --path "我的知识库" --count             # 轻量统计(JSON，AI友好)
 *   node export_kb_zip.cjs --kb-name "我的知识库" --out /path/x.zip --keep
 */

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const zlib = require('node:zlib');
const { resolveKbId: __resKb, resolvePathStr: __resPath, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { parseArgs, resolveKbId } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

const BASE = 'https://ima.qq.com';

// ─── 纯 Node zip 打包（跨平台，不依赖系统 zip 命令）───────────────
// Windows 没有 zip 命令；PowerShell Compress-Archive 对中文/UTF-8 文件名支持差。
// 此处用 zlib deflate + 手写 zip 结构（Local File Header + Central Directory + EOCD），
// 文件名 UTF-8 编码 + UTF-8 flag，Windows / Linux / macOS 行为完全一致。
const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
    t[n] = c >>> 0;
  }
  return t;
})();

function crc32(buf) {
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

// 递归打包 dirPath 下全部文件到 outPath（保留相对目录结构，UTF-8 文件名）
function zipDirectory(dirPath, outPath) {
  const files = [];
  (function walk(dir, prefix) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (entry.isDirectory()) walk(full, rel);
      else if (entry.isFile()) files.push({ full, rel });
    }
  })(dirPath, '');

  const central = [];
  const fd = fs.openSync(outPath, 'w');
  let offset = 0;
  try {
    for (const f of files) {
      const data = fs.readFileSync(f.full);
      const nameBuf = Buffer.from(f.rel, 'utf8');
      const crc = crc32(data);
      const comp = zlib.deflateRawSync(data, { level: 6 });

      // Local File Header
      const lfh = Buffer.alloc(30);
      lfh.writeUInt32LE(0x04034b50, 0);  // signature
      lfh.writeUInt16LE(20, 4);          // version needed
      lfh.writeUInt16LE(0x0800, 6);      // general purpose flag: UTF-8
      lfh.writeUInt16LE(8, 8);           // compression: deflate
      lfh.writeUInt32LE(crc, 14);
      lfh.writeUInt32LE(comp.length, 18);
      lfh.writeUInt32LE(data.length, 22);
      lfh.writeUInt16LE(nameBuf.length, 26);
      lfh.writeUInt16LE(0, 28);          // extra len
      fs.writeSync(fd, lfh);
      fs.writeSync(fd, nameBuf);
      fs.writeSync(fd, comp);

      // Central Directory entry
      const cd = Buffer.alloc(46);
      cd.writeUInt32LE(0x02014b50, 0);   // signature
      cd.writeUInt16LE(20, 4);           // version made by
      cd.writeUInt16LE(20, 6);           // version needed
      cd.writeUInt16LE(0x0800, 8);       // flag: UTF-8
      cd.writeUInt16LE(8, 10);           // method: deflate
      cd.writeUInt32LE(crc, 16);
      cd.writeUInt32LE(comp.length, 20);
      cd.writeUInt32LE(data.length, 24);
      cd.writeUInt16LE(nameBuf.length, 28);
      cd.writeUInt32LE(offset, 42);      // local header offset
      central.push(cd, nameBuf);
      offset += lfh.length + nameBuf.length + comp.length;
    }

    const cdBuf = Buffer.concat(central);
    const eocd = Buffer.alloc(22);
    eocd.writeUInt32LE(0x06054b50, 0);   // signature
    eocd.writeUInt16LE(files.length, 8);
    eocd.writeUInt16LE(files.length, 10);
    eocd.writeUInt32LE(cdBuf.length, 12);
    eocd.writeUInt32LE(offset, 16);
    fs.writeSync(fd, cdBuf);
    fs.writeSync(fd, eocd);
  } finally {
    fs.closeSync(fd);
  }
  return files.length;
}

// 凭证单一来源：环境变量（强制，与 ima_api.cjs 一致）
function loadCreds() {
  const clientId =
    process.env.IMA_OPENAPI_CLIENTID || process.env.IMA_CLIENT_ID;
  const apiKey =
    process.env.IMA_OPENAPI_APIKEY || process.env.IMA_API_KEY;
  if (!clientId || !apiKey) {
    throw new Error(
      '未设置凭证环境变量 IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY，技能无法使用。' +
      'ima.copilot 环境已自动注入；自建环境请 export（可写入 ~/.bashrc 或 ~/.zshrc）。'
    );
  }
  return { clientId, apiKey };
}

async function imaPost(apiPath, body, creds) {
  const res = await fetch(`${BASE}/${apiPath}`, {
    method: 'POST',
    headers: {
      'ima-openapi-clientid': creds.clientId,
      'ima-openapi-apikey': creds.apiKey,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  const text = await res.text();
  let json;
  try { json = JSON.parse(text); } catch { throw new Error(`接口 ${apiPath} 返回非 JSON：${text}`); }
  return json;
}

async function call(apiPath, body, creds) {
  const json = await imaPost(apiPath, body, creds);
  if (json.code !== 0) throw new Error(`接口 ${apiPath} 失败 (code=${json.code}): ${json.msg || ''}`);
  return json;
}

// 文件名净化：防止知识库条目标题携带目录分隔符 / ".." 导致落盘路径遍历（V1.0.11 加固）。
// 只作用于本地落盘路径，不影响 API 调用与 dry-run 清单中的 media_id。
function safeName(name) {
  const cleaned = String(name == null ? '' : name)
    .replace(/[\\/]/g, '_')                     // 目录分隔符
    .replace(/\.\./g, '_')                      // 上级目录
    .replace(/[\u0000-\u001f]/g, '')            // 控制字符
    .trim();
  return cleaned || 'unnamed';
}

// API 频率限制（实测 2026-08-16）：50 次/分钟触发 code=200001，约 40-45s 恢复
const RATE_LIMIT_PER_MIN = 50;
const RATE_RECOVER_MS = 45000;

async function listFolder(kbId, folderId, prefix, out, stats, creds, depth) {
  if (depth > 20) return;
  let cursor = '';
  let page = 0;
  do {
    const body = { knowledge_base_id: kbId, cursor, limit: 50 };
    if (folderId) body.folder_id = folderId;
    const resp = await call('openapi/wiki/v1/get_knowledge_list', body, creds);
    const items = (resp.data && resp.data.knowledge_list) || [];
    for (const it of items) {
      const seg = safeName(it.title);
      const p = prefix ? prefix + '/' + seg : seg;
      if (it.media_type === 99) {
        stats.folders += 1; // 每个文件夹 = 1 次 get_knowledge_list
        await listFolder(kbId, it.media_id, p, out, stats, creds, depth + 1);
      } else {
        stats.files += 1; // 每个文件 = 1 次 export_media
        out.push({ title: it.title, media_id: it.media_id, media_type: it.media_type, path: p });
      }
    }
    cursor = (resp.data && resp.data.next_cursor) || '';
    if (resp.data && resp.data.is_end) break;
    if (++page > 50) break; // 单目录上限 2500 条
  } while (cursor);
}

// 预估 API 调用次数：目录遍历(get_knowledge_list) + 下载(export_media)
function estimateApiCalls(stats) {
  return stats.folders + stats.files; // 遍历调用≈文件夹数（含根），下载=文件数
}

async function main() {
  const args = parseArgs(process.argv);
  await __withRetry(args, async () => {
  const creds = loadCreds();
  let kbId, folderId = args['folder-id'] || null;
  if (args.path) {
    const r = await resolveKbId(args, { needFolder: true });
    kbId = r.kb_id;
    if (r.folder_id && !folderId) folderId = r.folder_id;
  } else {
    kbId = await resolveKbId(args, creds);
  }

  // 1. 收集文件清单（从根或指定文件夹递归）+ 统计
  let files = [];
  const stats = { folders: 0, files: 0 };
  await listFolder(kbId, folderId, '', files, stats, creds, 0);

  // 2. 若指定了文件清单，则按 media_id 筛选（保留其在目录树中的路径）
  if (args['media-ids']) {
    const ids = String(args['media-ids']).split(',').map(s => s.trim()).filter(Boolean);
    const byId = new Map(files.map(f => [f.media_id, f]));
    files = ids.map(id => byId.get(id) || { title: id, media_id: id, media_type: 0, path: id });
    stats.files = files.length;
    stats.folders = 0; // 指定文件清单时不再遍历目录
  }

  // 调用量预估：遍历(≈文件夹数) + 下载(=文件数)
  const estCalls = estimateApiCalls(stats);
  const estFolders = stats.folders + 1; // +根目录
  const overLimit = estCalls > RATE_LIMIT_PER_MIN;
  const summary = {
    folders: stats.folders,
    files: stats.files,
    api_calls_estimate: estCalls,
    api_calls_breakdown: { listing: estFolders, download: stats.files },
    rate_limit_per_min: RATE_LIMIT_PER_MIN,
    over_limit: overLimit,
    note: overLimit
      ? `预估 ${estCalls} 次 > ${RATE_LIMIT_PER_MIN} 次/分钟，将自动限速（约 ${Math.ceil(estCalls / RATE_LIMIT_PER_MIN)} 分钟跑完）`
      : `预估 ${estCalls} 次 ≤ ${RATE_LIMIT_PER_MIN}，一次可跑完`,
  };

  // --count：轻量统计模式（结构化 JSON，AI 打包前快速判断）
  if (args.count) {
    console.log(JSON.stringify(summary, null, 2));
    return;
  }

  if (args['dry-run'] || args['estimate']) {
    console.log(`[dry-run] 目标目录结构：`);
    console.log(`  文件夹 ${stats.folders} 个，文件 ${stats.files} 个`);
    console.log(`  📊 预估 API 调用：${estCalls} 次（目录遍历≈${estFolders} 次 + 下载 ${stats.files} 次）`);
    console.log(`  ⏱  频率限制：${RATE_LIMIT_PER_MIN} 次/分钟（实测 ${RATE_RECOVER_MS / 1000}s 恢复）`);
    if (overLimit) {
      console.log(`  ⚠️  预估调用 ${estCalls} 次 > ${RATE_LIMIT_PER_MIN} 次/分钟阈值，将自动限速（每 ${Math.ceil(estCalls / RATE_LIMIT_PER_MIN)} 分钟跑完）`);
    } else {
      console.log(`  ✅ 预估 ${estCalls} 次 ≤ ${RATE_LIMIT_PER_MIN}，一次可跑完`);
    }
    if (args['dry-run']) {
      console.log(`  将导出 ${files.length} 个文件：`);
      for (const f of files) console.log(`  ${f.path}  (${f.media_id})`);
    }
    return;
  }

  // 正常打包：默认显示统计（一眼看清规模与是否限速）
  console.log(`📊 ${stats.files} 个文件 / ${stats.folders} 个子文件夹 · 预估调用 ${estCalls} 次` + (overLimit ? ` · ⚠️ 超限将自动限速` : ` · ✅ 阈值内`));
  if (!files.length) { console.log('没有可导出的文件。'); return; }

  // 下载阶段：限速保护（每 10 次暂停 1s）+ 自动重试 200001
  let calls = 0;
  const throttle = async () => {
    calls += 1;
    if (calls % 10 === 0 && overLimit) {
      const pause = 1000;
      process.stdout.write(`    ⏸ 限速暂停 ${pause / 1000}s（已 ${calls} 次调用）…\n`);
      await new Promise(r => setTimeout(r, pause));
    }
  };
  const callWithRetry = async (apiPath, body) => {
    for (let attempt = 1; attempt <= 3; attempt++) {
      await throttle();
      try {
        return await call(apiPath, body, creds);
      } catch (e) {
        if (String(e.message).includes('200001') && attempt < 3) {
          process.stdout.write(`    ⏳ 触发限流，等待 ${RATE_RECOVER_MS / 1000}s 重试…\n`);
          await new Promise(r => setTimeout(r, RATE_RECOVER_MS));
          continue;
        }
        throw e;
      }
    }
    throw new Error('重试 3 次仍失败');
  };

  // 3. 逐个导出下载到临时目录（保留目录结构，重名加序号）
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'kb-export-'));
  const used = {};
  let ok = 0;
  const fail = [];
  for (const f of files) {
    let rel = f.path;
    if (rel in used) {
      used[rel] += 1;
      const d = path.dirname(rel);
      const base = path.basename(rel);
      const dot = base.lastIndexOf('.');
      const stem = dot > 0 ? base.slice(0, dot) : base;
      const ext = dot > 0 ? base.slice(dot) : '';
      rel = path.join(d, `${stem}_${used[rel]}${ext}`);
    } else {
      used[rel] = 0;
    }
    try {
      process.stdout.write(`  [${String(ok + fail.length + 1).padStart(String(files.length).length)}/${files.length}] ${f.path} …`);
      const resp = await callWithRetry('openapi/wiki/v1/export_media_for_ima_sandbox', { media_id: f.media_id });
      const info = (resp.data && resp.data.media_content_url_info) || {};
      const url = info.url;
      const headers = info.headers || {};
      if (!url) throw new Error('无下载链接（该类型可能不支持导出）');
      const target = path.join(tmp, rel);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      const hdr = {};
      for (const [k, v] of Object.entries(headers)) hdr[k] = v;
      const r = await fetch(url, { headers: hdr });
      if (!r.ok) throw new Error(`下载 HTTP ${r.status}`);
      const buf = Buffer.from(await r.arrayBuffer());
      fs.writeFileSync(target, buf);
      ok++;
      process.stdout.write(` OK (${(buf.length / 1024).toFixed(0)}KB)\n`);
      // 默认不再重复打印第二条明细；--verbose 才输出带精确字节数的行
      if (args.verbose) console.log(`  OK   ${rel}  (${buf.length} bytes)`);
    } catch (e) {
      fail.push({ path: rel, media_id: f.media_id, err: e.message });
      console.log(`  FAIL ${rel}: ${e.message}`);
    }
  }

  if (ok === 0) {
    console.error(`\n[error] 全部 ${files.length} 个文件导出失败，未生成 zip。`);
    fs.rmSync(tmp, { recursive: true, force: true });
    process.exit(1);
  }

  // 4. 打包成 zip（纯 Node 实现，跨平台，不依赖系统 zip）
  const out = args.out || path.join('/sandbox/workspace/outputs', `知识库导出_${Date.now()}.zip`);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  const packed = zipDirectory(tmp, out);
  const size = fs.statSync(out).size;
  if (packed !== files.length) throw new Error(`zip 内文件数(${packed})与清单(${files.length})不一致`);

  console.log(`\n=== 完成 ===`);
  console.log(`导出成功: ${ok}/${files.length}`);
  if (fail.length) console.log(`失败: ${fail.length}（见上方 FAIL 列表，常见为网页/公众号类不支持导出）`);
  console.log(`zip 路径: ${out}  (${size} bytes)`);
  if (!args.keep) fs.rmSync(tmp, { recursive: true, force: true });
  });
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
