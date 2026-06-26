/**
 * Git Commit Helper 测试脚本
 */

const helper = require('./index.js');

async function runTest() {
  console.log('🧪 Git Commit Helper 测试开始...\n');

  try {
    // 模拟分析结果
    const mockAnalysis = {
      files: [
        { path: 'src/auth/login.js', changes: 50, additions: 45, deletions: 5 },
        { path: 'src/auth/login.test.js', changes: 30, additions: 30, deletions: 0 },
        { path: 'config.json', changes: 5, additions: 3, deletions: 2 }
      ],
      types: { feat: 2, test: 1, chore: 1 },
      scope: 'src',
      summary: ['新增 login.js', '新增 login.test.js', '更新 config.json'],
      type: 'feat'
    };

    console.log('1️⃣ 测试中文 commit message 生成...');
    const cnMessage = buildMessage(mockAnalysis, 'zh');
    console.log(cnMessage);
    console.log('');

    console.log('2️⃣ 测试英文 commit message 生成...');
    const enMessage = buildMessage(mockAnalysis, 'en');
    console.log(enMessage);
    console.log('');

    console.log('✅ 测试完成!\n');
    console.log('注意：完整测试需要在 git 仓库中运行');
    console.log('运行：node test.js 在 git 项目中');

  } catch (error) {
    console.error('❌ 测试出错:', error.message);
  }
}

// 辅助函数（复用逻辑）
function buildMessage(analysis, language) {
  const typeLabels = {
    feat: { zh: '添加新功能', en: 'Add new feature' },
    fix: { zh: '修复问题', en: 'Fix issue' },
    docs: { zh: '更新文档', en: 'Update documentation' }
  };

  const scope = analysis.scope ? `(${analysis.scope})` : '';
  const label = typeLabels[analysis.type]?.[language] || 'Update';
  
  let title = `${analysis.type}${scope}: ${label}`;
  
  if (analysis.files.length > 0) {
    const count = analysis.files.length;
    title += language === 'zh' 
      ? ` (${count} 个文件)`
      : ` (${count} files)`;
  }

  const body = analysis.summary.map(s => `- ${s}`).join('\n');
  
  return `${title}\n\n${body}`;
}

runTest();
