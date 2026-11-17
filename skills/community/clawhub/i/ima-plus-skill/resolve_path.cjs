#!/usr/bin/env node
'use strict';

/**
 * resolve_path.cjs — 自然语言路径解析器（ima_plus-skill-1.0.9 统一目录解析入口）
 *
 * 让 AI/用户用自然语言描述知识库与文件夹，脚本内部自动解析为 kb_id / folder_id，
 * 消除对长 kb_id 的记忆与幻觉依赖。
 *
 * 支持的路径格式（第一段=知识库名，后续段=文件夹逐级下钻）：
 *   --path "我的知识库"                      → 仅知识库（根目录）
 *   --path "我的知识库/项目"                  → 知识库 + 一级文件夹
 *   --path "我的知识库/项目/FAM"              → 知识库 + 多级文件夹
 *   --path "项目/FAM"（唯一库时省略库名）      → 自动匹配唯一知识库
 *   --path "FAM"（唯一库且文件夹唯一时）       → 自动匹配
 *
 * 也支持笔记笔记本：
 *   --notes --path "我的笔记本"              → 笔记本 folder_id
 *
 * Usage:
 *   node resolve_path.cjs --path "我的知识库/项目/FAM"
 *   node resolve_path.cjs --notes --path "默认笔记本"
 *   node resolve_path.cjs --kb-name "我的知识库" --folder-name "FAM"   （知识库名+单文件夹名）
 *
 * 输出：{ kb_id, folder_id, kb_name, folder_name, note_folder_id?, note_folder_name? }
 *
 * ─── 分层路径缓存（V1.0.7+）─────────────────────────────────────────────────
 * 解析结果按「知识库名 → 文件夹树」分层持久化到缓存文件，天然防重名串库
 * （同名文件夹在不同知识库/不同父目录下各占一个节点，互不干扰）：
 *
 *   {
 *     "version": 1,
 *     "kbs": {
 *       "我的知识库": {
 *         "kb_id": "Wx...=",
 *         "kb_name": "我的知识库",
 *         "folders": {
 *           "项目": { "folder_id": "folder_xxx", "folders": {
 *             "FAM":  { "folder_id": "folder_yyy", "folders": {} }
 *           } }
 *         }
 *       }
 *     },
 *     "notebooks": {
 *       "默认笔记本": { "folder_id": "note_folder_xxx" }
 *     }
 *   }
 *
 * 设计要点：
 * 1. 无过期时间（TTL）——缓存长期有效，靠「操作失败 → 自愈重查」保证正确性；
 * 2. 缓存优先：命中某层直接用，只对缺失层调 API（部分命中只补缺的层）；
 * 3. 自愈：消费脚本把操作包进 withPathRetry()，操作因「目标不存在」失败时
 *    自动删除该路径缓存 → 全 API 重新解析 → 重试一次；重查任一层失败
 *    即抛「目录位置不存在」，整个操作直接失败，不猜测后续层级；
 * 4. 缓存文件：~/.config/ima/resolve_cache.json（可用环境变量 IMA_RESOLVE_CACHE 覆盖）；
 *    原子写（tmp + rename）防并发损坏，last-write-wins 可接受（丢了大不了重查）。
 */

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { imaApi } = require(path.join(__dirname, 'ima_api.cjs'));

// ─── 分层缓存 ───────────────────────────────────────────────────────────────
const CACHE_ENV = 'IMA_RESOLVE_CACHE';
// 缓存位置确定规则（强制检查）：
//   1) 环境变量 IMA_RESOLVE_CACHE 显式指定 → 用它（所有环境，优先级最高）
//   2) ima.copilot 沙箱（存在 /sandbox/workspace）→ 默认 workspace（持久、平台不重置）
//   3) 其他环境（非 ima.copilot）未设置环境变量 → 明确报错：
//      安装 skill 时必须设置缓存位置，不设置无法使用（与凭证同等强制）
const CACHE_FILE = (function () {
  if (process.env[CACHE_ENV]) return process.env[CACHE_ENV];
  if (fs.existsSync('/sandbox/workspace')) {
    return path.join('/sandbox/workspace', '.ima_cache', 'resolve_cache.json');
  }
  throw new Error(
    '未设置缓存位置环境变量 IMA_RESOLVE_CACHE，技能无法使用。' +
    '非 ima.copilot 环境安装 skill 时必须显式指定缓存保存位置：' +
    'export IMA_RESOLVE_CACHE=/path/to/resolve_cache.json（可写入 ~/.bashrc 或 ~/.zshrc）。'
  );
})();

