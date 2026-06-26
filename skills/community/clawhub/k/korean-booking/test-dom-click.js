/**
 * 用 DOM 查询测试点击
 */
const playwright = require('playwright')
const hospitals = require('./data/hospitals.json')

async function testClickViaDom() {
  const jdHospital = hospitals.find(h => h.name.includes('JD') || h.name.includes('皮肤科'))
  const url = jdHospital.url

  console.log(`\n🧪 用 DOM 查询测试点击: ${jdHospital.name}\n`)

  let browser
  try {
    browser = await playwright.chromium.launch({ headless: false })
    const context = await browser.newContext()
    const page = await context.newPage()

    console.log(`📍 加载页面: ${url}`)
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 }).catch(() => {})
    
    console.log(`⏳ 等待 Vue 渲染...`)
    await page.waitForTimeout(5000)
    console.log(`✅ 页面准备好\n`)

    // 方法 1: 查找 .btns-consult class
    console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`方法 1: 查找 .btns-consult 元素`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)

    const foundByClass = await page.evaluate(() => {
      const el = document.querySelector('.btns-consult')
      if (el) {
        return {
          found: true,
          tag: el.tagName,
          text: el.textContent.trim(),
          class: el.className,
          html: el.outerHTML.substring(0, 200),
        }
      }
      return { found: false }
    })

    if (foundByClass.found) {
      console.log(`✅ 找到元素！`)
      console.log(`   标签: ${foundByClass.tag}`)
      console.log(`   文本: "${foundByClass.text}"`)
      console.log(`   class: ${foundByClass.class}`)
      console.log(`   HTML: ${foundByClass.html}`)
    } else {
      console.log(`❌ 未找到`)
    }

    // 方法 2: 尝试点击
    console.log(`\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`方法 2: 尝试点击`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)

    const clicked = await page.evaluate(() => {
      const el = document.querySelector('.btns-consult')
      if (!el) {
        return { success: false, reason: 'element not found' }
      }

      // 检查是否可见
      const rect = el.getBoundingClientRect()
      if (rect.width === 0 || rect.height === 0) {
        return { success: false, reason: 'element has zero dimensions' }
      }

      // 检查是否在视口中
      if (rect.top < 0 || rect.left < 0 || rect.top > window.innerHeight || rect.left > window.innerWidth) {
        return { success: false, reason: 'element not in viewport', rect }
      }

      // 尝试点击
      try {
        el.click()
        return { success: true, rect }
      } catch (e) {
        return { success: false, reason: e.message }
      }
    })

    console.log(`结果:`)
    console.log(JSON.stringify(clicked, null, 2))

    if (clicked.success) {
      console.log(`\n✅ 点击成功！`)
      await page.waitForTimeout(3000)
    } else {
      console.log(`\n❌ 点击失败: ${clicked.reason}`)
    }

    // 方法 3: 使用 Playwright 的 evaluate 获取更多信息
    console.log(`\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`方法 3: 检查 uni-view 组件`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)

    const uniViewInfo = await page.evaluate(() => {
      const elements = document.querySelectorAll('uni-view')
      const consultViews = []

      for (const el of elements) {
        if (el.textContent.includes('咨询')) {
          consultViews.push({
            text: el.textContent.trim().substring(0, 50),
            class: el.className,
            attrs: Array.from(el.attributes).map(a => ({ name: a.name, value: a.value })),
          })
        }
      }

      return {
        totalUniViews: elements.length,
        consultUniViews: consultViews,
      }
    })

    console.log(`找到 ${uniViewInfo.totalUniViews} 个 <uni-view> 元素`)
    console.log(`其中 ${uniViewInfo.consultUniViews.length} 个包含"咨询"`)
    
    uniViewInfo.consultUniViews.forEach((view, idx) => {
      console.log(`\n[${idx}] 文本: "${view.text}"`)
      console.log(`    class: ${view.class}`)
      console.log(`    其他属性:`)
      view.attrs.forEach(attr => {
        if (attr.name !== 'class' && attr.name !== 'style') {
          console.log(`      ${attr.name}: ${attr.value}`)
        }
      })
    })

    console.log(`\n\n✅ 诊断完成！浏览器保持打开 30 秒...`)
    await page.waitForTimeout(30000)

  } catch (err) {
    console.error('❌ 错误:', err.message)
  } finally {
    if (browser) await browser.close()
  }
}

testClickViaDom()
