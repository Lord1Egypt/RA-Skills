#!/usr/bin/env node
/**
 * scripts/check.mjs —— 论文配图的确定性合规检查（本地跑、不联网、不花一分钱）
 *
 * 对外接口（BRIEF 5.3 冻结）：
 *   checkFigure(workDir, opts) -> {
 *     ok,        // 检查本身跑成功了（不代表图合格）
 *     pass,      // 没有 error 级问题（warn 可以留着）
 *     issues: [{ level:'error'|'warn'|'info', code, message, fix }],
 *     summary: { errors, warns, text, stats }   // text = 给人看的整段报告
 *   }
 *
 * 八类硬校验（code 一览）：
 *   ① 物理尺寸   FIG_WIDTH_TOO_WIDE / FIG_WIDTH_TOO_NARROW / FIG_HEIGHT_TOO_TALL
 *                FIG_SIZE_DECLARED_MISMATCH
 *   ② 字号       FONT_SIZE_BELOW_MIN
 *   ③ 文字溢出   TEXT_OVERFLOW_CANVAS / TEXT_OVERFLOW_PARENT
 *   ④ DPI        DPI_BELOW_MIN / RASTER_DPI_LOW / EXPORTED_PNG_DPI_LOW
 *   ⑤ 色盲       COLORBLIND_RED_GREEN / COLORBLIND_LOW_LUMA_DIFF
 *   ⑥ 字体       FONT_NOT_ACCEPTED / FONT_DECORATIVE / CJK_FONT_MISSING
 *   ⑦ 越界       ELEMENT_OUT_OF_CANVAS
 *   ⑧ AI 图滥用  AI_IMAGE_AS_DATA_FIGURE / AI_IMAGE_UNMARKED /
 *                AI_IMAGE_EMBEDDED_IN_VECTOR / AI_CAPTION_MISSING_DISCLOSURE
 * 另有环境类：NO_SPEC / NO_SVG / SVG_PARSE_FAILED / JOURNAL_PRESET_FALLBACK
 *
 * 设计原则：
 *   - 只读磁盘，绝不联网，绝不写除 out/check.json 之外的东西；
 *   - 期刊数据优先从 scripts/lib/journal.mjs 取（render-core 维护），拿不到就用内置兜底表，
 *     并在结果里标 JOURNAL_PRESET_FALLBACK —— 兜底数字未经核实，别当法条用；
 *   - 每条 issue 都带人话 fix，用户看完能直接动手。
 */

import { existsSync, readFileSync, readdirSync, statSync, mkdirSync, writeFileSync, realpathSync } from 'node:fs'
import { join, resolve, dirname, basename, isAbsolute } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const MM_PER_IN = 25.4
const PT_PER_IN = 72
const PX_PER_IN = 96

/* ==========================================================================
 * 一、期刊预置（兜底表）
 * 这些数字是「常见量级」，用于 render-core 的 journal.mjs 尚未就绪时也能工作。
 * 真要投稿，以期刊最新 author guidelines 为准 —— summary 里会标注来源。
 * ========================================================================== */

/**
 * 最后一道兜底（只有 lib/journal.mjs 和 assets/journals.json 都读不到时才用）。
 * ★ 数值与 assets/journals.json 同源核对过（2026-11-03）；那边改了这边必须跟着改，
 *   否则安装坏掉的时候判定会静默放宽 —— 模板错 = 用户退稿，这是产品最不能出的错。
 * ★ 正常情况下根本走不到这里：journal.mjs 就绪时用它，坏了就用 journals.json，
 *   两处都失败才用本表，并且会打 CHECK_PRESET_FALLBACK 警告。
 */
export const FALLBACK_JOURNALS = {
  nature: {
    id: 'nature', label: 'Nature', single_mm: 89, double_mm: 183, max_height_mm: 170,
    min_font_pt: 5, max_font_pt: 7, dpi: null, formats: ['pdf', 'eps', 'svg', 'ai'],
    fonts: ['Arial', 'Helvetica'],
    color_mode: 'rgb', notes: '主图只收矢量（.ai/.eps/.pdf，另收分层 PSD 与 plain SVG）；图高 ≤170mm；字号 5–7pt；tif/jpeg 只能用于 Extended Data'
  },
  science: {
    id: 'science', label: 'Science', single_mm: 55, double_mm: 183, max_height_mm: 229,
    min_font_pt: 5, dpi: 600, formats: ['eps', 'pdf', 'tif'], fonts: ['Arial', 'Helvetica'],
    color_mode: 'rgb', notes: '栏宽 55/183mm；字号 5–7pt'
  },
  cell: {
    id: 'cell', label: 'Cell / Cell Press', single_mm: 85, double_mm: 178, max_height_mm: 234,
    min_font_pt: 6, dpi: 600, formats: ['pdf', 'eps', 'tif'], fonts: ['Arial', 'Helvetica'],
    color_mode: 'rgb', notes: '单栏 85mm、双栏 178mm；不小于 6pt'
  },
  ieee: {
    id: 'ieee', label: 'IEEE Transactions / Journals', single_mm: 88.9, double_mm: 181.9, max_height_mm: 234,
    min_font_pt: 8, dpi: 600, formats: ['pdf', 'eps', 'ps'], fonts: ['Times New Roman', 'Arial', 'Helvetica'],
    color_mode: 'rgb', notes: '图内字号 8–10pt；不要只靠彩色传达信息'
  },
  elsevier: {
    id: 'elsevier', label: 'Elsevier', single_mm: 90, double_mm: 190, max_height_mm: 240,
    min_font_pt: 7, dpi: 600, formats: ['eps', 'pdf', 'tif'], fonts: ['Arial', 'Helvetica', 'Times New Roman'],
    color_mode: 'rgb', notes: '单栏 90mm、双栏 190mm'
  },
  springer: {
    id: 'springer', label: 'Springer', single_mm: 84, double_mm: 174, max_height_mm: 234,
    min_font_pt: 6, dpi: 600, formats: ['eps', 'pdf', 'tif'], fonts: ['Arial', 'Helvetica'],
    color_mode: 'rgb', notes: '单栏 84mm、双栏 174mm'
  },
  acm: {
    id: 'acm', label: 'ACM (sigconf)', single_mm: 86.9, double_mm: 177.8, max_height_mm: 234,
    min_font_pt: 8, dpi: 600, formats: ['pdf', 'eps'], fonts: ['Arial', 'Helvetica', 'Times New Roman'],
    color_mode: 'rgb', notes: '图内字号不小于 8pt'
  },
  plos: {
    id: 'plos', label: 'PLOS ONE / PLOS 系列', single_mm: 66.8, double_mm: 190.5, max_height_mm: 233,
    min_font_pt: 8, dpi: 300, formats: ['tif', 'eps'], fonts: ['Arial', 'Times New Roman', 'Symbol'],
    color_mode: 'rgb', notes: '图宽 66.8–190.5mm（789–2250px@300dpi）；字号 ≥8pt；推荐 TIFF/EPS'
  },
  'thesis-cn': {
    id: 'thesis-cn', label: '中文学位论文（通用）', single_mm: 80, double_mm: 170, max_height_mm: 200,
    min_font_pt: 9, dpi: 600, formats: ['pdf', 'png', 'tif'],
    fonts: ['宋体', '黑体', 'Times New Roman', 'Arial'],
    color_mode: 'rgb', notes: '中文正文常用宋体/黑体，图内字号不小于 6pt；按学位授予单位模板为准'
  },
  custom: {
    id: 'custom', label: '自定义（兜底）', single_mm: 89, double_mm: 183, max_height_mm: 247,
    min_font_pt: 6, dpi: 600, formats: ['svg', 'pdf', 'png', 'tif'], fonts: ['Arial'],
    color_mode: 'rgb', notes: '没指定期刊时的通用兜底；正式投稿请用 --journal 指明'
  }
}

/**
 * 调色板兜底（只有 lib/palette.mjs 和 assets/palettes.json 都读不到时才会用到）。
 * 只关心「是否色盲安全 / 是否灰度可读」这两个判定位，具体色值归 render-core 管。
 * ★ 与 assets/palettes.json 同源核对过，smoke 会校验两边不漂。
 */
export const FALLBACK_PALETTES = {
  'okabe-ito': { id: 'okabe-ito', label: 'Okabe-Ito（色盲安全 · Nature 官方推荐）', colorblind_safe: true, grayscale_ok: false },
  'nature-cool': { id: 'nature-cool', label: 'Nature 冷色（低饱和）', colorblind_safe: false, grayscale_ok: true },
  'grayscale-safe': { id: 'grayscale-safe', label: '灰度安全（黑白打印友好）', colorblind_safe: true, grayscale_ok: true },
  brand: { id: 'brand', label: '品牌色（深海蓝/青）', colorblind_safe: false, grayscale_ok: false }
}

// 能被当「位图交付格式」的扩展名 / 「矢量交付格式」的扩展名
const RASTER_EXTS = ['png', 'tif', 'tiff', 'jpg', 'jpeg']
const VECTOR_EXTS = ['pdf', 'eps', 'ai', 'svg', 'ps']

// 期刊一般都不接受的花哨字体：看着就不像能投稿的
const DECORATIVE_FONTS = ['comic sans ms', 'comic sans', 'papyrus', 'impact', 'chalkboard',
  'chalkduster', 'marker felt', 'zapfino', 'bradley hand', 'curlz mt', 'brush script mt']

// 有中文字形的字体（用来判断「中文会不会变方框」）
const CJK_FONTS = ['pingfang', 'pingfang sc', 'hiragino sans gb', 'heiti', 'simhei', 'simsun',
  'songti', 'fangsong', 'kaiti', 'microsoft yahei', 'noto sans cjk', 'noto serif cjk',
  'source han sans', 'source han serif', 'wenquanyi', 'droid sans fallback', 'arial unicode ms']

const NAMED_COLORS = {
  white: '#ffffff', black: '#000000', red: '#ff0000', green: '#008000', blue: '#0000ff',
  lime: '#00ff00', gray: '#808080', grey: '#808080', silver: '#c0c0c0', maroon: '#800000',
  olive: '#808000', teal: '#008080', navy: '#000080', purple: '#800080', orange: '#ffa500',
  yellow: '#ffff00', cyan: '#00ffff', magenta: '#ff00ff', darkred: '#8b0000', darkgreen: '#006400'
}

