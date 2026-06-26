/**
 * Auto Load Memory Hook
 * Session start时自动加载核心记忆到上下文
 */
const fs = require('fs').promises;
const path = require('path');

exports.handler = async (event) => {
  const workspaceDir = process.env.OPENCLAW_WORKSPACE || '/root/.openclaw/workspace';
  const memoryDir = path.join(workspaceDir, 'memory');
  const logs = [];

  try {
    // 1. Read MEMORY.md
    const memoryPath = path.join(workspaceDir, 'MEMORY.md');
    try {
      const memory = await fs.readFile(memoryPath, 'utf-8');
      logs.push(`Loaded MEMORY.md (${memory.length} chars)`);
    } catch {
      logs.push('MEMORY.md not found, skipping');
    }

    // 2. Read today's short-term memory
    const today = new Date().toISOString().split('T')[0];
    const todayPath = path.join(memoryDir, 'short-term', `${today}.md`);
    try {
      const todayLog = await fs.readFile(todayPath, 'utf-8');
      logs.push(`Loaded today's short-term: ${today}.md (${todayLog.length} chars)`);
    } catch {
      logs.push('Today short-term not found, skipping');
    }

    // 3. Read preferences abstract
    const prefAbstract = path.join(memoryDir, 'user', 'preferences', '.abstract.md');
    try {
      const prefs = await fs.readFile(prefAbstract, 'utf-8');
      logs.push(`Loaded preferences abstract (${prefs.length} chars)`);
    } catch {
      logs.push('Preferences abstract not found, skipping');
    }

    return { logs, memory: logs.join(' | ') };
  } catch (err) {
    return { logs: [`Error: ${err.message}`] };
  }
};
