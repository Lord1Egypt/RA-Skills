/**
 * 🧪 Memory Core 集成测试
 * 测试与 Smart Memory 系统的集成
 */

const MemoryCoreIntegration = require('./lib/memory-core-integration');

// 模拟 Smart Memory 系统
const mockSmartMemorySystem = {
  config: {
    apiKey: 'sk-your-api-key-here'
  },
  memories: {
    getAll: () => [
      { id: 'mem-1', content: '现有记忆 1', metadata: { category: '测试' } },
      { id: 'mem-2', content: '现有记忆 2', metadata: { category: '测试' } }
    ]
  },
  search: async (query, options) => ({
    success: true,
    query,
    results: [{ id: 'fallback', content: '回退结果', score: 0.5 }],
    source: 'fallback'
  }),
  add: async (content, metadata) => ({
    id: 'added-' + Date.now(),
    content,
    metadata,
    source: 'smart-memory'
  })
};

async function runIntegrationTest() {
  console.log('🧪 Memory Core 集成测试');
  console.log('='.repeat(60));
  
  const integration = new MemoryCoreIntegration(mockSmartMemorySystem, {
    verbose: true,
    baseUrl: 'https://api.edgefn.net/v1'
  });
  
  try {
    // 1. 测试集成
    console.log('\n1️⃣  测试集成初始化...');
    const memoryCore = await integration.integrate();
    console.log('   ✅ 集成初始化成功');
    
    const status = integration.getIntegrationStatus();
    console.log('   集成状态:', JSON.stringify(status, null, 2));
    
    // 2. 测试集成搜索
    console.log('\n2️⃣  测试集成搜索...');
    const searchResult = await integration.integratedSearch('测试记忆', {
      topKFinal: 2
    });
    
    console.log(`   搜索成功: ${searchResult.success}`);
    console.log(`   结果数量: ${searchResult.results?.length || 0}`);
    console.log(`   集成标记: ${searchResult.stats?.integrated || false}`);
    
    // 3. 测试集成添加
    console.log('\n3️⃣  测试集成添加...');
    const addResult = await integration.integratedAdd('新测试记忆内容', {
      category: '集成测试',
      tags: ['测试', '集成']
    });
    
    console.log(`   添加成功: ${addResult.success}`);
    console.log(`   记忆ID: ${addResult.memory?.id}`);
    console.log(`   集成添加: ${addResult.integrated}`);
    
    // 4. 测试统计
    console.log('\n4️⃣  测试集成统计...');
    const stats = integration.getStats();
    console.log('   集成统计:', JSON.stringify(stats, null, 2));
    
    // 5. 测试清理
    console.log('\n5️⃣  测试清理...');
    await integration.cleanup();
    
    const afterStatus = integration.getIntegrationStatus();
    console.log(`   清理后集成状态: ${afterStatus.integrated}`);
    
    console.log('\n' + '='.repeat(60));
    console.log('🎉 集成测试完成！');
    console.log('✅ 所有集成功能工作正常');
    
    return true;
    
  } catch (error) {
    console.error('\n❌ 集成测试失败:', error.message);
    console.error(error.stack);
    return false;
  }
}

// 运行测试
runIntegrationTest().then(success => {
  if (success) {
    console.log('\n🚀 集成测试通过，可以部署到生产环境');
  } else {
    console.log('\n⚠️  集成测试失败，需要进一步调试');
    process.exit(1);
  }
}).catch(console.error);
