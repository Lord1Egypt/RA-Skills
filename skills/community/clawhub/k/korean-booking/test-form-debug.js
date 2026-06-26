#!/usr/bin/env node
/**
 * 调试脚本：截图分析预约表单的日历 DOM 结构
 */
const { createAuthorizedPage } = require('./api/browser/consult')
const path = require('path')
const fs = require('fs')

async function debug() {
  const url = process.argv[2] || 'https://i.beautsgo.com/cn/hospital/imageup-clinic/skill'
  console.log('🔍 Opening:', url)

  const { browser, page } = await createAuthorizedPage(url)

  try {
    console.log('⏳ Waiting for form to load...')
    await page.waitForSelector('.sub-right, .u-number-box__plus', { timeout: 20000 }).catch(() => {})
    await page.waitForTimeout(3000)

    // 截图1: 初始状态
    await page.screenshot({ path: '/tmp/form-step1-initial.png', fullPage: true })
    console.log('📸 Screenshot 1 saved: /tmp/form-step1-initial.png')

    // 输出时间行的 HTML
    const timeRowHtml = await page.evaluate(() => {
      const rows = document.querySelectorAll('.flex.info, .flex.info.add, [class*="time"], [class*="date"]')
      return Array.from(rows).slice(0, 10).map(el => ({
        class: el.className,
        text: el.textContent?.trim().slice(0, 50),
        html: el.outerHTML.slice(0, 200)
      }))
    })
    console.log('\n📋 Time-related rows:')
    console.log(JSON.stringify(timeRowHtml, null, 2))

    // 点击时间选择行
    console.log('\n📅 Clicking time selector...')
    const clicked = await page.evaluate(() => {
      // 尝试所有可能包含"时间"的行
      const candidates = [
        ...document.querySelectorAll('.flex.info.add'),
        ...document.querySelectorAll('.flex.info'),
        ...document.querySelectorAll('[class*="time"]'),
      ]
      for (const el of candidates) {
        const text = el.textContent || ''
        if (text.includes('选择') || text.includes('时间') || text.includes('预约')) {
          console.log('Clicking:', el.className, text.trim().slice(0, 30))
          el.click()
          return el.className
        }
      }
      return null
    })
    console.log('Clicked element:', clicked)

    await page.waitForTimeout(3000)

    // 截图2: 点击时间后
    await page.screenshot({ path: '/tmp/form-step2-after-time-click.png', fullPage: true })
    console.log('📸 Screenshot 2 saved: /tmp/form-step2-after-time-click.png')

    // 分析弹出层内容
    const popupHtml = await page.evaluate(() => {
      const popups = document.querySelectorAll('.u-popup, [class*="popup"], [class*="calendar"], [class*="picker"]')
      return Array.from(popups).filter(el => el.offsetParent !== null).map(el => ({
        class: el.className,
        visible: el.offsetParent !== null,
        html: el.innerHTML.slice(0, 1000)
      }))
    })
    console.log('\n📋 Visible popups after click:')
    console.log(JSON.stringify(popupHtml.slice(0, 3), null, 2))

    // 找所有数字格子
    const numbers = await page.evaluate(() => {
      const results = []
      for (const el of document.querySelectorAll('*')) {
        const text = (el.textContent || '').trim()
        if (/^\d{1,2}$/.test(text) && el.offsetParent !== null) {
          results.push({
            tag: el.tagName,
            class: el.className,
            text,
            parentClass: el.parentElement?.className
          })
        }
      }
      return results.slice(0, 30)
    })
    console.log('\n📋 Visible number elements (potential date cells):')
    console.log(JSON.stringify(numbers, null, 2))

    console.log('\n✅ Debug complete. Check screenshots in /tmp/')
    console.log('  /tmp/form-step1-initial.png')
    console.log('  /tmp/form-step2-after-time-click.png')

    // 保持浏览器打开 30 秒供手动检查
    console.log('\n⏸  Browser will stay open for 30s for manual inspection...')
    await page.waitForTimeout(30000)

  } finally {
    await browser.close()
  }
}

debug().catch(console.error)
