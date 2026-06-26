#!/usr/bin/env node

/**
 * Multi-User Long-Term Memory Manager
 * 多用户长期记忆管理
 *
 * 用户标识规则：从 sender_id 中提取 | 符号以前的部分作为用户名
 */

const fs = require('fs');
const path = require('path');

// 记忆存储目录
const USERS_DIR = path.join(__dirname, '..', 'users');

// 确保目录存在
function ensureDir() {
  if (!fs.existsSync(USERS_DIR)) {
    fs.mkdirSync(USERS_DIR, { recursive: true });
  }
}

/**
 * 从 senderId 中提取用户名
 * 规则：取 | 符号以前的部分
 * @param {string} senderId - 发送者ID（如 "hzg-demo-appWillNing|s-24485376"）
 * @returns {string} 用户名
 */
function extractUsername(senderId) {
  if (!senderId) {
    return 'unknown';
  }
  // 取 | 前的部分，如果没有 | 则使用全部
  const username = senderId.split('|')[0];
  // 清理文件名，移除不安全的字符
  return username.replace(/[^a-zA-Z0-9_-]/g, '_');
}

/**
 * 获取用户记忆文件路径
 * @param {string} senderId - 发送者ID
 * @returns {string} 记忆文件路径
 */
function getUserMemoryPath(senderId) {
  const username = extractUsername(senderId);
  return path.join(USERS_DIR, `${username}.md`);
}

/**
 * 获取用户记忆
 * @param {string} userId - 用户ID
 * @returns {string} 用户记忆内容，如果不存在返回空字符串
 */
function get(userId) {
  ensureDir();
  const memoryPath = getUserMemoryPath(userId);

  if (fs.existsSync(memoryPath)) {
    return fs.readFileSync(memoryPath, 'utf-8');
  }
  return '';
}

/**
 * 保存用户记忆（覆盖）
 * @param {string} userId - 用户ID
 * @param {string} content - 记忆内容
 */
function save(userId, content) {
  ensureDir();
  const memoryPath = getUserMemoryPath(userId);
  fs.writeFileSync(memoryPath, content, 'utf-8');
}

/**
 * 追加用户记忆
 * @param {string} userId - 用户ID
 * @param {string} content - 要追加的内容
 */
function append(userId, content) {
  ensureDir();
  const memoryPath = getUserMemoryPath(userId);

  let existingContent = '';
  if (fs.existsSync(memoryPath)) {
    existingContent = fs.readFileSync(memoryPath, 'utf-8');
  }

  const timestamp = new Date().toISOString();
  const newEntry = `\n\n## ${timestamp}\n${content}`;

  fs.writeFileSync(memoryPath, existingContent + newEntry, 'utf-8');
}

/**
 * 初始化用户记忆文件
 * @param {string} senderId - 发送者ID
 * @param {string} displayName - 显示名称（可选）
 */
function init(senderId, displayName = '') {
  ensureDir();
  const memoryPath = getUserMemoryPath(senderId);
  const username = extractUsername(senderId);

  if (!fs.existsSync(memoryPath)) {
    const header = `# Memory for User: ${displayName || username}\n\nUsername: ${username}\nSender ID: ${senderId}\nCreated: ${new Date().toISOString()}\n\n---\n\n`;
    fs.writeFileSync(memoryPath, header, 'utf-8');
  }
}

// CLI接口
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'get':
      if (args[1]) {
        console.log(get(args[1]));
      } else {
        console.error('Usage: user-memory.js get <userId>');
        process.exit(1);
      }
      break;

    case 'save':
      if (args[1] && args[2]) {
        save(args[1], args[2]);
        console.log('Saved.');
      } else {
        console.error('Usage: user-memory.js save <userId> <content>');
        process.exit(1);
      }
      break;

    case 'append':
      if (args[1] && args[2]) {
        append(args[1], args[2]);
        console.log('Appended.');
      } else {
        console.error('Usage: user-memory.js append <userId> <content>');
        process.exit(1);
      }
      break;

    case 'init':
      if (args[1]) {
        init(args[1], args[2] || '');
        console.log('Initialized.');
      } else {
        console.error('Usage: user-memory.js init <userId> [userName]');
        process.exit(1);
      }
      break;

    default:
      console.log(`
Multi-User Long-Term Memory Manager
Usage: user-memory.js <command> [args...]

Commands:
  get <userId>           - 获取用户记忆内容
  save <userId> <content> - 保存用户记忆（覆盖）
  append <userId> <content> - 追加用户记忆
  init <userId> [name]   - 初始化用户记忆文件
      `);
  }
}

module.exports = { get, save, append, init };
