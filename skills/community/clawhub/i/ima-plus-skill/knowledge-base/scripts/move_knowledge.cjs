#!/usr/bin/env node
'use strict';

/**
 * 移动文件到其他知识库/文件夹（封装 openapi/wiki/v1/move_knowledge）
 * 注意：不支持文件夹的移动，只能移动文件。
 *
 * Usage:
 *   node move_knowledge.cjs --src-path "我的知识库A" --dst-path "我的知识库B" --media-id <media_id>
 *   node move_knowledge.cjs --src-path "我的知识库A/文件夹" --dst-path "我的知识库B/目标文件夹" --media-id id1,id2,id3
 *   node move_knowledge.cjs --src-kb-name "源库" --dst-kb-name "目标库" --media-id <media_id>
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolvePathStr: __resPath, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, log, parseArgs } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

// 解析知识库 ID：支持 --<flag> / --<flag>-name / --<flag>-path / --<flag-prefix>-path（自然语言路径）
async function resolveKbId(flag, args, label) {
  const direct = args[flag];
  if (direct) return direct;
  // 兼容两种路径参数：--src-path / --src-kb-path（flag 去 -kb 后缀）
  const shortFlag = flag.replace(/-kb$/, '');
  const pathVal = args[`${flag}-path`] || args[`${shortFlag}-path`];
  if (pathVal) {
    const r = await __resPath(pathVal);
    log('🔎', `按路径匹配到${label}知识库：${r.kb_name}${r.folder_name ? '/' + r.folder_name : ''}`);
    return r.kb_id;
  }
  const nameVal = args[`${flag}-name`] || args[`${shortFlag}-name`];
  if (nameVal) {
    const resp = await call('openapi/wiki/v1/search_knowledge_base', {
      query: nameVal,
      cursor: '',
      limit: 20,
    });
    const list = (resp.data && resp.data.info_list) || [];
    const hit =
      list.find((k) => k.kb_name === nameVal) ||
      list.find((k) => (k.kb_name || '').includes(nameVal));
    if (!hit) throw new Error(`未找到名称包含「${nameVal}」的知识库`);
    log('🔎', `按名称匹配到${label}知识库：${hit.kb_name}`);
    return hit.kb_id;
  }
  throw new Error(
    `必须显式指定${label}知识库：用 --${flag} <id>、--${flag}-name <名称> 或 --${flag}-path <自然语言路径> 传入。`
  );
}

async function main() {
  const args = parseArgs(process.argv);
  // 自愈需覆盖源/目标两个自然语言路径
  const srcPath = args['src-path'] || args['src-kb-path'];
  const dstPath = args['dst-path'] || args['dst-kb-path'];
  await __withRetry(args, async () => {
    if (!args['media-id']) {
      console.error('[error] 缺少必需参数 --media-id <media_id>（多个用逗号分隔）');
      process.exit(1);
    }
    const mediaIds = String(args['media-id'])
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);
    if (mediaIds.length === 0) {
      console.error('[error] --media-id 为空');
      process.exit(1);
    }

    log('⏳', '定位源/目标知识库…');
    const srcKb = await resolveKbId('src-kb', args, '源');
    const dstKb = await resolveKbId('dst-kb', args, '目标');

    const body = {
      src_knowledge_base_id: srcKb,
      dst_knowledge_base_id: dstKb,
      infos: mediaIds.map((id) => ({ media_id: id })),
    };
    // 目标文件夹：优先 --dst-folder；--dst-path/--dst-kb-path 时取路径解析的 folder_id
    const dstPathVal = args['dst-path'] || args['dst-kb-path'];
    if (dstPathVal && !args['dst-folder']) {
      const r = await __resPath(dstPathVal);
      if (r.folder_id) body.dst_folder_id = r.folder_id;
    } else if (args['dst-folder']) {
      body.dst_folder_id = args['dst-folder'];
    }

    log('⏳', `移动 ${mediaIds.length} 个文件：${srcKb} → ${dstKb}…`);
    const resp = await call('openapi/wiki/v1/move_knowledge', body);
    const results = (resp.data && resp.data.move_results) || {};
    log('✅', '移动完成，逐文件结果：');
    console.log(JSON.stringify(results, null, 2));
  }, [srcPath, dstPath]);
}

main().catch((err) => {
  console.error(`[error] ${err.message}`);
  process.exit(1);
});
