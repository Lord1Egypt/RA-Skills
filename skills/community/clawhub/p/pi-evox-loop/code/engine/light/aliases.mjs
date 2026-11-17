// engine/light/aliases.mjs — 概念别名表（0.28 B 轨）
//
// 解决的问题：召回对 CJK 走 **2 字 bigram** 分词，因此多字中文 signals 永远匹配不上
//（实测 130 条基因里 54 个中文 signals 是死信号）；且英文 signals 与中文查询字面零交集。
//
// 做法：一张静态概念表（aliases.json），concept -> { en: [英文 canonical], zh: [中文别名短语] }
//   · 沉淀侧：--trigger 短语 → 切 bigram + 命中概念的 en tokens → **双写进 signals_match**
//   · 召回侧：query token 命中某概念的 zh 别名 → 把该概念的 en tokens **加入 query token 集合**
//     （于是中文查询能命中英文 canonical signals）
//
// 设计红线：只扩展"候选/信号"，**不改变打分公式与阈值**——语义管召回率，确定性管注入精度。
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const TABLE_PATH = path.join(path.dirname(fileURLToPath(import.meta.url)), 'aliases.json');

let _cache = null;
let _loadError = null;
function table() {
  if (_cache) return _cache;
  try {
    const raw = JSON.parse(fs.readFileSync(TABLE_PATH, 'utf8'));
    const concepts = raw.concepts || {};
    // 预计算：每个概念的中文别名 bigram 集合 → 概念映射
    const zhIndex = new Map(); // bigram -> [conceptId]
    for (const [id, c] of Object.entries(concepts)) {
      for (const phrase of c.zh || []) {
        for (const bg of bigrams(phrase)) {
          if (!zhIndex.has(bg)) zhIndex.set(bg, []);
          if (!zhIndex.get(bg).includes(id)) zhIndex.get(bg).push(id);
        }
      }
    }
    _cache = { concepts, zhIndex };
  } catch (e) {
    // 不再静默吞错：别名表读不到会让"预防型基因召不回来"，必须可见
    _loadError = String((e && e.message) || e);
    console.error('[gene-share] ⚠ 别名表加载失败（别名展开将退化为纯字面匹配）：' + _loadError);
    _cache = { concepts: {}, zhIndex: new Map() };
  }
  return _cache;
}

/** 别名表加载错误（供 doctor 体检用） */
export function aliasLoadError() { return _loadError; }

/** CJK bigram 切分（与 evolver-recall.mjs 的 queryTokens 规则一致）
 *  只对 CJK 片段切分——ASCII 片段由 asciiTokens() 单独处理（否则 "python" 会被切成 p/py/yt…噪声） */
export function bigrams(phrase) {
  const out = [];
  const runs = String(phrase || '').match(/[\u4e00-\u9fa5]+/g) || [];
  for (const run of runs) {
    const cs = [...run];
    for (let i = 0; i + 1 < cs.length; i++) out.push(cs[i] + cs[i + 1]);
  }
  return out;
}

/** ASCII token 提取（≥3 字符，与召回分词一致） */
export function asciiTokens(text) {
  return String(text || '').toLowerCase().match(/[a-z0-9_\-./]{3,}/g) || [];
}

/**
 * 展开触发短语 → signals 候选（英文 canonical + 中文 bigram 别名 + 原 ASCII token）
 * @param {string} phrase 触发短语（人话，如「用 python 批量改写文件」）
 * @returns {{tokens: string[], concepts: string[]}}
 */
export function expandTrigger(phrase) {
  const t = table();
  const tokens = new Set();
  const hitConcepts = new Set();
  for (const bg of bigrams(phrase)) {
    const ids = t.zhIndex.get(bg);
    if (ids) for (const id of ids) hitConcepts.add(id);
  }
  for (const a of asciiTokens(phrase)) tokens.add(a);
  for (const bg of bigrams(phrase)) tokens.add(bg); // 中文 bigram 别名直接进 signals
  for (const id of hitConcepts) {
    for (const en of t.concepts[id]?.en || []) tokens.add(en);
  }
  return { tokens: [...tokens], concepts: [...hitConcepts] };
}

/**
 * 召回侧：把 query 映射到概念的英文 canonical（中文 query → 英文 signals 命中）
 *
 * ⚠️ 匹配粒度必须是**整别名短语**（如「批量改写」「改文件」作为子串出现在 query 里），
 * **不能**用 bigram 级命中——单个二元词重合就太松（实测：「删除所有临时**文件**」含「文**件**」
 * 二元词，会命中「改**文件**」的概念 → 展开后把 batch-edit/file-rewrite 等英文 token 加进 query
 * → 无关基因凭 +3 跨过注入阈值 → 负控出现 4 个误选中）。短语级匹配后负控 0 误选。
 *
 * @param {Set<string>} qTokens query 分词结果
 * @param {string} [queryText] query 原文（用于短语级匹配；缺省则退化为 bigram 索引匹配）
 */
export function expandQueryTokens(qTokens, queryText = '') {
  const t = table();
  const out = new Set(qTokens);
  const text = String(queryText || '');
  let matched = false;
  if (text) {
    for (const [id, c] of Object.entries(t.concepts)) {
      for (const phrase of c.zh || []) {
        if (text.includes(phrase)) {
          for (const en of c.en || []) out.add(en);
          matched = true;
          break;
        }
      }
    }
  }
  if (matched) return out;
  // 无短语命中 → 退化：仅当同一概念命中 ≥2 个不同二元词时才展开（单二元词不足以判定意图）
  const counts = new Map();
  for (const tok of qTokens) {
    for (const id of t.zhIndex.get(tok) || []) {
      if (!counts.has(id)) counts.set(id, new Set());
      counts.get(id).add(tok);
    }
  }
  for (const [id, toks] of counts) {
    if (toks.size >= 2) for (const en of t.concepts[id]?.en || []) out.add(en);
  }
  return out;
}

/** 统计表规模（给 report / doctor 用） */
export function aliasStats() {
  const t = table();
  const nConcepts = Object.keys(t.concepts).length;
  let nEn = 0, nZh = 0;
  for (const c of Object.values(t.concepts)) { nEn += (c.en || []).length; nZh += (c.zh || []).length; }
  return { concepts: nConcepts, enTokens: nEn, zhPhrases: nZh, zhBigrams: t.zhIndex.size };
}

/** 找出 signals 中"永不可命中"的多字中文 token（>2 字，在 bigram 分词下是死信号） */
export function deadCjkSignals(signals) {
  return (signals || []).filter((s) => /[\u4e00-\u9fa5]{3,}/.test(String(s)));
}
