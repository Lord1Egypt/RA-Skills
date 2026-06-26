/**
 * 诊断脚本：检查"预约面诊"按钮的实际渲染时机和 DOM 结构
 */
const playwright = require('playwright')

async function diagnose() {
  const url = 'https://i.beautsgo.com/cn/hospital/jdclinic?from=skill'
  console.log('[诊断] 启动浏览器...')

  const browser = await playwright.chromium.launch({
    headless: false,
    args: ['--disable-features=ExternalProtocolDialog', '--no-default-browser-check']
  })
  const context = await browser.newContext({ bypassCSP: true })
  const page = await context.newPage()

  await page.route('**/*', async (route) => {
    const reqUrl = route.request().url()
    if (!reqUrl.startsWith('http://') && !reqUrl.startsWith('https://')) {
      await route.abort()
    } else {
      await route.continue()
    }
  })

  console.log('[诊断] 打开页面...')
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {})

  // 每秒检查一次按钮，最多等 15 秒
  for (let i = 1; i <= 15; i++) {
    await page.waitForTimeout(1000)
    const result = await page.evaluate(() => {
      // 找所有包含"预约"的可见元素
      const found = []
      const allEls = document.querySelectorAll('*')
      for (const el of allEls) {
        const text = (el.textContent || '').trim()
        if (text.includes('预约') && el.offsetParent !== null && text.length < 20) {
          found.push({
            tag: el.tagName,
            class: el.className,
            text,
            visible: el.offsetParent !== null
          })
        }
      }
      // 检查 .btns-right
      const btnsRight = document.querySelectorAll('.btns-right')
      const btnsRightInfo = Array.from(btnsRight).map(el => ({
        class: el.className,
        text: (el.textContent || '').trim(),
        visible: el.offsetParent !== null
      }))
      return { found, btnsRightInfo }
    })

    console.log(`[诊断] ${i}秒后:`)
    console.log('  含"预约"的可见元素:', result.found.length, result.found.map(f => `"${f.text}"(${f.class})`).join(', '))
    console.log('  .btns-right 元素:', result.btnsRightInfo.length, result.btnsRightInfo.map(b => `"${b.text}" visible=${b.visible}`).join(', '))

    // 如果找到了，尝试点击并记录
    if (result.found.length > 0) {
      const clicked = await page.evaluate(() => {
        const allEls = document.querySelectorAll('*')
        for (const el of allEls) {
          const text = (el.textContent || '').trim()
          if ((text === '预约面诊' || text === '立即预约' || text === '预约') && el.offsetParent !== null) {
            el.click()
            return { success: true, text }
          }
        }
        // 降级：.btns-right 第一个可见
        const btn = document.querySelector('.btns-right')
        if (btn && btn.offsetParent !== null) {
          btn.click()
          return { success: true, text: btn.textContent.trim() }
        }
        return { success: false }
      })
      console.log(`[诊断] 点击结果:`, clicked)
      if (clicked.success) {
        await page.waitForTimeout(3000)
        console.log('[诊断] 点击后 URL:', page.url())
        break
      }
    }
  }

  console.log('[诊断] 完成，10秒后关闭...')
  await page.waitForTimeout(10000)
  await browser.close()
}

diagnose().catch(console.error)
