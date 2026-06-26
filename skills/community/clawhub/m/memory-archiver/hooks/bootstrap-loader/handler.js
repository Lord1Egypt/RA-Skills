/**
 * Memory Bootstrap Load Hook
 * 
 * 事件：agent:bootstrap
 * 功能：OpenClaw 启动时自动加载记忆到 SESSION-STATE.md 缓存
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import * as fs from 'fs';

const execAsync = promisify(exec);

const handler = async (event) => {
  console.log('[MemoryBootstrapLoad] Event received:', event.type, event.action);
  
  // 只处理 bootstrap 事件
  if (event.type !== 'agent' || event.action !== 'bootstrap') {
    return;
  }
  
  const homeDir = process.env.HOME || '/root';
  const workspaceDir = path.join(homeDir, '.openclaw', 'workspace');
  const scriptPath = path.join(workspaceDir, 'skills', 'memory-archiver', 'scripts', 'memory-loader.js');
  
  // 检查脚本是否存在
  if (!fs.existsSync(scriptPath)) {
    console.log('[MemoryBootstrapLoad] 脚本不存在:', scriptPath);
    return;
  }
  
  try {
    console.log('[MemoryBootstrapLoad] 开始加载记忆到缓存...');
    const { stdout, stderr } = await execAsync(`bash "${scriptPath}"`);
    console.log('[MemoryBootstrapLoad] 加载完成:', stdout.trim());
    if (stderr) {
      console.log('[MemoryBootstrapLoad] 警告:', stderr.trim());
    }
  } catch (error) {
    console.log('[MemoryBootstrapLoad] 加载失败:', error.message);
  }
};

export default handler;
