/**
 * 需求分解业务报告生成器
 * 
 * 基于检查项生成业务分析报告，提供质量评估和改进建议
 * 
 * @version 1.0.0
 * @since 2026-04-05
 */

const schema = require('./decomposition_schema.js');
const checkItemsLoader = require('./check_items_loader.js');

class DecompositionReportGenerator {
  /**
   * 构造函数
   * @param {Object} options - 配置选项
   */
  constructor(options = {}) {
    this.options = {
      includeSuggestions: options.includeSuggestions !== false,
      includeEvidence: options.includeEvidence !== false,
      minScoreForPass: options.minScoreForPass || 80,
      ...options
    };
  }

  /**
   * 生成业务报告
   * @param {Object} decompositionData - 需求分解数据
   * @returns {Promise<Object>} 业务报告
   */
  async generate(decompositionData) {
    const report = {
      summary: await this.generateSummary(decompositionData),
      qualityAssessment: await this.assessQuality(decompositionData),
      moduleAnalysis: this.analyzeModules(decompositionData),
      riskIdentification: this.identifyRisks(decompositionData),
      improvementSuggestions: this.options.includeSuggestions 
        ? await this.generateSuggestions(decompositionData) 
        : [],
      checklist: await this.generateChecklist(decompositionData)
    };

    return report;
  }

  /**
   * 生成报告摘要
   * @param {Object} data - 需求分解数据
   * @returns {Promise<Object>} 摘要信息
   */
  async generateSummary(data) {
    const modules = data.modules || [];
    const stats = schema.calculateStatistics({ modules });

    return {
      projectName: data.projectName || '未命名项目',
      totalModules: stats.totalModules,
      priorityDistribution: stats.byPriority,
      coverage: stats.coverage,
      overallStatus: this.determineOverallStatus(stats),
      generatedAt: new Date().toISOString()
    };
  }

  /**
   * 确定整体状态
   * @param {Object} stats - 统计信息
   * @returns {string} 整体状态
   */
  determineOverallStatus(stats) {
    if (stats.coverage >= 90 && stats.totalRules > 0) {
      return 'excellent';
    } else if (stats.coverage >= 70 && stats.totalRules > 0) {
      return 'good';
    } else if (stats.coverage >= 50) {
      return 'fair';
    } else {
      return 'needs_improvement';
    }
  }

  /**
   * 评估质量
   * @param {Object} data - 需求分解数据
   * @returns {Promise<Object>} 质量评估结果
   */
  async assessQuality(data) {
    const modules = data.modules || [];
    const checkItems = await checkItemsLoader.loadForStage('decomposition');
    
    const assessment = {
      score: 0,
      maxScore: 100,
      status: 'pending',
      coreItemsPassed: 0,
      coreItemsTotal: 0,
      details: []
    };

    // 评估 CORE 检查项
    const coreItems = checkItems.filter(item => item.code === 'CORE');
    assessment.coreItemsTotal = coreItems.length;

    for (const item of coreItems) {
      const itemResult = await this.evaluateCheckItem(item, modules);
      assessment.details.push(itemResult);
      
      if (itemResult.status === 'pass') {
        assessment.coreItemsPassed++;
      }
    }

    // 计算得分
    if (assessment.coreItemsTotal > 0) {
      assessment.score = Math.round(
        (assessment.coreItemsPassed / assessment.coreItemsTotal) * 100
      );
    }

    // 确定状态
    if (assessment.coreItemsPassed === assessment.coreItemsTotal) {
      assessment.status = 'pass';
    } else if (assessment.coreItemsPassed > 0) {
      assessment.status = 'warning';
    } else {
      assessment.status = 'fail';
    }

    return assessment;
  }

  /**
   * 评估单个检查项
   * @param {Object} checkItem - 检查项
   * @param {Array} modules - 模块列表
   * @returns {Promise<Object>} 检查结果
   */
  async evaluateCheckItem(checkItem, modules) {
    const result = {
      itemId: checkItem.id,
      itemName: checkItem.name,
      category: checkItem.category,
      status: 'pending',
      score: 0,
      evidence: [],
      comment: ''
    };

    // 根据检查项类型评估
    switch (checkItem.id) {
      case 'CORE-1': // 业务规则完整性
        result.score = this.evaluateBusinessRulesCompleteness(modules);
        result.evidence = this.collectBusinessRulesEvidence(modules);
        break;
      
      case 'CORE-2': // 输入输出定义
        result.score = this.evaluateInputOutputDefinition(modules);
        result.evidence = this.collectInputOutputEvidence(modules);
        break;
      
      case 'CORE-3': // 异常处理
        result.score = this.evaluateExceptionHandling(modules);
        result.evidence = this.collectExceptionEvidence(modules);
        break;
      
      default:
        result.score = 50;
        result.evidence = ['未实现自动评估'];
    }

    // 确定状态
    if (result.score >= 90) {
      result.status = 'pass';
      result.comment = '完全符合要求';
    } else if (result.score >= 70) {
      result.status = 'warning';
      result.comment = '基本符合，建议改进';
    } else {
      result.status = 'fail';
      result.comment = '不符合要求，需要改进';
    }

    return result;
  }

