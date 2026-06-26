#!/usr/bin/env node
// dream-cycle.mjs v1.1 - 梦境模式执行器
// 触发：心跳或手动执行
// v1.1: 路径配置化 + 自动写入检测

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { semanticSimilarity, findSimilarMemories, mergeMemories } from './semantic-similarity.mjs';
import { searchSessionLogs, getRecentSessionSummary } from './session-search.mjs';
import { loadConfig, getPath } from './config-loader.mjs';

const config = loadConfig();

const INDEX_PATH = getPath('indexFile', config);
const DREAM_LOG_PATH = getPath('dreamLog', config);
const ARCHIVE_PATH = getPath('archiveFile', config);
const SESSION_DIR = getPath('sessionDir', config);

// 加载索引
function loadIndex() {
  if (!fs.existsSync(INDEX_PATH)) {
    return { version: 1, updatedAt: new Date().toISOString(), memories: [] };
  }
  const data = fs.readFileSync(INDEX_PATH, 'utf-8');
  return JSON.parse(data);
}

// 保存索引
function saveIndex(index) {
  index.updatedAt = new Date().toISOString();
  fs.writeFileSync(INDEX_PATH, JSON.stringify(index, null, 2));
}

// 记录梦境日志
function logDream(message, type = 'info') {
  const icon = {
    consolidate: '🧠',
    archive: '📦',
    forget: '🗑️',
    merge: '🔗',
    info: '💤',
    complete: '✨',
    autowrite: '✏️',
  }[type] || '💤';
  
  const entry = `${icon} ${message}`;
  
  let log = '';
  if (fs.existsSync(DREAM_LOG_PATH)) {
    log = fs.readFileSync(DREAM_LOG_PATH, 'utf-8');
  }
  const today = new Date().toISOString().split('T')[0];
  if (!log.includes(`## ${today}`)) {
    log += `\n## ${today}\n\n`;
  }
  log += `${entry}\n`;
  fs.writeFileSync(DREAM_LOG_PATH, log);
  console.log(entry);
}

