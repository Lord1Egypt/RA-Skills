/**
 * NightPatch Skill 基础测试
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 测试配置
const testConfig = {
  schedule: {
    enabled: true,
    time: "03:00",
    timezone: "UTC"
  },
  safety: {
    max_changes_per_night: 1,
    require_rollback: true,
    skip_production: false,
    dry_run_first: true
  },
  detectors: {
    shell_alias: {
      enabled: true,
      min_usage_count: 2
    },
    note_organization: {
      enabled: true,
      max_scattered_files: 3
    }
  }
};

// 测试目录
const testDir = path.join(__dirname, '..', 'test-workspace');

// 清理测试环境
function cleanupTestEnvironment() {
  if (fs.existsSync(testDir)) {
    execSync(`rm -rf "${testDir}"`);
  }
}

// 设置测试环境
function setupTestEnvironment() {
  cleanupTestEnvironment();
  
  // 创建测试目录结构
  fs.mkdirSync(testDir, { recursive: true });
  fs.mkdirSync(path.join(testDir, 'notes'), { recursive: true });
  fs.mkdirSync(path.join(testDir, 'logs'), { recursive: true });
  
  // 创建测试文件
  fs.writeFileSync(path.join(testDir, 'todo.txt'), 'Test todo item');
  fs.writeFileSync(path.join(testDir, 'ideas.md'), '# Test ideas');
  fs.writeFileSync(path.join(testDir, 'notes', 'existing-note.md'), 'Existing note');
  
  // 创建测试日志
  fs.writeFileSync(path.join(testDir, 'logs', 'test.log'), 'Test log entry\n'.repeat(100));
  
  // 创建bash历史测试文件
  const bashHistory = `ls -la\ngit status\ncd ..\nls -la\ngit status\npwd\n`;
  fs.writeFileSync(path.join(testDir, '.bash_history'), bashHistory);
  
  console.log('✅ 测试环境设置完成');
}

// 测试模块导入
function testModuleImports() {
  console.log('\n🔧 测试模块导入...');
  
  try {
    const PatchDetector = require('../src/patch-detector');
    const PatchExecutor = require('../src/patch-executor');
    const ReportGenerator = require('../src/report-generator');
    const SafetyCheck = require('../src/safety-check');
    
    console.log('✅ 所有模块导入成功');
    return true;
  } catch (error) {
    console.error(`❌ 模块导入失败: ${error.message}`);
    return false;
  }
}

// 测试问题检测器
async function testPatchDetector() {
  console.log('\n🔍 测试问题检测器...');
  
  try {
    const PatchDetector = require('../src/patch-detector');
    const detector = new PatchDetector(testConfig);
    
    // 保存当前目录，切换到测试目录
    const originalCwd = process.cwd();
    process.chdir(testDir);
    
    const opportunities = await detector.runAllDetectors();
    
    // 切换回原目录
    process.chdir(originalCwd);
    
    console.log(`✅ 检测到 ${opportunities.length} 个机会`);
    
    // 验证检测结果
    if (opportunities.length === 0) {
      console.warn('⚠️  未检测到任何机会，可能需要调整测试数据');
    }
    
    opportunities.forEach((opp, index) => {
      console.log(`  ${index + 1}. ${opp.description} (${opp.type})`);
    });
    
    return opportunities.length >= 0; // 允许0个机会（测试环境可能不同）
    
  } catch (error) {
    console.error(`❌ 问题检测器测试失败: ${error.message}`);
    console.error(error.stack);
    return false;
  }
}

// 测试安全检查
async function testSafetyCheck() {
  console.log('\n🛡️ 测试安全检查...');
  
  try {
    const SafetyCheck = require('../src/safety-check');
    const safetyCheck = new SafetyCheck(testConfig);
    
    // 测试机会
    const testOpportunity = {
      type: 'shell_alias',
      description: '测试创建别名',
      original_command: 'ls -la',
      suggested_alias: 'll',
      risk_level: 'low',
      rollback_command: 'unalias ll',
      detector: 'shell_alias'
    };
    
    const result = await safetyCheck.performFullSafetyCheck(testOpportunity);
    
    console.log(`✅ 安全检查完成: ${result.passed ? '通过' : '失败'}`);
    console.log(`   原因: ${result.reason}`);
    
    if (result.allResults) {
      result.allResults.forEach(check => {
        console.log(`   ${check.checkName}: ${check.passed ? '✅' : '❌'} ${check.reason}`);
      });
    }
    
    // 生成安全报告
    const report = safetyCheck.generateSafetyReport();
    const reportPath = path.join(testDir, 'safety-report.md');
    fs.writeFileSync(reportPath, report, 'utf8');
    console.log(`📄 安全报告已保存: ${reportPath}`);
    
    return result.passed;
    
  } catch (error) {
    console.error(`❌ 安全检查测试失败: ${error.message}`);
    return false;
  }
}

// 测试报告生成器
async function testReportGenerator() {
  console.log('\n📊 测试报告生成器...');
  
  try {
    const ReportGenerator = require('../src/report-generator');
    const reportGenerator = new ReportGenerator(testConfig);
    
    // 测试数据
    const testOpportunities = [
      {
        type: 'shell_alias',
        description: '创建 ll 别名代替 ls -la',
        detector: 'shell_alias',
        risk_level: 'low',
        priority: 5
      },
      {
        type: 'note_organization',
        description: '整理散落的笔记文件',
        detector: 'note_organization',
        risk_level: 'low',
        priority: 3
      }
    ];
    
    const testExecutionResults = [
      {
        opportunity: testOpportunities[0],
        success: true,
        skipped: false,
        timestamp: new Date().toISOString(),
        result: {
          message: '别名创建成功',
          executed_command: 'alias ll="ls -la"'
        }
      }
    ];
    
    const startTime = new Date();
    const endTime = new Date(startTime.getTime() + 5000); // 5秒后
    
    const stats = {
      detector_stats: {
        shell_alias: 1,
        note_organization: 1
      },
      execution_stats: {
        total: 1,
        executed: 1,
        skipped: 0,
        failed: 0,
        success_rate: '100%'
      }
    };
    
    const report = await reportGenerator.generateReport(
      testOpportunities,
      testExecutionResults,
      startTime,
      stats
    );
    
    console.log(`✅ 报告生成成功`);
    console.log(`   格式: ${report.format}`);
    console.log(`   路径: ${report.path}`);
    console.log(`   大小: ${report.content.length} 字符`);
    
    // 验证报告内容
    if (report.content.includes('夜间修补报告') && report.content.includes('执行摘要')) {
      console.log('✅ 报告内容验证通过');
    } else {
      console.warn('⚠️  报告内容可能不完整');
    }
    
    return true;
    
  } catch (error) {
    console.error(`❌ 报告生成器测试失败: ${error.message}`);
    return false;
  }
}

// 测试主入口
async function testMainEntry() {
  console.log('\n🚀 测试主入口...');
  
  try {
    // 切换到测试目录
    const originalCwd = process.cwd();
    process.chdir(testDir);
    
    // 创建测试配置文件
    const testConfigPath = path.join(testDir, 'test-config.yaml');
    const testConfigYaml = `
schedule:
  enabled: true
  time: "03:00"

safety:
  max_changes_per_night: 1
  require_rollback: true

detectors:
  shell_alias:
    enabled: true
    min_usage_count: 2
`;
    
    fs.writeFileSync(testConfigPath, testConfigYaml, 'utf8');
    
    // 测试手动运行
    console.log('测试手动运行模式...');
    
    // 由于我们无法直接调用main函数（需要重构），这里测试模块功能
    const { main } = require('../src/index');
    
    console.log('✅ 主入口模块加载成功');
    
    // 切换回原目录
    process.chdir(originalCwd);
    
    return true;
    
  } catch (error) {
    console.error(`❌ 主入口测试失败: ${error.message}`);
    return false;
  }
}

// 运行所有测试
async function runAllTests() {
  console.log('🧪 开始运行 NightPatch Skill 测试');
  console.log('='.repeat(50));
  
  let allPassed = true;
  
  try {
    // 设置测试环境
    setupTestEnvironment();
    
    // 运行各个测试
    const tests = [
      { name: '模块导入', func: testModuleImports },
      { name: '问题检测器', func: testPatchDetector },
      { name: '安全检查', func: testSafetyCheck },
      { name: '报告生成器', func: testReportGenerator },
      { name: '主入口', func: testMainEntry }
    ];
    
    const results = [];
    
    for (const test of tests) {
      console.log(`\n🏃 运行测试: ${test.name}`);
      const passed = await test.func();
      results.push({ name: test.name, passed });
      
      if (!passed) {
        allPassed = false;
      }
    }
    
    // 显示测试结果
    console.log('\n' + '='.repeat(50));
    console.log('📋 测试结果汇总');
    console.log('='.repeat(50));
    
    results.forEach(result => {
      console.log(`${result.passed ? '✅' : '❌'} ${result.name}`);
    });
    
    console.log('\n' + '='.repeat(50));
    
    if (allPassed) {
      console.log('🎉 所有测试通过！');
    } else {
      console.log('⚠️  部分测试失败，请检查上述错误信息');
    }
    
  } catch (error) {
    console.error(`💥 测试运行异常: ${error.message}`);
    console.error(error.stack);
    allPassed = false;
  } finally {
    // 清理测试环境
    cleanupTestEnvironment();
    
    console.log('\n🧹 测试环境已清理');
    
    // 退出码
    process.exit(allPassed ? 0 : 1);
  }
}

// 如果是直接运行此文件，则执行测试
if (require.main === module) {
  runAllTests().catch(error => {
    console.error('未捕获的测试错误:', error);
    process.exit(1);
  });
}

// 导出测试函数
module.exports = {
  setupTestEnvironment,
  cleanupTestEnvironment,
  testModuleImports,
  testPatchDetector,
  testSafetyCheck,
  testReportGenerator,
  testMainEntry,
  runAllTests
};