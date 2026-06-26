/**
 * Memory-Master v4.2.0 - 分层存储系统测试 (JavaScript 版本)
 */

const { LayeredManager } = require('../src/layers/layered-manager');

async function runTests() {
  console.log('🧪 Memory-Master v4.2.0 分层存储系统测试\n');

  // 初始化分层管理器
  const manager = new LayeredManager({
    basePath: './memory-test',
    autoMigrate: false // 测试时关闭自动迁移
  });

  let passed = 0;
  let failed = 0;

  try {
    // Test 1: 存储到 L0
    console.log('Test 1: 存储到 L0');
    const id1 = manager.store('这是一条测试记忆 - L0');
    console.log(`✅ 存储成功：${id1}`);
    passed++;

    // Test 2: 从 L0 读取
    console.log('\nTest 2: 从 L0 读取');
    const entry1 = manager.get(id1);
    if (entry1 && entry1.layer === 'L0' && entry1.content.includes('测试记忆')) {
      console.log(`✅ 读取成功：${entry1.content} (Layer: ${entry1.layer})`);
      passed++;
    } else {
      console.log('❌ 读取失败');
      failed++;
    }

    // Test 3: 存储到 L1
    console.log('\nTest 3: 存储到 L1');
    const id2 = manager.storeToLayer('这是一条测试记忆 - L1', 'L1');
    console.log(`✅ 存储成功：${id2}`);
    passed++;

    // Test 4: 从 L1 读取
    console.log('\nTest 4: 从 L1 读取');
    const entry2 = manager.get(id2);
    if (entry2 && entry2.layer === 'L1') {
      console.log(`✅ 读取成功：${entry2.content} (Layer: ${entry2.layer})`);
      passed++;
    } else {
      console.log('❌ 读取失败');
      failed++;
    }

    // Test 5: 存储到 L2
    console.log('\nTest 5: 存储到 L2');
    const id3 = manager.storeToLayer('这是一条测试记忆 - L2', 'L2');
    console.log(`✅ 存储成功：${id3}`);
    passed++;

    // Test 6: 从 L2 读取
    console.log('\nTest 6: 从 L2 读取');
    const entry3 = manager.get(id3);
    if (entry3 && entry3.layer === 'L2') {
      console.log(`✅ 读取成功：${entry3.content} (Layer: ${entry3.layer})`);
      passed++;
    } else {
      console.log('❌ 读取失败');
      failed++;
    }

    // Test 7: 跨层搜索
    console.log('\nTest 7: 跨层搜索');
    const results = manager.search('测试记忆', { limit: 10 });
    if (results.length >= 3) {
      console.log(`✅ 搜索成功：找到 ${results.length} 条结果`);
      results.forEach((r, i) => {
        console.log(`   ${i + 1}. [${r.layer}] ${r.content}`);
      });
      passed++;
    } else {
      console.log(`❌ 搜索失败：只找到 ${results.length} 条`);
      failed++;
    }

    // Test 8: 统计信息
    console.log('\nTest 8: 统计信息');
    const stats = manager.getStats();
    console.log('✅ 统计信息:');
    console.log(`   总查询次数：${stats.totalQueries}`);
    stats.layers.forEach(layer => {
      console.log(`   ${layer.layer}: ${layer.totalEntries} 条，${layer.size}`);
    });
    console.log(`   命中率：L0 ${stats.hitRates.L0}, L1 ${stats.hitRates.L1}, L2 ${stats.hitRates.L2}`);
    passed++;

    // Test 9: 删除记忆
    console.log('\nTest 9: 删除记忆');
    const deleted = manager.delete(id1);
    if (deleted) {
      console.log(`✅ 删除成功：${id1}`);
      passed++;
    } else {
      console.log('❌ 删除失败');
      failed++;
    }

    // Test 10: 验证删除
    console.log('\nTest 10: 验证删除');
    const afterDelete = manager.get(id1);
    if (!afterDelete) {
      console.log('✅ 验证成功：记忆已删除');
      passed++;
    } else {
      console.log('❌ 验证失败：记忆仍然存在');
      failed++;
    }

  } catch (error) {
    console.error('❌ 测试出错:', error);
    failed++;
  } finally {
    // 清理
    manager.destroy();
  }

  // 总结
  console.log('\n' + '='.repeat(50));
  console.log(`测试结果：${passed} 通过，${failed} 失败`);
  console.log('='.repeat(50));

  if (failed === 0) {
    console.log('\n🎉 所有测试通过！Phase 1 分层存储系统完成！');
  } else {
    console.log('\n⚠️  有测试失败，请检查代码');
  }
}

// 运行测试
runTests().catch(console.error);
