/**
 * 质量门禁 v2.6.0（改造版草稿）
 * 
 * 改动点：
 * 1. gate2 增加内容检查（业务规则/约束条件）
 * 2. gate3 增加规格设计检查
 * 3. 集成 check_items_loader
 */

const checkItemsLoader = require('./check_items_loader.js');

class QualityGate {
  constructor() {
    this.gates = {
      gate1_interview: {
        name: '访谈质量',
        threshold: { minDecisions: 12 },
        retryLimit: 3
      },
      gate2_decomposition: {
        name: '拆解质量',
        threshold: { 
          userStoryFormat: 100, 
          acFormat: 100,
          businessRulesMin: 3  // 新增：每个功能至少 3 条业务规则
        },
        retryLimit: 3
      },
      gate3_prd: {
        name: 'PRD 质量',
        threshold: { 
          chaptersComplete: 100,
          specDesignComplete: true  // 新增：规格设计完整性
        },
        retryLimit: 3
      },
      gate4_review: {
        name: '评审质量',
        threshold: { overallScore: 80 },
        retryLimit: 3
      },
      // ... 其他门禁保持不变
    };
  }
  
  /**
   * 执行门禁检查
   */
  async pass(gateName, data) {
    const gate = this.gates[gateName];
    
    if (!gate) {
      throw new Error(`未知门禁：${gateName}`);
    }
    
    console.log(`\n🔒 门禁检查：${gate.name}`);
    
    const result = await this.check(gateName, data);
    
    if (result.passed) {
      console.log(`✅ 门禁通过：${gate.name}`);
      return result;
    }
    
    console.warn(`⚠️  门禁未通过：${gate.name}`);
    console.warn(`   问题：${result.errors.join(', ')}`);
    
    return result;
  }
  
  /**
   * 检查逻辑 v2.6.0
   */
  async check(gateName, data) {
    const errors = [];
    
    switch (gateName) {
      case 'gate1_interview':
        if (!data.keyDecisions || data.keyDecisions.length < 12) {
          errors.push(`关键决策数量不足：${data.keyDecisions?.length || 0} < 12`);
        }
        break;
        
      case 'gate2_decomposition':
        // 1. 形式检查（保留）
        if (data.userStories) {
          const invalidStories = data.userStories.filter(s => {
            const sText = typeof s === 'string' ? s : (s.content || '');
            return !sText.includes('As a') || !sText.includes('I want') || !sText.includes('So that');
          });
          if (invalidStories.length > 0) {
            errors.push(`用户故事格式错误：${invalidStories.length} 个`);
          }
        }
        
        // 2. 内容检查（新增）
        if (data.features) {
          data.features.forEach(f => {
            // 检查业务规则数量
            if (!f.businessRules || f.businessRules.length < 3) {
              errors.push(`${f.name}: 业务规则不足 3 条`);
            }
            
            // 检查约束条件
            if (!f.constraints || 
                (!f.constraints.business && !f.constraints.technical && !f.constraints.compliance)) {
              errors.push(`${f.name}: 缺少约束条件`);
            }
          });
        }
        
        // 3. 检查报告生成
        if (!data.reportGenerated && !data.businessReportPath) {
          errors.push('需求分析报告未生成');
        }
        break;
        
      case 'gate3_prd':
        // 1. 章节完整性检查
        if (!data.chapters || data.chapters.length < 9) {
          errors.push(`章节不完整：${data.chapters?.length || 0} < 9`);
        }
        
        // 2. 规格设计检查（新增）
        if (data.features) {
          data.features.forEach(f => {
            // 检查输入输出定义
            if (!f.inputs || f.inputs.length === 0) {
              errors.push(`${f.name}: 缺少输入定义`);
            }
            if (!f.outputs || f.outputs.length === 0) {
              errors.push(`${f.name}: 缺少输出定义`);
            }
            
            // 检查异常处理
            if (!f.exceptions || f.exceptions.length < 2) {
              errors.push(`${f.name}: 异常处理不足 2 个`);
            }
          });
        }
        break;
        
      case 'gate4_review':
        if (data.overall !== undefined && data.overall < 80) {
          errors.push(`评审评分不足：${data.overall} < 80`);
        }
        break;
        
      // ... 其他门禁保持不变
    }
    
    return {
      passed: errors.length === 0,
      errors: errors
    };
  }
}

module.exports = { QualityGate };
