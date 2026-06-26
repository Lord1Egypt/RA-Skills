#!/usr/bin/env ts-node
/**
 * 批量生成推荐规则（基于模型分类）
 */

interface RuleTemplate {
  category: string;
  features: string[];
  bonus: number;
  reason: string;
}

const ruleTemplates: RuleTemplate[] = [
  // 心理学模型 - 情绪相关
  { category: 'psychology-emotion', features: ['hasEmotion'], bonus: 15, reason: '警惕情绪化决策' },
  { category: 'psychology-emotion', features: ['hasHerd'], bonus: 15, reason: '注意从众心理' },
  
  // 心理学模型 - 认知偏误
  { category: 'psychology-bias', features: ['hasUncertainty'], bonus: 15, reason: '识别认知偏误' },
  { category: 'psychology-bias', features: ['hasEmotion'], bonus: 10, reason: '警惕判断偏差' },
  
  // 商业模型 - 竞争相关
  { category: 'business', features: ['hasCompetition'], bonus: 20, reason: '评估竞争优势' },
  { category: 'business', features: ['hasLongTerm'], bonus: 15, reason: '关注长期价值' },
  
  // 投资模型 - 价值相关
  { category: 'investment', features: ['hasValue'], bonus: 20, reason: '评估投资价值' },
  { category: 'investment', features: ['hasRisk'], bonus: 15, reason: '识别投资风险' },
  
  // 经济学模型 - 资源相关
  { category: 'economics', features: ['hasResource'], bonus: 20, reason: '优化资源配置' },
  { category: 'economics', features: ['hasOpportunity'], bonus: 15, reason: '评估机会成本' },
  
  // 系统思维 - 长期相关
  { category: 'systems', features: ['hasLongTerm'], bonus: 20, reason: '系统性思考' },
  { category: 'systems', features: ['hasCompetition'], bonus: 10, reason: '理解系统动态' },
];

// 模型分类映射
const modelCategories: Record<string, string> = {
  // 已有的 30 个模型保持原有规则
  '06': 'custom', '07': 'custom', '08': 'custom', '09': 'custom', '10': 'custom',
  '11': 'custom', '12': 'custom', '13': 'custom', '14': 'custom', '15': 'custom',
  '16': 'custom', '17': 'custom', '18': 'custom', '19': 'custom', '20': 'custom',
  '21': 'custom', '22': 'custom', '23': 'custom', '24': 'custom', '25': 'custom',
  '26': 'custom', '27': 'custom', '28': 'custom', '29': 'custom', '30': 'custom',
  
  // 新增模型（31-83）按分类自动生成规则
  '31': 'psychology-emotion',
  '32': 'psychology-emotion',
  '33': 'psychology-bias',
  '34': 'psychology-bias',
  '35': 'psychology-bias',
  // ... 更多模型
};

function generateFeatureBonus(): string {
  let code = `  /**
   * 特征匹配加分
   */
  private getFeatureBonus(modelId: string, features: InputFeatures): number {
    let bonus = 0;
    
    // 核心模型（已有规则）
    if (modelId === '06') { // 误判心理学
      if (features.hasEmotion) bonus += 20;
      if (features.hasHerd) bonus += 20;
      if (features.hasUncertainty) bonus += 10;
    }
    
    // ... 其他已有规则 ...
    
    // 新增模型（通用规则）
    const category = this.getModelCategory(modelId);
    bonus += this.getCategoryBonus(category, features);
    
    return bonus;
  }
  
  /**
   * 获取模型分类
   */
  private getModelCategory(modelId: string): string {
    const categories: Record<string, string> = {
      // 心理学 - 情绪相关
      '31': 'psychology-emotion', '32': 'psychology-emotion',
      // 心理学 - 认知偏误
      '33': 'psychology-bias', '34': 'psychology-bias',
      // 商业模型
      '40': 'business', '41': 'business',
      // 投资模型
      '44': 'investment', '45': 'investment',
      // 经济学模型
      '50': 'economics', '51': 'economics',
      // 系统思维
      '60': 'systems', '61': 'systems',
    };
    return categories[modelId] || 'general';
  }
  
  /**
   * 根据分类获取加分
   */
  private getCategoryBonus(category: string, features: InputFeatures): number {
    let bonus = 0;
    
    switch (category) {
      case 'psychology-emotion':
        if (features.hasEmotion) bonus += 15;
        if (features.hasHerd) bonus += 15;
        break;
      case 'psychology-bias':
        if (features.hasUncertainty) bonus += 15;
        if (features.hasEmotion) bonus += 10;
        break;
      case 'business':
        if (features.hasCompetition) bonus += 20;
        if (features.hasLongTerm) bonus += 15;
        break;
      case 'investment':
        if (features.hasValue) bonus += 20;
        if (features.hasRisk) bonus += 15;
        break;
      case 'economics':
        if (features.hasResource) bonus += 20;
        if (features.hasOpportunity) bonus += 15;
        break;
      case 'systems':
        if (features.hasLongTerm) bonus += 20;
        if (features.hasCompetition) bonus += 10;
        break;
    }
    
    return bonus;
  }`;
  
  return code;
}

console.log(generateFeatureBonus());
