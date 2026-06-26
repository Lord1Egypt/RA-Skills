#!/usr/bin/env node

/**
 * 简单测试脚本
 * 验证药学系统招标信息收集技能的基本功能
 */

const PharmaceuticalBiddingCollector = require('./main');

async function runTests() {
  console.log('开始测试药学系统招标信息收集技能...\n');
  
  const collector = new PharmaceuticalBiddingCollector();
  
  try {
    // 测试1: 验证药学系统判断
    console.log('测试1: 验证药学系统判断');
    const testCases = [
      { title: '医院药学管理系统采购项目', description: '用于医院药房管理的综合系统' },
      { title: '药品库存管理系统', description: '药品库存管理软件' },
      { title: '办公设备采购项目', description: '办公电脑和打印机' }
    ];
    
    testCases.forEach((testCase, index) => {
      const result = collector.isPharmaceuticalSystem(testCase);
      console.log(`  ${index + 1}. "${testCase.title}" - ${result ? '✓ 药学系统' : '✗ 非药学系统'}`);
    });
    
    // 测试2: 验证截止时间判断
    console.log('\n测试2: 验证截止时间判断');
    const deadlineTestCases = [
      { deadline: moment().add(3, 'days').format('YYYY-MM-DD') }, // >2天
      { deadline: moment().add(1, 'days').format('YYYY-MM-DD') }  // <2天
    ];
    
    deadlineTestCases.forEach((testCase, index) => {
      const result = collector.hasValidDeadline(testCase);
      console.log(`  ${index + 1}. 截止时间: ${testCase.deadline} - ${result ? '✓ 有效' : '✗ 无效'}`);
    });
    
    // 测试3: 验证项目参与条件
    console.log('\n测试3: 验证项目参与条件');
    const projectTestCases = [
      {
        title: '三级医院药学系统',
        biddingUnit: '某某市第三人民医院',
        budget: 2000000,
        openingDate: moment().add(15, 'days').format('YYYY-MM-DD'),
        deadline: moment().add(5, 'days').format('YYYY-MM-DD')
      },
      {
        title: '县医院药房系统',
        biddingUnit: '某某县人民医院',
        budget: 800000,
        openingDate: moment().add(5, 'days').format('YYYY-MM-DD'),
        deadline: moment().add(1, 'days').format('YYYY-MM-DD')
      }
    ];
    
    projectTestCases.forEach((testCase, index) => {
      const result = collector.shouldParticipate(testCase);
      console.log(`  ${index + 1}. "${testCase.title}" - ${result ? '✓ 可参与' : '✗ 不可参与'}`);
    });
    
    console.log('\n✅ 所有测试完成');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    process.exit(1);
  }
}

// 如果直接运行此脚本，执行测试
if (require.main === module) {
  runTests();
}

module.exports = { runTests };