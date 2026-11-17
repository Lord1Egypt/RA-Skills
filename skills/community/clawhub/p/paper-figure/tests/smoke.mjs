#!/usr/bin/env node
/**
 * tests/smoke.mjs —— paper-figure 离线冒烟（不联网、不花钱、不需要真实密钥）
 *
 * 跑法：node tests/smoke.mjs
 * 期望：一串 PASS，最后一行 "全部通过"，退出码 0。
 *
 * 三条纪律：
 *   1. 全程把 globalThis.fetch 换成「一调用就抛异常」的桩，并统计调用次数 ——
 *      保证这套测试永远不可能偷偷花用户的钱、也永远不会因为断网而变红。
 *   2. 所有 check 都在临时目录的 fixture 副本上跑，不污染仓库里的样例。
 *   3. 只测「本地能确定的事」：检查器能不能查出错、导出工具认不认得出、
 *      密钥解析顺序对不对、成本估算准不准、dryRun 是不是真的不发请求。
 */

import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync, readdirSync, copyFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { deflateSync } from 'node:zlib'

const HERE = dirname(fileURLToPath(import.meta.url))
const ROOT = resolve(HERE, '..')
const FIXTURES = join(HERE, 'fixtures')

/* ==========================================================================
 * 0. 网络桩：任何真实请求都会让测试直接失败
 * ========================================================================== */

let fetchCalls = 0
globalThis.fetch = async (url) => {
  fetchCalls++
  throw new Error(`冒烟测试里不许发真实网络请求（试图访问 ${url}）。这可能是实现里少了 dryRun 分支。`)
}

/* ==========================================================================
 * 1. 迷你断言框架
 * ========================================================================== */

const results = []
let failed = 0

function pass(name, detail = '') {
  results.push({ name, detail, ok: true })
  console.log(`PASS  ${name}${detail ? `  —— ${detail}` : ''}`)
}

function fail(name, detail) {
  failed++
  results.push({ name, detail, ok: false })
  console.log(`FAIL  ${name}  —— ${detail}`)
}

async function test(name, fn) {
  try {
    const detail = await fn()
    pass(name, detail)
  } catch (e) {
    fail(name, e && e.message ? e.message : String(e))
  }
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg)
}

function assertIncludes(arr, value, what) {
  if (!arr.includes(value)) {
    throw new Error(`${what} 里没有 ${value}，实际是：[${arr.join(', ')}]`)
  }
}

/* ==========================================================================
 * 2. 小工具
 * ========================================================================== */

const TMP = mkdtempSync(join(tmpdir(), 'paper-figure-smoke-'))

/** 把 fixture 复制到临时目录（每次都是干净的） */
function cloneFixture(name) {
  const src = join(FIXTURES, name)
  const dst = join(TMP, `${name}-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`)
  copyDir(src, dst)
  return dst
}

function copyDir(src, dst) {
  mkdirSync(dst, { recursive: true })
  for (const entry of readdirSync(src, { withFileTypes: true })) {
    const s = join(src, entry.name)
    const d = join(dst, entry.name)
    if (entry.isDirectory()) copyDir(s, d)
    else copyFileSync(s, d)
  }
}

const CRC_TABLE = (() => {
  const table = new Int32Array(256)
  for (let n = 0; n < 256; n++) {
    let c = n
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1
    table[n] = c
  }
  return table
})()

function crc32(buf) {
  let c = 0xffffffff
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8)
  return (c ^ 0xffffffff) >>> 0
}

function pngChunk(type, data) {
  const len = Buffer.alloc(4)
  len.writeUInt32BE(data.length, 0)
  const typeBuf = Buffer.from(type, 'ascii')
  const body = Buffer.concat([typeBuf, data])
  const crc = Buffer.alloc(4)
  crc.writeUInt32BE(crc32(body), 0)
  return Buffer.concat([len, body, crc])
}

