/**
 * 需求分解数据结构定义
 * 
 * 定义需求分解阶段的数据结构和验证规则
 * 
 * @version 1.0.0
 * @since 2026-04-05
 */

/**
 * 功能模块数据结构
 * @typedef {Object} FunctionModule
 * @property {string} id - 模块唯一标识
 * @property {string} name - 模块名称
 * @property {string} description - 模块描述
 * @property {string} priority - 优先级 (P0/P1/P2)
 * @property {Array<string>} inputs - 输入列表
 * @property {Array<string>} outputs - 输出列表
 * @property {Array<string>} businessRules - 业务规则列表
 * @property {Array<string>} exceptions - 异常处理列表
 * @property {Array<string>} checkpoints - 检查点列表
 */

/**
 * 需求分解报告数据结构
 * @typedef {Object} DecompositionReport
 * @property {string} projectId - 项目 ID
 * @property {string} projectName - 项目名称
 * @property {string} version - 版本号
 * @property {string} createdAt - 创建时间
 * @property {string} stage - 当前阶段
 * @property {Array<FunctionModule>} modules - 功能模块列表
 * @property {Object} qualityCheck - 质量检查结果
 * @property {Object} statistics - 统计信息
 */

/**
 * 质量检查结果
 * @typedef {Object} QualityCheckResult
 * @property {string} status - 状态 (pass/warning/fail)
 * @property {number} score - 得分 (0-100)
 * @property {Array<Object>} items - 检查项结果列表
 * @property {Array<string>} issues - 问题列表
 * @property {Array<string>} suggestions - 建议列表
 */

/**
 * 检查项结果
 * @typedef {Object} CheckItemResult
 * @property {string} itemId - 检查项 ID
 * @property {string} itemName - 检查项名称
 * @property {string} category - 类别 (CORE/COMPLETE/OPTIMIZE)
 * @property {string} status - 状态 (pass/warning/fail)
 * @property {number} score - 得分
 * @property {Array<string>} evidence - 证据列表
 * @property {string} comment - 评语
 */

/**
 * 统计信息
 * @typedef {Object} Statistics
 * @property {number} totalModules - 总模块数
 * @property {number} totalRules - 总规则数
 * @property {number} totalExceptions - 总异常数
 * @property {number} coverage - 覆盖率
 * @property {Object} byPriority - 按优先级统计
 */

