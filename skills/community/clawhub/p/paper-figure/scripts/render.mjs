// scripts/render.mjs
// figure.json → SVG。六种版式：pipeline / architecture / mechanism / comparison / concept / toc。
//
// 排版规则（都是毫米量纲，1 用户单位 = 1mm）：
//   · 画布宽 = 期刊单栏/双栏宽，高 = max(内容自然高, figure.json 的 height_mm)；
//   · 面板按行往下码；comparison 改成并排分栏；concept 放射状；toc 单行；
//   · 节点按边做拓扑分层（左→右 或 上→下），同层并排、跨层连线走间隙，不穿节点；
//   · 文字超宽先换行、再缩字号，缩到期刊下限还放不下才截断，每条都进 warnings。
//
// 对外接口（BRIEF §5.3）：renderFigure(workDir, opts) -> {ok,svgPath,widthMm,heightMm,warnings:[]}

import { join } from 'node:path'
import {
  clamp,
  ensureDir,
  estimateTextWidthMm,
  fontLadder,
  lineHeightMm,
  luminance,
  PT_TO_MM,
  resolveIn,
  round,
  safeName,
  tint,
  truncateToWidth,
  wrapText,
  warn,
  writeTextFile,
} from './lib/util.mjs'
import {
  DASH,
  FONT_STACK,
  SW,
  arrowMarker,
  circle,
  el,
  group,
  nodeGroup,
  path,
  rect,
  roundedPolyline,
  svgDocument,
  text,
  textBlock,
} from './lib/svg.mjs'
import { getPreset, resolveWidthMm } from './lib/journal.mjs'
import { getPalette, seriesColor } from './lib/palette.mjs'
import { readSpec } from './spec.mjs'

// ---------------------------------------------------------------- 尺寸常量（mm）

const MARGIN_MM = 3 // 统一内边距：自动裁高时上下各 3mm（白边合计约为画布 10%，≤12%）
const PANEL_GAP_MM = 3.6 // 面板间距
const NODE_PAD_X_MM = 1.3 // 节点内左右留白
const NODE_PAD_Y_MM = 1.0 // 节点内上下留白
const ARROW_INSET_MM = 0.9 // 箭头尖回缩，避免压住节点边线
const MIN_NODE_W_MM = 14 // 再窄就放不下两个字了
const LANE_OFFSET_MM = 3.2 // 回向边绕行车道距节点外沿的距离

// 版式签名色：每个面板一个调色板颜色。
// 跳过近黑色（Okabe-Ito 的 #000 是 Nature 的对照色）：大色块填纯黑太沉，留给描边和文字。
function panelColor(palette, i) {
  const usable = palette.colors.filter((c) => luminance(c) > 0.06)
  const list = usable.length ? usable : palette.colors
  return list[((i % list.length) + list.length) % list.length]
}

// ================================================================ 主入口

/**
 * 把工作区的 figure.json 渲染成 SVG。
 * @param {string} workDir 工作区目录
 * @param {{spec?:object,out?:string,journal?:string,width?:string|number,height_mm?:number,font_size_pt?:number}} [opts]
 * @returns {Promise<{ok:true,svgPath:string,widthMm:number,heightMm:number,warnings:object[]}>}
 */
export async function renderFigure(workDir, opts = {}) {
  const dir = opts.workDir || workDir || '.'
  const spec = opts.spec || readSpec(dir)

  // chart 类型直接转给图表引擎，命令面保持一条路
  if (spec.type === 'chart') {
    const { renderChart } = await import('./chart.mjs')
    const r = await renderChart(dir, { ...opts, spec })
    return { ...r, warnings: [...(spec.__warnings || []), ...(r.warnings || [])] }
  }

  const preset = getPreset(opts.journal || spec.journal)
  const palette = getPalette(spec.palette)
  const warnings = [...(spec.__warnings || []), ...(palette.fallbackFrom ? [] : [])]

  if (palette.fallbackFrom) {
    warnings.push(warn('PALETTE_FALLBACK', `配色「${palette.fallbackFrom}」不认识，已用 ${palette.id}`, '在 figure.json 里换成 assets/palettes.json 里的 id。'))
  }
  if (preset.fallbackFrom) {
    warnings.push(warn('JOURNAL_FALLBACK', `期刊「${preset.fallbackFrom}」不认识，已按 custom 兜底`, '在 figure.json 里换成支持的期刊 id。'))
  }

  const fontName = opts.font || spec.font
  if (preset.fonts && preset.fonts.length && !preset.fonts.some((f) => String(f).toLowerCase() === String(fontName).toLowerCase())) {
    warnings.push(
      warn(
        'FONT_NOT_ACCEPTED',
        `字体 ${fontName} 不在 ${preset.label} 推荐字体里`,
        `换成 ${preset.fonts.join(' / ')}，多数期刊只收 Arial/Helvetica 这类无衬线字体。`,
      ),
    )
  }

  const pageW = resolveWidthMm(preset, opts.width ?? spec.width)
  const ctx = {
    preset,
    palette,
    pageW,
    margin: MARGIN_MM,
    contentW: pageW - MARGIN_MM * 2,
    fs: clamp(Number(opts.font_size_pt ?? spec.font_size_pt) || 7, 4, 24),
    minFs: Number(preset.min_font_pt) || 5,
    layout: spec.layout,
    type: spec.type,
    fontFamily: fontName || 'Arial',
    warnings,
  }
  const maxFont = Number(preset.max_font_pt) || ctx.fs
  if (ctx.fs > maxFont + 1e-6) {
    warnings.push(
      warn(
        'FONT_TOO_LARGE',
        `字号 ${ctx.fs}pt 超过 ${preset.label} 的上限 ${maxFont}pt`,
        `把 font_size_pt 调到 ${preset.min_font_pt}–${maxFont} 之间（这类刊按最终尺寸量字号）。`,
      ),
    )
  }
  ctx.ladder = fontLadder(ctx.fs, ctx.minFs, maxFont)
  ctx.fs = ctx.ladder[0]
  ctx.subFs = ctx.ladder[1] ?? ctx.ladder[0]

  // ---- 1) 版式
  const plan = layoutFigure(spec, ctx)

  // ---- 2) 画布高度
  const naturalH = plan.height + MARGIN_MM * 2
  let pageH = naturalH
  const requested = Number(opts.height_mm ?? spec.height_mm)
  if (Number.isFinite(requested) && requested > 0) {
    if (requested + 0.01 < naturalH) {
      warnings.push(
        warn(
          'HEIGHT_TOO_SMALL',
          `设定高度 ${round(requested, 1)}mm 装不下内容（需要 ${round(naturalH, 1)}mm），已自动加高`,
          '把 height_mm 调大，或减少面板/节点、把 layout.gap_mm 和 node_h_mm 调小。',
        ),
      )
    }
    pageH = Math.max(naturalH, requested)
  }
  if (pageH > Number(preset.max_height_mm) + 0.01) {
    warnings.push(
      warn(
        'HEIGHT_EXCEEDS_JOURNAL',
        `图高 ${round(pageH, 1)}mm 超过 ${preset.label} 的版面上限 ${preset.max_height_mm}mm`,
        '拆成两个图，或减少面板数；也可以把 width 改成 double 让内容横向铺开。',
      ),
    )
  }
  if (!plan.nodes.length && spec.type !== 'concept') {
    warnings.push(warn('EMPTY_FIGURE', '图里一个节点都没有', '在 figure.json 的 panels[].nodes 里补节点，或改 type。'))
  }

  // ---- 3) 出图
  const body = drawFigure(spec, ctx, plan, pageH)
  const svg = svgDocument({
    widthMm: pageW,
    heightMm: pageH,
    title: spec.caption || spec.name,
    desc: buildDesc(spec, preset, pageW, pageH),
    defs: buildDefs(ctx),
    body,
    background: palette.bg,
    meta: {
      type: spec.type,
      journal: preset.id,
      palette: palette.id,
      dpi: spec.dpi,
      font: ctx.fontFamily,
      'font-pt': ctx.fs,
    },
  })

  // 产物命名带类型后缀：diagram 与 chart 各写各的，别互相覆盖
  const outFile = opts.out ? resolveIn(dir, opts.out) : join(dir, 'out', `${safeName(spec.name)}-diagram.svg`)
  ensureDir(join(dir, 'out'))
  writeTextFile(outFile, svg)
  return { ok: true, svgPath: outFile, widthMm: round(pageW, 2), heightMm: round(pageH, 2), warnings }
}

