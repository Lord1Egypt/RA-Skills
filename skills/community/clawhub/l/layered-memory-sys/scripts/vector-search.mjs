// vector-search.mjs v1.1 - 向量搜索模块
// 混合方案：TF-IDF增强版 + Vectra接口预留
// 当有嵌入API时可切换到真正的向量搜索

import fs from 'fs';
import path from 'path';
import { getPath } from './config-loader.mjs';

const INDEX_PATH = getPath('indexFile');

// 中文分词器 v1.1（增强版）
function tokenize(text) {
  if (!text) return [];
  const cleaned = text.toLowerCase().replace(/[^\u4e00-\u9fa5a-z0-9]/g, ' ');
  const tokens = [];
  
  // 英文单词
  const englishWords = cleaned.match(/[a-z0-9]+/g) || [];
  tokens.push(...englishWords);
  
  // 中文字符
  const chars = cleaned.replace(/[a-z0-9]/g, '').split('').filter(c => c.trim());
  tokens.push(...chars);
  
  // 中文2-3字n-gram
  for (let n = 2; n <= 3 && n <= chars.length; n++) {
    for (let i = 0; i <= chars.length - n; i++) {
      tokens.push(chars.slice(i, i + n).join(''));
    }
  }
  
  return [...new Set(tokens)];
}

// IDF计算（逆文档频率）
function computeIDF(documents) {
  const N = documents.length;
  const docFreq = {};
  
  for (const doc of documents) {
    const tokens = new Set(tokenize(doc));
    for (const token of tokens) {
      docFreq[token] = (docFreq[token] || 0) + 1;
    }
  }
  
  const idf = {};
  for (const [token, df] of Object.entries(docFreq)) {
    idf[token] = Math.log((N + 1) / (df + 1)) + 1; // 平滑IDF
  }
  
  return idf;
}

// TF-IDF向量
function tfidfVector(text, vocab, idf) {
  const tokens = tokenize(text);
  const tf = {};
  for (const token of tokens) {
    tf[token] = (tf[token] || 0) + 1;
  }
  
  // 归一化TF
  const maxTf = Math.max(...Object.values(tf), 1);
  
  const vec = [];
  for (const token of vocab) {
    const normalizedTf = (tf[token] || 0) / maxTf;
    vec.push(normalizedTf * (idf[token] || 0));
  }
  
  return vec;
}

// 余弦相似度
function cosineSimilarity(vecA, vecB) {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < vecA.length; i++) {
    dot += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

// 构建索引缓存（避免每次重新计算IDF）
let _indexCache = null;
let _cacheTime = 0;

function getIndexedMemories() {
  const now = Date.now();
  if (_indexCache && now - _cacheTime < 60000) { // 60秒缓存
    return _indexCache;
  }
  
  const index = JSON.parse(fs.readFileSync(INDEX_PATH, 'utf-8'));
  const memories = index.memories || [];
  
  // 构建文档语料库
  const documents = memories.map(m => `${m.title} ${m.summary || ''} ${(m.tags || []).join(' ')}`);
  const vocab = [...new Set(documents.flatMap(d => tokenize(d)))];
  const idf = computeIDF(documents);
  
  // 预计算每条记忆的向量
  const vectors = documents.map(doc => tfidfVector(doc, vocab, idf));
  
  _indexCache = { memories, vocab, idf, vectors };
  _cacheTime = now;
  
  return _indexCache;
}

// 搜索记忆
export function searchMemories(query, options = {}) {
  const { maxResults = 10, layer = null, minScore = 0.1 } = options;
  
  const { memories, vocab, idf, vectors } = getIndexedMemories();
  const queryVec = tfidfVector(query, vocab, idf);
  
  const scored = memories.map((mem, i) => {
    const score = cosineSimilarity(queryVec, vectors[i]);
    return { memory: mem, score };
  });
  
  // 过滤
  let results = scored.filter(r => r.score >= minScore);
  if (layer) {
    results = results.filter(r => r.memory.layer === layer);
  }
  
  // 排序
  results.sort((a, b) => b.score - a.score);
  
  // 返回前N条
  return results.slice(0, maxResults);
}

// 检查是否与已有记忆相似（用于去重）
export function findSimilar(query, memories, threshold = 0.6) {
  const queryVec = tfidfVector(query, 
    [...new Set(tokenize(query))], 
    {}
  );
  
  return memories
    .map(mem => {
      const doc = `${mem.title} ${mem.summary || ''}`;
      const docVec = tfidfVector(doc, [...new Set(tokenize(doc))], {});
      return { memory: mem, score: cosineSimilarity(queryVec, docVec) };
    })
    .filter(r => r.score >= threshold)
    .sort((a, b) => b.score - a.score);
}

// 清除缓存
export function clearCache() {
  _indexCache = null;
  _cacheTime = 0;
}

// CLI测试
if (process.argv[1]?.endsWith('vector-search.mjs')) {
  const query = process.argv.slice(2).join(' ') || '记忆系统';
  console.log(`🔍 搜索: "${query}"\n`);
  
  const results = searchMemories(query);
  for (const { memory, score } of results) {
    console.log(`[${(score*100).toFixed(1)}%] [${memory.layer}] ${memory.title}`);
    console.log(`   ${(memory.summary || '').slice(0, 100)}\n`);
  }
}
