/**
 * 增加等待时间，保存完整 HTML 快照
 */
const playwright = require('playwright')
const hospitals = require('./data/hospitals.json')
const fs = require('fs')

async function deepInspect() {
  const jdHospital = hospitals.find(h => h.name.includes('JD') || h.name.includes('皮肤科'))
  const url = jdHospital.url

  console.log(`\n🔍 深度检查: ${jdHospital.name}`)
  console.log(`URL: ${url}\n`)

  let browser
  try {
    browser = await playwright.chromium.launch({ headless: false })
    const context = await browser.newContext()
    const page = await context.newPage()

    // 监听所有网络请求
    page.on('response', response => {
      if (response.url().includes('beautsgo')) {
        console.log(`[Network] ${response.status()} ${response.url().substring(30)}`)
      }
    })

    console.log(`📍 加载页面...`)
    const response = await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 })
    console.log(`[Page Load] Status: ${response.status()}\n`)

    // 多轮等待
    for (let i = 1; i <= 5; i++) {
      console.log(`⏳ 等待第 ${i} 轮（${i * 2}秒）...`)
      await page.waitForTimeout(2000)

      // 每轮检查一次
      const found = await page.evaluate(() => {
        const els = document.querySelectorAll('[class*="consult"]')
        return els.length
      })

      console.log(`   找到 ${found} 个包含"consult"的元素`)

      if (found > 0) {
        break
      }
    }

    // 保存 HTML
    const html = await page.content()
    fs.writeFileSync('/Users/wangning/project/company/korean-aesthetic-booking-guide/page-full-snapshot.html', html)
    console.log(`\n✅ HTML 已保存到 page-full-snapshot.html (${Math.round(html.length / 1024)} KB)\n`)

    // 完整页面分析
    const analysis = await page.evaluate(() => {
      const result = {
        consultElements: [],
        uniViews: [],
        shadowDoms: [],
      }

      // 查找所有包含"咨询"的元素（任何深度）
      const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_ELEMENT,
        null,
        false
      )

      let node
      let count = 0
      while ((node = walker.nextNode()) && count < 100) {
        const text = (node.textContent || '').trim()
        const hasConsult = text.includes('咨询')
        const className = (node.className || '').toString()
        const hasConsultClass = className.includes('consult')

        if (hasConsult || hasConsultClass) {
          result.consultElements.push({
            tag: node.tagName,
            text: text.substring(0, 50),
            class: className,
            id: node.id,
            depth: getDepth(node),
          })
          count++
        }
      }

      // 查找所有 uni-view
      const uniViews = document.querySelectorAll('uni-view')
      for (let i = 0; i < Math.min(10, uniViews.length); i++) {
        const text = uniViews[i].textContent.trim()
        if (text.length > 0 && text.length < 100) {
          result.uniViews.push({
            text: text.substring(0, 50),
            class: uniViews[i].className,
            index: i,
          })
        }
      }

      // 检查 shadow DOM
      let els = document.querySelectorAll('*')
      for (let el of els) {
        if (el.shadowRoot) {
          result.shadowDoms.push({
            tag: el.tagName,
            class: el.className,
            content: el.shadowRoot.textContent.substring(0, 50),
          })
        }
      }

      function getDepth(node) {
        let depth = 0
        let parent = node.parentElement
        while (parent) {
          depth++
          parent = parent.parentElement
        }
        return depth
      }

      return result
    })

    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`📊 分析结果`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)

    console.log(`🎯 包含"咨询"的元素 (${analysis.consultElements.length} 个):\n`)
    analysis.consultElements.slice(0, 15).forEach((el, idx) => {
      console.log(`[${idx}] <${el.tag}> (深度: ${el.depth})`)
      console.log(`    class: ${el.class}`)
      console.log(`    text: "${el.text}"`)
      console.log()
    })

    console.log(`\n🔎 uni-view 元素 (前 ${analysis.uniViews.length} 个):\n`)
    analysis.uniViews.forEach((view, idx) => {
      console.log(`[${idx}] "${view.text}" | class: ${view.class}`)
    })

    console.log(`\n\n🌐 Shadow DOM 元素: ${analysis.shadowDoms.length} 个`)

    // 尝试最后一次点击
    console.log(`\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`🖱️  尝试点击`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)

    const clickResults = await page.evaluate(() => {
      const results = []

      // 方法 1: 用 class
      let el1 = document.querySelector('.btns-consult')
      if (el1) {
        results.push('✓ .btns-consult 找到')
      }

      // 方法 2: 用文本
      let els = document.querySelectorAll('*')
      for (const el of els) {
        if (el.textContent.trim() === '咨询一下' && el.offsetParent !== null) {
          results.push('✓ 精确文本"咨询一下"找到')
          break
        }
      }

      // 方法 3: 包含咨询的最小元素
      let minEl = null
      let minLength = Infinity
      for (const el of els) {
        const text = el.textContent.trim()
        if (text.includes('咨询') && text.length > 0 && text.length < minLength && el.offsetParent !== null) {
          minEl = el
          minLength = text.length
        }
      }
      if (minEl) {
        results.push(`✓ 最小包含元素找到: "${minEl.textContent.trim()}"`)
      }

      return results
    })

    clickResults.forEach(r => console.log(r))

    console.log(`\n\n浏览器保持打开 60 秒，你可以手动检查页面...`)
    await page.waitForTimeout(60000)

  } catch (err) {
    console.error('❌ 错误:', err.message)
    console.error(err.stack)
  } finally {
    if (browser) await browser.close()
  }
}

deepInspect()
