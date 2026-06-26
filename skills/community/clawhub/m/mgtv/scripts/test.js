#!/usr/bin/env node

/**
 * MGTV Skill 快速测试脚本
 * 
 * 运行几个测试用例来验证功能
 */

const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

async function runTest(name, command) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`测试：${name}`);
  console.log(`命令：${command}`);
  console.log('='.repeat(60));
  
  try {
    const { stdout, stderr } = await execAsync(`node ${command}`);
    console.log(stdout);
    if (stderr) console.error(stderr);
    return true;
  } catch (error) {
    console.error(`测试失败：${error.message}`);
    return false;
  }
}

async function main() {
  console.log('\n🎬 MGTV Skill 测试套件\n');
  
  const tests = [
    {
      name: '搜索综艺节目',
      command: 'scripts/search-mgtv.js --query "歌手"'
    },
    {
      name: '搜索电视剧',
      command: 'scripts/search-mgtv.js --query "繁花"'
    },
    {
      name: '直接打开芒果 TV',
      command: 'scripts/search-mgtv.js --direct-url "https://www.mgtv.com"'
    }
  ];
  
  let passed = 0;
  let failed = 0;
  
  for (const test of tests) {
    const success = await runTest(test.name, test.command);
    if (success) {
      passed++;
    } else {
      failed++;
    }
    
    // 等待一下，避免打开太多浏览器窗口
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('测试结果');
  console.log('='.repeat(60));
  console.log(`通过：${passed}`);
  console.log(`失败：${failed}`);
  console.log(`总计：${tests.length}`);
  console.log('='.repeat(60) + '\n');
  
  if (failed > 0) {
    process.exit(1);
  }
}

main().catch(error => {
  console.error('测试执行失败:', error.message);
  process.exit(1);
});