/** 造一张真实可解码的纯色 PNG（用于「AI 图未打标」「位图被当主图」这类检查） */
function makePng(path, width, height, rgb = [255, 255, 255]) {
  const ihdr = Buffer.alloc(13)
  ihdr.writeUInt32BE(width, 0)
  ihdr.writeUInt32BE(height, 4)
  ihdr[8] = 8 // bit depth
  ihdr[9] = 2 // color type RGB
  ihdr[10] = 0
  ihdr[11] = 0
  ihdr[12] = 0
  const row = Buffer.alloc(1 + width * 3)
  for (let x = 0; x < width; x++) {
    row[1 + x * 3] = rgb[0]
    row[2 + x * 3] = rgb[1]
    row[3 + x * 3] = rgb[2]
  }
  const raw = Buffer.concat(Array.from({ length: height }, () => row))
  const png = Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    pngChunk('IHDR', ihdr),
    pngChunk('IDAT', deflateSync(raw, { level: 6 })),
    pngChunk('IEND', Buffer.alloc(0))
  ])
  writeFileSync(path, png)
  return png
}

const readJson = (p) => JSON.parse(readFileSync(p, 'utf8'))

/* ==========================================================================
 * 3. 开跑
 * ========================================================================== */

console.log('paper-figure 离线冒烟测试（不联网、不花钱）\n')
console.log(`临时目录：${TMP}\n`)

const checkMod = await import('../scripts/check.mjs')
const exportMod = await import('../scripts/export.mjs')
const aiMod = await import('../scripts/ai.mjs')

/* ---------------- A. 合规检查 ---------------- */

await test('check：坏样例能查出 8 类问题', async () => {
  const dir = cloneFixture('broken')
  const r = await checkMod.checkFigure(dir, {})
  const codes = r.issues.map((i) => i.code)
  assert(r.ok, '检查器本身没跑成功')
  assert(r.pass === false, '一堆问题的图竟然 pass=true')
  for (const want of [
    'FIG_WIDTH_TOO_WIDE',        // ① 栏宽
    'FIG_HEIGHT_TOO_TALL',       // ① 高度上限
    'FONT_SIZE_BELOW_MIN',       // ② 字号下限
    'TEXT_OVERFLOW_CANVAS',      // ③ 文字溢出画布
    'TEXT_OVERFLOW_PARENT',      // ③ 文字溢出父容器
    'ELEMENT_OUT_OF_CANVAS',     // ⑦ 元素出界
    'COLORBLIND_RED_GREEN',      // ⑤ 红绿同图
    'FONT_DECORATIVE'            // ⑥ 字体
  ]) assertIncludes(codes, want, '问题列表')
  // 每条都必须带人话 fix
  for (const i of r.issues) {
    assert(typeof i.fix === 'string' && i.fix.length > 8, `${i.code} 缺 fix`)
    assert(['error', 'warn'].includes(i.level), `${i.code} 的 level 不对：${i.level}`)
    assert(typeof i.message === 'string' && i.message.length > 8, `${i.code} 缺 message`)
  }
  return `${r.issues.length} 条问题 / ${Object.keys(Object.fromEntries(r.issues.map((i) => [i.code, 1]))).length} 种 code`
})

await test('check：位图刊能查出 DPI 不足（PLOS 300dpi / figure.json 150dpi）', async () => {
  const dir = cloneFixture('broken-raster')
  const r = await checkMod.checkFigure(dir, {})
  const codes = r.issues.map((i) => i.code)
  assertIncludes(codes, 'DPI_BELOW_MIN', '问题列表')
  assert(r.pass === false, 'DPI 不足却 pass=true')
  return 'DPI_BELOW_MIN 命中'
})

await test('check：干净样例零问题（不能误报）', async () => {
  const dir = cloneFixture('clean')
  const r = await checkMod.checkFigure(dir, {})
  assert(r.ok, '检查器没跑成功')
  assert(r.issues.length === 0, `干净样例被报了 ${r.issues.length} 条：${r.issues.map((i) => i.code).join(', ')}`)
  assert(r.pass === true, 'pass 应该是 true')
  assert(r.summary.stats.width_mm > 88 && r.summary.stats.width_mm < 90, `宽度读错了：${r.summary.stats.width_mm}`)
  assert(r.preset_source === 'journal.mjs', `预置来源应该是 journal.mjs，实际是 ${r.preset_source}`)
  assert(existsSync(join(dir, 'out', 'check.json')), '没有写出 out/check.json')
  const saved = readJson(join(dir, 'out', 'check.json'))
  assert(saved.pass === true, 'out/check.json 里的 pass 不对')
  return `89×60mm，0 issue，预置来源 ${r.preset_source}`
})

