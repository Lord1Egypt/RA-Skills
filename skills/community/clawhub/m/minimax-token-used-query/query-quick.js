#!/usr/bin/env node

/**
 * MiniMax Token Left Query - Quick Version
 * 直接从已打开的浏览器页面快速获取 token 使用量
 * 
 * 使用方式:
 *   node query-quick.js
 */

const { } = require('child_process');

 execSyncfunction run(command) {
    return execSync(command, { encoding: 'utf-8', shell: '/bin/bash' });
}

function getTokenUsage() {
    console.log('🔍 正在查询 MiniMax Token 使用情况...\n');
    
    try {
        // 直接从浏览器获取页面文本
        const pageText = run(`browser-use -b real --profile "Default" eval "document.body.innerText" 2>/dev/null`);
        
        // 提取使用百分比
        const usedMatch = pageText.match(/(\d+)% 已使用/);
        const usedPercent = usedMatch ? parseInt(usedMatch[1]) : null;
        
        // 提取重置分钟数
        const resetMatch = pageText.match(/(\d+) 分钟后重置/);
        const resetMinutes = resetMatch ? parseInt(resetMatch[1]) : null;
        
        // 提取时间窗口
        const timeMatch = pageText.match(/(\d+:\d+-\d+:\d+\(UTC\+\d+\))/);
        const timeWindow = timeMatch ? timeMatch[1] : null;
        
        // 提取可用额度
        const quotaMatch = pageText.match(/可用额度：(\d+) prompts/);
        const totalPrompts = quotaMatch ? parseInt(quotaMatch[1]) : null;
        
        if (usedPercent === null) {
            console.log('❌ 无法获取使用数据，页面可能未加载或未登录');
            console.log('\n请确保：');
            console.log('1. 已打开 MiniMax 账户管理页面');
            console.log('2. 已登录账号');
            return null;
        }
        
        // 输出结果
        console.log('📊 MiniMax Token 使用情况');
        console.log('═══════════════════════════');
        console.log(`已使用: ${usedPercent}%`);
        console.log(`重置剩余: ${resetMinutes} 分钟`);
        if (timeWindow) console.log(`时间窗口: ${timeWindow}`);
        if (totalPrompts) console.log(`可用额度: ${totalPrompts} prompts`);
        console.log('═══════════════════════════');
        
        // 警告
        if (usedPercent >= 90) {
            console.log('\n⚠️ 警告：Token 使用量已达 ' + usedPercent + '%！即将耗尽！');
        } else if (usedPercent >= 70) {
            console.log('\n⚡ 注意：Token 使用量已超 70%，请留意');
        }
        
        // 返回 JSON
        console.log('\n📄 JSON:');
        console.log(JSON.stringify({
            used_percent: usedPercent,
            reset_minutes: resetMinutes,
            time_window: timeWindow,
            total_prompts: totalPrompts,
            timestamp: new Date().toISOString()
        }, null, 2));
        
        return {
            used_percent: usedPercent,
            reset_minutes: resetMinutes,
            time_window: timeWindow,
            total_prompts: totalPrompts
        };
        
    } catch (error) {
        console.error('❌ 查询失败:', error.message);
        return null;
    }
}

// 运行
getTokenUsage();
