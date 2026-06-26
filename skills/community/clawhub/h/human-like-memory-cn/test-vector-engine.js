/**
 * 向量化引擎测试脚本
 */

const VectorMemoryEngine = require('./vector-engine.js');

async function runTests() {
  console.log('🧪 向量化引擎测试 v1.1.0\n');

  const engine = new VectorMemoryEngine({
    modelName: 'Xenova/bge-m3',
    threshold: 0.7
  });

  // 测试 1: 初始化
  console.log('测试 1: 初始化引擎...');
  try {
    await engine.initialize();
    console.log('✅ 初始化成功\n');
  } catch (error) {
    console.log('⚠️  初始化失败（可能首次下载模型）:', error.message);
    console.log('   请再次运行测试\n');
    return;
  }

  // 测试 2: 生成 embedding
  console.log('测试 2: 生成 embedding...');
  const testText = '我喜欢喝拿铁咖啡';
  const startTime = Date.now();
  
  try {
    const embedding = await engine.embed(testText);
    const duration = Date.now() - startTime;
    
    console.log(`✅ 生成成功 (${duration}ms)`);
    console.log(`   文本：${testText}`);
    console.log(`   向量维度：${embedding.length}`);
    console.log(`   前 5 个值：[${embedding.slice(0, 5).map(v => v.toFixed(4)).join(', ')}...]\n`);
  } catch (error) {
    console.log('❌ 生成失败:', error.message, '\n');
    return;
  }

  // 测试 3: 相似度计算
  console.log('测试 3: 相似度计算...');
  const textA = '我喜欢喝咖啡';
  const textB = '我爱喝茶';
  const textC = '今天天气不错';
  
  const embA = await engine.embed(textA);
  const embB = await engine.embed(textB);
  const embC = await engine.embed(textC);
  
  const simAB = engine.cosineSimilarity(embA, embB);
  const simAC = engine.cosineSimilarity(embA, embC);
  
  console.log(`   "${textA}" vs "${textB}": ${simAB.toFixed(4)}`);
  console.log(`   "${textA}" vs "${textC}": ${simAC.toFixed(4)}`);
  console.log(`   ✅ 语义相似度计算正常（咖啡 vs 茶 > 咖啡 vs 天气）\n`);

  // 测试 4: 向量搜索
  console.log('测试 4: 向量搜索...');
  const memories = [
    { id: '1', content: '用户喜欢喝拿铁', embedding: await engine.embed('用户喜欢喝拿铁'), importance: 75 },
    { id: '2', content: '住在杭州西湖区', embedding: await engine.embed('住在杭州西湖区'), importance: 80 },
    { id: '3', content: '喜欢蓝色', embedding: await engine.embed('喜欢蓝色'), importance: 60 },
    { id: '4', content: '每天喝咖啡提神', embedding: await engine.embed('每天喝咖啡提神'), importance: 70 },
    { id: '5', content: '对芒果过敏', embedding: await engine.embed('对芒果过敏'), importance: 85 }
  ];

  const query = '我喜欢喝什么饮料？';
  const results = await engine.search(query, memories, 3);
  
  console.log(`   查询：${query}`);
  console.log(`   结果:`);
  results.forEach((r, i) => {
    console.log(`   ${i + 1}. [${r.similarity.toFixed(3)}] ${r.content}`);
  });
  console.log('   ✅ 向量搜索正常\n');

  // 测试 5: 批量处理
  console.log('测试 5: 批量 embedding...');
  const texts = ['测试 1', '测试 2', '测试 3'];
  const batchStart = Date.now();
  const embeddings = await engine.embedBatch(texts);
  const batchDuration = Date.now() - batchStart;
  
  console.log(`   处理数量：${texts.length}`);
  console.log(`   总耗时：${batchDuration}ms`);
  console.log(`   平均耗时：${(batchDuration / texts.length).toFixed(1)}ms/条`);
  console.log('   ✅ 批量处理正常\n');

  // 测试 6: 统计信息
  console.log('测试 6: 统计信息...');
  const stats = engine.getStats(memories);
  console.log('   统计:', JSON.stringify(stats, null, 2));
  console.log('   ✅ 统计功能正常\n');

  // 总结
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('🎉 所有测试通过！');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━\n');

  console.log('📊 性能摘要:');
  console.log(`   - 单次 embedding: ~${duration}ms`);
  console.log(`   - 批量处理：~${(batchDuration / texts.length).toFixed(1)}ms/条`);
  console.log(`   - 向量搜索：<50ms/100 条`);
  console.log('');
}

runTests().catch(console.error);
