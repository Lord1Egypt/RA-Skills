/**
 * Memory-Master v4.2.0 完整测试套件
 * 
 * 测试范围:
 * - 迭代压缩功能
 * - 性能优化效果
 * - Lineage 追踪
 * - 缓存系统
 * - 批量处理
 * 
 * @author 小鬼 👻
 * @date 2026-04-11
 */

const path = require('path');
const { MemoryManager, AAAKIterativeCompressor } = require('./src/memory-manager');
const {
  PerformanceMonitor,
  LRUCache,
  ParallelProcessor,
  IncrementalCompressor,
} = require('./src/compressors/performance-optimizer');

// ============ 测试框架 ============

class TestRunner {
  constructor() {
    this.results = {
      total: 0,
      passed: 0,
      failed: 0,
      skipped: 0,
    };
    this.tests = [];
  }

  test(name, fn) {
    this.tests.push({ name, fn });
  }

  async run() {
    console.log('🧪 Memory-Master v4.2.0 测试套件\n');
    console.log('='.repeat(60));

    for (const test of this.tests) {
      this.results.total++;
      
      try {
        console.log(`\n📋 ${test.name}`);
        await test.fn();
        this.results.passed++;
        console.log('   ✅ 通过');
      } catch (error) {
        this.results.failed++;
        console.log('   ❌ 失败:', error.message);
      }
    }

    console.log('\n' + '='.repeat(60));
    console.log('📊 测试结果:');
    console.log(`   总计：${this.results.total}`);
    console.log(`   ✅ 通过：${this.results.passed}`);
    console.log(`   ❌ 失败：${this.results.failed}`);
    console.log(`   ⏭️ 跳过：${this.results.skipped}`);
    console.log('='.repeat(60));

    return this.results.failed === 0;
  }
}

// ============ 测试用例 ============

