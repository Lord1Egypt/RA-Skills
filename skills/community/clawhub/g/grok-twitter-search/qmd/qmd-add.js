#!/usr/bin/env node
/**
 * QMD - 添加记忆并重建索引
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function addMemory(content, memType = 'daily') {
    const workspace = process.env.WORKSPACE || '/Users/ben/.openclaw/workspace';
    const memoryDir = path.join(workspace, 'memory');
    
    // 确保目录存在
    if (!fs.existsSync(memoryDir)) {
        fs.mkdirSync(memoryDir, { recursive: true });
    }
    
    // 写入今日记忆文件
    const today = new Date().toISOString().split('T')[0];
    const filePath = path.join(memoryDir, `${today}.md`);
    
    let fileContent = '';
    if (fs.existsSync(filePath)) {
        fileContent = fs.readFileSync(filePath, 'utf-8');
    }
    
    fileContent += `\n\n## ${new Date().toLocaleTimeString('zh-CN')}\n${content}\n`;
    fs.writeFileSync(filePath, fileContent.trim());
    
    console.log(`✅ 记忆已写入：${filePath}`);
    
    // 重建索引
    console.log('🔄 重建索引...');
    try {
        execSync('node qmd-index.js', { cwd: path.join(workspace, 'qmd'), stdio: 'inherit' });
    } catch (err) {
        console.error('❌ 重建索引失败:', err.message);
    }
}

// 从命令行获取内容
const content = process.argv.slice(2).join(' ');
if (!content) {
    console.log(JSON.stringify({ error: '请提供记忆内容', usage: 'qmd-add.js <记忆内容>' }));
    process.exit(1);
}

addMemory(content);
