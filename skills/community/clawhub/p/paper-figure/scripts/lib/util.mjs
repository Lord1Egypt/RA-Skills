// scripts/lib/util.mjs
// 共用工具箱：单位换算、文字宽度估算与自动换行、CSV 解析、JSON/文本读写、结构化告警。
// 零依赖，只用 node: 内置模块。所有坐标内部统一用 pt（1pt = 1/72 英寸），对外描述用 mm。

import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { dirname, isAbsolute, join, resolve } from 'node:path'

// ---------------------------------------------------------------- 单位换算

export const MM_PER_INCH = 25.4
export const PT_PER_INCH = 72
export const PT_PER_MM = PT_PER_INCH / MM_PER_INCH // ≈ 2.8346456693

// SVG 用户单位约定：**1 用户单位 = 1mm**。
// 几何量一律用 mm；字号一律用 pt 声明（figure.json 的 font_size_pt），落盘时换成 mm：
//   1pt = 0.3528mm（精确值 25.4/72 = 0.352777…），7pt ≈ 2.47mm。
// 好处：viewBox 数字就是毫米刻度，宽 89mm 的图 viewBox 就是 "0 0 89 60"，肉眼可校。

/** 毫米 → 点 */
export const mmToPt = (mm) => mm * PT_PER_MM
/** 1pt = 0.3528mm 这个数，做乘法时用它（ptToMm 是函数，别当常量用） */
export const PT_TO_MM = 1 / PT_PER_MM
/** 点 → 毫米（0.3528） */
export const ptToMm = (pt) => pt / PT_PER_MM
/** 7pt → 2.4696mm 这类换算，写图里/注释里都用这个 */
export const fontPtToMm = (pt) => pt / PT_PER_MM
/** 毫米 → 像素（按 dpi） */
export const mmToPx = (mm, dpi = 300) => Math.round((mm / MM_PER_INCH) * dpi)

/** 数字去掉浮点尾巴，输出成 SVG 属性友好的短字符串 */
export function fmtNum(n, digits = 3) {
  const v = Number(n)
  if (!Number.isFinite(v)) return '0'
  const s = v.toFixed(digits)
  return s.includes('.') ? s.replace(/0+$/, '').replace(/\.$/, '') : s
}

export const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v))
export const round = (v, d = 2) => Math.round(v * 10 ** d) / 10 ** d

// ---------------------------------------------------------------- 错误与告警

/** 带「下一步怎么办」的业务错误；CLI 会把它翻成 {ok:false, error, fix} */
export class PFError extends Error {
  /**
   * @param {string} message 人话错误描述
   * @param {string} [fix] 人话的下一步
   * @param {string} [code] 机器可读错误码
   */
  constructor(message, fix = '', code = 'PF_ERROR') {
    super(message)
    this.name = 'PFError'
    this.fix = fix
    this.code = code
  }
}

export function fail(message, fix = '', code = 'PF_ERROR') {
  throw new PFError(message, fix, code)
}

/** 统一告警结构：渲染/图表/web 检查器都吃这个格式 */
export function warn(code, message, fix = '', extra = {}) {
  return { level: 'warn', code, message, fix, ...extra }
}

// ---------------------------------------------------------------- 终端输出（stderr）

const PREFIX = '[paper-figure]'

/** 进度/人话提示一律走 stderr，stdout 只留给 JSON */
export function log(...parts) {
  process.stderr.write(`${PREFIX} ${parts.join(' ')}\n`)
}

export function logStep(label, detail = '') {
  log(detail ? `${label} · ${detail}` : label)
}

export function logWarnings(warnings = []) {
  for (const w of warnings) {
    log(`注意：${w.message}${w.fix ? ` → ${w.fix}` : ''}`)
  }
}

// ---------------------------------------------------------------- 文件与路径

export function ensureDir(dir) {
  mkdirSync(dir, { recursive: true })
  return dir
}

export function fileExists(p) {
  try {
    return existsSync(p) && statSync(p).isFile()
  } catch {
    return false
  }
}

export function dirExists(p) {
  try {
    return existsSync(p) && statSync(p).isDirectory()
  } catch {
    return false
  }
}

