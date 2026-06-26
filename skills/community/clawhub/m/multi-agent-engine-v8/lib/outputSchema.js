/**
 * 统一输出Schema定义 - 强约束JSON输出格式
 * 
 * 目的：
 * 1. 降低tokens消耗（精简提示词）
 * 2. 提升流程遵循性（强约束输出）
 * 3. 简化校验逻辑
 */

// ===== 核心输出Schema =====

/**
 * 研究代理输出Schema
 */
export const RESEARCH_OUTPUT_SCHEMA = {
  type: 'object',
  required: ['findings', 'analysis', 'conclusion', 'sources'],
  properties: {
    findings: {
      type: 'array',
      maxItems: 5,
      description: '核心发现（≤5条，每条≤50字）'
    },
    analysis: {
      type: 'string',
      maxLength: 800,
      description: '详细分析（≤800字）'
    },
    conclusion: {
      type: 'string',
      maxLength: 300,
      description: '结论（≤300字）'
    },
    sources: {
      type: 'array',
      maxItems: 10,
      description: '参考来源（≤10条）'
    },
    confidence: {
      type: 'string',
      enum: ['high', 'medium', 'low'],
      description: '置信度评估'
    }
  }
};

/**
 * 技术代理输出Schema
 */
export const TECH_OUTPUT_SCHEMA = {
  type: 'object',
  required: ['approach', 'implementation', 'risks', 'recommendation'],
  properties: {
    approach: {
      type: 'string',
      maxLength: 500,
      description: '技术方案概述（≤500字）'
    },
    implementation: {
      type: 'array',
      maxItems: 5,
      description: '实施步骤（≤5条）'
    },
    risks: {
      type: 'array',
      maxItems: 5,
      description: '技术风险（≤5条）'
    },
    recommendation: {
      type: 'string',
      maxLength: 200,
      description: '推荐方案（≤200字）'
    }
  }
};

/**
 * Critic代理输出Schema
 */
export const CRITIC_OUTPUT_SCHEMA = {
  type: 'object',
  required: ['issues', 'strengths', 'improvements', 'verdict'],
  properties: {
    issues: {
      type: 'array',
      maxItems: 10,
      description: '发现的问题（≤10条）'
    },
    strengths: {
      type: 'array',
      maxItems: 5,
      description: '优点（≤5条）'
    },
    improvements: {
      type: 'array',
      maxItems: 10,
      description: '改进建议（≤10条）'
    },
    verdict: {
      type: 'string',
      enum: ['pass', 'fail', 'conditional'],
      description: '审核结论'
    },
    score: {
      type: 'number',
      min: 0,
      max: 100,
      description: '质量评分（0-100）'
    }
  }
};

/**
 * 策略代理输出Schema
 */
export const STRATEGY_OUTPUT_SCHEMA = {
  type: 'object',
  required: ['insights', 'scenarios', 'actions', 'rationale'],
  properties: {
    insights: {
      type: 'array',
      maxItems: 5,
      description: '战略洞察（≤5条）'
    },
    scenarios: {
      type: 'array',
      maxItems: 3,
      description: '可能场景（≤3条）'
    },
    actions: {
      type: 'array',
      maxItems: 5,
      description: '行动建议（≤5条）'
    },
    rationale: {
      type: 'string',
      maxLength: 300,
      description: '决策依据（≤300字）'
    }
  }
};

// ===== Schema选择器 =====

/**
 * 根据代理类型选择对应Schema
 */
export function selectSchema(agentName) {
  const schemaMap = {
    'Research_Analyst': RESEARCH_OUTPUT_SCHEMA,
    'Technical_Specialist': TECH_OUTPUT_SCHEMA,
    'Strategy_Analyst': STRATEGY_OUTPUT_SCHEMA,
    'Critic': CRITIC_OUTPUT_SCHEMA
  };
  
  // 匹配代理名称（支持部分匹配）
  for (const [key, schema] of Object.entries(schemaMap)) {
    if (agentName.includes(key) || key.includes(agentName)) {
      return schema;
    }
  }
  
  // 默认返回研究Schema
  return RESEARCH_OUTPUT_SCHEMA;
}

// ===== JSON校验函数 =====

/**
 * 校验JSON输出是否符合Schema
 */
export function validateOutput(output, schema) {
  const errors = [];
  
  // 1. 检查是否为合法JSON
  let parsed;
  try {
    parsed = typeof output === 'string' ? JSON.parse(output) : output;
  } catch (e) {
    return {
      valid: false,
      errors: ['输出不是合法的JSON格式'],
      action: 'retry',
      parsed: null
    };
  }
  
  // 2. 检查必需字段
  for (const field of schema.required) {
    if (!parsed[field]) {
      errors.push(`缺少必需字段: ${field}`);
    }
  }
  
  // 3. 检查字段类型和限制
  for (const [field, props] of Object.entries(schema.properties)) {
    const value = parsed[field];
    
    if (value === undefined || value === null) continue;
    
    // 类型检查
    if (props.type === 'array' && !Array.isArray(value)) {
      errors.push(`字段 ${field} 应为数组`);
    } else if (props.type === 'string' && typeof value !== 'string') {
      errors.push(`字段 ${field} 应为字符串`);
    } else if (props.type === 'number' && typeof value !== 'number') {
      errors.push(`字段 ${field} 应为数字`);
    }
    
    // 数量限制
    if (props.maxItems && Array.isArray(value) && value.length > props.maxItems) {
      errors.push(`字段 ${field} 超过最大数量 ${props.maxItems}（当前 ${value.length}）`);
    }
    
    // 长度限制
    if (props.maxLength && typeof value === 'string' && value.length > props.maxLength) {
      errors.push(`字段 ${field} 超过最大长度 ${props.maxLength}（当前 ${value.length}）`);
    }
    
    // 范围限制
    if (props.min !== undefined && value < props.min) {
      errors.push(`字段 ${field} 小于最小值 ${props.min}`);
    }
    if (props.max !== undefined && value > props.max) {
      errors.push(`字段 ${field} 大于最大值 ${props.max}`);
    }
    
    // 枚举检查
    if (props.enum && !props.enum.includes(value)) {
      errors.push(`字段 ${field} 值不在允许范围: ${props.enum.join('/')}`);
    }
  }
  
  return {
    valid: errors.length === 0,
    errors,
    action: errors.length === 0 ? 'pass' : 'retry',
    parsed
  };
}

// ===== Schema格式化输出（用于提示词） =====

/**
 * 将Schema格式化为简洁的提示词文本
 */
export function formatSchemaPrompt(schema) {
  let text = '## 输出格式（JSON，强制遵守）\n\n';
  text += '```json\n';
  text += '{\n';
  
  for (const field of schema.required) {
    const props = schema.properties[field];
    text += `  "${field}": `;
    
    if (props.type === 'array') {
      text += `[] // ${props.description}\n`;
    } else if (props.type === 'string') {
      text += `"" // ${props.description}\n`;
    } else if (props.type === 'number') {
      text += `0 // ${props.description}\n`;
    }
  }
  
  text += '}\n```\n\n';
  text += '**规则**：\n';
  text += '- 必须输出合法JSON\n';
  text += '- 所有必需字段必须填写\n';
  text += '- 不符合Schema将被拒绝并重试\n';
  
  return text;
}

// ===== 导出所有Schema =====

export const OUTPUT_SCHEMAS = {
  research: RESEARCH_OUTPUT_SCHEMA,
  tech: TECH_OUTPUT_SCHEMA,
  critic: CRITIC_OUTPUT_SCHEMA,
  strategy: STRATEGY_OUTPUT_SCHEMA
};