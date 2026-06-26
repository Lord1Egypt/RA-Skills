/**
 * 🎯 Memory Core 集成测试
 */

const { createMemoryCore } = require('../index');
const fs = require('fs');
const path = require('path');

// 测试配置
const TEST_CONFIG = {
  verbose: false,
  apiKey: process.env.EDGEFN_API_KEY,
  embeddingService: {
    cacheEnabled: false // 测试中禁用缓存
  }
};

describe('Memory Core 集成测试', () => {
  let memoryCore;
  
  beforeAll(async () => {
    console.log('🚀 启动 Memory Core 测试...');
    memoryCore = createMemoryCore(TEST_CONFIG);
    await memoryCore.initialize();
  });
  
  afterAll(() => {
    console.log('🧹 清理测试数据...');
  });
  
  test('1. 系统初始化', () => {
    expect(memoryCore).toBeDefined();
    expect(memoryCore.memoryService).toBeDefined();
    expect(memoryCore.embeddingService).toBeDefined();
  });
  
  test('2. 添加记忆', async () => {
    const memory = await memoryCore.addMemory('测试记忆内容', {
      test: true,
      category: '测试'
    });
    
    expect(memory).toBeDefined();
    expect(memory.id).toBeDefined();
    expect(memory.content).toBe('测试记忆内容');
    expect(memory.metadata.test).toBe(true);
  });
  
  test('3. 搜索记忆', async () => {
    // 先添加一些测试记忆
    await memoryCore.addMemory('人工智能是未来的关键技术', { category: 'AI' });
    await memoryCore.addMemory('向量搜索比关键词搜索更智能', { category: '搜索' });
    await memoryCore.addMemory('Edgefn 提供了高质量的 embeddings API', { category: 'API' });
    
    // 搜索测试
    const result = await memoryCore.search('人工智能技术', {
      topKFinal: 2
    });
    
    expect(result.success).toBe(true);
    expect(result.results).toBeInstanceOf(Array);
    expect(result.results.length).toBeGreaterThan(0);
    
    // 检查结果格式
    const firstResult = result.results[0];
    expect(firstResult).toHaveProperty('id');
    expect(firstResult).toHaveProperty('content');
    expect(firstResult).toHaveProperty('score');
    expect(typeof firstResult.score).toBe('number');
  });
  
  test('4. Flomo 适配器', async () => {
    const flomoAdapter = memoryCore.createFlomoAdapter({
      verbose: false
    });
    
    expect(flomoAdapter).toBeDefined();
    expect(typeof flomoAdapter.parseExport).toBe('function');
    expect(typeof flomoAdapter.importToMemory).toBe('function');
    
    // 测试解析功能
    const testHtml = `
      <div class="memo">
        <div class="date">2026-03-06</div>
        <div class="content">这是一个测试笔记 #测试 #示例</div>
        <div class="tags">
          <span class="tag">测试</span>
          <span class="tag">示例</span>
        </div>
      </div>
    `;
    
    const parseResult = await flomoAdapter.parseExport(testHtml);
    expect(parseResult.success).toBe(true);
    expect(parseResult.notes).toBeInstanceOf(Array);
    
    if (parseResult.notes.length > 0) {
      const note = parseResult.notes[0];
      expect(note.content).toContain('这是一个测试笔记');
      expect(note.tags).toContain('测试');
      expect(note.tags).toContain('示例');
    }
  });
  
  test('5. 系统信息获取', () => {
    const info = memoryCore.getInfo();
    
    expect(info).toBeDefined();
    expect(info.initialized).toBe(true);
    expect(info.services).toBeDefined();
    expect(info.providers).toBeDefined();
    
    // 检查服务状态
    expect(info.services.memory).toBeDefined();
    expect(info.services.embedding).toBeDefined();
  });
  
  test('6. 批量操作', async () => {
    const contents = [
      '批量测试记忆 1',
      '批量测试记忆 2',
      '批量测试记忆 3'
    ];
    
    const metadataArray = [
      { batch: 1, category: '测试' },
      { batch: 2, category: '测试' },
      { batch: 3, category: '测试' }
    ];
    
    // 批量添加
    for (let i = 0; i < contents.length; i++) {
      await memoryCore.addMemory(contents[i], metadataArray[i]);
    }
    
    // 批量搜索
    const queries = ['测试记忆', '批量'];
    const searchResults = [];
    
    for (const query of queries) {
      const result = await memoryCore.search(query);
      if (result.success) {
        searchResults.push(...result.results);
      }
    }
    
    expect(searchResults.length).toBeGreaterThan(0);
  });
});

// 运行测试的函数
async function runTests() {
  console.log('🧪 开始 Memory Core 集成测试...\n');
  
  try {
    const tests = [
      { name: '系统初始化', fn: async () => {
        memoryCore = createMemoryCore(TEST_CONFIG);
        await memoryCore.initialize();
        console.log('✅ 系统初始化通过');
      }},
      
      { name: '基本功能测试', fn: async () => {
        // 添加记忆
        const memory = await memoryCore.addMemory('集成测试记忆', { test: true });
        console.log(`✅ 添加记忆: ${memory.id}`);
        
        // 搜索记忆
        const result = await memoryCore.search('集成测试');
        console.log(`✅ 搜索完成: ${result.results.length} 个结果`);
        
        // 系统信息
        const info = memoryCore.getInfo();
        console.log(`✅ 系统信息获取: ${Object.keys(info.services).length} 个服务`);
      }},
      
      { name: 'Flomo 适配器测试', fn: async () => {
        const flomoAdapter = memoryCore.createFlomoAdapter();
        const testHtml = '<div class="memo"><div class="content">Flomo 测试笔记</div></div>';
        
        const result = await flomoAdapter.parseExport(testHtml);
        console.log(`✅ Flomo 解析: ${result.notes.length} 个笔记`);
      }}
    ];
    
    let passed = 0;
    let failed = 0;
    
    for (const test of tests) {
      try {
        await test.fn();
        passed++;
        console.log(`🎉 ${test.name} 通过\n`);
      } catch (error) {
        failed++;
        console.error(`❌ ${test.name} 失败: ${error.message}\n`);
      }
    }
    
    console.log('📊 测试结果:');
    console.log(`   通过: ${passed}`);
    console.log(`   失败: ${failed}`);
    console.log(`   总计: ${tests.length}`);
    
    if (failed === 0) {
      console.log('\n🎉 所有测试通过！');
    } else {
      console.log('\n⚠️  有测试失败');
      process.exit(1);
    }
    
  } catch (error) {
    console.error('❌ 测试运行失败:', error.message);
    process.exit(1);
  }
}

// 如果直接运行此文件
if (require.main === module) {
  runTests();
}

module.exports = { runTests };
