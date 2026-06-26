/**
 * 测试新的咨询按钮选择器
 */
const playwright = require('playwright')
const hospitals = require('./data/hospitals.json')

async function testNewSelectors() {
  const jdHospital = hospitals.find(h => h.name.includes('JD') || h.name.includes('皮肤科'))
  const url = jdHospital.url

  console.log(`\n🧪 测试新选择器: ${jdHospital.name}\n`)

  let browser
  try {
    browser = await playwright.chromium.launch({ headless: false })
    const context = await browser.newContext()
    const page = await context.newPage()

    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 }).catch(() => {})
    await page.waitForTimeout(5000)

    const newSelectors = [
      '.btns-consult',
      '.btns-right:has-text("咨询一下")',
      'uni-view.btns-consult',
      'text=/咨询一下/',
    ]

    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`🧪 测试新的 Playwright 选择器`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)

    for (const selector of newSelectors) {
      try {
        const locator = page.locator(selector)
        const count = await locator.count()

        if (count > 0) {
          const isVisible = await locator.first().isVisible().catch(() => false)
          
          console.log(`✅ [${selector}]`)
          console.log(`   ✓ 找到 ${count} 个元素`)
          console.log(`   ✓ 可见: ${isVisible}`)

          if (isVisible) {
            console.log(`   🎯 这个选择器可以用！`)
            
            // 尝试点击
            try {
              await locator.first().scrollIntoViewIfNeeded()
              await page.waitForTimeout(500)
              await locator.first().click()
              console.log(`   ✅ 点击成功！`)
              await page.waitForTimeout(2000)
            } catch (e) {
              console.log(`   ⚠️  点击失败: ${e.message}`)
            }
          }
          console.log()
        }
      } catch (e) {
        console.log(`❌ [${selector}]`)
        console.log(`   错误: ${e.message}\n`)
      }
    }

    console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`📋 选择器测试完成！`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    
    await page.waitForTimeout(30000)

  } catch (err) {
    console.error('❌ 错误:', err.message)
  } finally {
    if (browser) await browser.close()
  }
}

testNewSelectors()
