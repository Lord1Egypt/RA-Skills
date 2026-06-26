#!/usr/bin/env node
/**
 * 长期计划 - 多计划关联模块
 * 
 * 支持：
 * - 计划间引用（如理财计划引用学习计划）
 * - 冲突检测（资金竞争、时间竞争）
 * - 依赖关系（A完成后才能开始B）
 * - 资源竞争预警
 */

import fs from 'fs';
import path from 'path';

const TASKS_DIR = path.join(process.env.HOME, '.openclaw', 'workspace', 'memory', 'tasks');
const RELATION_FILE = path.join(TASKS_DIR, 'relations.json');

/**
 * 计划关系类型
 * @typedef {'depends-on'|'conflicts-with'|'related-to'|'blocks'} RelationType
 * 
 * depends-on: 依赖关系（B依赖A，A完成才能启动B）
 * conflicts-with: 冲突关系（A和B竞争资源）
 * related-to: 关联关系（A和B有联系但无冲突）
 * blocks: 阻塞关系（A阻塞B的进度）
 */

/**
 * 创建计划关联
 */
export function createRelation(from, to, type, reason = '') {
  const relations = loadRelations();
  
  // 检查是否已存在
  const exists = relations.find(
    r => (r.from === from && r.to === to) || (r.from === to && r.to === from)
  );
  if (exists) {
    return { success: false, message: `关联已存在：${from} ↔ ${to}` };
  }
  
  relations.push({
    from,
    to,
    type,
    reason,
    createdAt: new Date().toISOString()
  });
  
  saveRelations(relations);
  return { success: true, message: `已创建关联：${from} ${typeSymbol(type)} ${to}` };
}

/**
 * 删除计划关联
 */
export function removeRelation(from, to) {
  const relations = loadRelations();
  const filtered = relations.filter(
    r => !((r.from === from && r.to === to) || (r.from === to && r.to === from))
  );
  
  if (filtered.length === relations.length) {
    return { success: false, message: `未找到关联：${from} ↔ ${to}` };
  }
  
  saveRelations(filtered);
  return { success: true, message: `已删除关联：${from} ↔ ${to}` };
}

/**
 * 检测计划间冲突
 */
export function detectConflicts() {
  const relations = loadRelations();
  const indexFile = path.join(TASKS_DIR, 'index.json');
  
  if (!fs.existsSync(indexFile)) return [];
  
  const index = JSON.parse(fs.readFileSync(indexFile, 'utf-8'));
  const activePlans = index.plans.filter(p => p.status === 'active');
  
  const conflicts = [];
  
  // 检查冲突关系
  const conflictRelations = relations.filter(r => r.type === 'conflicts-with');
  for (const rel of conflictRelations) {
    const fromActive = activePlans.find(p => p.name === rel.from);
    const toActive = activePlans.find(p => p.name === rel.to);
    
    if (fromActive && toActive) {
      conflicts.push({
        type: 'resource_conflict',
        plans: [rel.from, rel.to],
        reason: rel.reason,
        severity: 'medium',
        suggestion: `建议暂停其中一个计划，或调整资源分配`
      });
    }
  }
  
  // 检查依赖阻塞
  const dependsRelations = relations.filter(r => r.type === 'depends-on');
  for (const rel of dependsRelations) {
    const fromActive = activePlans.find(p => p.name === rel.from);
    const toActive = activePlans.find(p => p.name === rel.to);
    
    if (toActive && !fromActive) {
      // 目标计划还在跑，但依赖的计划已经不在active了
      conflicts.push({
        type: 'dependency_missing',
        plans: [rel.to],
        dependsOn: rel.from,
        reason: `${rel.to} 依赖 ${rel.from}，但 ${rel.from} 未激活`,
        severity: 'high',
        suggestion: `请先激活 ${rel.from} 或移除依赖关系`
      });
    }
  }
  
  // 检查资金竞争（自动检测）
  const financePlans = activePlans.filter(p => 
    p.assetSnapshot?.positions?.length || p.triggers?.conditional?.length
  );
  
  if (financePlans.length > 1) {
    conflicts.push({
      type: 'resource_overlap',
      plans: financePlans.map(p => p.name),
      reason: '多个计划同时涉及资产操作',
      severity: 'low',
      suggestion: '注意操作时避免互相影响，建议分时段执行'
    });
  }
  
  // 检查时间竞争（同一天有多个里程碑）
  const milestonesByDate = {};
  for (const plan of activePlans) {
    const ms = plan.milestones || [];
    for (const m of ms) {
      const date = m.date || m.日期;
      if (!date || m.status === '✅') continue;
      
      if (!milestonesByDate[date]) milestonesByDate[date] = [];
      milestonesByDate[date].push({ plan: plan.name, event: m.event || m.事件 });
    }
  }
  
  for (const [date, items] of Object.entries(milestonesByDate)) {
    if (items.length > 1) {
      conflicts.push({
        type: 'schedule_conflict',
        plans: items.map(i => i.plan),
        date,
        reason: `同一天有${items.length}个里程碑：${items.map(i => i.event).join('、')}`,
        severity: 'low',
        suggestion: '确认当天是否能同时处理'
      });
    }
  }
  
  return conflicts;
}

