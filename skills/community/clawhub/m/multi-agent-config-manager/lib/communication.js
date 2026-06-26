/**
 * 通信总线 - 管理代理间的消息传递和协作
 * v8.0 精简版 - 强约束JSON输出 + 提示词压缩
 * 
 * 变化：
 * 1. 提示词长度从 ~800行 → ~80行（减少90%)
 * 2. 强制JSON输出格式（提升流程遵循性）
 * 3. 去除冗余协议描述和质量要求
 */

import path from 'path';
import { selectSchema, formatSchemaPrompt } from './outputSchema.js';

// 通信协议模板
export const COMMUNICATION_PROTOCOLS = {
  // 标准任务执行协议
  standard_task: {
    name: '标准任务执行',
    description: '主代理分配任务 → 分支代理执行 → 返回结果',
    message_flow: [
      { step: 1, type: 'task_assignment', from: 'main', to: 'branch' },
      { step: 2, type: 'task_result', from: 'branch', to: 'main' }
    ],
    timeout_minutes: 15
  },

  // 带反馈的任务协议
  task_with_feedback: {
    name: '带反馈的任务执行',
    description: '主代理分配 → 分支执行 → 主代理验证 → 可能反馈返工',
    message_flow: [
      { step: 1, type: 'task_assignment', from: 'main', to: 'branch' },
      { step: 2, type: 'task_result', from: 'branch', to: 'main' },
      { step: 3, type: 'feedback', from: 'main', to: 'branch', condition: 'validation_failed' },
      { step: 4, type: 'task_result', from: 'branch', to: 'main', condition: 'after_feedback' }
    ],
    timeout_minutes: 30
  },

  // 批判性审核协议
  critical_review: {
    name: '批判性审核',
    description: '主代理提交成果 → 批判代理审核 → 返回审核意见',
    message_flow: [
      { step: 1, type: 'task_assignment', from: 'main', to: 'critic', payload: 'aggregated_result' },
      { step: 2, type: 'critical_review', from: 'critic', to: 'main' }
    ],
    timeout_minutes: 20
  },

  // 完整协作协议
  full_collaboration: {
    name: '完整多代理协作',
    description: '分解 → 执行 → 验证 → 返工(可选) → 汇总 → 审核 → 决策',
    message_flow: [
      { step: 1, type: 'broadcast', from: 'main', to: 'all', content: 'task_decomposition' },
      { step: 2, type: 'task_assignment', from: 'main', to: 'each_branch' },
      { step: 3, type: 'task_result', from: 'each_branch', to: 'main' },
      { step: 4, type: 'feedback', from: 'main', to: 'failed_branches', condition: 'validation_failed' },
      { step: 5, type: 'task_assignment', from: 'main', to: 'critic', payload: 'aggregated' },
      { step: 6, type: 'critical_review', from: 'critic', to: 'main' },
      { step: 7, type: 'decision', from: 'main', to: 'all', content: 'final_decision' }
    ],
    timeout_minutes: 60
  },

  // 辩论协议
  debate: {
    name: '正反方辩论',
    description: '正方论证 → 反方反驳 → 综合评判',
    message_flow: [
      { step: 1, type: 'task_assignment', from: 'main', to: 'pro' },
      { step: 2, type: 'task_assignment', from: 'main', to: 'con' },
      { step: 3, type: 'task_result', from: 'pro', to: 'main' },
      { step: 4, type: 'task_result', from: 'con', to: 'main' },
      { step: 5, type: 'query', from: 'pro', to: 'con', content: 'rebuttal' },
      { step: 6, type: 'response', from: 'con', to: 'pro' },
      { step: 7, type: 'task_assignment', from: 'main', to: 'judge' },
      { step: 8, type: 'critical_review', from: 'judge', to: 'main' }
    ],
    timeout_minutes: 45
  }
};

/**
 * 生成精简版子代理任务提示词（v8.0）
 * 
 * 核心变化：
 * 1. 提示词长度从 ~800行 → ~80行（减少90%）
 * 2. 强制JSON输出格式（提升流程遵循性）
 * 3. 去除冗余协议描述和质量要求
 * 4. 保留必要的文件写入指令
 * 
 * @param {object} agent - 代理配置
 * @param {object} task - 任务描述
 * @param {string} protocol - 协议名称（保留参数，但不嵌入冗余描述）
 * @param {object} context - 上下文信息
 * @returns {string} 精简后的提示词
 */
