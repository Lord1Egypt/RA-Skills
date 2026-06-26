const KnowledgeConnector = require('../src/index.js');
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const childProcess = require('child_process');

async function runTests() {
  console.log('🧪 开始运行测试...\n');
  
  const testDir = fs.mkdtempSync(path.join(os.tmpdir(), 'knowledge-connector-test-'));
  const kc = new KnowledgeConnector({ dataDir: testDir });
  let passed = 0;
  let failed = 0;
  
  // 测试 1: 提取概念
  try {
    const concepts = await kc.extract('人工智能是机器学习的基础，深度学习是人工智能的重要分支');
    assert(concepts.length > 0, '应该提取到概念');
    console.log('✅ 测试 1: 概念提取 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 1: 概念提取 - 失败:', e.message);
    failed++;
  }
  
  // 测试 2: 保存概念
  try {
    const concepts = await kc.extract('测试概念 A 和测试概念 B');
    await kc.saveConcepts(concepts);
    const saved = kc.loadConcepts();
    assert(saved.length > 0, '应该保存了概念');
    console.log('✅ 测试 2: 保存概念 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 2: 保存概念 - 失败:', e.message);
    failed++;
  }
  
  // 测试 3: 建立关联
  try {
    const concepts = kc.loadConcepts();
    if (concepts.length >= 2) {
      await kc.connect({
        from: concepts[0].name,
        to: concepts[1].name,
        type: '相关'
      });
      console.log('✅ 测试 3: 建立关联 - 通过');
      passed++;
    } else {
      console.log('⚠️  测试 3: 建立关联 - 跳过 (概念不足)');
    }
  } catch (e) {
    console.log('❌ 测试 3: 建立关联 - 失败:', e.message);
    failed++;
  }
  
  // 测试 4: 搜索
  try {
    const results = await kc.search('测试');
    assert(Array.isArray(results.concepts), '应该返回概念列表');
    console.log('✅ 测试 4: 搜索功能 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 4: 搜索功能 - 失败:', e.message);
    failed++;
  }
  
  // 测试 5: 统计信息
  try {
    const stats = await kc.getStats();
    assert(typeof stats.conceptCount === 'number', '应该有概念数量');
    console.log('✅ 测试 5: 统计信息 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 5: 统计信息 - 失败:', e.message);
    failed++;
  }
  
  // 测试 6: 可视化
  try {
    const html = await kc.visualize({ format: 'html' });
    assert(html.includes('<html>'), '应该生成 HTML');
    console.log('✅ 测试 6: 可视化 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 6: 可视化 - 失败:', e.message);
    failed++;
  }
  
  // 测试 7: 导出
  try {
    const data = await kc.export();
    assert(data.concepts, '应该有概念数据');
    assert(data.relations, '应该有关系数据');
    console.log('✅ 测试 7: 导出功能 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 7: 导出功能 - 失败:', e.message);
    failed++;
  }
  
  // 测试 8: 推荐
  try {
    const concepts = kc.loadConcepts();
    if (concepts.length > 0) {
      const recommendations = await kc.recommend(concepts[0].name, 3);
      console.log('✅ 测试 8: 推荐功能 - 通过');
      passed++;
    } else {
      console.log('⚠️  测试 8: 推荐功能 - 跳过 (概念不足)');
    }
  } catch (e) {
    console.log('❌ 测试 8: 推荐功能 - 失败:', e.message);
    failed++;
  }

  // 测试 9: 批量导入文档
  try {
    const docsDir = path.join(testDir, 'docs');
    fs.mkdirSync(docsDir, { recursive: true });
    fs.writeFileSync(path.join(docsDir, 'a.md'), '人工智能 连接 机器学习');
    fs.writeFileSync(path.join(docsDir, 'b.md'), '机器学习 连接 深度学习');
    const summary = await kc.importDocuments([docsDir]);
    assert(summary.fileCount === 2, '应该导入 2 个文档');
    assert(summary.conceptCount > 0, '应该导入概念');
    console.log('✅ 测试 9: 批量导入文档 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 9: 批量导入文档 - 失败:', e.message);
    failed++;
  }

  // 测试 10: 概念子图
  try {
    const map = await kc.map('机器学习', 1);
    assert(map && Array.isArray(map.nodes), '应该生成子图');
    console.log('✅ 测试 10: 概念子图 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 10: 概念子图 - 失败:', e.message);
    failed++;
  }

  // 测试 11: 导入预览
  try {
    const docsDir = path.join(testDir, 'docs');
    const plan = kc.planImport([docsDir]);
    assert(plan.fileCount >= 2, '应该预览到导入文件');
    assert(Array.isArray(plan.supportedTypes), '应该返回支持类型');
    console.log('✅ 测试 11: 导入预览 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 11: 导入预览 - 失败:', e.message);
    failed++;
  }

  // 测试 12: 答案页结果
  try {
    const answer = await kc.answer('机器学习');
    assert(answer.summary && answer.summary.includes('问题'), '应该生成答案摘要');
    const html = await kc.answer('机器学习', { format: 'html' });
    assert(typeof html === 'string' && html.includes('<html>'), '应该生成 HTML 答案页');
    console.log('✅ 测试 12: 答案页结果 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 12: 答案页结果 - 失败:', e.message);
    failed++;
  }

  // 测试 13: 重复导入同一文件不会重复创建来源
  try {
    const dedupeDir = fs.mkdtempSync(path.join(os.tmpdir(), 'knowledge-connector-dedupe-'));
    const docsDir = path.join(dedupeDir, 'docs');
    fs.mkdirSync(docsDir, { recursive: true });
    fs.writeFileSync(path.join(docsDir, 'same.md'), '规划 连接 强化学习');
    const dedupeKc = new KnowledgeConnector({ dataDir: path.join(dedupeDir, 'data') });
    await dedupeKc.importDocuments([docsDir], { autoConnect: false });
    await dedupeKc.importDocuments([docsDir], { autoConnect: false });
    const stats = await dedupeKc.getStats();
    assert(stats.sourceCount === 1, '重复导入同一文件时来源应该保持 1 个');
    console.log('✅ 测试 13: 来源去重 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 13: 来源去重 - 失败:', e.message);
    failed++;
  }

  // 测试 14: 中文自然语言问题能命中文档
  try {
    const answerDir = fs.mkdtempSync(path.join(os.tmpdir(), 'knowledge-connector-answer-'));
    const docsDir = path.join(answerDir, 'docs');
    fs.mkdirSync(docsDir, { recursive: true });
    fs.writeFileSync(path.join(docsDir, 'rl-plan.md'), '规划和强化学习互相连接，用于智能体决策。');
    const answerKc = new KnowledgeConnector({ dataDir: path.join(answerDir, 'data') });
    await answerKc.importDocuments([docsDir], { autoConnect: false });
    const answer = await answerKc.answer('哪些文档把规划和强化学习连起来了？');
    assert(answer.sources.some((source) => source.title === 'rl-plan.md'), '应该命中包含规划和强化学习的来源文档');
    assert(answer.concepts.length > 0, '应该命中相关概念');
    console.log('✅ 测试 14: 中文自然问答命中 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 14: 中文自然问答命中 - 失败:', e.message);
    failed++;
  }

  // 测试 15: HTML 答案页转义用户内容
  try {
    const htmlDir = fs.mkdtempSync(path.join(os.tmpdir(), 'knowledge-connector-html-'));
    const htmlKc = new KnowledgeConnector({ dataDir: htmlDir });
    await htmlKc.saveConcepts([{
      id: 'malicious-concept',
      name: '<script>alert(1)</script>',
      type: 'term',
      description: '',
      source: 'unsafe.md',
      sourceId: 'unsafe',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }]);
    const html = await htmlKc.answer('<script>', { format: 'html' });
    assert(!html.includes('<script>alert(1)</script>'), 'HTML 不应该包含未转义脚本概念');
    assert(html.includes('&lt;script&gt;alert(1)&lt;/script&gt;'), 'HTML 应该包含转义后的脚本概念');
    console.log('✅ 测试 15: HTML 转义 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 15: HTML 转义 - 失败:', e.message);
    failed++;
  }

  // 测试 16: DOT 输出转义引号
  try {
    const dotDir = fs.mkdtempSync(path.join(os.tmpdir(), 'knowledge-connector-dot-'));
    const dotKc = new KnowledgeConnector({ dataDir: dotDir });
    await dotKc.saveConcepts([{
      id: 'quoted',
      name: 'danger"node',
      type: 'term',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }]);
    const dot = await dotKc.visualize({ format: 'dot' });
    assert(dot.includes('danger\\"node'), 'DOT label 应该转义引号');
    console.log('✅ 测试 16: DOT 转义 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 16: DOT 转义 - 失败:', e.message);
    failed++;
  }

  // 测试 17: Doctor 自检
  try {
    const doctor = kc.doctor();
    assert(Array.isArray(doctor.checks), 'doctor 应该返回检查项');
    assert(doctor.version === '1.3.0', 'doctor 应该读取当前包版本');
    assert(doctor.checks.some((check) => check.name === 'CLI entry file exists' && check.ok), 'doctor 应该检查 CLI 文件');
    console.log('✅ 测试 17: Doctor 自检 - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 17: Doctor 自检 - 失败:', e.message);
    failed++;
  }

  // 测试 18: CLI doctor 在未安装依赖时也可运行
  try {
    const cliPath = path.join(__dirname, '..', 'bin', 'cli.js');
    const cliDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'knowledge-connector-cli-'));
    const output = childProcess.execFileSync(process.execPath, [cliPath, 'doctor'], {
      encoding: 'utf-8',
      env: { ...process.env, KC_DATA_DIR: cliDataDir }
    });
    assert(output.includes('Knowledge Connector Doctor'), 'CLI doctor 应该输出自检标题');
    assert(output.includes('1.3.0'), 'CLI doctor 应该输出版本');
    console.log('✅ 测试 18: CLI Doctor fallback - 通过');
    passed++;
  } catch (e) {
    console.log('❌ 测试 18: CLI Doctor fallback - 失败:', e.message);
    failed++;
  }
  
  console.log('\n' + '='.repeat(40));
  console.log(`测试结果: ${passed} 通过, ${failed} 失败`);
  console.log('='.repeat(40));
  
  process.exit(failed > 0 ? 1 : 0);
}

runTests();