// ================================================================ 字号与文本

/** 行高 = 1.25 × 字号（Lead 明确口径） */
function textLeading(fontSizePt) {
  return lineHeightMm(fontSizePt, 1.25)
}

/** 节点上下留白下限 = 1.2 × 正文字号 */
function nodePadY(ctx) {
  return Math.max(1.0, 1.2 * ctx.fs * PT_TO_MM)
}

/** 按字号阶梯逐档试排：优先大字号，放不下就降一档，降到底再截断 */
function fitLadder(text, maxW, sizes, opts = {}) {
  const maxLines = opts.maxLines ?? 2
  const list = (sizes && sizes.length ? sizes : [7]).slice().sort((a, b) => b - a)
  for (const size of list) {
    const r = wrapText(text, maxW, size, opts)
    if (r.lines.length <= maxLines) {
      return { lines: r.lines, fontSizePt: size, shrunk: size < list[0] - 1e-6, truncated: false, overflow: r.overflow }
    }
  }
  const size = list[list.length - 1]
  const r = wrapText(text, maxW, size, opts)
  let lines = r.lines
  let truncated = false
  if (lines.length > maxLines) {
    lines = lines.slice(0, maxLines)
    const li = lines.length - 1
    lines[li] = truncateToWidth(lines[li], maxW, size, opts)
    truncated = true
  }
  return { lines, fontSizePt: size, shrunk: size < list[0] - 1e-6, truncated, overflow: r.overflow || truncated }
}

/**
 * 量一个节点：先按可用宽度排字，再决定高度。字太大就缩，仍放不下就截断。
 */
function measureNode(node, availW, ctx) {
  const w = Math.max(MIN_NODE_W_MM, availW)
  // note 的右上角折角要占地方，文字可用宽度相应收窄，别压到折角上
  const foldReserve = node.kind === 'note' ? Math.min(2.4, w * 0.12) : 0
  const innerW = Math.max(3, w - NODE_PAD_X_MM * 2 - foldReserve)
  const labelFit = fitLadder(node.label || node.id, innerW, ctx.ladder, { maxLines: 2 })
  const subSizes = ctx.ladder.filter((v) => v <= ctx.subFs + 1e-6)
  const subFit = node.sub ? fitLadder(node.sub, innerW, subSizes.length ? subSizes : [ctx.subFs], { maxLines: 1 }) : null
  const leadL = textLeading(labelFit.fontSizePt)
  const leadS = subFit ? textLeading(subFit.fontSizePt) : 0
  const textH = labelFit.lines.length * leadL + (subFit ? leadS : 0)
  const h = Math.max(ctx.layout.node_h_mm, textH + nodePadY(ctx) * 2)
  return { w, h, labelFit, subFit, leadL, leadS, textH }
}

function placeNode(node, x, y, m, ctx) {
  if (m.labelFit.shrunk) {
    ctx.warnings.push(
      warn(
        'NODE_FONT_SHRUNK',
        `节点「${node.label}」字号从 ${round(ctx.fs, 1)}pt 缩到 ${round(m.labelFit.fontSizePt, 1)}pt 才放得下`,
        '把节点文字改短，或调大 layout.node_w_mm / 减少同层节点数量。',
      ),
    )
  }
  if (m.labelFit.truncated) {
    ctx.warnings.push(
      warn(
        'NODE_LABEL_TRUNCATED',
        `节点「${node.label}」太长，已截断成「${m.labelFit.lines.join('')}」`,
        '把 label 压到 8 个字以内，短说明放 sub 字段。',
      ),
    )
  }
  return {
    ...node,
    x,
    y,
    w: m.w,
    h: m.h,
    measure: m,
    cx: x + m.w / 2,
    cy: y + m.h / 2,
  }
}