export function generateAgentPrompt(agent, task, protocol, context = {}) {
  // ===== 选择输出Schema =====
  const schema = selectSchema(agent.name);
  const schemaPrompt = formatSchemaPrompt(schema);
  
  // ===== 构建精简提示词 =====
  let prompt = '';
  
  // 1. 任务描述（核心）
  prompt += `# 任务：${task.description}\n\n`;
  
  // 2. 任务要求（如果有）
  if (task.requirements && task.requirements.length > 0) {
    prompt += `## 要求\n`;
    for (const req of task.requirements) {
      prompt += `- ${req}\n`;
    }
    prompt += '\n';
  }
  
  // 3. 输出格式（强约束JSON）
  prompt += schemaPrompt;
  
  // 4. 文件输出路径（简化）
  if (context.output_dir) {
    prompt += `## 输出\n`;
    prompt += `- 路径: ${context.output_dir}/${agent.name}_report.json\n`;
    prompt += `- 使用 write 工具写入\n`;
    prompt += `- 写入后用 read 验证\n`;
    prompt += `- 最后输出: EXECUTION_COMPLETE\n\n`;
  }
  
  // 5. 总体目标（如果有，简化为一行）
  if (context.goal) {
    prompt += `背景: ${context.goal}\n\n`;
  }
  
  return prompt;
}

/**
 * 生成Legacy版提示词（向后兼容，供需要Markdown输出的场景使用）
 */
export function generateAgentPromptLegacy(agent, task, protocol, context = {}) {
  const CONFIG_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace');
  const agentWorkspacePath = path.join(CONFIG_DIR, 'agents', agent.name);

  let prompt = `# 你是 ${agent.name}\n`;
  prompt += `职责: ${agent.description}\n\n`;

  prompt += `## 任务\n`;
  prompt += `${task.description}\n\n`;

  if (task.requirements && task.requirements.length > 0) {
    prompt += `## 要求\n`;
    for (const req of task.requirements) {
      prompt += `- ${req}\n`;
    }
    prompt += '\n';
  }

  prompt += `## 输出\n`;
  prompt += `1. 核心发现（≤5条）\n`;
  prompt += `2. 分析过程\n`;
  prompt += `3. 结论\n`;
  prompt += `4. 来源\n\n`;

  prompt += `## 文件\n`;
  prompt += `输出至: ${context.output_dir}/${agent.name}_report.md\n`;
  prompt += `使用 write 工具，禁止 shell 命令\n`;
  prompt += `最后输出: EXECUTION_COMPLETE\n\n`;

  if (context.goal) {
    prompt += `背景: ${context.goal}\n`;
  }

  return prompt;
}

/**
 * 生成验证反馈提示词
 */
export function generateFeedbackPrompt(task, validation, agent) {
  let prompt = `# 任务返工通知\n\n`;
  prompt += `你好 ${agent.name}，你之前提交的任务结果需要补充修改。\n\n`;

  prompt += `## 原始任务\n`;
  prompt += `${task.description}\n\n`;

  prompt += `## 验证结果\n`;
  prompt += `综合评分: ${Math.round(validation.score * 100)}%\n`;
  prompt += `通过阈值: ${Math.round(validation.threshold * 100)}%\n\n`;

  if (validation.failed_rules && validation.failed_rules.length > 0) {
    prompt += `## 需要改进的方面\n`;
    for (const rule of validation.failed_rules) {
      prompt += `- ${rule}\n`;
    }
    prompt += '\n';
  }

  prompt += `## 具体检查结果\n`;
  for (const check of validation.checks) {
    const icon = check.result === 'pass' ? '✅' : check.result === 'warning' ? '⚠️' : '❌';
    prompt += `${icon} ${check.rule_name}: ${check.detail}\n`;
  }
  prompt += '\n';

  prompt += `## 返工要求\n`;
  prompt += `请针对上述未达标的方面进行补充和完善，保持原有优势的同时改进不足之处。\n`;
  prompt += `完成后重新提交结果。\n`;

  return prompt;
}
