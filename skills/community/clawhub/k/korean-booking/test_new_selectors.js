const playwright = require('playwright')

async function testNewSelectors() {
  let browser
  try {
    browser = await playwright.chromium.launch({ headless: false })
    const context = await browser.newContext()
    const page = await context.newPage()
    
    const url = 'https://i.beautsgo.com/cn/hospital/jdclinic?from=google_map'
    console.log(`🌐 打开页面: ${url}`)
    
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 }).catch(() => {})
    await page.waitForTimeout(3000)
    console.log(`✅ 页面已加载\n`)
    
    // 测试新的选择器
    const selectors = [
      'text=/咨询一下|立即咨询/',
      'div:has-text("咨询一下")',
      'span:has-text("咨询一下")',
      '[class*="btn"]:has-text("咨询")',
      'text=/咨询/',
    ]
    
    console.log('🔍 测试选择器:\n')
    for (const selector of selectors) {
      try {
        const elements = await page.locator(selector).all()
        console.log(`${selector}`)
        console.log(`  ├─ 找到: ${elements.length} 个`)
        
        // 检查可见性
        for (let i = 0; i < Math.min(3, elements.length); i++) {
          const visible = await elements[i].isVisible().catch(() => false)
          const text = await elements[i].textContent().catch(() => '<无法读取>')
          console.log(`  ├─ [${i}] ${text.trim().substring(0, 20)} (visible: ${visible})`)
        }
      } catch (e) {
        console.log(`${selector}`)
        console.log(`  └─ 错误: ${e.message}`)
      }
      console.log()
    }
    
    // 尝试用 evaluate 找到"咨询"元素
    console.log('🔍 使用 DOM evaluate 查找:\n')
    const result = await page.evaluate(() => {
      const allElements = document.querySelectorAll('*')
      const found = []
      
      for (const el of allElements) {
        const text = el.textContent || ''
        if (text.includes('咨询') && text.length < 50 && el.offsetParent !== null) {
          found.push({
            tag: el.tagName,
            text: text.substring(0, 30),
            class: el.className,
            id: el.id
          })
          if (found.length >= 5) break
        }
      }
      
      return found
    })
    
    console.log(`找到 ${result.length} 个包含"咨询"的可见元素:\n`)
    result.forEach((el, i) => {
      console.log(`  [${i}] <${el.tag} class="${el.class}"> ${el.text}`)
    })
    
    console.log('\n✅ 测试完成。浏览器将在 20 秒后关闭。')
    await page.waitForTimeout(20000)
  } catch (err) {
    console.error('❌ 错误:', err.message)
  } finally {
    if (browser) await browser.close()
  }
}

testNewSelectors()
