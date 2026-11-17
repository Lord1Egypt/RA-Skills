// scripts/chart.mjs
// CSV → 期刊风格图表（bar / line / scatter / grouped-bar / errorbar）。
//
// 跟 render.mjs 同一套约定：1 用户单位 = 1mm、字号 pt、根节点给 mm 尺寸 + viewBox。
// 风格取向：期刊正文图 —— 只留左/下轴线、细轴线、无花哨网格、直接标注优先于图例。
//
// 对外接口（BRIEF §5.3）：renderChart(workDir, opts) -> {ok,svgPath,widthMm,heightMm,warnings:[]}

import { join } from 'node:path'
import {
  clamp,
  ensureDir,
  estimateTextWidthMm,
  fail,
  fmtNum,
  fontLadder,
  lineHeightMm,
  linearScale,
  parseCSV,
  PT_TO_MM,
  readTextFile,
  resolveIn,
  round,
  safeName,
  toNumber,
  warn,
  writeTextFile,
} from './lib/util.mjs'
import { SW, el, group, line, rect, svgDocument, text } from './lib/svg.mjs'
import { getPreset, resolveWidthMm } from './lib/journal.mjs'
import { chartColorAt, getPalette } from './lib/palette.mjs'

// 图表系列取色：走 palettes.json 的 chart_colors（跳过纯黑，黑色只留给坐标轴/文字/边框）
const chartColor = chartColorAt
import { readSpec } from './spec.mjs'

const MARGIN_MM = 3
const TICK_LEN_MM = 1.1  // 刻度线长度
const KINDS = ['bar', 'line', 'scatter', 'grouped-bar', 'errorbar']

/**
 * 把工作区的 CSV 画成期刊风格 SVG。
 * @param {string} workDir
 * @param {{spec?:object,out?:string,journal?:string,width?:string|number,height_mm?:number}} [opts]
 */
export async function renderChart(workDir, opts = {}) {
  const dir = opts.workDir || workDir || '.'
  const spec = opts.spec || readSpec(dir)
  const preset = getPreset(opts.journal || spec.journal)
  const palette = getPalette(spec.palette)
  const warnings = [...(spec.__warnings || [])]
  if (palette.fallbackFrom) {
    warnings.push(warn('PALETTE_FALLBACK', `配色「${palette.fallbackFrom}」不认识，已用 ${palette.id}`, '见 assets/palettes.json。'))
  }

  const data = spec.data || {}
  if (!data.file) {
    fail(
      'figure.json 的 data.file 没写，画不了图。',
      '在 figure.json 里写 "data": {"file": "data/main.csv", "kind": "bar", "x": "group", "y": ["value"]}。',
      'NO_DATA_FILE',
    )
  }
  const csvPath = resolveIn(dir, data.file)
  const csvText = readTextFile(csvPath, '数据文件')
  const parsed = parseCSV(csvText)
  if (!parsed.rows.length) {
    fail(
      `${data.file} 里没有数据行。`,
      '第一行是表头，从第二行开始写数据；分隔符 , ; Tab 都认。',
      'EMPTY_CSV',
    )
  }

  const kind = KINDS.includes(data.kind) ? data.kind : 'bar'
  const pageW = resolveWidthMm(preset, opts.width ?? spec.width)
  const series = buildSeries(parsed, data, kind, warnings)

  const ticket = makeStyle(spec, preset)
  const pageH = chooseHeight(spec, data, opts, pageW)

  const chart = layoutChart({ series, kind, data, pageW, pageH, style: ticket, palette, warnings })
  const svg = svgDocument({
    widthMm: pageW,
    heightMm: pageH,
    title: spec.caption || spec.name,
    desc: `${spec.name || 'chart'} · ${preset.label} · ${kind} · ${series.yKeys.join(' / ')} · ${pageW}×${pageH}mm`,
    defs: '',
    body: chart.body,
    background: palette.bg,
    meta: {
      type: 'chart',
      kind,
      journal: preset.id,
      palette: palette.id,
      font: spec.font,
      'font-pt': spec.font_size_pt,
    },
  })

  // 与 render 分开命名：data 图写 -chart.svg，结构图写 -diagram.svg
  const outFile = opts.out ? resolveIn(dir, opts.out) : join(dir, 'out', `${safeName(spec.name)}-chart.svg`)
  ensureDir(join(dir, 'out'))
  writeTextFile(outFile, svg)
  return { ok: true, svgPath: outFile, widthMm: round(pageW, 2), heightMm: round(pageH, 2), warnings, stats: chart.stats }
}

