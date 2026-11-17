/**
 * JD皮肤科预约技能 — 主入口
 *
 * 处理流程：
 *   view     → 显示预约指南（首次访问）
 *   open     → 打开医院详情页
 *   book     → 收集信息 → 提交预约 API
 *   consult  → 打开在线客服页
 *   price    → API 查价格 / 打开价格表页
 *   download → APP 下载链接
 */

const hospital = require('../data/hospital.json')
const { getBookingGuide } = require('../core/service')
const { detectIntent, parseFormInput, extractProjectKeyword } = require('../core/preprocessor')
const { openUrl } = require('./browser/open-url')
const https = require('https')

// ── 预约接口配置 ─────────────────────────────────────────────────────────────

const BOOKING_API_URL = 'https://api.yestokr.com/api/Appointment/saveFromSkill'
const BOOKING_API_TOKEN = 'beautsgo-openapi-fixed-token-change-me'

const PRICE_API_URL = 'https://apis.beise.com:50144/c5d1dcbc/ProjectDraft/search'
const PRICE_API_TOKEN = '275aed9b-7c41-4a88-b291-20c0df803148'

// ── URL 辅助 ─────────────────────────────────────────────────────────────────

function getChatUrl(h) {
  return `https://i.beautsgo.com/cn/hospital/${h.chat_slug}-chat`
}

function getPriceUrl(h) {
  return `https://i.beautsgo.com/cn/hospital/${h.chat_slug}-price`
}

// ── API 调用 ─────────────────────────────────────────────────────────────────

function submitBookingApi(payload) {
  return new Promise((resolve, reject) => {
    const url = new URL(BOOKING_API_URL)
    const body = JSON.stringify(payload)
    const options = {
      hostname: url.hostname,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Open-Token': BOOKING_API_TOKEN,
      },
    }
    const req = https.request(options, (res) => {
      let data = ''
      res.on('data', chunk => { data += chunk })
      res.on('end', () => {
        try { resolve(JSON.parse(data)) }
        catch (e) { reject(new Error(`Parse error: ${data.slice(0, 100)}`)) }
      })
    })
    req.on('error', reject)
    req.setTimeout(15000, () => { req.destroy(); reject(new Error('Booking API timeout')) })
    req.write(body)
    req.end()
  })
}

function queryProjectPrice(hId, keyword) {
  return new Promise((resolve, reject) => {
    const urlStr = `${PRICE_API_URL}?h_id=${hId}&keywords=${encodeURIComponent(keyword)}`
    const url = new URL(urlStr)
    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      port: url.port,
      method: 'GET',
      headers: { 'Authorization': PRICE_API_TOKEN },
    }
    const req = https.request(options, (res) => {
      let data = ''
      res.on('data', chunk => { data += chunk })
      res.on('end', () => {
        try { resolve(JSON.parse(data)) }
        catch (e) { reject(new Error(`Parse error: ${data.slice(0, 100)}`)) }
      })
    })
    req.on('error', reject)
    req.setTimeout(10000, () => { req.destroy(); reject(new Error('Price API timeout')) })
    req.end()
  })
}

// ── 日期解析 ─────────────────────────────────────────────────────────────────

