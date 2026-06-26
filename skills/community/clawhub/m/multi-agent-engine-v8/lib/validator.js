/**
 * 验证器 - 检查子代理产出是否符合目标要求
 * 支持多种验证规则和自定义标准
 */

// 验证规则类型
export const ValidationRuleType = {
  COMPLETENESS: 'completeness',      // 完整性检查
  RELEVANCE: 'relevance',            // 相关性检查
  QUALITY: 'quality',                // 质量检查
  FORMAT: 'format',                  // 格式检查
  CONSISTENCY: 'consistency',        // 一致性检查
  DEPTH: 'depth',                    // 深度检查
  EVIDENCE: 'evidence',              // 证据支持检查
  CUSTOM: 'custom'                   // 自定义规则
};

// 验证结果
export const ValidationResult = {
  PASS: 'pass',
  FAIL: 'fail',
  WARNING: 'warning',
  NEEDS_REVIEW: 'needs_review'
};

/**
 * 预设验证规则集
 */
export const VALIDATION_RULESETS = {
  // 标准研究产出验证
  research_output: {
    name: '研究产出验证',
    rules: [
      {
        type: ValidationRuleType.COMPLETENESS,
        name: '内容完整性',
        check: 'result must contain at least 500 words',
        weight: 0.25
      },
      {
        type: ValidationRuleType.RELEVANCE,
        name: '目标相关性',
        check: 'content must directly address the assigned task',
        weight: 0.25
      },
      {
        type: ValidationRuleType.EVIDENCE,
        name: '证据支持',
        check: 'claims must be supported by data or references',
        weight: 0.20
      },
      {
        type: ValidationRuleType.DEPTH,
        name: '分析深度',
        check: 'analysis must go beyond surface-level observations',
        weight: 0.15
      },
      {
        type: ValidationRuleType.FORMAT,
        name: '格式规范',
        check: 'output must follow the specified format',
        weight: 0.15
      }
    ],
    pass_threshold: 0.7
  },

  // 技术方案验证
  technical_output: {
    name: '技术方案验证',
    rules: [
      {
        type: ValidationRuleType.COMPLETENESS,
        name: '方案完整性',
        check: 'must include architecture, implementation, and risks',
        weight: 0.30
      },
      {
        type: ValidationRuleType.QUALITY,
        name: '技术质量',
        check: 'solution must be technically sound and feasible',
        weight: 0.30
      },
      {
        type: ValidationRuleType.CONSISTENCY,
        name: '内部一致性',
        check: 'no contradictions within the proposal',
        weight: 0.20
      },
      {
        type: ValidationRuleType.EVIDENCE,
        name: '技术依据',
        check: 'decisions must reference established patterns or benchmarks',
        weight: 0.20
      }
    ],
    pass_threshold: 0.75
  },

  // 批判性审核验证
  critical_review: {
    name: '批判性审核验证',
    rules: [
      {
        type: ValidationRuleType.COMPLETENESS,
        name: '维度覆盖',
        check: 'must evaluate at least 3 dimensions',
        weight: 0.25
      },
      {
        type: ValidationRuleType.DEPTH,
        name: '批判深度',
        check: 'must identify specific weaknesses with reasoning',
        weight: 0.30
      },
      {
        type: ValidationRuleType.QUALITY,
        name: '建议质量',
        check: 'must provide actionable improvement suggestions',
        weight: 0.25
      },
      {
        type: ValidationRuleType.CONSISTENCY,
        name: '评判一致性',
        check: 'scores must align with textual assessment',
        weight: 0.20
      }
    ],
    pass_threshold: 0.7
  }
};

/**
 * 执行验证
 */
export function validate(result, rulesetName, context = {}) {
  const ruleset = VALIDATION_RULESETS[rulesetName];
  if (!ruleset) {
    throw new Error(`未知验证规则集: ${rulesetName}`);
  }

  const checks = [];
  let totalScore = 0;
  let totalWeight = 0;

  for (const rule of ruleset.rules) {
    const check = executeRule(rule, result, context);
    checks.push(check);
    totalScore += check.score * rule.weight;
    totalWeight += rule.weight;
  }

  const finalScore = totalWeight > 0 ? totalScore / totalWeight : 0;
  const passed = finalScore >= ruleset.pass_threshold;

  return {
    ruleset: rulesetName,
    passed,
    score: Math.round(finalScore * 100) / 100,
    threshold: ruleset.pass_threshold,
    checks,
    recommendation: passed ? 
      '产出符合要求，可以进入下一阶段' : 
      `产出未达到标准 (${Math.round(finalScore * 100)}% < ${Math.round(ruleset.pass_threshold * 100)}%)，需要返工`,
    failed_rules: checks.filter(c => c.result === ValidationResult.FAIL).map(c => c.rule_name),
    timestamp: new Date().toISOString()
  };
}

/**
 * 执行单条规则检查
 */
