#!/usr/bin/env node
/**
 * 龙虾记忆大师 - 自动归档脚本
 * Created by: 天道桐哥 & AI龙虾元龙
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || '/root/.openclaw/workspace';
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const BUFFER_FILE = path.join(MEMORY_DIR, 'working-buffer.md');

function getTodayFile() {
  const today = new Date().toISOString().split('T')[0];
  return path.join(MEMORY_DIR, `${today}.md`);
}

function archiveMemory() {
  console.log('🦞 龙虾记忆大师 - 自动归档');
  console.log('========================');
  
  // Ensure memory directory exists
  if (!fs.existsSync(MEMORY_DIR)) {
    fs.mkdirSync(MEMORY_DIR, { recursive: true });
    console.log('✅ 创建 memory 目录');
  }
  
  // Read working buffer
  let buffer = '';
  try {
    buffer = fs.readFileSync(BUFFER_FILE, 'utf8');
  } catch {
    console.log('⚠️ Working buffer 不存在，创建新的');
    buffer = '# Working Buffer\n\n**Status:** EMPTY\n';
    fs.writeFileSync(BUFFER_FILE, buffer);
  }
  
  // Check if there's content to archive
  if (buffer.includes('Status: CLEARED') || buffer.includes('Status: EMPTY')) {
    console.log('ℹ️ 没有需要归档的内容');
    return;
  }
  
  // Archive to today's file
  const archiveFile = getTodayFile();
  const timestamp = new Date().toISOString();
  const archiveContent = `\n\n<!-- Archived at ${timestamp} -->\n${buffer}`;
  
  fs.appendFileSync(archiveFile, archiveContent);
  console.log(`✅ 已归档到: ${path.basename(archiveFile)}`);
  
  // Clear working buffer
  fs.writeFileSync(BUFFER_FILE, `# Working Buffer\n\n**Status:** CLEARED\n**Cleared At:** ${timestamp}\n`);
  console.log('✅ 已清空 Working Buffer');
  
  console.log('========================');
  console.log('🎉 归档完成！');
}

// Run if called directly
if (require.main === module) {
  archiveMemory();
}

module.exports = { archiveMemory };
