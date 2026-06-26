/**
 * 检查页面 HTML 结构
 * 找出实际的按钮文字和选择器
 */
const playwright = require('playwright')
const hospitals = require('./data/hospitals.json')

async function inspectPageHTML() {
  const jdHospital = hospitals.find(h => h.name.includes('JD') || h.name.includes('皮肤科'))
  if (!jdHospital) {
    console.error('❌ 找不到 JD 皮肤科医院')
    return
  }

  const url = jdHospital.url
  console.log(`\n🔍 检查页面：${jdHospital.name}`)
  console.log(`📍 URL: ${url}\n`)

  let browser
  try {
    browser = await playwright.chromium.launch({ headless: false })
    const context = await browser.newContext()
    const page = await context.newPage()

    console.log(`⏳ 正在加载页面...`)
    await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 }).catch(() => {})
    
    console.log(`⏳ 等待 5 秒...`)
    await page.waitForTimeout(5000)

    // 获取页面的完整 HTML
    const html = await page.content()
    
    // 保存到文件，方便查看
    const fs = require('fs')
    fs.writeFileSync('/Users/wangning/project/company/korean-aesthetic-booking-guide/page-snapshot.html', html)
    console.log(`✅ 页面 HTML 已保存到 page-snapshot.html\n`)

    // 分析页面结构
    const analysis = await page.evaluate(() => {
      const results = {
        pageTitle: document.title,
        buttons: [],
        divs: [],
        allClickable: [],
        bodyHTML: document.body ? document.body.innerHTML.substring(0, 2000) : '无 body',
      }

      // 查找所有 button
      const buttons = document.querySelectorAll('button')
      buttons.forEach((btn, idx) => {
        results.buttons.push({
          idx,
          text: btn.textContent.trim().substring(0, 50),
          className: btn.className,
          id: btn.id,
          html: btn.outerHTML.substring(0, 100),
        })
      })

      // 查找所有可点击的元素
      const clickables = document.querySelectorAll('[onclick], [role="button"], .btn, [class*="button"]')
      clickables.forEach((el, idx) => {
        if (idx < 20) { // 限制数量
          results.allClickable.push({
            tag: el.tagName,
            text: el.textContent.trim().substring(0, 30),
            className: el.className,
            onclick: el.onclick ? 'yes' : 'no',
          })
        }
      })

      // 查找所有含有"预约"的元素
      const allElements = document.querySelectorAll('*')
      let bookingElements = []
      for (const el of allElements) {
        const text = el.textContent.trim()
        if ((text.includes('预约') || text.includes('咨询') || text.includes('客服')) && text.length < 100) {
          bookingElements.push({
            tag: el.tagName,
            text: text.substring(0, 50),
            className: el.className,
          })
        }
      }

      results.bookingElements = bookingElements.slice(0, 20)

      return results
    })

    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`📄 页面标题: ${analysis.pageTitle}`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)

    console.log(`🔘 找到 ${analysis.buttons.length} 个 <button> 元素：\n`)
    analysis.buttons.forEach(btn => {
      console.log(`  [${btn.idx}] "${btn.text}"`)
      console.log(`      Class: ${btn.className || '(无)'}`)
      console.log(`      ID: ${btn.id || '(无)'}`)
      console.log()
    })

    console.log(`\n🎯 所有包含"预约/咨询/客服"的元素 (前20个)：\n`)
    analysis.bookingElements.forEach((el, idx) => {
      console.log(`  [${idx}] <${el.tag}> "${el.text}"`)
      console.log(`       Class: ${el.className}`)
      console.log()
    })

    console.log(`\n⚙️  所有可点击元素 (前20个)：\n`)
    analysis.allClickable.forEach((el, idx) => {
      console.log(`  [${idx}] <${el.tag}> "${el.text}"`)
      console.log(`       Class: ${el.className}`)
      console.log()
    })

    console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`📋 分析完成！`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`\n浏览器保持打开 30 秒，你可以用 F12 查看实际页面...`)

    await page.waitForTimeout(30000)

  } catch (err) {
    console.error('❌ 检查失败:', err.message)
  } finally {
    if (browser) {
      await browser.close()
    }
  }
}

inspectPageHTML()
