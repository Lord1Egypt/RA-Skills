const playwright = require('playwright')

async function inspectDOM() {
  let browser
  try {
    browser = await playwright.chromium.launch({ headless: false })
    const context = await browser.newContext()
    const page = await context.newPage()
    
    // 打开页面
    const url = 'https://i.beautsgo.com/cn/hospital/jdclinic?from=google_map'
    console.log(`🌐 打开页面: ${url}`)
    
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 })
    } catch (e) {
      console.log(`⚠️ 页面加载超时: ${e.message}`)
    }
    
    await page.waitForTimeout(3000)
    
    console.log('✅ 页面已加载\n')
    
    // 获取整个 HTML（仅前 3000 个字符）
    const html = await page.content()
    console.log('📄 页面 HTML 前 3000 字符:')
    console.log(html.substring(0, 3000))
    console.log('\n...[截断]\n')
    
    // 查找所有包含"咨询"的文本节点
    console.log('🔍 查找所有包含"咨询"的元素:')
    const result = await page.evaluate(() => {
      const elements = []
      const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_ELEMENT,
        null
      )
      
      let node
      while (node = walker.nextNode()) {
        const text = node.textContent || ''
        if (text.includes('咨询') && text.length < 50) {
          elements.push({
            tag: node.tagName,
            class: node.className,
            id: node.id,
            text: text.trim().substring(0, 30),
            visible: node.offsetParent !== null
          })
        }
      }
      return elements
    })
    
    console.log(`找到 ${result.length} 个元素`)
    result.slice(0, 10).forEach((el, i) => {
      console.log(`  [${i}] <${el.tag} class="${el.class}" id="${el.id}"> "${el.text}" (visible: ${el.visible})`)
    })
    
    console.log('\n✅ 完成。浏览器窗口将在 20 秒后关闭。')
    await page.waitForTimeout(20000)
  } catch (err) {
    console.error('❌ 错误:', err.message)
  } finally {
    if (browser) await browser.close()
  }
}

inspectDOM()