/* ==========================================================================
 * 二、小工具
 * ========================================================================== */

const round = (n, d = 1) => Number(Number(n).toFixed(d))
const clampNum = (n, lo, hi) => Math.min(hi, Math.max(lo, n))

function readJsonSafe(path) {
  try {
    if (!existsSync(path)) return null
    return JSON.parse(readFileSync(path, 'utf8'))
  } catch {
    return null
  }
}

function exists(p) {
  try { return existsSync(p) && statSync(p).isFile() } catch { return false }
}

function listDir(dir) {
  try { return readdirSync(dir) } catch { return [] }
}

/** 把可能是相对路径的 workDir 变成绝对路径（跨平台） */
function absDir(workDir) {
  const d = workDir ? String(workDir) : process.cwd()
  try { return realpathSync(resolve(d)) } catch { return resolve(d) }
}

/* ==========================================================================
 * 三、SVG 解析（零依赖手写）
 * 目标不是完整实现 SVG 规范，而是把「我们的渲染器会产出的那部分」读准：
 * <svg width/height/viewBox> <g transform> <rect> <text> <tspan> <image> <style>
 * ========================================================================== */

/** 解析标签里的属性，返回小写 key 的字典 */
function parseAttrs(src) {
  const attrs = {}
  const re = /([A-Za-z_:][\w:.-]*)\s*=\s*("([^"]*)"|'([^']*)'|([^\s"'>]+))/g
  let m
  while ((m = re.exec(src))) {
    attrs[m[1].toLowerCase()] = m[3] !== undefined ? m[3] : m[4] !== undefined ? m[4] : m[5]
  }
  return attrs
}

/** 把 SVG 文本切成 token 流：open / close / text / style */
function tokenizeSvg(svg) {
  const tokens = []
  let i = 0
  const n = svg.length
  while (i < n) {
    const lt = svg.indexOf('<', i)
    if (lt < 0) {
      tokens.push({ type: 'text', value: svg.slice(i) })
      break
    }
    if (lt > i) tokens.push({ type: 'text', value: svg.slice(i, lt) })

    if (svg.startsWith('<!--', lt)) {
      const e = svg.indexOf('-->', lt)
      i = e < 0 ? n : e + 3
      continue
    }
    if (svg.startsWith('<![CDATA[', lt)) {
      const e = svg.indexOf(']]>', lt)
      const body = svg.slice(lt + 9, e < 0 ? n : e)
      tokens.push({ type: 'text', value: body })
      i = e < 0 ? n : e + 3
      continue
    }
    if (svg.startsWith('<?', lt) || svg.startsWith('<!', lt)) {
      const e = svg.indexOf('>', lt)
      i = e < 0 ? n : e + 1
      continue
    }

    // 找到这个标签的结尾（跳过引号里的 >）
    let j = lt + 1
    let quote = null
    while (j < n) {
      const c = svg[j]
      if (quote) { if (c === quote) quote = null } else if (c === '"' || c === "'") quote = c
      else if (c === '>') break
      j++
    }
    const raw = svg.slice(lt + 1, j)
    i = j + 1

    if (raw.startsWith('/')) {
      tokens.push({ type: 'close', name: raw.slice(1).trim().toLowerCase() })
      continue
    }
    const selfClose = /\/\s*$/.test(raw)
    const body = selfClose ? raw.replace(/\/\s*$/, '') : raw
    const nameMatch = body.match(/^([A-Za-z][\w:.-]*)/)
    const name = nameMatch ? nameMatch[1].toLowerCase() : ''
    const attrs = parseAttrs(body.slice(nameMatch ? nameMatch[0].length : 0))

    if (name === 'style' && !selfClose) {
      const end = svg.indexOf('</style>', i)
      tokens.push({ type: 'style', value: svg.slice(i, end < 0 ? n : end) })
      i = end < 0 ? n : end + 8
      continue
    }
    if (name === 'script' && !selfClose) {
      const end = svg.indexOf('</script>', i)
      i = end < 0 ? n : end + 9
      continue
    }
    tokens.push({ type: 'open', name, attrs, selfClose })
  }
  return tokens
}

/* --- 变换矩阵 [a,b,c,d,e,f]：x' = a·x + c·y + e, y' = b·x + d·y + f --- */

const IDENTITY = [1, 0, 0, 1, 0, 0]

function mulMatrix(p, c) {
  return [
    p[0] * c[0] + p[2] * c[1],
    p[1] * c[0] + p[3] * c[1],
    p[0] * c[2] + p[2] * c[3],
    p[1] * c[2] + p[3] * c[3],
    p[0] * c[4] + p[2] * c[5] + p[4],
    p[1] * c[4] + p[3] * c[5] + p[5]
  ]
}

function applyMatrix(m, x, y) {
  return [m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]]
}

function scaleOf(m) {
  const sx = Math.hypot(m[0], m[1])
  const sy = Math.hypot(m[2], m[3])
  return (sx + sy) / 2 || 1
}

function parseTransform(str) {
  let m = IDENTITY.slice()
  if (!str) return m
  const re = /(matrix|translate|scale|rotate|skewX|skewY)\s*\(([^)]*)\)/g
  let g
  while ((g = re.exec(str))) {
    const nums = (g[2].match(/-?\d*\.?\d+(?:e[-+]?\d+)?/gi) || []).map(Number)
    let t = IDENTITY.slice()
    switch (g[1]) {
      case 'matrix':
        if (nums.length >= 6) t = nums.slice(0, 6)
        break
      case 'translate':
        t = [1, 0, 0, 1, nums[0] || 0, nums[1] || 0]
        break
      case 'scale':
        t = [nums[0] ?? 1, 0, 0, nums[1] ?? nums[0] ?? 1, 0, 0]
        break
      case 'rotate': {
        const a = ((nums[0] || 0) * Math.PI) / 180
        const cos = Math.cos(a)
        const sin = Math.sin(a)
        t = [cos, sin, -sin, cos, 0, 0]
        if (nums.length >= 3) {
          const cx = nums[1]
          const cy = nums[2]
          // rotate(a,cx,cy) = translate(cx,cy)·rotate(a)·translate(-cx,-cy)
          t = mulMatrix(mulMatrix([1, 0, 0, 1, cx, cy], t), [1, 0, 0, 1, -cx, -cy])
        }
        break
      }
      case 'skewX':
        t = [1, 0, Math.tan(((nums[0] || 0) * Math.PI) / 180), 1, 0, 0]
        break
      case 'skewY':
        t = [1, Math.tan(((nums[0] || 0) * Math.PI) / 180), 0, 1, 0, 0]
        break
    }
    m = mulMatrix(m, t)
  }
  return m
}

/** 把 style="a:b;c:d" 拆成 {a:'b', c:'d'} */
function parseInlineStyle(str) {
  const out = {}
  if (!str) return out
  for (const part of String(str).split(';')) {
    const k = part.indexOf(':')
    if (k < 0) continue
    out[part.slice(0, k).trim().toLowerCase()] = part.slice(k + 1).trim()
  }
  return out
}

/** 极简 CSS 解析：够用于 .cls{font-size:6px} / text{...} 这种规模 */
function parseCss(css) {
  const byClass = {}
  const base = {}
  const allFontSizes = []
  const allFontFamilies = []
  if (!css) return { byClass, base, allFontSizes, allFontFamilies }
  const re = /([^{}]+)\{([^{}]*)\}/g
  let m
  while ((m = re.exec(css))) {
    const selector = m[1].trim()
    const decls = parseInlineStyle(m[2])
    for (const [k, v] of Object.entries(decls)) {
      if (k === 'font-size') allFontSizes.push(v)
      if (k === 'font-family') allFontFamilies.push(v)
    }
    for (const sel of selector.split(',')) {
      const s = sel.trim()
      if (/^\.[\w-]+$/.test(s)) byClass[s.slice(1)] = { ...(byClass[s.slice(1)] || {}), ...decls }
      else if (s === 'text' || s === 'svg' || s === 'svg *' || s === '*') {
        Object.assign(base, decls)
      }
    }
  }
  return { byClass, base, allFontSizes, allFontFamilies }
}

/** 解析带单位的长度 → 用户单位（viewBox 坐标系） */
function toUserUnits(value, unit, unitToMm) {
  const v = Number(String(value).replace(/[a-z%]+$/i, ''))
  if (!Number.isFinite(v)) return null
  switch (String(unit || '').toLowerCase()) {
    case '':
    case 'px':
    case 'user': return v
    case 'mm': return v / unitToMm
    case 'cm': return (v * 10) / unitToMm
    case 'in': return (v * MM_PER_IN) / unitToMm
    case 'pt': return (v * MM_PER_IN) / PT_PER_IN / unitToMm
    case 'pc': return (v * MM_PER_IN) / 6 / unitToMm
    case 'q': return (v * 0.25) / unitToMm
    default: return null
  }
}

function splitLen(raw) {
  if (raw === undefined || raw === null) return null
  const m = String(raw).trim().match(/^(-?\d*\.?\d+(?:e[-+]?\d+)?)\s*([a-z%]*)$/i)
  if (!m) return null
  return { value: Number(m[1]), unit: (m[2] || '').toLowerCase() }
}

/**
 * 解析整份 SVG。
 * 返回 { widthMm, heightMm, unitToMm, viewBox, texts, rects, shapes, images, colors,
 *        fontFamilies, fontSizesPt, hasCjkText, overflowHints }
 */
