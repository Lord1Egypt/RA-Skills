#!/usr/bin/env node

/**
 * memory-master 压缩检测 - 精简版
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const WORKSPACE = process.env.WORKSPACE || path.join(os.homedir(), '.openclaw', 'workspace');

// 快速估算：只统计核心文件
function estimate() {
    let chars = 0;
    
    const files = [
        path.join(WORKSPACE, 'AGENTS.md'),
        path.join(WORKSPACE, 'MEMORY.md'),
        path.join(WORKSPACE, 'memory/daily'),
        path.join(WORKSPACE, 'memory/knowledge')
    ];
    
    for (const f of files.slice(0, 2)) {
        if (fs.existsSync(f)) chars += fs.statSync(f).size;
    }
    
    // 最近7天记忆
    const daily = files[2];
    if (fs.existsSync(daily)) {
        fs.readdirSync(daily).slice(-7).forEach(file => {
            chars += fs.statSync(path.join(daily, file)).size;
        });
    }
    
    // 知识库前5个
    const kb = files[3];
    if (fs.existsSync(kb)) {
        fs.readdirSync(kb).filter(f => f.endsWith('.md')).slice(0, 5).forEach(file => {
            chars += fs.statSync(path.join(kb, file)).size;
        });
    }
    
    return Math.round((chars / 200000) * 100);
}

const percent = estimate();

if (percent >= 85) {
    console.log('🚨 使用率85%，请立即记录当前进度！');
} else if (percent >= 70) {
    console.log('⚠️ 使用率70%，建议记录当前进度');
} else if (percent >= 50) {
    console.log('📝 使用率50%，是否需要记录记忆或知识库？');
} else {
    console.log('✅ 安全');
}
