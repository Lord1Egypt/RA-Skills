#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire('/opt/homebrew/lib/node_modules/openclaw/package.json');
const Lark = require('@larksuiteoapi/node-sdk');

function parseArgs(argv) {
  const out = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    const b = argv[i + 1];
    if (a === '-d' || a === '--dir') { out.reportDir = b; i++; continue; }
    if (a === '-u' || a === '--url') { out.docUrl = b; i++; continue; }
    if (a === '-t' || a === '--title') { out.title = b; i++; continue; }
    if (a === '-h' || a === '--help') { out.help = true; }
  }
  return out;
}

function usage() {
  console.log(`上传周报到飞书文档

用法:
  node upload-to-feishu.js -d <report_dir> [-u <doc_url>] [-t <title>]

说明:
  - 提供 -u: 覆盖写入已有文档
  - 不提供 -u: 若 config.json 配了 feishu.parent_wiki_url，则默认在该父 wiki 下新建子文档；否则新建独立文档

环境变量:
  FEISHU_APP_ID
  FEISHU_APP_SECRET`);
}

function extractToken(url) {
  const m = String(url).match(/\/(wiki|docx)\/([^/?#]+)/);
  if (!m) throw new Error(`无法从 URL 提取 token: ${url}`);
  return { kind: m[1], token: m[2] };
}

function getFeishuOrigin(url) {
  try {
    const u = new URL(url);
    return `${u.protocol}//${u.host}`;
  } catch {
    return 'https://feishu.cn';
  }
}

function expandHome(p) {
  if (!p) return p;
  return p.startsWith('~/') ? path.join(os.homedir(), p.slice(2)) : p;
}

function loadConfig() {
  const configPath = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../config/config.json');
  if (!fs.existsSync(configPath)) return {};
  try {
    return JSON.parse(fs.readFileSync(configPath, 'utf8'));
  } catch {
    return {};
  }
}

function loadUserAccessToken(cfg) {
  const envToken = process.env.FEISHU_USER_ACCESS_TOKEN;
  if (envToken) return envToken;
  const tokenFile = expandHome(cfg?.feishu?.user_token_file || '~/path/to/feishu_token.json');
  if (!tokenFile || !fs.existsSync(tokenFile)) return '';
  try {
    const data = JSON.parse(fs.readFileSync(tokenFile, 'utf8'));
    return data?.access_token || '';
  } catch {
    return '';
  }
}

function normalizeMarkdownForFeishu(markdown) {
  return String(markdown)
    .replace(/\r\n/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .replace(/^\s{2,}-\s+/gm, '- ')
    .replace(/^\s{4,}-\s+/gm, '- ')
    .replace(/^\|(.+)\|$/gm, (_m, inner) => `- ${String(inner).replace(/\|/g, '｜').trim()}`)
    .trim() + '\n';
}

function splitMarkdownByHeadings(markdown) {
  const lines = markdown.split('\n');
  const chunks = [];
  let current = [];
  let inFence = false;
  for (const line of lines) {
    if (/^(`{3,}|~{3,})/.test(line)) inFence = !inFence;
    if (!inFence && /^#{1,2}\s/.test(line) && current.length > 0) {
      chunks.push(current.join('\n'));
      current = [];
    }
    current.push(line);
  }
  if (current.length) chunks.push(current.join('\n'));
  return chunks.filter(Boolean);
}

function splitMarkdownForAppend(markdown, maxChars = 6000) {
  const sections = [];
  const lines = markdown.split('\n');
  let current = [];
  for (const line of lines) {
    if (line.startsWith('## ') && current.length > 0) {
      sections.push(current.join('\n').trim() + '\n');
      current = [line];
    } else {
      current.push(line);
    }
  }
  if (current.length) sections.push(current.join('\n').trim() + '\n');

  const out = [];
  for (const section of sections) {
    if (section.length <= maxChars) {
      out.push(section);
      continue;
    }
    const subparts = splitMarkdownByHeadings(section);
    let buf = '';
    for (const part of subparts) {
      const candidate = buf ? `${buf}\n${part}` : part;
      if (candidate.length <= maxChars) {
        buf = candidate;
      } else {
        if (buf) out.push(buf.trim() + '\n');
        if (part.length <= maxChars) {
          buf = part;
        } else {
          const paras = part.split(/\n\n+/);
          let pbuf = '';
          for (const para of paras) {
            const cand = pbuf ? `${pbuf}\n\n${para}` : para;
            if (cand.length <= maxChars) pbuf = cand;
            else {
              if (pbuf) out.push(pbuf.trim() + '\n');
              pbuf = para;
            }
          }
          buf = pbuf;
        }
      }
    }
    if (buf) out.push(buf.trim() + '\n');
  }
  return out.filter(Boolean);
}

function cleanBlocksForInsert(blocks) {
  const skipped = [];
  const cleaned = (blocks || []).filter(Boolean).map((block) => {
    const clone = JSON.parse(JSON.stringify(block));
    delete clone.block_id;
    delete clone.parent_id;
    delete clone.children;
    delete clone.children_ids;
    delete clone.revision_id;
    delete clone.deleted;
    delete clone.create_time;
    delete clone.update_time;
    return clone;
  }).filter((block) => {
    if (block.block_type === 31 || block.block_type === 32) {
      skipped.push(`skip structured block type=${block.block_type}`);
      return false;
    }
    return true;
  });
  return { cleaned, skipped };
}

async function clearDocumentContent(client, docToken, options = undefined) {
  const existing = await client.docx.documentBlock.list({ path: { document_id: docToken } }, options);
  if (existing.code !== 0) throw new Error(existing.msg);
  const childIds = (existing.data?.items || [])
    .filter((b) => b.parent_id === docToken && b.block_type !== 1)
    .map((b) => b.block_id);
  if (childIds.length > 0) {
    const res = await client.docx.documentBlockChildren.batchDelete({
      path: { document_id: docToken, block_id: docToken },
      data: { start_index: 0, end_index: childIds.length },
    }, options);
    if (res.code !== 0) throw new Error(res.msg);
  }
  return childIds.length;
}

async function updateWikiNodeTitle(client, spaceId, nodeToken, title, options = undefined) {
  if (!spaceId || !nodeToken || !title) return;
  const res = await client.wiki.spaceNode.updateTitle({
    path: { space_id: spaceId, node_token: nodeToken },
    data: { title },
  }, options);
  if (res.code !== 0) throw new Error(`更新 wiki 节点标题失败: ${res.msg}`);
}

async function convertMarkdown(client, markdown, options = undefined) {
  const res = await client.docx.document.convert({
    data: { content_type: 'markdown', content: markdown },
  }, options);
  if (res.code !== 0) throw new Error(res.msg);
  return { blocks: res.data?.blocks || [], firstLevelBlockIds: res.data?.first_level_block_ids || [] };
}

function sortBlocksByFirstLevel(blocks, firstLevelIds) {
  if (!firstLevelIds || !firstLevelIds.length) return blocks;
  const sorted = firstLevelIds.map((id) => blocks.find((b) => b.block_id === id)).filter(Boolean);
  const sortedIds = new Set(firstLevelIds);
  return [...sorted, ...blocks.filter((b) => !sortedIds.has(b.block_id))];
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function insertBlocks(client, docToken, blocks, options = undefined) {
  const { cleaned, skipped } = cleanBlocksForInsert(blocks);
  const allInserted = [];
  for (const block of cleaned) {
    let lastErr;
    for (let attempt = 1; attempt <= 6; attempt++) {
      try {
        const res = await client.docx.documentBlockChildren.create({
          path: { document_id: docToken, block_id: docToken },
          data: { children: [block] },
        }, options);
        if (res.code !== 0) throw new Error(res.msg);
        allInserted.push(...(res.data?.children || []));
        await sleep(180);
        lastErr = undefined;
        break;
      } catch (err) {
        lastErr = err;
        const msg = String(err?.message || err || '');
        if (!msg.includes('429') || attempt === 6) {
          throw err;
        }
        await sleep(500 * attempt);
      }
    }
    if (lastErr) throw lastErr;
  }
  return { inserted: allInserted.length, skipped };
}

async function resolveDocToken(client, url) {
  const { kind, token } = extractToken(url);
  if (kind === 'docx') return token;
  const res = await client.wiki.space.getNode({ params: { token, obj_type: 'wiki' } });
  if (res.code !== 0) throw new Error(`解析 wiki 节点失败: ${res.msg}`);
  const objToken = res.data?.node?.obj_token;
  if (!objToken) throw new Error('wiki 节点没有返回 obj_token');
  return objToken;
}

async function createDoc(client, title, options = undefined) {
  const res = await client.docx.document.create({ data: { title } }, options);
  if (res.code !== 0) throw new Error(`创建文档失败: ${res.msg}`);
  const docToken = res.data?.document?.document_id;
  if (!docToken) throw new Error('创建文档成功但没有返回 document_id');
  return { docToken, docUrl: `https://feishu.cn/docx/${docToken}` };
}

async function createDocUnderWiki(client, parentWikiUrl, title, options) {
  const { token } = extractToken(parentWikiUrl);
  const nodeRes = await client.wiki.space.getNode({ params: { token, obj_type: 'wiki' } }, options);
  if (nodeRes.code !== 0) throw new Error(`解析父 wiki 节点失败: ${nodeRes.msg}`);
  const spaceId = nodeRes.data?.node?.space_id;
  const parentNodeToken = nodeRes.data?.node?.node_token;
  if (!spaceId || !parentNodeToken) throw new Error('父 wiki 节点缺少 space_id 或 node_token');
  const createRes = await client.wiki.spaceNode.create({
    path: { space_id: spaceId },
    data: { obj_type: 'docx', parent_node_token: parentNodeToken, node_type: 'origin', title },
  }, options);
  if (createRes.code !== 0) throw new Error(`在 wiki 下创建子文档失败: ${createRes.msg}`);
  const docToken = createRes.data?.node?.obj_token;
  const nodeToken = createRes.data?.node?.node_token;
  if (!docToken) throw new Error('wiki 子文档创建成功但没有返回 obj_token');
  const origin = getFeishuOrigin(parentWikiUrl);
  return {
    docToken,
    nodeToken,
    docUrl: `${origin}/docx/${docToken}`,
    wikiNodeUrl: `${origin}/wiki/${nodeToken}`,
  };
}

async function maybeUpdateTitle(client, docToken, title) {
  if (!title) return;
  if (typeof client.docx?.document?.patch !== 'function') return;
  const res = await client.docx.document.patch({ path: { document_id: docToken }, data: { title } });
  if (res.code !== 0) console.warn(`⚠️ 更新标题失败: ${res.msg}`);
}

async function appendMarkdownChunk(client, docToken, markdown, options = undefined) {
  const converted = await convertMarkdown(client, markdown, options);
  const sorted = sortBlocksByFirstLevel(converted.blocks, converted.firstLevelBlockIds);
  return insertBlocks(client, docToken, sorted, options);
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help || !args.reportDir) {
    usage();
    process.exit(args.help ? 0 : 1);
  }
  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) throw new Error('缺少 FEISHU_APP_ID / FEISHU_APP_SECRET');

  const mdFile = path.join(path.resolve(args.reportDir), 'weekly_report.md');
  if (!fs.existsSync(mdFile)) throw new Error(`周报文件不存在: ${mdFile}`);
  const markdown = normalizeMarkdownForFeishu(fs.readFileSync(mdFile, 'utf8'));

  const client = new Lark.Client({
    appId,
    appSecret,
    appType: Lark.AppType.SelfBuild,
    domain: Lark.Domain.Feishu,
  });

  const cfg = loadConfig();
  const configTitlePrefix = cfg?.report?.title_prefix || 'GitLab Weekly Report';
  const desiredTitle = args.title || `${configTitlePrefix} ${path.basename(path.resolve(args.reportDir)).replace('_to_', ' ~ ')}`;
  const userAccessToken = loadUserAccessToken(cfg);
  const userOpts = userAccessToken ? Lark.withUserAccessToken(userAccessToken) : undefined;
  let docUrl = args.docUrl || cfg?.feishu?.doc_url || '';
  const parentWikiUrl = cfg?.feishu?.parent_wiki_url || '';
  let docToken;
  let created = false;
  let createdUnderWiki = false;
  let wikiNodeUrl = '';
  let wikiSpaceId = '';
  let wikiNodeToken = '';

  if (docUrl) {
    docToken = await resolveDocToken(client, docUrl);
  } else if (parentWikiUrl && userOpts) {
    const createdDoc = await createDocUnderWiki(client, parentWikiUrl, desiredTitle, userOpts);
    docToken = createdDoc.docToken;
    docUrl = createdDoc.docUrl;
    wikiNodeUrl = createdDoc.wikiNodeUrl;
    wikiNodeToken = createdDoc.nodeToken;
    created = true;
    createdUnderWiki = true;
    const parentNode = await client.wiki.space.getNode({ params: { token: extractToken(parentWikiUrl).token, obj_type: 'wiki' } }, userOpts);
    wikiSpaceId = parentNode.data?.node?.space_id || '';
  } else {
    const createdDoc = await createDoc(client, desiredTitle, userOpts);
    docToken = createdDoc.docToken;
    docUrl = createdDoc.docUrl;
    created = true;
  }

  const editOpts = userOpts;
  const deleted = await clearDocumentContent(client, docToken, editOpts);
  const chunks = splitMarkdownForAppend(markdown, 6000);
  let inserted = 0;
  const skipped = [];
  for (let i = 0; i < chunks.length; i++) {
    const res = await appendMarkdownChunk(client, docToken, chunks[i], editOpts);
    inserted += res.inserted;
    skipped.push(...res.skipped);
    await sleep(1200);
  }
  if (createdUnderWiki) {
    await updateWikiNodeTitle(client, wikiSpaceId, wikiNodeToken, desiredTitle, userOpts);
  } else {
    await maybeUpdateTitle(client, docToken, desiredTitle);
  }

  const result = {
    success: true,
    created,
    created_under_wiki: createdUnderWiki,
    parent_wiki_url: parentWikiUrl || undefined,
    wiki_node_url: wikiNodeUrl || undefined,
    doc_url: docUrl,
    doc_token: docToken,
    markdown_file: mdFile,
    blocks_deleted: deleted,
    blocks_inserted: inserted,
    skipped,
  };
  console.log(JSON.stringify(result, null, 2));
}

main().catch((err) => {
  console.error(err?.stack || String(err));
  process.exit(1);
});
