#!/usr/bin/env node

/**
 * 多轮对话流程测试脚本
 * 演示如何通过多轮对话完成预约流程
 */

const skill = require('./api/skill')

async function testMultiTurnFlow() {
  console.log('='.repeat(60))
  console.log('韩国医美预约 Skill - 多轮对话测试')
  console.log('='.repeat(60))
  
  // 第1轮：用户询问预约流程
  console.log('\n【第1轮】用户询问预约流程')
  console.log('> 用户输入: "CNP皮肤科怎么预约？"')
  console.log('-'.repeat(60))
  
  let result = await skill({
    query: 'CNP皮肤科怎么预约',
    lang: 'zh'
  })
  console.log(result)
  
  // 第2轮：用户选择打开链接
  console.log('\n【第2轮】用户选择打开链接')
  console.log('> 用户输入: "打开链接"')
  console.log('-'.repeat(60))
  
  result = await skill({
    query: '打开链接',
    lang: 'zh'
  })
  console.log(result)
  
  // 第3轮：用户选择自动预约
  console.log('\n【第3轮】用户选择自动预约')
  console.log('> 用户输入: "帮我预约"')
  console.log('-'.repeat(60))
  
  result = await skill({
    query: 'CNP皮肤科怎么预约', // 需要包含医院名
    lang: 'zh'
  })
  console.log(result)
  
  // 模拟自动预约操作
  result = await skill({
    query: '帮我预约',
    lang: 'zh'
  })
  console.log(result)
  
  console.log('\n' + '='.repeat(60))
  console.log('测试完成！')
  console.log('='.repeat(60))
}

// 运行测试
testMultiTurnFlow().catch(err => {
  console.error('测试失败:', err)
  process.exit(1)
})