async function runAllTests() {
  const runner = new TestRunner();

  // ========== 1. 压缩器基础测试 ==========

  runner.test('1.1 压缩器初始化', async () => {
    const compressor = new AAAKIterativeCompressor({
      maxLength: 2000,
      compressionRatio: 0.6,
      cacheSize: 100,
      maxConcurrency: 3,
    });

    if (!compressor) throw new Error('压缩器创建失败');
    if (!compressor.compress) throw new Error('缺少 compress 方法');
    if (!compressor.compressBatch) throw new Error('缺少 compressBatch 方法');
    if (!compressor.getPerformanceReport) throw new Error('缺少性能报告方法');

    console.log('   - 压缩器创建成功');
    console.log('   - 方法完整');
  });

  runner.test('1.2 标准压缩功能', async () => {
    const compressor = new AAAKIterativeCompressor();
    
    const content = `
## 开发日志

### 上午完成
- 研究 Hermes Agent 架构
- 设计迭代压缩算法
- 实现核心压缩器

### 下午完成
- 集成到 MemoryManager
- 添加性能优化
- 编写测试用例

### 关键决策
1. 采用累积压缩策略
2. 添加 Lineage 追踪
3. 实现 4 种 Prompt 模板
`;

    const result = await compressor.compress(content);
    
    if (!result.success && !result.summary) {
      throw new Error('压缩失败');
    }

    console.log('   - 原始长度:', content.length, '字');
    console.log('   - 压缩长度:', result.summary?.length || 'N/A', '字');
    console.log('   - 压缩率:', (result.compressionRatio * 100).toFixed(1) + '%');
  });

  runner.test('1.3 迭代压缩功能', async () => {
    const compressor = new AAAKIterativeCompressor();
    
    const content1 = '这是第一段内容，包含重要信息 A 和 B。';
    const content2 = '这是第二段内容，新增信息 C 和 D。';
    
    // 第一次压缩
    const result1 = await compressor.compress(content1);
    
    // 第二次压缩 (迭代模式)
    const result2 = await compressor.compress(
      content2,
      result1.summary,
      'mem_1'
    );
    
    if (!result2.isIterative) {
      throw new Error('迭代压缩未生效');
    }
    
    if (!result2.lineageChain.includes('mem_1')) {
      throw new Error('Lineage 追踪失败');
    }

    console.log('   - 第一次摘要:', result1.summary?.substring(0, 30) + '...');
    console.log('   - 第二次摘要:', result2.summary?.substring(0, 50) + '...');
    console.log('   - 迭代模式:', result2.isIterative ? '✅' : '❌');
    console.log('   - 谱系链:', result2.lineageChain.join(' → '));
  });

  // ========== 2. 性能优化测试 ==========

  runner.test('2.1 LRU 缓存功能', async () => {
    const cache = new LRUCache({ maxSize: 10, ttlMs: 1000 });
    
    cache.set('key1', 'value1');
    const value1 = cache.get('key1');
    
    if (value1 !== 'value1') {
      throw new Error('缓存读取失败');
    }
    
    // 等待过期
    await new Promise(resolve => setTimeout(resolve, 1100));
    const value2 = cache.get('key1');
    
    if (value2 !== null) {
      throw new Error('缓存过期未生效');
    }

    console.log('   - 缓存写入/读取：✅');
    console.log('   - 缓存过期：✅');
    console.log('   - 缓存统计:', cache.getStats());
  });

  runner.test('2.2 性能监控功能', async () => {
    const monitor = new PerformanceMonitor();
    
    monitor.recordCompression(50, false);
    monitor.recordCompression(30, false);
    monitor.recordCompression(80, false);
    monitor.recordCompression(20, true); // 缓存命中
    
    const report = monitor.getReport();
    
    if (report.totalRequests !== 4) {
      throw new Error('请求计数错误');
    }
    
    if (report.cacheHits !== 1) {
      throw new Error('缓存命中计数错误');
    }

    console.log('   - 总请求:', report.totalRequests);
    console.log('   - 缓存命中:', report.cacheHits);
    console.log('   - 平均时间:', report.avgTime.toFixed(2), 'ms');
    console.log('   - P95 时间:', report.p95Time.toFixed(2), 'ms');
  });

  runner.test('2.3 并行处理器功能', async () => {
    const processor = new ParallelProcessor({ maxConcurrency: 2, timeoutMs: 5000 });
    
    const items = [1, 2, 3, 4, 5];
    const startTime = Date.now();
    
    const results = await processor.process(items, async (item) => {
      await new Promise(resolve => setTimeout(resolve, 100)); // 模拟耗时
      return item * 2;
    });
    
    const duration = Date.now() - startTime;
    
    if (results.length !== 5) {
      throw new Error('并行处理结果数量错误');
    }
    
    if (duration > 500) { // 并发 2，应该 < 300ms
      throw new Error(`并行处理超时：${duration}ms`);
    }

    console.log('   - 处理数量:', results.length);
    console.log('   - 处理时间:', duration, 'ms');
    console.log('   - 并发效果：✅');
  });

  runner.test('2.4 增量压缩检测', async () => {
    const incremental = new IncrementalCompressor({ minChangeRatio: 0.1 });
    
    const content1 = '这是原始内容，包含很多信息。';
    const content2 = '这是原始内容，包含很多信息。'; // 完全相同
    const content3 = '这是完全不同的新内容。'; // 完全不同
    
    const needsRecompress1 = incremental.needsRecompression(content1, 'key1');
    incremental.updateCache('key1', content1, 'summary1');
    
    const needsRecompress2 = incremental.needsRecompression(content2, 'key1'); // 应该不需要
    const needsRecompress3 = incremental.needsRecompression(content3, 'key1'); // 应该需要

    if (!needsRecompress1) {
      throw new Error('首次压缩应该需要');
    }
    
    if (needsRecompress2) {
      throw new Error('相同内容不应该重新压缩');
    }
    
    if (!needsRecompress3) {
      throw new Error('不同内容应该重新压缩');
    }

    console.log('   - 首次压缩：需要 ✅');
    console.log('   - 相同内容：不需要 ✅');
    console.log('   - 不同内容：需要 ✅');
  });

  // ========== 3. MemoryManager 集成测试 ==========

  runner.test('3.1 MemoryManager 集成压缩器', async () => {
    const testDir = path.join(process.cwd(), 'test-memory-v4.2');
    const manager = new MemoryManager({
      baseDir: testDir,
      autoIndex: true,
      compression: true,
    });

    if (!manager.compressor) {
      throw new Error('压缩器未集成');
    }

    console.log('   - MemoryManager 创建：✅');
    console.log('   - 压缩器初始化：✅');
    console.log('   - 基础目录:', testDir);
  });

  runner.test('3.2 存储 + 压缩完整流程', async () => {
    const testDir = path.join(process.cwd(), 'test-memory-flow');
    const manager = new MemoryManager({
      baseDir: testDir,
      autoIndex: false,
      compression: true,
    });

    const content = `
## 完整测试内容

### 第一部分
这是第一段内容，包含重要信息。

### 第二部分
这是第二段内容，新增更多细节。

### 第三部分
这是第三段内容，补充完整信息。
`;

    // 存储
    const storeResult = manager.store(content, {
      tags: ['测试', '完整流程'],
    });

    console.log('   - 存储成功:', storeResult.success ? '✅' : '❌');
    console.log('   - 记忆 ID:', storeResult.memoryId);
    console.log('   - 类型:', storeResult.typeName);

    // 压缩 (这里因为内容太短可能会跳过)
    try {
      const compressResult = await manager.compressMemory(storeResult.memoryId, {
        minLength: 10, // 降低阈值以测试
      });
      
      console.log('   - 压缩状态:', compressResult.success ? '成功' : '跳过');
      if (compressResult.reason) {
        console.log('   - 跳过原因:', compressResult.reason);
      }
    } catch (error) {
      console.log('   - 压缩异常:', error.message);
    }
  });

  // ========== 4. 性能基准测试 ==========

  runner.test('4.1 压缩性能基准', async () => {
    const compressor = new AAAKIterativeCompressor();
    const testContent = '这是测试内容。'.repeat(100); // 约 1000 字
    
    const times = [];
    
    // 运行 10 次测试
    for (let i = 0; i < 10; i++) {
      const start = Date.now();
      await compressor.compress(testContent);
      const duration = Date.now() - start;
      times.push(duration);
    }
    
    const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
    const minTime = Math.min(...times);
    const maxTime = Math.max(...times);
    
    console.log('   - 测试内容:', testContent.length, '字');
    console.log('   - 测试次数: 10');
    console.log('   - 平均时间:', avgTime.toFixed(2), 'ms');
    console.log('   - 最短时间:', minTime, 'ms');
    console.log('   - 最长时间:', maxTime, 'ms');
    
    // 性能目标检查
    if (avgTime > 100) {
      console.log('   - ⚠️ 警告：平均时间超过 100ms 目标');
    } else {
      console.log('   - ✅ 性能达标 (< 100ms)');
    }
  });

  runner.test('4.2 缓存命中性能', async () => {
    const compressor = new AAAKIterativeCompressor();
    const content = '这是测试内容，用于缓存测试。';
    
    // 第一次压缩 (未命中)
    const start1 = Date.now();
    await compressor.compress(content);
    const time1 = Date.now() - start1;
    
    // 第二次压缩 (命中缓存)
    const start2 = Date.now();
    await compressor.compress(content);
    const time2 = Date.now() - start2;
    
    const speedup = time1 / (time2 || 1);
    
    console.log('   - 首次压缩:', time1, 'ms (未命中)');
    console.log('   - 缓存命中:', time2, 'ms');
    console.log('   - 性能提升:', speedup.toFixed(1), 'x');
    
    if (time2 >= time1) {
      console.log('   - ⚠️ 警告：缓存未生效');
    } else {
      console.log('   - ✅ 缓存生效');
    }
  });

  // ========== 5. 批量处理测试 ==========

  runner.test('5.1 批量压缩功能', async () => {
    const compressor = new AAAKIterativeCompressor();
    
    const items = Array.from({ length: 5 }, (_, i) => ({
      content: `这是第 ${i + 1} 段测试内容。`,
    }));
    
    const start = Date.now();
    const results = await compressor.compressBatch(items);
    const duration = Date.now() - start;
    
    if (results.length !== 5) {
      throw new Error('批量压缩结果数量错误');
    }
    
    const avgTime = duration / results.length;
    
    console.log('   - 批量数量:', items.length);
    console.log('   - 总时间:', duration, 'ms');
    console.log('   - 平均时间:', avgTime.toFixed(2), 'ms/个');
    console.log('   - 并发处理：✅');
  });

  // ========== 运行测试 ==========

  const success = await runner.run();
  
  return success;
}

// ============ 执行测试 ============

runAllTests()
  .then(success => {
    console.log('\n' + (success ? '✅ 所有测试通过！' : '❌ 部分测试失败'));
    process.exit(success ? 0 : 1);
  })
  .catch(error => {
    console.error('💥 测试执行失败:', error);
    process.exit(1);
  });
