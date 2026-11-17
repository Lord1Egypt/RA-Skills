#!/usr/bin/env node
/**
 * scripts/ai.mjs —— 钱包桥 + AI 概念图 + 多 AI 会审（唯一会花钱的模块）
 *
 * 对外接口（BRIEF 5.3 冻结）：
 *   resolveWallet(explicitKey)   -> { key, source, base, pay, hint }
 *   walletStatus(opts)           -> { ok, source, balance, models? }       只读，不探活
 *   generateConcept(workDir,opts)-> { ok, files:[{path,cost}], promptUsed }
 *   reviewFigure(workDir,opts)   -> { ok, tier, verdict, fixes, scores, raw }
 *
 * ── 计费口径（2026-11-03 虾盘云网关实测）──────────────────────────────
 *   ¥1 = 500,000 额度（按模型倍率扣 token，不是「500,000 次调用」）
 *   出图 gpt-image-2.5-1k：单张扣 15,000 额度 = ¥0.03（1024×1024，约 35 秒）
 *   会审 econ 档 4 家 + 裁判：约 ¥0.01–0.07/轮
 *     （实测一轮 prompt 1467 / completion 7605 tokens；成员容易被截断，见下）
 *
 * ── 三条硬约束 ──────────────────────────────────────────────────────
 *   1. 本模块绝不在测试/冒烟里发真实请求：所有对外函数都支持 dryRun，测试只跑 dryRun。
 *   2. 余额不足时上游返回 `Invalid token`（不是密钥坏了）—— 先查余额，别急着换 key。
 *   3. walletStatus 只用 `GET /api/usage/token/` + `GET /api/pricing` 这两个免计费接口，
 *      绝不「生成一张图试试能不能用」。
 *
 * ── 会审的两个实战教训（Lead 2026-11-03 实测）──────────────────────────
 *   · econ 档成员会被 max_tokens 截断：所以成员默认给 3500（不是 800），
 *     `finish_reason==='length'` 时标 truncated 并**只重试一次**更大的额度（别自动烧钱）。
 *   · 卖清单不卖分数：fixes[] 放在输出最前面，每条动词开头、带位置、尽量挂 check 的 code；
 *     scores 往后放并注明「仅用于横向比较」；裁判的「共识/分歧/独到且正确/明显错误/结论」
 *     五段原样保留，别只留结论。
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync } from 'node:fs'
import { homedir } from 'node:os'
import { dirname, isAbsolute, join, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const ROOT = resolve(HERE, '..')

export const BASE_URL = (process.env.UCLAW_API_BASE_URL || 'https://api.u-claw.org.cn').replace(/\/+$/, '')
export const PAY_URL = (process.env.UCLAW_PAY_BASE_URL || 'https://u-claw.org.cn').replace(/\/+$/, '')
export const DEFAULT_IMAGE_MODEL = 'gpt-image-2.5-1k'

/** 成本口径（改价前先看 /api/pricing 的 model_price；这里只是估算，不是账单） */
export const COSTS = {
  creditsPerYuan: 500000,
  image: { model: DEFAULT_IMAGE_MODEL, credits: 15000, cny: 0.03, note: '1024×1024 单张；gpt-image-2 是 ¥0.32/张，贵 10.7 倍，别做默认' },
  review: {
    econ: { cnyMin: 0.01, cnyMax: 0.07, note: '4 家成员 + 裁判；实测 prompt 1467 / completion 7605 tokens' },
    std: { cnyMin: 0.03, cnyMax: 0.15, note: '6 家 + 裁判' },
    deep: { cnyMin: 0.08, cnyMax: 0.25, note: '旗舰 5 家 + 裁判' }
  }
}

/**
 * 会审档位。成员名来自虾盘云实测可用的模型（2026-11-03 全量扫 146 个对话模型），
 * 真值以 `GET /api/pricing` 为准；支持 opts.models / opts.judge 覆盖。
 */
export const TIERS = {
  econ: {
    label: '低价会审',
    models: ['deepseek-v4.1-flash', 'glm-5.3-flash', 'qwen3.8-flash', 'kimi-k3'],
    judge: 'claude-haiku-5-5'
  },
  std: {
    label: '标准会审',
    models: ['deepseek-v4.1-flash', 'glm-5.3', 'qwen3.8-flash', 'kimi-k3.1-pro', 'MiniMax-M3', 'claude-haiku-5-5'],
    judge: 'claude-sonnet-5-5'
  },
  deep: {
    label: '深度会审',
    models: ['gpt-6.1-sol', 'claude-sonnet-5-5', 'deepseek-v4-pro', 'glm-5.3', 'kimi-k3'],
    judge: 'claude-opus-5-5'
  }
}

// 成员默认 token 额度：800 会被截断（实测 4 家全断在中途），3500 才够把三维都说完。
const MEMBER_TOKENS = 3500
const MEMBER_RETRY_TOKENS = 6000 // 截断后只重试一次，最多到这里
const JUDGE_TOKENS = 4000

const MEMBER_SYSTEM = '你是一位资深科研数据可视化审稿人。直接给结论，不要客套、不要反问。只输出 JSON，不要 markdown 代码块围栏。'
const JUDGE_SYSTEM = '你是评审组主席。几位成员独立评了同一张论文配图。你要合并成一份可执行的结论。只输出 JSON，不要 markdown 代码块围栏。'

/* ==========================================================================
 * 一、钱包：密钥解析（只读，不联网）
 * ========================================================================== */

function readJsonSafe(path) {
  try {
    if (!existsSync(path)) return null
    return JSON.parse(readFileSync(path, 'utf8'))
  } catch { return null }
}

/**
 * 解析密钥。优先级（与 dsh-aigc / skill-model-consult 保持一致）：
 *   --key  >  $XIAPAN_API_KEY  >  ~/.dsh/aigc-wallet.json 的 apiKey  >  ~/.uking/device.json 的 key
 *
 * @param {string} explicitKey CLI 传进来的 --key
 * @param {object} opts { homeDir, env } 只为测试注入，正常调用不用传
 * @returns {{ key, source:'flag'|'env'|'wallet'|'uking'|'none', base, pay, hint }}
 */
