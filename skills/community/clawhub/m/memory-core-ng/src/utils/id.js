/**
 * 🎯 简单的 ID 生成器
 * 用于避免外部依赖
 */

class SimpleIdGenerator {
  /**
   * 生成简单唯一 ID
   */
  static generate() {
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substring(2, 10);
    return `id_${timestamp}_${random}`;
  }
  
  /**
   * 生成基于内容的 ID
   */
  static generateFromContent(content) {
    // 简单哈希
    let hash = 0;
    for (let i = 0; i < content.length; i++) {
      hash = ((hash << 5) - hash) + content.charCodeAt(i);
      hash = hash & hash; // 转换为 32 位整数
    }
    
    const timestamp = Date.now().toString(36);
    return `cid_${Math.abs(hash).toString(36)}_${timestamp}`;
  }
}

module.exports = { SimpleIdGenerator };