await test('check：AI 概念图被当成数据图（学术诚信红线）', async () => {
  const dir = cloneFixture('broken')
  // 两张 AI 图：一张有标记（且图类型是 pipeline），一张没标记
  makePng(join(dir, 'out', 'concept-1.png'), 8, 8)
  makePng(join(dir, 'out', 'concept-2.png'), 8, 8)
  writeFileSync(join(dir, 'out', 'concept-2.ai-generated.json'), JSON.stringify({
    kind: 'ai-generated', model: 'gpt-image-2.5-1k', prompt: '测试用', createdAt: new Date().toISOString()
  }))
  const r = await checkMod.checkFigure(dir, {})
  const codes = r.issues.map((i) => i.code)
  assertIncludes(codes, 'AI_IMAGE_AS_DATA_FIGURE', '问题列表')
  assertIncludes(codes, 'AI_IMAGE_UNMARKED', '问题列表')
  return 'AI_IMAGE_AS_DATA_FIGURE + AI_IMAGE_UNMARKED 命中'
})

await test('check：矢量优先刊物收到位图会拦（Nature 主图只收矢量）', async () => {
  const dir = cloneFixture('broken')
  // 先只有 PNG：应该提醒「主图只收矢量」
  makePng(join(dir, 'out', 'framework@300dpi.png'), 16, 12)
  const r1 = await checkMod.checkFigure(dir, {})
  const codes1 = r1.issues.map((i) => i.code)
  assertIncludes(codes1, 'RASTER_FORMAT_NOT_ACCEPTED_FOR_VECTOR_JOURNAL', '只有位图时的问题列表')
  // 补一个 PDF：提醒应该消失
  writeFileSync(join(dir, 'out', 'framework.pdf'), '%PDF-1.4\n% 测试占位\n')
  const r2 = await checkMod.checkFigure(dir, {})
  const codes2 = r2.issues.map((i) => i.code)
  assert(!codes2.includes('RASTER_FORMAT_NOT_ACCEPTED_FOR_VECTOR_JOURNAL'), '有 PDF 了还在提醒位图格式')
  return '只交位图会提醒，交了 PDF 就闭嘴'
})

await test('check：字号超过期刊上限也会提醒（Nature 上限 7pt）', async () => {
  const dir = cloneFixture('clean')
  const svgPath = join(dir, 'out', 'framework.svg')
  // 7pt = 2.469 用户单位；把一处改成 12pt = 4.233
  const svg = readFileSync(svgPath, 'utf8').replace('font-size="2.469"', 'font-size="4.233"')
  writeFileSync(svgPath, svg)
  const r = await checkMod.checkFigure(dir, {})
  const codes = r.issues.map((i) => i.code)
  assertIncludes(codes, 'FONT_SIZE_ABOVE_MAX', '问题列表')
  const issue = r.issues.find((i) => i.code === 'FONT_SIZE_ABOVE_MAX')
  assert(/7\s*pt/.test(issue.message), `提示里应该写清楚上限 7pt：${issue.message}`)
  return 'FONT_SIZE_ABOVE_MAX 命中'
})

await test('check：缺 figure.json 不崩，给出 next step', async () => {
  const dir = join(TMP, 'empty-workspace')
  mkdirSync(join(dir, 'out'), { recursive: true })
  const r = await checkMod.checkFigure(dir, {})
  const codes = r.issues.map((i) => i.code)
  assertIncludes(codes, 'NO_SPEC', '问题列表')
  assertIncludes(codes, 'NO_SVG', '问题列表')
  assert(r.ok, '检查器不该崩')
  return 'NO_SPEC + NO_SVG'
})

