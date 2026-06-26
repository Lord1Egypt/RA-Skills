const { createMemoryCore } = require('../index');

const CONFIG = {
  verbose: true,
  apiKey: 'sk-BrwHc1ZiaEGQ1GecD3D760384b874795A194882c2cF3AbE6',
  baseUrl: 'https://api.edgefn.net/v1',
  embeddingProvider: {
    type: 'edgefn',
    model: 'BAAI/bge-m3',
    dimensions: 1024,
    timeout: 30000,
    resilience: { maxRetries: 3, baseDelay: 1000 }
  },
  rerankProvider: {
    type: 'edgefn',
    model: 'bge-reranker-v2-m3',
    timeout: 30000
  },
  embeddingService: {
    defaultProvider: 'edgefn',
    cacheEnabled: true,
    verbose: true
  },
  memoryService: {
    autoEmbed: true,
    verbose: true,
    defaultSearchOptions: {
      useReranker: true,
      topKInitial: 10,
      topKFinal: 3,
      embeddingWeight: 0.4,
      rerankerWeight: 0.6,
      minScore: 0.1
    }
  }
};

async function runTests() {
  console.log('🧪 Memory Core 真实 API 测试');
  console.log('='.repeat(60));
  
  let memoryCore;
  let testResults = { total: 0, passed: 0, failed: 0, details: [] };
  
  try {
    console.log('\n1️⃣  测试系统初始化...');
    testResults.total++;
    
    memoryCore = createMemoryCore(CONFIG);
    await memoryCore.initialize();
    
    const info = memoryCore.getInfo();
    console.log('   ✅ 初始化成功');
    console.log(`     服务: ${Object.keys(info.services).join(', ')}`);
    
    testResults.passed++;
    testResults.details.push({ test: '初始化', result: '✅ 通过' });
    
    console.log('\n2️⃣  测试 Edgefn API 连接...');
    testResults.total++;
    
    try {
      const embeddingService = memoryCore.embeddingService;
      const testTexts = ['测试文本 1', '测试文本 2'];
      
      console.log('   生成 embeddings...');
      const embeddings = await embeddingService.embed(testTexts, {
        useCache: false
      });
      
      if (embeddings && embeddings.length === 2) {
        console.log(`   ✅ API 连接成功`);
        console.log(`     维度: ${embeddings[0].length}`);
        
        testResults.passed++;
        testResults.details.push({ test: 'API连接', result: '✅ 通过' });
      } else {
        throw new Error('Embeddings 生成失败');
      }
      
    } catch (apiError) {
      console.log(`   ❌ API 连接失败: ${apiError.message}`);
      testResults.failed++;
      testResults.details.push({ test: 'API连接', result: `❌ 失败: ${apiError.message}` });
      console.log('   ⚠️  API 失败，跳过后续测试');
      console.log('='.repeat(60));
      console.log(`📊 测试结果: ${testResults.passed}/${testResults.total} 通过`);
      return testResults;
    }
    
    console.log('\n3️⃣  测试记忆添加...');
    testResults.total++;
    
    try {
      const testMemories = [
        'Worldcoin (WLD) 是 AI 时代的人类身份验证基础设施',
        '向量搜索比关键词搜索更能理解语义意图'
      ];
      
      for (const content of testMemories) {
        const memory = await memoryCore.addMemory(content, {
          category: '测试',
          tags: ['api-test']
        });
        console.log(`   ✅ 添加: ${content.substring(0, 40)}...`);
      }
      
      testResults.passed++;
      testResults.details.push({ test: '记忆添加', result: '✅ 通过' });
      
    } catch (error) {
      console.log(`   ❌ 记忆添加失败: ${error.message}`);
      testResults.failed++;
      testResults.details.push({ test: '记忆添加', result: `❌ 失败: ${error.message}` });
    }
    
    console.log('\n4️⃣  测试语义搜索...');
    testResults.total++;
    
    try {
      const query = 'WLD 身份验证';
      console.log(`   搜索: "${query}"`);
      
      const startTime = Date.now();
      const result = await memoryCore.search(query, {
        topKFinal: 2,
        useReranker: true
      });
      const searchTime = Date.now() - startTime;
      
      if (result.success) {
        console.log(`     ✅ 找到 ${result.results.length} 个结果 (${searchTime}ms)`);
        result.results.forEach((r, i) => {
          console.log(`       ${i + 1}. [${r.score.toFixed(4)}] ${r.preview}`);
        });
        testResults.passed++;
        testResults.details.push({ test: '语义搜索', result: '✅ 通过' });
      } else {
        throw new Error(`搜索失败: ${result.error}`);
      }
      
    } catch (error) {
      console.log(`   ❌ 搜索测试失败: ${error.message}`);
      testResults.failed++;
      testResults.details.push({ test: '语义搜索', result: `❌ 失败: ${error.message}` });
    }
    
    console.log('\n5️⃣  测试系统统计...');
    testResults.total++;
    
    try {
      const stats = memoryCore.memoryService.getStats();
      console.log('   📊 统计:');
      console.log(`      记忆数量: ${stats.totalMemories}`);
      console.log(`      搜索次数: ${stats.totalSearches}`);
      console.log(`      搜索成功率: ${stats.searchSuccessRate}%`);
      
      testResults.passed++;
      testResults.details.push({ test: '系统统计', result: '✅ 通过' });
      
    } catch (error) {
      console.log(`   ❌ 统计获取失败: ${error.message}`);
      testResults.failed++;
      testResults.details.push({ test: '系统统计', result: `❌ 失败: ${error.message}` });
    }
    
  } catch (error) {
    console.log(`\n❌ 测试运行失败: ${error.message}`);
    testResults.failed++;
    testResults.details.push({ test: '测试框架', result: `❌ 失败: ${error.message}` });
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('📊 最终测试结果');
  console.log('='.repeat(60));
  
  console.log(`总测试: ${testResults.total}`);
  console.log(`通过: ${testResults.passed} ✅`);
  console.log(`失败: ${testResults.failed} ❌`);
  console.log(`通过率: ${Math.round((testResults.passed / testResults.total) * 100)}%`);
  
  console.log('\n📋 详细结果:');
  testResults.details.forEach(detail => {
    console.log(`  ${detail.result} - ${detail.test}`);
  });
  
  console.log('\n' + '='.repeat(60));
  
  if (testResults.failed === 0) {
    console.log('🎉 所有测试通过！Memory Core 工作正常！');
  } else {
    console.log('⚠️  有测试失败，需要进一步调试');
  }
  
  return testResults;
}

runTests().catch(console.error);
