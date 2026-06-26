const playwright = require('playwright')

async function inspectConsultButton() {
  let browser
  try {
    browser = await playwright.chromium.launch({ headless: false })
    const context = await browser.newContext()
    const page = await context.newPage()
    
    // 打开 JD 医院页面，用更宽松的等待条件
    const url = 'https://i.beautsgo.com/cn/hospital/jdclinic?from=google_map'
    console.log(`🌐 打开页面: ${url}`)
    
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 })
    } catch (e) {
      console.log(`⚠️ 页面加载超时，继续执行: ${e.message}`)
    }
    
    console.log(`✅ 页面已加载\n`)
    
    // 等待一下让页面完全渲染
    await page.waitForTimeout(3000)
    
    // 查找所有可能的咨询按钮
    console.log('📍 正在搜索咨询相关元素...\n')
    
    // 查找所有 button 元素
    const allButtons = await page.locator('button').all()
    console.log(`总共找到 ${allButtons.length} 个 button 元素\n`)
    
    // 打印所有按钮
    console.log('所有按钮:')
    for (let i = 0; i < allButtons.length; i++) {
      try {
        const text = await allButtons[i].textContent()
        const visible = await allButtons[i].isVisible().catch(() => false)
        console.log(`  [${i}] "${text.trim()}" (visible: ${visible})`)
      } catch (e) {
        console.log(`  [${i}] <error reading>`)
      }
    }
    
    // 查找包含"咨询"的元素
    console.log('\n🔍 查找包含"咨询"的元素...')
    try {
      const consultElements = await page.locator('text=/咨询/').all()
      console.log(`找到 ${consultElements.length} 个\n`)
      
      for (let i = 0; i < Math.min(3, consultElements.length); i++) {
        const text = await consultElements[i].textContent()
        const visible = await consultElements[i].isVisible()
        console.log(`  [${i}] "${text}" (visible: ${visible})`)
      }
    } catch (e) {
      console.log(`错误: ${e.message}`)
    }
    
    console.log('\n✅ 检查完成。浏览器窗口将在 20 秒后关闭。')
    await page.waitForTimeout(20000)
  } catch (err) {
    console.error('❌ 错误:', err.message)
  } finally {
    if (browser) await browser.close()
  }
}

inspectConsultButton()