function parseSvg(svgText) {
  const tokens = tokenizeSvg(svgText)
  const css = parseCss(tokens.filter((t) => t.type === 'style').map((t) => t.value).join('\n'))

  let viewBox = null
  let widthAttr = null
  let heightAttr = null

  // 先找根 <svg> 的尺寸
  for (const t of tokens) {
    if (t.type === 'open' && t.name === 'svg') {
      widthAttr = t.attrs.width ?? null
      heightAttr = t.attrs.height ?? null
      const vb = t.attrs.viewbox
      if (vb) {
        const nums = (vb.match(/-?\d*\.?\d+(?:e[-+]?\d+)?/gi) || []).map(Number)
        if (nums.length >= 4) viewBox = { x: nums[0], y: nums[1], w: nums[2], h: nums[3] }
      }
      break
    }
  }

  const wLen = splitLen(widthAttr)
  const hLen = splitLen(heightAttr)

  // 物理宽度（mm）：width 属性给绝对单位最准，px 按 96dpi 换算，没单位当用户单位（96dpi）
  let widthMm = null
  if (wLen && wLen.unit && wLen.unit !== 'px' && wLen.unit !== '%') {
    const conv = toUserUnits(wLen.value, wLen.unit, 1) // unitToMm=1 时返回值即 mm
    if (conv !== null) widthMm = conv
  } else if (wLen) {
    widthMm = (wLen.value * MM_PER_IN) / PX_PER_IN
  }
  let heightMm = null
  if (hLen && hLen.unit && hLen.unit !== 'px' && hLen.unit !== '%') {
    const conv = toUserUnits(hLen.value, hLen.unit, 1)
    if (conv !== null) heightMm = conv
  } else if (hLen) {
    heightMm = (hLen.value * MM_PER_IN) / PX_PER_IN
  }

  // 用户单位 → mm 的比例：优先 width/vbWidth，其次 height/vbHeight，再不行按 96dpi
  let unitToMm = MM_PER_IN / PX_PER_IN
  if (viewBox && viewBox.w > 0 && widthMm) unitToMm = widthMm / viewBox.w
  else if (viewBox && viewBox.h > 0 && heightMm) unitToMm = heightMm / viewBox.h
  else if (viewBox && viewBox.w > 0 && !widthMm) {
    widthMm = viewBox.w * (MM_PER_IN / PX_PER_IN)
    if (viewBox.h > 0) heightMm = viewBox.h * (MM_PER_IN / PX_PER_IN)
  } else if (!viewBox && widthMm && heightMm) {
    viewBox = { x: 0, y: 0, w: (widthMm * PX_PER_IN) / MM_PER_IN, h: (heightMm * PX_PER_IN) / MM_PER_IN }
  }

  const out = {
    viewBox,
    widthMm,
    heightMm,
    unitToMm,
    texts: [],        // { x, y, w, h, fontSizeUser, anchor, family, content, matrix }
    rects: [],        // { x, y, w, h } 已转成用户单位、已应用变换
    shapes: [],       // 用于越界检查的几何元素 bbox
    images: [],       // { x, y, w, h, href }
    colors: new Map(),// '#rrggbb' -> { count, roles:Set }
    fontFamilies: new Set(),
    fontChains: new Set(), // 完整 font-family 回退链（判断中文会不会变方框要看整条链）
    fontSizesPt: [],  // 直接从 font-size 属性换算出来的 pt
    hasCjkText: false,
    textContent: ''
  }

  // ---------- 遍历 ----------
  const stack = [] // { name, matrix }
  let matrix = IDENTITY.slice()
  let textCtx = null
  let textSegs = []
  let skippedDepth = 0 // 在 <defs>/<symbol>/<clipPath>/<marker> 里不算可见内容

  const pushColor = (raw, role) => {
    if (!raw) return
    const v = String(raw).trim().toLowerCase()
    if (!v || v === 'none' || v === 'transparent' || v === 'currentcolor' || v.startsWith('url(')) return
    let hex = v
    if (v.startsWith('#')) {
      if (v.length === 4) hex = '#' + v[1] + v[1] + v[2] + v[2] + v[3] + v[3]
      else if (v.length === 7) hex = v
      else return
    } else if (NAMED_COLORS[v]) {
      hex = NAMED_COLORS[v]
    } else if (/^rgb/i.test(v)) {
      const nums = (v.match(/\d+(\.\d+)?/g) || []).map(Number)
      if (nums.length < 3) return
      hex = '#' + nums.slice(0, 3).map((x) => clampNum(Math.round(x), 0, 255).toString(16).padStart(2, '0')).join('')
    } else {
      return
    }
    const cur = out.colors.get(hex) || { count: 0, roles: new Set() }
    cur.count++
    cur.roles.add(role)
    out.colors.set(hex, cur)
  }

  const flushText = () => {
    if (!textCtx) return
    const content = textCtx.content.replace(/\s+/g, ' ').trim()
    if (!content) { textCtx = null; return }
    const fs = textCtx.fontSizeUser
    if (!(fs > 0)) { textCtx = null; return }
    const m = textCtx.matrix
    const scale = scaleOf(m)
    // 文字框先在「自己的局部坐标」里算（宽 = 估算字宽 × 字号），再整体套变换矩阵。
    // 不这么做的话，y 轴那种 rotate(-90) 的标签会被当成横着排，
    // 每张带坐标轴标签的图都会误报溢出 —— 实测踩过（render-core 的 chart.mjs 就是这么画的）。
    const wLocal = estimateTextWidthEm(content) * fs
    const x0 = textCtx.anchor === 'middle' ? -wLocal / 2 : (textCtx.anchor === 'end' ? -wLocal : 0)
    const local = [
      [textCtx.x + x0, textCtx.y - fs * 0.82],
      [textCtx.x + x0 + wLocal, textCtx.y - fs * 0.82],
      [textCtx.x + x0, textCtx.y + fs * 0.26],
      [textCtx.x + x0 + wLocal, textCtx.y + fs * 0.26]
    ].map(([lx, ly]) => applyMatrix(m, lx, ly))
    const xs = local.map((pt) => pt[0])
    const ys = local.map((pt) => pt[1])
    const left = Math.min(...xs)
    const top = Math.min(...ys)
    const w = Math.max(...xs) - left
    const h = Math.max(...ys) - top
    const [px, py] = applyMatrix(m, textCtx.x, textCtx.y)
    textSegs.push({
      x: left, y: top, w, h,
      fontSizeUser: fs * scale,
      anchor: textCtx.anchor, family: textCtx.family, content,
      anchorPoint: [px, py],
      rotated: Math.abs(Math.sin(Math.atan2(m[1], m[0]))) > 0.2
    })
    out.textContent += content + ' '
    if (/[\u2e80-\u9fff\uf900-\ufaff\u3000-\u303f\uff00-\uffef]/.test(content)) out.hasCjkText = true
    if (textCtx.family) out.fontFamilies.add(textCtx.family)
    if (textCtx.familyChain) out.fontChains.add(textCtx.familyChain)
    textCtx = null
  }

  const resolveStyle = (attrs) => {
    const inline = parseInlineStyle(attrs.style)
    const cls = (attrs.class || '').split(/\s+/).filter(Boolean)
    const fromCss = {}
    for (const c of cls) if (css.byClass[c]) Object.assign(fromCss, css.byClass[c])
    return { ...css.base, ...fromCss, ...attrs, ...inline }
  }

  for (const t of tokens) {
    if (t.type === 'text') {
      if (textCtx) textCtx.content += t.value
      continue
    }
    if (t.type === 'style') continue

    if (t.type === 'open') {
      const name = t.name
      if (name === 'defs' || name === 'symbol' || name === 'clippath' || name === 'mask' || name === 'marker' || name === 'pattern') {
        if (!t.selfClose) skippedDepth++
        continue
      }
      const st = resolveStyle(t.attrs)
      const local = parseTransform(t.attrs.transform)
      const prevMatrix = matrix
      matrix = mulMatrix(matrix, local)

      if (skippedDepth === 0) {
        if (name === 'text') {
          flushText()
          const fsRaw = st['font-size']
          const fsl = splitLen(fsRaw)
          let fsUser = null
          if (fsl) fsUser = toUserUnits(fsl.value, fsl.unit, out.unitToMm)
          if (!(fsUser > 0)) fsUser = 3 // 缺省字号按 SVG 默认 12px 估算即可
          const scale = scaleOf(matrix)
          textCtx = {
            x: Number(st.x ?? 0) || 0,
            y: Number(st.y ?? 0) || 0,
            anchor: (st['text-anchor'] || 'start').toLowerCase(),
            fontSizeUser: fsUser,
            scale,
            matrix,
            family: normFamily(st['font-family']),
            familyChain: st['font-family'] ? String(st['font-family']) : '',
            content: ''
          }
          if (fsUser > 0 && out.unitToMm > 0) {
            const pt = fsUser * scale * out.unitToMm * (PT_PER_IN / MM_PER_IN)
            out.fontSizesPt.push(pt)
          }
          if (st['font-family']) out.fontChains.add(String(st['font-family']))
        } else if (name === 'tspan' && textCtx) {
          // tspan 有自己的 y/x 就是新的一行
          if (st.y !== undefined || st.x !== undefined) {
            const prev = { ...textCtx, content: textCtx.content }
            textCtx.content = ''
            flushText()
            textCtx = {
              ...prev,
              x: Number(st.x ?? prev.x) || prev.x,
              y: Number(st.y ?? prev.y) || prev.y,
              content: ''
            }
            if (st['font-size']) {
              const l = splitLen(st['font-size'])
              const u = l ? toUserUnits(l.value, l.unit, out.unitToMm) : null
              if (u > 0) textCtx.fontSizeUser = u
            }
          }
          if (st['font-family']) {
            textCtx.family = normFamily(st['font-family']) || textCtx.family
            textCtx.familyChain = String(st['font-family'])
          }
        } else if (name === 'rect') {
          const x = Number(st.x ?? 0) || 0
          const y = Number(st.y ?? 0) || 0
          const w = Number(st.width ?? 0) || 0
          const h = Number(st.height ?? 0) || 0
          const bbox = rectBBox(x, y, w, h, matrix)
          out.rects.push({ x: bbox.x, y: bbox.y, w: bbox.w, h: bbox.h, fill: st.fill || '', raw: { x, y, w, h } })
          out.shapes.push({ kind: 'rect', ...bbox })
          if (st.fill) pushColor(st.fill, 'fill')
          if (st.stroke && st.stroke !== 'none') pushColor(st.stroke, 'stroke')
        } else if (name === 'circle' || name === 'ellipse') {
          const cx = Number(st.cx ?? 0) || 0
          const cy = Number(st.cy ?? 0) || 0
          const rx = name === 'circle' ? Number(st.r ?? 0) || 0 : Number(st.rx ?? 0) || 0
          const ry = name === 'circle' ? Number(st.r ?? 0) || 0 : Number(st.ry ?? 0) || 0
          const bbox = rectBBox(cx - rx, cy - ry, rx * 2, ry * 2, matrix)
          out.shapes.push({ kind: name, ...bbox })
          if (st.fill) pushColor(st.fill, 'fill')
          if (st.stroke && st.stroke !== 'none') pushColor(st.stroke, 'stroke')
        } else if (name === 'line') {
          const x1 = Number(st.x1 ?? 0) || 0
          const y1 = Number(st.y1 ?? 0) || 0
          const x2 = Number(st.x2 ?? 0) || 0
          const y2 = Number(st.y2 ?? 0) || 0
          const a = applyMatrix(matrix, x1, y1)
          const b = applyMatrix(matrix, x2, y2)
          out.shapes.push({
            kind: 'line',
            x: Math.min(a[0], b[0]), y: Math.min(a[1], b[1]),
            w: Math.abs(a[0] - b[0]), h: Math.abs(a[1] - b[1])
          })
          if (st.stroke && st.stroke !== 'none') pushColor(st.stroke, 'stroke')
        } else if (name === 'path') {
          const bb = pathBBox(st.d, matrix)
          if (bb) out.shapes.push({ kind: 'path', ...bb })
          if (st.fill) pushColor(st.fill, 'fill')
          if (st.stroke && st.stroke !== 'none') pushColor(st.stroke, 'stroke')
        } else if (name === 'polygon' || name === 'polyline') {
          const nums = (st.points || '').trim().split(/[\s,]+/).map(Number).filter((x) => Number.isFinite(x))
          const pts = []
          for (let i = 0; i + 1 < nums.length; i += 2) pts.push(applyMatrix(matrix, nums[i], nums[i + 1]))
          if (pts.length) {
            out.shapes.push({
              kind: name,
              x: Math.min(...pts.map((p) => p[0])), y: Math.min(...pts.map((p) => p[1])),
              w: Math.max(...pts.map((p) => p[0])) - Math.min(...pts.map((p) => p[0])),
              h: Math.max(...pts.map((p) => p[1])) - Math.min(...pts.map((p) => p[1]))
            })
          }
          if (st.fill) pushColor(st.fill, 'fill')
          if (st.stroke && st.stroke !== 'none') pushColor(st.stroke, 'stroke')
        } else if (name === 'image') {
          const x = Number(st.x ?? 0) || 0
          const y = Number(st.y ?? 0) || 0
          const wRaw = st.width
          const hRaw = st.height
          const wu = wRaw !== undefined ? toUserUnits(splitLen(wRaw)?.value ?? 0, splitLen(wRaw)?.unit, out.unitToMm) : null
          const hu = hRaw !== undefined ? toUserUnits(splitLen(hRaw)?.value ?? 0, splitLen(hRaw)?.unit, out.unitToMm) : null
          const bbox = rectBBox(x, y, wu ?? 0, hu ?? 0, matrix)
          out.images.push({ ...bbox, href: st.href || st['xlink:href'] || '' })
        }
      }

      if (!t.selfClose) stack.push({ name, matrix: prevMatrix })
      if (t.selfClose) matrix = prevMatrix
      continue
    }

    if (t.type === 'close') {
      const name = t.name
      if (name === 'defs' || name === 'symbol' || name === 'clippath' || name === 'mask' || name === 'marker' || name === 'pattern') {
        if (skippedDepth > 0) skippedDepth--
        continue
      }
      if (name === 'text' && textCtx) flushText()
      const top = stack.pop()
      if (top) matrix = top.matrix
      else matrix = IDENTITY.slice()
    }
  }
  flushText()

  out.texts = textSegs
  // CSS 里声明的字号也算进来（有些渲染器把字号放 <style> 里）
  for (const raw of css.allFontSizes) {
    const l = splitLen(String(raw).trim())
    if (!l) continue
    const u = toUserUnits(l.value, l.unit, out.unitToMm)
    if (u > 0) out.fontSizesPt.push(u * out.unitToMm * (PT_PER_IN / MM_PER_IN))
  }
  for (const raw of css.allFontFamilies) {
    const f = normFamily(raw)
    if (f) out.fontFamilies.add(f)
    if (raw) out.fontChains.add(String(raw))
  }
  return out
}