// ==========================================
// 自动写入检测 (v1.1 新增)
// ==========================================
function detectNewMemoriesFromSessions() {
  if (!config.autoWrite?.enabled) return [];
  
  const rules = config.autoWrite.rules;
  const newMemories = [];
  
  try {
    const files = fs.readdirSync(SESSION_DIR)
      .filter(f => f.endsWith('.jsonl') && !f.includes('.reset') && !f.includes('.deleted'))
      .map(f => ({
        path: path.join(SESSION_DIR, f),
        mtime: fs.statSync(path.join(SESSION_DIR, f)).mtime,
      }))
      .sort((a, b) => b.mtime - a.mtime)
      .slice(0, 3);
    
    const existingIds = new Set(loadIndex().memories.map(m => m.id));
    
    for (const file of files) {
      const lines = fs.readFileSync(file.path, 'utf-8').split('\n').filter(l => l.trim());
      let turnCount = 0;
      let userMessages = [];
      let hasTaskComplete = false;
      let hasRemember = false;
      
      for (const line of lines) {
        try {
          const obj = JSON.parse(line);
          const role = obj?.message?.role;
          let content = '';
          if (typeof obj?.message?.content === 'string') content = obj.message.content;
          else if (Array.isArray(obj?.message?.content)) {
            content = obj.message.content.map(c => c.text || '').join('');
          }
          
          // Bug fix: 过滤心跳模板/系统消息（非真实对话内容）
          const isHeartbeatTemplate = content.includes('Read HEARTBEAT.md') || 
            content.includes('HEARTBEAT_OK') ||
            content.startsWith('HEARTBEAT_') ||
            content.includes('Conversation info (untrusted metadata)') || // 微信系统元数据
            content.startsWith('System (untrusted)') || // 系统消息
            content.startsWith('Queued messages') || // 队列消息头
            content.length < 10; // 过滤太短的消息
          if (isHeartbeatTemplate) continue;
          
          if (role === 'user') {
            turnCount++;
            userMessages.push(content);
            
            // 检测"记住"关键词
            if (rules.rememberKeywords.some(kw => content.includes(kw))) {
              hasRemember = true;
            }
          } else if (role === 'assistant') {
            // 检测任务完成
            if (rules.taskCompletePatterns.some(p => content.includes(p))) {
              hasTaskComplete = true;
            }
          }
        } catch (e) {}
      }
      
      // 规则1: 轮次>10的高价值对话
      if (turnCount > rules.turnsThreshold) {
        const topic = userMessages.slice(0, 3).join(' ').slice(0, 100);
        const id = `auto-session-${file.mtime.toISOString().split('T')[0]}`;
        if (!existingIds.has(id)) {
          newMemories.push({
            id,
            title: `对话: ${topic.slice(0, 40)}...`,
            tags: ['自动检测', '对话'],
            type: 'exploration',
            layer: 'active',
            ttl: 7,
            created: file.mtime.toISOString().split('T')[0],
            lastActive: new Date().toISOString().split('T')[0],
            recallCount: 0,
            recallDays: [],
            turns: turnCount,
            status: 'active',
            summary: `多轮对话(${turnCount}轮): ${topic}`,
            autoDetected: true,
          });
        }
      }
      
      // 规则2: 用户说"记住" → settled层
      if (hasRemember && userMessages.length > 0) {
        const rememberMsg = userMessages.find(m => rules.rememberKeywords.some(kw => m.includes(kw)));
        const id = `auto-remember-${file.mtime.toISOString().replace(/[:.]/g, '-')}`;
        if (!existingIds.has(id)) {
          newMemories.push({
            id,
            title: `用户记忆: ${rememberMsg?.slice(0, 60) || '重要信息'}`,
            tags: ['用户标记', '重要'],
            type: 'short',
            layer: 'settled',
            ttl: 90,
            created: new Date().toISOString().split('T')[0],
            lastActive: new Date().toISOString().split('T')[0],
            recallCount: 0,
            recallDays: [],
            turns: 1,
            status: 'active',
            summary: rememberMsg?.slice(0, 200) || '用户要求记住的重要信息',
            autoDetected: true,
          });
        }
      }
      
      // 规则3: 检测任务完成 → 标记completed
      if (hasTaskComplete) {
        const completedIds = loadIndex().memories
          .filter(m => m.status === 'active' && m.autoDetected)
          .map(m => m.id);
        // 交给主流程处理
      }
    }
  } catch (e) {
    console.warn('⚠️ 自动写入检测出错:', e.message);
  }
  
  return newMemories;
}