// ================================================================ 数据

function buildSeries(parsed, data, kind, warnings) {
  const { header, rows } = parsed
  const xKey = data.x && header.includes(data.x) ? data.x : header[0]
  let yKeys = (data.y || []).filter((k) => header.includes(k))
  if (!yKeys.length) {
    yKeys = header.filter((h) => h !== xKey)
    if (data.y && data.y.length) {
      warnings.push(
        warn('Y_COLUMN_MISSING', `data.y 里的列不在 CSV 里：${data.y.join(', ')}`, `CSV 表头是：${header.join(', ')}`),
      )
    }
  }
  // 误差列不参与作图
  yKeys = yKeys.filter((k) => !/(^|_)(sd|se|err|error|std|ci)$/i.test(k))
  if (!yKeys.length) {
    fail(
      `CSV 里没有可作图的数值列（表头：${header.join(', ')}）。`,
      '至少给一列数值，例如 group,method_a,method_b；再在 figure.json 的 data.y 里点名要画哪几列。',
      'NO_Y_COLUMN',
    )
  }

  const xRaw = rows.map((r) => r[xKey] ?? '')
  const numericX = xRaw.every((v) => Number.isFinite(toNumber(v)))
  const xValues = numericX ? xRaw.map((v) => toNumber(v)) : xRaw

  const yColumns = {}
  for (const key of yKeys) {
    const vals = []
    for (let i = 0; i < rows.length; i++) {
      const n = toNumber(rows[i][key])
      if (!Number.isFinite(n)) {
        warnings.push(warn('NON_NUMERIC', `第 ${i + 2} 行 ${key} 的值「${rows[i][key]}」不是数字，已跳过`, '检查 CSV 里是不是混了单位或空格。'))
      }
      vals.push(Number.isFinite(n) ? n : null)
    }
    yColumns[key] = vals
  }

  // 误差列：data.error 指定列名，或自动找 <col>_sd / <col>_se / <col>_err / sd 列
  const errors = {}
  for (const key of yKeys) {
    const cand = findErrorColumn(header, key, data.error)
    if (cand) errors[key] = rows.map((r) => {
      const n = toNumber(r[cand])
      return Number.isFinite(n) ? Math.abs(n) : 0
    })
  }
  if ((kind === 'errorbar' || data.error) && !Object.keys(errors).length) {
    warnings.push(
      warn(
        'NO_ERROR_COLUMN',
        '要画误差棒，但 CSV 里没找到误差列',
        '加一列 sd/se/err（或 <列名>_sd），然后在 data.error 里写列名。',
      ),
    )
  }

  return { xKey, xValues, numericX, yKeys, yColumns, errors, rows }
}

function findErrorColumn(header, yKey, hint) {
  if (hint && header.includes(hint)) return hint
  const candidates = [
    `${yKey}_sd`, `${yKey}_se`, `${yKey}_err`, `${yKey}_error`, `${yKey}_std`, `${yKey}_ci`,
    'sd', 'se', 'err', 'error', 'std',
  ]
  return candidates.find((c) => header.includes(c)) || null
}

// ================================================================ 样式

function makeStyle(spec, preset) {
  const fs = clamp(Number(spec.font_size_pt) || 7, 4, 24)
  const maxFs = Number(preset.max_font_pt) || fs
  const minFs = Number(preset.min_font_pt) || 5
  const ladder = fontLadder(fs, minFs, maxFs)
  return {
    fs: ladder[0],
    tickFs: ladder[ladder.length - 1], // 刻度数字用最小档，别抢戏
    titleFs: ladder[1] ?? ladder[0], // 轴标题比正文小半档
    legendFs: ladder[ladder.length - 1],
    leading: lineHeightMm(ladder[0]),
    fontFamily: spec.font || 'Arial',
  }
}