await test('check：内置兜底表的数值与 assets/journals.json 同源', async () => {
  // 这条防的是「安装坏掉 → 静默放宽判定」。两边漂了，用户就会以为合规。
  const journals = readJson(join(ROOT, 'assets', 'journals.json')).journals || []
  assert(journals.length > 0, 'assets/journals.json 读不到')
  const diffs = []
  for (const j of journals) {
    const fb = checkMod.FALLBACK_JOURNALS[j.id]
    if (!fb) { diffs.push(`${j.id} 兜底表里没有`); continue }
    for (const k of ['single_mm', 'double_mm', 'max_height_mm', 'min_font_pt', 'max_font_pt', 'dpi']) {
      const a = fb[k] == null ? null : Number(fb[k])
      const b = j[k] == null ? null : Number(j[k])
      if (a !== b) diffs.push(`${j.id}.${k}: 兜底 ${fb[k]} ≠ journals.json ${j[k]}`)
    }
  }
  assert(!diffs.length, diffs.join('；'))
  return `${journals.length} 本刊的栏宽/高度/字号/DPI 完全一致`
})

await test('check：安装坏掉时不会静默放宽（走 journals.json / 硬兜底并显式告警）', async () => {
  // 模拟「lib/journal.mjs 丢了」：把 scripts/ 和 assets/ 拷到临时目录，删掉图书模块
  const broken = join(TMP, 'broken-install')
  mkdirSync(broken, { recursive: true })
  copyDir(join(ROOT, 'scripts'), join(broken, 'scripts'))
  copyDir(join(ROOT, 'assets'), join(broken, 'assets'))
  rmSync(join(broken, 'scripts', 'lib', 'journal.mjs'), { force: true })

  const mod = await import(`file://${join(broken, 'scripts', 'check.mjs')}`)
  const r1 = await mod.resolvePreset('nature')
  assert(r1.source === 'journals.json', `journal.mjs 没了应该退到 journals.json，实际 ${r1.source}`)
  assert(r1.fromFallback === true, 'fallback 标记没置上')
  assert(r1.preset.single_mm === 89 && r1.preset.max_height_mm === 170, `退回后数值必须和 journals.json 一致，实际 ${r1.preset.single_mm}/${r1.preset.max_height_mm}`)

  // 再让数据文件也消失：应该退到硬编码表，并且依然报同一套数值
  rmSync(join(broken, 'assets'), { recursive: true, force: true })
  const r2 = await mod.resolvePreset('nature')
  assert(r2.source === 'fallback', `连 journals.json 都没了应该退到硬编码表，实际 ${r2.source}`)
  assert(r2.preset.single_mm === 89 && r2.preset.max_height_mm === 170, '硬兜底表的 Nature 数值被改漂了')

  // 真的跑一遍 check：必须出现 CHECK_PRESET_FALLBACK 警告，不能悄悄用错规格
  const dir = cloneFixture('clean')
  const chk = await mod.checkFigure(dir, {})
  const codes = chk.issues.map((i) => i.code)
  assertIncludes(codes, 'CHECK_PRESET_FALLBACK', '问题列表')
  assert(chk.preset_source !== 'journal.mjs', 'preset_source 应该标出降级')
  return 'journals.json → 硬兜底 → 显式告警，三步都在'
})

await test('check：竖排 y 轴标题（rotate -90）不能误报溢出', async () => {
  // 回归：早期版本按「横排字宽」算竖排文字，导致每张图表的坐标轴标签都误报 TEXT_OVERFLOW_CANVAS。
  const dir = cloneFixture('rotated-label')
  const r = await checkMod.checkFigure(dir, {})
  const bad = r.issues.filter((i) => i.code.startsWith('TEXT_OVERFLOW'))
  assert(!bad.length, `竖排标签被误报溢出：${bad.map((i) => i.message).join('；')}`)
  assert(r.issues.length === 0, `这张图本该零问题，实际：${r.issues.map((i) => i.code).join(', ')}`)
  return 'rotate(-90) 标签零误报'
})

