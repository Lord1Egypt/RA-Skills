#!/usr/bin/env node
/**
 * Session Memory 会话跟踪脚本
 * 维护当前活跃会话笔记，会话结束后归档
 * 
 * 用法:
 *   node tracker.js --current          # 查看当前会话笔记
 *   node tracker.js --update "<内容>"   # 更新会话笔记
 *   node tracker.js --archive           # 归档当前会话
 *   node tracker.js --list             # 列出所有会话
 *   node tracker.js --init "<主题>"     # 初始化新会话
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const MEMORY_DIR = WORKSPACE + '/memory';
const SESSIONS_DIR = MEMORY_DIR + '/sessions';
const CURRENT_FILE = SESSIONS_DIR + '/.current-session.json';
const ARCHIVE_DIR = SESSIONS_DIR + '/archive';

// 确保目录存在
function ensureDirs() {
  [SESSIONS_DIR, ARCHIVE_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
}

// 读取当前会话元数据
function readCurrentSession() {
  try {
    return JSON.parse(fs.readFileSync(CURRENT_FILE, 'utf8'));
  } catch (e) {
    return null;
  }
}

// 保存当前会话元数据
function saveCurrentSession(meta) {
  fs.writeFileSync(CURRENT_FILE, JSON.stringify(meta, null, 2));
}

// 生成会话 ID
function generateSessionId() {
  return Date.now().toString(36) + Math.random().toString(36).substring(2, 8);
}

// 初始化新会话
function initSession(topic = '未命名会话') {
  ensureDirs();
  
  const sessionId = generateSessionId();
  const now = new Date().toISOString();
  const filepath = path.join(SESSIONS_DIR, `${sessionId}.md`);
  
  const meta = {
    sessionId,
    topic,
    startedAt: now,
    endedAt: null,
    filepath,
    messageCount: 0,
    lastUpdatedAt: now,
    archived: false
  };
  
  const content = `---
session_id: ${sessionId}
topic: ${topic}
started: ${now}
ended: 
message_count: 0
archived: false
---

# 会话笔记: ${topic}

## 关键决策


## 待办事项


## 重要发现


## 用户偏好


`;
  
  fs.writeFileSync(filepath, content, 'utf8');
  saveCurrentSession(meta);
  
  console.log(`[会话初始化] ID: ${sessionId}`);
  console.log(`  主题: ${topic}`);
  console.log(`  文件: ${filepath}`);
  return meta;
}

// 更新会话笔记
function updateSession(content, section = null) {
  const meta = readCurrentSession();
  
  if (!meta) {
    console.log('[提示] 无活跃会话，自动初始化...');
    initSession('自动会话 ' + new Date().toLocaleString('zh-CN'));
    return updateSession(content, section);
  }
  
  const filepath = meta.filepath;
  if (!fs.existsSync(filepath)) {
    console.log('[错误] 会话文件不存在');
    return;
  }
  
  let fileContent = fs.readFileSync(filepath, 'utf8');
  
  if (section) {
    // 更新指定部分
    const sectionRegex = new RegExp(`(## ${section}\\n)([\\s\\S]*?)(?=\\n## |$)`);
    if (sectionRegex.test(fileContent)) {
      fileContent = fileContent.replace(sectionRegex, `$1${content}\n`);
    } else {
      fileContent += `\n## ${section}\n\n${content}\n`;
    }
  } else {
    // 追加到末尾
    fileContent += `\n${content}\n`;
  }
  
  // 更新元数据
  meta.messageCount = (meta.messageCount || 0) + 1;
  meta.lastUpdatedAt = new Date().toISOString();
  saveCurrentSession(meta);
  
  // 更新文件中的 message_count
  fileContent = fileContent.replace(/message_count: \d+/, `message_count: ${meta.messageCount}`);
  fs.writeFileSync(filepath, fileContent, 'utf8');
  
  console.log(`[会话更新] +1 条笔记 (${meta.messageCount} 总计)`);
}

// 归档当前会话
function archiveSession() {
  const meta = readCurrentSession();
  
  if (!meta) {
    console.log('[提示] 无活跃会话');
    return;
  }
  
  const filepath = meta.filepath;
  if (!fs.existsSync(filepath)) {
    console.log('[错误] 会话文件不存在');
    return;
  }
  
  // 更新文件
  let content = fs.readFileSync(filepath, 'utf8');
  content = content
    .replace(/ended: \n/, `ended: ${new Date().toISOString()}\n`)
    .replace(/archived: false/, 'archived: true');
  
  // 移动到归档目录
  const archivePath = path.join(ARCHIVE_DIR, path.basename(filepath));
  fs.writeFileSync(archivePath, content, 'utf8');
  fs.unlinkSync(filepath);
  
  // 更新元数据
  meta.endedAt = new Date().toISOString();
  meta.archived = true;
  saveCurrentSession(meta);
  
  // 清除当前会话
  fs.unlinkSync(CURRENT_FILE);
  
  console.log(`[会话归档] ${meta.sessionId}`);
  console.log(`  主题: ${meta.topic}`);
  console.log(`  笔记数: ${meta.messageCount}`);
  console.log(`  时长: ${((Date.now() - new Date(meta.startedAt).getTime()) / 60000).toFixed(0)} 分钟`);
  console.log(`  归档: ${archivePath}`);
}

// 列出所有会话
function listSessions() {
  ensureDirs();
  
  console.log('=== 活跃会话 ===');
  const current = readCurrentSession();
  if (current) {
    const duration = ((Date.now() - new Date(current.startedAt).getTime()) / 60000).toFixed(0);
    console.log(`📝 ${current.sessionId} - ${current.topic}`);
    console.log(`   开始: ${new Date(current.startedAt).toLocaleString('zh-CN')}`);
    console.log(`   笔记: ${current.messageCount} 条 | 时长: ${duration} 分钟`);
  } else {
    console.log('  无活跃会话');
  }
  
  console.log('\n=== 已归档会话 ===');
  if (fs.existsSync(ARCHIVE_DIR)) {
    const files = fs.readdirSync(ARCHIVE_DIR).filter(f => f.endsWith('.md'));
    if (files.length === 0) {
      console.log('  无归档会话');
    } else {
      for (const file of files.slice(-10).reverse()) { // 最近 10 个
        const filepath = path.join(ARCHIVE_DIR, file);
        const content = fs.readFileSync(filepath, 'utf8');
        const topicMatch = content.match(/^topic: (.+)$/m);
        const startedMatch = content.match(/^started: (.+)$/m);
        const countMatch = content.match(/^message_count: (\d+)$/m);
        
        const topic = topicMatch ? topicMatch[1] : '未命名';
        const started = startedMatch ? new Date(startedMatch[1]).toLocaleDateString('zh-CN') : '?';
        const count = countMatch ? countMatch[1] : '?';
        
        console.log(`📦 ${file} - ${topic}`);
        console.log(`   日期: ${started} | 笔记: ${count} 条`);
      }
    }
  }
}

// 查看当前会话笔记
function showCurrent() {
  const meta = readCurrentSession();
  
  if (!meta) {
    console.log('无活跃会话');
    return;
  }
  
  const filepath = meta.filepath;
  if (!fs.existsSync(filepath)) {
    console.log('会话文件不存在');
    return;
  }
  
  console.log(fs.readFileSync(filepath, 'utf8'));
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('用法:');
    console.log('  node tracker.js --init "<主题>"      初始化新会话');
    console.log('  node tracker.js --current             查看当前笔记');
    console.log('  node tracker.js --update "<内容>"     更新笔记');
    console.log('  node tracker.js --archive             归档会话');
    console.log('  node tracker.js --list                列出会话');
    process.exit(1);
  }
  
  if (args[0] === '--init' && args[1]) {
    initSession(args.slice(1).join(' '));
  } else if (args[0] === '--current') {
    showCurrent();
  } else if (args[0] === '--update' && args[1]) {
    const section = args.includes('--section') ? args[args.indexOf('--section') + 1] : null;
    updateSession(args.slice(1, args.indexOf('--section') !== -1 ? args.indexOf('--section') : undefined).join(' '), section);
  } else if (args[0] === '--archive') {
    archiveSession();
  } else if (args[0] === '--list') {
    listSessions();
  }
}

main();
