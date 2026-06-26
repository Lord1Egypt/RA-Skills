/**
 * Fallback 预设模板模块 - v8.0 第二阶段
 * 
 * 功能：
 * 1. 各代理类型的预设兜底模板
 * 2. 部分成功的聚合模板
 * 3. 错误恢复策略配置
 * 4. 用户可控的失败处理
 * 
 * 目的：解决GPT评价指出的"缺乏失败边界"问题
 */

// ===== Fallback模板定义 =====

/**
 * 各代理类型的预设兜底模板
 */
export const FALLBACK_TEMPLATES = {
  // 研究代理兜底
  research: {
    complete: {
      findings: ['[系统兜底] 数据不足，需人工复核'],
      analysis: '[自动生成] 研究任务未能完成，建议重新执行或人工干预',
      conclusion: '系统降级输出，质量不可靠',
      sources: [],
      confidence: 'low',
      _meta: {
        fallback: true,
        reason: '代理执行失败',
        timestamp: new Date().toISOString()
      }
    },
    
    partial: {
      findings: ['[部分完成] 已完成部分研究'],
      analysis: '[部分数据] 分析过程不完整',
      conclusion: '结果不完整，需补充',
      sources: ['待补充'],
      confidence: 'low',
      _meta: {
        fallback: true,
        type: 'partial',
        timestamp: new Date().toISOString()
      }
    }
  },
  
  // Critic代理兜底
  critic: {
    complete: {
      issues: ['[系统兜底] 未完成审核'],
      strengths: [],
      improvements: ['需人工复核所有产出'],
      verdict: 'conditional',
      score: 50,
      _meta: {
        fallback: true,
        reason: 'Critic代理执行失败',
        timestamp: new Date().toISOString()
      }
    },
    
    partial: {
      issues: ['[部分审核] 已审核部分内容'],
      strengths: ['部分产出质量可接受'],
      improvements: ['需补充完整审核'],
      verdict: 'conditional',
      score: 60,
      _meta: {
        fallback: true,
        type: 'partial',
        timestamp: new Date().toISOString()
      }
    }
  },
  
  // 技术代理兜底
  tech: {
    complete: {
      approach: '[系统兜底] 技术分析未能完成',
      implementation: ['需人工重新评估'],
      risks: ['技术风险未识别'],
      recommendation: '建议暂停执行，人工介入',
      _meta: {
        fallback: true,
        reason: '技术代理执行失败',
        timestamp: new Date().toISOString()
      }
    },
    
    partial: {
      approach: '[部分完成] 技术方案部分生成',
      implementation: ['部分步骤已定义'],
      risks: ['部分风险已识别'],
      recommendation: '可继续执行，但需补充',
      _meta: {
        fallback: true,
        type: 'partial',
        timestamp: new Date().toISOString()
      }
    }
  },
  
  // 策略代理兜底
  strategy: {
    complete: {
      insights: ['[系统兜底] 战略分析未能完成'],
      scenarios: ['需人工重新规划'],
      actions: ['暂停策略执行'],
      rationale: '代理失败，需人工介入',
      _meta: {
        fallback: true,
        reason: '策略代理执行失败',
        timestamp: new Date().toISOString()
      }
    },
    
    partial: {
      insights: ['[部分完成] 已完成部分战略分析'],
      scenarios: ['部分场景已分析'],
      actions: ['可执行部分行动'],
      rationale: '结果不完整，需补充',
      _meta: {
        fallback: true,
        type: 'partial',
        timestamp: new Date().toISOString()
      }
    }
  }
};

// ===== 失败策略配置 =====

/**
 * 失败处理策略（用户可控）
 */
