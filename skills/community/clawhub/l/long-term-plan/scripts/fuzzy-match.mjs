#!/usr/bin/env node
/**
 * 长期计划 - 自然语言匹配模块
 * 
 * 支持模糊匹配完成任务：
 * - "今天把定投设好了" → 匹配"设置每月定投参数"
 * - "阶段1的前两个都搞完了" → 批量完成
 * - "半导体那个卖了" → 匹配"半导体止盈"
 */

import fs from 'fs';
import path from 'path';

const TASKS_DIR = path.join(process.env.HOME, '.openclaw', 'workspace', 'memory', 'tasks');

/**
 * 模糊匹配任务
 * @param {string} input - 用户输入（如"定投设好了"）
 * @param {Array} tasks - 任务列表（[{text, status}]）
 * @returns {Array} 匹配结果（按相似度排序）
 */
export function fuzzyMatchTask(input, tasks) {
  const results = [];
  const inputLower = input.toLowerCase();
  
  for (const task of tasks) {
    if (task.status === 'completed' || task.status === '[x]') continue;
    
    const taskText = task.text || task;
    const taskLower = taskText.toLowerCase();
    
    let score = 0;
    
    // 1. 完全包含匹配
    if (taskLower.includes(inputLower) || inputLower.includes(taskLower)) {
      score = 100;
    }
    
    // 2. 关键词匹配
    const inputWords = segment(inputLower);
    const taskWords = segment(taskLower);
    const commonWords = inputWords.filter(w => taskWords.includes(w));
    if (commonWords.length > 0) {
      score = Math.max(score, 50 + commonWords.length * 10);
    }
    
    // 3. 特殊规则匹配
    // "xxx设好了" → 匹配"设置xxx"
    if (input.includes('设好') && taskText.includes('设置')) {
      const target = input.replace(/设好.*/, '').replace(/.*把/, '');
      if (taskText.includes(target)) {
        score = Math.max(score, 80);
      }
    }
    
    // "xxx完成了" → 匹配包含xxx的任务
    if (input.includes('完成') || input.includes('好了') || input.includes('搞定了')) {
      const target = input.replace(/完成.*/, '').replace(/好了.*/, '').replace(/搞定了.*/, '').replace(/.*把/, '');
      if (taskText.includes(target)) {
        score = Math.max(score, 75);
      }
    }
    
    // "xxx卖了/止盈/止损" → 匹配相关任务
    if (input.includes('卖') || input.includes('止盈') || input.includes('止损')) {
      if (taskText.includes('止盈') || taskText.includes('止损') || taskText.includes('卖出')) {
        score = Math.max(score, 70);
      }
    }
    
    if (score > 0) {
      results.push({ task: taskText, score, original: task });
    }
  }
  
  // 按分数排序
  return results.sort((a, b) => b.score - a.score);
}

/**
 * 中文分词（简单实现）
 */
function segment(text) {
  const words = [];
  // 提取2-4字的词
  for (let len = 2; len <= 4; len++) {
    for (let i = 0; i <= text.length - len; i++) {
      words.push(text.slice(i, i + len));
    }
  }
  // 提取单字（过滤常见虚词）
  const stopWords = ['的', '了', '是', '在', '和', '与', '或', '把', '被', '对', '给', '向'];
  for (const char of text) {
    if (!stopWords.includes(char) && !/\s/.test(char)) {
      words.push(char);
    }
  }
  return words;
}

/**
 * 批量匹配任务
 * @param {string} input - 用户输入（如"阶段1的前两个都搞完了"）
 * @param {Object} plan - 计划对象
 * @returns {Array} 匹配结果
 */
export function batchMatchTask(input, plan) {
  let tasks = [];
  try { tasks = extractTasks(plan); } catch { tasks = []; }
  const results = [];
  
  // "前两个" / "前三个"
  const prefixMatch = input.match(/前(\d+)[个项]/);
  if (prefixMatch) {
    const count = parseInt(prefixMatch[1]);
    const pending = tasks.filter(t => t.status !== 'completed' && t.status !== '[x]');
    for (let i = 0; i < Math.min(count, pending.length); i++) {
      results.push({ task: pending[i].text, score: 90, batch: true, index: i + 1 });
    }
    return results;
  }
  
  // "阶段1的所有任务"
  if (input.includes('阶段') && (input.includes('所有') || input.includes('全部'))) {
    const pending = tasks.filter(t => t.status !== 'completed' && t.status !== '[x]');
    return pending.map((t, i) => ({ task: t.text, score: 85, batch: true, index: i + 1 }));
  }
  
  // "都完成了" / "全搞定了"
  if (input.includes('都完成') || input.includes('全搞定') || input.includes('全部完成')) {
    const pending = tasks.filter(t => t.status !== 'completed' && t.status !== '[x]');
    return pending.map((t, i) => ({ task: t.text, score: 80, batch: true, index: i + 1 }));
  }
  
  return results;
}