function executeRule(rule, result, context) {
  // 这里是简化的规则执行逻辑
  // 实际使用时由主代理根据规则描述进行判断
  
  const resultText = typeof result === 'string' ? result : JSON.stringify(result);
  let score = 0;
  let resultStatus = ValidationResult.NEEDS_REVIEW;
  let detail = '';

  switch (rule.type) {
    case ValidationRuleType.COMPLETENESS:
      // 检查内容长度
      if (resultText.length > 2000) {
        score = 1.0;
        resultStatus = ValidationResult.PASS;
        detail = '内容充分';
      } else if (resultText.length > 500) {
        score = 0.7;
        resultStatus = ValidationResult.WARNING;
        detail = '内容基本完整，但可以更详细';
      } else {
        score = 0.3;
        resultStatus = ValidationResult.FAIL;
        detail = '内容过于简短';
      }
      break;

    case ValidationRuleType.RELEVANCE:
      // 由上下文判断相关性
      if (context.goal) {
        const goalWords = context.goal.toLowerCase().split(/\s+/);
        const resultLower = resultText.toLowerCase();
        const matchCount = goalWords.filter(w => resultLower.includes(w)).length;
        score = Math.min(1, matchCount / Math.max(1, goalWords.length * 0.5));
        resultStatus = score >= 0.7 ? ValidationResult.PASS : 
                       score >= 0.4 ? ValidationResult.WARNING : ValidationResult.FAIL;
        detail = `目标关键词匹配度: ${Math.round(score * 100)}%`;
      } else {
        score = 0.5;
        resultStatus = ValidationResult.NEEDS_REVIEW;
        detail = '无法判断相关性（缺少目标上下文）';
      }
      break;

    case ValidationRuleType.EVIDENCE:
      // 检查是否有数据/引用支撑
      const hasNumbers = /\d+%|\d+\.\d+|数据|研究|报告|调查|分析/g.test(resultText);
      const hasReferences = /引用|参考|来源|据.*报道|根据.*显示/g.test(resultText);
      if (hasNumbers && hasReferences) {
        score = 1.0;
        resultStatus = ValidationResult.PASS;
        detail = '有充分的数据和引用支撑';
      } else if (hasNumbers || hasReferences) {
        score = 0.6;
        resultStatus = ValidationResult.WARNING;
        detail = '有一定支撑，但不够充分';
      } else {
        score = 0.2;
        resultStatus = ValidationResult.FAIL;
        detail = '缺乏数据和引用支撑';
      }
      break;

    case ValidationRuleType.FORMAT:
      // 检查格式规范
      const hasStructure = /#{1,3}\s|^\d+\.|^[*-]\s/m.test(resultText);
      if (hasStructure) {
        score = 1.0;
        resultStatus = ValidationResult.PASS;
        detail = '格式规范';
      } else {
        score = 0.5;
        resultStatus = ValidationResult.WARNING;
        detail = '缺少结构化格式';
      }
      break;

    case ValidationRuleType.DEPTH:
      // 检查分析深度：是否有分章节、多角度分析
      const sections = (resultText.match(/^#{1,3}\s/gm) || []).length;
      const hasAnalysis = /分析|评估|比较|原因|影响/g.test(resultText);
      if (sections >= 3 && hasAnalysis) {
        score = 1.0;
        resultStatus = ValidationResult.PASS;
        detail = `深度充分（${sections}个章节，含分析内容）`;
      } else if (sections >= 2 || hasAnalysis) {
        score = 0.6;
        resultStatus = ValidationResult.WARNING;
        detail = '深度一般，可扩展更多维度';
      } else {
        score = 0.2;
        resultStatus = ValidationResult.FAIL;
        detail = '分析过于表面';
      }
      break;

    default:
      score = 0.5;
      resultStatus = ValidationResult.NEEDS_REVIEW;
      detail = `规则 ${rule.type} 需要人工判断`;
  }

  return {
    rule_name: rule.name,
    rule_type: rule.type,
    result: resultStatus,
    score,
    detail,
    check_description: rule.check
  };
}

/**
 * 生成验证报告
 */
export function formatValidationReport(validationResult) {
  let report = `📋 验证报告: ${validationResult.ruleset}\n`;
  report += `${'─'.repeat(50)}\n`;
  report += `📊 综合评分: ${Math.round(validationResult.score * 100)}% `;
  report += `(阈值: ${Math.round(validationResult.threshold * 100)}%)\n`;
  report += `🎯 结果: ${validationResult.passed ? '✅ 通过' : '❌ 未通过'}\n\n`;

  report += `📝 各项检查:\n`;
  for (const check of validationResult.checks) {
    const icon = check.result === ValidationResult.PASS ? '✅' :
                 check.result === ValidationResult.WARNING ? '⚠️' :
                 check.result === ValidationResult.FAIL ? '❌' : '🔍';
    report += `  ${icon} ${check.rule_name}: ${Math.round(check.score * 100)}% - ${check.detail}\n`;
  }

  report += `\n💡 建议: ${validationResult.recommendation}\n`;

  if (validationResult.failed_rules.length > 0) {
    report += `\n❌ 未达标项: ${validationResult.failed_rules.join(', ')}\n`;
  }

  return report;
}