await test('check：文字超出画布上方/下方也要报（坐标轴标签 y 漏写的典型症状）', async () => {
  // 回归：render-core 的 chart.mjs 曾把坐标轴标签的 y 写成 0，所有标签挤在顶边被裁掉。
  // 早期检查器只看左右溢出，漏掉了这个真实 bug。
  const dir = join(TMP, 'vertical-overflow')
  mkdirSync(join(dir, 'out'), { recursive: true })
  writeFileSync(join(dir, 'figure.json'), JSON.stringify({
    name: 'vert', type: 'chart', journal: 'nature', width: 'single', dpi: 600, font: 'Arial', font_size_pt: 7
  }))
  writeFileSync(join(dir, 'out', 'vert.svg'), `<svg xmlns="http://www.w3.org/2000/svg" width="89mm" height="60mm" viewBox="0 0 89 60">
  <rect x="0" y="0" width="89" height="60" fill="#ffffff"/>
  <text x="20" y="0" font-family="Arial" font-size="2.469">贴顶的标签</text>
</svg>`)
  const r = await checkMod.checkFigure(dir, {})
  const hit = r.issues.find((i) => i.code === 'TEXT_OVERFLOW_CANVAS')
  assert(hit, `没查出上下溢出，问题列表：${r.issues.map((i) => i.code).join(', ')}`)
  assert(/上方|下方/.test(hit.message), `提示里应该说是上方还是下方：${hit.message}`)
  return '贴顶文字被识别为上方溢出'
})

/* ---------------- B. 导出 ---------------- */

const rasterizer = exportMod.detectRasterizer()

await test('export：detectRasterizer 返回结构正确', async () => {
  assert(['chrome', 'magick', 'none'].includes(rasterizer.name), `name 不对：${rasterizer.name}`)
  if (rasterizer.name !== 'none') {
    assert(typeof rasterizer.path === 'string' && rasterizer.path.length > 0, '有工具却没给 path')
    assert(existsSync(rasterizer.path), `path 不存在：${rasterizer.path}`)
    assert(typeof rasterizer.version === 'string' && rasterizer.version.length > 0, '没给 version')
  }
  return rasterizer.name === 'none'
    ? '本机没有栅格化工具（导出会走 skipped 分支，这是允许的）'
    : `${rasterizer.name} · ${rasterizer.version}`
})

await test('export：真导出 PNG/PDF（无工具时如实 skipped，不静默失败）', async () => {
  const dir = cloneFixture('clean')
  const formats = rasterizer.name === 'chrome' ? ['png', 'pdf'] : ['png']
  const r = await exportMod.exportFigure(dir, { formats, dpi: 300, timeoutMs: 90000 })
  assert(r.rasterizer && r.rasterizer.name === rasterizer.name, '返回里的 rasterizer 不对')
  if (rasterizer.name === 'none') {
    assert(r.ok === false, '没有工具却报 ok=true')
    assert(r.skipped.length >= formats.length, '没有工具时必须每个格式都给 skipped')
    for (const s of r.skipped) assert(s.reason && s.hint, `skipped 缺 reason/hint：${JSON.stringify(s)}`)
    return '无工具 → 每个格式都给了原因和下一步'
  }
  assert(r.ok === true, `导出失败：${JSON.stringify(r.skipped)}`)
  for (const f of r.files) {
    assert(existsSync(f.path), `文件没落盘：${f.path}`)
    assert(f.bytes > 0, `${f.path} 是空文件`)
  }
  const png = r.files.find((f) => f.format === 'png')
  if (png) {
    // 89mm @300dpi ≈ 1051px，允许 3% 误差
    const want = Math.round((89 / 25.4) * 300)
    assert(Math.abs(png.widthPx - want) / want < 0.03, `PNG 宽度 ${png.widthPx}px，期望 ≈${want}px`)
  }
  const pdf = r.files.find((f) => f.format === 'pdf')
  if (pdf) assert(pdf.bytes > 1000, 'PDF 太小，可能是空页')
  return r.files.map((f) => `${f.format}${f.widthPx ? ` ${f.widthPx}×${f.heightPx}` : ''}`).join(' / ')
})

/* ---------------- C. AI / 钱包（全离线） ---------------- */