function emptyCache() {
  return { version: 1, kbs: {}, notebooks: {} };
}

function loadCache() {
  try {
    const raw = fs.readFileSync(CACHE_FILE, 'utf8');
    const c = JSON.parse(raw);
    if (c && typeof c === 'object' && c.kbs && c.notebooks) return c;
  } catch { /* 文件缺失/损坏 → 空缓存 */ }
  return emptyCache();
}

function saveCache(cache) {
  try {
    fs.mkdirSync(path.dirname(CACHE_FILE), { recursive: true });
    const tmp = `${CACHE_FILE}.tmp-${process.pid}`;
    fs.writeFileSync(tmp, JSON.stringify(cache, null, 2), 'utf8');
    fs.renameSync(tmp, CACHE_FILE);
  } catch { /* 缓存写失败不影响主流程 */ }
}

/**
 * 删除某条路径在缓存中的整棵子树（该知识库的所有文件夹缓存一并失效）。
 * 无法定位缓存键（如省略库名场景）时保守全清 kbs，保证重查正确性。
 */
function invalidateCachePath(pathStr, kbName) {
  const cache = loadCache();
  let target = kbName || null;
  if (!target && pathStr) {
    const segs = String(pathStr).split(/[/\\]/).map((s) => s.trim()).filter(Boolean);
    if (segs.length) target = segs[0];
  }
  if (target) {
    const hitKb = cache.kbs[target];
    const hitNb = cache.notebooks[target];
    if (hitKb) delete cache.kbs[target];
    if (hitNb) delete cache.notebooks[target];
    if (!hitKb && !hitNb) {
      cache.kbs = {};
      cache.notebooks = {};
    }
  } else {
    cache.kbs = {};
    cache.notebooks = {};
  }
  saveCache(cache);
}

/** 判断 API 错误是否为「目标不存在」类（缓存 ID 失效的信号）；权限/限流类不算。 */
function isTargetMissing(err) {
  const msg = ((err && (err.msg || err.message)) || '').toLowerCase();
  if (!msg) return false;
  if (/220030|200001|权限|频率|限流/.test(msg)) return false;
  // 目标不存在类：220001 invalid media_id / 222001 知识库已删除 / 310001 文件夹不存在 / invalid / not found / 不存在 / 未找到 / 无效 / 已删除
  return /220001|222001|310001|invalid|not\s*found|no\s*such|不存在|未找到|已删除|无效|is\s*not\s*exist|does\s*not\s*exist/i.test(msg);
}

/**
 * 自愈重试包装器：消费脚本把「解析 + 操作」整体包进来。
 * 操作失败且为「目标不存在」→ 失效该路径缓存 → 重试一次（内部重新全 API 解析）。
 * 重查任一层失败（目录真的不存在）→ 抛错，整个操作直接失败。
 * extraPaths：附加失效路径（如 move 的 --src-path / --dst-path），可为空数组。
 */
async function withPathRetry(args, operationFn, extraPaths = []) {
  const targets = [];
  if (args.path) targets.push(args.path);
  if (args['kb-name']) targets.push({ kbName: args['kb-name'] });
  for (const p of extraPaths || []) if (p) targets.push(p);
  if (!targets.length) return operationFn();
  try {
    return await operationFn();
  } catch (err) {
    if (!isTargetMissing(err)) throw err;
    for (const t of targets) {
      if (typeof t === 'string') invalidateCachePath(t);
      else invalidateCachePath(null, t.kbName);
    }
    return await operationFn(); // 重试一次；再失败原样抛出
  }
}

