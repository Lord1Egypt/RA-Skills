// semantic-similarity.mjs - 语义相似度检测
// 基于TF-IDF + 余弦相似度的简化实现

// 简单中文分词（字符级 + n-gram + 英文词）
function tokenize(text) {
  if (!text) return [];
  const cleaned = text.toLowerCase().replace(/[^\u4e00-\u9fa5a-z0-9]/g, ' ');
  const tokens = [];
  
  // 提取英文单词
  const englishWords = cleaned.match(/[a-z0-9]+/g) || [];
  tokens.push(...englishWords);
  
  // 提取中文字符（单字）
  const chars = cleaned.replace(/[a-z0-9]/g, '').split('').filter(c => c.trim());
  tokens.push(...chars);
  
  // 提取2-3字中文n-gram
  for (let n = 2; n <= 3 && n <= chars.length; n++) {
    for (let i = 0; i <= chars.length - n; i++) {
      tokens.push(chars.slice(i, i + n).join(''));
    }
  }
  
  return [...new Set(tokens)];
}

// 创建词频向量
function createVector(text, vocab) {
  const tokens = tokenize(text);
  const vec = new Array(vocab.length).fill(0);
  for (const token of tokens) {
    const idx = vocab.indexOf(token);
    if (idx >= 0) vec[idx]++;
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

// 语义相似度检测（核心函数）
export function semanticSimilarity(textA, textB) {
  const tokensA = tokenize(textA);
  const tokensB = tokenize(textB);
  const vocab = [...new Set([...tokensA, ...tokensB])];
  
  const vecA = createVector(textA, vocab);
  const vecB = createVector(textB, vocab);
  
  return cosineSimilarity(vecA, vecB);
}

// 批量比较 - 找出相似的记忆
export function findSimilarMemories(newMemory, existingMemories, threshold = 0.6) {
  const similarities = [];
  
  for (const mem of existingMemories) {
    const titleSim = semanticSimilarity(newMemory.title, mem.title);
    const summarySim = semanticSimilarity(newMemory.summary, mem.summary);
    const tagsOverlap = newMemory.tags.filter(t => mem.tags.includes(t)).length;
    
    // 综合相似度
    const combined = (titleSim * 0.4) + (summarySim * 0.4) + (tagsOverlap * 0.2);
    
    if (combined >= threshold || tagsOverlap >= 3) {
      similarities.push({
        id: mem.id,
        title: mem.title,
        similarity: combined,
        titleSim,
        summarySim,
        tagsOverlap,
        canMerge: combined >= 0.7 || tagsOverlap >= 3
      });
    }
  }
  
  return similarities.sort((a, b) => b.similarity - a.similarity);
}

// 合并两个记忆
export function mergeMemories(memA, memB) {
  return {
    ...memA,
    id: memA.id, // 保留较新的ID
    title: memA.title.length > memB.title.length ? memA.title : memB.title,
    tags: [...new Set([...memA.tags, ...memB.tags])],
    recallCount: (memA.recallCount || 0) + (memB.recallCount || 0) + 1,
    recallDays: [...new Set([...(memA.recallDays || []), ...(memB.recallDays || [])])],
    summary: memA.summary + ' | ' + memB.summary.slice(0, 100),
    turns: (memA.turns || 0) + (memB.turns || 0),
    lastActive: new Date().toISOString().split('T')[0],
    ttl: Math.max(memA.ttl || 7, memB.ttl || 7) // TTL取较长
  };
}

// CLI测试
if (process.argv[1].endsWith('semantic-similarity.mjs')) {
  const testPairs = [
    ["AI定价策略讨论", "Token成本分析"],
    ["iPhone17价格查询", "苹果手机多少钱"],
    ["龙虾服务修复", "AI记忆系统架构"],
    ["memory-architecture", "记忆系统优化"]
  ];
  
  console.log('语义相似度测试:\n');
  for (const [a, b] of testPairs) {
    const sim = semanticSimilarity(a, b);
    console.log(`"${a}" <-> "${b}"`);
    console.log(`相似度: ${(sim * 100).toFixed(1)}%\n`);
  }
  
  // 测试记忆合并
  const memA = {
    id: "test-1",
    title: "AI定价策略",
    tags: ["AI", "定价"],
    summary: "讨论了Token成本",
    recallCount: 3,
    ttl: 7
  };
  const memB = {
    id: "test-2", 
    title: "Token成本分析",
    tags: ["Token", "成本", "AI"],
    summary: "分析了厂商定价",
    recallCount: 5,
    ttl: 15
  };
  
  console.log('记忆合并测试:');
  console.log('记忆A:', memA);
  console.log('记忆B:', memB);
  console.log('\n合并结果:', mergeMemories(memA, memB));
}
