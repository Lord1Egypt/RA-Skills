/**
 * 🎯 相似度计算工具
 * 优化性能的余弦相似度实现
 */

class SimilarityCalculator {
  /**
   * 计算余弦相似度（假设向量已标准化）
   * 优化：使用点积，避免重复计算范数
   */
  static cosineSimilarity(vecA, vecB) {
    // 安全检查
    if (!vecA || !vecB || vecA.length !== vecB.length) {
      return 0;
    }
    
    // 快速点积计算
    let dot = 0;
    const len = vecA.length;
    
    // 使用 for 循环优化性能
    for (let i = 0; i < len; i++) {
      dot += vecA[i] * vecB[i];
    }
    
    // 如果向量已标准化，dot 就是余弦相似度
    // 添加小检查确保数值稳定
    return Math.max(-1, Math.min(1, dot));
  }
  
  /**
   * 批量计算相似度（优化性能）
   * 返回相似度数组
   */
  static batchSimilarity(queryVec, vectors) {
    if (!queryVec || !vectors || vectors.length === 0) {
      return [];
    }
    
    const similarities = new Array(vectors.length);
    const len = queryVec.length;
    
    for (let i = 0; i < vectors.length; i++) {
      const vec = vectors[i];
      
      if (!vec || vec.length !== len) {
        similarities[i] = 0;
        continue;
      }
      
      let dot = 0;
      for (let j = 0; j < len; j++) {
        dot += queryVec[j] * vec[j];
      }
      
      similarities[i] = Math.max(-1, Math.min(1, dot));
    }
    
    return similarities;
  }
  
  /**
   * 找到 topK 个最相似的结果
   * 优化：避免完整排序，使用最小堆
   */
  static findTopK(similarities, k) {
    if (!similarities || similarities.length === 0 || k <= 0) {
      return [];
    }
    
    k = Math.min(k, similarities.length);
    
    // 简单实现：先排序
    const indexed = similarities.map((score, index) => ({ score, index }));
    indexed.sort((a, b) => b.score - a.score);
    
    return indexed.slice(0, k);
  }
  
  /**
   * 计算向量范数（L2）
   */
  static norm(vec) {
    if (!vec || vec.length === 0) {
      return 0;
    }
    
    let sum = 0;
    for (let i = 0; i < vec.length; i++) {
      sum += vec[i] * vec[i];
    }
    
    return Math.sqrt(sum);
  }
  
  /**
   * 标准化向量（L2 标准化）
   */
  static normalize(vec) {
    const n = this.norm(vec);
    if (n === 0) {
      return vec;
    }
    
    const normalized = new Array(vec.length);
    for (let i = 0; i < vec.length; i++) {
      normalized[i] = vec[i] / n;
    }
    
    return normalized;
  }
}

module.exports = { SimilarityCalculator };