  /**
   * 评估业务规则完整性
   * @param {Array} modules - 模块列表
   * @returns {number} 得分
   */
  evaluateBusinessRulesCompleteness(modules) {
    if (modules.length === 0) return 0;

    const modulesWithRules = modules.filter(
      m => m.businessRules && m.businessRules.length > 0
    ).length;

    const coverage = (modulesWithRules / modules.length) * 100;
    
    // 检查规则质量
    let qualityBonus = 0;
    modules.forEach(module => {
      if (module.businessRules && module.businessRules.length >= 3) {
        qualityBonus += 5;
      }
    });

    return Math.min(100, coverage + qualityBonus);
  }

  /**
   * 评估输入输出定义
   * @param {Array} modules - 模块列表
   * @returns {number} 得分
   */
  evaluateInputOutputDefinition(modules) {
    if (modules.length === 0) return 0;

    let totalScore = 0;

    modules.forEach(module => {
      const hasInputs = module.inputs && module.inputs.length > 0;
      const hasOutputs = module.outputs && module.outputs.length > 0;
      
      if (hasInputs && hasOutputs) {
        totalScore += 100;
      } else if (hasInputs || hasOutputs) {
        totalScore += 50;
      }
    });

    return Math.round(totalScore / modules.length);
  }

  /**
   * 评估异常处理
   * @param {Array} modules - 模块列表
   * @returns {number} 得分
   */
  evaluateExceptionHandling(modules) {
    if (modules.length === 0) return 0;

    const modulesWithExceptions = modules.filter(
      m => m.exceptions && m.exceptions.length > 0
    ).length;

    const coverage = (modulesWithExceptions / modules.length) * 100;
    
    // 检查异常处理质量
    let qualityBonus = 0;
    modules.forEach(module => {
      if (module.exceptions && module.exceptions.length >= 2) {
        qualityBonus += 5;
      }
    });

    return Math.min(100, coverage + qualityBonus);
  }

  /**
   * 收集业务规则证据
   * @param {Array} modules - 模块列表
   * @returns {Array} 证据列表
   */
  collectBusinessRulesEvidence(modules) {
    const evidence = [];
    
    modules.forEach(module => {
      if (module.businessRules && module.businessRules.length > 0) {
        evidence.push(`✓ ${module.name}: ${module.businessRules.length} 条业务规则`);
      } else {
        evidence.push(`✗ ${module.name}: 缺少业务规则`);
      }
    });

    return evidence;
  }

  /**
   * 收集输入输出证据
   * @param {Array} modules - 模块列表
   * @returns {Array} 证据列表
   */
  collectInputOutputEvidence(modules) {
    const evidence = [];
    
    modules.forEach(module => {
      const inputs = module.inputs?.length || 0;
      const outputs = module.outputs?.length || 0;
      
      if (inputs > 0 && outputs > 0) {
        evidence.push(`✓ ${module.name}: ${inputs} 个输入，${outputs} 个输出`);
      } else if (inputs > 0 || outputs > 0) {
        evidence.push(`⚠ ${module.name}: ${inputs} 个输入，${outputs} 个输出（不完整）`);
      } else {
        evidence.push(`✗ ${module.name}: 缺少输入输出定义`);
      }
    });

    return evidence;
  }

  /**
   * 收集异常处理证据
   * @param {Array} modules - 模块列表
   * @returns {Array} 证据列表
   */
  collectExceptionEvidence(modules) {
    const evidence = [];
    
    modules.forEach(module => {
      if (module.exceptions && module.exceptions.length > 0) {
        evidence.push(`✓ ${module.name}: ${module.exceptions.length} 个异常处理`);
      } else {
        evidence.push(`✗ ${module.name}: 缺少异常处理`);
      }
    });

    return evidence;
  }

