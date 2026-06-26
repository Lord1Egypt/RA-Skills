const { analyzeUpdateImpact, fetchReleaseNotes, scanLocalConfigs, analyzeImpact } = require('./index');

async function runTests() {
  console.log('🧪 开始运行 openclaw-upgrade-assistant 测试...\n');

  try {
    // 1. 测试 fetchReleaseNotes
    console.log('测试: fetchReleaseNotes');
    const releaseNotes = await fetchReleaseNotes('latest');
    if (!releaseNotes || !releaseNotes.version) {
      throw new Error('fetchReleaseNotes 失败');
    }
    console.log('✅ fetchReleaseNotes 成功\n');

    // 2. 测试 scanLocalConfigs
    console.log('测试: scanLocalConfigs');
    const configs = await scanLocalConfigs();
    if (!Array.isArray(configs)) {
      throw new Error('scanLocalConfigs 返回格式不正确');
    }
    console.log(`✅ scanLocalConfigs 成功 (扫描到 ${configs.length} 项)\n`);

    // 3. 测试 analyzeImpact
    console.log('测试: analyzeImpact');
    const impact = analyzeImpact(releaseNotes, configs);
    if (!impact || !impact.compatibilityCheck) {
      throw new Error('analyzeImpact 分析结果格式不正确');
    }
    console.log('✅ analyzeImpact 成功\n');

    console.log('🎉 所有基础测试通过！');
    process.exit(0);
  } catch (error) {
    console.error(`❌ 测试失败: ${error.message}`);
    process.exit(1);
  }
}

runTests();