module.exports = {
  /**
   * 创建功能模块
   * @param {Object} data - 模块数据
   * @returns {FunctionModule} 功能模块对象
   */
  createFunctionModule(data) {
    return {
      id: data.id || `MOD-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      name: data.name || '未命名模块',
      description: data.description || '',
      priority: data.priority || 'P2',
      inputs: data.inputs || [],
      outputs: data.outputs || [],
      businessRules: data.businessRules || [],
      exceptions: data.exceptions || [],
      checkpoints: data.checkpoints || []
    };
  },

  /**
   * 创建需求分解报告
   * @param {Object} data - 报告数据
   * @returns {DecompositionReport} 需求分解报告对象
   */
  createDecompositionReport(data) {
    return {
      projectId: data.projectId || '',
      projectName: data.projectName || '',
      version: data.version || '1.0.0',
      createdAt: data.createdAt || new Date().toISOString(),
      stage: data.stage || 'decomposition',
      modules: data.modules || [],
      qualityCheck: data.qualityCheck || this.createQualityCheckResult(),
      statistics: data.statistics || this.createStatistics()
    };
  },

  /**
   * 创建质量检查结果
   * @param {Object} data - 检查结果数据
   * @returns {QualityCheckResult} 质量检查结果对象
   */
  createQualityCheckResult(data) {
    return {
      status: data?.status || 'pending',
      score: data?.score || 0,
      items: data?.items || [],
      issues: data?.issues || [],
      suggestions: data?.suggestions || []
    };
  },

  /**
   * 创建检查项结果
   * @param {Object} data - 检查项结果数据
   * @returns {CheckItemResult} 检查项结果对象
   */
  createCheckItemResult(data) {
    return {
      itemId: data?.itemId || '',
      itemName: data?.itemName || '',
      category: data?.category || 'CORE',
      status: data?.status || 'pending',
      score: data?.score || 0,
      evidence: data?.evidence || [],
      comment: data?.comment || ''
    };
  },

  /**
   * 创建统计信息
   * @param {Object} data - 统计数据
   * @returns {Statistics} 统计信息对象
   */
  createStatistics(data) {
    return {
      totalModules: data?.totalModules || 0,
      totalRules: data?.totalRules || 0,
      totalExceptions: data?.totalExceptions || 0,
      coverage: data?.coverage || 0,
      byPriority: data?.byPriority || {
        P0: 0,
        P1: 0,
        P2: 0
      }
    };
  },

  /**
   * 验证功能模块
   * @param {FunctionModule} module - 功能模块
   * @returns {Object} 验证结果
   */
  validateFunctionModule(module) {
    const errors = [];
    const warnings = [];

    if (!module.name || module.name.trim() === '') {
      errors.push('模块名称不能为空');
    }

    if (!module.description || module.description.trim() === '') {
      warnings.push('建议添加模块描述');
    }

    if (!['P0', 'P1', 'P2'].includes(module.priority)) {
      errors.push(`优先级必须是 P0/P1/P2，当前为：${module.priority}`);
    }

    if (!module.inputs || module.inputs.length === 0) {
      warnings.push('建议定义模块的输入');
    }

    if (!module.outputs || module.outputs.length === 0) {
      warnings.push('建议定义模块的输出');
    }

    if (!module.businessRules || module.businessRules.length === 0) {
      errors.push('业务规则不能为空（CORE-1）');
    }

    return {
      valid: errors.length === 0,
      errors,
      warnings
    };
  },

  /**
   * 验证需求分解报告
   * @param {DecompositionReport} report - 需求分解报告
   * @returns {Object} 验证结果
   */
  validateDecompositionReport(report) {
    const errors = [];
    const warnings = [];

    if (!report.projectId || report.projectId.trim() === '') {
      errors.push('项目 ID 不能为空');
    }

    if (!report.projectName || report.projectName.trim() === '') {
      errors.push('项目名称不能为空');
    }

    if (!report.modules || report.modules.length === 0) {
      errors.push('功能模块列表不能为空');
    }

    // 验证每个模块
    if (report.modules && report.modules.length > 0) {
      report.modules.forEach((module, index) => {
        const moduleValidation = this.validateFunctionModule(module);
        if (!moduleValidation.valid) {
          errors.push(`模块 [${index + 1}] ${module.name}: ${moduleValidation.errors.join(', ')}`);
        }
        moduleValidation.warnings.forEach(warning => {
          warnings.push(`模块 [${index + 1}] ${module.name}: ${warning}`);
        });
      });
    }

    return {
      valid: errors.length === 0,
      errors,
      warnings
    };
  },

  /**
   * 计算统计信息
   * @param {DecompositionReport} report - 需求分解报告
   * @returns {Statistics} 统计信息
   */
  calculateStatistics(report) {
    const stats = {
      totalModules: report.modules?.length || 0,
      totalRules: 0,
      totalExceptions: 0,
      coverage: 0,
      byPriority: {
        P0: 0,
        P1: 0,
        P2: 0
      }
    };

    if (report.modules) {
      report.modules.forEach(module => {
        // 统计规则数
        stats.totalRules += module.businessRules?.length || 0;
        
        // 统计异常数
        stats.totalExceptions += module.exceptions?.length || 0;
        
        // 统计优先级
        if (stats.byPriority.hasOwnProperty(module.priority)) {
          stats.byPriority[module.priority]++;
        }
      });

      // 计算覆盖率（有规则和异常的模块比例）
      const coveredModules = report.modules.filter(
        m => (m.businessRules?.length > 0) && (m.exceptions?.length > 0)
      ).length;
      
      stats.coverage = stats.totalModules > 0 
        ? Math.round((coveredModules / stats.totalModules) * 100) 
        : 0;
    }

    return stats;
  },

  /**
   * 将报告转换为 Markdown
   * @param {DecompositionReport} report - 需求分解报告
   * @returns {string} Markdown 字符串
   */
  toMarkdown(report) {
    let md = `# 需求分解报告\n\n`;
    md += `**项目名称**: ${report.projectName}\n`;
    md += `**项目 ID**: ${report.projectId}\n`;
    md += `**版本**: ${report.version}\n`;
    md += `**创建时间**: ${report.createdAt}\n`;
    md += `**当前阶段**: ${report.stage}\n\n`;

    md += `---\n\n`;

    md += `## 统计信息\n\n`;
    const stats = report.statistics || this.calculateStatistics(report);
    md += `- 总模块数：${stats.totalModules}\n`;
    md += `- 总业务规则数：${stats.totalRules}\n`;
    md += `- 总异常处理数：${stats.totalExceptions}\n`;
    md += `- 覆盖率：${stats.coverage}%\n`;
    md += `- 优先级分布：P0=${stats.byPriority.P0}, P1=${stats.byPriority.P1}, P2=${stats.byPriority.P2}\n\n`;

    md += `---\n\n`;

    md += `## 功能模块列表\n\n`;
    
    if (report.modules && report.modules.length > 0) {
      report.modules.forEach((module, index) => {
        md += `### ${index + 1}. ${module.name} (${module.priority})\n\n`;
        md += `${module.description}\n\n`;

        if (module.inputs && module.inputs.length > 0) {
          md += `**输入**:\n`;
          module.inputs.forEach(input => {
            md += `- ${input}\n`;
          });
          md += `\n`;
        }

        if (module.outputs && module.outputs.length > 0) {
          md += `**输出**:\n`;
          module.outputs.forEach(output => {
            md += `- ${output}\n`;
          });
          md += `\n`;
        }

        if (module.businessRules && module.businessRules.length > 0) {
          md += `**业务规则**:\n`;
          module.businessRules.forEach(rule => {
            md += `- ${rule}\n`;
          });
          md += `\n`;
        }

        if (module.exceptions && module.exceptions.length > 0) {
          md += `**异常处理**:\n`;
          module.exceptions.forEach(exception => {
            md += `- ${exception}\n`;
          });
          md += `\n`;
        }

        md += `---\n\n`;
      });
    } else {
      md += `*暂无功能模块*\n\n`;
    }

    // 质量检查结果
    if (report.qualityCheck && report.qualityCheck.status !== 'pending') {
      md += `## 质量检查结果\n\n`;
      md += `**状态**: ${this.getStatusText(report.qualityCheck.status)}\n`;
      md += `**得分**: ${report.qualityCheck.score}/100\n\n`;

      if (report.qualityCheck.issues && report.qualityCheck.issues.length > 0) {
        md += `**问题列表**:\n`;
        report.qualityCheck.issues.forEach(issue => {
          md += `- ${issue}\n`;
        });
        md += `\n`;
      }

      if (report.qualityCheck.suggestions && report.qualityCheck.suggestions.length > 0) {
        md += `**改进建议**:\n`;
        report.qualityCheck.suggestions.forEach(suggestion => {
          md += `- ${suggestion}\n`;
        });
        md += `\n`;
      }
    }

    return md;
  },

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
};
