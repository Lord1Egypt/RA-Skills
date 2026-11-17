#!/usr/bin/env node
'use strict';

/**
 * 递归列举知识库全部文件目录（含任意层级子文件夹）
 *
 * 用于「打包导出」「全量盘点」「批量处理」等需要先拿到完整文件清单的场景。
 * 输出全部条目的目录树：文件夹(media_type=99) 与 文件(非99)，含路径 / media_id / media_type。
 *
 * 输出：默认紧凑清单，每行 `路径 \t 类型 \t media_id`（文件夹路径以 / 结尾）。
 *
 * 用法:
 *   node list_all_files.cjs --path "我的知识库"                 # 紧凑全量清单
 *   node list_all_files.cjs --path "我的知识库" --summary       # 只出数量与类型分布（最省 token）
 *   node list_all_files.cjs --path "我的知识库" --files-only    # 只列文件，跳过文件夹
 *   node list_all_files.cjs --path "我的知识库" --json          # 紧凑 JSON（单行，程序用）；--pretty 缩进
 *   node list_all_files.cjs --path "我的知识库" --with-url      # 额外逐个 get_media_info 获取下载链接(较慢)
 */

const fs = require('node:fs');
const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveKbId: __resKb, resolvePathStr: __resPath, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, parseArgs, resolveKbId } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

const MEDIA_TYPE_NAME = {
  1: 'PDF', 2: '网页', 3: 'Word', 4: 'PPT', 5: 'Excel', 6: '公众号',
  7: 'Markdown', 9: '图片', 11: '笔记', 12: 'QA', 13: 'TXT', 14: 'Xmind',
  15: '录音', 16: '网页视频', 17: '对话', 18: '视频', 19: '播客', 20: 'HTML', 99: '文件夹',
};

async function listFolder(kbId, folderId, prefix, out, withUrl, depth) {
  if (depth > 20) return;
  let cursor = '';
  let page = 0;
  do {
    const body = { knowledge_base_id: kbId, cursor, limit: 50 };
    if (folderId) body.folder_id = folderId;
    const resp = await call('openapi/wiki/v1/get_knowledge_list', body);
    const items = (resp.data && resp.data.knowledge_list) || [];
    for (const it of items) {
      const p = prefix ? prefix + '/' + it.title : it.title;
      if (it.media_type === 99) {
        out.push({ type: 'folder', title: it.title, media_id: it.media_id, media_type: 99, path: p });
        await listFolder(kbId, it.media_id, p, out, withUrl, depth + 1);
      } else {
        const entry = { type: 'file', title: it.title, media_id: it.media_id, media_type: it.media_type, path: p };
        if (withUrl) {
          try {
            const mi = await call('openapi/wiki/v1/get_media_info', { media_id: it.media_id });
            const ui = (mi.data && mi.data.url_info) || {};
            entry.url = ui.url || '';
            if (!ui.url) entry.url_error = mi.msg || 'no url';
          } catch (e) { entry.url_error = e.message; }
        }
        out.push(entry);
      }
    }
    cursor = (resp.data && resp.data.next_cursor) || '';
    if (resp.data && resp.data.is_end) break;
    if (++page > 50) break; // 单目录上限 2500 条
  } while (cursor);
}

// 紧凑输出：路径 \t 类型 \t media_id（文件夹路径以 / 结尾）。去掉 emoji 与冗余括号以节省 token。
function printTree(out, opts = {}) {
  const filesOnly = !!opts.filesOnly;
  for (const it of out) {
    if (filesOnly && it.type === 'folder') continue;
    const mark = it.type === 'folder' ? '/' : '';
    const mt = MEDIA_TYPE_NAME[it.media_type] || ('type' + it.media_type);
    console.log(`${it.path}${mark}\t${mt}\t${it.media_id}`);
  }
}

async function main() {
  const args = parseArgs(process.argv);
  await __withRetry(args, async () => {
    const kbId = await resolveKbId(args);
    const out = [];
    await listFolder(kbId, null, '', out, !!args['with-url'], 0);
    const files = out.filter(x => x.type === 'file');
    const folders = out.filter(x => x.type === 'folder');
    if (args.json) {
      // 默认紧凑 JSON（单行，省 token）；--pretty 才缩进缩进供人阅读
      console.log(JSON.stringify(out, null, args.pretty ? 2 : 0));
    } else if (args.summary) {
      // 只出统计不列条目（盘点 / 决策场景，最省 token）
      const byType = {};
      for (const f of files) {
        const n = MEDIA_TYPE_NAME[f.media_type] || ('type' + f.media_type);
        byType[n] = (byType[n] || 0) + 1;
      }
      console.log(`文件夹 ${folders.length} 个 · 文件 ${files.length} 个`);
      const dist = Object.entries(byType).map(([k, v]) => `${k}×${v}`).join('  ');
      if (dist) console.log(dist);
    } else {
      printTree(out, { filesOnly: !!args['files-only'] });
      console.log(`\n合计：文件夹 ${folders.length} 个 · 文件 ${files.length} 个`);
    }
  });
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