// ================================================================ 版式总控

function layoutFigure(spec, ctx) {
  // 画布边界（mm）：绕行车道 / 标签都不能越过它
  spec.__bounds = {
    minX: ctx.margin,
    minY: ctx.margin,
    maxX: ctx.pageW - ctx.margin,
    maxY: Number.MAX_SAFE_INTEGER,
  }
  const panels = (spec.panels || []).filter((p) => Array.isArray(p.nodes) && p.nodes.length)
  const ctxW = { ...ctx, contentW: ctx.contentW }

  if (ctx.type === 'concept') {
    return layoutConcept(spec, panels, ctxW)
  }
  if (ctx.type === 'comparison') {
    return layoutComparison(spec, panels, ctxW)
  }
  return layoutRows(spec, panels, ctxW, ctx.type === 'toc')
}

// ---------------------------------------------------------------- 竖排行（默认）

function layoutRows(spec, panels, ctx, isToc) {
  const x = ctx.margin
  const w = ctx.contentW
  let y = 0
  const placedPanels = []
  const allNodes = []
  const allEdges = []

  if (!panels.length) {
    return { height: 20, panels: [], nodes: [], edges: [], mode: 'rows' }
  }

  panels.forEach((panel, pi) => {
    const headerH = panelHeaderHeight(panel, ctx)
    const dir = isToc ? 'left-right' : ctx.layout.direction
    const r = layoutPanelContent({
      panel,
      x,
      y: y + headerH,
      w,
      dir,
      ctx,
      paletteIndex: pi,
      panelEdges: edgesForPanel(spec, panel),
    })
    placedPanels.push({ ...panel, headerH, bx: x, by: y, bw: w, bh: headerH + r.height, paletteIndex: pi })
    allNodes.push(...r.nodes)
    allEdges.push(...r.edges)
    y += headerH + r.height + (pi < panels.length - 1 ? PANEL_GAP_MM : 0)
  })

  const height = Math.max(...placedPanels.map((p) => p.by + p.bh), 0)
  attachCrossPanelEdges(spec, panels, allNodes, allEdges, false)
  return { height, panels: placedPanels, nodes: allNodes, edges: allEdges, mode: 'rows' }
}

// ---------------------------------------------------------------- 并排分栏（comparison）

function layoutComparison(spec, panels, ctx) {
  if (!panels.length) return { height: 20, panels: [], nodes: [], edges: [], mode: 'columns' }
  const n = panels.length
  const gap = Math.max(3, ctx.layout.gap_mm)
  const colW = (ctx.contentW - gap * (n - 1)) / n
  const placedPanels = []
  const allNodes = []
  const allEdges = []
  let maxH = 0

  panels.forEach((panel, pi) => {
    const x = ctx.margin + pi * (colW + gap)
    const headerH = panelHeaderHeight(panel, ctx)
    const r = layoutPanelContent({
      panel,
      x,
      y: headerH,
      w: colW,
      dir: 'top-down',
      ctx,
      paletteIndex: pi,
      panelEdges: edgesForPanel(spec, panel),
    })
    const bh = headerH + r.height
    placedPanels.push({ ...panel, headerH, bx: x, by: 0, bw: colW, bh, paletteIndex: pi })
    allNodes.push(...r.nodes)
    allEdges.push(...r.edges)
    maxH = Math.max(maxH, bh)
  })

  // 让每一栏内容在同一基线开始，栏高对齐（视觉上一排齐）
  for (const p of placedPanels) p.bh = maxH
  attachCrossPanelEdges(spec, panels, allNodes, allEdges, true)
  return { height: maxH, panels: placedPanels, nodes: allNodes, edges: allEdges, mode: 'columns' }
}

// ---------------------------------------------------------------- 放射（concept）

function layoutConcept(spec, panels, ctx) {
  const nodes = panels.flatMap((p) => p.nodes.map((n) => ({ ...n })))
  if (!nodes.length) return { height: 24, panels: [], nodes: [], edges: [], mode: 'radial' }

  const center = nodes[0]
  const others = nodes.slice(1)
  const cx = ctx.margin + ctx.contentW / 2
  const centerW = Math.min(ctx.contentW * 0.46, 52)
  const mC = measureNode(center, centerW, ctx)
  const nodeW = Math.min(
    others.length ? (ctx.contentW * 0.9) / Math.max(2, others.length) : centerW,
    34,
  )
  const measured = others.map((n) => measureNode(n, Math.max(MIN_NODE_W_MM, nodeW), ctx))
  const ringNodeH = Math.max(12, ...measured.map((m) => m.h), mC.h)
  const rx = Math.max(centerW * 0.9, (ctx.contentW - nodeW) / 2 - 1)
  const ry = Math.max(ringNodeH * 0.85, rx * 0.42)

  const ccy = ry + ringNodeH / 2 + Math.max(0, (mC.h - ringNodeH) / 2)
  const placedCenter = placeNode(center, cx - mC.w / 2, ccy - mC.h / 2, mC, ctx)
  const ring = []
  others.forEach((n, i) => {
    const m = measured[i]
    const ang = -Math.PI / 2 + (i * 2 * Math.PI) / Math.max(1, others.length)
    const px = cx + rx * Math.cos(ang) - m.w / 2
    const py = ccy + ry * Math.sin(ang) - m.h / 2
    ring.push(placeNode(n, px, py, m, ctx))
  })

  const allNodes = [placedCenter, ...ring]
  const edges = []
  const explicit = edgesForPanel(spec, panels[0] || { id: 'a', edges: [] })
  const list = explicit.length
    ? explicit
    : others.map((n, i) => ({ from: center.id, to: n.id, kind: 'arrow', label: '' }))
  for (const e of list) {
    const a = allNodes.find((n) => n.id === e.from)
    const b = allNodes.find((n) => n.id === e.to)
    if (!a || !b) continue
    const pts = straightEdge(a, b)
    edges.push({ ...e, points: pts, straight: true })
  }

  const height = ccy + ry + ringNodeH / 2 + MARGIN_MM
  const panel = {
    id: 'a',
    title: panels[0]?.title || '',
    caption: panels[0]?.caption || '',
    headerH: 0,
    bx: ctx.margin,
    by: 0,
    bw: ctx.contentW,
    bh: height,
    paletteIndex: 0,
    ellipse: { cx, cy: ccy, rx, ry },
  }
  return { height, panels: [panel], nodes: allNodes, edges, mode: 'radial' }
}