function chooseHeight(spec, data, opts, pageW) {
  const explicit = Number(opts.height_mm ?? data.height_mm ?? spec.height_mm)
  if (Number.isFinite(explicit) && explicit > 0) return explicit
  // 默认比例：单栏 89mm → 58mm；双栏 183mm → 72mm（接近期刊常见的 3:2 ~ 5:2）
  return pageW <= 110 ? 58 : 72
}

// ================================================================ 排版 + 绘制

function layoutChart({ series, kind, data, pageW, pageH, style, palette, warnings }) {
  const { xValues, yKeys, yColumns, errors, numericX } = series
  const n = xValues.length

  // ---- 1) 数值范围（含误差棒）
  const all = []
  for (const k of yKeys) {
    for (let i = 0; i < n; i++) {
      const v = yColumns[k][i]
      if (v === null) continue
      const e = errors[k]?.[i] || 0
      all.push(v - e, v + e)
    }
  }
  if (!all.length) fail('数据列全是空的，画不出图。', 'CSV 里至少要有几个数字。', 'NO_VALUES')
  const rawMin = Math.min(...all)
  const rawMax = Math.max(...all)
  const useLog = data.log === true && kind !== 'bar' && kind !== 'grouped-bar' && kind !== 'errorbar'
  if (data.log && !useLog) {
    warnings.push(warn('LOG_IGNORED', '柱状/误差棒图不支持对数轴，已按线性轴画', '想用对数轴请把 data.kind 改成 line 或 scatter。'))
  }
  const yScale = useLog ? makeLogScale(rawMin, rawMax, warnings) : makeLinearScale(rawMin, rawMax, kind)

  // ---- 2) 先量文字，再定绘图区（先算宽度，再决定 x 轴标签要不要斜排）
  const tickLabels = yScale.ticks.map((v) => formatNum(v, yScale.step))
  const yLabelW = Math.max(...tickLabels.map((t) => estimateTextWidthMm(t, style.tickFs)))
  const xTitleH = data.xlabel ? lineHeightMm(style.titleFs) + 1.4 : 0
  const yTitleH = data.ylabel ? lineHeightMm(style.titleFs) + 1.4 : 0

  const left = MARGIN_MM + yTitleH + yLabelW + TICK_LEN_MM + 1.2
  const right = MARGIN_MM + 1
  const top = MARGIN_MM + (data.legend !== false && yKeys.length > 1 ? legendHeight(style) : 0)
  const bottomBase = MARGIN_MM + xTitleH
  const plotX0 = left
  const plotW0 = Math.max(10, pageW - left - right)

  // 数值 x 轴（line/scatter 用真数值等距映射；柱状图仍按槽位排）
  const numericAxis = numericX && (kind === 'line' || kind === 'scatter')
  let xTicksData
  let xSc = null
  if (numericAxis) {
    xSc = linearScale(Math.min(...xValues), Math.max(...xValues), Math.max(2, Math.min(6, n)))
    const span = xSc.max - xSc.min || 1
    xTicksData = xSc.ticks.map((v) => ({ x: plotX0 + ((v - xSc.min) / span) * plotW0, label: formatNum(v, xSc.step) }))
  } else {
    xTicksData = xValues.map((v, i) => ({ x: plotX0 + (plotW0 * (i + 0.5)) / Math.max(1, n), label: String(v) }))
  }
  const xTickW = Math.max(...xTicksData.map((t) => estimateTextWidthMm(t.label, style.tickFs)))
  const slot = plotW0 / Math.max(1, xTicksData.length)
  const rotateX = xTickW > slot - 1.0

  const xTickH = rotateX
    ? Math.min(18, xTickW * Math.sin((35 * Math.PI) / 180) + 2)
    : lineHeightMm(style.tickFs) + TICK_LEN_MM + 1
  const bottom = bottomBase + xTickH + (rotateX ? 2.5 : 1)

  const plotX = left
  const plotY = top
  const plotW = plotW0
  const plotH = Math.max(10, pageH - top - bottom)

  let xAt
  if (numericAxis) {
    const span = xSc.max - xSc.min || 1
    xAt = (i) => plotX + ((xValues[i] - xSc.min) / span) * plotW
    xTicksData = xTicksData.map((t) => ({ ...t, x: plotX + ((t.x - plotX0) / plotW0) * plotW }))
  } else {
    xAt = (i) => (n === 1 ? plotX + plotW / 2 : plotX + (plotW * (i + 0.5)) / n)
    xTicksData = xTicksData.map((t, i) => ({ ...t, x: xAt(i) }))
  }
  const yAt = (v) => {
    const t = useLog
      ? (Math.log10(Math.max(v, yScale.min)) - Math.log10(yScale.min)) / (Math.log10(yScale.max) - Math.log10(yScale.min))
      : (v - yScale.min) / (yScale.max - yScale.min || 1)
    return plotY + plotH - clamp(t, 0, 1) * plotH
  }

  const parts = []

  // ---- 3) 轴线 + 刻度
  const axisColor = palette.edge
  const zeroY = yScale.min <= 0 && yScale.max >= 0 ? yAt(0) : null

  parts.push(
    group(
      { attrs: { 'data-role': 'axes' } },
      line({ x1: plotX, y1: plotY, x2: plotX, y2: plotY + plotH, stroke: axisColor, sw: SW.base }) +
        line({ x1: plotX, y1: plotY + plotH, x2: plotX + plotW, y2: plotY + plotH, stroke: axisColor, sw: SW.base }),
    ),
  )

  const yTicks = []
  yScale.ticks.forEach((v, i) => {
    const y = yAt(v)
    if (y < plotY - 0.2 || y > plotY + plotH + 0.2) return
    yTicks.push(
      line({ x1: plotX - TICK_LEN_MM, y1: y, x2: plotX, y2: y, stroke: axisColor, sw: SW.thin }) +
        text({
          x: plotX - TICK_LEN_MM - 0.9,
          y: y + style.tickFs * 0.352 * PT_TO_MM,
          content: tickLabels[i],
          size: style.tickFs,
          fill: palette.muted,
          anchor: 'end',
          role: 'axis-label',
        }),
    )
  })
  parts.push(group({ attrs: { 'data-role': 'y-ticks' } }, yTicks.join('')))

  const xTicks = []
  xTicksData.forEach((t) => {
    const y = plotY + plotH
    xTicks.push(line({ x1: t.x, y1: y, x2: t.x, y2: y + TICK_LEN_MM, stroke: axisColor, sw: SW.thin }))
    if (rotateX) {
      xTicks.push(
        text({
          x: t.x,
          y: y + TICK_LEN_MM + 1.6,
          content: t.label,
          size: style.tickFs,
          fill: palette.muted,
          anchor: 'end',
          role: 'axis-label',
          extra: { transform: `rotate(-35 ${fmtNum(t.x)} ${fmtNum(y + TICK_LEN_MM + 1.6)})` },
        }),
      )
    } else {
      xTicks.push(
        text({
          x: t.x,
          y: y + TICK_LEN_MM + 1.2 + style.tickFs * 0.352 * PT_TO_MM,
          content: t.label,
          size: style.tickFs,
          fill: palette.muted,
          anchor: 'middle',
          role: 'axis-label',
        }),
      )
    }
  })
  parts.push(group({ attrs: { 'data-role': 'x-ticks' } }, xTicks.join('')))

  // ---- 4) 轴标题
  if (data.xlabel) {
    parts.push(
      text({
        x: plotX + plotW / 2,
        y: pageH - MARGIN_MM,
        content: data.xlabel,
        size: style.titleFs,
        fill: palette.ink,
        anchor: 'middle',
        role: 'axis-label',
      }),
    )
  }
  if (data.ylabel) {
    const cx = MARGIN_MM
    const cy = plotY + plotH / 2
    parts.push(
      el(
        'g',
        { transform: `rotate(-90 ${fmtNum(cx)} ${fmtNum(cy)})` },
        text({
          x: cx,
          y: cy,
          content: data.ylabel,
          size: style.titleFs,
          fill: palette.ink,
          anchor: 'middle',
          role: 'axis-label',
        }),
      ),
    )
  }

  // ---- 5) 数据
  parts.push(drawSeries({ kind, series, palette, style, xAt, yAt, plotX, plotW, plotH, zeroY, warnings }))

  // ---- 6) 图例
  if (data.legend !== false && yKeys.length > 1) {
    parts.push(drawLegend({ yKeys, palette, style, plotX, y: MARGIN_MM, maxW: plotW }))
  }

  // ---- 7) 说明：数据点数太少/太多时给提示，不改图
  const stats = { kind, x: series.xKey, series: yKeys, points: n, yMin: round(yScale.min, 3), yMax: round(yScale.max, 3), log: useLog }
  return { body: parts.join('\n'), stats }
}

