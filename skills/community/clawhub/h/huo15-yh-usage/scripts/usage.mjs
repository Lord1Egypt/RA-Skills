#!/usr/bin/env node
// 烟花智汇 model usage —— 凭客户 API Key 查该 Key 的 token 用量与费用,输出中文报告。
// 用法: node usage.mjs <fsk-key> [days=30] [--usd] [--json]
//   --usd : 费用按美元显示(= 人民币 / usdRate,汇率由端点返回);默认人民币 ¥。
// 数据源: GET https://fireworks-simulator-api.huo15.com/v1/usage?days=N (Authorization: Bearer fsk-...)
// 端点按 apiKeyId 聚合,返回 totals / byModel / byProvider / daily,费用本位 CNY(¥),附 usdRate。

const BASE = process.env.YH_BASE || 'https://fireworks-simulator-api.huo15.com/v1'

const args = process.argv.slice(2)
const json = args.includes('--json')
const usd = args.includes('--usd')
const rest = args.filter((a) => !a.startsWith('--'))
const key = rest[0]
const days = Math.min(90, Math.max(1, parseInt(rest[1], 10) || 30))

if (!key || !key.startsWith('fsk-')) {
  console.error('用法: node usage.mjs <fsk-...key> [天数=30] [--usd] [--json]\n缺少有效的烟花智汇 API Key(fsk- 开头)。')
  process.exit(1)
}

const n = (x) => Number(x || 0)
const fmtTok = (t) => (t >= 1e6 ? (t / 1e6).toFixed(2) + 'M' : t >= 1e3 ? (t / 1e3).toFixed(1) + 'K' : String(t))
const pad = (s, w) => { s = String(s); const len = [...s].reduce((a, c) => a + (c.charCodeAt(0) > 255 ? 2 : 1), 0); return s + ' '.repeat(Math.max(0, w - len)) }

const r = await fetch(`${BASE}/usage?days=${days}`, { headers: { authorization: `Bearer ${key}` } }).catch((e) => {
  console.error('请求失败:', e.message); process.exit(2)
})
if (!r.ok) {
  console.error(`烟花智汇返回 ${r.status}: ${(await r.text().catch(() => '')).slice(0, 300)}`)
  process.exit(2)
}
const d = await r.json()
if (json) { console.log(JSON.stringify(d, null, 2)); process.exit(0) }

const rate = n(d.usdRate) || 7.2
// 费用格式化:按所选币种(人民币本位,美元=人民币/汇率)
const money = (cny) => {
  const v = n(cny)
  return usd ? '$' + (v / rate).toFixed(v / rate < 1 ? 4 : 2) : '¥' + v.toFixed(v < 1 ? 4 : 2)
}
const curName = usd ? `美元 $(按汇率 ${rate} 折算)` : '人民币 ¥'

const t = d.totals || {}
const L = []
L.push(`## 🎆 烟花智汇 用量账单 · ${d.key?.masked || key.slice(0, 8) + '…'}`)
L.push(`> 近 **${d.range?.days ?? days}** 天 · 费用:**${curName}** · 数据源:平台服务端权威计费`)
L.push(`> 币种切换:默认人民币;加 \`--usd\` 看美元。`)
L.push('')
L.push('### 总览')
L.push(`- 调用 **${n(t.calls)}** 次`)
L.push(`- Token:输入 **${fmtTok(n(t.promptTokens))}** · 输出 **${fmtTok(n(t.completionTokens))}**` +
  (n(t.cachedTokens) ? ` · 缓存 **${fmtTok(n(t.cachedTokens))}**` : '') + ` · 合计 **${fmtTok(n(t.totalTokens))}**`)
L.push(`- 费用合计:**${money(t.cost)}**`)
L.push('')

const bp = d.byProvider || []
if (bp.length) {
  L.push('### 按供应商(按费用降序)')
  L.push('| 供应商 | 调用 | 总Token | 费用 |')
  L.push('|---|--:|--:|--:|')
  for (const p of bp) L.push(`| ${p.provider} | ${n(p.calls)} | ${fmtTok(n(p.totalTokens))} | ${money(p.cost)} |`)
  L.push('')
}

const bm = d.byModel || []
if (bm.length) {
  L.push('### 按模型(按费用降序)')
  L.push('| 模型 | 调用 | 输入 | 输出 | 总Token | 费用 |')
  L.push('|---|--:|--:|--:|--:|--:|')
  for (const m of bm) L.push(`| ${m.model} | ${n(m.calls)} | ${fmtTok(n(m.promptTokens))} | ${fmtTok(n(m.completionTokens))} | ${fmtTok(n(m.totalTokens))} | ${money(m.cost)} |`)
  L.push('')
}

const dl = (d.daily || []).filter((x) => n(x.calls) > 0)
if (dl.length) {
  const max = Math.max(...dl.map((x) => n(x.cost)), 0.0001)
  L.push('### 按天趋势(费用)')
  L.push('```')
  for (const x of dl) L.push(`${x.day}  ${pad(money(x.cost), 10)} ${pad(fmtTok(n(x.tokens)) + 'tok', 8)} ${'█'.repeat(Math.max(1, Math.round((n(x.cost) / max) * 24)))}`)
  L.push('```')
}
L.push('')
L.push('> 费用为烟花智汇按你的套餐/分组实际计费(含缓存折价、分组倍率);美元为按汇率折算的参考值,结算以人民币为准。')
console.log(L.join('\n'))