// ---------------------------------------------------------------- 单个面板的内容排版

function layoutPanelContent({ panel, x, y, w, dir, ctx, paletteIndex, panelEdges }) {
  const nodes = panel.nodes.map((n) => ({ ...n, group: n.group || panel.id }))
  const ids = new Set(nodes.map((n) => n.id))
  const edges = (panelEdges || []).filter((e) => ids.has(e.from) && ids.has(e.to) && e.from !== e.to)
  const gap = ctx.layout.gap_mm

  // 1) 拓扑分层
  const layers = assignLayers(nodes, edges)
  const order = [...layers.entries()].sort((a, b) => a[1] - b[1]).map(([id]) => id)
  const maxLayer = Math.max(0, ...layers.values())
  let layerCount = maxLayer + 1

  // 无边（或全在一层）时退化成网格
  const hasRealLayers = edges.length > 0 && layerCount > 1
  if (!hasRealLayers) {
    const cols = Math.max(1, Math.ceil(Math.sqrt(nodes.length)))
    layers.clear()
    order.forEach((id, i) => layers.set(id, i % cols))
    layerCount = Math.min(cols, nodes.length)
  }

  const groups = new Map()
  for (const id of order) {
    const L = layers.get(id)
    if (!groups.has(L)) groups.set(L, [])
    groups.get(L).push(id)
  }

  // 2) 量尺寸
  const layerKeys = [...groups.keys()].sort((a, b) => a - b)
  const horizontal = dir === 'left-right'
  const trackCount = layerKeys.length
  const trackAvail = horizontal ? (w - gap * (trackCount - 1)) / trackCount : (w - gap * (Math.max(...layerKeys.map((k) => groups.get(k).length)) - 1)) / Math.max(1, Math.max(...layerKeys.map((k) => groups.get(k).length)))

  // node_w_mm 是「偏好下限」：空间富裕时放大到 66mm 上限，让宽图排满而不是挤在中间
  const growCap = Math.max(ctx.layout.node_w_mm, Math.min(66, trackAvail))
  let nodeW = Math.min(trackAvail, growCap)
  if (nodeW < MIN_NODE_W_MM) {
    nodeW = trackAvail
    if (nodeW < MIN_NODE_W_MM) {
      ctx.warnings.push(
        warn(
          'NODE_TOO_NARROW',
          `同层节点太多，每个只剩 ${round(nodeW, 1)}mm 宽`,
          '把 layout.gap_mm 调小、减少同层节点，或把图宽改成 double。',
        ),
      )
    }
  }
  nodeW = Math.max(6, nodeW)

  const measures = new Map()
  for (const n of nodes) measures.set(n.id, measureNode(n, nodeW, ctx))

  // 3) 摆位
  const placed = new Map()
  let height = 0

  if (horizontal) {
    // 列：每层一列
    const colW = nodeW
    const totalW = trackCount * colW + gap * (trackCount - 1)
    const startX = x + Math.max(0, (w - totalW) / 2)
    const colHeights = layerKeys.map((k) => {
      const ids = groups.get(k)
      return ids.reduce((s, id) => s + measures.get(id).h, 0) + gap * (ids.length - 1)
    })
    height = Math.max(0, ...colHeights)
    layerKeys.forEach((k, ci) => {
      const ids = groups.get(k)
      const colX = startX + ci * (colW + gap)
      let cy = y + (height - colHeights[ci]) / 2
      for (const id of ids) {
        const m = measures.get(id)
        placed.set(id, placeNode(nodes.find((n) => n.id === id), colX, cy, m, ctx))
        cy += m.h + gap
      }
    })
  } else {
    // 行：每层一行
    const rows = layerKeys.map((k) => groups.get(k))
    const rowHeights = rows.map((ids) => Math.max(...ids.map((id) => measures.get(id).h)))
    const totalH = rowHeights.reduce((s, v) => s + v, 0) + gap * (rows.length - 1)
    height = totalH
    let cy = y
    rows.forEach((ids, ri) => {
      const rw = ids.length * nodeW + gap * (ids.length - 1)
      let cx = x + (w - rw) / 2
      for (const id of ids) {
        const m = measures.get(id)
        const nh = m.h
        const ny = cy + (rowHeights[ri] - nh) / 2
        placed.set(id, placeNode(nodes.find((n) => n.id === id), cx, ny, m, ctx))
        cx += m.w + gap
      }
      cy += rowHeights[ri] + gap
    })
  }

  const placedNodes = [...placed.values()].map((n) => ({ ...n, panelId: panel.id, paletteIndex }))
  const placedEdges = []
  for (const e of edges) {
    const a = placed.get(e.from)
    const b = placed.get(e.to)
    if (!a || !b) continue
    const routed = routeEdge(a, b, { horizontal, obstacles: placedNodes })
    placedEdges.push({ ...e, points: routed.points, straight: routed.straight })
  }

  // 4) 分组框（architecture 用：同一 group 的节点框成一个虚线区）
  const groupBoxes = computeGroupBoxes(placedNodes, panel.id)

  return { height, nodes: placedNodes, edges: placedEdges, groupBoxes, layers }
}

