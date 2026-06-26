/**
 * 需求对比器 v2.6.0
 * 
 * 检测新旧需求差异，识别追加、修改、删除
 */

class RequirementDiff {
  constructor() {
    this.keywords = {
      addition: ['追加', '新增', '添加', '增加', 'plus', 'add', 'new'],
      modification: ['修改', '调整', '优化', '改进', 'update', 'modify', 'improve'],
      removal: ['删除', '移除', '去掉', 'remove', 'delete'],
      iteration: ['迭代', '更新', '升级', 'iterate', 'update']
    };
  }
  
  /**
   * 检测需求类型
   */
  detectType(userInput) {
    const input = userInput.toLowerCase();
    
    for (const [type, keywords] of Object.entries(this.keywords)) {
      if (keywords.some(keyword => input.includes(keyword))) {
        return type;
      }
    }
    
    return 'unknown';
  }
  
  /**
   * 对比新旧需求
   */
  async compare(newInput, existingDecomposition) {
    const diffType = this.detectType(newInput);
    
    const changes = {
      type: diffType,
      newInput: newInput,
      timestamp: new Date().toISOString(),
      affectedFeatures: [],
      newFeatures: [],
      modifiedFeatures: [],
      removedFeatures: []
    };
    
    // 根据类型分析变更
    switch (diffType) {
      case 'addition':
        changes.newFeatures = this.extractFeatures(newInput);
        break;
        
      case 'modification':
        changes.modifiedFeatures = this.extractFeatures(newInput);
        break;
        
      case 'removal':
        changes.removedFeatures = this.extractFeatures(newInput);
        break;
        
      default:
        // 未知类型，尝试智能分析
        changes.newFeatures = this.extractFeatures(newInput);
    }
    
    // 检查是否影响现有功能
    if (existingDecomposition && existingDecomposition.features) {
      changes.affectedFeatures = this.findAffectedFeatures(
        newInput,
        existingDecomposition.features
      );
    }
    
    return changes;
  }
  
  /**
   * 提取功能关键词
   */
  extractFeatures(text) {
    // 简单实现：提取名词短语
    const features = [];
    
    // 匹配"XX 功能"、"XX 模块"等模式
    const patterns = [
      /(.+?) 功能/g,
      /(.+?) 模块/g,
      /(.+?) 系统/g,
      /(.+?) 服务/g
    ];
    
    patterns.forEach(pattern => {
      let match;
      while ((match = pattern.exec(text)) !== null) {
        features.push(match[1].trim());
      }
    });
    
    // 如果没有匹配到，使用整个输入
    if (features.length === 0) {
      features.push(text.trim());
    }
    
    return features;
  }
  
  /**
   * 查找受影响的功能
   */
  findAffectedFeatures(newInput, existingFeatures) {
    const affected = [];
    
    existingFeatures.forEach(feature => {
      // 检查新输入是否提到现有功能
      if (newInput.includes(feature.name) || newInput.includes(feature.description)) {
        affected.push({
          feature: feature,
          reason: '直接提及'
        });
      }
      
      // 检查语义相关性（简化版：关键词匹配）
      const relatedKeywords = this.getRelatedKeywords(feature.name);
      if (relatedKeywords.some(keyword => newInput.includes(keyword))) {
        affected.push({
          feature: feature,
          reason: '语义相关'
        });
      }
    });
    
    return affected;
  }
  
  /**
   * 获取相关关键词
   */
  getRelatedKeywords(featureName) {
    // 简化实现：返回功能名称的分词
    return featureName.split(/[\s,，.。]/).filter(w => w.length > 1);
  }
  
  /**
   * 生成变更摘要
   */
  generateSummary(changes) {
    const summary = [];
    
    switch (changes.type) {
      case 'addition':
        summary.push(`新增 ${changes.newFeatures.length} 个功能`);
        break;
      case 'modification':
        summary.push(`修改 ${changes.modifiedFeatures.length} 个功能`);
        break;
      case 'removal':
        summary.push(`删除 ${changes.removedFeatures.length} 个功能`);
        break;
      default:
        summary.push(`更新需求`);
    }
    
    if (changes.affectedFeatures.length > 0) {
      summary.push(`影响 ${changes.affectedFeatures.length} 个现有功能`);
    }
    
    return summary.join('，');
  }
}

module.exports = { RequirementDiff };
