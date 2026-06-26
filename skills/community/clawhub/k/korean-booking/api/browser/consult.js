#!/usr/bin/env node
/**
 * consult.js — 打开医院页面并自动点击"咨询一下"按钮
 *
 * 用法：
 *   node api/browser/consult.js <url>
 *
 * 退出码：
 *   0 — 成功点击
 *   2 — 页面已打开但按钮未找到（用户可手动操作）
 *   1 — 启动失败
 */

const playwright = require('playwright')

async function createAuthorizedPage(url) {
  const browser = await playwright.chromium.launch({
    headless: false,
    args: [
      '--disable-external-intent-requests',
      '--disable-features=ExternalProtocolDialog',
      '--no-default-browser-check',
      // 禁用 Web 安全策略，解决 CORS + 私有网络访问限制（api.yestokr.com 被拦截导致白屏）
      '--disable-web-security',
      '--disable-features=BlockInsecurePrivateNetworkRequests,PrivateNetworkAccessSendPreflights',
      '--allow-running-insecure-content',
      '--no-sandbox',
    ]
  })

  // uni-app 需要手机 UA 才能正常渲染
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    permissions: ['geolocation', 'notifications', 'clipboard-read', 'clipboard-write'],
    bypassCSP: true,
  })

  context.on('page', page => {
    page.on('dialog', async dialog => {
      await dialog.accept().catch(() => dialog.dismiss().catch(() => {}))
    })
  })

  const page = await context.newPage()

  await page.route('**/*', async (route) => {
    const reqUrl = route.request().url()
    if (!reqUrl.startsWith('http://') && !reqUrl.startsWith('https://')) {
      await route.abort()
    } else {
      await route.continue()
    }
  })

  page.on('dialog', async dialog => {
    await dialog.accept().catch(() => dialog.dismiss().catch(() => {}))
  })

  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {
    console.warn('⚠️  networkidle timeout, continuing anyway')
  })

  return { browser, page }
}

async function clickConsult(url) {
  let browser
  try {
    const result = await createAuthorizedPage(url)
    browser = result.browser
    const page = result.page

    console.log('⏳ Waiting for Vue components to render...')
    await page.waitForTimeout(8000)
    await page.waitForSelector('.btns-consult', { timeout: 10000 }).catch(() => {})

    const clicked = await page.evaluate(() => {
      // 方法1: class 精确定位
      let btn = document.querySelector('.btns-consult')
      if (btn) { btn.click(); return true }

      // 方法2: 精确文本"咨询一下"
      for (const el of document.querySelectorAll('*')) {
        const text = (el.textContent || '').trim()
        if (text === '咨询一下' && el.offsetParent !== null) {
          el.click(); return true
        }
      }

      // 方法3: 最小可见含"咨询"元素
      let target = null, minLen = Infinity
      for (const el of document.querySelectorAll('*')) {
        const text = (el.textContent || '').trim()
        if (text.includes('咨询') && el.offsetParent !== null && text.length < 100) {
          if (text.length < minLen) { minLen = text.length; target = el }
        }
      }
      if (target) { target.click(); return true }

      return false
    })

    if (clicked) {
      console.log('✅ Consult button clicked')
      await page.waitForTimeout(3000)
      process.exit(0)
    }

    // Playwright fallback
    for (const selector of ['text=/咨询一下/', '[class*="consult"]', 'text=/咨询/']) {
      try {
        const locator = page.locator(selector).first()
        if (await locator.count() > 0 && await locator.isVisible().catch(() => false)) {
          await locator.click()
          console.log(`✅ Clicked via fallback: ${selector}`)
          await page.waitForTimeout(2000)
          process.exit(0)
        }
      } catch (e) { /* continue */ }
    }

    console.warn('⚠️  Consult button not found, page is open for manual operation')
    process.exit(2)

  } catch (err) {
    console.error(`❌ Error: ${err.message}`)
    if (browser) await browser.close()
    process.exit(1)
  }
}

if (require.main === module) {
  const url = process.argv[2]
  if (!url) { console.error('❌ URL is required'); process.exit(1) }
  clickConsult(url)
}

module.exports = { clickConsult, createAuthorizedPage }