function rectBBox(x, y, w, h, m) {
  const pts = [applyMatrix(m, x, y), applyMatrix(m, x + w, y), applyMatrix(m, x, y + h), applyMatrix(m, x + w, y + h)]
  const xs = pts.map((p) => p[0])
  const ys = pts.map((p) => p[1])
  return {
    x: Math.min(...xs), y: Math.min(...ys),
    w: Math.max(...xs) - Math.min(...xs), h: Math.max(...ys) - Math.min(...ys)
  }
}

/** 路径 bbox：解析 M/L/H/V/C/S/Q/T/A/Z 的绝对/相对坐标（够用就行） */
function pathBBox(d, m) {
  if (!d) return null
  const toks = String(d).match(/[a-zA-Z]|-?\d*\.?\d+(?:e[-+]?\d+)?/g)
  if (!toks) return null
  let i = 0
  let cmd = 'M'
  let cx = 0
  let cy = 0
  let sx = 0
  let sy = 0
  const pts = []
  const num = () => Number(toks[i++])
  const push = (x, y) => { pts.push(applyMatrix(m, x, y)) }
  while (i < toks.length) {
    if (/^[a-zA-Z]$/.test(toks[i])) { cmd = toks[i]; i++ }
    const rel = cmd === cmd.toLowerCase()
    const C = cmd.toUpperCase()
    if (C === 'Z') { cx = sx; cy = sy; continue }
    if (C === 'M' || C === 'L') {
      const x = num(); const y = num()
      cx = rel ? cx + x : x; cy = rel ? cy + y : y
      if (C === 'M') { sx = cx; sy = cy }
      push(cx, cy)
    } else if (C === 'H') { const x = num(); cx = rel ? cx + x : x; push(cx, cy) }
    else if (C === 'V') { const y = num(); cy = rel ? cy + y : y; push(cx, cy) }
    else if (C === 'C') {
      const x1 = num(); const y1 = num(); const x2 = num(); const y2 = num(); const x = num(); const y = num()
      push(rel ? cx + x1 : x1, rel ? cy + y1 : y1)
      push(rel ? cx + x2 : x2, rel ? cy + y2 : y2)
      cx = rel ? cx + x : x; cy = rel ? cy + y : y; push(cx, cy)
    } else if (C === 'S' || C === 'Q') {
      const x1 = num(); const y1 = num(); const x = num(); const y = num()
      push(rel ? cx + x1 : x1, rel ? cy + y1 : y1)
      cx = rel ? cx + x : x; cy = rel ? cy + y : y; push(cx, cy)
    } else if (C === 'T') {
      const x = num(); const y = num()
      cx = rel ? cx + x : x; cy = rel ? cy + y : y; push(cx, cy)
    } else if (C === 'A') {
      num(); num(); num(); num(); num()
      const x = num(); const y = num()
      cx = rel ? cx + x : x; cy = rel ? cy + y : y; push(cx, cy)
    } else {
      i++ // 不认识的命令，跳过一个 token 防止死循环
    }
  }
  if (!pts.length) return null
  const xs = pts.map((p) => p[0])
  const ys = pts.map((p) => p[1])
  return {
    x: Math.min(...xs), y: Math.min(...ys),
    w: Math.max(...xs) - Math.min(...xs), h: Math.max(...ys) - Math.min(...ys)
  }
}

/** 字体族名归一：去掉引号/回退链，只留第一个 */
function normFamily(raw) {
  if (!raw) return ''
  const first = String(raw).split(',')[0].trim().replace(/^["']|["']$/g, '')
  return first
}

/**
 * 文字宽度估算（单位 em）。
 * 只求「够用」：中文字 = 1em；西文按字宽分档；宁可略高估，少报漏报。
 */
function estimateTextWidthEm(str) {
  let w = 0
  for (const ch of String(str)) {
    const code = ch.codePointAt(0)
    if (code >= 0x2e80 && code <= 0x9fff) { w += 1.0; continue }     // 中日韩
    if (code >= 0xac00 && code <= 0xd7af) { w += 1.0; continue }     // 韩文
    if (code >= 0xf900 && code <= 0xfaff) { w += 1.0; continue }
    if (code >= 0xff00 && code <= 0xffef) { w += 1.0; continue }     // 全角标点
    if (code >= 0x3000 && code <= 0x303f) { w += 1.0; continue }
    if (ch === ' ') { w += 0.28; continue }
    if ('iljtfrI.,;:!|`\'"()[]{}'.includes(ch)) { w += 0.33; continue }
    if ('mwMW'.includes(ch)) { w += 0.85; continue }
    if (/[A-Z]/.test(ch)) { w += 0.66; continue }
    if (/[0-9]/.test(ch)) { w += 0.56; continue }
    if (/[a-z]/.test(ch)) { w += 0.53; continue }
    w += 0.6
  }
  return w
}

/* ==========================================================================
 * 四、颜色：红绿判定 & 色盲风险
 * ========================================================================== */

function hexToHsl(hex) {
  const h = hex.replace('#', '')
  if (h.length !== 6) return null
  const r = parseInt(h.slice(0, 2), 16) / 255
  const g = parseInt(h.slice(2, 4), 16) / 255
  const b = parseInt(h.slice(4, 6), 16) / 255
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  const l = (max + min) / 2
  const d = max - min
  let s = 0
  if (d !== 0) s = d / (1 - Math.abs(2 * l - 1))
  let hue = 0
  if (d !== 0) {
    if (max === r) hue = ((g - b) / d) % 6
    else if (max === g) hue = (b - r) / d + 2
    else hue = (r - g) / d + 4
    hue *= 60
    if (hue < 0) hue += 360
  }
  return { h: hue, s, l }
}

const isRedish = ({ h, s, l }) => s > 0.35 && l > 0.12 && l < 0.88 && (h >= 340 || h <= 20)
const isGreenish = ({ h, s, l }) => s > 0.28 && l > 0.10 && l < 0.88 && h >= 75 && h <= 170

/* ==========================================================================
 * 五、位图尺寸（PNG / JPEG / GIF 头解析，用来算实际 DPI）
 * ========================================================================== */

function pngDims(buf) {
  if (!buf || buf.length < 24) return null
  if (buf[0] !== 0x89 || buf[1] !== 0x50 || buf[2] !== 0x4e || buf[3] !== 0x47) return null
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) }
}

