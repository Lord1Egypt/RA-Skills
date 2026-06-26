/**
 * FTSIndexer - P1-1 FTS5全文检索
 * 从 JSON 遍历 → 毫秒级检索
 * 
 * 实现：
 * 1. 反向索引（Inverted Index）- 词 → 文档列表
 * 2. TF-IDF 权重计算
 * 3. 支持模糊匹配和短语检索
 */

const fs = require('fs');
const path = require('path');

const INDEX_DIR = path.join(__dirname, '.fts');

// 停用词（中文常用）
const STOP_WORDS = new Set([
  '的', '了', '是', '我', '你', '他', '她', '它', '在', '有', '和',
  '就', '不', '也', '都', '这', '那', '要', '会', '能', '可以',
  '的', '吗', '呢', '吧', '啊', '哦', '嗯', '啦', '喔', '呀'
]);

class FTSIndexer {
  constructor() {
    this.invertedIndex = new Map();  // word → [{docId, tf, positions}]
    this.documents = new Map();       // docId → {content, meta}
    this.docCount = 0;
  }

  /**
   * 分词
   */
  tokenize(text) {
    if (!text) return [];
    
    // 中英文混合分词
    const tokens = [];
    
    // 处理中文
    const chinesePattern = /[\u4e00-\u9fa5]+/g;
    let match;
    while ((match = chinesePattern.exec(text)) !== null) {
      const word = match[0];
      // 简单处理：取前两个字和整词
      if (word.length >= 2) {
        tokens.push(word.substring(0, 2));
      }
      tokens.push(word);
    }
    
    // 处理英文和数字
    const englishPattern = /[a-zA-Z0-9_]+/g;
    while ((match = englishPattern.exec(text)) !== null) {
      const word = match[0].toLowerCase();
      if (word.length > 1) {
        tokens.push(word);
      }
    }
    
    // 过滤停用词
    return tokens.filter(t => !STOP_WORDS.has(t) && t.length > 1);
  }

  /**
   * 添加文档到索引
   */
  addDocument(docId, content, meta = {}) {
    const tokens = this.tokenize(content);
    
    // 存储文档
    this.documents.set(docId, { content, meta, tokenCount: tokens.length });
    this.docCount++;
    
    // 统计词频
    const wordCount = new Map();
    for (const token of tokens) {
      wordCount.set(token, (wordCount.get(token) || 0) + 1);
    }
    
    // 更新反向索引
    for (const [word, tf] of wordCount) {
      if (!this.invertedIndex.has(word)) {
        this.invertedIndex.set(word, []);
      }
      
      // 记录词出现位置
      const positions = [];
      for (let i = 0; i < tokens.length; i++) {
        if (tokens[i] === word) {
          positions.push(i);
        }
      }
      
      this.invertedIndex.get(word).push({
        docId,
        tf: tf / tokens.length,  // 归一化词频
        positions
      });
    }
    
    return this;
  }

  /**
   * 计算 IDF（逆文档频率）
   */
  idf(word) {
    const docs = this.invertedIndex.get(word);
    if (!docs) return 0;
    return Math.log(this.docCount / (docs.length + 1)) + 1;
  }

