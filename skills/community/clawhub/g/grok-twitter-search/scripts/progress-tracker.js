#!/usr/bin/env node
/**
 * 进度跟踪器 - 自动编辑 Telegram 消息显示任务进度
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const STATE_FILE = path.join(__dirname, '.progress-state.json');

function loadState() {
    if (fs.existsSync(STATE_FILE)) {
        return JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
    }
    return { messageId: null, total: 0, current: 0 };
}

function saveState(state) {
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function sendMessage(message) {
    const cmd = `message action=send target=6287092183 message="${message}"`;
    const output = execSync(cmd, { encoding: 'utf-8' });
    // 解析返回的 messageId (实际需要从输出中提取)
    const match = output.match(/messageId["\s:]+(\d+)/);
    return match ? match[1) : null;
}

function editMessage(messageId, message) {
    const cmd = `message action=edit messageId=${messageId} message="${message}"`;
    execSync(cmd, { encoding: 'utf-8', stdio: 'ignore' });
}

function startProgress(task, total) {
    const state = { messageId: null, task, total, current: 0 };
    const message = `📊 **${task}**\n进度：0% (0/${total})`;
    
    console.log('发送初始进度消息...');
    const messageId = sendMessage(message);
    
    if (messageId) {
        state.messageId = messageId;
        saveState(state);
        console.log(`✅ 进度消息已发送 (ID: ${messageId})`);
    } else {
        console.error('❌ 发送失败');
    }
}

function updateProgress(current) {
    const state = loadState();
    if (!state.messageId) {
        console.error('❌ 没有活动的进度跟踪');
        return;
    }
    
    state.current = current;
    const percent = Math.round((current / state.total) * 100);
    const message = `📊 **${state.task}**\n进度：${percent}% (${current}/${state.total})`;
    
    console.log(`更新进度到 ${percent}%...`);
    editMessage(state.messageId, message);
    saveState(state);
}

function completeProgress() {
    const state = loadState();
    if (!state.messageId) {
        console.error('❌ 没有活动的进度跟踪');
        return;
    }
    
    const message = `✅ **${state.task}**\n完成！ (${state.total}/${state.total})`;
    editMessage(state.messageId, message);
    
    // 清除状态
    fs.unlinkSync(STATE_FILE);
    console.log('✅ 任务完成！');
}

// 命令行接口
const command = process.argv[2];
if (command === 'start') {
    const task = process.argv[3] || '当前任务';
    const total = parseInt(process.argv[4]) || 5;
    startProgress(task, total);
} else if (command === 'update') {
    const current = parseInt(process.argv[3]);
    updateProgress(current);
} else if (command === 'complete') {
    completeProgress();
} else {
    console.log(`用法：
  progress start <任务名> <总步数>   - 开始进度跟踪
  progress update <当前步数>        - 更新进度
  progress complete                 - 完成任务
`);
}