  /**
   * 分析模块
   * @param {Object} data - 需求分解数据
   * @returns {Object} 模块分析结果
   */
  analyzeModules(data) {
    const modules = data.modules || [];
    
    return {
      totalModules: modules.length,
      byPriority: {
        P0: modules.filter(m => m.priority === 'P0').length,
        P1: modules.filter(m => m.priority === 'P1').length,
        P2: modules.filter(m => m.priority === 'P2').length
      },
      avgRulesPerModule: modules.length > 0
        ? Math.round(modules.reduce((sum, m) => sum + (m.businessRules?.length || 0), 0) / modules.length)
        : 0,
      avgExceptionsPerModule: modules.length > 0
        ? Math.round(modules.reduce((sum, m) => sum + (m.exceptions?.length || 0), 0) / modules.length)
        : 0,
      modulesNeedingImprovement: modules
        .filter(m => !m.businessRules || m.businessRules.length === 0 || 
                     !m.exceptions || m.exceptions.length === 0)
        .map(m => ({
          id: m.id,
          name: m.name,
          issues: [
            !m.businessRules || m.businessRules.length === 0 ? '缺少业务规则' : null,
            !m.exceptions || m.exceptions.length === 0 ? '缺少异常处理' : null,
            !m.inputs || m.inputs.length === 0 ? '缺少输入定义' : null,
            !m.outputs || m.outputs.length === 0 ? '缺少输出定义' : null
          ].filter(Boolean)
        }))
    };
  }

  /**
   * 识别风险
   * @param {Object} data - 需求分解数据
   * @returns {Array} 风险列表
   */
  identifyRisks(data) {
    const risks = [];
    const modules = data.modules || [];

    // 检查 P0 模块是否有完整的规则和异常处理
    const p0Modules = modules.filter(m => m.priority === 'P0');
    p0Modules.forEach(module => {
      if (!module.businessRules || module.businessRules.length === 0) {
        risks.push({
          level: 'high',
          module: module.name,
          issue: 'P0 模块缺少业务规则',
          impact: '可能导致核心功能逻辑不清晰'
        });
      }
      if (!module.exceptions || module.exceptions.length === 0) {
        risks.push({
          level: 'high',
          module: module.name,
          issue: 'P0 模块缺少异常处理',
          impact: '可能导致系统稳定性问题'
        });
      }
    });

    // 检查覆盖率
    const stats = schema.calculateStatistics({ modules });
    if (stats.coverage < 70) {
      risks.push({
        level: 'medium',
        module: '整体',
        issue: `模块覆盖率较低 (${stats.coverage}%)`,
        impact: '可能遗漏重要功能场景'
      });
    }

    // 检查规则数量
    if (stats.totalRules < modules.length * 2) {
      risks.push({
        level: 'medium',
        module: '整体',
        issue: '平均每个模块的业务规则数少于 2 条',
        impact: '业务逻辑可能不够完善'
      });
    }

    return risks;
  }

  /**
   * 生成改进建议
   * @param {Object} data - 需求分解数据
   * @returns {Promise<Array>} 建议列表
   */
  async generateSuggestions(data) {
    const suggestions = [];
    const modules = data.modules || [];
    const checkItems = await checkItemsLoader.loadForStage('decomposition');

    // 基于检查项生成建议
    for (const item of checkItems) {
      const itemResult = await this.evaluateCheckItem(item, modules);
      
      if (itemResult.status !== 'pass') {
        suggestions.push({
          category: item.category,
          checkItem: item.name,
          priority: item.category === 'CORE' ? 'high' : 'medium',
          suggestion: `改进"${item.name}"：${itemResult.comment}`,
          actions: item.questions?.map(q => `检查：${q}?`) || []
        });
      }
    }

    // 基于风险分析生成建议
    const risks = this.identifyRisks(data);
    risks.forEach(risk => {
      suggestions.push({
        category: 'RISK',
        checkItem: risk.issue,
        priority: risk.level === 'high' ? 'high' : 'medium',
        suggestion: `解决风险：${risk.issue}`,
        actions: [`影响：${risk.impact}`]
      });
    });

    // 按优先级排序
    suggestions.sort((a, b) => {
      const priorityOrder = { high: 0, medium: 1, low: 2 };
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    });

    return suggestions;
  }

  /**
   * 生成检查清单
   * @param {Object} data - 需求分解数据
   * @returns {Promise<Array>} 检查清单
   */
  async generateChecklist(data) {
    const modules = data.modules || [];
    const checkItems = await checkItemsLoader.loadForStage('decomposition');
    
    const checklist = [];

    for (const item of checkItems) {
      const itemResult = await this.evaluateCheckItem(item, modules);
      
      checklist.push({
        itemId: item.id,
        itemName: item.name,
        category: item.category,
        status: itemResult.status === 'pass' ? 'checked' : 'unchecked',
        score: itemResult.score,
        evidence: itemResult.evidence
      });
    }

    return checklist;
  }