/** 拓扑分层：Kahn 最长路径；有环时把剩下的节点压到最后一层 */
function assignLayers(nodes, edges) {
  const layer = new Map()
  if (!nodes.length) return layer
  const ids = nodes.map((n) => n.id)
  const adj = new Map(ids.map((id) => [id, []]))
  const indeg = new Map(ids.map((id) => [id, 0]))
  for (const e of edges) {
    if (!adj.has(e.from) || !adj.has(e.to) || e.from === e.to) continue
    adj.get(e.from).push(e.to)
    indeg.set(e.to, indeg.get(e.to) + 1)
  }
  let frontier = ids.filter((id) => indeg.get(id) === 0)
  let level = 0
  let guard = 0
  while (frontier.length && guard++ < ids.length + 2) {
    for (const id of frontier) layer.set(id, level)
    const next = []
    for (const id of frontier) {
      for (const v of adj.get(id)) {
        indeg.set(v, indeg.get(v) - 1)
        if (indeg.get(v) === 0) next.push(v)
      }
    }
    frontier = next
    level++
  }
  for (const id of ids) if (!layer.has(id)) layer.set(id, level)
  return layer
}

/** 同一 group 的节点包一个虚线框 */
function computeGroupBoxes(placedNodes, panelId) {
  const byGroup = new Map()
  for (const n of placedNodes) {
    const g = n.group || panelId
    if (!g || g === panelId) continue // 和面板同名的 group 不画框，避免套娃
    if (!byGroup.has(g)) byGroup.set(g, [])
    byGroup.get(g).push(n)
  }
  const out = []
  for (const [g, list] of byGroup) {
    if (list.length < 1) continue
    const x0 = Math.min(...list.map((n) => n.x)) - 1.6
    const y0 = Math.min(...list.map((n) => n.y)) - 1.6
    const x1 = Math.max(...list.map((n) => n.x + n.w)) + 1.6
    const y1 = Math.max(...list.map((n) => n.y + n.h)) + 1.6
    out.push({ id: g, x: x0, y: y0, w: x1 - x0, h: y1 - y0 })
  }
  return out
}

/**
 * 跨面板的边：面板内的边已经在 layoutPanelContent 里画过，
 * 这里只补「起点终点不在同一面板」的边，用全图坐标路由（上下排的图会自然走竖线）。
 */
function attachCrossPanelEdges(spec, panels, allNodes, allEdges, horizontal) {
  const byId = new Map(allNodes.map((n) => [n.id, n]))
  const have = new Set(allEdges.map((e) => `${e.from}->${e.to}->${e.label || ''}`))
  const list = [...(Array.isArray(spec.edges) ? spec.edges : []), ...panels.flatMap((p) => (Array.isArray(p.edges) ? p.edges : []))]
  for (const e of list) {
    const a = byId.get(e.from)
    const b = byId.get(e.to)
    if (!a || !b || a === b) continue
    const key = `${e.from}->${e.to}->${e.label || ''}`
    if (have.has(key)) continue
    have.add(key)
    const routed = routeEdge(a, b, { horizontal, bounds: spec.__bounds, obstacles: allNodes })
    allEdges.push({ ...e, points: routed.points, straight: routed.straight, crossPanel: true })
  }
}

/** 版面自检：节点两两相交就报出来（网格排版本不该发生，发生了说明有 bug） */
function detectOverlaps(nodes) {
  const hits = []
  const boxes = nodes.filter((n) => n.w > 0 && n.h > 0)
  for (let i = 0; i < boxes.length; i++) {
    for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i]
      const b = boxes[j]
      const overlapX = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x)
      const overlapY = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y)
      if (overlapX > 0.15 && overlapY > 0.15) hits.push({ a: a.id, b: b.id, overlapX, overlapY })
    }
  }
  return hits
}

function edgesForPanel(spec, panel) {
  const own = Array.isArray(panel.edges) ? panel.edges : []
  const root = Array.isArray(spec.edges) ? spec.edges : []
  return [...own, ...root]
}

function panelHeaderHeight(panel, ctx) {
  const hasTitle = Boolean(panel.title) || Boolean(panel.id)
  if (!hasTitle && !panel.caption) return 0
  // 上边留 0.3mm 再排字，保证面板标号的字顶也在 3mm 安全边距以内
  const capMm = ctx.fs * 0.72 * PT_TO_MM
  const titleH = capMm + 0.3 + ctx.fs * 0.3 * PT_TO_MM + 1.0
  const capH = panel.caption ? lineHeightMm(ctx.subFs) + 0.6 : 0
  return titleH + capH
}

// ================================================================ 连线

/** 矩形边界上朝 (tx,ty) 方向的交点 */
function rectEdgePoint(box, tx, ty) {
  const cx = box.cx ?? box.x + box.w / 2
  const cy = box.cy ?? box.y + box.h / 2
  const dx = tx - cx
  const dy = ty - cy
  if (Math.abs(dx) < 1e-6 && Math.abs(dy) < 1e-6) return { x: cx, y: cy }
  const hw = box.w / 2
  const hh = box.h / 2
  const scale = Math.min(
    Math.abs(dx) > 1e-6 ? hw / Math.abs(dx) : Infinity,
    Math.abs(dy) > 1e-6 ? hh / Math.abs(dy) : Infinity,
  )
  return { x: cx + dx * scale, y: cy + dy * scale }
}

function shorten(points, inset) {
  if (points.length < 2 || inset <= 0) return points
  const out = points.map((p) => ({ ...p }))
  const a = out[out.length - 2]
  const b = out[out.length - 1]
  const dx = b.x - a.x
  const dy = b.y - a.y
  const len = Math.hypot(dx, dy)
  if (len <= inset) return out
  out[out.length - 1] = { x: b.x - (dx / len) * inset, y: b.y - (dy / len) * inset }
  return out
}

/**
 * 直角路由：先判断两个节点的相对位置，再选一条不穿节点的车道。
 * obstacles 传全图节点框——BRIEF 质量红线里「箭头不穿 node」就是靠这个保证的。
 * @returns {{points:{x,y}[], straight:boolean}}
 */
