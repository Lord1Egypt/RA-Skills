const playwright = require('playwright')

async function inspectConsultButton() {
  let browser
  try {
    browser = await playwright.chromium.launch({ headless: false })
    const context = await browser.newContext()
    const page = await context.newPage()
    
    // 打开 JD 医院页面
    const url = 'https://i.beautsgo.com/cn/hospital/jdclinic?from=google_map'
    console.log(`🌐 打开页面: ${url}`)
    await page.goto(url, { waitUntil: 'networkidle' })
    console.log(`✅ 页面已加载\n`)
    
    // 等待一下让页面完全渲染
    await page.waitForTimeout(3000)
    
    // 查找所有可能的咨询按钮
    console.log('📍 正在搜索咨询相关元素...\n')
    
    // 1. 查找包含"咨询"的元素
    const consultElements = await page.locator('text=/咨询|客服/').all()
    console.log(`1️⃣ 包含"咨询"或"客服"的元素: ${consultElements.length} 个`)
    
    // 2. 查找所有 button 元素
    const allButtons = await page.locator('button, [role="button"]').all()
    console.log(`2️⃣ 所有 button/role="button" 元素: ${allButtons.length} 个`)
    
    // 打印前 10 个按钮
    console.log('\n按钮列表:')
    for (let i = 0; i < Math.min(10, allButtons.length); i++) {
      const text = await allButtons[i].textContent()
      const visible = await allButtons[i].isVisible().catch(() => false)
      const classList = await allButtons[i].evaluate(el => el.className)
      console.log(`  [${i}] "${text.trim()}" | visible: ${visible} | class: ${classList}`)
    }
    
    // 查找"咨询一下"按钮
    console.log('\n🔍 查找"咨询一下"按钮...')
    try {
      const consultBtn = await page.locator('text="咨询一下"').first()
      const visible = await consultBtn.isVisible()
      console.log(`  状态: ${visible ? '✓ 可见' : '✗ 不可见'}`)
      
      if (visible) {
        console.log('✅ 找到！即将点击...')
        await consultBtn.click()
        console.log('✅ 已点击！')
        await page.waitForTimeout(3000)
      }
    } catch (e) {
      console.log(`  ✗ 错误: ${e.message}`)
    }
    
    console.log('\n✅ 检查完成。浏览器窗口将在 15 秒后关闭。')
    await page.waitForTimeout(15000)
  } catch (err) {
    console.error('❌ 错误:', err.message)
  } finally {
    if (browser) await browser.close()
  }
}

inspectConsultButton()