function legendHeight(style) {
  return lineHeightMm(style.legendFs) + 2
}

function drawLegend({ yKeys, palette, style, plotX, y, maxW }) {
  const items = []
  const fs = style.legendFs
  const swatch = 4
  let cursor = 0
  let row = 0
  const rowH = lineHeightMm(fs) + 1.6
  for (let i = 0; i < yKeys.length; i++) {
    const label = yKeys[i]
    const w = swatch + 1.2 + estimateTextWidthMm(label, fs) + 3.2
    if (cursor + w > maxW && cursor > 0) {
      row++
      cursor = 0
    }
    const x = plotX + cursor
    const yTop = y + row * rowH
    const color = chartColor(palette, i)
    items.push(
      rect({ x, y: yTop + fs * 0.35, w: swatch, h: 1.1, rx: 0.3, fill: color }) +
        text({
          x: x + swatch + 1.2,
          y: yTop + fs * 0.352 * PT_TO_MM + fs * 0.35,
          content: label,
          size: fs,
          fill: palette.ink,
          anchor: 'start',
          role: 'legend-label',
        }),
    )
    cursor += w
  }
  return group({ attrs: { 'data-role': 'legend' } }, items.join(''))
}

function drawSeries({ kind, series, palette, style, xAt, yAt, plotX, plotW, plotH, zeroY, warnings }) {
  const { yKeys, yColumns, xValues, errors } = series
  const n = xValues.length
  const out = []
  const grouped = kind === 'grouped-bar' || ((kind === 'bar' || kind === 'errorbar') && yKeys.length > 1)
  const slot = plotW / Math.max(1, n)
  const groupPad = Math.max(0.8, slot * 0.18)
  const usable = Math.max(0.8, slot - groupPad * 2)
  const MAX_BAR_MM = 16 // 柱子别宽到像色块，宽图上限制单根宽度
  let barW = grouped ? Math.max(0.8, (usable - (yKeys.length - 1) * 0.55) / yKeys.length) : Math.min(usable * 0.72, MAX_BAR_MM * 1.4)
  barW = Math.min(barW, MAX_BAR_MM)

  if (kind === 'line' || kind === 'scatter') {
    yKeys.forEach((key, si) => {
      const color = chartColor(palette, si)
      const pts = []
      for (let i = 0; i < n; i++) {
        const v = yColumns[key][i]
        if (v === null) continue
        pts.push({ x: xAt(i), y: yAt(v), v, i })
      }
      if (kind === 'line') {
        const d = pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${fmtNum(p.x)},${fmtNum(p.y)}`).join(' ')
        out.push(
          group(
            { attrs: { 'data-role': 'series', 'data-series': key } },
            d ? el('path', { d, fill: 'none', stroke: color, 'stroke-width': SW.node, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }) : '',
          ),
        )
      }
      const mark = pts
        .map((p) =>
          el('circle', {
            cx: fmtNum(p.x),
            cy: fmtNum(p.y),
            r: 0.75,
            fill: kind === 'scatter' ? color : palette.bg,
            stroke: color,
            'stroke-width': SW.thin,
          }),
        )
        .join('')
      out.push(group({ attrs: { 'data-role': 'markers', 'data-series': key } }, mark))
      // 误差棒：line/scatter 也挂（用同一个 yAt 映射）
      if (errors[key]) {
        const barItems = []
        for (const p of pts) {
          const e = errors[key][p.i] || 0
          if (!e) continue
          const top = yAt(p.v + e)
          const bot = yAt(p.v - e)
          barItems.push(
            line({ x1: p.x, y1: top, x2: p.x, y2: bot, stroke: color, sw: SW.thin }) +
              line({ x1: p.x - 0.7, y1: top, x2: p.x + 0.7, y2: top, stroke: color, sw: SW.thin }) +
              line({ x1: p.x - 0.7, y1: bot, x2: p.x + 0.7, y2: bot, stroke: color, sw: SW.thin }),
          )
        }
        if (barItems.length) out.push(group({ attrs: { 'data-role': 'error-bars', 'data-series': key } }, barItems.join('')))
      }
    })
    return group({ attrs: { 'data-role': 'data' } }, out.join(''))
  }

  // 柱状 / 分组柱状 / 误差棒
  yKeys.forEach((key, si) => {
    const color = chartColor(palette, si)
    const bars = []
    for (let i = 0; i < n; i++) {
      const v = yColumns[key][i]
      if (v === null) continue
      const cx = xAt(i)
      const groupW = grouped ? yKeys.length * barW + (yKeys.length - 1) * 0.55 : barW
      const x = grouped ? cx - groupW / 2 + si * (barW + 0.55) : cx - barW / 2
      const yv = yAt(v)
      const y0 = zeroY ?? plotY + plotH
      const y1 = Math.min(yv, y0)
      const hgt = Math.max(0.35, Math.abs(y0 - yv))
      bars.push(rect({ x, y: y1, w: barW, h: hgt, rx: 0.4, fill: color, stroke: null }))
      if (errors[key] && errors[key][i]) {
        const top = yAt(v + errors[key][i])
        const bot = yAt(v - errors[key][i])
        bars.push(
          line({ x1: x + barW / 2, y1: top, x2: x + barW / 2, y2: bot, stroke: palette.ink, sw: SW.thin }) +
            line({ x1: x + barW / 2 - 0.8, y1: top, x2: x + barW / 2 + 0.8, y2: top, stroke: palette.ink, sw: SW.thin }) +
            line({ x1: x + barW / 2 - 0.8, y1: bot, x2: x + barW / 2 + 0.8, y2: bot, stroke: palette.ink, sw: SW.thin }),
        )
      }
    }
    out.push(group({ attrs: { 'data-role': 'series', 'data-series': key } }, bars.join('')))
  })
  return group({ attrs: { 'data-role': 'data' } }, out.join(''))
}

// ================================================================ 坐标刻度

function makeLinearScale(rawMin, rawMax, kind) {
  let lo = rawMin
  let hi = rawMax
  if (kind === 'bar' || kind === 'grouped-bar' || kind === 'errorbar') {
    // 柱状图基线固定从 0 起，别放大差异
    lo = Math.min(0, lo)
    hi = Math.max(0, hi)
  }
  const sc = linearScale(lo, hi, 5)
  return { ...sc, ticks: sc.ticks, log: false }
}

function makeLogScale(rawMin, rawMax, warnings) {
  if (rawMin <= 0) {
    warnings.push(warn('LOG_NONPOSITIVE', '对数轴遇到 ≤0 的值，已按线性轴画', '对数轴要求所有值 > 0；要么删掉 0/负值，要么把 data.log 关掉。'))
    const sc = linearScale(rawMin, rawMax, 5)
    return { ...sc, log: false }
  }
  const e0 = Math.floor(Math.log10(rawMin))
  const e1 = Math.ceil(Math.log10(rawMax))
  const ticks = []
  for (let e = e0; e <= e1; e++) ticks.push(Number((10 ** e).toPrecision(12)))
  return { min: 10 ** e0, max: 10 ** e1, step: 0, ticks, log: true }
}

function formatNum(v, step) {
  const abs = Math.abs(v)
  if (abs >= 1e6) return `${round(v / 1e6, 1)}M`
  if (abs >= 1e4) return `${round(v / 1e3, abs >= 1e5 ? 0 : 1)}k`
  let digits = 0
  if (step > 0 && step < 1) digits = Math.min(4, Math.ceil(-Math.log10(step)))
  else if (Math.abs(v - Math.round(v)) > 1e-9) digits = 2
  return String(round(v, digits))
}

// 兼容导出，方便测试
export const __internals = { buildSeries, makeLinearScale, makeLogScale, chooseHeight }
