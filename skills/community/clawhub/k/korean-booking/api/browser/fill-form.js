#!/usr/bin/env node
/**
 * fill-form.js — 打开预约表单页并自动填写提交
 *
 * 用法（命令行）：
 *   node api/browser/fill-form.js <booking_url> <persons> <dateText> [contact] [timeSlot]
 *
 *   booking_url — 预约表单页 URL
 *   persons     — 预约人数（数字）
 *   dateText    — 预约日期文本，例如 "3月26日"
 *   contact     — 联系方式（可选）
 *   timeSlot    — 时间段：全天/上午/下午（可选，默认全天）
 *
 * 作为模块调用时返回：
 *   { success: true }                          — 全部完成
 *   { success: false, step, message }          — 某步失败
 */

const { createAuthorizedPage } = require('./consult')

/**
 * @returns {Promise<{ success: boolean, step?: string, message?: string }>}
 */
async function fillForm(bookingUrl, persons, dateText, contact, timeSlot) {
  let browser
  try {
    const result = await createAuthorizedPage(bookingUrl)
    browser = result.browser
    const page = result.page

    console.log('⏳ Waiting for booking form...')
    await page.waitForSelector('.u-number-box__plus, .sub-right', { timeout: 15000 }).catch(() => {})
    await page.waitForTimeout(2000)

    // ── 1. 填写人数 ────────────────────────────────────────
    if (persons && persons > 1) {
      console.log(`👥 Setting persons: ${persons}`)
      await page.evaluate((n) => {
        const input = document.querySelector('.u-number-box__input input, input.uni-input-input[type="number"]')
        if (input) {
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set
          setter.call(input, n)
          input.dispatchEvent(new Event('input', { bubbles: true }))
          input.dispatchEvent(new Event('change', { bubbles: true }))
        }
      }, persons)

      const current = await page.evaluate(() => {
        const input = document.querySelector('input.uni-input-input[type="number"]')
        return input ? parseInt(input.value, 10) : 1
      })
      const clicks = persons - (current || 1)
      for (let i = 0; i < clicks; i++) {
        await page.evaluate(() => {
          const btn = document.querySelector('.u-number-box__plus')
          if (btn) btn.click()
        })
        await page.waitForTimeout(300)
      }
    }

    // ── 2. 选择预约时间 ────────────────────────────────────
    if (dateText) {
      console.log(`📅 Selecting date: ${dateText}`)
      // 点击"选择预约时间"行，打开日历
      await page.evaluate(() => {
        for (const row of document.querySelectorAll('.flex.info.add')) {
          if (row.textContent?.includes('选择预约时间')) { row.click(); return }
        }
      })
      await page.waitForTimeout(2000)

      // 等待日历弹窗真正出现
      await page.waitForSelector('.u-calendar, .u-popup', { timeout: 8000 }).catch(() => {})
      await page.waitForTimeout(500)

      const dayMatch = dateText.match(/(\d{1,2})[日号]$/) || dateText.match(/[月\/\-](\d{1,2})/)
      const targetDay = dayMatch ? parseInt(dayMatch[1], 10) : null

      if (!targetDay) {
        await browser.close()
        return { success: false, step: 'date_parse', message: `无法从"${dateText}"解析出日期数字` }
      }

      // 2a. 点击日期格子
      const dateClicked = await page.evaluate((day) => {
        // 优先：在 .u-calendar 内找 SPAN 文本匹配的日期格子
        const calendar = document.querySelector('.u-calendar')
        if (calendar && calendar.offsetParent !== null) {
          for (const span of calendar.querySelectorAll('span')) {
            if ((span.textContent || '').trim() === String(day) && span.offsetParent !== null) {
              span.click(); return true
            }
          }
        }
        // 降级：在所有可见 .u-popup 内找
        for (const popup of document.querySelectorAll('.u-popup')) {
          if (popup.offsetParent !== null) {
            for (const el of popup.querySelectorAll('*')) {
              if ((el.textContent || '').trim() === String(day) && el.offsetParent !== null) {
                el.click(); return true
              }
            }
          }
        }
        return false
      }, targetDay)

      console.log(`📅 Date ${targetDay} clicked: ${dateClicked}`)

      // ⚠️ 日期选择失败 → 提前返回错误，不继续走后面步骤
      if (!dateClicked) {
        await browser.close()
        return { success: false, step: 'date_click', message: `日历中未找到 ${targetDay} 号，可能该日期不可预约或日历尚未加载` }
      }

      await page.waitForTimeout(1500)

      // 2b. 点"下一步"
      const nextClicked = await page.evaluate(() => {
        // 优先：u-calendar__confirm 按钮
        const confirm = document.querySelector('.u-calendar__confirm')
        if (confirm && confirm.offsetParent !== null) { confirm.click(); return true }
        // 降级：文本匹配
        for (const el of document.querySelectorAll('*')) {
          const text = (el.textContent || '').trim()
          if ((text === '下一步' || text === '确定' || text === '完成') && el.offsetParent !== null) {
            el.click(); return true
          }
        }
        return false
      })
      console.log(`⏭️  Next button clicked: ${nextClicked}`)

      if (!nextClicked) {
        await browser.close()
        return { success: false, step: 'date_next', message: '日历"下一步"按钮未找到' }
      }

      await page.waitForTimeout(1500)

      // 2c. 选择时间段（全天/上午/下午）
      const slotMap = {
        '上午': ['上午', 'AM', 'morning'],
        '下午': ['下午', 'PM', 'afternoon'],
        '全天': ['全天', '不限', 'all day']
      }
      const preferredSlot = timeSlot || '全天'
      const slotKeywords = slotMap[preferredSlot] || slotMap['全天']

      console.log(`🕐 Selecting time slot: ${preferredSlot}`)
      const slotClicked = await page.evaluate((keywords) => {
        for (const kw of keywords) {
          for (const el of document.querySelectorAll('*')) {
            if ((el.textContent || '').trim() === kw && el.offsetParent !== null) {
              el.click(); return kw
            }
          }
        }
        return null
      }, slotKeywords)
      console.log(`🕐 Time slot clicked: ${slotClicked}`)
      await page.waitForTimeout(1000)

      // 2d. 点"确认"关闭时间段弹窗
      const timeConfirmed = await page.evaluate(() => {
        for (const el of document.querySelectorAll('*')) {
          const text = (el.textContent || '').trim()
          if (text === '确认' && el.offsetParent !== null) { el.click(); return true }
        }
        return false
      })
      console.log(`✅ Time confirm clicked: ${timeConfirmed}`)
      await page.waitForTimeout(1000)
    }

    // ── 3. 填写联系方式 ────────────────────────────────────
    if (contact && contact.length > 0) {
      console.log(`📞 Filling contact: ${contact}`)
      await page.evaluate((c) => {
        const inputs = document.querySelectorAll('input.uni-input-input[type="text"], input[type="text"]')
        for (const input of inputs) {
          if (input.offsetParent !== null) {
            const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set
            setter.call(input, c)
            input.dispatchEvent(new Event('input', { bubbles: true }))
            return true
          }
        }
        return false
      }, contact)
      await page.waitForTimeout(500)
    }

    // ── 4. 勾选服务条款 ────────────────────────────────────
    console.log('☑️  Accepting terms...')
    await page.evaluate(() => {
      const termsEl = document.querySelector('.text')
      if (termsEl) {
        const img = termsEl.querySelector('img, uni-image')
        if (img) { img.click(); return }
        termsEl.click()
      }
    })
    await page.waitForTimeout(500)

    // ── 5. 点击"去付款/去下单" ──────────────────────────────
    console.log('💳 Clicking submit...')
    const submitted = await page.evaluate(() => {
      const btn = document.querySelector('.sub-right')
      if (btn && btn.offsetParent !== null) { btn.click(); return true }
      for (const el of document.querySelectorAll('*')) {
        const text = (el.textContent || '').trim()
        if ((text === '去付款' || text === '去下单' || text === '提交预约') && el.offsetParent !== null) {
          el.click(); return true
        }
      }
      return false
    })

    if (submitted) {
      console.log('✅ Form submitted')
      await page.waitForTimeout(3000)
      return { success: true }
    } else {
      return { success: false, step: 'submit', message: '未找到提交按钮（去付款/去下单）' }
    }

  } catch (err) {
    console.error(`❌ Error: ${err.message}`)
    if (browser) await browser.close().catch(() => {})
    return { success: false, step: 'exception', message: err.message }
  }
}

// 命令行入口：处理退出码
if (require.main === module) {
  const [,, bookingUrl, persons, dateText, contact, timeSlot] = process.argv
  if (!bookingUrl || !dateText) {
    console.error('❌ Usage: node fill-form.js <booking_url> <persons> <dateText> [contact] [timeSlot]')
    process.exit(1)
  }
  fillForm(bookingUrl, parseInt(persons) || 1, dateText, contact || '', timeSlot || '').then(res => {
    if (res.success) {
      process.exit(0)
    } else {
      console.error(`❌ [${res.step}] ${res.message}`)
      process.exit(res.step === 'exception' ? 1 : 2)
    }
  })
}

module.exports = { fillForm }
