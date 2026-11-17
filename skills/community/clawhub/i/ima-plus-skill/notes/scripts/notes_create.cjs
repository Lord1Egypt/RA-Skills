#!/usr/bin/env node
'use strict';

/**
 * notes_create.cjs — 新建笔记（封装 openapi/note/v1/import_doc）
 *
 * 让 AI/用户用自然语言操作，不用手拼 JSON：
 *   --content <markdown> 或 --file <path> 二选一（--file 优先）
 *   --path <笔记本名>  可选，自动解析笔记本 folder_id（带缓存）；省略则建到默认位置
 *   --format <0|1>     可选，默认 1（MARKDOWN），0=纯文本
 *
 * Usage:
 *   node notes_create.cjs --content "# 标题\n\n正文内容"
 *   node notes_create.cjs --content "学习笔记" --path "测试笔记本"
 *   node notes_create.cjs --file /tmp/note.md --path "测试笔记本"
 *
 * 自动处理：UTF-8 校验（非法字节直接中止，防止永久乱码）；过滤本地图片引用
 * （import_doc 不支持 file:// 本地图片，只保留 http(s) 网络图片）。
 */

const fs = require('node:fs');
const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveNotePathStr, withPathRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, log, parseArgs } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

// 严格 UTF-8 校验：读文件内容，非法字节直接报错（防止永久乱码）
function readContentFile(filePath) {
  const buf = fs.readFileSync(filePath);
  try {
    return new TextDecoder('utf-8', { fatal: true }).decode(buf);
  } catch {
    throw new Error(`文件 ${filePath} 不是合法 UTF-8，已中止写入（防止笔记永久乱码）`);
  }
}

// 过滤本地图片（import_doc 不支持 file:// 本地图片），保留网络图片
function filterLocalImages(content) {
  const RE = /!\[[^\]]*\]\(([^)]+)\)/g;
  const removed = [];
  const out = content.replace(RE, (m, url) => {
    if (/^https?:\/\//i.test(url.trim())) return m;
    removed.push(url.trim());
    return '';
  });
  return { content: out, removed };
}

async function main() {
  const args = parseArgs(process.argv);
  const content = args.file ? readContentFile(args.file) : (args.content || '');
  if (!content.trim()) { console.error('[error] 缺少内容：--content <markdown> 或 --file <path>'); process.exit(1); }

  const format = args.format !== undefined ? Number(args.format) : 1;
  if (![0, 1].includes(format)) { console.error('[error] --format 只能是 0（纯文本）或 1（Markdown）'); process.exit(1); }

  const { content: clean, removed } = filterLocalImages(content);
  if (removed.length) log('⚠️', `已过滤本地图片引用（直接调 import_doc 不支持本地图片）：${removed.join('、')}。如需插入本地图片，请改用 notes/scripts/note-images.cjs --note-id <id> --file <md>`);

  const body = { content_format: format, content: clean };
  if (args.path) {
    await withPathRetry(args, async () => {
      const nb = await resolveNotePathStr(args.path); // 带缓存解析笔记本
      body.folder_id = nb.note_folder_id;
      log('🔎', `笔记本：${nb.note_folder_name}`);
    });
  }

  if (args['dry-run']) {
    console.log('[dry-run] 请求体预览（未调用 API）：');
    console.log(JSON.stringify(body, null, 2));
    return;
  }

  log('⏳', '创建笔记…');
  const resp = await withPathRetry(args, async () => await call('openapi/note/v1/import_doc', body));
  const noteId = (resp.data && resp.data.note_id) || '';
  log('🎉', `笔记创建成功：note_id=${noteId}`);
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