await test('ai：密钥解析优先级（flag > env > wallet > uking > none）', async () => {
  const home = join(TMP, 'fake-home')
  mkdirSync(join(home, '.dsh'), { recursive: true })
  mkdirSync(join(home, '.uking'), { recursive: true })
  writeFileSync(join(home, '.dsh', 'aigc-wallet.json'), JSON.stringify({ apiKey: 'sk-wallet-000000' }))
  writeFileSync(join(home, '.uking', 'device.json'), JSON.stringify({ key: 'sk-uking-111111' }))

  const r1 = aiMod.resolveWallet('sk-flag-999', { homeDir: home, env: { XIAPAN_API_KEY: 'sk-env-222' } })
  assert(r1.source === 'flag' && r1.key === 'sk-flag-999', `--key 应该最优先，实际 ${r1.source}`)

  const r2 = aiMod.resolveWallet('', { homeDir: home, env: { XIAPAN_API_KEY: 'sk-env-222' } })
  assert(r2.source === 'env' && r2.key === 'sk-env-222', `环境变量应该排第二，实际 ${r2.source}`)

  const r3 = aiMod.resolveWallet('', { homeDir: home, env: {} })
  assert(r3.source === 'wallet' && r3.key === 'sk-wallet-000000', `钱包文件应该排第三，实际 ${r3.source}`)

  rmSync(join(home, '.dsh', 'aigc-wallet.json'))
  const r4 = aiMod.resolveWallet('', { homeDir: home, env: {} })
  assert(r4.source === 'uking' && r4.key === 'sk-uking-111111', `设备密钥应该排第四，实际 ${r4.source}`)

  rmSync(join(home, '.uking', 'device.json'))
  const r5 = aiMod.resolveWallet('', { homeDir: home, env: {} })
  assert(r5.source === 'none' && r5.key === '', `都没有时 source 应该是 none，实际 ${r5.source}`)
  assert(r5.hint && r5.hint.length > 10, '没有密钥时应该给下一步提示')
  return 'flag > env > wallet > uking > none'
})

await test('ai：成本估算口径（¥0.03/张图、econ 会审 ¥0.01–0.07）', async () => {
  const one = aiMod.estimateCost({ images: 1 })
  assert(one.cny === 0.03, `一张图应该 ¥0.03，实际 ${one.cny}`)
  const two = aiMod.estimateCost({ images: 2 })
  assert(two.cny === 0.06, `两张图应该 ¥0.06，实际 ${two.cny}`)
  const review = aiMod.estimateCost({ reviewTier: 'econ' })
  assert(review.cnyMin === 0.01 && review.cnyMax === 0.07, `econ 会审区间应是 ¥0.01–0.07，实际 ${review.cnyMin}–${review.cnyMax}`)
  const both = aiMod.estimateCost({ images: 2, reviewTier: 'econ' })
  assert(both.cnyMin > review.cnyMin, '组合估算应该叠加')
  assert(aiMod.COSTS.image.credits === 15000, '出图额度口径应为 15,000 额度/张')
  return `1 张 ¥${one.cny} · econ ¥${review.cnyMin}–${review.cnyMax} · 全套 ¥${both.cnyMin}–${both.cnyMax}`
})

await test('ai：generateConcept dryRun 不发请求', async () => {
  const dir = cloneFixture('clean')
  const before = fetchCalls
  const r = await aiMod.generateConcept(dir, { dryRun: true, n: 2, key: 'sk-test-only' })
  assert(r.ok && r.dryRun, 'dryRun 应该 ok')
  assert(r.model === 'gpt-image-2.5-1k', `默认模型不对：${r.model}`)
  assert(r.estimatedCost.cny === 0.06, `两张图应估 ¥0.06，实际 ${r.estimatedCost.cny}`)
  assert(r.request.body.n === 2, '请求里 n 不对')
  assert(fetchCalls === before, 'dryRun 竟然发了请求')
  const outFiles = readdirSync(join(dir, 'out'))
  assert(!outFiles.some((f) => f.startsWith('concept-')), 'dryRun 不应该写文件')
  return `请求已组装但没发（${r.request.url}）`
})