/** 相对路径按 base 解析；绝对路径原样返回（跨平台，不认死分隔符） */
export function resolveIn(base, p) {
  if (!p) return base
  return isAbsolute(p) ? p : resolve(base, p)
}

export function readTextFile(file, label = '文件') {
  if (!fileExists(file)) {
    fail(`${label}不存在：${file}`, `先跑 node scripts/fig.mjs init <工作区> 生成一份，再填内容。`)
  }
  return readFileSync(file, 'utf8')
}

export function readJSONFile(file, label = 'JSON 文件') {
  const raw = readTextFile(file, label)
  try {
    return JSON.parse(raw)
  } catch (e) {
    fail(
      `${label}不是合法 JSON：${file}（${e.message}）`,
      '常见原因：多写了一个逗号、用了中文引号、注释没删。改完再跑一次。',
      'BAD_JSON',
    )
  }
}

export function writeTextFile(file, text) {
  ensureDir(dirname(file))
  writeFileSync(file, text, 'utf8')
  return file
}

export function writeJSONFile(file, data) {
  return writeTextFile(file, `${JSON.stringify(data, null, 2)}\n`)
}

/** 输出文件名清洗：只留字母数字中文和 -_ */
export function safeName(name, fallback = 'figure') {
  const s = String(name ?? '').trim().replace(/[\\/:*?"<>|\s]+/g, '-').replace(/^-+|-+$/g, '')
  return s || fallback
}

export function nowIso() {
  return new Date().toISOString()
}

export function relFrom(base, target) {
  const rel = resolve(target).slice(resolve(base).length)
  return rel.replace(/^[\\/]+/, '') || '.'
}

export { join, resolve, dirname }

// ---------------------------------------------------------------- 颜色

export function normalizeHex(input) {
  if (typeof input !== 'string') return null
  let s = input.trim()
  if (!s.startsWith('#')) s = `#${s}`
  if (/^#[0-9a-fA-F]{3}$/.test(s)) {
    s = `#${s[1]}${s[1]}${s[2]}${s[2]}${s[3]}${s[3]}`
  }
  return /^#[0-9a-fA-F]{6}$/.test(s) ? s.toLowerCase() : null
}

function hexToRgb(hex) {
  const h = normalizeHex(hex) || '#000000'
  return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]
}

function rgbToHex([r, g, b]) {
  const to = (v) => clamp(Math.round(v), 0, 255).toString(16).padStart(2, '0')
  return `#${to(r)}${to(g)}${to(b)}`
}

/** 两个颜色线性插值，t=0 取 a，t=1 取 b */
export function mixHex(a, b, t = 0.5) {
  const A = hexToRgb(a)
  const B = hexToRgb(b)
  return rgbToHex(A.map((v, i) => v + (B[i] - v) * t))
}

/** 往白色里调：t=0 原色，t=1 纯白（用于节点浅底色） */
export const tint = (hex, t = 0.85) => mixHex(hex, '#ffffff', t)
/** 往黑色里调：t=0 原色，t=1 纯黑（用于描边/文字加深） */
export const shade = (hex, t = 0.2) => mixHex(hex, '#000000', t)

/** WCAG 相对亮度 */
export function luminance(hex) {
  const [r, g, b] = hexToRgb(hex).map((v) => {
    const c = v / 255
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4
  })
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}

/** 对比度，1~21 */
export function contrastRatio(a, b) {
  const la = luminance(a)
  const lb = luminance(b)
  const [hi, lo] = la >= lb ? [la, lb] : [lb, la]
  return (hi + 0.05) / (lo + 0.05)
}

// ---------------------------------------------------------------- 文字宽度估算
// 用 Helvetica/Arial 的 AFM 字宽表（单位 1/1000 em）。Arial 与 Helvetica 宽度几乎一致，
// 中文字按全角 1em 算。这张表让「文字会不会撑破框」的判断足够准，不依赖浏览器测量。

const HELV_W = {
  ' ': 278, '!': 278, '"': 355, '#': 556, $: 556, '%': 889, '&': 667, "'": 191, '(': 333,
  ')': 333, '*': 389, '+': 584, ',': 278, '-': 333, '.': 278, '/': 278, ':': 278, ';': 278,
  '<': 584, '=': 584, '>': 584, '?': 556, '@': 1015, '[': 278, '\\': 278, ']': 278, '^': 469,
  _: 556, '`': 333, '{': 334, '|': 260, '}': 334, '~': 584,
  A: 667, B: 667, C: 722, D: 722, E: 667, F: 611, G: 778, H: 722, I: 278, J: 500, K: 667,
  L: 556, M: 833, N: 722, O: 778, P: 667, Q: 778, R: 722, S: 667, T: 611, U: 722, V: 667,
  W: 944, X: 667, Y: 667, Z: 611,
  a: 556, b: 556, c: 500, d: 556, e: 556, f: 278, g: 556, h: 556, i: 222, j: 222, k: 500,
  l: 222, m: 833, n: 556, o: 556, p: 556, q: 556, r: 333, s: 500, t: 278, u: 556, v: 500,
  w: 722, x: 500, y: 500, z: 500,
  '·': 278, '—': 1000, '–': 556, '…': 1000, '±': 584, '×': 584, '÷': 584, '°': 278, '′': 278,
  '≤': 584, '≥': 584, '≈': 584, '→': 800, '←': 800, '↑': 800, '↓': 800, 'μ': 556, 'α': 556,
  'β': 556, 'γ': 556, 'δ': 556, 'Δ': 612, 'σ': 556, 'Ω': 768, 'θ': 556, 'λ': 500, 'π': 556,
}

const CJK_RE = /[\u2e80-\u9fff\u3000-\u303f\uf900-\ufaff\uff00-\uffef]/

/** 单个字符的字宽（单位：em 的千分之一） */
export function charWidthEm(ch) {
  const c = ch.codePointAt(0)
  if (c >= 0x2e80) return 1000 // 中日韩、全角标点：等宽全角
  const v = HELV_W[ch]
  if (v !== undefined) return v
  if (/[0-9]/.test(ch)) return 556
  if (/[A-Z]/.test(ch)) return 667
  if (/[a-z]/.test(ch)) return 500
  return 556
}

/**
 * 估算一段文字的渲染宽度（pt）。
 * @param {string} text
 * @param {number} fontSizePt
 * @param {{bold?:boolean, italic?:boolean}} [opts]
 */
export function estimateTextWidthPt(text, fontSizePt, opts = {}) {
  const s = String(text ?? '')
  if (!s) return 0
  let em = 0
  for (const ch of s) em += charWidthEm(ch)
  let width = (em / 1000) * fontSizePt
  if (opts.bold) width *= 1.06 // Arial Bold 略宽
  if (opts.italic) width *= 1.02
  return width
}

/**
 * 估算文字宽度，单位 mm（SVG 用户单位 = 1mm）。
 * 字号入参永远是 pt。
 */
export function estimateTextWidthMm(text, fontSizePt, opts = {}) {
  return estimateTextWidthPt(text, fontSizePt, opts) * PT_TO_MM
}

/** 行高（mm）：默认 1.25 倍字号（期刊图通用口径） */
export function lineHeightMm(fontSizePt, factor = 1.25) {
  return fontSizePt * factor * PT_TO_MM
}

/**
 * 字号阶梯：一张图最多三档（正文 / 次级 / 下限）。
 * 所有文字只能取阶梯里的值，避免「每个节点一个字号」的乱象。
 * @returns {number[]} 从大到小
 */
export function fontLadder(fs, minFs = 5, maxFs = null) {
  const top = Math.max(minFs, Math.min(Number.isFinite(maxFs) ? maxFs : fs, fs))
  const steps = [top, top - 0.5, top - 1].map((v) => Math.max(minFs, Math.round(v * 10) / 10))
  return [...new Set(steps)].sort((a, b) => b - a)
}

const TOKEN_RE = /[\u2e80-\u9fff\u3000-\u303f\uf900-\ufaff\uff00-\uffef]|[^\s\u2e80-\u9fff\u3000-\u303f\uf900-\ufaff\uff00-\uffef]+|\s+/gu

/**
 * 按宽度（mm）贪心换行。中文按字断开，英文按词断开；单个超长词会强制截断。
 * @param {string} text
 * @param {number} maxWidthMm 可用宽度（mm）
 * @param {number} fontSizePt 字号（pt）
 * @returns {{lines:string[], overflow:boolean}}
 */
export function wrapText(text, maxWidthMm, fontSizePt, opts = {}) {
  const maxW = Math.max(0.2, maxWidthMm)
  const measure = (s) => estimateTextWidthMm(s, fontSizePt, opts)
  const paragraphs = String(text ?? '').split(/\r?\n/)
  const lines = []
  let overflow = false

  for (const para of paragraphs) {
    const tokens = para.match(TOKEN_RE) || ['']
    let cur = ''
    for (const tok of tokens) {
      if (/^\s+$/.test(tok)) {
        if (cur) cur += ' '
        continue
      }
      const cand = cur + tok
      if (cur && measure(cand) > maxW) {
        lines.push(cur.trimEnd())
        cur = tok
      } else {
        cur = cand
      }
      // 单个词本身就超宽：硬切
      if (!cur.includes(' ') && measure(cur) > maxW && [...cur].length > 1) {
        const chars = [...cur]
        let buf = ''
        for (const ch of chars) {
          if (buf && measure(buf + ch) > maxW) {
            lines.push(buf)
            buf = ch
          } else buf += ch
        }
        cur = buf
        overflow = true
      }
    }
    lines.push(cur.trimEnd())
  }
  while (lines.length > 1 && lines[0] === '') lines.shift()
  return { lines, overflow }
}

/** 把一行文字截断到给定宽度（mm），超出部分用省略号 */
export function truncateToWidth(text, maxWidthMm, fontSizePt, opts = {}) {
  const s = String(text ?? '')
  if (estimateTextWidthMm(s, fontSizePt, opts) <= maxWidthMm) return s
  const chars = [...s]
  let out = ''
  for (const ch of chars) {
    const cand = out + ch + '…'
    if (estimateTextWidthMm(cand, fontSizePt, opts) > maxWidthMm) break
    out += ch
  }
  return out ? `${out}…` : '…'
}

/**
 * 在给定框宽（mm）内排版一段文字：先试原字号，放不下就缩字号，缩到下限还放不下就截断。
 * 字号始终以 pt 计。
 * @returns {{lines:string[], fontSizePt:number, shrunk:boolean, truncated:boolean, overflow:boolean}}
 */
export function fitText(text, maxWidthMm, fontSizePt, opts = {}) {
  const { minFontSizePt = 5, maxLines = 2, bold = false, step = 0.25 } = opts
  const start = fontSizePt
  let fs = start
  let r = wrapText(text, maxWidthMm, fs, { bold })
  let guard = 0
  while (r.lines.length > maxLines && fs > minFontSizePt + 1e-6 && guard++ < 200) {
    fs = Math.max(minFontSizePt, Number((fs - step).toFixed(3)))
    r = wrapText(text, maxWidthMm, fs, { bold })
  }
  let truncated = false
  let lines = r.lines
  if (lines.length > maxLines) {
    truncated = true
    lines = lines.slice(0, maxLines)
    const li = lines.length - 1
    lines[li] = truncateToWidth(lines[li], maxWidthMm, fs, { bold })
  }
  return {
    lines,
    fontSizePt: fs,
    shrunk: fs < start - 1e-6,
    truncated,
    overflow: r.overflow || truncated,
  }
}

// ---------------------------------------------------------------- CSV 解析

function sniffDelimiter(text) {
  const firstLine = text.split(/\r?\n/, 1)[0] || ''
  const counts = [
    [',', (firstLine.match(/,/g) || []).length],
    [';', (firstLine.match(/;/g) || []).length],
    ['\t', (firstLine.match(/\t/g) || []).length],
  ].sort((a, b) => b[1] - a[1])
  return counts[0][1] > 0 ? counts[0][0] : ','
}

/**
 * 解析 CSV（支持引号、逗号/分号/制表符分隔、BOM、CRLF）。
 * @returns {{header:string[], rows:Record<string,string>[], delimiter:string}}
 */
export function parseCSV(text) {
  const raw = String(text ?? '').replace(/^\uFEFF/, '')
  const delimiter = sniffDelimiter(raw)
  const records = []
  let field = ''
  let row = []
  let inQuotes = false

  const pushField = () => {
    row.push(field)
    field = ''
  }
  const pushRow = () => {
    pushField()
    if (row.some((c) => c.trim() !== '')) records.push(row)
    row = []
  }

  for (let i = 0; i < raw.length; i++) {
    const ch = raw[i]
    if (inQuotes) {
      if (ch === '"') {
        if (raw[i + 1] === '"') {
          field += '"'
          i++
        } else inQuotes = false
      } else field += ch
    } else if (ch === '"') {
      inQuotes = true
    } else if (ch === delimiter) {
      pushField()
    } else if (ch === '\n') {
      pushRow()
    } else if (ch === '\r') {
      // 交给 \n 处理
    } else {
      field += ch
    }
  }
  if (field !== '' || row.length) pushRow()

  if (!records.length) return { header: [], rows: [], delimiter }
  const header = records[0].map((h, i) => (h.trim() || `col${i + 1}`))
  const seen = new Map()
  const uniqueHeader = header.map((h) => {
    const n = (seen.get(h) || 0) + 1
    seen.set(h, n)
    return n === 1 ? h : `${h}_${n}`
  })
  const rows = records.slice(1).map((rec) => {
    const obj = {}
    uniqueHeader.forEach((h, i) => {
      obj[h] = (rec[i] ?? '').trim()
    })
    return obj
  })
  return { header: uniqueHeader, rows, delimiter }
}

/** 把 CSV 单元格转成数字，空/非数字返回 NaN */
export function toNumber(v) {
  if (typeof v === 'number') return v
  const s = String(v ?? '').trim().replace(/,/g, '')
  if (!s) return NaN
  const n = Number(s)
  return Number.isFinite(n) ? n : NaN
}

// ---------------------------------------------------------------- 刻度算法

/** 统计意义上的「好看」步长（1/2/5×10^n） */
export function niceNum(range, roundTo = false) {
  const exp = Math.floor(Math.log10(range || 1))
  const f = (range || 1) / 10 ** exp
  let nf
  if (roundTo) nf = f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10
  else nf = f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10
  return nf * 10 ** exp
}

/**
 * 线性坐标刻度：把 [min,max] 扩到好读的整数，返回 ticks。
 * @returns {{min:number,max:number,step:number,ticks:number[]}}
 */
export function linearScale(min, max, targetTicks = 5) {
  let lo = Number.isFinite(min) ? min : 0
  let hi = Number.isFinite(max) ? max : 1
  if (lo === hi) {
    const pad = Math.abs(lo) > 0 ? Math.abs(lo) * 0.1 : 1
    lo -= pad
    hi += pad
  }
  if (hi < lo) [lo, hi] = [hi, lo]
  const range = niceNum(hi - lo, false)
  const step = niceNum(range / Math.max(1, targetTicks - 1), true)
  const niceMin = Math.floor(lo / step) * step
  const niceMax = Math.ceil(hi / step) * step
  const ticks = []
  const n = Math.round((niceMax - niceMin) / step)
  for (let i = 0; i <= n; i++) {
    const v = niceMin + i * step
    ticks.push(Math.abs(v) < step * 1e-9 ? 0 : Number(v.toPrecision(12)))
  }
  return { min: niceMin, max: niceMax, step, ticks }
}

/** 对数坐标刻度：按 10 的整数幂给主刻度 */
export function logScale(min, max) {
  const lo = min > 0 ? min : 0.1
  const hi = max > lo ? max : lo * 10
  const e0 = Math.floor(Math.log10(lo))
  const e1 = Math.ceil(Math.log10(hi))
  const ticks = []
  for (let e = e0; e <= e1; e++) ticks.push(Number((10 ** e).toPrecision(12)))
  return { min: 10 ** e0, max: 10 ** e1, ticks }
}

/** 刻度标签的紧凑写法（1000 → 1k，1000000 → 1M） */
export function formatTick(v, step = 0) {
  const abs = Math.abs(v)
  if (abs >= 1e6) return `${round(v / 1e6, 1)}M`
  if (abs >= 1e4) return `${round(v / 1e3, abs >= 1e5 ? 0 : 1)}k`
  let digits = 0
  if (step > 0 && step < 1) digits = Math.min(4, Math.ceil(-Math.log10(step)))
  else if (Math.abs(v - Math.round(v)) > 1e-9) digits = 2
  return String(round(v, digits))
}
