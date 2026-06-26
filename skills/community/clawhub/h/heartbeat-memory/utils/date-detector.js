#!/usr/bin/env node

/**
 * date-detector.js - 日期自动检测工具
 * 
 * 负责自动检测 processSessionsAfter 日期
 * 优先使用最早的 session 日期，fallback 到 workspace 创建日期
 */

const fs = require('fs');
const path = require('path');

/**
 * 自动检测 processSessionsAfter 日期
 * 优先使用最早的 session 日期，fallback 到 workspace 创建日期
 * 
 * @param {string} workspacePath - 工作区路径
 * @param {Array} sessions - sessions 列表（可选）
 * @returns {string} ISO 日期或 null
 */
function autoDetectProcessSessionsAfter(workspacePath, sessions) {
  try {
    // 方案 1：从 sessions 中找最早的日期
    if (sessions && sessions.length > 0) {
      const dates = sessions
        .map(s => s.updatedAt || s.modified || s.createdAt)
        .filter(d => d)
        .map(d => new Date(d).getTime())
        .filter(t => !isNaN(t));
      
      if (dates.length > 0) {
        const earliest = new Date(Math.min(...dates));
        const isoDate = earliest.toISOString();
        console.log(`📅 从 sessions 检测到最早日期：${isoDate}`);
        return isoDate;
      }
    }
    
    // 方案 2：使用 workspace 创建日期（AGENTS.md 的 mtime）
    const agentsFile = path.join(workspacePath, 'AGENTS.md');
    if (fs.existsSync(agentsFile)) {
      const stats = fs.statSync(agentsFile);
      const createDate = new Date(stats.mtime);
      const isoDate = createDate.toISOString();
      console.log(`📅 从 AGENTS.md 检测到创建日期：${isoDate}`);
      return isoDate;
    }
    
    // 方案 3：使用 memory 目录创建日期
    const memoryDir = path.join(workspacePath, 'memory');
    if (fs.existsSync(memoryDir)) {
      const stats = fs.statSync(memoryDir);
      const createDate = new Date(stats.mtime);
      const isoDate = createDate.toISOString();
      console.log(`📅 从 memory 目录检测到创建日期：${isoDate}`);
      return isoDate;
    }
    
    // Fallback: 使用当前日期（向前推 7 天，避免处理太多历史）
    const fallbackDate = new Date();
    fallbackDate.setDate(fallbackDate.getDate() - 7);
    const isoDate = fallbackDate.toISOString();
    console.log(`📅 使用 Fallback 日期（当前日期 -7 天）: ${isoDate}`);
    return isoDate;
  } catch (e) {
    console.error('⚠️  自动检测日期失败:', e.message);
    // 最终 fallback: 使用当前日期向前推 7 天
    const fallbackDate = new Date();
    fallbackDate.setDate(fallbackDate.getDate() - 7);
    return fallbackDate.toISOString();
  }
}

// 导出
module.exports = {
  autoDetectProcessSessionsAfter
};