/**
 * 从计划文件提取任务列表
 */
function extractTasks(plan) {
  const content = fs.readFileSync(path.join(TASKS_DIR, plan.file), 'utf-8');
  const tasks = [];
  
  // 匹配任务行
  const lines = content.split('\n');
  for (const line of lines) {
    // - [ ] 任务 [高]
    // - [x] 已完成
    // - [?] 待决策
    // - [!] 条件触发
    // - [~] 进行中
    const match = line.match(/-\s*\[([ x?~!])\]\s*(.+?)(?:\s+\[[高中低]\])?$/);
    if (match) {
      tasks.push({
        text: match[2].trim(),
        status: match[1] === 'x' ? 'completed' : 'pending',
        raw: line
      });
    }
  }
  
  return tasks;
}

/**
 * 智能匹配入口
 * @param {string} input - 用户输入
 * @param {string} planName - 计划名称（可选）
 * @returns {{ matched: Array, suggestions: Array, ambiguous: boolean }}
 */
export function smartMatch(input, planName = null) {
  // 读取所有活跃计划
  const indexFile = path.join(TASKS_DIR, 'index.json');
  if (!fs.existsSync(indexFile)) {
    return { matched: [], suggestions: [], ambiguous: false };
  }
  
  const index = JSON.parse(fs.readFileSync(indexFile, 'utf-8'));
  const activePlans = index.plans.filter(p => p.status === 'active');
  
  let allTasks = [];
  for (const plan of activePlans) {
    const tasks = extractTasks(plan);
    for (const t of tasks) {
      allTasks.push({ ...t, planName: plan.name });
    }
  }
  
  // 尝试批量匹配
  const batchResults = batchMatchTask(input, activePlans[0] || {});
  if (batchResults.length > 0) {
    return { matched: batchResults, suggestions: [], ambiguous: false, batch: true };
  }
  
  // 模糊匹配
  const fuzzyResults = fuzzyMatchTask(input, allTasks);
  
  if (fuzzyResults.length === 0) {
    // 无匹配，返回待办列表作为建议
    const pending = allTasks.filter(t => t.status !== 'completed');
    return { 
      matched: [], 
      suggestions: pending.slice(0, 5).map(t => t.text),
      ambiguous: false 
    };
  }
  
  if (fuzzyResults.length === 1 || fuzzyResults[0].score >= 80) {
    // 高置信度匹配
    return { matched: [fuzzyResults[0]], suggestions: [], ambiguous: false };
  }
  
  // 多个候选，返回让用户确认
  return { 
    matched: [], 
    suggestions: fuzzyResults.slice(0, 3).map(r => r.task),
    ambiguous: true 
  };
}

/**
 * 标记任务完成
 */
export function markTaskComplete(planFile, taskText) {
  const filePath = path.join(TASKS_DIR, planFile);
  let content = fs.readFileSync(filePath, 'utf-8');
  
  // 找到任务行并标记
  const lines = content.split('\n');
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes(taskText) && lines[i].match(/-\s*\[([ x?~!])\]/)) {
      lines[i] = lines[i].replace(/\[([ x?~!])\]/, '[x]');
    }
  }
  
  content = lines.join('\n');
  
  // 原子写入
  const tmpFile = filePath + '.tmp';
  fs.writeFileSync(tmpFile, content);
  fs.renameSync(tmpFile, filePath);
  
  return true;
}

// CLI入口
if (process.argv[1] && process.argv[1].endsWith('fuzzy-match.mjs')) {
  const input = process.argv[2];
  if (!input) {
    console.log('用法: node fuzzy-match.mjs "我完成了定投"');
    process.exit(1);
  }
  
  const result = smartMatch(input);
  console.log(JSON.stringify(result, null, 2));
}
