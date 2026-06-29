#!/usr/bin/env node
/**
 * Multi-Engine Search Script (Node.js版本)
 * 无需Python，安装即用
 * 
 * 用法和Python版完全兼容：
 * node multi-search.js "搜索关键词" [--max-results 20] [--engine bing-cn] [--all-engines]
 */

const fs = require('fs');
const path = require('path');
const FreeSearch = require('./free-search');

// 解析命令行参数
const args = process.argv.slice(2);
let keyword = '';
let maxResults = 10;
let engine = 'free';
let showAllEngines = false;

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--max-results' && args[i+1]) {
        maxResults = parseInt(args[i+1]);
        i++;
    } else if (args[i] === '--engine' && args[i+1]) {
        engine = args[i+1];
        i++;
    } else if (args[i] === '--all-engines') {
        showAllEngines = true;
    } else if (!keyword) {
        keyword = args[i];
    }
}

// 显示帮助
if (!keyword || args.includes('--help') || args.includes('-h')) {
    console.log("🔍 Search Pro - 多引擎搜索工具（Node.js版本）");
    console.log("=".repeat(50));
    console.log("无需Python，无需API Key，安装即用");
    console.log("\n用法:");
    console.log("  node multi-search.js \"搜索关键词\" [选项]");
    console.log("\n选项:");
    console.log("  --max-results <数量>   最多返回多少条结果（默认10）");
    console.log("  --engine <引擎>       指定搜索引擎：bing-cn/sogou/so360/free（默认auto）");
    console.log("  --all-engines         显示结果来源引擎");
    console.log("  --help/-h             显示帮助");
    console.log("\n示例:");
    console.log("  node multi-search.js \"OpenClaw 技能\"");
    console.log("  node multi-search.js \"Python 教程\" --max-results 20");
    console.log("  node multi-search.js \"今天天气\" --engine bing-cn");
    console.log("\n可用引擎：");
    console.log("  free    自动选择最优引擎（默认）");
    console.log("  bing-cn 必应中国");
    console.log("  sogou   搜狗搜索");
    console.log("  so360   360搜索");
    process.exit(0);
}

// 主函数
async function main() {
    console.log("🔍 Search Pro - 多引擎搜索工具");
    console.log("=".repeat(50));
    console.log(`🔎 搜索关键词: ${keyword}`);
    console.log(`🚀 引擎: ${engine === 'free' ? '自动选择' : engine}`);
    console.log(`📊 最大结果数: ${maxResults}`);
    console.log();
    
    const searcher = new FreeSearch();
    const results = await searcher.search(keyword, maxResults, engine);
    
    if (results.length === 0) {
        console.log("❌ 未找到相关结果，请尝试其他关键词或引擎");
        process.exit(1);
    }
    
    console.log(`✅ 找到 ${results.length} 条结果：`);
    console.log();
    
    results.forEach((item, index) => {
        console.log(`${index + 1}. ${item.title}`);
        console.log(`   🔗 ${item.url}`);
        console.log(`   📄 ${item.snippet.substring(0, 150)}${item.snippet.length > 150 ? '...' : ''}`);
        if (showAllEngines) {
            console.log(`   🛠️  来源: ${item.engine}`);
        }
        console.log();
    });
    
    console.log("=".repeat(50));
    console.log("💡 提示: 使用 --all-engines 参数可查看每条结果的来源引擎");
}

main().catch(err => {
    console.error("❌ 搜索失败:", err.message);
    process.exit(1);
});