function routeEdge(a, b, opts = {}) {
  const bounds = opts.bounds || null
  const obstacles = (opts.obstacles || []).filter((o) => o && o.id !== a.id && o.id !== b.id)
  const cyA = a.y + a.h / 2
  const cyB = b.y + b.h / 2
  const cxA = a.x + a.w / 2
  const cxB = b.x + b.w / 2
  const yOverlap = a.y < b.y + b.h && b.y < a.y + a.h
  const hForward = b.x >= a.x + a.w - 0.4
  const vForward = b.y >= a.y + a.h - 0.4
  const hBackward = b.x + b.w <= a.x + 0.4

  // 水平前向：竖直段落在两列之间的空隙里，基本不会穿；仍检一遍
  if (hForward && (yOverlap || !vForward || Math.abs(cyB - cyA) < b.h)) {
    const x1 = a.x + a.w
    const x2 = b.x - ARROW_INSET_MM
    if (Math.abs(cyB - cyA) < 0.15) return { points: [{ x: x1, y: cyA }, { x: x2, y: cyB }], straight: true }
    const midX = pickLane({
      axis: 'x',
      preferred: x1 + (b.x - x1) / 2,
      from: x1,
      to: b.x,
      fixedA: cyA,
      fixedB: cyB,
      obstacles,
    })
    return { points: [{ x: x1, y: cyA }, { x: midX, y: cyA }, { x: midX, y: cyB }, { x: x2, y: cyB }], straight: false }
  }
  // 垂直前向：横向段最容易横穿其它节点（跨面板的边尤其），必须挑空档
  if (vForward) {
    const y1 = a.y + a.h
    const y2 = b.y - ARROW_INSET_MM
    if (Math.abs(cxB - cxA) < 0.15) {
      const blocked = !segmentClearY(cxA, y1, b.y, obstacles)
      if (!blocked) return { points: [{ x: cxA, y: y1 }, { x: cxB, y: y2 }], straight: true }
    }
    const midY = pickLane({
      axis: 'y',
      preferred: y1 + (b.y - y1) / 2,
      from: cxA,
      to: cxB,
      obstacles,
      bounds,
    })
    return { points: [{ x: cxA, y: y1 }, { x: cxA, y: midY }, { x: cxB, y: midY }, { x: cxB, y: y2 }], straight: false }
  }
  // 水平回向：从右侧绕出去（车道要留在画布内，否则导出会被裁）
  if (hBackward) {
    let laneX = Math.max(a.x + a.w, b.x + b.w) + LANE_OFFSET_MM
    if (bounds) laneX = Math.min(laneX, bounds.maxX - 0.6)
    return {
      points: [
        { x: a.x + a.w, y: cyA },
        { x: laneX, y: cyA },
        { x: laneX, y: cyB },
        { x: b.x + b.w + ARROW_INSET_MM, y: cyB },
      ],
      straight: false,
    }
  }
  // 垂直回向：从下方绕
  let laneY = Math.max(a.y + a.h, b.y + b.h) + LANE_OFFSET_MM
  if (bounds) laneY = Math.min(laneY, bounds.maxY - 0.6)
  return {
    points: [
      { x: cxA, y: a.y + a.h },
      { x: cxA, y: laneY },
      { x: cxB, y: laneY },
      { x: cxB, y: b.y + b.h + ARROW_INSET_MM },
    ],
    straight: false,
  }
}

/** 矩形的「外扩」版本，用来给车道留 0.5mm 余量 */
function inflated(box, pad = 0.5) {
  return { x: box.x - pad, y: box.y - pad, w: box.w + pad * 2, h: box.h + pad * 2, id: box.id }
}

/** 竖直段 x 从 y1 到 y2 是否不穿任何节点 */
function segmentClearY(x, y1, y2, obstacles) {
  const lo = Math.min(y1, y2)
  const hi = Math.max(y1, y2)
  return !obstacles.some((o) => {
    const b = inflated(o)
    return x > b.x && x < b.x + b.w && hi > b.y && lo < b.y + b.h
  })
}

/** 水平段 y 从 x1 到 x2 是否不穿任何节点 */
function segmentClearX(y, x1, x2, obstacles) {
  const lo = Math.min(x1, x2)
  const hi = Math.max(x1, x2)
  return !obstacles.some((o) => {
    const b = inflated(o)
    return y > b.y && y < b.y + b.h && hi > b.x && lo < b.x + b.w
  })
}

/**
 * 找一个「离理想位置最近、且不穿节点」的车道坐标。
 * axis='y'：横排车道（水平走线），候选是 y；axis='x'：竖排车道（竖直走线），候选是 x。
 */
function pickLane({ axis, preferred, from, to, fixedA, fixedB, obstacles, bounds }) {
  const clear = (v) =>
    axis === 'y' ? segmentClearX(v, from, to, obstacles) : segmentClearY(v, fixedA, fixedB, obstacles)
  const lo = bounds ? (axis === 'y' ? bounds.minY + 0.6 : bounds.minX + 0.6) : null
  const hi = bounds ? (axis === 'y' ? bounds.maxY - 0.6 : bounds.maxX - 0.6) : null
  for (let d = 0; d <= 80; d += 0.4) {
    for (const v of [preferred + d, preferred - d]) {
      if (lo !== null && (v < lo || v > hi)) continue
      if (clear(v)) return v
    }
  }
  return preferred
}

/** 放射状直连：两端都落在矩形边界上 */
function straightEdge(a, b) {
  const p1 = rectEdgePoint(a, b.cx, b.cy)
  const p2 = rectEdgePoint(b, a.cx, a.cy)
  const dx = p2.x - p1.x
  const dy = p2.y - p1.y
  const len = Math.hypot(dx, dy) || 1
  const end = { x: p2.x - (dx / len) * ARROW_INSET_MM, y: p2.y - (dy / len) * ARROW_INSET_MM }
  return [p1, end]
}

// ================================================================ 绘制