  /**
   * 将报告转换为 Markdown
   * @param {Object} report - 业务报告
   * @returns {string} Markdown 字符串
   */
  toMarkdown(report) {
    let md = `# 需求分析业务报告\n\n`;
    md += `**生成时间**: ${report.summary.generatedAt}\n\n`;
    md += `---\n\n`;

    // 摘要
    md += `## 📊 项目摘要\n\n`;
    md += `**项目名称**: ${report.summary.projectName}\n`;
    md += `**模块总数**: ${report.summary.totalModules}\n`;
    md += `**覆盖率**: ${report.summary.coverage}%\n`;
    md += `**整体状态**: ${this.getStatusEmoji(report.summary.overallStatus)}\n\n`;
    
    md += `**优先级分布**:\n`;
    md += `- P0: ${report.summary.priorityDistribution.P0}\n`;
    md += `- P1: ${report.summary.priorityDistribution.P1}\n`;
    md += `- P2: ${report.summary.priorityDistribution.P2}\n\n`;

    // 质量评估
    md += `## 🔍 质量评估\n\n`;
    md += `**得分**: ${report.qualityAssessment.score}/100\n`;
    md += `**状态**: ${this.getStatusText(report.qualityAssessment.status)}\n`;
    md += `**核心检查项**: ${report.qualityAssessment.coreItemsPassed}/${report.qualityAssessment.coreItemsTotal}\n\n`;

    if (report.qualityAssessment.details && report.qualityAssessment.details.length > 0) {
      md += `**详细评估**:\n\n`;
      report.qualityAssessment.details.forEach(detail => {
        md += `- ${detail.itemName}: ${this.getStatusText(detail.status)} (${detail.score}分)\n`;
        if (detail.comment) {
          md += `  - ${detail.comment}\n`;
        }
      });
      md += `\n`;
    }

    // 风险识别
    if (report.riskIdentification && report.riskIdentification.length > 0) {
      md += `## ⚠️ 风险识别\n\n`;
      report.riskIdentification.forEach((risk, index) => {
        md += `${index + 1}. **${risk.level === 'high' ? '🔴' : '🟡'} ${risk.issue}**\n`;
        md += `   - 模块：${risk.module}\n`;
        md += `   - 影响：${risk.impact}\n\n`;
      });
    }

    // 改进建议
    if (report.improvementSuggestions && report.improvementSuggestions.length > 0) {
      md += `## 💡 改进建议\n\n`;
      report.improvementSuggestions.forEach((suggestion, index) => {
        md += `${index + 1}. **${suggestion.suggestion}** [${suggestion.priority === 'high' ? '🔴 高优先级' : '🟡 中优先级'}]\n`;
        if (suggestion.actions && suggestion.actions.length > 0) {
          suggestion.actions.forEach(action => {
            md += `   - ${action}\n`;
          });
        }
        md += `\n`;
      });
    }

    // 检查清单
    if (report.checklist && report.checklist.length > 0) {
      md += `## ✅ 检查清单\n\n`;
      report.checklist.forEach(item => {
        const checkbox = item.status === 'checked' ? '✅' : '❌';
        md += `${checkbox} **${item.itemId}**: ${item.itemName} (${item.score}分)\n`;
        if (item.evidence && item.evidence.length > 0) {
          item.evidence.slice(0, 3).forEach(ev => {
            md += `   - ${ev}\n`;
          });
          if (item.evidence.length > 3) {
            md += `   - ... 还有 ${item.evidence.length - 3} 项\n`;
          }
        }
      });
    }

    return md;
  }

  /**
   * 获取状态文本
   * @param {string} status - 状态代码
   * @returns {string} 状态文本
   */
  getStatusText(status) {
    const statusMap = {
      'pass': '✅ 通过',
      'warning': '⚠️ 警告',
      'fail': '❌ 不通过',
      'pending': '⏳ 待检查'
    };
    return statusMap[status] || status;
  }

  /**
   * 获取状态表情
   * @param {string} status - 状态代码
   * @returns {string} 状态表情
   */
  getStatusEmoji(status) {
    const emojiMap = {
      'excellent': '🌟 优秀',
      'good': '✅ 良好',
      'fair': '⚠️ 一般',
      'needs_improvement': '❌ 需改进'
    };
    return emojiMap[status] || status;
  }
}

module.exports = {
  DecompositionReportGenerator,
  generate: async (data, options) => {
    const generator = new DecompositionReportGenerator(options);
    return await generator.generate(data);
  },
  toMarkdown: (report) => {
    const generator = new DecompositionReportGenerator();
    return generator.toMarkdown(report);
  }
};
