/**
 * 检查预约表单页面 DOM 结构
 * 目标：找到人数加减、时间选择、备注、条款复选框、去下单按钮的选择器
 */
const playwright = require('playwright')

const FORM_URL = 'https://i.beautsgo.com/subPackages_sub/googlemapmake/googlemapmake?type=1&id=250'

async function main() {
  const browser = await playwright.chromium.launch({
    headless: false,
    args: [
      '--disable-features=ExternalProtocolDialog',
      '--disable-external-intent-requests',
    ]
  })

  const context = await browser.newContext({ bypassCSP: true })
  const page = await context.newPage()

  await page.route('**/*', async (route) => {
    const url = route.request().url()
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      await route.abort()
    } else {
      await route.continue()
    }
  })

  console.log('打开表单页面...')
  await page.goto(FORM_URL, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {})
  await page.waitForTimeout(8000)

  console.log('\n========== 表单元素分析 ==========\n')

  const info = await page.evaluate(() => {
    const result = {}

    // 1. 查找所有包含"人数"的元素
    result.personElements = []
    document.querySelectorAll('*').forEach(el => {
      const t = el.textContent?.trim()
      if (t && t.includes('人数') && t.length < 50) {
        result.personElements.push({
          tag: el.tagName,
          class: el.className,
          text: t
        })
      }
    })

    // 2. 查找加减按钮
    result.plusMinus = []
    document.querySelectorAll('*').forEach(el => {
      const t = el.textContent?.trim()
      if (t === '+' || t === '-' || t === '＋' || t === '－') {
        result.plusMinus.push({
          tag: el.tagName,
          class: el.className,
          text: t,
          visible: el.offsetParent !== null
        })
      }
    })

    // 3. 查找时间/日期相关
    result.timeElements = []
    document.querySelectorAll('*').forEach(el => {
      const t = el.textContent?.trim()
      if (t && (t.includes('预约时间') || t.includes('选择时间') || t.includes('日期')) && t.length < 50) {
        result.timeElements.push({
          tag: el.tagName,
          class: el.className,
          text: t
        })
      }
    })

    // 4. 查找 input/textarea
    result.inputs = []
    document.querySelectorAll('input, textarea').forEach(el => {
      result.inputs.push({
        tag: el.tagName,
        type: el.type,
        placeholder: el.placeholder,
        class: el.className,
        name: el.name
      })
    })

    // 5. 查找条款复选框
    result.checkboxes = []
    document.querySelectorAll('*').forEach(el => {
      const t = el.textContent?.trim()
      if (t && (t.includes('条款') || t.includes('已阅读') || t.includes('同意')) && t.length < 80) {
        result.checkboxes.push({
          tag: el.tagName,
          class: el.className,
          text: t.substring(0, 60)
        })
      }
    })

    // 6. 查找"去下单"按钮
    result.submitBtn = []
    document.querySelectorAll('*').forEach(el => {
      const t = el.textContent?.trim()
      if (t && (t.includes('去下单') || t.includes('提交') || t.includes('确认预约')) && t.length < 30) {
        result.submitBtn.push({
          tag: el.tagName,
          class: el.className,
          text: t,
          visible: el.offsetParent !== null
        })
      }
    })

    // 7. 输出完整 body HTML（截取前 5000 字符）
    result.bodyHtml = document.body.innerHTML.substring(0, 5000)

    return result
  })

  console.log('人数相关元素:')
  console.log(JSON.stringify(info.personElements, null, 2))

  console.log('\n加减按钮:')
  console.log(JSON.stringify(info.plusMinus, null, 2))

  console.log('\n时间相关元素:')
  console.log(JSON.stringify(info.timeElements, null, 2))

  console.log('\ninput/textarea:')
  console.log(JSON.stringify(info.inputs, null, 2))

  console.log('\n条款复选框:')
  console.log(JSON.stringify(info.checkboxes, null, 2))

  console.log('\n去下单按钮:')
  console.log(JSON.stringify(info.submitBtn, null, 2))

  console.log('\n页面 HTML (前5000):')
  console.log(info.bodyHtml)

  console.log('\n等待 10 秒供手动查看...')
  await page.waitForTimeout(10000)

  await browser.close()
}

main().catch(console.error)