function buildDefs(ctx) {
  const edgeColor = ctx.palette.edge
  return [arrowMarker({ id: 'pf-arrow', color: edgeColor, scale: 9 }), arrowMarker({ id: 'pf-arrow-soft', color: ctx.palette.muted, scale: 8 })].join('\n')
}

function buildDesc(spec, preset, w, h) {
  return [
    `${spec.name || 'figure'} · ${preset.label} · ${spec.type}`,
    `${w}×${h}mm · 1 用户单位 = 1mm · 字号 ${spec.font_size_pt}pt`,
    spec.caption || '',
  ]
    .filter(Boolean)
    .join(' | ')
}

function drawFigure(spec, ctx, plan, pageH) {
  const parts = []
  const yShift = Math.max(0, (pageH - plan.height - MARGIN_MM * 2) / 2) + MARGIN_MM

  // 放射状的底圈先画
  for (const p of plan.panels) {
    if (p.ellipse) {
      parts.push(
        el(
          'g',
          { 'data-role': 'concept-ring' },
          el('ellipse', {
              cx: p.ellipse.cx,
              cy: p.ellipse.cy + yShift,
              rx: p.ellipse.rx,
              ry: p.ellipse.ry,
              fill: tint(panelColor(ctx.palette, 0), 0.94),
              stroke: ctx.palette.grid,
              'stroke-width': SW.thin,
              'stroke-dasharray': DASH.dashed,
            }),
        ),
      )
    }
  }

  // 分组框
  for (const p of plan.panels) {
    if (!p.groupBoxes) continue
    for (const g of p.groupBoxes) {
      parts.push(
        el(
          'g',
          { 'data-role': 'group-box', 'data-group-id': g.id },
          rect({
            x: g.x,
            y: g.y + yShift,
            w: g.w,
            h: g.h,
            rx: 2,
            fill: 'none',
            stroke: ctx.palette.muted,
            sw: SW.thin,
            dash: DASH.dashed,
          }) +
            text({
              x: g.x + 1.2,
              y: g.y + yShift + 2.2,
              content: g.id,
              size: ctx.subFs,
              fill: ctx.palette.muted,
              anchor: 'start',
              role: 'group-label',
            }),
        ),
      )
    }
  }

  // 先画线，节点压在线上
  parts.push(drawEdges(plan, ctx, yShift))
  parts.push(drawNodes(plan, ctx, yShift))
  parts.push(drawEdgeLabels(plan, ctx, yShift))
  parts.push(drawPanelHeaders(plan, ctx, yShift))

  return parts.filter(Boolean).join('\n')
}

function drawNodes(plan, ctx, yShift) {
  const groupChildren = []
  const colorMemo = new Map()

  for (const n of plan.nodes) {
    const colorIdx = Number.isFinite(n.paletteIndex) ? n.paletteIndex : 0
    const color = n.color || panelColor(ctx.palette, colorIdx)
    colorMemo.set(n.id, color)
    const fill = tint(color, 0.9)
    const y = n.y + yShift
    const m = n.measure

    let shape = ''
    const outline = { stroke: color, sw: SW.node }
    if (n.kind === 'box') {
      shape = rect({ x: n.x, y, w: n.w, h: n.h, fill, stroke: color, sw: SW.node })
    } else if (n.kind === 'circle') {
      shape = rect({ x: n.x, y, w: n.w, h: n.h, rx: Math.min(n.w, n.h) / 2, fill, stroke: color, sw: SW.node })
    } else if (n.kind === 'db') {
      shape = cylinderPath(n.x, y, n.w, n.h, fill, outline.stroke, outline.sw)
    } else if (n.kind === 'note') {
      shape = notePath(n.x, y, n.w, n.h, fill, outline.stroke, outline.sw)
    } else {
      shape = rect({ x: n.x, y, w: n.w, h: n.h, rx: 1.6, fill, stroke: color, sw: SW.node })
    }

    // 文字：整块垂直居中
    const blockH = m.labelFit.lines.length * m.leadL + (m.subFit ? m.leadS : 0)
    const cy = y + n.h / 2
    const labelCenter = cy - blockH / 2 + (m.labelFit.lines.length * m.leadL) / 2
    const subCenter = cy + blockH / 2 - m.leadS / 2
    const texts = [
      textBlock({
        x: n.x + n.w / 2,
        centerY: labelCenter,
        lines: m.labelFit.lines,
        size: m.labelFit.fontSizePt,
        leading: m.leadL,
        fill: ctx.palette.ink,
        role: 'node-label',
        extra: { 'data-node-id': n.id },
      }),
      m.subFit
        ? textBlock({
            x: n.x + n.w / 2,
            centerY: subCenter,
            lines: m.subFit.lines,
            size: m.subFit.fontSizePt,
            leading: m.leadS,
            fill: ctx.palette.muted,
            role: 'node-sub',
            extra: { 'data-node-id': n.id },
          })
        : '',
    ].join('')

    groupChildren.push(nodeGroup({ id: n.id, kind: n.kind, panel: n.group, x: n.x, y, w: n.w, h: n.h }, shape + texts))
  }
  return group({ attrs: { 'data-role': 'nodes' } }, groupChildren.join(''))
}

function cylinderPath(x, y, w, h, fill, stroke, sw) {
  const ry = Math.min(2.4, h * 0.18)
  const rx = w / 2
  const body = `M${x},${y + ry} A${rx},${ry} 0 0 1 ${x + w},${y + ry} L${x + w},${y + h - ry} A${rx},${ry} 0 0 1 ${x},${y + h - ry} Z`
  const top = `M${x},${y + ry} A${rx},${ry} 0 0 0 ${x + w},${y + ry}`
  return (
    path({ d: body, fill, stroke, sw }) +
    path({ d: top, fill: 'none', stroke, sw: sw * 0.85 })
  )
}

