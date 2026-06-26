#!/usr/bin/env node
/**
 * 读取日报消息文件并发送到飞书
 * 由 OpenClaw Cron 调用
 */

const fs = require('fs');
const path = require('path');

const MESSAGE_FILE = '/tmp/kids-points-daily-message.json';
const CHAT_ID = 'oc_7d968e918766825eb21d51ce45d7e043';

async function main() {
  console.log('📤 开始发送 Kids 积分日报...');
  console.log('时间:', new Date().toISOString());
  
  // 检查消息文件是否存在
  if (!fs.existsSync(MESSAGE_FILE)) {
    console.log('⚠️ 消息文件不存在，跳过发送');
    console.log('   文件路径:', MESSAGE_FILE);
    process.exit(0);
  }
  
  try {
    // 读取消息数据
    const messageData = JSON.parse(fs.readFileSync(MESSAGE_FILE, 'utf8'));
    const { message, date } = messageData;
    
    console.log('📋 消息日期:', date);
    console.log('💬 目标群聊:', CHAT_ID);
    
    // 构建完整消息
    const fullMessage = `📊 ${date} 积分日报

${message}

*Kids 积分系统自动生成*`;
    
    // 输出消息内容（供 OpenClaw Agent 读取并发送）
    console.log('\n========== 消息内容 ==========');
    console.log(fullMessage);
    console.log('========== 消息结束 ==========\n');
    
    // 保存到另一个文件，供 OpenClaw 工具读取
    const sendFile = '/tmp/kids-points-send-ready.txt';
    fs.writeFileSync(sendFile, fullMessage);
    console.log('✅ 消息已准备，保存到:', sendFile);
    console.log('📤 请使用 message 工具发送:');
    console.log('   chatId:', CHAT_ID);
    console.log('   message: (见上文)');
    
    // 删除原始消息文件（防止重复发送）
    fs.unlinkSync(MESSAGE_FILE);
    console.log('🗑️ 已删除原始消息文件');
    
    console.log('\n✅ 准备完成，等待 OpenClaw 发送...');
    
  } catch (error) {
    console.error('❌ 发送准备失败:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

main();
