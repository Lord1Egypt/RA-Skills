#!/usr/bin/env node

/**
 * session-filters.js - Session 过滤工具
 * 
 * 负责过滤 sessions（日期范围、已处理、格式兼容性等）
 */

/**
 * 过滤 sessions（日期范围、已处理、格式兼容性、自身 subagent 排除）
 * 
 * @param {Array} sessions - sessions 列表
 * @param {Set} processedIds - 已处理的 session IDs
 * @param {Object} config - 配置对象
 * @param {Set|Array} [ownSubagentIds] - heartbeat-memory 自身产生的 subagent session IDs（可选）
 * @returns {Object} { validSessions, newSessions, skippedCount }
 */
function filterSessions(sessions, processedIds, config, ownSubagentIds) {
  // Issue #5 修复：兼容不同 OpenClaw 版本的 session 字段
  const validSessions = sessions.filter(s => {
    // 至少需要一个标识字段
    const hasId = s.sessionKey || s.sessionId || s.key || s.id;
    // 至少需要一个内容来源（transcriptPath 或 messages）
    const hasContent = s.transcriptPath || s.messages || s.history;
    return hasId && hasContent;
  });
  
  const skippedCount = sessions.length - validSessions.length;
  if (skippedCount > 0) {
    console.log(`⚠️  跳过 ${skippedCount} 个格式不兼容的 sessions`);
  }
  
  // 过滤掉 subagent session（避免 heartbeat 自身的 subagent 被下一轮当作"新 session"处理，造成无限递归空转）
  const ownIds = ownSubagentIds instanceof Set ? ownSubagentIds : new Set(ownSubagentIds || []);
  const nonSubagentSessions = validSessions.filter(s => {
    const key = s.sessionKey || s.key || '';
    const id = s.sessionId || s.id || '';
    // 1. 排除 key 中含 :subagent: 的（标准格式）
    if (key.includes(':subagent:')) {
      return false;
    }
    // 2. 排除 kind 标记为 subagent/heartbeat 的
    if (s.kind === 'subagent' || s.kind === 'heartbeat') {
      return false;
    }
    // 3. 排除 heartbeat-memory 自身追踪的 subagent IDs（纯 UUID 格式也能命中）
    if (ownIds.has(key) || ownIds.has(id)) {
      return false;
    }
    return true;
  });

  const skippedSubagents = validSessions.length - nonSubagentSessions.length;
  if (skippedSubagents > 0) {
    console.log(`⏭️  跳过 ${skippedSubagents} 个 subagent sessions（内部会话，非用户交互）`);
  }

  const newSessions = nonSubagentSessions.filter(s => {
    const id = s.sessionKey || s.sessionId || s.key || s.id;
    if (!id || processedIds.has(id)) return false;
    
    // Issue #6 修复：日期范围过滤
    if (config.memorySave?.processSessionsAfter) {
      const cutoffDate = new Date(config.memorySave.processSessionsAfter);
      const sessionDate = s.updatedAt || s.modified || s.createdAt;
      if (sessionDate) {
        const sessionTime = new Date(sessionDate);
        if (sessionTime < cutoffDate) {
          console.log(`  ⏭️  跳过 ${id.substring(0, 20)}... (早于 ${config.memorySave.processSessionsAfter})`);
          return false;
        }
      }
    }
    
    return true;
  });

  return { validSessions, newSessions, skippedCount };
}

/**
 * 限制 sessions 处理数量（防止 OOM）
 * 
 * @param {Array} sessions - sessions 列表
 * @param {number} maxSessions - 最大处理数量
 * @returns {Object} { limitedSessions, remainingCount }
 */
function limitSessions(sessions, maxSessions = 50) {
  if (sessions.length <= maxSessions) {
    return { limitedSessions: sessions, remainingCount: 0 };
  }
  
  const remainingCount = sessions.length - maxSessions;
  console.log(`⚠️  限制处理数量：${maxSessions} 个（剩余 ${remainingCount} 个下次处理）`);
  
  return {
    limitedSessions: sessions.slice(0, maxSessions),
    remainingCount
  };
}

// 导出
module.exports = {
  filterSessions,
  limitSessions
};