function notePath(x, y, w, h, fill, stroke, sw) {
  // 折角控制在 2.4mm 以内：太大会啃掉第一行文字
  const fold = Math.min(2.4, Math.min(w, h) * 0.2, w * 0.12)
  const d = `M${x},${y} L${x + w - fold},${y} L${x + w},${y + fold} L${x + w},${y + h} L${x},${y + h} Z`
  const foldLine = `M${x + w - fold},${y} L${x + w - fold},${y + fold} L${x + w},${y + fold}`
  return path({ d, fill, stroke, sw }) + path({ d: foldLine, fill: 'none', stroke, sw: sw * 0.8 })
}

function drawEdges(plan, ctx, yShift) {
  const stroke = ctx.palette.edge
  const out = []
  for (const e of plan.edges) {
    if (!e.points || e.points.length < 2) continue
    const pts = e.points.map((p) => ({ x: p.x, y: p.y + yShift }))
    const dashed = e.kind === 'dashed'
    const isLine = e.kind === 'line'
    const d = pts.length === 2 && e.straight ? `M${fmt(pts[0].x)},${fmt(pts[0].y)} L${fmt(pts[1].x)},${fmt(pts[1].y)}` : roundedPolyline(pts, 0.9)
    out.push(
      el(
        'g',
        { 'data-role': 'edge', 'data-from': e.from, 'data-to': e.to },
        path({
          d,
          fill: 'none',
          stroke: isLine ? ctx.palette.muted : stroke,
          sw: SW.thin,
          dash: dashed ? DASH.dashed : isLine ? DASH.solid : null,
          markerEnd: isLine ? null : 'url(#pf-arrow)',
        }),
      ),
    )
  }
  return group({ attrs: { 'data-role': 'edges' } }, out.join(''))
}

function drawEdgeLabels(plan, ctx, yShift) {
  const out = []
  for (const e of plan.edges) {
    if (!e.label || !e.points || e.points.length < 2) continue
    // 标签落在整条折线（按弧长）的中点，再沿法线往外让 1mm：
    // 这样 elbow 三段式的边，标签始终贴在线上，而不是飘在两条线中间的空当里。
    const midSeg = pathMidpoint(e.points)
    if (!midSeg) continue
    const fs = ctx.subFs
    const gap = 1.0
    const mid = {
      x: midSeg.x + (midSeg.horizontal ? 0 : gap),
      y: midSeg.y + (midSeg.horizontal ? -gap : 0),
    }
    const wText = estimateTextWidthMm(e.label, fs)
    const bx = mid.x - wText / 2 - 0.7
    const by = mid.y + yShift - fs * PT_TO_MM * 0.86
    out.push(
      rect({ x: bx, y: by, w: wText + 1.4, h: fs * PT_TO_MM * 1.25 + 0.5, rx: 0.5, fill: ctx.palette.bg, opacity: 0.94 }),
      text({
        x: mid.x,
        y: mid.y + yShift + fs * PT_TO_MM * 0.2,
        content: e.label,
        size: fs,
        fill: ctx.palette.muted,
        role: 'edge-label',
        extra: { 'data-from': e.from, 'data-to': e.to },
      }),
    )
  }
  return group({ attrs: { 'data-role': 'edge-labels' } }, out.join(''))
}

function drawPanelHeaders(plan, ctx, yShift) {
  const out = []
  for (const p of plan.panels) {
    if (!p.title && !p.caption && !p.id) continue
    const fs = ctx.fs
    const baseY = p.by + yShift + fs * 0.72 * PT_TO_MM + 0.3
    const letterX = p.bx
    let nextX = letterX
    if (p.id) {
      out.push(
        text({
          x: letterX,
          y: baseY,
          content: p.id,
          size: fs,
          fill: ctx.palette.ink,
          anchor: 'start',
          weight: 'bold',
          role: 'panel-letter',
        }),
      )
      nextX = letterX + 2.4
    }
    if (p.title) {
      out.push(
        text({
          x: nextX,
          y: baseY,
          content: p.title,
          size: fs,
          fill: ctx.palette.ink,
          anchor: 'start',
          role: 'panel-title',
        }),
      )
    }
    if (p.caption) {
      out.push(
        text({
          x: p.bx,
          y: baseY + ctx.subFs * 1.3 * PT_TO_MM + 0.4,
          content: p.caption,
          size: ctx.subFs,
          fill: ctx.palette.muted,
          anchor: 'start',
          role: 'caption',
        }),
      )
    }
  }
  return group({ attrs: { 'data-role': 'panel-headers' } }, out.join(''))
}

// ---------------------------------------------------------------- 绘图小工具

function fmt(v) {
  const n = Number(v)
  return Number.isFinite(n) ? String(Math.round(n * 1000) / 1000) : '0'
}

/**
 * 折线按弧长取中点，返回中点坐标与所在段的方向（水平/垂直）。
 * 边标签就贴这儿——elbow 三段式里，取「最长段的中点」会飘。
 */
function pathMidpoint(points) {
  if (!points || points.length < 2) return null
  const segs = []
  let total = 0
  for (let i = 1; i < points.length; i++) {
    const a = points[i - 1]
    const b = points[i]
    const len = Math.hypot(b.x - a.x, b.y - a.y)
    segs.push({ a, b, len, start: total })
    total += len
  }
  if (total < 0.5) return null
  const target = total / 2
  const seg = segs.find((sg) => target >= sg.start && target <= sg.start + sg.len) || segs[segs.length - 1]
  const t = seg.len > 1e-6 ? (target - seg.start) / seg.len : 0
  return {
    x: seg.a.x + (seg.b.x - seg.a.x) * t,
    y: seg.a.y + (seg.b.y - seg.a.y) * t,
    horizontal: Math.abs(seg.b.x - seg.a.x) >= Math.abs(seg.b.y - seg.a.y),
  }
}

// 兼容：有些调用方会直接 import 这些常量做检查
export const LAYOUT_CONSTANTS = {
  MARGIN_MM,
  PANEL_GAP_MM,
  NODE_PAD_X_MM,
  NODE_PAD_Y_MM,
  ARROW_INSET_MM,
}

// 给测试/排障用的内部句柄（不属于公共契约，别在别处依赖）
export const __internals = { layoutFigure, assignLayers, routeEdge, measureNode }
