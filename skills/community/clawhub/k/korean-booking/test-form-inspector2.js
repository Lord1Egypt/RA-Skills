/**
 * 深度检查表单交互流程
 * 重点：加号按钮、时间选择器交互、条款勾选
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
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      await route.abort()
    } else { await route.continue() }
  })

  await page.goto(FORM_URL, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {})
  await page.waitForTimeout(8000)

  const info = await page.evaluate(() => {
    const res = {}

    // 1. 找加号按钮（+ 按钮）
    res.plusBtn = []
    document.querySelectorAll('*').forEach(el => {
      const cls = el.className || ''
      if (cls.includes('plus') || cls.includes('add') || cls.includes('increase')) {
        res.plusBtn.push({ tag: el.tagName, class: cls.substring(0, 80), text: el.textContent?.trim().substring(0, 20) })
      }
    })

    // 2. number-box 完整结构
    const nb = document.querySelector('.u-number-box')
    if (nb) {
      res.numberBox = nb.innerHTML.substring(0, 2000)
    }

    // 3. 时间行的可点击元素
    res.timeRow = []
    document.querySelectorAll('.info.add, .info').forEach(el => {
      const t = el.textContent?.trim()
      if (t && (t.includes('时间') || t.includes('日期'))) {
        res.timeRow.push({
          tag: el.tagName,
          class: el.className?.substring(0, 80),
          text: t.substring(0, 50),
          children: el.children.length
        })
      }
    })

    // 4. 条款勾选区域
    const terms = document.querySelector('.text')
    if (terms) {
      res.termsHtml = terms.outerHTML.substring(0, 500)
    }

    // 5. 备注输入框（textarea / contenteditable）
    res.remarkArea = []
    document.querySelectorAll('textarea, [contenteditable]').forEach(el => {
      res.remarkArea.push({
        tag: el.tagName,
        class: el.className,
        placeholder: el.placeholder || el.getAttribute('placeholder') || ''
      })
    })

    // 6. 找所有 uni-input（可能的备注输入）
    res.uniInputs = []
    document.querySelectorAll('uni-input, uni-textarea').forEach(el => {
      res.uniInputs.push({
        tag: el.tagName,
        class: el.className,
        text: el.textContent?.trim().substring(0, 30)
      })
    })

    // 7. 更多 HTML（5001~10000）
    res.bodyHtml2 = document.body.innerHTML.substring(5000, 10000)

    return res
  })

  console.log('加号按钮:')
  console.log(JSON.stringify(info.plusBtn, null, 2))

  console.log('\nnumber-box HTML:')
  console.log(info.numberBox)

  console.log('\n时间行:')
  console.log(JSON.stringify(info.timeRow, null, 2))

  console.log('\n条款区域 HTML:')
  console.log(info.termsHtml)

  console.log('\n备注 textarea:')
  console.log(JSON.stringify(info.remarkArea, null, 2))

  console.log('\nuni-input/textarea:')
  console.log(JSON.stringify(info.uniInputs, null, 2))

  console.log('\nHTML 5000-10000:')
  console.log(info.bodyHtml2)

  await browser.close()
}

main().catch(console.error)
