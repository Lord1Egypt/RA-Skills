// scripts/lib/journal.mjs
// 期刊预置库读取：assets/journals.json → getPreset / listPresets / resolveWidthMm。
// 预置只是排版默认值；真合规以目标刊当期作者指南为准（每条都带 source 与 verified）。

import { readJSONFile, fail, join, dirname, fileExists } from './util.mjs'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
/** 仓库根目录（scripts/lib → 上两级） */
export const ROOT_DIR = join(HERE, '..', '..')
/** assets 目录绝对路径，其他模块可直接用 */
export const ASSETS_DIR = join(ROOT_DIR, 'assets')

const FILE = join(ASSETS_DIR, 'journals.json')
let cache = null

function load() {
  if (cache) return cache
  if (!fileExists(FILE)) {
    fail(
      `找不到期刊预置库：${FILE}`,
      '仓库不完整，重新 clone 一次；或者检查 assets/ 是否被误删。',
      'MISSING_JOURNALS',
    )
  }
  const data = readJSONFile(FILE, '期刊预置库 assets/journals.json')
  if (!Array.isArray(data.journals) || !data.journals.length) {
    fail('期刊预置库格式不对：journals 应该是非空数组。', '对照 assets/journals.json 的 _meta 说明修。', 'BAD_JOURNALS')
  }
  cache = data
  return data
}

/** 所有预置（浅拷贝，防止调用方改坏缓存） */
export function listPresets() {
  return load().journals.map((p) => ({ ...p }))
}

/** 默认预置 id */
export function defaultPresetId() {
  return load().default || 'nature'
}

/** 全部可选 id，给 --help 和报错用 */
export function presetIds() {
  return load().journals.map((p) => p.id)
}

/**
 * 按 id / 别名取预置。
 * 认不出来时回退到 custom，并在返回值里带 fallbackFrom，让上层能报警告。
 * @param {string} [id]
 */
export function getPreset(id = defaultPresetId()) {
  const data = load()
  const list = data.journals
  const key = String(id ?? '').trim().toLowerCase()
  const hit =
    list.find((p) => p.id.toLowerCase() === key) ||
    list.find((p) => (p.aliases || []).some((a) => String(a).toLowerCase() === key))
  if (hit) return { ...hit }
  const fallback = list.find((p) => p.id === 'custom') || list[0]
  return { ...fallback, fallbackFrom: String(id) }
}

/** 给人看的一行摘要：「Nature · 单 89 / 双 183mm · 最小 5pt · 600dpi」 */
export function describePreset(p) {
  if (!p) return ''
  return `${p.label} · 单栏 ${p.single_mm}mm / 双栏 ${p.double_mm}mm · 最小字号 ${p.min_font_pt}pt · ${p.dpi}dpi`
}

const UNIT_TO_MM = { mm: 1, cm: 10, in: 25.4, pt: 25.4 / 72, px: 25.4 / 300 }

/**
 * 把 figure.json 的 width 字段解析成实际毫米。
 * 支持：'single' / 'double' / 'onehalf' / 数字(mm) / '183mm' / '7.2in' / '18cm'
 * @param {object} preset getPreset() 的返回值
 * @param {string|number} [width]
 * @returns {number} 毫米
 */
export function resolveWidthMm(preset, width) {
  const p = preset || getPreset()
  const single = Number(p.single_mm) || 89
  const double = Number(p.double_mm) || 183
  if (width === undefined || width === null || width === '') return single
  if (typeof width === 'number' && Number.isFinite(width)) return checkWidth(width, p)

  const s = String(width).trim().toLowerCase()
  if (['single', '单栏', '1', '1col', 'one'].includes(s)) return checkWidth(single, p)
  if (['double', '双栏', '2', '2col', 'full', '通栏'].includes(s)) return checkWidth(double, p)
  if (['onehalf', '1.5', '1.5col', '1.5栏'].includes(s)) return checkWidth(Number(p.onehalf_mm) || (single + double) / 2, p)

  const m = s.match(/^([\d.]+)\s*(mm|cm|in|pt|px)?$/)
  if (m) {
    const unit = m[2] || 'mm'
    return checkWidth(Number(m[1]) * (UNIT_TO_MM[unit] || 1), p)
  }
  fail(
    `width 看不懂：「${width}」`,
    "可写 single / double / onehalf，或直接写毫米如 89、'183mm'、'7.2in'。",
    'BAD_WIDTH',
  )
}

function checkWidth(mm, p) {
  if (!Number.isFinite(mm) || mm < 20 || mm > 420) {
    fail(
      `图宽 ${mm}mm 不合理（合理范围 20–420mm）。`,
      `按 ${p?.label || '当前期刊'} 的栏宽来：单栏 ${p?.single_mm ?? 89}mm、双栏 ${p?.double_mm ?? 183}mm。`,
      'BAD_WIDTH',
    )
  }
  return Math.round(mm * 100) / 100
}

/** 当前宽度算单栏还是双栏（check 报告里用） */
export function widthClass(preset, widthMm) {
  const p = preset || getPreset()
  const d = Math.abs(widthMm - Number(p.double_mm))
  const s = Math.abs(widthMm - Number(p.single_mm))
  const h = Math.abs(widthMm - (Number(p.onehalf_mm) || 0))
  if (h <= 1.5) return 'onehalf'
  if (d <= 1.5) return 'double'
  if (s <= 1.5) return 'single'
  return 'custom'
}
