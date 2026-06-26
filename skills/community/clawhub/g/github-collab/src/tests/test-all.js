/**
 * 测试运行器 - 运行所有测试
 */

const { execSync } = require('child_process');
const path = require('path');

const testFiles = [
  'test-task-manager.js',
  'test-agent-binding.js',
  'test-stp-integration.js',
  'test-integration.js',
  'test-performance.js'
];

console.log('🚀 开始运行所有测试...\n');

let passed = 0;
let failed = 0;

for (const file of testFiles) {
  const filePath = path.join(__dirname, file);

  try {
    console.log(`📋 运行测试：${file}`);
    execSync(`node ${filePath}`, {
      stdio: 'inherit',
      cwd: __dirname
    });
    passed++;
    console.log(`✅ ${file} 通过\n`);
  } catch (error) {
    failed++;
    console.log(`❌ ${file} 失败\n`);
  }
}

console.log('\n📊 测试结果汇总:');
console.log(`✅ 通过：${passed}`);
console.log(`❌ 失败：${failed}`);
console.log(`📈 总计：${testFiles.length}`);

if (failed > 0) {
  process.exit(1);
}
