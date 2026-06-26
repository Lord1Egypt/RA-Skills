#!/usr/bin/env node
/**
 * 自动日报脚本
 * 
 * 职责：
 * - 由 OpenClaw Cron 定时触发（UTC 23:00 = 北京时间 07:00）
 * - 生成昨日积分日报
 * - 保存到本地文件
 * - 发送飞书消息到指定群聊
 * 
 * 注意：此脚本只读 balance.json，绝不修改数据
 */

const fs = require('fs');
const path = require('path');
const { generateDailyReport } = require('./report-generator');

const WORKSPACE = process.env.WORKSPACE || '/home/wang/.openclaw/agents/kids-study/workspace';
const REPORTS_DIR = path.join(WORKSPACE, 'kids-points', 'daily-reports');

// 飞书配置
const FEISHU_CHAT_ID = 'oc_7d968e918766825eb21d51ce45d7e043'; // 目标群聊

/**
 * 确保目录存在
 */
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

/**
 * 保存日报到文件
 */
function saveReport(report) {
  ensureDir(REPORTS_DIR);
  
  const dateStr = report.data.date;
  const filename = path.join(REPORTS_DIR, `${dateStr}.md`);
  
  const content = `# 昨日积分日报（${dateStr}）

生成时间：${new Date().toISOString()}

---

## 结构化消息

${report.message}

---

## TTS 朗读文本

${report.speechText}

---

## 原始数据

\`\`\`json
${JSON.stringify(report.data, null, 2)}
\`\`\`
`;
  
  fs.writeFileSync(filename, content);
  return filename;
}

/**
 * 保存消息到文件，供 OpenClaw Agent 发送
 */
function saveMessageForAgent(report) {
  const messageFile = '/tmp/kids-points-daily-message.json';
  const messageData = {
    chat_id: FEISHU_CHAT_ID,
    message: report.message,
    date: report.data.date,
    timestamp: new Date().toISOString()
  };
  fs.writeFileSync(messageFile, JSON.stringify(messageData, null, 2));
  return messageFile;
}

/**
 * 主函数
 */
async function main() {
  console.log('📊 开始生成昨日积分日报...');
  console.log('时间:', new Date().toISOString());
  
  try {
    // 1. 生成日报
    const report = generateDailyReport();
    
    if (!report.data) {
      console.log('⚠️ 无数据，跳过');
      process.exit(0);
    }
    
    console.log('✅ 日报生成成功');
    console.log('昨日日期:', report.data.date);
    console.log('收入:', report.data.totalIncome, '分');
    console.log('支出:', report.data.totalExpense, '分');
    
    // 2. 保存到文件
    const filename = saveReport(report);
    console.log('✅ 日报已保存到:', filename);
    
    // 3. 保存消息供 Agent 发送
    const messageFile = saveMessageForAgent(report);
    console.log('✅ 消息已保存到:', messageFile);
    console.log('📤 目标群聊:', FEISHU_CHAT_ID);
    
    // 4. 同时输出到 stdout（方便 cron 日志查看）
    console.log('\n--- 日报内容 ---');
    console.log(report.message);
    console.log('\n--- TTS 文本 ---');
    console.log(report.speechText);
    
    console.log('\n✅ 日报生成完成');
    console.log('💡 提示: 消息已保存到', messageFile);
    console.log('   请配置 OpenClaw Agent 读取该文件并发送飞书消息');
    
  } catch (error) {
    console.error('❌ 日报生成失败:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// 执行
main();
