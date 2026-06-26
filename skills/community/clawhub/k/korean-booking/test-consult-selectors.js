/**
 * 测试咨询按钮选择器
 * 诊断 clickConsultButton 为什么失败
 */
const playwright = require('playwright')
const hospitals = require('./data/hospitals.json')

async function testConsultSelectors() {
  // 获取 JD 皮肤科的 URL
  const jdHospital = hospitals.find(h => h.name.includes('JD') || h.name.includes('皮肤科'))
  if (!jdHospital) {
    console.error('❌ 找不到 JD 皮肤科医院')
    return
  }

  const url = jdHospital.url
  console.log(`\n🔍 测试医院：${jdHospital.name}`)
  console.log(`📍 URL: ${url}\n`)

  let browser
  try {
    browser = await playwright.chromium.launch({ headless: false })
    const context = await browser.newContext()
    const page = await context.newPage()

    // 设置 console 消息监听，看浏览器输出
    page.on('console', msg => {
      console.log(`[浏览器输出] ${msg.type()}: ${msg.text()}`)
    })

    console.log(`⏳ 正在加载页面...`)
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 }).catch(() => {})

    console.log(`⏳ 等待 Vue 组件渲染（5秒）...`)
    await page.waitForTimeout(5000)

    console.log(`✅ 页面加载完成\n`)

    // 测试 1: 使用 Playwright 选择器
    console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`🧪 测试 Playwright 选择器`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)

    const consultSelectors = [
      'text=/咨询一下/',
      'text=/立即咨询/',
      '[class*="btn"]:has-text("咨询")',
      'div:has-text("咨询一下")',
      'text=/咨询/',
      'text=/客服/',
      'button:has-text("咨询一下")',
      'button:has-text("咨询")',
      '[onclick*="consult"]',
      '.consult-btn',
      '.service-btn',
    ]

    for (const selector of consultSelectors) {
      try {
        const locator = page.locator(selector)
        const count = await locator.count()

        if (count > 0) {
          const isVisible = await locator.first().isVisible().catch(() => false)
          const text = await locator.first().textContent().catch(() => '无法读取')
          
          console.log(`✅ [${selector}]`)
          console.log(`   找到: ${count} 个元素`)
          console.log(`   可见: ${isVisible}`)
          console.log(`   文本: ${text}`)
          console.log()
        }
      } catch (e) {
        // 跳过错误
      }
    }

    // 测试 2: 使用 DOM 查询
    console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`🧪 测试 DOM 查询`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)

    const domResults = await page.evaluate(() => {
      const allElements = document.querySelectorAll('*')
      console.log(`页面总元素数: ${allElements.length}`)

      const candidates = []
      for (const el of allElements) {
        const text = (el.textContent || '').trim()
        // 查找包含"咨询"的元素
        if (text.includes('咨询') && text.length < 100) {
          const tagName = el.tagName
          const className = el.className
          const isVisible = el.offsetParent !== null
          const rect = el.getBoundingClientRect()

          candidates.push({
            tagName,
            className,
            text: text.substring(0, 50), // 截断长文本
            isVisible,
            isClickable: el.offsetParent !== null && rect.width > 0 && rect.height > 0,
            rect: {
              width: rect.width,
              height: rect.height,
              x: rect.x,
              y: rect.y,
            }
          })
        }
      }

      return {
        totalElements: allElements.length,
        consultElements: candidates,
      }
    })

    console.log(`📊 找到 ${domResults.consultElements.length} 个包含"咨询"的元素:\n`)

    domResults.consultElements.forEach((el, idx) => {
      console.log(`[${idx + 1}] <${el.tagName.toLowerCase()}>`)
      console.log(`    Class: ${el.className || '(无)'}`)
      console.log(`    文本: "${el.text}"`)
      console.log(`    可见: ${el.isVisible}`)
      console.log(`    可点击: ${el.isClickable}`)
      console.log(`    尺寸: ${el.rect.width}x${el.rect.height}px`)
      console.log(`    位置: (${Math.round(el.rect.x)}, ${Math.round(el.rect.y)})`)
      console.log()
    })

    // 测试 3: 尝试点击第一个找到的元素
    if (domResults.consultElements.length > 0) {
      console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
      console.log(`🧪 尝试点击第一个"咨询"按钮`)
      console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)

      const firstClickable = domResults.consultElements.find(el => el.isClickable)
      if (firstClickable) {
        console.log(`📌 目标: ${firstClickable.text}`)
        
        try {
          // 滚动到元素
          await page.evaluate(() => {
            const elements = document.querySelectorAll('*')
            for (const el of elements) {
              if ((el.textContent || '').includes('咨询')) {
                el.scrollIntoView({ behavior: 'smooth', block: 'center' })
                break
              }
            }
          })
          
          await page.waitForTimeout(500)

          // 点击
          const clicked = await page.evaluate(() => {
            const elements = document.querySelectorAll('*')
            for (const el of elements) {
              const text = (el.textContent || '').trim()
              if (text.includes('咨询') && text.length < 100 && el.offsetParent !== null) {
                el.click()
                return true
              }
            }
            return false
          })

          if (clicked) {
            console.log(`✅ 点击成功！`)
            await page.waitForTimeout(2000)
          } else {
            console.log(`❌ 点击失败`)
          }
        } catch (e) {
          console.log(`❌ 点击异常: ${e.message}`)
        }
      } else {
        console.log(`⚠️  没有找到可点击的"咨询"按钮`)
      }
    }

    console.log(`\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`📋 诊断完成！`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`\n浏览器仍保持打开状态 60 秒，方便你检查页面结构...`)

    // 保持浏览器打开 60 秒
    await page.waitForTimeout(60000)

  } catch (err) {
    console.error('❌ 测试出错:', err.message)
  } finally {
    if (browser) {
      await browser.close()
      console.log(`\n✅ 浏览器已关闭`)
    }
  }
}

testConsultSelectors()
