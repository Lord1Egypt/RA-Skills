// tokenizer.mjs - 中文分词 + TF-IDF (v2.0)
// 支持 jieba 精确分词 + n-gram fallback

import { getDb } from '../db/database.mjs';

let _jieba = null;
let _jiebaLoaded = false;
let _ngramSize = 3;
let _stopwords = new Set([
  '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
  '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
  '自己', '这', '那', '他', '她', '它', '们', '什么', '怎么', '为什么', '哪',
  '吗', '啊', '吧', '呢', '哦', '嗯', '哈', '呀', '喂', '诶', '唉', '嘿',
  '可以', '可能', '应该', '需要', '还是', '或者', '但是', '因为', '所以',
  '如果', '虽然', '即使', '不过', '只是', '而且', '然后', '再', '又',
]);

// 初始化分词器
export async function initTokenizer(config) {
  const mode = config?.tokenizer?.mode || 'auto';

  if (mode === 'jieba' || mode === 'auto') {
    try {
      _jieba = await import('nodejieba');
      // nodejieba 默认已加载词典
      _jiebaLoaded = true;
      console.log('✅ 分词器: jieba 已加载');
      return true;
    } catch (e) {
      console.log('ℹ️ jieba 不可用，使用 n-gram fallback:', e.message);
      _jieba = null;
      if (mode === 'jieba') return false;
    }
  }

  console.log('✅ 分词器: n-gram fallback 已激活');
  _ngramSize = config?.tokenizer?.ngramSize || 3;
  return true;
}

// 分词
export function tokenize(text) {
  if (!text) return [];

  // jieba 分词
  if (_jiebaLoaded && _jieba) {
    try {
      const words = _jieba.cut(text, false);  // 精确模式
      return words.filter(w => !_stopwords.has(w) && w.length > 1);
    } catch {
      // fallback to n-gram
    }
  }

  // n-gram fallback
  return ngramTokenize(text, _ngramSize);
}

// n-gram 分词
function ngramTokenize(text, size) {
  const tokens = [];
  const cleanText = text.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '');

  // 字符级 n-gram
  for (let n = 2; n <= size; n++) {
    for (let i = 0; i <= cleanText.length - n; i++) {
      const gram = cleanText.slice(i, i + n);
      if (!_stopwords.has(gram)) {
        tokens.push(gram);
      }
    }
  }

  // 英文单词提取（简单空格分割）
  const words = cleanText.split(/[\u4e00-\u9fa5]+/).filter(w => w.length > 2);
  for (const word of words) {
    tokens.push(word.toLowerCase());
  }

  return tokens;
}

// ============= TF-IDF 计算 =============

let _idfCache = new Map();
let _docCount = 0;

// 计算文档 TF
function computeTF(tokens) {
  const tf = new Map();
  const total = tokens.length;

  for (const token of tokens) {
    tf.set(token, (tf.get(token) || 0) + 1);
  }

  for (const [token, count] of tf) {
    tf.set(token, count / total);
  }

  return tf;
}

// 从数据库计算 IDF
function computeIDF(config) {
  const db = getDb();
  const rows = db.exec("SELECT id, title, summary, content FROM memories WHERE status != 'archived'");
  if (!rows.length) return;

  const docs = rows[0].values.map(v => `${v[1]} ${v[2]} ${v[3]}`);
  _docCount = docs.length;

  // 统计每个词出现的文档数
  const df = new Map();
  for (const doc of docs) {
    const tokens = tokenize(doc);
    const uniqueTokens = new Set(tokens);
    for (const token of uniqueTokens) {
      df.set(token, (df.get(token) || 0) + 1);
    }
  }

  // 计算 IDF
  for (const [token, count] of df) {
    _idfCache.set(token, Math.log(_docCount / (count + 1)) + 1);
  }
}

// TF-IDF 向量
export function computeTFIDF(text, config) {
  if (_idfCache.size === 0) computeIDF(config);

  const tokens = tokenize(text);
  const tf = computeTF(tokens);

  const vector = new Map();
  for (const [token, tfVal] of tf) {
    const idfVal = _idfCache.get(token) || 1;
    vector.set(token, tfVal * idfVal);
  }

  return vector;
}

// TF-IDF 搜索
export function searchTFIDF(query, options = {}) {
  const { limit = 20, threshold = 0.1, config } = options;

  if (_idfCache.size === 0) computeIDF(config);

  const queryVector = computeTFIDF(query, config);
  const db = getDb();

  const rows = db.exec(
    "SELECT id, title, summary, content, layer, recall_count, last_active_ts FROM memories WHERE status != 'archived'"
  );

  if (!rows.length) return [];

  const results = [];
  for (const row of rows[0].values) {
    const [id, title, summary, content, layer, recallCount, lastActiveTs] = row;
    const docText = `${title} ${summary} ${content}`;
    const docVector = computeTFIDF(docText, config);

    const score = dotProduct(queryVector, docVector);
    if (score >= threshold) {
      results.push({
        id, title, summary, layer, recallCount, lastActiveTs,
        score, matchType: 'tfidf',
      });
    }
  }

  // 按分数排序
  results.sort((a, b) => b.score - a.score);
  return results.slice(0, limit);
}

// 点积
function dotProduct(vecA, vecB) {
  let sum = 0;
  for (const [token, valA] of vecA) {
    const valB = vecB.get(token) || 0;
    sum += valA * valB;
  }
  return sum;
}

// 清空 IDF 缓存（新记忆添加后调用）
export function clearIDFCache() {
  _idfCache.clear();
  _docCount = 0;
}

// 获取状态
export function getStatus() {
  return {
    mode: _jiebaLoaded ? 'jieba' : 'ngram',
    ngramSize: _ngramSize,
    idfCached: _idfCache.size,
    docCount: _docCount,
  };
}