// scripts/lib/palette.mjs
// 调色板读取：assets/palettes.json → getPalette / listPalettes / 取色辅助。
// 原则：颜色只从色板取，不允许在渲染代码里散落硬编码 hex（改配色只改 JSON 一处）。

import { readJSONFile, fail, normalizeHex, tint, join, dirname, fileExists } from './util.mjs'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const ASSETS = join(HERE, '..', '..', 'assets')
const FILE = join(ASSETS, 'palettes.json')

let cache = null

function load() {
  if (cache) return cache
  if (!fileExists(FILE)) {
    fail(`找不到调色板库：${FILE}`, '仓库不完整，重新 clone；或确认 assets/palettes.json 存在。', 'MISSING_PALETTES')
  }
  const data = readJSONFile(FILE, '调色板库 assets/palettes.json')
  if (!Array.isArray(data.palettes) || !data.palettes.length) {
    fail('调色板库格式不对：palettes 应该是非空数组。', '对照 palettes.json 的 _meta 说明修。', 'BAD_PALETTES')
  }
  cache = data
  return data
}

export function listPalettes() {
  return load().palettes.map((p) => ({ ...p }))
}

export function defaultPaletteId() {
  return load().default || 'okabe-ito'
}

export function paletteIds() {
  return load().palettes.map((p) => p.id)
}

/**
 * 按 id / 别名取色板；认不出回退默认色板并带 fallbackFrom。
 * @returns {{id:string,label:string,colors:string[],colorblind_safe:boolean,grayscale_ok:boolean,
 *            ink:string,muted:string,grid:string,bg:string,edge:string,notes?:string}}
 */
export function getPalette(id = defaultPaletteId()) {
  const data = load()
  const key = String(id ?? '').trim().toLowerCase()
  const list = data.palettes
  const hit =
    list.find((p) => p.id.toLowerCase() === key) ||
    list.find((p) => (p.aliases || []).some((a) => String(a).toLowerCase() === key))
  const p = hit || list.find((x) => x.id === defaultPaletteId()) || list[0]
  const colors = (p.colors || []).map((c) => normalizeHex(c)).filter(Boolean)
  if (!colors.length) {
    fail(`色板 ${p.id} 没有有效颜色。`, '检查 palettes.json 里 colors 是否是 #RRGGBB。', 'BAD_PALETTE_COLORS')
  }
  const chartColors = (p.chart_colors && p.chart_colors.length ? p.chart_colors : p.colors)
    .map((c) => normalizeHex(c))
    .filter(Boolean)
  return {
    ...p,
    colors,
    chart_colors: chartColors,
    ink: normalizeHex(p.ink) || '#1a1a1a',
    muted: normalizeHex(p.muted) || '#5f5f5f',
    grid: normalizeHex(p.grid) || '#e6e6e6',
    bg: normalizeHex(p.bg) || '#ffffff',
    edge: normalizeHex(p.edge) || '#4a4a4a',
    ...(hit ? {} : { fallbackFrom: String(id) }),
  }
}

/**
 * 图表系列取色：优先 chart_colors（跳过纯黑，黑色留给坐标轴/文字），没有就退回 colors。
 * @param {object} palette
 * @param {number} index
 */
export function chartColorAt(palette, index) {
  const p = palette || getPalette()
  const list = (p.chart_colors && p.chart_colors.length ? p.chart_colors : p.colors).map((c) => normalizeHex(c)).filter(Boolean)
  const n = list.length
  return list[((index % n) + n) % n]
}

/** 按序号循环取主色：系列数超过色板长度时循环，但不重复相邻色 */
export function seriesColor(palette, index) {
  const p = palette || getPalette()
  const n = p.colors.length
  return p.colors[((index % n) + n) % n]
}

/** 第 index 个系列的浅色填充（节点底色用） */
export function seriesTint(palette, index, amount = 0.86) {
  return tint(seriesColor(palette, index), amount)
}

/** 给不入色板的元素用的中性色（边框、说明文字、网格） */
export function neutral(palette) {
  const p = palette || getPalette()
  return {
    ink: p.ink,
    muted: p.muted,
    grid: p.grid,
    bg: p.bg,
    edge: p.edge,
    white: '#ffffff',
    // 常见语义色：正/负/警告（图表标注用，不参与系列配色）
    positive: '#0072B2',
    negative: '#D55E00',
    neutral: '#6b6b6b',
  }
}