// ─── 工具函数 ───────────────────────────────────────────────────────────────
async function call(apiPath, body) {
  const raw = await imaApi(apiPath, body);
  let json;
  try {
    json = JSON.parse(raw);
  } catch {
    throw new Error(`接口 ${apiPath} 返回非 JSON：${raw}`);
  }
  if (json.code !== 0) {
    throw new Error(`接口 ${apiPath} 失败 (code=${json.code}): ${json.msg || ''}`);
  }
  return json;
}

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const tok = argv[i];
    if (!tok.startsWith('--')) continue;
    const key = tok.replace(/^--/, '');
    const next = argv[i + 1];
    if (next && !next.startsWith('--')) {
      args[key] = next;
      i++;
    } else {
      args[key] = true;
    }
  }
  return args;
}

// ─── 知识库名 → kb_id（带缓存） ─────────────────────────────────────────────
async function resolveKbIdByName(kbName, cache) {
  // 0) 缓存优先：同名库已解析过 → 0 次 API 调用
  const cacheRef = cache || loadCache();
  const cachedKb = cacheRef.kbs[kbName];
  if (cachedKb && cachedKb.kb_id) {
    return { kb_id: cachedKb.kb_id, kb_name: cachedKb.kb_name || kbName, from_cache: true };
  }
  // 1) 关键词搜索（可能对新库/未索引库返回空）
  let list = [];
  try {
    const resp = await call('openapi/wiki/v1/search_knowledge_base', {
      query: kbName,
      cursor: '',
      limit: 20,
    });
    list = (resp.data && resp.data.info_list) || [];
  } catch (e) { /* 搜索失败则走全量回退 */ }
  let hit =
    list.find((k) => k.kb_name === kbName) ||
    list.find((k) => (k.kb_name || '').includes(kbName));
  // 2) 回退：空 query 拉全量再匹配（关键词搜索对新库不可靠，实测踩过）
  if (!hit) {
    const resp2 = await call('openapi/wiki/v1/search_knowledge_base', {
      query: '',
      cursor: '',
      limit: 20,
    });
    const all = (resp2.data && resp2.data.info_list) || [];
    hit =
      all.find((k) => k.kb_name === kbName) ||
      all.find((k) => (k.kb_name || '').includes(kbName));
    if (!hit) {
      const names = all.map((k) => k.kb_name).join('、');
      throw new Error(`未找到名称包含「${kbName}」的知识库。当前知识库：${names || '(无)'}`);
    }
  }
  // 3) 写缓存
  if (!cacheRef.kbs[kbName]) cacheRef.kbs[kbName] = { kb_id: hit.kb_id, kb_name: hit.kb_name, folders: {} };
  else {
    cacheRef.kbs[kbName].kb_id = hit.kb_id;
    cacheRef.kbs[kbName].kb_name = hit.kb_name;
    cacheRef.kbs[kbName].folders = cacheRef.kbs[kbName].folders || {};
  }
  if (!cache) saveCache(cacheRef);
  return { kb_id: hit.kb_id, kb_name: hit.kb_name };
}

// 知识库 ID：优先 --path 第一段 / --kb / --kb-name（带缓存）
async function resolveKbId(args, { kbNameFromPath } = {}) {
  if (args.kb) return { kb_id: args.kb, kb_name: '(按ID指定)' };
  const name = kbNameFromPath || args['kb-name'];
  if (!name) {
    // 未指定名称：尝试唯一知识库（只有一个时自动采用；该结果不缓存，库数量可能变化）
    const resp = await call('openapi/wiki/v1/search_knowledge_base', { query: '', cursor: '', limit: 20 });
    const list = (resp.data && resp.data.info_list) || [];
    if (list.length === 1) {
      return { kb_id: list[0].kb_id, kb_name: list[0].kb_name, auto: true };
    }
    throw new Error(
      `无法确定目标知识库：请用 --path "知识库名/文件夹..." 或 --kb-name <名称> 指定。当前有 ${list.length} 个知识库。`
    );
  }
  const hit = await resolveKbIdByName(name);
  return { kb_id: hit.kb_id, kb_name: hit.kb_name };
}

