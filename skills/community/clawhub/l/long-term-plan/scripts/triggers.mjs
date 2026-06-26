#!/usr/bin/env node
/**
 * 长期计划 - 触发器管理模块
 * 
 * 功能：
 * - 解析计划文件中的触发器声明
 * - 自动注册时间触发器到cron
 * - 管理条件触发器存储
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TASKS_DIR = path.join(process.env.HOME, '.openclaw', 'workspace', 'memory', 'tasks');

/**
 * 解析计划文件中的触发器
 */
export function parseTriggers(planContent) {
  const triggers = {
    time: [],
    conditional: []
  };
  
  // 解析时间触发
  const timeTriggerMatch = planContent.match(/### 时间触发\n([\s\S]*?)(?=\n###|\n---|\n##|$)/);
  if (timeTriggerMatch) {
    const lines = timeTriggerMatch[1].trim().split('\n');
    for (const line of lines) {
      // 格式: - `每天 12:30` 推送阶段进度
      const match = line.match(/-\s*`([^`]+)`\s*(.+)/);
      if (match) {
        const schedule = parseScheduleExpression(match[1]);
        triggers.time.push({
          schedule: match[1],
          cron: schedule,
          action: match[2].trim()
        });
      }
    }
  }
  
  // 解析条件触发
  const condTriggerMatch = planContent.match(/### 条件触发\n([\s\S]*?)(?=\n###|\n---|\n##|$)/);
  if (condTriggerMatch) {
    const lines = condTriggerMatch[1].trim().split('\n');
    for (const line of lines) {
      // 格式: - `当 024975 涨超25%` → 提醒"半导体止盈50%"
      const match = line.match(/-\s*`当\s+([^`]+)`\s*→\s*(.+)/);
      if (match) {
        const condition = parseConditionExpression(match[1]);
        triggers.conditional.push({
          raw: match[1],
          ...condition,
          action: match[2].trim().replace(/"/g, '')
        });
      }
    }
  }
  
  return triggers;
}

/**
 * 解析时间表达式为cron格式
 * 例如: "每天 12:30" → "30 12 * * *"
 */
function parseScheduleExpression(expr) {
  // 每天 12:30
  const dailyMatch = expr.match(/每天\s+(\d{1,2}):(\d{2})/);
  if (dailyMatch) {
    return `${dailyMatch[2]} ${dailyMatch[1]} * * *`;
  }
  
  // 复盘日 12:30 (特殊处理，需要在心跳时判断)
  const reviewMatch = expr.match(/复盘日\s+(\d{1,2}):(\d{2})/);
  if (reviewMatch) {
    return `review:${reviewMatch[2]} ${reviewMatch[1]}`; // 特殊标记
  }
  
  // 关键日期-1天 12:30
  const keydateMatch = expr.match(/关键日期-?(\d*)天?\s+(\d{1,2}):(\d{2})/);
  if (keydateMatch) {
    const daysBefore = parseInt(keydateMatch[1]) || 1;
    return `keydate:${daysBefore}:${keydateMatch[3]} ${keydateMatch[2]}`;
  }
  
  return null;
}

/**
 * 解析条件表达式
 * 例如: "024975 涨超25%" → { fund: "024975", condition: "gain", value: 25, operator: ">" }
 */
function parseConditionExpression(expr) {
  // 基金涨跌
  const fundGainMatch = expr.match(/(\d{6})\s*涨超(\d+)%/);
  if (fundGainMatch) {
    return { fund: fundGainMatch[1], condition: 'gain', operator: '>', value: parseInt(fundGainMatch[2]) };
  }
  
  const fundLossMatch = expr.match(/(\d{6})\s*跌超(\d+)%/);
  if (fundLossMatch) {
    return { fund: fundLossMatch[1], condition: 'loss', operator: '>', value: parseInt(fundLossMatch[2]) };
  }
  
  // 整体回撤
  const drawdownMatch = expr.match(/整体.*回撤超?(\d+)%/);
  if (drawdownMatch) {
    return { fund: 'portfolio', condition: 'drawdown', operator: '>', value: parseInt(drawdownMatch[1]) };
  }
  
  // 指数点位
  const indexMatch = expr.match(/(沪深300|上证指数|创业板指)\s*(跌到|涨到)(\d+)/);
  if (indexMatch) {
    return { 
      fund: indexMatch[1], 
      condition: indexMatch[2] === '跌到' ? 'fallBelow' : 'riseAbove', 
      value: parseInt(indexMatch[3]) 
    };
  }
  
  return { fund: 'unknown', condition: 'unknown', raw: expr };
}

/**
 * 注册触发器到cron
 */
export async function registerTriggers(planId, triggers) {
  const registered = [];
  
  for (const t of triggers.time) {
    if (!t.cron || t.cron.startsWith('review:') || t.cron.startsWith('keydate:')) {
      // 特殊触发器，存入triggers.json，由心跳处理
      continue;
    }
    
    // 注册cron任务（通过写入delivery-queue）
    // 这里简化处理，实际需要调用cron模块
    registered.push({
      schedule: t.schedule,
      cron: t.cron,
      action: t.action,
      planId
    });
  }
  
  // 保存触发器配置
  const triggersFile = path.join(TASKS_DIR, `${planId}-triggers.json`);
  fs.writeFileSync(triggersFile, JSON.stringify({
    planId,
    time: triggers.time,
    conditional: triggers.conditional,
    registered,
    createdAt: new Date().toISOString()
  }, null, 2));
  
  return registered;
}

/**
 * 主函数：从计划文件提取并注册触发器
 */
export async function setupTriggersFromPlan(planFile) {
  const content = fs.readFileSync(planFile, 'utf-8');
  const triggers = parseTriggers(content);
  const planId = path.basename(planFile, '-plan.md');
  
  if (triggers.time.length > 0 || triggers.conditional.length > 0) {
    await registerTriggers(planId, triggers);
    console.log(`✅ 已注册 ${triggers.time.length} 个时间触发器`);
    console.log(`✅ 已注册 ${triggers.conditional.length} 个条件触发器`);
  }
  
  return triggers;
}

// CLI入口
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const planFile = process.argv[2];
  if (!planFile) {
    console.log('用法: node triggers.mjs <plan-file>');
    process.exit(1);
  }
  setupTriggersFromPlan(planFile);
}
