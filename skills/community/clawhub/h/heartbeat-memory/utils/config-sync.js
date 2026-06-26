#!/usr/bin/env node

/**
 * config-sync.js - HEARTBEAT.md 同步工具
 * 
 * 负责同步 HEARTBEAT.md 中的配置状态，仅在配置变更时更新
 */

const fs = require('fs');
const path = require('path');

/**
 * 同步 HEARTBEAT.md 配置状态
 * 只更新"记忆自动保存"部分，不管其他内容
 * 仅在配置变更时更新（通过 configHash 检测）
 * 
 * @param {Object} config - 配置对象
 * @param {string} workspacePath - 工作区路径
 */
function syncHeartbeatMD(config, workspacePath) {
  const heartbeatPath = path.join(workspacePath, 'HEARTBEAT.md');
  const workspaceName = path.basename(workspacePath);
  
  // 动态路径（使用 ~ 开头，更简洁）
  const configPath = `~/.openclaw/${workspaceName}/memory/heartbeat-memory-config.json`;
  const dailyDir = `~/.openclaw/${workspaceName}/memory/daily`;
  const memoryFile = `~/.openclaw/${workspaceName}/MEMORY.md`;
  const stateFile = `~/.openclaw/${workspaceName}/memory/heartbeat-state.json`;
  
  // 配置值
  const date = config.memorySave?.processSessionsAfter?.split('T')[0] || 'N/A';
  const maxSessions = config.memorySave?.maxSessionsPerRun || 20;
  const timeout = config.memorySave?.timeoutSeconds || 1000;
  
  // 新的"记忆自动保存"部分（干净简洁）
  const memorySection = `## 🧠 记忆自动保存
<!-- 此部分由 heartbeat-memory skill 自动维护，请勿手动修改 -->

- [x] 启用 heartbeat-memory Skill
- [x] 工作区：${workspaceName}
- [x] 配置：处理 ${date} 之后的 sessions
- [x] 配置：每次最多处理 ${maxSessions} 个 sessions
- [x] 配置：超时时间 ${timeout} 秒

**执行方式：** Heartbeat 触发时自动执行 heartbeat-memory Skill

**配置文件：** \`${configPath}\`

**输出位置：**
- Daily 笔记：\`${dailyDir}/YYYY-MM-DD.md\`
- 长期记忆：\`${memoryFile}\`
- 状态文件：\`${stateFile}\`

---
`;
  
  try {
    // 检查文件是否存在
    if (!fs.existsSync(heartbeatPath)) {
      // 创建最小模板（只有记忆自动保存部分）
      const content = `# HEARTBEAT.md - 心跳任务

${memorySection}
`;
      fs.writeFileSync(heartbeatPath, content, 'utf-8');
      console.log('✅ 创建 HEARTBEAT.md');
    } else {
      // 读取现有文件
      let content = fs.readFileSync(heartbeatPath, 'utf-8');
      
      // 使用正则替换"记忆自动保存"部分
      const sectionRegex = /## 🧠 记忆自动保存[\s\S]*?---\n/;
      if (sectionRegex.test(content)) {
        content = content.replace(sectionRegex, memorySection);
        console.log('✅ 更新 HEARTBEAT.md - 记忆自动保存部分');
      } else {
        // 如果没有该部分，插入到标题后
        content = content.replace(
          /^# HEARTBEAT.md - 心跳任务\n/,
          `# HEARTBEAT.md - 心跳任务

${memorySection}`
        );
        console.log('✅ 插入 HEARTBEAT.md - 记忆自动保存部分');
      }
      
      fs.writeFileSync(heartbeatPath, content, 'utf-8');
    }
  } catch (e) {
    console.error('⚠️  同步 HEARTBEAT.md 失败:', e.message);
  }
}

/**
 * 计算配置 hash（用于检测配置变更）
 * @param {Object} config - 配置对象
 * @returns {string} hash 值
 */
function computeConfigHash(config) {
  try {
    const crypto = require('crypto');
    const relevant = {
      enabled: config.memorySave?.enabled,
      processSessionsAfter: config.memorySave?.processSessionsAfter,
      maxSessionsPerRun: config.memorySave?.maxSessionsPerRun,
      timeoutSeconds: config.memorySave?.timeoutSeconds
    };
    return crypto.createHash('md5').update(JSON.stringify(relevant)).digest('hex');
  } catch (e) {
    // crypto 不可用时，使用简单 hash
    console.warn('⚠️  crypto 模块不可用，使用简单 hash');
    const str = JSON.stringify(config.memorySave || {});
    return Buffer.from(str).toString('base64').substring(0, 16);
  }
}

// 导出
module.exports = {
  syncHeartbeatMD,
  computeConfigHash
};