  /**
   * 搜索
   */
  search(query, options = {}) {
    const {
      fuzzy = true,
      fuzzyDistance = 2,
      boost = 0.5,  // 模糊匹配的boost因子
      limit = 10
    } = options;
    
    const queryTokens = this.tokenize(query);
    if (queryTokens.length === 0) return [];
    
    const scores = new Map();  // docId → score
    
    for (const token of queryTokens) {
      // 精确匹配
      if (this.invertedIndex.has(token)) {
        const idf = this.idf(token);
        for (const entry of this.invertedIndex.get(token)) {
          const score = entry.tf * idf;
          scores.set(entry.docId, (scores.get(entry.docId) || 0) + score);
        }
      }
      
      // 模糊匹配
      if (fuzzy) {
        for (const [indexedWord, entries] of this.invertedIndex) {
          if (indexedWord === token) continue;
          
          const distance = this.levenshtein(token, indexedWord);
          if (distance <= fuzzyDistance) {
            const idf = this.idf(indexedWord);
            const fuzzyBoost = boost * (1 - distance / (fuzzyDistance + 1));
            
            for (const entry of entries) {
              const score = entry.tf * idf * fuzzyBoost;
              scores.set(entry.docId, (scores.get(entry.docId) || 0) + score);
            }
          }
        }
      }
    }
    
    // 排序并返回
    const results = Array.from(scores.entries())
      .map(([docId, score]) => ({
        docId,
        score,
        doc: this.documents.get(docId)
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
    
    return results;
  }

  /**
   * 短语搜索
   */
  searchPhrase(phrase, options = {}) {
    const { limit = 10 } = options;
    const tokens = this.tokenize(phrase);
    if (tokens.length === 0) return [];
    
    const scores = new Map();
    
    // 找到包含所有词项的文档
    const docCandidates = new Set();
    for (const token of tokens) {
      if (this.invertedIndex.has(token)) {
        for (const entry of this.invertedIndex.get(token)) {
          docCandidates.add(entry.docId);
        }
      }
    }
    
    // 检查短语是否连续
    for (const docId of docCandidates) {
      const doc = this.documents.get(docId);
      const docTokens = this.tokenize(doc.content);
      
      for (let i = 0; i < docTokens.length - tokens.length + 1; i++) {
        let match = true;
        for (let j = 0; j < tokens.length; j++) {
          if (docTokens[i + j] !== tokens[j]) {
            match = false;
            break;
          }
        }
        
        if (match) {
          const idf = tokens.reduce((acc, t) => acc + this.idf(t), 0) / tokens.length;
          scores.set(docId, (scores.get(docId) || 0) + idf * (tokens.length + 1));
          break;
        }
      }
    }
    
    return Array.from(scores.entries())
      .map(([docId, score]) => ({
        docId,
        score,
        doc: this.documents.get(docId)
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
  }

  /**
   * Levenshtein 距离
   */
  levenshtein(a, b) {
    if (a.length === 0) return b.length;
    if (b.length === 0) return a.length;
    
    const matrix = [];
    
    for (let i = 0; i <= b.length; i++) {
      matrix[i] = [i];
    }
    
    for (let j = 0; j <= a.length; j++) {
      matrix[0][j] = j;
    }
    
    for (let i = 1; i <= b.length; i++) {
      for (let j = 1; j <= a.length; j++) {
        if (b.charAt(i - 1) === a.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          );
        }
      }
    }
    
    return matrix[b.length][a.length];
  }

  /**
   * 保存索引到文件
   */
  save(indexName = 'default') {
    if (!fs.existsSync(INDEX_DIR)) {
      fs.mkdirSync(INDEX_DIR, { recursive: true });
    }
    
    const data = {
      invertedIndex: Array.from(this.invertedIndex.entries()),
      documents: Array.from(this.documents.entries()),
      docCount: this.docCount
    };
    
    const filePath = path.join(INDEX_DIR, `${indexName}.json`);
    fs.writeFileSync(filePath, JSON.stringify(data), 'utf-8');
    
    console.log(`[FTSIndexer] 💾 索引已保存: ${indexName} (${this.docCount} 文档)`);
    return this;
  }

  /**
   * 从文件加载索引
   */
  load(indexName = 'default') {
    const filePath = path.join(INDEX_DIR, `${indexName}.json`);
    
    if (!fs.existsSync(filePath)) {
      console.log(`[FTSIndexer] ⚠️ 索引文件不存在: ${indexName}`);
      return this;
    }
    
    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    
    this.invertedIndex = new Map(data.invertedIndex);
    this.documents = new Map(data.documents);
    this.docCount = data.docCount;
    
    console.log(`[FTSIndexer] 📂 索引已加载: ${indexName} (${this.docCount} 文档)`);
    return this;
  }

  /**
   * 获取索引统计
   */
  getStats() {
    return {
      docCount: this.docCount,
      wordCount: this.invertedIndex.size,
      avgDocLength: Array.from(this.documents.values())
        .reduce((acc, d) => acc + d.tokenCount, 0) / (this.docCount || 1)
    };
  }
}

// 导出
module.exports = { FTSIndexer };