export const FAILURE_STRATEGIES = {
  // 默认策略：重试
  retry: {
    name: '重试',
    description: '重新调用失败的代理（最多2次）',
    maxRetries: 2,
    timeoutMultiplier: 1.5,
    modelSwitch: true, // 重试时切换模型
    applicable: ['timeout', 'invalid_output', 'partial_failure'],
    userControlled: true
  },
  
  // 跳过策略
  skip: {
    name: '跳过',
    description: '跳过失败的代理，继续执行其他代理',
    maxRetries: 0,
    timeoutMultiplier: 1,
    modelSwitch: false,
    applicable: ['non_critical_agent', 'parallel_phase'],
    userControlled: true
  },
  
  // 兜底策略
  fallback: {
    name: '兜底',
    description: '使用预设模板结果，继续流程',
    maxRetries: 0,
    timeoutMultiplier: 1,
    modelSwitch: false,
    applicable: ['critical_agent', 'single_agent'],
    templateProvider: (agentName) => getFallbackTemplate(agentName, 'complete'),
    userControlled: true
  },
  
  // 部分成功策略
  partial: {
    name: '部分',
    description: '使用部分成功的结果，继续聚合',
    maxRetries: 0,
    timeoutMultiplier: 1,
    modelSwitch: false,
    applicable: ['partial_output', 'quality_below_threshold'],
    templateProvider: (agentName) => getFallbackTemplate(agentName, 'partial'),
    userControlled: true
  },
  
  // 人工介入策略
  manual: {
    name: '人工介入',
    description: '暂停执行，等待人工确认',
    maxRetries: 0,
    timeoutMultiplier: 0,
    modelSwitch: false,
    applicable: ['critical_failure', 'quality_critical'],
    userControlled: true,
    requiresUserAction: true
  }
};

// ===== 获取Fallback模板 =====

/**
 * 根据代理类型获取Fallback模板
 * 
 * @param {string} agentName - 代理名称
 * @param {string} type - 模板类型 ('complete' | 'partial')
 * @returns {object} Fallback模板
 */
export function getFallbackTemplate(agentName, type = 'complete') {
  const nameLC = agentName.toLowerCase();
  
  // 匹配代理类型
  let templateType = 'research'; // 默认
  
  if (nameLC.includes('research') || nameLC.includes('analyst')) {
    templateType = 'research';
  } else if (nameLC.includes('critic') || nameLC.includes('review')) {
    templateType = 'critic';
  } else if (nameLC.includes('tech') || nameLC.includes('technical')) {
    templateType = 'tech';
  } else if (nameLC.includes('strategy')) {
    templateType = 'strategy';
  }
  
  const templates = FALLBACK_TEMPLATES[templateType];
  return templates[type] || templates.complete;
}

// ===== 错误恢复策略选择 =====

/**
 * 根据错误类型选择恢复策略
 * 
 * @param {object} errorInfo - 错误信息
 * @param {object} options - 用户配置选项
 * @returns {object} 恢复策略
 */
export function selectRecoveryStrategy(errorInfo, options = {}) {
  const { errorType, agentName, phaseType, retryCount } = errorInfo;
  
  // 用户配置覆盖（最高优先级）
  if (options.userStrategy && FAILURE_STRATEGIES[options.userStrategy]) {
    return {
      strategy: FAILURE_STRATEGIES[options.userStrategy],
      reason: '用户指定策略',
      userControlled: true
    };
  }
  
  // 自动策略选择（基于规则）
  const rules = [
    // 规则1：超时错误 → 重试（如果未超过最大次数）
    {
      condition: errorType === 'timeout' && retryCount < 2,
      strategy: 'retry',
      reason: '超时，尝试重试'
    },
    
    // 规则2：输出无效 → 兜底
    {
      condition: errorType === 'invalid_output',
      strategy: 'fallback',
      reason: '输出格式无效，使用兜底模板'
    },
    
    // 规则3：Critic失败 → 必须兜底
    {
      condition: agentName.toLowerCase().includes('critic') && errorType !== 'success',
      strategy: 'fallback',
      reason: 'Critic代理失败，使用兜底审核'
    },
    
    // 规则4：并行阶段单代理失败 → 跳过
    {
      condition: phaseType === 'parallel' && retryCount >= 2,
      strategy: 'skip',
      reason: '并行阶段，允许跳过失败代理'
    },
    
    // 规则5：部分成功 → 继续
    {
      condition: errorType === 'partial_failure',
      strategy: 'partial',
      reason: '部分成功，继续聚合'
    },
    
    // 规则6：重试次数用尽 → 兜底
    {
      condition: retryCount >= 2,
      strategy: 'fallback',
      reason: '重试次数用尽，使用兜底'
    },
    
    // 默认规则：重试
    {
      condition: true,
      strategy: 'retry',
      reason: '默认策略'
    }
  ];
  
  // 匹配规则
  for (const rule of rules) {
    if (rule.condition) {
      return {
        strategy: FAILURE_STRATEGIES[rule.strategy],
        reason: rule.reason,
        matchedRule: rule,
        userControlled: false
      };
    }
  }
  
  // 兜底返回
  return {
    strategy: FAILURE_STRATEGIES.fallback,
    reason: '无法匹配规则，使用兜底',
    userControlled: false
  };
}