/**
 * 获取计划的关系图
 */
export function getPlanRelations(planName) {
  const relations = loadRelations();
  
  return {
    outgoing: relations.filter(r => r.from === planName),
    incoming: relations.filter(r => r.to === planName),
    all: relations.filter(r => r.from === planName || r.to === planName)
  };
}

/**
 * 生成冲突报告
 */
export function generateConflictReport() {
  const conflicts = detectConflicts();
  
  if (conflicts.length === 0) {
    return '✅ 无计划冲突，所有计划运行正常。';
  }
  
  const lines = [`⚠️ 检测到 ${conflicts.length} 个冲突：\n`];
  
  for (const c of conflicts) {
    const icon = c.severity === 'high' ? '🔴' : c.severity === 'medium' ? '🟡' : '🟢';
    lines.push(`${icon} **${c.reason}**`);
    if (c.plans) lines.push(`   涉及计划：${c.plans.join('、')}`);
    if (c.suggestion) lines.push(`   建议：${c.suggestion}`);
    lines.push('');
  }
  
  return lines.join('\n');
}

/**
 * 关联状态摘要（心跳推送用）
 */
export function getRelationsSummary() {
  const relations = loadRelations();
  const conflicts = detectConflicts();
  
  if (relations.length === 0 && conflicts.length === 0) return null;
  
  const summary = [];
  
  // 关联关系概览
  if (relations.length > 0) {
    const grouped = {};
    for (const r of relations) {
      if (!grouped[r.type]) grouped[r.type] = [];
      grouped[r.type].push(`${r.from} ↔ ${r.to}`);
    }
    for (const [type, items] of Object.entries(grouped)) {
      summary.push(`🔗 ${typeLabel(type)}：${items.join('、')}`);
    }
  }
  
  // 冲突预警
  const activeConflicts = conflicts.filter(c => c.severity === 'high' || c.severity === 'medium');
  if (activeConflicts.length > 0) {
    summary.push(`⚠️ ${activeConflicts.length}个活跃冲突需要关注`);
  }
  
  return summary.join('\n');
}

function typeSymbol(type) {
  const symbols = {
    'depends-on': '→',
    'conflicts-with': '⚡',
    'related-to': '~',
    'blocks': '🚫'
  };
  return symbols[type] || '→';
}

function typeLabel(type) {
  const labels = {
    'depends-on': '依赖关系',
    'conflicts-with': '冲突关系',
    'related-to': '关联关系',
    'blocks': '阻塞关系'
  };
  return labels[type] || type;
}

function loadRelations() {
  if (!fs.existsSync(RELATION_FILE)) return [];
  try {
    return JSON.parse(fs.readFileSync(RELATION_FILE, 'utf-8'));
  } catch {
    return [];
  }
}

function saveRelations(relations) {
  const tmpFile = RELATION_FILE + '.tmp';
  fs.writeFileSync(tmpFile, JSON.stringify(relations, null, 2));
  fs.renameSync(tmpFile, RELATION_FILE);
}

// CLI入口
if (process.argv[1] && process.argv[1].endsWith('plan-relations.mjs')) {
  const cmd = process.argv[2];
  
  if (cmd === 'list') {
    const relations = loadRelations();
    console.log(JSON.stringify(relations, null, 2));
  } else if (cmd === 'conflicts') {
    const report = generateConflictReport();
    console.log(report);
  } else if (cmd === 'add') {
    const from = process.argv[3];
    const to = process.argv[4];
    const type = process.argv[5] || 'related-to';
    const reason = process.argv[6] || '';
    
    if (!from || !to) {
      console.log('用法: node plan-relations.mjs add <planA> <planB> [type] [reason]');
      process.exit(1);
    }
    
    const result = createRelation(from, to, type, reason);
    console.log(result.message);
  } else if (cmd === 'remove') {
    const from = process.argv[3];
    const to = process.argv[4];
    const result = removeRelation(from, to);
    console.log(result.message);
  } else {
    console.log('用法:');
    console.log('  node plan-relations.mjs list          — 列出所有关联');
    console.log('  node plan-relations.mjs conflicts     — 检测冲突');
    console.log('  node plan-relations.mjs add A B [type] [reason] — 创建关联');
    console.log('  node plan-relations.mjs remove A B    — 删除关联');
    console.log('');
    console.log('类型：depends-on | conflicts-with | related-to | blocks');
  }
}