function jpegDims(buf) {
  if (!buf || buf.length < 4 || buf[0] !== 0xff || buf[1] !== 0xd8) return null
  let i = 2
  while (i < buf.length - 9) {
    if (buf[i] !== 0xff) { i++; continue }
    const marker = buf[i + 1]
    const len = buf.readUInt16BE(i + 2)
    if (marker >= 0xc0 && marker <= 0xcf && marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc) {
      return { h: buf.readUInt16BE(i + 5), w: buf.readUInt16BE(i + 7) }
    }
    i += 2 + len
  }
  return null
}

function gifDims(buf) {
  if (!buf || buf.length < 10) return null
  if (buf.toString('ascii', 0, 3) !== 'GIF') return null
  return { w: buf.readUInt16LE(6), h: buf.readUInt16LE(8) }
}

function imageDims(buf) {
  return pngDims(buf) || jpegDims(buf) || gifDims(buf)
}

/** 从 data URI 或文件取图片像素尺寸；取不到返回 null（不报错） */
function readImageDims(href, workDir) {
  try {
    if (!href) return null
    if (href.startsWith('data:')) {
      const base64 = href.slice(href.indexOf(',') + 1)
      const buf = Buffer.from(base64, 'base64')
      return imageDims(buf)
    }
    let p = decodeURIComponent(href.replace(/^file:\/\//, ''))
    if (!isAbsolute(p)) p = resolve(workDir, p)
    if (!exists(p)) return null
    if (statSync(p).size > 30 * 1024 * 1024) return null
    return imageDims(readFileSync(p))
  } catch {
    return null
  }
}

/* ==========================================================================
 * 六、期刊预置加载（优先 render-core 的 journal.mjs，失败用兜底表）
 * ========================================================================== */

let presetCache = null

async function loadPresetModule() {
  if (presetCache !== null) return presetCache
  presetCache = { mod: null, error: '' }
  try {
    const mod = await import(pathToFileURL(join(HERE, 'lib', 'journal.mjs')).href)
    if (typeof mod.getPreset === 'function') presetCache = { mod, error: '' }
    else presetCache = { mod: null, error: 'lib/journal.mjs 里没有 getPreset' }
  } catch (e) {
    presetCache = { mod: null, error: e && e.message ? e.message : String(e) }
  }
  return presetCache
}

async function loadPaletteModule() {
  try {
    const mod = await import(pathToFileURL(join(HERE, 'lib', 'palette.mjs')).href)
    if (typeof mod.getPalette === 'function') return { getPalette: mod.getPalette }
  } catch { /* render-core 还没写好，用兜底 */ }
  return { getPalette: (id) => FALLBACK_PALETTES[id] || null }
}

/**
 * 取期刊预置。三档来源，优先级严格：
 *   1) scripts/lib/journal.mjs 的 getPreset(id)  ← 正常路径，唯一真相源
 *   2) assets/journals.json 直接读（journal.mjs 坏了但数据还在时）
 *   3) 本文件里的 FALLBACK_JOURNALS（连同数据文件都没了，只在安装被破坏时发生）
 * 只要不是第 1 档，就标记出来并告警 —— 绝不能让「读不到预置」变成静默放宽判定。
 *
 * @returns {{ preset, source:'journal.mjs'|'journals.json'|'fallback', fromFallback:boolean, error:string }}
 */
export async function resolvePreset(journalId) {
  const id = String(journalId || 'custom').toLowerCase()
  const { mod, error } = await loadPresetModule()

  if (mod) {
    try {
      const p = mod.getPreset(id)
      if (p && typeof p === 'object' && Number(p.single_mm) > 0) {
        return { preset: normalizePreset(p, id), source: 'journal.mjs', fromFallback: false, error: '' }
      }
    } catch (e) {
      // journal.mjs 自己有 bug，落到下一档，但把原因留住
      return loadPresetFromJson(id, String((e && e.message) || e))
    }
  }
  return loadPresetFromJson(id, error)
}

/** 第二档：直接读 assets/journals.json（数据文件在，模块没起来） */
function loadPresetFromJson(id, upstreamError = '') {
  try {
    const p = join(HERE, '..', 'assets', 'journals.json')
    if (existsSync(p)) {
      const raw = JSON.parse(readFileSync(p, 'utf8'))
      const list = Array.isArray(raw) ? raw : (raw.journals || [])
      const found = list.find((x) => {
        if (!x || !x.id) return false
        if (String(x.id).toLowerCase() === id) return true
        return Array.isArray(x.aliases) && x.aliases.some((a) => String(a).toLowerCase() === id)
      })
      if (found) {
        return {
          preset: normalizePreset(found, id),
          source: 'journals.json',
          fromFallback: true,
          error: upstreamError
        }
      }
    }
  } catch { /* 落到第三档 */ }

  // 第三档：硬编码兜底。数值与 journals.json 同源核对过，但仍是最后手段。
  const hard = FALLBACK_JOURNALS[id]
  return {
    preset: normalizePreset(hard || FALLBACK_JOURNALS.custom, id),
    source: hard ? 'fallback' : 'fallback',
    fromFallback: true,
    error: upstreamError || 'assets/journals.json 也读不到'
  }
}

function normalizePreset(p, id) {
  const base = FALLBACK_JOURNALS[id] || FALLBACK_JOURNALS.custom
  const formats = Array.isArray(p.formats) && p.formats.length ? p.formats : base.formats
  return {
    id: p.id || id,
    label: p.label || base.label,
    single_mm: Number(p.single_mm) || base.single_mm,
    double_mm: Number(p.double_mm) || base.double_mm,
    max_height_mm: Number(p.max_height_mm) || base.max_height_mm,
    min_font_pt: Number(p.min_font_pt) || base.min_font_pt,
    max_font_pt: Number(p.max_font_pt) || parseMaxFontPt(p) || null,
    // dpi 显式为 null = 这个刊主图不收位图，dpi 无意义（Nature 这种）。
    // 用 || 会把 null 吞成兜底的 600，导致判定口径和 journals.json 不一致。
    dpi: p.dpi === null ? null : (Number(p.dpi) || base.dpi),
    formats: formats.map((f) => String(f).toLowerCase()),
    // 「主图只收矢量」：接受格式里一个位图都没有（Nature / ACM 这种）
    vector_only: formats.length > 0 && !formats.some((f) => RASTER_EXTS.includes(String(f).toLowerCase())),
    fonts: Array.isArray(p.fonts) && p.fonts.length ? p.fonts : base.fonts,
    color_mode: p.color_mode || base.color_mode,
    notes: p.notes || base.notes,
    source: p.source || (base.source || '')
  }
}

/**
 * 字号上限：预置里没有 max_font_pt 时，从 notes 的「5–7pt」这类区间里抠出来。
 * 抠不到就是没有上限（不硬编），宁可少报也不许乱报。
 */
function parseMaxFontPt(preset) {
  if (!preset) return null
  if (Number.isFinite(Number(preset.max_font_pt))) return Number(preset.max_font_pt)
  const text = `${preset.notes || ''} ${preset.verified_note || ''}`
  const m = text.match(/(\d+(?:\.\d+)?)\s*[–—~\-]\s*(\d+(?:\.\d+)?)\s*pt/i)
  if (m) {
    const hi = Number(m[2])
    if (Number.isFinite(hi) && hi > 0) return hi
  }
  return null
}

/* ==========================================================================
 * 七、找产物文件
 * ========================================================================== */

function pickSvg(workDir, spec, opts) {
  if (opts.svgPath) {
    const p = isAbsolute(opts.svgPath) ? opts.svgPath : resolve(workDir, opts.svgPath)
    return exists(p) ? p : null
  }
  const outDir = join(workDir, 'out')
  const files = listDir(outDir).filter((f) => f.toLowerCase().endsWith('.svg'))
  if (!files.length) return null
  const name = spec && typeof spec.name === 'string' ? spec.name : ''
  if (name && files.includes(`${name}.svg`)) return join(outDir, `${name}.svg`)
  // 多个 SVG 时取最新的那个
  let best = null
  for (const f of files) {
    const p = join(outDir, f)
    try {
      const m = statSync(p).mtimeMs
      if (!best || m > best.m) best = { p, m }
    } catch { /* ignore */ }
  }
  return best ? best.p : null
}

/* ==========================================================================
 * 八、主函数
 * ========================================================================== */

/**
 * 确定性合规检查。
 * @param {string} workDir 工作区目录（含 figure.json / out/）
 * @param {object} opts
 *   - journal  覆盖 figure.json 里的期刊 id
 *   - dpi      覆盖 figure.json 里的 dpi（比如你打算按 export --dpi 600 交稿）
 *   - svgPath  指定要检查的 SVG
 *   - toleranceMm 尺寸容忍度（默认 0.8mm，缺省好看一点）
 *   - write    是否写 out/check.json（默认 true）
 */
export async function checkFigure(workDir, opts = {}) {
  const wd = absDir(workDir)
  const issues = []
  const add = (level, code, message, fix) => issues.push({ level, code, message, fix })

  const spec = readJsonSafe(join(wd, 'figure.json'))
  const specMissing = !spec
  if (specMissing) {
    add('error', 'NO_SPEC', '这个工作区里没有 figure.json —— 检查器不知道你要投哪本刊、图多宽、字号多少。',
      '先跑 `node scripts/fig.mjs init <dir>` 建工作区，或手写一个 figure.json（字段见 BRIEF 5.2）。')
  }

  const journalId = String(opts.journal || (spec && spec.journal) || 'custom').toLowerCase()
  const { preset, source: presetSource, error: presetError } = await resolvePreset(journalId)
  const fromFallback = presetSource !== 'journal.mjs'

  if (fromFallback) {
    // 正常路径永远是 journal.mjs。落到这里说明安装被破坏了。
    // 必须显式告警：预置读不到时最危险的失败模式是「判定静默放宽」，用户以为合规、投出去被退。
    add('warn', 'CHECK_PRESET_FALLBACK',
      `预置表未就绪（当前用的是 ${presetSource === 'journals.json' ? 'assets/journals.json' : '内置硬编码表'}），本次判定按保守兜底执行，数字可能与期刊当期要求有出入${presetError ? `；原因：${presetError}` : ''}。`,
      '先修安装：确认 scripts/lib/journal.mjs 和 assets/journals.json 都在（重新拷一份完整包即可），然后重跑 check 再交稿。别拿这次结果当最终合规依据。')
  } else if (preset.id !== journalId) {
    add('warn', 'UNKNOWN_JOURNAL', `没有「${journalId}」这个期刊预置，已按通用值（${preset.label}）检查。`,
      `用 --journal 指定已支持的期刊；可用值：nature / science / cell / ieee / elsevier / springer / acm / plos / thesis-cn / custom。`)
  }

  const svgPath = pickSvg(wd, spec, opts)
  let svg = null
  if (!svgPath) {
    add('error', 'NO_SVG', 'out/ 里没找到 SVG —— 检查器没有图可查（大概率还没 render/chart）。',
      '先跑 `node scripts/fig.mjs render <dir>` 或 `chart <dir>` 生成 out/<name>.svg，再 check。')
  } else {
    try {
      svg = parseSvg(readFileSync(svgPath, 'utf8'))
    } catch (e) {
      add('error', 'SVG_PARSE_FAILED', `SVG 读不出来或格式坏了：${e && e.message ? e.message : e}`,
        '用浏览器打开这个 SVG 看看能不能正常显示；重跑 render 覆盖它。')
    }
  }

  /* ---------------- ① 物理尺寸 ---------------- */
  const widthMode = (spec && spec.width) || 'single'
  const targetWidthMm = widthMode === 'double' ? preset.double_mm : preset.single_mm
  let actualWidthMm = svg ? svg.widthMm : null
  let actualHeightMm = svg ? svg.heightMm : null

  if (svg && (!actualWidthMm || !actualHeightMm)) {
    add('warn', 'SVG_NO_PHYSICAL_SIZE',
      'SVG 根元素没写以 mm 为单位的 width/height（只有 viewBox），排版软件插入时可能按像素算，尺寸会跑偏。',
      '让 render 输出 `width="89mm" height="60mm" viewBox="..."`，这样期刊排版系统才能按 mm 摆放。')
  }

  // 没 SVG 时退回 figure.json 声明值，让尺寸检查仍能给意见
  if (actualWidthMm == null && spec) {
    actualWidthMm = Number(spec.width_mm) || targetWidthMm
  }
  if (actualHeightMm == null && spec) {
    actualHeightMm = Number(spec.height_mm) || null
  }

  const tol = Number(opts.toleranceMm ?? 0.8)

  if (actualWidthMm) {
    if (actualWidthMm > targetWidthMm + tol) {
      add('error', 'FIG_WIDTH_TOO_WIDE',
        `图宽 ${round(actualWidthMm)}mm，超过 ${preset.label} 的${widthMode === 'double' ? '双' : '单'}栏宽 ${targetWidthMm}mm（多出 ${round(actualWidthMm - targetWidthMm)}mm）。排版时要么被整体缩小（字号跟着变 4pt），要么压到正文里。`,
        `把画布收到 ${targetWidthMm}mm：改 figure.json 的 width（single=${preset.single_mm}mm / double=${preset.double_mm}mm）后重跑 render；如果内容太挤，拆成两栏摆放或减少一列。`)
    } else if (actualWidthMm < targetWidthMm * 0.6) {
      add('warn', 'FIG_WIDTH_TOO_NARROW',
        `图宽只有 ${round(actualWidthMm)}mm，占 ${preset.label} ${widthMode === 'double' ? '双' : '单'}栏宽（${targetWidthMm}mm）的 ${Math.round((actualWidthMm / targetWidthMm) * 100)}%，两边会留大片空白，视觉上比正文小一号。`,
        `把宽度拉到 ${targetWidthMm}mm（figure.json 的 width），或者干脆按更窄的单栏 ${preset.single_mm}mm 排，别卡在中间。`)
    }
    if (spec && Number(spec.width_mm) > 0 && Math.abs(Number(spec.width_mm) - actualWidthMm) > 1.5) {
      add('warn', 'FIG_SIZE_DECLARED_MISMATCH',
        `figure.json 说宽 ${round(Number(spec.width_mm))}mm，实际 SVG 是 ${round(actualWidthMm)}mm —— 不致命，但下次 render 会按 json 里的数走。`,
        '改 figure.json 里的 width_mm 与实际一致，或重新 render 让两者对齐。')
    }
  }

  if (actualHeightMm && preset.max_height_mm && actualHeightMm > preset.max_height_mm + tol) {
    add('error', 'FIG_HEIGHT_TOO_TALL',
      `图高 ${round(actualHeightMm)}mm，超过 ${preset.label} 单页上限 ${preset.max_height_mm}mm。期刊会缩到能放进一页，字号和线宽一起被压瘪。`,
      `减高度：figure.json 的 height_mm 调到 ≤${preset.max_height_mm}；内容多就拆成两张图（主图 + 补充材料）。`)
  }

  /* ---------------- ② 字号 ---------------- */
  if (svg) {
    const sizes = svg.fontSizesPt.filter((x) => Number.isFinite(x) && x > 0)
    if (sizes.length) {
      const minPt = Math.min(...sizes)
      const maxPt = Math.max(...sizes)
      if (minPt < preset.min_font_pt - 0.05) {
        const tooSmall = svg.texts.filter((t) => {
          const pt = t.fontSizeUser * svg.unitToMm * (PT_PER_IN / MM_PER_IN)
          return pt < preset.min_font_pt - 0.05
        })
        const sample = tooSmall.slice(0, 3).map((t) => `「${t.content.slice(0, 14)}」`).join('、')
        add('error', 'FONT_SIZE_BELOW_MIN',
          `图里最小字号 ${round(minPt)}pt，低于 ${preset.label} 要求的 ${preset.min_font_pt}pt${sample ? `；涉及 ${tooSmall.length} 处文字，例如 ${sample}` : ''}。缩到 5pt 以下的字，印刷后基本看不清。`,
          `把 figure.json 的 font_size_pt 提到 ≥${preset.min_font_pt}（建议 ${preset.min_font_pt + 1}pt 留余量）后重跑 render；如果提字号后放不下，就先减文字量或加宽到双栏。`)
      }
      if (preset.max_font_pt && maxPt > preset.max_font_pt + 0.05) {
        add('warn', 'FONT_SIZE_ABOVE_MAX',
          `图里最大字号 ${round(maxPt)}pt，超过 ${preset.label} 的上限 ${preset.max_font_pt}pt。字太大一样不合规：期刊要的是「图和正文一个体量」，图注字号也是 7pt 左右。`,
          `把 figure.json 的 font_size_pt 调到 ${preset.min_font_pt}–${preset.max_font_pt}pt 之间（${preset.label} 官方口径是 ${preset.min_font_pt}–${preset.max_font_pt}pt），重跑 render。`)
      }
      if (sizes.length > 1 && maxPt / Math.max(minPt, 0.1) > 2.2) {
        add('warn', 'FONT_SIZE_INCONSISTENT',
          `图内字号从 ${round(minPt)}pt 到 ${round(maxPt)}pt，差 ${round(maxPt / Math.max(minPt, 0.1))} 倍 —— 看起来像拼贴，不像一张图。`,
          '把字号收敛到 2 档（标题 / 正文）以内，通常正文 pt、标题 pt×1.5。')
      }
    }
  }

  /* ---------------- ③ 文字溢出 ---------------- */
  if (svg && svg.viewBox) {
    const vb = svg.viewBox
    const vbRight = vb.x + vb.w
    const vbBottom = vb.y + vb.h
    const slack = vb.w * 0.004 // 4‰ 容差，避免小数点误差天天报警

    const slackY = vb.h * 0.004
    for (const t of svg.texts) {
      // 四边都要看：横排文字常溢出左右，竖排/坐标轴标签常溢出上下（y 坐标没写对就全挤在边上）
      const overflowRight = t.x + t.w - vbRight
      const overflowLeft = vb.x - t.x
      const overflowBottom = t.y + t.h - vbBottom
      const overflowTop = vb.y - t.y
      const worst = Math.max(overflowRight, overflowLeft, overflowBottom, overflowTop)
      const tol = Math.max(overflowRight, overflowLeft, overflowBottom, overflowTop) === Math.max(overflowRight, overflowLeft) ? slack : slackY
      if (worst > tol) {
        const dir = worst === overflowRight ? '右侧' : worst === overflowLeft ? '左侧' : worst === overflowBottom ? '下方' : '上方'
        const axis = dir === '右侧' || dir === '左侧' ? '宽' : '高'
        add('error', 'TEXT_OVERFLOW_CANVAS',
          `文字「${t.content.slice(0, 16)}」超出画布${dir} ${round(worst * svg.unitToMm)}mm —— 导出后这半截字会被裁掉。`,
          `把画布加${axis} ${round(worst * svg.unitToMm, 0)}mm 以上（figure.json 的 ${axis === '宽' ? 'width 改 double' : 'height_mm 调大'}），或缩短这段文字 / 调小字号 / 挪动位置；如果这段是坐标轴标签，先确认它的 x/y 坐标真写上了（渲染器漏写 y 时标签会全挤到画布边上）。`)
        break // 同类问题报一条就够，别刷屏
      }
    }

    // 父容器溢出：找最小的、包含文字锚点的 rect。
    // 先排除「背景板」——整幅画布的底色矩形（面积 ≥85% 画布，或白色填充），否则每段自由文字
    // 都会认这张背景当父容器，报出一堆假警。
    const canvasArea = vb.w * vb.h
    const isBackgroundRect = (r) => {
      if (canvasArea > 0 && r.w * r.h >= canvasArea * 0.85) return true
      const f = String(r.fill || '').trim().toLowerCase()
      if (!f || f === 'none' || f === 'transparent') return false
      const hex = NAMED_COLORS[f] || (f.startsWith('#') ? f : '')
      const hsl = hex ? hexToHsl(hex.length === 4 ? '#' + f[1] + f[1] + f[2] + f[2] + f[3] + f[3] : hex) : null
      return Boolean(hsl && hsl.l >= 0.95) // 近似纯白 = 底色
    }

    let parentHits = 0
    for (const t of svg.texts) {
      const [ax, ay] = t.anchorPoint
      let best = null
      for (const r of svg.rects) {
        if (r.w <= 0 || r.h <= 0) continue
        if (isBackgroundRect(r)) continue
        if (ax >= r.x && ax <= r.x + r.w && ay >= r.y && ay <= r.y + r.h) {
          if (!best || r.w * r.h < best.w * best.h) best = r
        }
      }
      if (!best) continue
      const pad = Math.max(0.4, 0.3 / Math.max(svg.unitToMm, 1e-6)) // 0.3mm 内边距
      const overRight = t.x + t.w - (best.x + best.w - pad)
      const overLeft = best.x + pad - t.x
      if (overRight > pad || overLeft > pad) {
        add('error', 'TEXT_OVERFLOW_PARENT',
          `文字「${t.content.slice(0, 16)}」比它所在的框宽：估宽 ${round(t.w * svg.unitToMm)}mm，可用 ${round((best.w - pad * 2) * svg.unitToMm)}mm，${overRight > overLeft ? '右边' : '左边'}顶出去了 —— 渲染出来是压在框线上或盖住隔壁节点。`,
          `把节点宽度调大（figure.json 的 layout.node_w_mm）或把这段标签改短/换行；也可以在节点里用副标题分行（node.label + node.sub）。`)
        parentHits++
        if (parentHits >= 3) break
      }
    }

    /* ---------------- ⑦ 元素越界 ---------------- */
    const outside = []
    for (const s of svg.shapes) {
      if (s.w === 0 && s.h === 0) continue
      const eps = vb.w * 0.01
      if (s.x + s.w < vb.x - eps || s.x > vbRight + eps || s.y + s.h < vb.y - eps || s.y > vbBottom + eps) {
        outside.push(s)
      }
    }
    if (outside.length) {
      const s0 = outside[0]
      add('error', 'ELEMENT_OUT_OF_CANVAS',
        `有 ${outside.length} 个图形元素整块跑到画布外（例如 ${s0.kind} 在 x=${round(s0.x * svg.unitToMm)}mm、y=${round(s0.y * svg.unitToMm)}mm，画布只有 ${round(vb.w * svg.unitToMm)}×${round(vb.h * svg.unitToMm)}mm）。导出后它们直接消失，看图的人会以为少画了东西。`,
        '检查版面坐标：八成是节点数超过一行宽度导致换行错位，或组内 translate 叠加了两遍；跑 render 后拿浏览器打开 SVG 对照一下。')
    }
  }

  /* ---------------- ④ DPI ---------------- */
  const declaredDpi = Number(opts.dpi || (spec && spec.dpi) || 0)
  if (preset.vector_only) {
    // Nature / ACM 这类：主图只收 .ai/.eps/.pdf（Nature 另收分层 PSD 与 plain SVG），
    // 位图只能放 Extended Data —— 所以「主图多少 dpi」这个问题本身不适用，别拿 dpi 去卡用户。
    // 真正该提醒的是「你交的是不是位图」（见下方 RASTER_FORMAT 检查）。
  } else if (!declaredDpi) {
    add('warn', 'DPI_UNDECLARED', 'figure.json 里没写 dpi，检查器无法确认导出够不够清晰。',
      `在 figure.json 里写 "dpi": ${preset.dpi}，或导出时显式 --dpi ${preset.dpi}。`)
  } else if (declaredDpi < preset.dpi) {
    add('error', 'DPI_BELOW_MIN',
      `导出 DPI 是 ${declaredDpi}，低于 ${preset.label} 要求的 ${preset.dpi}。位图位不够，印刷出来是糊的、斜线有锯齿。`,
      `把 figure.json 的 dpi 改成 ${preset.dpi}（或更高），然后跑 \`node scripts/fig.mjs export <dir> --dpi ${preset.dpi}\`。矢量 PDF/EPS 不受这条限制，但审稿系统常要 TIFF/PNG。`)
  }

  // 内嵌位图的实际有效 DPI
  if (svg && svg.images.length) {
    let rasterBad = 0
    for (const img of svg.images) {
      const dims = readImageDims(img.href, wd)
      if (!dims) continue
      const wMm = img.w * svg.unitToMm
      if (!(wMm > 0)) continue
      const effDpi = dims.w / (wMm / MM_PER_IN)
      if (effDpi < preset.dpi - 1) {
        add('error', 'RASTER_DPI_LOW',
          `图里内嵌了一张 ${dims.w}×${dims.h}px 的位图，摆在 ${round(wMm)}mm 宽的位置，实际只有 ${Math.round(effDpi)}dpi（要 ${preset.dpi}dpi）—— 放大了，糊。`,
          `换更高的原图，或者把这张元素改成矢量（用 rect/line/path 画）；只做概念示意的话，接受模糊就别把它放进要投的数据图里。`)
        rasterBad++
        if (rasterBad >= 2) break
      }
    }
  }

  // 交付格式：矢量优先的刊，主图收的是 .ai/.eps/.pdf，交 PNG/TIFF 会被要求重投
  {
    const outFilesAll = listDir(join(wd, 'out'))
    const extOf = (f) => String(f).toLowerCase().split('.').pop()
    const deliveredRaster = outFilesAll.filter((f) => RASTER_EXTS.includes(extOf(f)) && !/^concept-/i.test(f))
    const deliveredVector = outFilesAll.filter((f) => VECTOR_EXTS.includes(extOf(f)) && !/\.svg$/i.test(f))
    const acceptsRaster = (preset.formats || []).some((f) => RASTER_EXTS.includes(String(f).toLowerCase()))
    if (!acceptsRaster && deliveredRaster.length && !deliveredVector.length) {
      add('warn', 'RASTER_FORMAT_NOT_ACCEPTED_FOR_VECTOR_JOURNAL',
        `${preset.label} 的主图只收矢量（${(preset.formats || []).join(' / ')}），但 out/ 里现在只有位图（${deliveredRaster.slice(0, 2).join('、')}）—— 交上去大概率被要求重投；位图只能用在这个刊的 Extended Data / 补充材料里。`,
        `导出 PDF：\`node scripts/fig.mjs export <dir> --formats pdf\`（矢量、字保留，Nature 首选）；投稿时主图交 ${preset.formats.join('/')}，PNG/TIFF 留给 Extended Data。`)
    }
  }

  // 已经导出的 PNG 实际够不够 dpi（防止"文件名写着 600dpi、实际 150"）
  if (actualWidthMm && !preset.vector_only) {
    const outDir = join(wd, 'out')
    const pngs = listDir(outDir).filter((f) => /\.png$/i.test(f) && !f.startsWith('concept-'))
    for (const f of pngs) {
      const p = join(outDir, f)
      const dims = (() => {
        try { return pngDims(readFileSync(p)) } catch { return null }
      })()
      if (!dims || !dims.w) continue
      const effDpi = dims.w / (actualWidthMm / MM_PER_IN)
      const want = Number(opts.dpi || preset.dpi)
      if (effDpi < want * 0.98) {
        add('error', 'EXPORTED_PNG_DPI_LOW',
          `导出的 ${f} 实际是 ${dims.w}×${dims.h}px，摆在 ${round(actualWidthMm)}mm 宽的位置只有 ${Math.round(effDpi)}dpi，达不到 ${want}dpi —— 文件名字骗人，投稿系统会退回。`,
          `重新导出：\`node scripts/fig.mjs export <dir> --dpi ${want}\`（像素数会按 mm×dpi/25.4 重算）。`)
        break
      }
    }
  }

  /* ---------------- ⑤ 色盲 / 红绿 ---------------- */
  const paletteId = (spec && spec.palette) || ''
  const { getPalette } = await loadPaletteModule()
  let palette = null
  try { palette = getPalette(paletteId) } catch { palette = null }
  if (!palette) palette = (FALLBACK_PALETTES && FALLBACK_PALETTES[paletteId]) || null

  if (svg) {
    const hslColors = []
    for (const [hex, meta] of svg.colors) {
      const hsl = hexToHsl(hex)
      if (!hsl) continue
      if (hsl.l < 0.06 || hsl.l > 0.95) continue // 纯黑/纯白不算
      if (hsl.s < 0.12) continue                // 灰阶不算
      hslColors.push({ hex, hsl, ...meta })
    }
    const reds = hslColors.filter((c) => isRedish(c.hsl))
    const greens = hslColors.filter((c) => isGreenish(c.hsl))
    if (reds.length && greens.length) {
      const safe = palette && (palette.colorblind_safe === true || palette.grayscale_ok === true)
      const minLumaGap = Math.min(...reds.flatMap((r) => greens.map((g) => Math.abs(r.hsl.l - g.hsl.l))))
      if (!safe) {
        add('error', 'COLORBLIND_RED_GREEN',
          `同一张图里同时用了红（${reds.map((c) => c.hex).slice(0, 2).join('/')}）和绿（${greens.map((c) => c.hex).slice(0, 2).join('/')}）${palette ? `，调色板「${palette.label}」没有色盲安全兜底` : '，且没指定色盲安全调色板'}。约 8% 的男性红绿色盲会把这两类看成同一个颜色 —— 图里的对比就消失了。`,
          `换调色板：figure.json 里把 palette 改成 okabe-ito（色盲安全）后重跑 render；或者改用「色相 + 形状/线型」双重编码（比如实线圆点 vs 虚线方块）。`)
      }
      if (minLumaGap < 0.12) {
        add('warn', 'COLORBLIND_LOW_LUMA_DIFF',
          `图里的红和绿明度差只有 ${round(minLumaGap, 2)}（<0.12），连打印成黑白、或色盲用户看，都分不出来。`,
          '把其中一类的明度拉开（浅红配深绿），或改用纹理/虚线/直接标注文字区分。')
      }
    }
    // 颜色太多也提醒一句
    if (hslColors.length > 8) {
      add('warn', 'TOO_MANY_COLORS',
        `图里出现 ${hslColors.length} 种非灰阶颜色，读者要对照图例逐个认，认知负担偏高。`,
        '数据结构复杂时，用「主色 + 深浅」代替多种色相（palette 换 nature-cool），或者把次要类别合并成 Other。')
    }
  }

  /* ---------------- ⑥ 字体 ---------------- */
  if (svg) {
    const families = new Set(svg.fontFamilies)
    if (spec && spec.font) families.add(normFamily(spec.font))
    const acceptedRaw = preset.fonts || []
    const accepted = acceptedRaw.map((f) => f.toLowerCase())
    for (const fam of families) {
      if (!fam) continue
      const low = fam.toLowerCase()
      if (DECORATIVE_FONTS.some((d) => low.includes(d))) {
        add('error', 'FONT_DECORATIVE',
          `用了「${fam}」这种装饰字体 —— 期刊基本一律退。`,
          `换成 ${acceptedRaw.slice(0, 2).join(' 或 ') || 'Arial / Helvetica'}（figure.json 的 font 字段），重跑 render。`)
        continue
      }
      if (accepted.length && !accepted.some((a) => low === a || low.includes(a) || a.includes(low))) {
        add('warn', 'FONT_NOT_ACCEPTED',
          `字体「${fam}」不在 ${preset.label} 的常见接受清单里（${acceptedRaw.slice(0, 4).join(' / ')}…）。不一定退稿，但排版系统可能替换成别的字形，宽度会变、词会撞。`,
          `把 figure.json 的 font 改成 ${acceptedRaw.slice(0, 2).join(' 或 ')}；改完重跑 render，顺带看重排后文字有没有再溢出。`)
      }
    }
    // 中文 + 无中文字形字体 = 方框。要看整条回退链（Arial, PingFang SC, sans-serif 是合格的）
    const chainFamilies = [...svg.fontChains]
      .flatMap((chain) => String(chain).split(','))
      .map((f) => f.trim().replace(/^["']|["']$/g, '').toLowerCase())
      .filter(Boolean)
    if (spec && spec.font) chainFamilies.push(String(spec.font).toLowerCase())
    if (svg.hasCjkText && families.size) {
      const hasCjkFont = chainFamilies.some((f) => CJK_FONTS.some((c) => f.includes(c)))
      if (!hasCjkFont) {
        add('warn', 'CJK_FONT_MISSING',
          `图里有中文，但字体清单（${[...families].join(' / ')}）里没有一款带中文字形 —— 在没有该字体的机器上会显示成「□□」。`,
          '给中文指定 font-family 回退链，或在 figure.json 里用带中文字形的字体（Noto Sans CJK SC / PingFang SC / SimHei）。')
      }
    }
  }

  /* ---------------- ⑧ AI 概念图被当数据图 ---------------- */
  const outDir = join(wd, 'out')
  const outFiles = listDir(outDir)
  const aiMarkers = outFiles.filter((f) => f.endsWith('.ai-generated.json'))
  const dataishTypes = ['chart', 'pipeline', 'architecture', 'mechanism', 'comparison']
  const figType = (spec && spec.type) || ''

  if (aiMarkers.length) {
    if (dataishTypes.includes(figType)) {
      add('error', 'AI_IMAGE_AS_DATA_FIGURE',
        `这个工作区是「${figType}」类型的图，但 out/ 里有 ${aiMarkers.length} 个 AI 生成标记（${aiMarkers.slice(0, 2).join('、')}）—— AI 图里的文字和数据都是编的，当数据图/结构图交上去就是学术不端。`,
        `把这些 concept-*.png 只当风格参考：真正的${figType === 'chart' ? '数据图用 chart 命令从 CSV 画' : '结构图用 render 命令画'}；确要用 AI 图，就新建一个 type="concept" 的工作区单独交付，并在图注写明「AI 生成示意」。`)
    }
    if (figType && figType !== 'concept' && figType !== 'toc') {
      add('warn', 'AI_CAPTION_MISSING_DISCLOSURE',
        `图注里没提这些图是 AI 生成的（当前 type=${figType}）。审稿人一旦发现，比图丑严重得多。`,
        '图注里写明「图中背景为 AI 生成的概念示意图，非真实数据」；或把 AI 图移出这个工作区。')
    }
    // 标记文件本身要能自证：prompt/model/时间都在
    for (const m of aiMarkers.slice(0, 3)) {
      const j = readJsonSafe(join(outDir, m))
      if (!j || !j.prompt || !j.model) {
        add('warn', 'AI_MARKER_INCOMPLETE',
          `标记文件 ${m} 里缺 prompt 或 model —— 将来被问到「这图怎么来的」拿不出记录。`,
          '重新跑 concept 生成（会自动补全 marker），或手动把 prompt/model/createdAt 补进这个 json。')
      }
    }
  }
  // 有 AI 图却没有标记 = 更危险
  const conceptPngs = outFiles.filter((f) => /^concept-.*\.png$/i.test(f))
  for (const png of conceptPngs) {
    const marker = join(outDir, png.replace(/\.png$/i, '.ai-generated.json'))
    if (!exists(marker)) {
      add('error', 'AI_IMAGE_UNMARKED',
        `out/${png} 看起来是 AI 生成的概念图，但没有对应的 .ai-generated.json 标记 —— 学术诚信要求留下「这是 AI 生成的」证据。`,
        `重跑 \`node scripts/fig.mjs concept <dir>\`（会自动写标记）；或手工建 out/${png.replace(/\.png$/i, '.ai-generated.json')} 写明 prompt/model/时间。`)
    }
  }
  // 矢量图里嵌了 AI 图
  if (svg && svg.images.length) {
    for (const img of svg.images) {
      const href = String(img.href || '')
      if (!/concept-|ai-generated/i.test(href)) continue
      add('error', 'AI_IMAGE_EMBEDDED_IN_VECTOR',
        `SVG 里嵌入了 AI 生成的位图（${basename(href).slice(0, 40)}）—— 位图进矢量图会又糊又没法编辑，还容易被当成真实数据。`,
        '把 AI 图当独立的 concept 交付文件，别嵌进 render 出的结构图里；结构图里的所有元素都应该由代码画。')
      break
    }
  }

  /* ---------------- 汇总 ---------------- */
  const errors = issues.filter((i) => i.level === 'error').length
  const warns = issues.filter((i) => i.level === 'warn').length
  const pass = errors === 0

  const lines = []
  const dpiText = preset.dpi ? `${preset.dpi}dpi` : '矢量交付（不收位图，不判 dpi）'
  const fontRange = preset.max_font_pt ? `${preset.min_font_pt}–${preset.max_font_pt}pt` : `≥${preset.min_font_pt}pt`
  lines.push(`期刊：${preset.label}（${widthMode === 'double' ? '双栏' : '单栏'} ${targetWidthMm}mm，最大高 ${preset.max_height_mm}mm，字号 ${fontRange}，${dpiText}）${fromFallback ? ' [兜底规格]' : ''}`)
  lines.push(`图：${svgPath ? basename(svgPath) : '（无 SVG）'}${actualWidthMm ? `  ${round(actualWidthMm)}×${actualHeightMm ? round(actualHeightMm) : '?'}mm` : ''}${svg && svg.texts.length ? `  ${svg.texts.length} 段文字` : ''}${declaredDpi ? `  ${declaredDpi}dpi` : ''}`)
  lines.push('')
  if (!issues.length) {
    lines.push('✅ 没有发现合规问题。可以导出了。')
  } else {
    if (errors) {
      lines.push(`❌ ${errors} 个必须改的问题：`)
      for (const i of issues.filter((x) => x.level === 'error')) {
        lines.push(`  · [${i.code}] ${i.message}`)
        lines.push(`    → 怎么改：${i.fix}`)
      }
    }
    if (warns) {
      if (errors) lines.push('')
      lines.push(`⚠️  ${warns} 条建议（不改也能投，但改了更稳）：`)
      for (const i of issues.filter((x) => x.level === 'warn')) {
        lines.push(`  · [${i.code}] ${i.message}`)
        lines.push(`    → 怎么改：${i.fix}`)
      }
    }
  }

  const result = {
    ok: true,
    pass,
    // journal.mjs = 正常路径；其余一律 "fallback"（安装有问题），细节看 preset_source_detail
    preset_source: fromFallback ? 'fallback' : 'journal.mjs',
    preset_source_detail: presetSource,
    journal: preset.id,
    issues,
    summary: {
      errors,
      warns,
      text: lines.join('\n'),
      stats: {
        journal: preset.id,
        journalFromFallback: fromFallback,
        preset_source: fromFallback ? 'fallback' : 'journal.mjs',
        preset_source_detail: presetSource,
        vector_only: Boolean(preset.vector_only),
        svg: svgPath ? basename(svgPath) : null,
        width_mm: actualWidthMm ? round(actualWidthMm) : null,
        height_mm: actualHeightMm ? round(actualHeightMm) : null,
        target_width_mm: targetWidthMm,
        min_font_pt: svg && svg.fontSizesPt.length ? round(Math.min(...svg.fontSizesPt)) : null,
        dpi: declaredDpi || null,
        texts: svg ? svg.texts.length : 0,
        shapes: svg ? svg.shapes.length : 0,
        colors: svg ? svg.colors.size : 0,
        ai_markers: aiMarkers.length
      }
    }
  }

  // 落盘 out/check.json（BRIEF 5.4 的产物布局），失败不影响检查结论
  if (opts.write !== false) {
    try {
      mkdirSync(outDir, { recursive: true })
      writeFileSync(join(outDir, 'check.json'), JSON.stringify({
        generatedAt: new Date().toISOString(),
        journal: preset.id,
        pass,
        ...result.summary,
        issues
      }, null, 2), 'utf8')
      result.checkPath = join(outDir, 'check.json')
    } catch (e) {
      result.issues.push({
        level: 'warn', code: 'CHECK_REPORT_UNWRITTEN',
        message: `检查报告没能写到 out/check.json：${e && e.message ? e.message : e}（检查结果本身有效）`,
        fix: '确认 out/ 目录可写、磁盘没满；不影响这次检查结论。'
      })
    }
  }

  return result
}

/* ==========================================================================
 * 九、CLI：node scripts/check.mjs <workdir> [--journal X] [--dpi N] [--json]
 * ========================================================================== */

async function main(argv) {
  const args = argv.slice(2)
  const flags = {}
  const rest = []
  for (let i = 0; i < args.length; i++) {
    const a = args[i]
    if (a === '--json') flags.json = true
    else if (a === '--no-write') flags.write = false
    else if (a.startsWith('--')) { flags[a.slice(2)] = args[i + 1]; i++ }
    else rest.push(a)
  }
  const workDir = rest[0] || process.cwd()
  const res = await checkFigure(workDir, {
    journal: flags.journal,
    dpi: flags.dpi ? Number(flags.dpi) : undefined,
    svgPath: flags.svg,
    write: flags.write !== false
  })
  if (flags.json) {
    process.stdout.write(JSON.stringify(res, null, 2) + '\n')
  } else {
    process.stdout.write(res.summary.text + '\n')
  }
  process.exit(res.pass ? 0 : 1)
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main(process.argv).catch((e) => {
    process.stderr.write(`检查器自己崩了：${e && e.stack ? e.stack : e}\n`)
    process.exit(2)
  })
}

export default checkFigure