// ==========================================
// 梦境核心流程
// ==========================================
async function dreamCycle() {
  console.log('💤 梦境模式 v1.1 开始...\n');
  
  const index = loadIndex();
  let memories = index.memories || [];
  const today = new Date().toISOString().split('T')[0];
  
  let consolidated = 0, archived = 0, forgotten = 0, mergedCount = 0, autoWritten = 0;
  
  // 0. 自动写入检测 (v1.1 新增)
  logDream('执行自动写入检测...', 'autowrite');
  const newMemories = detectNewMemoriesFromSessions();
  if (newMemories.length > 0) {
    for (const mem of newMemories) {
      // 检查是否与已有记忆重复
      const similar = findSimilarMemories(mem, memories, 0.7);
      if (similar.length === 0) {
        memories.push(mem);
        logDream(`自动写入: ${mem.title} (${mem.layer}层)`, 'autowrite');
        autoWritten++;
      }
    }
  }
  if (autoWritten === 0) {
    logDream('无新记忆需要自动写入', 'autowrite');
  }
  
  // 1. 巩固检查
  logDream('开始巩固检查...', 'info');
  for (const mem of memories) {
    const recallCount = mem.recallCount || 0;
    const currentLayer = mem.layer;
    
    if (recallCount >= 3 && currentLayer === 'flash') {
      mem.layer = 'active';
      mem.ttl = 7;
      logDream(`巩固：${mem.title} (flash→active, recall=${recallCount})`, 'consolidate');
      consolidated++;
    } else if (recallCount >= 5 && currentLayer === 'active') {
      mem.layer = 'attention';
      mem.ttl = 30;
      logDream(`巩固：${mem.title} (active→attention, recall=${recallCount})`, 'consolidate');
      consolidated++;
    } else if (recallCount >= 10 && currentLayer === 'attention') {
      mem.layer = 'settled';
      mem.ttl = 90;
      logDream(`巩固：${mem.title} (attention→settled, recall=${recallCount})`, 'consolidate');
      consolidated++;
    }
  }
  
  // 2. 归档/遗忘检查
  logDream('开始归档/遗忘检查...', 'info');
  for (let i = memories.length - 1; i >= 0; i--) {
    const mem = memories[i];
    const lastActive = mem.lastActive || mem.created;
    const ttl = mem.ttl || 7;
    const daysSince = Math.floor((new Date(today) - new Date(lastActive)) / (1000 * 60 * 60 * 24));
    
    if (daysSince >= ttl) {
      if (mem.layer === 'flash') {
        memories.splice(i, 1);
        logDream(`遗忘：${mem.title} (${daysSince}天过期)`, 'forget');
        forgotten++;
      } else {
        let archive = '';
        if (fs.existsSync(ARCHIVE_PATH)) {
          archive = fs.readFileSync(ARCHIVE_PATH, 'utf-8');
        }
        const category = mem.tags?.[0] || '其他';
        const archiveEntry = `- [${mem.lastActive}] ${mem.title}\n  状态：${mem.status || 'unknown'} | 概括：${(mem.summary || '').slice(0, 100)}`;
        
        if (!archive.includes(`## ${category}`)) {
          archive += `\n## ${category}\n\n${archiveEntry}\n`;
        } else {
          archive = archive.replace(
            `## ${category}\n\n`,
            `## ${category}\n\n${archiveEntry}\n`
          );
        }
        fs.writeFileSync(ARCHIVE_PATH, archive);
        
        memories.splice(i, 1);
        logDream(`归档：${mem.title} → archive.md (${daysSince}天过期)`, 'archive');
        archived++;
      }
    }
  }
  
  // 3. 合并检查
  logDream('开始合并检查...', 'info');
  const toMerge = [];
  for (let i = 0; i < memories.length; i++) {
    for (let j = i + 1; j < memories.length; j++) {
      // Bug fix: 带remindAt的提醒记忆不参与合并，避免提醒时间丢失
      if (memories[i].remindAt || memories[j].remindAt) continue;
      const sim = findSimilarMemories(memories[i], [memories[j]], 0.6);
      if (sim.length > 0 && sim[0].canMerge) {
        toMerge.push([i, j, sim[0].similarity]);
      }
    }
  }
  
  toMerge.sort((a, b) => b[2] - a[2]);
  const mergedIds = new Set();
  for (const [i, j, sim] of toMerge) {
    if (!mergedIds.has(i) && !mergedIds.has(j)) {
      const merged = mergeMemories(memories[i], memories[j]);
      logDream(`合并：${memories[i].title} + ${memories[j].title} (相似度${(sim*100).toFixed(0)}%)`, 'merge');
      memories[i] = merged;
      mergedIds.add(j);
      mergedCount++;
    }
  }
  index.memories = memories.filter((_, i) => !mergedIds.has(i));
  saveIndex(index);
  
  // 4. 搜索session日志补充上下文
  logDream('搜索session日志...', 'info');
  try {
    const recentSummary = getRecentSessionSummary(60, 5);
    if (recentSummary.length > 0) {
      logDream(`从session日志找到 ${recentSummary.length} 条最近对话`, 'info');
    }
  } catch (e) {
    logDream('session日志搜索跳过（无权限或路径不存在）', 'info');
  }
  
  // 完成
  logDream('梦境模式完成', 'complete');
  logDream(`统计：巩固${consolidated}条 归档${archived}条 遗忘${forgotten}条 合并${mergedCount}条 自动写入${autoWritten}条`, 'info');
  
  console.log('\n💤 梦境结束，下次检查将在下次心跳触发');
}

dreamCycle().catch(err => {
  console.error('梦境模式出错:', err);
  process.exit(1);
});
