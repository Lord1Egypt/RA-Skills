/**
 * 状态管理模块 - v8.0 第二阶段
 * 
 * 功能：
 * 1. JSON Schema校验增强（使用 ajv 风格的校验规则）
 * 2. 版本号管理（数据版本追踪）
 * 3. 文件锁机制（防止并发冲突）
 * 4. 状态持久化（事务式写入）
 * 
 * 目的：解决GPT评价指出的"状态管理混乱"问题
 */

import fs from 'fs';
import path from 'path';
import { selectSchema } from './outputSchema.js';

const CONFIG_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace');

// ===== Schema校验规则（增强版） =====

/**
 * 扩展的校验规则（比 outputSchema.js 更严格）
 */
export const ENHANCED_VALIDATION_RULES = {
  // 研究代理
  research: {
    required: ['findings', 'analysis', 'conclusion'],
    constraints: {
      findings: { min: 1, max: 5, itemMaxLength: 100 },
      analysis: { minLength: 50, maxLength: 1000 },
      conclusion: { minLength: 20, maxLength: 400 },
      sources: { max: 10 },
      confidence: { enum: ['high', 'medium', 'low'] }
    },
    qualityChecks: [
      { name: 'findingsNotEmpty', rule: 'findings.length >= 1' },
      { name: 'analysisHasContent', rule: 'analysis.length >= 50' },
      { name: 'conclusionValid', rule: 'conclusion.length >= 20' }
    ]
  },
  
  // Critic代理
  critic: {
    required: ['issues', 'verdict', 'score'],
    constraints: {
      issues: { max: 10 },
      improvements: { max: 10 },
      verdict: { enum: ['pass', 'fail', 'conditional'] },
      score: { min: 0, max: 100 }
    },
    qualityChecks: [
      { name: 'scoreInRange', rule: 'score >= 0 && score <= 100' },
      { name: 'verdictValid', rule: ['pass', 'fail', 'conditional'].includes(verdict)' }
    ]
  },
  
  // 技术代理
  tech: {
    required: ['approach', 'risks'],
    constraints: {
      approach: { minLength: 30, maxLength: 600 },
      risks: { max: 5 },
      implementation: { max: 5 }
    },
    qualityChecks: [
      { name: 'approachNotEmpty', rule: 'approach.length >= 30' },
      { name: 'risksIdentified', rule: 'risks.length >= 0' }
    ]
  },
  
  // 策略代理
  strategy: {
    required: ['insights', 'actions'],
    constraints: {
      insights: { min: 1, max: 5 },
      actions: { min: 1, max: 5 },
      scenarios: { max: 3 }
    },
    qualityChecks: [
      { name: 'hasInsights', rule: 'insights.length >= 1' },
      { name: 'hasActions', rule: 'actions.length >= 1' }
    ]
  }
};

// ===== 增强版校验函数 =====

/**
 * 增强版JSON校验（带质量检查）
 * 
 * @param {object|string} output - 输出内容
 * @param {string} agentName - 代理名称
 * @returns {object} 校验结果 { valid, errors, warnings, score, action }
 */
export function validateEnhanced(output, agentName) {
  const result = {
    valid: true,
    errors: [],
    warnings: [],
    score: 100,
    action: 'pass',
    qualityIssues: []
  };
  
  // 1. JSON解析检查
  let parsed;
  try {
    parsed = typeof output === 'string' ? JSON.parse(output) : output;
  } catch (e) {
    result.valid = false;
    result.errors.push('JSON解析失败: ' + e.message);
    result.action = 'retry';
    return result;
  }
  
  // 2. 选择校验规则
  const rules = selectEnhancedRules(agentName);
  if (!rules) {
    result.warnings.push('未找到对应校验规则，使用默认规则');
    return result;
  }
  
  // 3. 必需字段检查
  for (const field of rules.required) {
    if (!parsed[field] || parsed[field] === '') {
      result.errors.push(`必需字段缺失: ${field}`);
      result.valid = false;
    }
  }
  
  // 4. 字段约束检查
  for (const [field, constraints] of Object.entries(rules.constraints || {})) {
    const value = parsed[field];
    if (value === undefined || value === null) continue;
    
    // 数量约束
    if (constraints.min !== undefined && Array.isArray(value) && value.length < constraints.min) {
      result.errors.push(`${field} 数量不足: 最少 ${constraints.min}，当前 ${value.length}`);
      result.valid = false;
    }
    if (constraints.max !== undefined) {
      if (Array.isArray(value) && value.length > constraints.max) {
        result.warnings.push(`${field} 数量过多: 最多 ${constraints.max}，当前 ${value.length}`);
        result.score -= 5;
      }
    }
    
    // 长度约束
    if (constraints.minLength !== undefined && typeof value === 'string' && value.length < constraints.minLength) {
      result.warnings.push(`${field} 内容过短: 最少 ${constraints.minLength} 字符`);
      result.score -= 10;
    }
    if (constraints.maxLength !== undefined && typeof value === 'string' && value.length > constraints.maxLength) {
      result.warnings.push(`${field} 内容过长: 最多 ${constraints.maxLength} 字符`);
      result.score -= 5;
    }
    
    // 枚举约束
    if (constraints.enum && !constraints.enum.includes(value)) {
      result.errors.push(`${field} 值不在允许范围: ${constraints.enum.join('/')}`);
      result.valid = false;
    }
    
    // 范围约束
    if (constraints.min !== undefined && typeof value === 'number' && value < constraints.min) {
      result.errors.push(`${field} 值过低: 最小 ${constraints.min}`);
      result.valid = false;
    }
    if (constraints.max !== undefined && typeof value === 'number' && value > constraints.max) {
      result.errors.push(`${field} 值过高: 最大 ${constraints.max}`);
      result.valid = false;
    }
  }
  
  // 5. 质量检查（自定义规则）
  for (const check of rules.qualityChecks || []) {
    try {
      // 简单的条件评估
      const passed = evaluateQualityCheck(check.rule, parsed);
      if (!passed) {
        result.qualityIssues.push(check.name);
        result.score -= 10;
      }
    } catch (e) {
      result.warnings.push(`质量检查失败: ${check.name}`);
    }
  }
  
  // 6. 确定action
  if (result.errors.length > 0) {
    result.action = 'retry';
  } else if (result.score < 70) {
    result.action = 'review';
    result.warnings.push('质量评分低于70，建议人工审核');
  }
  
  return result;
}

/**
 * 选择增强校验规则
 */
function selectEnhancedRules(agentName) {
  const nameLC = agentName.toLowerCase();
  
  if (nameLC.includes('research') || nameLC.includes('analyst')) {
    return ENHANCED_VALIDATION_RULES.research;
  }
  if (nameLC.includes('critic') || nameLC.includes('review')) {
    return ENHANCED_VALIDATION_RULES.critic;
  }
  if (nameLC.includes('tech') || nameLC.includes('technical')) {
    return ENHANCED_VALIDATION_RULES.tech;
  }
  if (nameLC.includes('strategy')) {
    return ENHANCED_VALIDATION_RULES.strategy;
  }
  
  return ENHANCED_VALIDATION_RULES.research; // 默认
}

/**
 * 评估质量检查规则
 */
function evaluateQualityCheck(rule, data) {
  // 简单的规则评估（支持常见的JS表达式）
  try {
    // 提取字段名和条件
    const match = rule.match(/(\w+)\s*(>=|<=|>|<|===|includes)\s*(.+)/);
    if (!match) return true;
    
    const [, field, operator, value] = match;
    const fieldValue = data[field];
    
    if (fieldValue === undefined) return false;
    
    const numValue = parseFloat(value);
    
    switch (operator) {
      case '>=': return fieldValue >= numValue;
      case '<=': return fieldValue <= numValue;
      case '>': return fieldValue > numValue;
      case '<': return fieldValue < numValue;
      case '===': return fieldValue === value;
      case 'includes': return Array.isArray(fieldValue) ? fieldValue.length >= numValue : fieldValue.includes(value);
      default: return true;
    }
  } catch (e) {
    return true;
  }
}

// ===== 版本号管理 =====

/**
 * 状态版本管理器
 */
export class StateVersionManager {
  constructor(stateFile) {
    this.stateFile = stateFile;
    this.currentVersion = 0;
    this.lockFile = stateFile + '.lock';
  }
  
  /**
   * 加载状态（带版本检查）
   */
  load() {
    try {
      if (!fs.existsSync(this.stateFile)) {
        return { version: 0, data: {} };
      }
      
      const content = fs.readFileSync(this.stateFile, 'utf-8');
      const state = JSON.parse(content);
      this.currentVersion = state.version || 0;
      
      return state;
    } catch (e) {
      return { version: 0, data: {}, error: e.message };
    }
  }
  
  /**
   * 保存状态（带版本号更新）
   */
  save(data, forceVersion = null) {
    // 获取锁
    this.acquireLock();
    
    try {
      const newVersion = forceVersion !== null ? forceVersion : this.currentVersion + 1;
      
      const state = {
        version: newVersion,
        data: data,
        updatedAt: new Date().toISOString(),
        previousVersion: this.currentVersion
      };
      
      // 写入临时文件，然后原子替换
      const tempFile = this.stateFile + '.tmp';
      fs.writeFileSync(tempFile, JSON.stringify(state, null, 2), 'utf-8');
      fs.renameSync(tempFile, this.stateFile);
      
      this.currentVersion = newVersion;
      
      return { success: true, version: newVersion };
    } catch (e) {
      return { success: false, error: e.message };
    } finally {
      this.releaseLock();
    }
  }
  
  /**
   * 获取文件锁
   */
  acquireLock() {
    const maxWait = 5000; // 最多等待5秒
    const startTime = Date.now();
    
    while (fs.existsSync(this.lockFile)) {
      if (Date.now() - startTime > maxWait) {
        throw new Error('锁获取超时');
      }
      // 等待100ms
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 100);
    }
    
    // 创建锁文件
    fs.writeFileSync(this.lockFile, JSON.stringify({
      acquiredAt: new Date().toISOString(),
      pid: process.pid
    }), 'utf-8');
  }
  
  /**
   * 释放文件锁
   */
  releaseLock() {
    try {
      if (fs.existsSync(this.lockFile)) {
        fs.unlinkSync(this.lockFile);
      }
    } catch (e) {
      // 锁文件可能已被其他进程删除
    }
  }
  
  /**
   * 版本冲突检查
   */
  checkConflict(expectedVersion) {
    const state = this.load();
    if (state.version !== expectedVersion) {
      return {
        hasConflict: true,
        currentVersion: state.version,
        expectedVersion: expectedVersion,
        message: `版本冲突: 当前版本 ${state.version}，期望版本 ${expectedVersion}`
      };
    }
    return { hasConflict: false };
  }
}