// ─── 文件夹路径 → folder_id（逐级下钻，带缓存） ────────────────────────────
// kbCacheKey：缓存树中该知识库的键（通常=用户输入的库名或真实库名）
async function resolveFolderIdByPath(kbId, segments, cache, kbCacheKey) {
  const cacheRef = cache || loadCache();
  let changed = false;
  let folderId = '';
  let folderName = '';
  let parent = '';
  let node = kbCacheKey ? cacheRef.kbs[kbCacheKey] : null; // 缓存节点，逐级下钻
  for (let i = 0; i < segments.length; i++) {
    const seg = String(segments[i]).trim();
    if (!seg) continue;
    // 缓存优先：该层已解析过 → 0 次 API 调用
    const cachedFolder = node && node.folders && node.folders[seg];
    if (kbCacheKey && cachedFolder && cachedFolder.folder_id) {
      folderId = cachedFolder.folder_id;
      folderName = seg;
      parent = folderId;
      node = cachedFolder;
      continue;
    }
    // 缓存 miss → API 查当前层
    const body = { knowledge_base_id: kbId, cursor: '', limit: 50 };
    if (parent) body.folder_id = parent;
    const resp = await call('openapi/wiki/v1/get_knowledge_list', body);
    const list = (resp.data && resp.data.knowledge_list) || [];
    const folders = list.filter((it) => it.media_type === 99); // 99 = 文件夹
    const hit =
      folders.find((f) => f.title === seg) ||
      folders.find((f) => (f.title || '').includes(seg));
    if (!hit) {
      const names = folders.map((f) => f.title).join('、');
      throw new Error(
        `在「${folderName || '根目录'}」下未找到文件夹「${seg}」。当前文件夹：${names || '(无)'}`
      );
    }
    folderId = hit.media_id;
    folderName = hit.title;
    parent = folderId;
    // 写缓存（确保节点挂在树上，--kb-name 首次解析时树节点可能不存在）
    if (kbCacheKey) {
      if (!cacheRef.kbs[kbCacheKey]) {
        cacheRef.kbs[kbCacheKey] = { kb_id: kbId, kb_name: kbCacheKey, folders: {} };
      }
      node = node || cacheRef.kbs[kbCacheKey];
      node.folders = node.folders || {};
      node.folders[seg] = { folder_id: folderId, folders: {} };
      node = node.folders[seg];
      changed = true;
    }
  }
  if (kbCacheKey && changed && !cache) saveCache(cacheRef);
  return { folder_id: folderId, folder_name: folderName, changed };
}