export function resolveWallet(explicitKey, opts = {}) {
  const home = opts.homeDir || homedir()
  const env = opts.env || process.env
  const walletPath = join(home, '.dsh', 'aigc-wallet.json')
  const devicePath = join(home, '.uking', 'device.json')

  const out = (key, source) => ({
    key: key || '',
    source,
    base: BASE_URL,
    pay: PAY_URL,
    hint: key
      ? ''
      : '没有可用密钥。三个办法任选：① 跑 `node scripts/fig.mjs wallet --bind` 绑一个设备钱包；② 设置环境变量 XIAPAN_API_KEY；③ 用 --key sk-xxx 临时指定。'
  })

  if (explicitKey && String(explicitKey).trim()) return out(String(explicitKey).trim(), 'flag')

  const envKey = env.XIAPAN_API_KEY || env.UCLAW_API_KEY
  if (envKey && String(envKey).trim()) return out(String(envKey).trim(), 'env')

  const wallet = readJsonSafe(walletPath)
  if (wallet && typeof wallet.apiKey === 'string' && wallet.apiKey.trim()) return out(wallet.apiKey.trim(), 'wallet')

  const device = readJsonSafe(devicePath)
  if (device && typeof device.key === 'string' && device.key.trim()) return out(device.key.trim(), 'uking')

  return out('', 'none')
}

function maskKey(key) {
  if (!key) return ''
  if (key.length <= 10) return `${key.slice(0, 3)}…`
  return `${key.slice(0, 6)}…${key.slice(-4)}`
}

/* ==========================================================================
 * 二、HTTP：统一超时 + 人话错误
 * ========================================================================== */

function explainHttp(status, text, what) {
  const t = String(text || '')
  if (/invalid token/i.test(t)) {
    // 虾盘云的坑：余额为 0 时 /v1/* 也返回 Invalid token，看起来像密钥坏了
    return `${what}失败（HTTP ${status}）：上游说 Invalid token。多半不是密钥坏了，而是**钱包余额为 0 或已耗尽** —— 先跑 \`node scripts/fig.mjs wallet\` 看余额，再去 ${PAY_URL}/recharge 充值；确认余额充足再考虑换密钥。`
  }
  if (/quota|insufficient|余额|欠费|exceed/i.test(t)) {
    return `${what}失败（HTTP ${status}）：余额不足。去 ${PAY_URL}/recharge 充值后重试。`
  }
  if (/model.*(not.*found|unavailable)|无可用渠道|no available channel/i.test(t)) {
    return `${what}失败（HTTP ${status}）：这个模型当前没有可用渠道。换一个（--models 指定），或用默认档位。${t.slice(0, 160)}`
  }
  if (status === 401 || status === 403) {
    return `${what}失败（HTTP ${status}）：凭证被拒绝。检查密钥来源与余额（余额 0 也会表现为鉴权失败）。${t.slice(0, 160)}`
  }
  if (status === 429) {
    return `${what}失败（HTTP 429）：请求太频繁，等十几秒再试。`
  }
  return `${what}失败（HTTP ${status}）：${t.slice(0, 240)}`
}

