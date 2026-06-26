#!/usr/bin/env node

/**
 * 完整的多轮对话流程测试
 * 模拟用户与 OpenClaw 中的 korean-booking skill 的交互
 */

const skill = require('./api/skill')

async function runCompleteTest() {
  console.log('\n' + '='.repeat(70))
  console.log('🚀 韩国医美预约 Skill v2.1.0 - 完整流程测试')
  console.log('='.repeat(70) + '\n')
  
  try {
    // 第1轮：用户询问预约流程
    console.log('【第1轮】用户询问预约流程')
    console.log('📱 用户输入: "怎么预约 CNP 皮肤科?"')
    console.log('-'.repeat(70))
    
    let result = await skill({
      query: '怎么预约 CNP 皮肤科',
      lang: 'zh'
    })
    console.log(result)
    
    // 第2轮：用户选择打开链接（需要重复医院名称以便识别）
    console.log('\n\n【第2轮】用户选择打开链接')
    console.log('📱 用户输入: "打开 CNP 皮肤科 的链接"')
    console.log('-'.repeat(70))
    console.log('⏳ 等待浏览器打开...')
    
    result = await skill({
      query: '打开 CNP 皮肤科 的链接',
      lang: 'zh'
    })
    console.log(result)
    
    // 延迟，让用户看到浏览器
    await new Promise(resolve => setTimeout(resolve, 3000))
    
    // 第3轮：用户选择帮我预约
    console.log('\n\n【第3轮】用户选择自动预约')
    console.log('📱 用户输入: "帮我预约 CNP"')
    console.log('-'.repeat(70))
    console.log('⏳ Playwright 自动打开浏览器并点击预约按钮...')
    
    result = await skill({
      query: '帮我预约 CNP 皮肤科',
      lang: 'zh'
    })
    console.log(result)
    
    // 延迟，让用户看到自动化过程
    await new Promise(resolve => setTimeout(resolve, 3000))
    
    // 第4轮：用户选择咨询客服
    console.log('\n\n【第4轮】用户选择咨询客服')
    console.log('📱 用户输入: "咨询 CNP 皮肤科 客服"')
    console.log('-'.repeat(70))
    console.log('⏳ 自动打开浏览器并点击咨询按钮...')
    
    result = await skill({
      query: 'CNP 皮肤科 咨询客服',
      lang: 'zh'
    })
    console.log(result)
    
    // 延迟
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    console.log('\n' + '='.repeat(70))
    console.log('✅ 测试完成！')
    console.log('='.repeat(70))
    console.log('\n📊 测试总结：')
    console.log('  ✓ 第1轮: 预约流程查询')
    console.log('  ✓ 第2轮: 打开链接自动化')
    console.log('  ✓ 第3轮: 预约按钮自动化')
    console.log('  ✓ 第4轮: 咨询按钮自动化')
    console.log('\n💡 提示：')
    console.log('  • 浏览器窗口应该已在后台打开')
    console.log('  • 请检查浏览器中是否显示 BeautsGO 的医院页面')
    console.log('  • 如果自动化成功，应该看到预约表单或客服对话框')
    console.log('\n')
    
  } catch (err) {
    console.error('❌ 测试失败:', err.message)
    console.error(err)
    process.exit(1)
  }
}

// 运行测试
runCompleteTest()