// ===== 失败边界处理 =====

/**
 * 失败边界处理器
 * 
 * @param {object} validationResult - 校验结果
 * @param {object} agentProfile - 代理配置
 * @param {object} options - 处理选项
 * @returns {object} 处理结果 { action, template, shouldContinue }
 */
export function handleFailureBoundary(validationResult, agentProfile, options = {}) {
  const { valid, errors, action, score } = validationResult;
  
  // 成功 → 继续
  if (valid && action === 'pass') {
    return {
      action: 'continue',
      template: null,
      shouldContinue: true,
      message: '校验通过，继续执行'
    };
  }
  
  // 需要审核 → 人工确认
  if (action === 'review' && score < 70) {
    return {
      action: 'review',
      template: null,
      shouldContinue: false,
      message: `质量评分 ${score}，需人工审核`,
      requiresUserAction: true
    };
  }
  
  // 失败 → 选择恢复策略
  const errorInfo = {
    errorType: errors.length > 0 ? 'invalid_output' : 'quality_failure',
    agentName: agentProfile.name,
    phaseType: options.phaseType || 'unknown',
    retryCount: options.retryCount || 0
  };
  
  const recovery = selectRecoveryStrategy(errorInfo, options);
  
  // 生成Fallback模板
  const fallbackType = recovery.strategy.name === 'partial' ? 'partial' : 'complete';
  const template = recovery.strategy.templateProvider 
    ? recovery.strategy.templateProvider(agentProfile.name)
    : getFallbackTemplate(agentProfile.name, fallbackType);
  
  return {
    action: recovery.strategy.name,
    strategy: recovery.strategy,
    template: template,
    shouldContinue: recovery.strategy.name !== 'manual',
    message: recovery.reason,
    maxRetries: recovery.strategy.maxRetries,
    userControlled: recovery.userControlled
  };
}

// ===== 聚合Fallback =====

/**
 * 多代理失败后的聚合Fallback
 * 
 * @param {array} agentResults - 各代理结果（含失败）
 * @param {object} workflow - 工作流配置
 * @returns {object} 聚合结果
 */
export function aggregateWithFallbacks(agentResults, workflow) {
  const successful = agentResults.filter(r => r.status === 'success');
  const failed = agentResults.filter(r => r.status !== 'success');
  
  // 全部成功 → 正常聚合
  if (failed.length === 0) {
    return {
      type: 'full',
      results: successful.map(r => r.output),
      message: '全部代理成功',
      quality: 'high'
    };
  }
  
  // 部分失败 → 混合聚合
  if (successful.length > 0 && failed.length > 0) {
    const fallbackOutputs = failed.map(f => 
      getFallbackTemplate(f.agentName, 'partial')
    );
    
    return {
      type: 'partial',
      results: [...successful.map(r => r.output), ...fallbackOutputs],
      message: `部分成功 (${successful.length}/${agentResults.length})`,
      quality: 'medium',
      warnings: failed.map(f => `${f.agentName}: ${f.error}`),
      _meta: {
        fallbackCount: failed.length,
        needsReview: true
      }
    };
  }
  
  // 全部失败 → 兜底聚合
  return {
    type: 'fallback',
    results: agentResults.map(r => getFallbackTemplate(r.agentName, 'complete')),
    message: '全部失败，使用兜底模板',
    quality: 'low',
    errors: agentResults.map(r => `${r.agentName}: ${r.error}`),
    _meta: {
      allFallback: true,
      needsManualIntervention: true
    }
  };
}

// ===== 导出 =====

export default {
  FALLBACK_TEMPLATES,
  FAILURE_STRATEGIES,
  getFallbackTemplate,
  selectRecoveryStrategy,
  handleFailureBoundary,
  aggregateWithFallbacks
};