async function httpJson(url, { method = 'GET', key, body, timeoutMs = 120000, what = '请求' } = {}) {
  const started = Date.now()
  let r
  try {
    r = await fetch(url, {
      method,
      headers: {
        ...(body ? { 'content-type': 'application/json' } : {}),
        ...(key ? { authorization: `Bearer ${key}` } : {})
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
      signal: AbortSignal.timeout(timeoutMs)
    })
  } catch (e) {
    const msg = String((e && e.message) || e)
    if (/timeout|aborted/i.test(msg)) {
      throw Object.assign(new Error(`${what}超时（${Math.round(timeoutMs / 1000)} 秒）—— 上游慢或网络卡住了。稍后重试；出图一般 30–60 秒。`), { code: 'ETIMEDOUT' })
    }
    throw Object.assign(new Error(`${what}连不上：${msg}。检查网络，或设代理后重试。`), { code: 'ENETWORK' })
  }
  const text = await r.text()
  let json = null
  try { json = JSON.parse(text) } catch { /* 上游偶尔返回纯文本 */ }
  if (!r.ok) {
    throw Object.assign(new Error(explainHttp(r.status, text, what)), { status: r.status, body: text.slice(0, 2000) })
  }
  return { status: r.status, json, text, ms: Date.now() - started }
}

/* ==========================================================================
 * 三、钱包状态（只读）
 * ========================================================================== */

/**
 * 读余额与可用模型。全程只 GET，不产生任何费用。
 * @param {object} opts { key, homeDir, env, dryRun, timeoutMs }
 */
export async function walletStatus(opts = {}) {
  const w = resolveWallet(opts.key, opts)
  const base = { source: w.source, keyPreview: maskKey(w.key), base: w.base, pay: w.pay }
  if (!w.key) return { ok: false, ...base, balance: null, fix: w.hint }
  if (opts.dryRun) {
    return {
      ok: true, dryRun: true, ...base,
      wouldGet: [`${w.base}/api/usage/token/`, `${w.base}/api/pricing`],
      note: 'dryRun：没有发任何请求，也没花钱'
    }
  }

  const result = { ok: false, ...base, balance: null, models: null, warnings: [] }

  // 1) 余额：/api/usage/token/ -> { code:true, data:{ total_available, total_used, ... } }
  try {
    const r = await httpJson(`${w.base}/api/usage/token/`, { key: w.key, timeoutMs: opts.timeoutMs || 15000, what: '查余额' })
    const d = (r.json && (r.json.data || r.json)) || {}
    result.balance = {
      total_available: d.total_available ?? null,
      total_used: d.total_used ?? null,
      total_granted: d.total_granted ?? null,
      unlimited: d.unlimited_quota === true,
      cny: d.total_available != null ? Number((d.total_available / COSTS.creditsPerYuan).toFixed(2)) : null
    }
    result.ok = true
  } catch (e) {
    result.warnings.push(`余额查不到：${e.message}`)
  }

  // 2) 模型清单：/api/pricing（免计费）。失败不算致命。
  try {
    const r = await httpJson(`${w.base}/api/pricing`, { key: w.key, timeoutMs: opts.timeoutMs || 20000, what: '查模型清单' })
    const list = (r.json && r.json.data) || []
    const rows = Array.isArray(list) ? list : []
    const image = rows.filter((m) => /image/i.test(m.model_name || ''))
    result.models = {
      total: rows.length,
      image: image.length,
      default_image_available: rows.some((m) => m.model_name === DEFAULT_IMAGE_MODEL),
      review_members_available: TIERS.econ.models.filter((m) => rows.some((x) => x.model_name === m)),
      sample: rows.slice(0, 12).map((m) => m.model_name)
    }
  } catch (e) {
    result.warnings.push(`模型清单查不到：${e.message}`)
  }

  if (result.balance && result.balance.total_available === 0) {
    result.fix = `余额是 0。去 ${PAY_URL}/recharge 充一点（¥10 能做几百张图）再跑。`
  }
  if (!result.ok) result.fix = result.fix || '余额接口没通。先确认网络/代理，再确认密钥没被换过（换过就用新 key 重试）。'
  return result
}

/* ==========================================================================
 * 四、成本估算（纯函数，不联网）
 * ========================================================================== */

/**
 * 估算一次操作的价钱。给 CLI 在花钱前打个招呼，也给会审结果标注成本。
 * @param {object} plan { images, reviewTier, vision }
 */
export function estimateCost(plan = {}) {
  const images = Math.max(0, Number(plan.images) || 0)
  const tier = plan.reviewTier ? TIERS[plan.reviewTier] : null
  const items = []
  let cny = 0
  let cnyMin = 0
  let cnyMax = 0

  if (images) {
    const c = images * COSTS.image.cny
    items.push({ what: `${images} 张概念图（${COSTS.image.model}）`, cny: Number(c.toFixed(2)) })
    cny += c; cnyMin += c; cnyMax += c
  }
  if (tier) {
    const r = COSTS.review[plan.reviewTier] || COSTS.review.econ
    const mult = plan.vision ? 1.6 : 1 // 带图会明显多耗 token
    items.push({
      what: `${tier.label}（${tier.models.length} 家 + 裁判 ${tier.judge}）${plan.vision ? '，带图' : ''}`,
      cnyMin: Number((r.cnyMin * mult).toFixed(3)),
      cnyMax: Number((r.cnyMax * mult).toFixed(3))
    })
    cnyMin += r.cnyMin * mult
    cnyMax += r.cnyMax * mult
    cny += (r.cnyMin + r.cnyMax) / 2 * mult
  }
  return {
    items,
    cny: Number(cny.toFixed(3)),
    cnyMin: Number(cnyMin.toFixed(3)),
    cnyMax: Number(cnyMax.toFixed(3)),
    note: `¥1 = ${COSTS.creditsPerYuan.toLocaleString('en-US')} 额度；本钱只是估算，真实扣费以网关账单为准`
  }
}

/* ==========================================================================
 * 五、AI 概念图
 * ==========================================================================*/

/** 把 figure.json / brief.md 揉成一句能出图的中文提示词 */
function buildConceptPrompt(spec, opts) {
  if (opts.prompt) return String(opts.prompt)
  const bits = []
  const typeZh = {
    concept: '概念示意图', toc: '期刊目录图 (TOC graphic)', pipeline: '流程示意',
    architecture: '系统架构示意', mechanism: '机制示意', comparison: '对比示意', chart: '数据图示意'
  }
  const kind = typeZh[(spec && spec.type) || 'concept'] || '概念示意图'
  bits.push(`为学术论文绘制的${kind}，扁平矢量风格，干净的白底，克制的学术配色（蓝/青/橙），细线条，无渐变无阴影`)
  if (spec && spec.caption) bits.push(`主题：${String(spec.caption).replace(/^图\s*\d+\s*/, '').trim()}`)
  if (spec && spec.notes) bits.push(`补充：${String(spec.notes).slice(0, 300)}`)
  if (opts.direction) bits.push(`风格方向：${opts.direction}`)
  bits.push('不要在图里写具体数字或统计结果，不要出现可读的文字标签，只有图形与示意符号')
  return bits.join('。')
}

function normalizeSize(size, spec) {
  const raw = String(size || '').trim().toLowerCase()
  const ok = ['1024x1024', '1024x1536', '1536x1024', '1536x2048', '2048x1536', 'auto']
  if (ok.includes(raw)) return raw
  const m = raw.match(/^(\d+(?:\.\d+)?)\s*[:x/]\s*(\d+(?:\.\d+)?)$/)
  if (m) {
    const r = Number(m[1]) / Number(m[2])
    if (r > 1.25) return '1536x1024'
    if (r < 0.8) return '1024x1536'
    return '1024x1024'
  }
  // 没指定就按图的宽高比走
  const w = Number(spec && spec.width_mm)
  const h = Number(spec && spec.height_mm)
  if (w > 0 && h > 0) {
    const r = w / h
    if (r > 1.6) return '1536x1024'
    if (r < 0.65) return '1024x1536'
  }
  return '1024x1024'
}

function stamp() {
  return new Date().toISOString().replace(/[-:T.]/g, '').slice(0, 14)
}

/**
 * 生成 AI 概念示意图。默认 gpt-image-2.5-1k（¥0.03/张）。
 * 产物：out/concept-<时间戳>-<n>.png + 同名 .ai-generated.json（学术诚信标记）
 *
 * @param {string} workDir
 * @param {object} opts { key, prompt, n, size, model, dryRun, timeoutMs, direction, homeDir, env }
 */
export async function generateConcept(workDir, opts = {}) {
  const wd = resolve(String(workDir || process.cwd()))
  const spec = readJsonSafe(join(wd, 'figure.json')) || {}
  const prompt = buildConceptPrompt(spec, opts)
  const n = Math.min(Math.max(Number(opts.n) || 1, 1), 4)
  const size = normalizeSize(opts.size, spec)
  const model = opts.model || DEFAULT_IMAGE_MODEL
  const cost = Number((COSTS.image.cny * n).toFixed(2))

  const request = {
    url: `${BASE_URL}/v1/images/generations`,
    body: { model, prompt, n, size, response_format: 'b64_json' },
    estimatedCost: { cny: cost, credits: COSTS.image.credits * n }
  }

  const wallet = resolveWallet(opts.key, opts)
  if (!wallet.key) {
    return { ok: false, error: '没有可用密钥，没法生成概念图。', fix: wallet.hint, promptUsed: prompt, request }
  }

  if (opts.dryRun) {
    return {
      ok: true,
      dryRun: true,
      promptUsed: prompt,
      model,
      size,
      n,
      keySource: wallet.source,
      request,
      estimatedCost: request.estimatedCost,
      note: 'dryRun：只组装了请求，没发出去，也没花钱'
    }
  }

  const r = await httpJson(request.url, {
    method: 'POST',
    key: wallet.key,
    body: request.body,
    timeoutMs: Number(opts.timeoutMs) || 180000,
    what: '生成概念图'
  })

  const items = (r.json && (r.json.data || r.json.images)) || []
  const list = Array.isArray(items) ? items : []
  if (!list.length) {
    return {
      ok: false,
      error: `上游返回里没有图片：${String(r.text).slice(0, 200)}`,
      fix: '通常是模型临时不可用或提示词被拦。换 --model gpt-image-2 试一次，或稍后重试。',
      promptUsed: prompt, model, size, n
    }
  }

  const outDir = join(wd, 'out')
  mkdirSync(outDir, { recursive: true })
  const ts = stamp()
  const files = []
  for (let i = 0; i < list.length; i++) {
    const item = list[i] || {}
    const pngPath = join(outDir, `concept-${ts}-${i + 1}.png`)
    try {
      if (item.b64_json) {
        writeFileSync(pngPath, Buffer.from(item.b64_json, 'base64'))
      } else if (item.url) {
        const resp = await fetch(item.url, { signal: AbortSignal.timeout(Number(opts.timeoutMs) || 180000) })
        if (!resp.ok) throw new Error(`下载图片失败 HTTP ${resp.status}`)
        writeFileSync(pngPath, Buffer.from(await resp.arrayBuffer()))
      } else {
        continue
      }
    } catch (e) {
      files.push({ path: pngPath, ok: false, error: e.message, cost: 0 })
      continue
    }
    const markerPath = pngPath.replace(/\.png$/i, '.ai-generated.json')
    writeFileSync(markerPath, JSON.stringify({
      kind: 'ai-generated',
      file: pngPath.split(/[\\/]/).pop(),
      model,
      size,
      prompt,
      createdAt: new Date().toISOString(),
      cost: { cny: COSTS.image.cny, credits: COSTS.image.credits, note: COSTS.image.note },
      captionSuggestion: '图 X  AI 生成的概念示意图（非真实数据），仅用于表达研究思路；如需投稿请替换为矢量绘制版本。',
      constraint: '学术诚信：本图不得作为数据图/结构图直接投稿，图注必须声明 AI 生成。'
    }, null, 2), 'utf8')
    files.push({ path: pngPath, marker: markerPath, ok: true, cost: COSTS.image.cny })
  }

  const okFiles = files.filter((f) => f.ok)
  return {
    ok: okFiles.length > 0,
    files,
    promptUsed: prompt,
    model,
    size,
    n,
    keySource: wallet.source,
    cost: { cny: Number((COSTS.image.cny * okFiles.length).toFixed(2)), note: '按次固定价，重试会再扣一次' },
    ...(okFiles.length ? { captionSuggestion: '这些是 AI 概念示意图，图注里必须写明「AI 生成」，且不能当数据图用。' } : {}),
    ...(okFiles.length ? {} : { error: '图片一张都没落盘。', fix: '检查 out/ 是否可写、磁盘是否满，然后重试（注意重试会再扣费）。' })
  }
}

/* ==========================================================================
 * 六、多 AI 会审
 * ========================================================================== */

/** 读评分规则（references/review-rubric.md），读不到就用内置精简版 */
function loadRubric() {
  const p = join(ROOT, 'references', 'review-rubric.md')
  try {
    if (existsSync(p)) {
      const text = readFileSync(p, 'utf8')
      // 只取前面「四档描述 + 判分纪律」，全文塞给成员太长，反而稀释重点
      return text.slice(0, 4200)
    }
  } catch { /* 忽略 */ }
  return [
    '评分口径：视觉 40 分 / 信息 40 分 / 合规 20 分。',
    '视觉：缩小到目标栏宽后文字是否清晰、元素是否对齐、有几处明显瑕疵。',
    '信息：不看正文能否说出做了什么、结果如何；有没有缺单位/n/误差定义；图注与图是否一致。',
    '合规：只能引用 check 的结果（确定性检查），不许自己估 dpi/字号。',
    '判分纪律：每条扣分必须指到具体位置；不许因为「不够漂亮」扣分；不确定就写「存疑」。'
  ].join('\n')
}

/** 从 figure.json 里抽一段摘要给模型看（别把整个 json 塞过去） */
function specSummary(spec) {
  if (!spec) return '（没有 figure.json）'
  const pick = ['name', 'type', 'journal', 'width', 'width_mm', 'height_mm', 'dpi', 'font', 'font_size_pt', 'palette']
  const lines = []
  for (const k of pick) {
    if (spec[k] !== undefined && spec[k] !== null && spec[k] !== '') lines.push(`${k}: ${spec[k]}`)
  }
  if (spec.caption) lines.push(`caption: ${spec.caption}`)
  if (spec.notes) lines.push(`notes: ${String(spec.notes).slice(0, 400)}`)
  const panels = Array.isArray(spec.panels) ? spec.panels : []
  if (panels.length) {
    lines.push(`panels(${panels.length}): ${panels.map((p) => `${p.id || '?'}${p.title ? '=' + p.title : ''}`).join(' | ').slice(0, 400)}`)
  }
  if (spec.data && typeof spec.data === 'object') lines.push(`data: ${JSON.stringify(spec.data).slice(0, 300)}`)
  return lines.join('\n')
}

/** 从 SVG 里抽「图上都写了什么字」，让看不见图的模型也能判断信息完整性 */
function svgTextSummary(workDir, spec) {
  const outDir = join(workDir, 'out')
  let svgPath = null
  const named = spec && spec.name ? join(outDir, `${spec.name}.svg`) : null
  if (named && existsSync(named)) svgPath = named
  else {
    try {
      const f = readdirSync(outDir).find((x) => x.toLowerCase().endsWith('.svg'))
      if (f) svgPath = join(outDir, f)
    } catch { /* 忽略 */ }
  }
  if (!svgPath) return ''
  try {
    const svg = readFileSync(svgPath, 'utf8')
    const texts = [...svg.matchAll(/<text\b[^>]*>([\s\S]*?)<\/text>/gi)]
      .map((m) => m[1].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim())
      .filter(Boolean)
    const nRect = (svg.match(/<rect\b/gi) || []).length
    const nPath = (svg.match(/<path\b/gi) || []).length
    const nLine = (svg.match(/<line\b/gi) || []).length
    const nImg = (svg.match(/<image\b/gi) || []).length
    return [
      `SVG 元素统计：rect ${nRect} / path ${nPath} / line ${nLine} / image ${nImg}`,
      `图内文字（按出现顺序，共 ${texts.length} 段）：${texts.slice(0, 40).join(' | ')}`
    ].join('\n')
  } catch {
    return ''
  }
}

/** 读 check.json：合规分必须引用它，不许模型自己估 */
function checkSummary(workDir) {
  const p = join(workDir, 'out', 'check.json')
  const j = readJsonSafe(p)
  if (!j) return ''
  const issues = Array.isArray(j.issues) ? j.issues : []
  const errors = issues.filter((i) => i.level === 'error')
  const warns = issues.filter((i) => i.level === 'warn')
  const lines = [
    `确定性合规检查结果（check.json，${issues.length} 条）：pass=${j.pass}`,
    ...errors.slice(0, 12).map((i) => `  [error][${i.code}] ${i.message}`),
    ...warns.slice(0, 8).map((i) => `  [warn][${i.code}] ${i.message}`)
  ]
  if (!issues.length) lines.push('  （无问题：尺寸/字号/DPI/字体/溢出/色盲全过）')
  return lines.join('\n')
}

/** 找一张 PNG 当视觉输入（优先 `<name>@<dpi>dpi.png`） */
function findPng(workDir, spec) {
  const outDir = join(workDir, 'out')
  try {
    const files = readdirSync(outDir).filter((f) => /\.png$/i.test(f) && !/^concept-/i.test(f))
    if (!files.length) return null
    const exact = spec && spec.name ? `${spec.name}.png` : ''
    if (exact && files.includes(exact)) return join(outDir, exact)
    const dpiNamed = files.find((f) => spec && spec.name && f.startsWith(`${spec.name}@`))
    if (dpiNamed) return join(outDir, dpiNamed)
    return join(outDir, files[0])
  } catch { return null }
}

/** 从模型输出里抠出第一个 JSON 对象（容忍 ```json 围栏和前后废话） */
export function extractJson(text) {
  if (!text) return null
  const s = String(text)
  const fenced = s.match(/```(?:json)?\s*([\s\S]*?)```/i)
  const candidates = []
  if (fenced) candidates.push(fenced[1])
  candidates.push(s)
  for (const c of candidates) {
    const start = c.indexOf('{')
    if (start < 0) continue
    let depth = 0
    let inStr = false
    let esc = false
    for (let i = start; i < c.length; i++) {
      const ch = c[i]
      if (inStr) {
        if (esc) esc = false
        else if (ch === '\\') esc = true
        else if (ch === '"') inStr = false
        continue
      }
      if (ch === '"') { inStr = true; continue }
      if (ch === '{') depth++
      else if (ch === '}') {
        depth--
        if (depth === 0) {
          const raw = c.slice(start, i + 1)
          try { return JSON.parse(raw) } catch {
            // 常见毛病：单引号 / 尾逗号，救一把
            try {
              return JSON.parse(raw.replace(/,\s*([}\]])/g, '$1').replace(/'/g, '"'))
            } catch { /* 继续试下一个候选 */ }
          }
        }
      }
    }
  }
  return null
}

/** 统一模型回答的读取：content 空就回退 reasoning_content（glm 系推理模型的坑） */
function readMessage(j) {
  const msg = (j && j.choices && j.choices[0] && j.choices[0].message) || {}
  const flat = (v) => (typeof v === 'string' ? v : Array.isArray(v) ? v.map((p) => (p && p.text) || '').join('') : '')
  const content = flat(msg.content).trim()
  const reasoning = flat(msg.reasoning_content).trim()
  return {
    answer: content || reasoning,
    fromReasoning: !content && Boolean(reasoning),
    finishReason: (j && j.choices && j.choices[0] && j.choices[0].finish_reason) || '',
    usage: {
      prompt: (j && j.usage && j.usage.prompt_tokens) || 0,
      completion: (j && j.usage && j.usage.completion_tokens) || 0
    }
  }
}

async function chat({ key, model, system, user, maxTokens, timeoutMs, images }) {
  const userContent = images && images.length
    ? [{ type: 'text', text: user }, ...images.map((img) => ({ type: 'image_url', image_url: { url: img } }))]
    : user
  const body = {
    model,
    messages: [
      { role: 'system', content: system },
      { role: 'user', content: userContent }
    ],
    max_tokens: maxTokens
    // 注意：claude-haiku-5-5 等模型已不接受 temperature，默认不传
  }
  const r = await httpJson(`${BASE_URL}/v1/chat/completions`, {
    method: 'POST', key, body, timeoutMs, what: `调用 ${model}`
  })
  return { model, ...readMessage(r.json), raw: r.json }
}

/**
 * 判断错误是不是「上游不支持图片输入」，是的话可以优雅降级成纯文本会审
 */
function looksLikeVisionUnsupported(err) {
  const msg = String((err && err.message) || '')
  return /(image|vision|multimodal|图像|图片)/i.test(msg) && /(not supported|unsupported|invalid|不支持|无法)/i.test(msg)
}

const MEMBER_TASK = (ctx) => `你在评审一张准备投给【${ctx.journal}】的论文配图。请按下面的评分口径独立打分，并给出能直接照着改的清单。

${ctx.caption ? `【图注】\n${ctx.caption}\n` : ''}【figure.json 摘要】
${ctx.spec}

${ctx.check ? `【确定性合规检查（已跑过，合规分只能引用它，不许自己估 dpi/字号）】\n${ctx.check}\n` : ''}${ctx.svgText ? `【图内文字与元素（你看不到图时，靠这个判断信息完整性）】\n${ctx.svgText}\n` : ''}${ctx.hasImage ? '\n【另外附上了这张图的 PNG，请结合图像判断视觉维度。】\n' : ''}
【评分口径】
${ctx.rubric}

只输出一个 JSON 对象（不要 markdown 围栏、不要解释），格式：
{
  "scores": {
    "visual": {"score": 0-40 的整数, "notes": ["<具体位置>：<问题>", "..."]},
    "information": {"score": 0-40 的整数, "notes": ["..."]},
    "compliance": {"score": 0-20 的整数, "notes": ["引用 check 的 code 与结论"]}
  },
  "band": "A|B|C|D",
  "fixes": [
    {"where": "panel b / 图例第 2 项 / y 轴标签", "dimension": "visual|information|compliance", "action": "动词开头的可执行句子，含改成什么", "why": "为什么，可选", "issue_code": "若是合规问题，填 check 的 code"}
  ]
}
要求：fixes 至少 3 条，每条都要指到具体位置；分数先从满分往下扣，扣在哪写清楚；不确定的地方写「存疑」而不是瞎猜。`

const JUDGE_TASK = (ctx) => `你是评审组主席。${ctx.count} 位成员独立评了同一张论文配图（投【${ctx.journal}】）。

${ctx.caption ? `【图注】\n${ctx.caption}\n` : ''}${ctx.check ? `【确定性合规检查（合规分的唯一依据）】\n${ctx.check}\n` : ''}
【各成员作答】
${ctx.memberText}

【评分口径】
${ctx.rubric}

把它们合并成一份主席结论。只输出一个 JSON 对象（不要 markdown 围栏）：
{
  "verdict": "一句话结论，例如 B / 小改可投",
  "band": "A|B|C|D",
  "scores": {"visual": 整数, "information": 整数, "compliance": 整数},
  "fixes": [
    {"id": "F1", "dimension": "visual|information|compliance", "where": "具体位置", "action": "动词开头的可执行句子", "why": "为什么", "issue_code": "对应 check 的 code，没有就留空"}
  ],
  "sections": {
    "consensus": "共识：多数成员一致且站得住的点",
    "disagreements": "分歧：谁跟谁不一致、各自理由、你采纳哪边",
    "unique": "独到且正确的点：只有一家发现但确实对",
    "errors": "明显错误：说得不对或不可执行的地方，为什么",
    "conclusion": "结论：用户现在该做什么（按先后顺序）"
  }
}
要求：
1. fixes 按「改了收益最大」排序，合并重复项，去掉无法执行的（「优化布局」这种一律删）。
2. 每条 action 必须是动词开头、含具体位置和改成什么。
3. scores 三个维度都要给，满分分别是 40 / 40 / 20；合规分必须和 check 结论一致（check 有 error 就不许给 18 分以上）。
4. sections 五段都要写，不要偷懒合并。`

/**
 * 多 AI 会审。
 * @param {string} workDir
 * @param {object} opts {
 *   key, tier='econ', models, judge, vision, dryRun, timeoutMs,
 *   memberTokens, judgeTokens, homeDir, env, write=true
 * }
 * @returns {{ ok, tier, verdict, fixes, scores, raw, ... }}
 */
export async function reviewFigure(workDir, opts = {}) {
  const wd = resolve(String(workDir || process.cwd()))
  const spec = readJsonSafe(join(wd, 'figure.json')) || {}
  const tierName = String(opts.tier || 'econ').toLowerCase()
  const tier = TIERS[tierName]
  if (!tier) {
    return {
      ok: false,
      error: `没有「${tierName}」这个档位。`,
      fix: `可选：${Object.keys(TIERS).join(' / ')}。默认 econ（最便宜，¥0.01–0.07/轮）。`
    }
  }

  const models = Array.isArray(opts.models) && opts.models.length
    ? opts.models
    : String(opts.models || '').split(',').map((s) => s.trim()).filter(Boolean).length
      ? String(opts.models).split(',').map((s) => s.trim()).filter(Boolean)
      : tier.models.slice()
  const judge = opts.judge || tier.judge
  const memberTokens = Math.max(1200, Number(opts.memberTokens) || MEMBER_TOKENS)
  const judgeTokens = Math.max(1500, Number(opts.judgeTokens) || JUDGE_TOKENS)

  const ctx = {
    journal: (spec && spec.journal) || 'custom',
    caption: (spec && spec.caption) || '',
    spec: specSummary(spec),
    check: checkSummary(wd),
    svgText: svgTextSummary(wd, spec),
    rubric: loadRubric(),
    hasImage: Boolean(opts.vision)
  }

  const wallet = resolveWallet(opts.key, opts)
  if (!wallet.key) {
    return { ok: false, error: '没有可用密钥，没法发起会审。', fix: wallet.hint, tier: tierName }
  }

  const plan = estimateCost({ reviewTier: tierName, vision: Boolean(opts.vision) })

  // ---- dryRun：把要发的东西全组装好，但不发 —— 测试和「先看看花多少钱」都靠它 ----
  if (opts.dryRun) {
    return {
      ok: true,
      dryRun: true,
      tier: tierName,
      tierLabel: tier.label,
      members: models,
      judge,
      keySource: wallet.source,
      memberTokens,
      judgeTokens,
      vision: opts.vision ? 'requested' : 'off',
      estimatedCost: plan,
      requestPreview: {
        url: `${BASE_URL}/v1/chat/completions`,
        members: models.length,
        memberPromptChars: MEMBER_TASK(ctx).length,
        judgePromptChars: JUDGE_TASK({ ...ctx, count: models.length, memberText: '（省略）' }).length
      },
      note: 'dryRun：一个请求都没发，也没花钱'
    }
  }

  /* ---- 视觉输入 ---- */
  let images = null
  let visionState = 'off'
  let visionNote = ''
  if (opts.vision) {
    const png = findPng(wd, spec)
    if (!png) {
      visionState = 'skipped'
      visionNote = '要带图会审，但 out/ 里没有 PNG。先跑 export 出图；本次已自动降级成纯文本会审。'
    } else {
      try {
        const buf = readFileSync(png)
        if (buf.length > 8 * 1024 * 1024) {
          visionState = 'skipped'
          visionNote = `PNG 有 ${(buf.length / 1024 / 1024).toFixed(1)}MB，太大容易超时；已降级成纯文本会审。先导出小一点的图再试。`
        } else {
          images = [`data:image/png;base64,${buf.toString('base64')}`]
          visionState = 'on'
        }
      } catch (e) {
        visionState = 'skipped'
        visionNote = `PNG 读不了（${e.message}），已降级成纯文本会审。`
      }
    }
  }

  const timeoutMs = Number(opts.timeoutMs) || 180000
  const userPrompt = MEMBER_TASK({ ...ctx, hasImage: Boolean(images) })

  /* ---- 成员并发作答，单家失败不影响整场 ---- */
  const settled = await Promise.allSettled(models.map(async (model) => {
    const first = await chat({ key: wallet.key, model, system: MEMBER_SYSTEM, user: userPrompt, maxTokens: memberTokens, timeoutMs, images })
    let answer = first
    let retried = false
    // 被截断了：只重试一次更大的额度（别自动反复烧钱）
    if (answer.finishReason === 'length' && memberTokens < MEMBER_RETRY_TOKENS) {
      retried = true
      const second = await chat({
        key: wallet.key, model, system: MEMBER_SYSTEM, user: userPrompt,
        maxTokens: Math.min(MEMBER_RETRY_TOKENS, Math.round(memberTokens * 1.7)), timeoutMs, images
      })
      if (second.answer.length > answer.answer.length) answer = second
    }
    return { ...answer, retried }
  }))

  const answers = []
  const failed = []
  settled.forEach((s, i) => {
    if (s.status === 'fulfilled') answers.push(s.value)
    else failed.push({ model: models[i], error: s.reason && s.reason.message ? s.reason.message : String(s.reason) })
  })

  /* ---- 视觉降级：上游不认图片就退回纯文本，并在结果里标注 ---- */
  if (!answers.length && images && failed.some((f) => looksLikeVisionUnsupported({ message: f.error }))) {
    visionState = 'degraded'
    visionNote = '上游不接受图片输入，这一轮已自动降级成纯文本会审（图内文字摘要仍然交给模型了）。'
    const retrySettled = await Promise.allSettled(models.map((model) => chat({
      key: wallet.key, model, system: MEMBER_SYSTEM, user: userPrompt, maxTokens: memberTokens, timeoutMs, images: null
    })))
    failed.length = 0
    retrySettled.forEach((s, i) => {
      if (s.status === 'fulfilled') answers.push(s.value)
      else failed.push({ model: models[i], error: s.reason && s.reason.message ? s.reason.message : String(s.reason) })
    })
  }

  if (!answers.length) {
    return {
      ok: false,
      tier: tierName,
      error: `全部成员失败，这一轮没有结果（没有白花钱，失败请求不计费或已按上游规则退回）。`,
      detail: failed,
      fix: '先跑 `node scripts/fig.mjs wallet` 看余额；余额正常再试一轮，或换 --tier std / --models 指定别的模型。',
      cost: plan
    }
  }

  /* ---- 解析成员作答 ---- */
  const parsed = answers.map((a, i) => {
    const json = extractJson(a.answer)
    return {
      model: a.model,
      ok: Boolean(json),
      truncated: a.finishReason === 'length',
      retried: a.retried,
      fromReasoning: a.fromReasoning,
      scores: json && json.scores ? json.scores : null,
      fixes: json && Array.isArray(json.fixes) ? json.fixes : [],
      band: (json && json.band) || '',
      text: a.answer,
      usage: a.usage
    }
  })

  /* ---- 裁判汇总 ---- */
  const memberText = parsed.map((p, i) => {
    const lines = [`### 成员 ${i + 1}：${p.model}${p.truncated ? '（本次回答被截断，权重可下调）' : ''}`]
    if (p.scores) lines.push(`打分：${JSON.stringify(p.scores)}`)
    if (p.fixes.length) lines.push(`修改清单：${JSON.stringify(p.fixes)}`)
    if (!p.ok) lines.push(`（成员没给 JSON，原文如下）\n${p.text.slice(0, 2500)}`)
    else if (!p.scores) lines.push(p.text.slice(0, 1200))
    return lines.join('\n')
  }).join('\n\n')

  let judgeResult = null
  let judgeRaw = ''
  let judgeError = ''
  try {
    const jr = await chat({
      key: wallet.key, model: judge, system: JUDGE_SYSTEM,
      user: JUDGE_TASK({ ...ctx, count: parsed.length, memberText }),
      maxTokens: judgeTokens, timeoutMs
    })
    judgeRaw = jr.answer
    judgeResult = extractJson(jr.answer)
    if (!judgeResult) judgeError = '裁判没按 JSON 输出（原文已保留在 raw.judge）'
  } catch (e) {
    judgeError = e.message
  }

  /* ---- 兜底汇总：裁判挂了也要给用户一份能用的清单，不能让几毛钱白花 ---- */
  const fallbackAggregate = aggregate(parsed)

  const final = judgeResult && (judgeResult.scores || judgeResult.fixes)
    ? normalizeJudge(judgeResult, fallbackAggregate)
    : { ...fallbackAggregate, degraded: true, degradedReason: judgeError || '裁判输出不可解析，已用成员结果的确定性汇总' }

  const usage = parsed.reduce((acc, p) => ({
    prompt: acc.prompt + (p.usage.prompt || 0),
    completion: acc.completion + (p.usage.completion || 0)
  }), { prompt: 0, completion: 0 })

  const truncated = parsed.filter((p) => p.truncated).map((p) => p.model)

  const result = {
    ok: true,
    tier: tierName,
    tierLabel: tier.label,
    // ↓↓ 卖清单不卖分数：fixes 放在最前面
    verdict: final.verdict,
    band: final.band,
    blocking: Boolean(final.blocking),
    fixes: final.fixes,
    // ↓↓ 分数只用于横向比较，不是验收标准
    scores: final.scores,
    scoreNote: '分数仅用于横向比较（同一个工作区前后两轮 / 同一批图之间），不是验收标准；验收看 fixes 和 check。',
    total: final.total,
    sections: final.sections || null,
    members: parsed.map((p) => ({ model: p.model, ok: p.ok, band: p.band, truncated: p.truncated, retried: p.retried })),
    failed,
    truncated,
    vision: { state: visionState, note: visionNote || null },
    usage,
    cost: plan,
    degraded: Boolean(final.degraded),
    ...(final.degradedReason ? { degradedReason: final.degradedReason } : {}),
    judgeError: judgeError || null,
    keySource: wallet.source,
    raw: {
      members: parsed.map((p) => ({
        model: p.model, ok: p.ok, truncated: p.truncated, retried: p.retried,
        scores: p.scores, fixes: p.fixes, text: p.text
      })),
      judge: judgeRaw
    }
  }

  if (opts.write !== false) {
    try {
      mkdirSync(join(wd, 'out'), { recursive: true })
      const p = join(wd, 'out', 'review.json')
      writeFileSync(p, JSON.stringify({ generatedAt: new Date().toISOString(), ...result }, null, 2), 'utf8')
      result.reviewPath = p
    } catch (e) {
      result.warnings = [...(result.warnings || []), `会审结果没能写到 out/review.json：${e.message}`]
    }
  }

  return result
}

/** 裁判没给出可用结论时的确定性汇总（中位数 + 合并 fixes） */
function aggregate(parsed) {
  const dims = { visual: 40, information: 40, compliance: 20 }
  const scores = {}
  for (const [dim, max] of Object.entries(dims)) {
    const vals = parsed
      .map((p) => (p.scores && p.scores[dim] && Number(p.scores[dim].score)) || null)
      .filter((v) => Number.isFinite(v))
      .sort((a, b) => a - b)
    scores[dim] = { score: vals.length ? Math.round(vals[Math.floor(vals.length / 2)]) : null, max, notes: [] }
  }
  const seen = new Set()
  const fixes = []
  for (const p of parsed) {
    for (const f of p.fixes) {
      const action = String((f && f.action) || '').trim()
      if (!action) continue
      const key = action.slice(0, 24)
      if (seen.has(key)) continue
      seen.add(key)
      fixes.push({
        id: `F${fixes.length + 1}`,
        dimension: (f && f.dimension) || 'visual',
        where: (f && f.where) || '',
        action,
        why: (f && f.why) || '',
        issue_code: (f && (f.issue_code || f.code)) || ''
      })
    }
  }
  const total = Object.entries(scores).reduce((a, [, v]) => a + (v.score || 0), 0)
  const band = total >= 90 ? 'A' : total >= 70 ? 'B' : total >= 45 ? 'C' : 'D'
  return {
    verdict: `${band}（${total} 分，成员结果确定性汇总）`,
    band,
    total,
    scores,
    fixes: fixes.slice(0, 20),
    sections: null,
    blocking: false
  }
}

/** 裁判输出规整：补默认值、确保 fixes 结构统一 */
function normalizeJudge(j, fallback) {
  const dims = { visual: 40, information: 40, compliance: 20 }
  const scores = {}
  for (const [dim, max] of Object.entries(dims)) {
    const raw = j.scores && j.scores[dim]
    const score = typeof raw === 'number' ? raw : (raw && Number(raw.score))
    scores[dim] = {
      score: Number.isFinite(score) ? Math.max(0, Math.min(max, Math.round(score))) : (fallback.scores[dim].score ?? null),
      max,
      notes: (raw && Array.isArray(raw.notes)) ? raw.notes : (fallback.scores[dim].notes || [])
    }
  }
  const fixes = (Array.isArray(j.fixes) ? j.fixes : [])
    .map((f, i) => ({
      id: (f && f.id) || `F${i + 1}`,
      dimension: (f && f.dimension) || 'visual',
      where: (f && f.where) || '',
      action: String((f && f.action) || '').trim(),
      why: (f && f.why) || '',
      issue_code: (f && (f.issue_code || f.code)) || ''
    }))
    .filter((f) => f.action)
  const total = Object.values(scores).reduce((a, v) => a + (v.score || 0), 0)
  const band = j.band || (total >= 90 ? 'A' : total >= 70 ? 'B' : total >= 45 ? 'C' : 'D')
  return {
    verdict: j.verdict || `${band}（${total} 分）`,
    band,
    total,
    scores,
    fixes: fixes.length ? fixes : fallback.fixes,
    sections: j.sections || null,
    blocking: Boolean(j.blocking)
  }
}

/* ==========================================================================
 * 七、CLI
 * ========================================================================== */

function parseArgs(argv) {
  const flags = {}
  const rest = []
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (a === '--json') flags.json = true
    else if (a === '--dry-run') flags.dryRun = true
    else if (a === '--vision') flags.vision = true
    else if (a === '--no-write') flags.write = false
    else if (a.startsWith('--')) { flags[a.slice(2)] = argv[i + 1]; i++ }
    else rest.push(a)
  }
  return { flags, rest }
}