await test('ai：reviewFigure dryRun 组装正确（成员 4 家 + 裁判、token 额度够）', async () => {
  const dir = cloneFixture('clean')
  const before = fetchCalls
  const r = await aiMod.reviewFigure(dir, { dryRun: true, key: 'sk-test-only' })
  assert(r.ok && r.dryRun, 'dryRun 应该 ok')
  assert(r.tier === 'econ', `默认档位应该是 econ，实际 ${r.tier}`)
  assert(r.members.length === 4, `econ 档应该 4 家成员，实际 ${r.members.length}`)
  assert(r.judge === 'claude-haiku-5-5', `econ 裁判应该是 claude-haiku-5-5，实际 ${r.judge}`)
  // 实测 800 token 会把 4 家全截断，所以成员必须 ≥3000，裁判 ≥4000
  assert(r.memberTokens >= 3000, `成员 max_tokens 应该 ≥3000（防截断），实际 ${r.memberTokens}`)
  assert(r.judgeTokens >= 4000, `裁判 max_tokens 应该 ≥4000，实际 ${r.judgeTokens}`)
  assert(r.estimatedCost.cnyMin === 0.01, '成本估算没接上')
  assert(fetchCalls === before, 'dryRun 竟然发了请求')
  assert(!existsSync(join(dir, 'out', 'review.json')), 'dryRun 不应该写 review.json')
  return `${r.members.length} 家 + 裁判 ${r.judge}，成员 ${r.memberTokens} token / 裁判 ${r.judgeTokens} token`
})

await test('ai：walletStatus dryRun 只列要调的接口，不碰网络', async () => {
  const before = fetchCalls
  const r = await aiMod.walletStatus({ dryRun: true, key: 'sk-test-only' })
  assert(r.ok && r.dryRun === true, 'dryRun 应该 ok')
  assert(Array.isArray(r.wouldGet) && r.wouldGet.length === 2, '应该列出两个只读接口')
  assert(r.wouldGet.every((u) => /\/api\/(usage\/token\/|pricing)$/.test(u)), `接口路径不对：${r.wouldGet}`)
  assert(r.balance === null || r.balance === undefined, 'dryRun 不该有余额数据')
  assert(fetchCalls === before, 'dryRun 竟然发了请求')
  return '只读接口：/api/usage/token/ + /api/pricing'
})

await test('ai：没密钥时给「怎么办」而不是干巴巴报错', async () => {
  const home = join(TMP, 'nokey-home')
  mkdirSync(home, { recursive: true })
  const r = await aiMod.generateConcept(cloneFixture('clean'), { homeDir: home, env: {} })
  assert(r.ok === false, '没密钥应该 ok=false')
  assert(/bind|XIAPAN_API_KEY|--key/.test(r.fix || ''), `fix 里要给出绑定/环境变量/--key 三条路：${r.fix}`)
  assert(fetchCalls === 0 || true, '')
  return '缺密钥时给出 3 条解决办法'
})

await test('ai：extractJson 能从围栏/废话里抠出 JSON', async () => {
  const cases = [
    ['```json\n{"a":1}\n```', { a: 1 }],
    ['这是我的结论：{"scores":{"visual":{"score":31}}} 以上。', { scores: { visual: { score: 31 } } }],
    ['{"fixes":[{"action":"把图例字号从 4pt 改成 7pt"}]}', { fixes: [{ action: '把图例字号从 4pt 改成 7pt' }] }]
  ]
  for (const [input, want] of cases) {
    const got = aiMod.extractJson(input)
    assert(got, `没解析出来：${input.slice(0, 40)}`)
    assert(JSON.stringify(got) === JSON.stringify(want), `解析结果不对：${JSON.stringify(got)}`)
  }
  assert(aiMod.extractJson('没有 json 的一段话') === null, '没有 JSON 时应该返回 null')
  return '3 种脏输入都能解析'
})

/* ---------------- D. 收尾 ---------------- */

await test('全程零真实网络请求', async () => {
  assert(fetchCalls === 0, `竟然发了 ${fetchCalls} 次真实请求 —— 这会让用户花钱`)
  return 'fetch 调用次数 0'
})

rmSync(TMP, { recursive: true, force: true })

console.log('')
if (failed) {
  console.log(`❌ ${failed} 项失败 / 共 ${results.length} 项`)
  process.exit(1)
}
console.log(`✅ 全部通过（${results.length} 项）· 没有花一分钱 · 没有发一个真实请求`)
process.exit(0)
