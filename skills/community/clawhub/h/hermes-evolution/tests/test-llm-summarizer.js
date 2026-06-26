/**
 * LLMSummarizer 测试
 */

const {
  LLMSummarizer,
  SummaryStrategy
} = require('./llm-summarizer');

async function runTests() {
  console.log('🧪 LLMSummarizer 测试\n');

  const summarizer = new LLMSummarizer();

  // 1. 测试基础摘要
  console.log('1️⃣ 测试基础摘要');
  const longContent = `
今天完成了PM Router的架构设计和实现。这是一个复杂的任务路由系统，需要协调多个Agent之间的工作。

主要完成了以下功能：
1. 任务创建和状态管理
2. Agent路由逻辑
3. 上下文传递机制
4. 结果汇总和汇报

在实现过程中，遇到了一些挑战，特别是在状态转换和错误处理方面。但是通过团队协作，这些问题都得到了很好的解决。

下一步计划：
- 完成剩余的测试用例
- 优化性能
- 准备上线部署
`.trim();

  const result1 = await summarizer.summarize(longContent, { topic: 'PM Router开发' });
  console.log(`   原始长度: ${result1.originalTokens} Tokens`);
  console.log(`   摘要长度: ${result1.summaryTokens} Tokens`);
  console.log(`   压缩比: ${result1.tokenReduction}%`);
  console.log(`   来自缓存: ${result1.fromCache || false}`);
  console.log(`   摘要预览: ${result1.summary.substring(0, 80)}...`);

  // 2. 测试短内容
  console.log('\n2️⃣ 测试短内容（不需摘要）');
  const shortContent = '这是一个很短的文本，不需要摘要处理。';
  const result2 = await summarizer.summarize(shortContent);
  console.log(`   内容: ${shortContent}`);
  console.log(`   压缩后: ${result2.summary}`);
  console.log(`   需压缩: ${result2.reduced}`);

  // 3. 测试批量摘要
  console.log('\n3️⃣ 测试批量摘要');
  const contents = [
    '这是第一篇关于人工智能的文章，讨论了机器学习和深度学习的基本概念。机器学习是人工智能的一个分支，而深度学习则是机器学习的一个子领域。',
    '这是第二篇关于职业发展的文章，讨论了如何在职场中提升自己。包括技术能力、沟通能力、领导力等多个方面。',
    '这是第三篇关于健康管理的内容，讨论了工作与生活的平衡。包括运动、睡眠、饮食等多个因素。'
  ];

  const batchResults = await summarizer.summarizeBatch(contents);
  for (let i = 0; i < batchResults.length; i++) {
    const keywords = (batchResults[i].keywords || []).slice(0, 3).join(', ');
    console.log(`   [${i+1}] 压缩比: ${batchResults[i].tokenReduction}%, 关键词: ${keywords}`);
  }

  // 4. 测试缓存
  console.log('\n4️⃣ 测试缓存');
  const cached = await summarizer.summarize(longContent, { topic: 'PM Router开发' });
  console.log(`   来自缓存: ${cached.fromCache || false}`);
  const stats = summarizer.getStats();
  console.log(`   缓存命中: ${stats.cachedHits}`);

  // 5. 测试不同策略
  console.log('\n5️⃣ 测试不同摘要策略');
  const testContent = `
这是一个测试文档，用于验证不同的摘要策略。

第一部分介绍了一些基本概念。
第二部分讨论了具体的实现方法。
第三部分给出了实际的例子。
第四部分总结了关键的要点。
第五部分提供了进一步学习的资源。

关键词包括：测试、策略、摘要、验证。
`.trim();

  const strategies = [
    { name: '抽取式', strategy: SummaryStrategy.EXTRACTIVE },
    { name: '结构化', strategy: SummaryStrategy.STRUCTURED },
    { name: '混合', strategy: SummaryStrategy.HYBRID }
  ];

  for (const s of strategies) {
    const stratSummarizer = new LLMSummarizer({ strategy: s.strategy });
    const r = await stratSummarizer.summarize(testContent);
    console.log(`\n   ${s.name}:`);
    console.log(`   ${r.summary}`);
    console.log(`   压缩比: ${r.tokenReduction}%`);
  }

  // 6. 打印统计
  console.log('\n6️⃣ 打印统计');
  summarizer.printStats();

  console.log('\n✅ LLMSummarizer 测试完成！');
  console.log('\nP2-2 LLM自动摘要 核心概念:');
  console.log('  📝 summarize() - 生成摘要');
  console.log('  🔄 summarizeBatch() - 批量摘要');
  console.log('  💾 缓存机制 - 避免重复摘要');
  console.log('  📊 压缩比统计 - Token开销可视化');
  console.log('\n效果: 大量检索结果 → 精炼摘要 → 上下文注入');
}

runTests().catch(console.error);