async function main(argv) {
  const [, , cmd, ...tail] = argv
  const { flags, rest } = parseArgs(tail)
  const workDir = rest[0] || process.cwd()

  if (cmd === 'wallet') {
    const r = await walletStatus({ key: flags.key, dryRun: flags.dryRun === true })
    if (flags.json) return console.log(JSON.stringify(r, null, 2))
    if (!r.ok) {
      console.error(r.fix || r.error || '查不到钱包状态')
      process.exitCode = 1
      return
    }
    console.log(`密钥：${r.keyPreview}（来源 ${r.source}）`)
    if (r.balance) console.log(`余额：${r.balance.total_available} 额度 ≈ ¥${r.balance.cny}（已用 ${r.balance.total_used}）`)
    if (r.models) console.log(`可用模型：${r.models.total} 个（其中图片模型 ${r.models.image} 个）`)
    console.log(`充值：${r.pay}/recharge`)
    for (const w of r.warnings || []) console.error(`提醒：${w}`)
    return
  }

  if (cmd === 'cost') {
    const plan = estimateCost({
      images: Number(flags.images) || 0,
      reviewTier: flags.tier || null,
      vision: flags.vision
    })
    if (flags.json) return console.log(JSON.stringify(plan, null, 2))
    for (const it of plan.items) {
      console.log(`· ${it.what}：${it.cny != null ? `¥${it.cny}` : `¥${it.cnyMin}–${it.cnyMax}`}`)
    }
    console.log(`合计约 ¥${plan.cnyMin}–${plan.cnyMax}。${plan.note}`)
    return
  }

  if (cmd === 'concept') {
    const r = await generateConcept(workDir, {
      key: flags.key, prompt: flags.prompt, n: flags.n, size: flags.size,
      model: flags.model, dryRun: flags.dryRun
    })
    if (flags.json) return console.log(JSON.stringify(r, null, 2))
    if (r.dryRun) return console.log(`[dry-run] 会发到 ${r.request.url}\n模型 ${r.model}，${r.n} 张 ${r.size}，预计 ¥${r.estimatedCost.cny}\n提示词：${r.promptUsed}`)
    if (!r.ok) {
      console.error(r.error)
      if (r.fix) console.error(`→ ${r.fix}`)
      process.exitCode = 1
      return
    }
    for (const f of r.files) console.log(`出图：${f.path}（¥${f.cost}）`)
    console.log(r.captionSuggestion || '')
    return
  }

  if (cmd === 'review') {
    const r = await reviewFigure(workDir, {
      key: flags.key, tier: flags.tier, models: flags.models, judge: flags.judge,
      vision: flags.vision, dryRun: flags.dryRun,
      memberTokens: flags['member-tokens'], judgeTokens: flags['judge-tokens']
    })
    if (flags.json) return console.log(JSON.stringify(r, null, 2))
    if (r.dryRun) {
      return console.log(`[dry-run] 档位 ${r.tierLabel}，成员 ${r.members.length} 家 + 裁判 ${r.judge}，预计 ¥${r.estimatedCost.cnyMin}–${r.estimatedCost.cnyMax}`)
    }
    if (!r.ok) {
      console.error(r.error)
      if (r.fix) console.error(`→ ${r.fix}`)
      process.exitCode = 1
      return
    }
    console.log(`## ${r.verdict}\n`)
    console.log('### 先改这些（按收益排序）')
    r.fixes.forEach((f) => console.log(`- [ ] ${f.action}${f.where ? `（${f.where}）` : ''}${f.issue_code ? ` [${f.issue_code}]` : ''}`))
    if (r.sections) {
      const s = r.sections
      if (s.consensus) console.log(`\n### 共识\n${s.consensus}`)
      if (s.disagreements) console.log(`\n### 分歧\n${s.disagreements}`)
      if (s.unique) console.log(`\n### 独到且正确\n${s.unique}`)
      if (s.errors) console.log(`\n### 明显错误\n${s.errors}`)
      if (s.conclusion) console.log(`\n### 结论\n${s.conclusion}`)
    }
    console.log(`\n（分数仅用于横向比较：视觉 ${r.scores.visual.score}/40 · 信息 ${r.scores.information.score}/40 · 合规 ${r.scores.compliance.score}/20）`)
    if (r.failed.length) console.log(`\n本轮失败成员：${r.failed.map((f) => f.model).join('、')}`)
    if (r.truncated.length) console.log(`本轮被截断的成员：${r.truncated.join('、')}（已尝试加大额度重试一次）`)
    if (r.vision.note) console.log(`视觉：${r.vision.note}`)
    return
  }

  console.error(`用法：
  node scripts/ai.mjs wallet                      看密钥来源与余额（只读，免费）
  node scripts/ai.mjs cost --images 2 --tier econ 估算要花多少钱（免费）
  node scripts/ai.mjs concept <dir> [--n 2] [--dry-run]
  node scripts/ai.mjs review <dir> [--tier econ|std|deep] [--vision] [--dry-run]`)
  if (cmd) process.exitCode = 2
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main(process.argv).catch((e) => {
    console.error(`ai 模块出错：${e && e.message ? e.message : e}`)
    process.exit(1)
  })
}

export default { resolveWallet, walletStatus, generateConcept, reviewFigure, estimateCost }