// ===== 状态持久化助手 =====

/**
 * 工作流状态管理器
 */
export class WorkflowStateManager {
  constructor(workflowId) {
    const stateFile = path.join(CONFIG_DIR, '.multi-agent-workflows.json');
    this.versionManager = new StateVersionManager(stateFile);
    this.workflowId = workflowId;
  }
  
  /**
   * 初始化工作流状态
   */
  initWorkflow(goal, agents) {
    const state = this.versionManager.load();
    
    state.data[this.workflowId] = {
      goal: goal,
      agents: agents,
      status: 'initialized',
      phases: {},
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    return this.versionManager.save(state.data);
  }
  
  /**
   * 更新阶段状态
   */
  updatePhase(phaseId, phaseData) {
    const state = this.versionManager.load();
    
    if (!state.data[this.workflowId]) {
      return { success: false, error: '工作流不存在' };
    }
    
    state.data[this.workflowId].phases[phaseId] = {
      ...phaseData,
      updatedAt: new Date().toISOString()
    };
    state.data[this.workflowId].updatedAt = new Date().toISOString();
    
    return this.versionManager.save(state.data);
  }
  
  /**
   * 获取工作流状态
   */
  getWorkflow() {
    const state = this.versionManager.load();
    return state.data[this.workflowId] || null;
  }
  
  /**
   * 标记完成
   */
  markCompleted(result) {
    const state = this.versionManager.load();
    
    if (!state.data[this.workflowId]) {
      return { success: false, error: '工作流不存在' };
    }
    
    state.data[this.workflowId].status = 'completed';
    state.data[this.workflowId].result = result;
    state.data[this.workflowId].completedAt = new Date().toISOString();
    
    return this.versionManager.save(state.data);
  }
}

// ===== 导出 =====

export default {
  validateEnhanced,
  ENHANCED_VALIDATION_RULES,
  StateVersionManager,
  WorkflowStateManager
};