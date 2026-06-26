#!/usr/bin/env node
/**
 * 🎯 Memory Core 快速启动示例
 */

const { quickStart } = require('../index');

async function main() {
  console.log('🚀 Memory Core 快速示例');
  
  try {
    // 1. 快速启动
    const memoryCore = await quickStart({
      verbose: true,
      apiKey: process.env.EDGEFN_API_KEY
    });
    
    // 2. 添加一些示例记忆
    console.log('\n📝 添加示例记忆...');
    
    const memories = [
      'Worldcoin (WLD) 是解决 AI 时代身份验证的关键基础设施',
      'Moltbook 是 AI Agent 的社交平台，展示了 AI 社会的形成',
      '向量搜索比传统关键词搜索更理解语义意图',
      'OpenClaw 是一个强大的 AI 助手框架'
    ];
    
    for (const content of memories) {
      const memory = await memoryCore.addMemory(content, {
        source: 'example',
        category: '技术'
      });
      console.log(`   ✅ 添加: ${content.substring(0, 40)}...`);
    }
    
    // 3. 测试搜索
    console.log('\n🔍 测试语义搜索...');
    
    const testQueries = [
      'AI 身份验证',
      '向量搜索的优势',
      'Moltbook 是什么'
    ];
    
    for (const query of testQueries) {
      console.log(`\n  搜索: "${query}"`);
      const result = await memoryCore.search(query, {
        topKFinal: 2
      });
      
      if (result.success) {
        console.log(`   ✅ 找到 ${result.results.length} 个结果:`);
        result.results.forEach((r, i) => {
          console.log(`     ${i + 1}. [${r.score.toFixed(4)}] ${r.preview}`);
        });
      } else {
        console.log(`   ❌ 搜索失败: ${result.error}`);
      }
    }
    
    // 4. 显示系统信息
    console.log('\n📊 系统统计:');
    const info = memoryCore.getInfo();
    console.log(JSON.stringify(info, null, 2));
    
    console.log('\n🎉 示例完成！');
    
  } catch (error) {
    console.error('❌ 示例失败:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = main;