// ─── 完整路径解析（自然语言，缓存优先） ─────────────────────────────────────
async function resolvePathStr(pathStr, { notes = false } = {}) {
  if (notes) return resolveNotePathStr(pathStr);
  const segs = String(pathStr || '')
    .split(/[/\\]/)
    .map((s) => s.trim())
    .filter(Boolean);
  if (segs.length === 0) throw new Error('路径为空');

  const cache = loadCache();

  // 第一段：知识库层（缓存优先；匹配失败回退到唯一库自动识别，该结果不缓存）
  let kb, folderSegs, kbCacheKey = null;
  let dirty = false; // 缓存是否有实际变更（有变更才落盘，全命中不写文件）
  const cachedKb = cache.kbs[segs[0]];
  if (cachedKb && cachedKb.kb_id) {
    kb = { kb_id: cachedKb.kb_id, kb_name: cachedKb.kb_name || segs[0], from_cache: true };
    kbCacheKey = segs[0];
    folderSegs = segs.slice(1);
  } else {
    try {
      kb = await resolveKbId({ 'kb-name': segs[0] }, { kbNameFromPath: segs[0] });
      kbCacheKey = segs[0];
      folderSegs = segs.slice(1);
      const existing = cache.kbs[segs[0]] || {};
      cache.kbs[segs[0]] = { kb_id: kb.kb_id, kb_name: kb.kb_name, folders: existing.folders || {} };
      dirty = true;
    } catch (e) {
      // 第一段不是知识库名 → 若账号唯一知识库则自动采用，全部段视为文件夹路径
      const kb2 = await resolveKbId({});
      kb = kb2;
      kbCacheKey = kb2.kb_name; // 缓存挂在真实库名下
      folderSegs = segs;
      if (kbCacheKey) {
        const existing = cache.kbs[kbCacheKey] || {};
        cache.kbs[kbCacheKey] = { kb_id: kb2.kb_id, kb_name: kb2.kb_name, folders: existing.folders || {} };
        dirty = true;
      }
    }
  }

  const folder = folderSegs.length
    ? await resolveFolderIdByPath(kb.kb_id, folderSegs, cache, kbCacheKey)
    : { folder_id: '', folder_name: '', changed: false };
  // 只有实际变更才落盘（全命中 = 0 次 API + 0 次磁盘写）
  if (dirty || folder.changed) saveCache(cache);
  return {
    kb_id: kb.kb_id,
    kb_name: kb.kb_name,
    folder_id: folder.folder_id,
    folder_name: folder.folder_name,
    auto_kb: !!kb.auto,
  };
}

// ─── 笔记本名 → 笔记本 folder_id（带缓存） ───────────────────────────────────
async function resolveNotePathStr(pathStr) {
  const name = String(pathStr || '').trim();
  if (!name) throw new Error('笔记本名称不能为空');
  const cache = loadCache();
  const cached = cache.notebooks[name];
  if (cached && cached.folder_id) {
    return { note_folder_id: cached.folder_id, note_folder_name: name, from_cache: true };
  }
  const resp = await call('openapi/note/v1/list_notebook', { cursor: '0', limit: 20 });
  const list = (resp.data && resp.data.note_folder_infos) || [];
  const hit =
    list.find((n) => n.name === name || n.folder_name === name) ||
    list.find((n) => ((n.name || n.folder_name) || '').includes(name));
  if (!hit) {
    const names = list.map((n) => n.name || n.folder_name).join('、');
    throw new Error(`未找到笔记本「${name}」。当前笔记本：${names || '(无)'}`);
  }
  const hitName = hit.name || hit.folder_name;
  cache.notebooks[name] = { folder_id: hit.folder_id, folder_name: hitName };
  saveCache(cache);
  return { note_folder_id: hit.folder_id, note_folder_name: hitName };
}

// ─── CLI 入口 ───────────────────────────────────────────────────────────────
async function main() {
  const args = parseArgs(process.argv);
  if (!args.path && !args['kb-name']) {
    console.error('[error] 缺少参数：--path "知识库名/文件夹..." 或 --kb-name <知识库名> [--folder-name <文件夹名>]');
    process.exit(1);
  }
  let result;
  if (args.path) {
    result = await resolvePathStr(args.path, { notes: !!args.notes });
  } else {
    const { kb_id, kb_name } = await resolveKbId(args);
    let folder_id = '', folder_name = '';
    if (args['folder-name']) {
      const f = await resolveFolderIdByPath(kb_id, [args['folder-name']], null, args['kb-name'] || kb_name);
      folder_id = f.folder_id;
      folder_name = f.folder_name;
    }
    result = { kb_id, kb_name, folder_id, folder_name };
  }
  console.log(JSON.stringify(result, null, 2));
}

// 模块导出（供其他脚本 require）
module.exports = {
  call,
  parseArgs,
  resolveKbId,
  resolveKbIdByName,
  resolveFolderIdByPath,
  resolvePathStr,
  resolveNotePathStr,
  withPathRetry,
  isTargetMissing,
  loadCache,
  saveCache,
  invalidateCachePath,
  CACHE_FILE,
};

if (require.main === module) {
  main().catch((err) => {
    console.error(`[error] ${err.message}`);
    process.exit(1);
  });
}
