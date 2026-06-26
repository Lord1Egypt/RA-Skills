const { chromium } = require('playwright')

async function inspectForm() {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()
  
  await page.goto('https://i.beautsgo.com/cn/hospital/jd-clinic/skill', { waitUntil: 'networkidle' })
  await page.waitForTimeout(5000)
  
  const fields = await page.evaluate(() => {
    const results = []
    
    // 所有 input
    document.querySelectorAll('input').forEach(el => {
      results.push({ tag: 'input', type: el.type, placeholder: el.placeholder, class: el.className, value: el.value })
    })
    
    // 所有 textarea
    document.querySelectorAll('textarea').forEach(el => {
      results.push({ tag: 'textarea', placeholder: el.placeholder, class: el.className })
    })
    
    // 所有可见的 label / 字段标签
    document.querySelectorAll('.form-item, .field, .label, uni-view[class*="label"], uni-view[class*="title"]').forEach(el => {
      const text = el.textContent.trim()
      if (text && text.length < 20) {
        results.push({ tag: 'label', text, class: el.className })
      }
    })
    
    // 找包含"联系"、"电话"、"手机"文字的元素
    document.querySelectorAll('*').forEach(el => {
      const text = (el.textContent || '').trim()
      if ((text.includes('联系') || text.includes('电话') || text.includes('手机') || text.includes('姓名') || text.includes('名字')) && text.length < 30 && el.children.length === 0) {
        results.push({ tag: 'label-match', text, class: el.className })
      }
    })
    
    return results
  })
  
  console.log('=== 表单字段 ===')
  fields.forEach(f => console.log(JSON.stringify(f)))
  
  await browser.close()
}

inspectForm().catch(console.error)