function parseDateToISO(dateText) {
  const now = new Date()
  let year = now.getFullYear()
  const match = dateText.match(/(\d{1,2})月(\d{1,2})日/)
  if (match) {
    const month = parseInt(match[1], 10)
    const day = parseInt(match[2], 10)
    // 如果月份小于当前月，可能是明年
    if (month < now.getMonth() + 1) year += 1
    return `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  }
  return dateText
}

// ── 主处理函数 ───────────────────────────────────────────────────────────────

async function processQuery(query, lang = 'zh', context = {}) {
  try {
    const intent = detectIntent(query, context)

    // 补全 context 中的医院信息（单医院技能自动填入）
    if (!context.resolvedHospital) {
      context.resolvedHospital = hospital
    }
    context.intent = intent

    // ─────────────────────────────────────────────────────────────────────────
    // view — 查看预约指南
    // ─────────────────────────────────────────────────────────────────────────
    if (intent === 'view') {
      const guide = await getBookingGuide(lang)

      return `${guide}

---

💡 **你可以对我说：**
• 「帮我预约」— 直接提交预约申请
• 「咨询客服」— 联系在线客服
• 「查价格」— 查看项目价格
• 「打开链接」— 打开医院详情页
• 「下载APP」— 获取 BeautsGO App 下载链接`
    }

    // ─────────────────────────────────────────────────────────────────────────
    // open — 打开医院详情页
    // ─────────────────────────────────────────────────────────────────────────
    if (intent === 'open') {
      const targetUrl = hospital.booking_url || hospital.url
      const opened = await openUrl(targetUrl).then(() => true).catch(() => false)

      if (opened) {
        return `✅ 已为你打开 **${hospital.name}** 的详情页面！

详情页：${targetUrl}

你可以直接在页面上：
• 📍 查看中韩文地址和交通路线
• ⏰ 查看营业时间
• 💰 查看最新价格表和优惠活动
• ⚡ 直接点击【立即预约】

还有其他需要吗？`
      }
      return `⚠️ 自动打开页面失败，请手动访问：\n\n${targetUrl}`
    }

    // ─────────────────────────────────────────────────────────────────────────
    // book — 提交预约
    // ─────────────────────────────────────────────────────────────────────────
    if (intent === 'book') {
      // 如果用户输入的是完整表单信息
      const formData = parseFormInput(query)

      // 如果是初次预约（还没有填写信息）
      if (!formData.dateText) {
        return `📋 **${hospital.name} — 预约申请**

请告诉我以下信息（一次或分次提供均可）：
• 📅 **预约日期**：例如「3月26日」、「明天」
• ⏰ **时间段**：上午 / 下午 / 晚上（可选）
• 👥 **人数**：默认 1 人
• 📞 **联系方式**：手机号（可选）

例如：「2人，3月26日下午，电话19102044571」

> 信息不全也没关系，分多次告诉我也可以 😊`
      }

      // 有完整信息 → 提交 API
      if (!hospital.id) {
        return `❌ 该医院暂不支持在线预约，请手动预约：${hospital.url || ''}`
      }

      const dateISO = parseDateToISO(formData.dateText)
      const expectedTime = formData.timeSlot && formData.timeSlot !== '全天'
        ? `${dateISO} ${formData.timeSlot}`
        : `${dateISO} 全天`

      const payload = {
        contact: formData.contact || '',
        expected_time: expectedTime,
        project_type: '',
        d_id: '',
        h_id: hospital.id,
        p_id: '',
        num: formData.persons,
        source_type: 'skill',
      }

      const result = await submitBookingApi(payload)

      if (result.code === 0) {
        return `✅ **预约已提交！**

📋 **预约信息摘要：**
• 🏥 机构：${hospital.name}
• 👥 人数：${formData.persons} 人
• 📅 时间：${expectedTime}${formData.contact ? `\n• 📞 联系方式：${formData.contact}` : ''}

🎉 提交成功！BeautsGO 平台会尽快联系机构为你匹配时间。

还有什么需要帮忙的吗？`
      }

      const errMsg = result.msg || result.message || JSON.stringify(result)
      return `❌ 预约提交失败：${errMsg}

你可以手动预约：
• 打开 BeautsGO App 搜索「${hospital.name}」
• 或说「打开链接」打开医院页面`
    }

    // ─────────────────────────────────────────────────────────────────────────
    // download — APP 下载链接
    // ─────────────────────────────────────────────────────────────────────────
    if (intent === 'download') {
      return `📲 **BeautsGO APP 下载**

🍎 **iOS（苹果）**
[App Store 下载](https://apps.apple.com/cn/app/beautsgo%E5%BD%BC%E6%AD%A4%E7%BE%8E-%E9%9F%A9%E5%9B%BD%E7%9A%AE%E8%82%A4%E7%A7%91%E9%A2%84%E7%BA%A6/id6741841509)

🤖 **Android（Google Play）**
[Google Play 下载](https://play.google.com/store/apps/details?id=uni.UNIEF980DB)

📦 **Android（国内 APK）**
[下载 APK](https://img.beautsgo.com/3.6.apk)

安装后搜索「${hospital.name}」即可预约 ✅`
    }

    // ─────────────────────────────────────────────────────────────────────────
    // price — 查价格
    // ─────────────────────────────────────────────────────────────────────────
    if (intent === 'price') {
      const projectKeyword = extractProjectKeyword(query, hospital)

      if (projectKeyword && hospital.id) {
        const priceResult = await queryProjectPrice(hospital.id, projectKeyword).catch(() => null)

        if (priceResult && priceResult.code === 0 && priceResult.data && priceResult.data.length > 0) {
          const items = priceResult.data.map(item => {
            const priceText = item.korean_won
              ? `💰 ${new Intl.NumberFormat().format(parseFloat(item.korean_won))}원`
              : ''
            const unitText = item.unit ? `（${item.unit}）` : ''
            return `• **${item.name}**${unitText}\n  ${priceText}`
          }).join('\n')

          return `🏥 **${hospital.name}** — **${projectKeyword}** 项目价格\n\n${items}\n\n---\n💡 说「查价格」查看全部价格表\n📖 说「打开链接」查看医院详情\n⚡ 说「帮我预约」直接提交`
        }
      }

      // 回退：打开价格表页面
      const priceUrl = getPriceUrl(hospital)
      const opened = await openUrl(priceUrl).then(() => true).catch(() => false)

      if (opened) {
        return `✅ 已为你打开 **${hospital.name}** 的价格表页面！

价格页面：${priceUrl}

💡 如果想查询具体项目价格，可以说「Onda 价格」
还需要预约或咨询吗？`
      }
      return `⚠️ 打开价格页面失败，请手动访问：\n\n${priceUrl}`
    }

    // ─────────────────────────────────────────────────────────────────────────
    // consult — 咨询客服
    // ─────────────────────────────────────────────────────────────────────────
    if (intent === 'consult') {
      const chatUrl = getChatUrl(hospital)
      const opened = await openUrl(chatUrl).then(() => true).catch(() => false)

      if (opened) {
        return `✅ 已为你打开 **${hospital.name}** 的在线客服对话页面！

客服页面：${chatUrl}

你可以直接向客服咨询：
• 💰 价格和套餐详情
• 👨‍⚕️ 指定医生是否有档期
• 📅 预约时间确认
• 📋 术前术后注意事项

还需要预约或其他帮助吗？`
      }
      return `⚠️ 打开咨询页面失败，请手动访问：\n\n${chatUrl}`
    }

    return '请告诉我你的需求，例如「查看预约流程」「帮我预约」「咨询客服」「查价格」'
  } catch (err) {
    console.error('[JD Booking Skill] Error:', err.message)
    return `❌ 处理请求时出错：${err.message}。请重试或告诉我具体需求。`
  }
}

// ── 导出（兼容 skill.json 的入口规范） ─────────────────────────────────────

module.exports = { processQuery, hospital }
