/**
 * Memory-Master v4.2.0 迭代压缩集成测试
 * 
 * 测试 AAAK 迭代压缩器集成到 MemoryManager
 */

const path = require('path');
const { MemoryManager, AAAKIterativeCompressor } = require('./src/memory-manager');

async function runTests() {
  console.log('🧠 Memory-Master v4.2.0 迭代压缩集成测试\n');
  console.log('='.repeat(60));

  // 创建测试实例
  const testDir = path.join(process.cwd(), 'test-memory-v4.2');
  const manager = new MemoryManager({
    baseDir: testDir,
    autoIndex: true,
    compression: true,
    compressionMaxLength: 2000,
    compressionRatio: 0.6,
  });

  console.log('\n✅ 测试 1: MemoryManager 初始化');
  console.log('   - 基础目录:', testDir);
  console.log('   - 自动索引:', manager.config.autoIndex);
  console.log('   - 压缩器:', manager.compressor ? '✅ 已初始化' : '❌ 未初始化');

  // 测试 1: 存储记忆
  console.log('\n📝 测试 2: 存储记忆');
  const longContent = `
## [2026-04-11] Memory-Master v4.2.0 开发日志

### 上午 (9:00-12:00)
- 研究 Hermes Agent 记忆系统架构
- 分析 FTS5 + SQLite 存储方案
- 学习 Lineage 谱系追踪设计
- 设计迭代压缩算法架构

### 下午 (13:00-17:00)
- 实现 AAAK 迭代压缩器核心
- 创建 4 种 Prompt 模板 (标准/结构化/迭代/紧急)
- 添加数据库 Schema 更新支持
- 编写使用指南文档

### 晚上 (19:00-21:00)
- 集成压缩器到 MemoryManager
- 添加 compressMemory 方法
- 添加 compressMemoriesBatch 批量压缩
- 测试迭代压缩功能

### 关键决策
1. 采用 Hermes 的"Compression as Consolidation"理念
2. 支持累积更新而非重新开始
3. 添加 Lineage 追踪保证可追溯性

### 技术细节
- 压缩器类：AAAKIterativeCompressor
- Prompt 模板：4 种类型
- 数据库字段：parent_memory_id, compression_chain, last_compressed_summary
- 压缩率目标：0.6

### 待办事项
- [ ] 性能优化 (< 100ms)
- [ ] 压缩质量评估
- [ ] 多语言支持
- [ ] 部署到 ClawHub
`;

  const storeResult = manager.store(longContent, {
    tags: ['开发日志', 'Memory-Master', 'v4.2.0'],
    source: 'test'
  });

  console.log('   - 记忆 ID:', storeResult.memoryId);
  console.log('   - 类型:', storeResult.typeName);
  console.log('   - 内容长度:', longContent.length, '字');
  console.log('   - ✅ 存储成功');

  // 测试 2: 压缩记忆
  console.log('\n🗜️ 测试 3: 压缩记忆 (标准模式)');
  try {
    const compressResult = await manager.compressMemory(storeResult.memoryId);
    
    if (compressResult.success) {
      console.log('   - ✅ 压缩成功');
      console.log('   - 压缩率:', (compressResult.compressionRatio * 100).toFixed(1) + '%');
      console.log('   - 迭代压缩:', compressResult.isIterative ? '是' : '否');
      console.log('   - 摘要预览:', compressResult.summary.substring(0, 100) + '...');
    } else {
      console.log('   - ⚠️ 压缩跳过:', compressResult.reason);
    }
  } catch (error) {
    console.log('   - ❌ 压缩失败:', error.message);
  }

  // 测试 3: 迭代压缩
  console.log('\n🔄 测试 4: 迭代压缩');
  const newContent = `
## [2026-04-12] 新增内容

### 上午完成
- 修复了 3 个 Bug
- 优化了压缩算法性能
- 添加了单元测试

### 新决策
4. 添加压缩质量自动评估
5. 支持自定义 Prompt 模板

### 新待办
- [ ] 编写 API 文档
- [ ] 创建示例项目
`;

  const newMemory = manager.store(newContent, {
    tags: ['开发日志', 'Day 2'],
    source: 'test'
  });

  try {
    const iterativeResult = await manager.compressMemory(newMemory.memoryId, {
      parentMemoryId: storeResult.memoryId
    });

    if (iterativeResult.success) {
      console.log('   - ✅ 迭代压缩成功');
      console.log('   - 迭代模式:', iterativeResult.isIterative ? '是' : '否');
      console.log('   - 谱系链:', iterativeResult.lineageChain.join(' → '));
      console.log('   - 摘要预览:', iterativeResult.summary.substring(0, 150) + '...');
    }
  } catch (error) {
    console.log('   - ❌ 迭代压缩失败:', error.message);
  }

  // 测试 4: 批量压缩
  console.log('\n📦 测试 5: 批量压缩');
  const memories = [
    manager.store('这是第一段测试内容，包含一些重要信息需要压缩...', { tags: ['测试'] }),
    manager.store('这是第二段测试内容，也包含重要信息...', { tags: ['测试'] }),
    manager.store('这是第三段测试内容，同样需要压缩处理...', { tags: ['测试'] }),
  ].map(m => m.memoryId);

  try {
    const batchResult = await manager.compressMemoriesBatch(memories, {
      delayMs: 100,
      minLength: 20
    });

    console.log('   - 总数:', batchResult.total);
    console.log('   - 成功:', batchResult.success);
    console.log('   - 失败:', batchResult.failed);
  } catch (error) {
    console.log('   - ❌ 批量压缩失败:', error.message);
  }

  // 测试 5: 获取摘要
  console.log('\n💡 测试 6: 获取记忆摘要');
  try {
    const summary = await manager.getMemorySummary(storeResult.memoryId);
    console.log('   - ✅ 获取成功');
    console.log('   - 摘要:', summary ? summary.substring(0, 80) + '...' : '无摘要');
  } catch (error) {
    console.log('   - ❌ 获取失败:', error.message);
  }

  // 清理
  console.log('\n🧹 清理测试目录...');
  try {
    const { execSync } = require('child_process');
    execSync(`rmdir /s /q "${testDir}"`, { stdio: 'ignore' });
    console.log('   - ✅ 清理完成');
  } catch (error) {
    console.log('   - ⚠️ 清理失败，请手动删除:', testDir);
  }

  console.log('\n' + '='.repeat(60));
  console.log('✅ 测试完成！\n');
}

// 运行测试
runTests().catch(console.error);
