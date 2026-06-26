/**
 * 检查日期选择弹窗 + 备注输入框结构
 */
const playwright = require('playwright')
const FORM_URL = 'https://i.beautsgo.com/subPackages_sub/googlemapmake/googlemapmake?type=1&id=250'

async function main() {
  const browser = await playwright.chromium.launch({
    headless: false,
    args: ['--disable-features=ExternalProtocolDialog', '--disable-external-intent-requests']
  })
  const ctx = await browser.newContext({ bypassCSP: true })
  const page = await ctx.newPage()
  await page.route('**/*', async (route) => {
    const url = route.request().url()
    if (!url.startsWith('http://') && !url.startsWith('https://')) { await route.abort() }
    else { await route.continue() }
  })
  await page.goto(FORM_URL, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {})
  await page.waitForTimeout(8000)

  // 先看备注输入区域（HTML 后半部分）
  const html2 = await page.evaluate(() => document.body.innerHTML.substring(5000, 12000))
  console.log('HTML 5000-12000:')
  console.log(html2)

  // 点击时间行，触发日期弹窗
  console.log('\n--- 点击时间行 ---')
  await page.evaluate(() => {
    const rows = document.querySelectorAll('.flex.info.add')
    for (const row of rows) {
      if (row.textContent?.includes('选择预约时间')) {
        row.click()
        break
      }
    }
  })
  await page.waitForTimeout(3000)

  // 检查日期弹窗
  const calendarInfo = await page.evaluate(() => {
    const res = {}
    // 查找日历相关元素
    res.calendarEls = []
    document.querySelectorAll('*').forEach(el => {
      const cls = el.className || ''
      if (cls.includes('calendar') || cls.includes('date') || cls.includes('picker') || cls.includes('popup')) {
        const t = el.textContent?.trim()
        if (t && t.length < 100) {
          res.calendarEls.push({ tag: el.tagName, class: cls.substring(0, 80), text: t.substring(0, 50) })
        }
      }
    })

    // 查找"下一步"按钮
    res.nextBtn = []
    document.querySelectorAll('*').forEach(el => {
      const t = el.textContent?.trim()
      if (t && (t === '下一步' || t === '确定' || t === '完成')) {
        res.nextBtn.push({ tag: el.tagName, class: (el.className || '').substring(0, 80), text: t, visible: el.offsetParent !== null })
      }
    })

    // 查找日期数字（可点击的日期格子）
    res.dateNums = []
    document.querySelectorAll('*').forEach(el => {
      const cls = el.className || ''
      if ((cls.includes('day') || cls.includes('date')) && el.offsetParent !== null) {
        const t = el.textContent?.trim()
        if (t && /^\d{1,2}$/.test(t)) {
          res.dateNums.push({ tag: el.tagName, class: cls.substring(0, 60), text: t })
        }
      }
    })

    // 完整 HTML（弹窗部分）
    res.popupHtml = document.body.innerHTML.substring(12000, 18000)

    return res
  })

  console.log('\n日历相关元素:')
  console.log(JSON.stringify(calendarInfo.calendarEls, null, 2))

  console.log('\n下一步/确定按钮:')
  console.log(JSON.stringify(calendarInfo.nextBtn, null, 2))

  console.log('\n日期格子样例 (前10个):')
  console.log(JSON.stringify(calendarInfo.dateNums.slice(0, 10), null, 2))

  console.log('\nHTML 12000-18000:')
  console.log(calendarInfo.popupHtml)

  await browser.close()
}

main().catch(console.error)
