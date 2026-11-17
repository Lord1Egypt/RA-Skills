// scripts/lib/svg.mjs
// 极简 SVG 拼装：文档头、属性转义、矩形/线/路径/文字/分组、箭头 marker、圆角折线。
//
// 单位约定（与 Lead 对过口径，别改）：
//   · SVG 用户单位 = 1mm，viewBox="0 0 <宽mm> <高mm>"；
//   · 根节点同时给真实物理尺寸 width="89mm" height="60mm"，导出链路靠它算 @page size；
//   · 字号一律以 pt 入参（figure.json 的 font_size_pt），落盘时 ×0.3528 换成 mm。
//
// 语义属性（platform-tools 的 check.mjs 依赖，别用随机 class）：
//   · 节点外层 <g data-node-id="n1" data-kind="box">
//   · 文字 <text data-role="node-label|edge-label|panel-title|axis-label|caption|..." data-font-pt="7">

import { fmtNum, PT_TO_MM, ptToMm } from './util.mjs'

/** 期刊通用无衬线字体栈（本机实测中文可渲染；Arial 打头，投稿最稳） */
export const FONT_STACK =
  "Arial, Helvetica, 'PingFang SC', 'Noto Sans CJK SC', 'Microsoft YaHei', sans-serif"

const XML_ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' }

export function escXml(s) {
  return String(s ?? '').replace(/[&<>"']/g, (c) => XML_ESC[c])
}

/** 线宽（pt 入参 → mm 用户单位） */
export const SW = {
  hair: ptToMm(0.35),
  thin: ptToMm(0.5),
  base: ptToMm(0.6),
  node: ptToMm(0.75),
  bold: ptToMm(1.0),
  heavy: ptToMm(1.4),
}

/** 字号（pt）→ mm 用户单位；同时返回可读的字符串 */
export function fontMm(pt) {
  return fmtNum(pt * PT_TO_MM, 4)
}

function attrStr(attrs = {}) {
  const parts = []
  for (const [k, v] of Object.entries(attrs)) {
    if (v === null || v === undefined || v === false) continue
    if (v === true) {
      parts.push(k)
      continue
    }
    parts.push(`${k}="${escXml(typeof v === 'number' ? fmtNum(v) : v)}"`)
  }
  return parts.length ? ` ${parts.join(' ')}` : ''
}

/** 生成一个元素；children 为 null/'' 时自闭合 */
export function el(name, attrs = {}, children = null) {
  const a = attrStr(attrs)
  if (children === null || children === undefined || children === '') return `<${name}${a}/>`
  return `<${name}${a}>${children}</${name}>`
}

// ---------------------------------------------------------------- 文档

/**
 * 生成独立 SVG 文件内容。
 * @param {object} o
 * @param {number} o.widthMm 物理宽度（写进 width 属性，同时是 viewBox 宽度）
 * @param {number} o.heightMm 物理高度
 * @param {string} [o.defs] <defs> 内容
 * @param {string} [o.body] 图元
 * @param {string} [o.title] <title>
 * @param {string} [o.desc]
 * @param {string|null} [o.background] 底色；传 null 则透明
 * @param {string} [o.generator]
 * @param {object} [o.meta] 额外写进注释的键值（如 journal / type / dpi）
 */
export function svgDocument(o) {
  const {
    widthMm,
    heightMm,
    defs = '',
    body = '',
    title = '',
    desc = '',
    background = '#ffffff',
    generator = 'paper-figure',
    meta = {},
  } = o
  const w = fmtNum(widthMm, 2)
  const h = fmtNum(heightMm, 2)
  const metaLine = Object.entries(meta)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${v}`)
    .join(' ')
  const head = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    `<!-- ${escXml(generator)}${metaLine ? ` · ${escXml(metaLine)}` : ''}`,
    `     单位：1 用户单位 = 1mm；物理尺寸 ${w}mm × ${h}mm；viewBox="0 0 ${w} ${h}"`,
    `     字号：以 pt 声明，落盘 ×0.3528 换成 mm（1pt = 25.4/72 mm）。data-font-pt 保留原始 pt 值。 -->`,
    `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"` +
      ` width="${w}mm" height="${h}mm" viewBox="0 0 ${w} ${h}"` +
      ` shape-rendering="geometricPrecision" text-rendering="geometricPrecision">`,
  ]
  if (title) head.push(`<title>${escXml(title)}</title>`)
  if (desc) head.push(`<desc>${escXml(desc)}</desc>`)
  const bg = background ? el('rect', { x: 0, y: 0, width: w, height: h, fill: background }) : ''
  const out = [...head]
  if (defs) out.push(`<defs>${defs}</defs>`)
  if (bg) out.push(bg)
  out.push(body)
  out.push('</svg>')
  return `${out.filter(Boolean).join('\n')}\n`
}

// ---------------------------------------------------------------- 基元

export function rect(o) {
  const { x, y, w, h, rx = null, fill = 'none', stroke = null, sw = 0, dash = null, opacity = null } = o
  return el('rect', {
    x,
    y,
    width: w,
    height: h,
    rx: rx === null ? null : rx,
    ry: rx === null ? null : rx,
    fill,
    stroke,
    'stroke-width': stroke ? sw : null,
    'stroke-dasharray': dash,
    opacity,
  })
}

export function line(o) {
  const { x1, y1, x2, y2, stroke = '#333', sw = SW.base, dash = null, opacity = null, cap = 'butt' } = o
  return el('line', {
    x1,
    y1,
    x2,
    y2,
    stroke,
    'stroke-width': sw,
    'stroke-dasharray': dash,
    'stroke-linecap': cap,
    opacity,
  })
}

export function path(o) {
  const {
    d,
    fill = 'none',
    stroke = null,
    sw = SW.base,
    dash = null,
    markerEnd = null,
    opacity = null,
    cap = 'butt',
    join = 'round',
  } = o
  return el('path', {
    d,
    fill,
    stroke,
    'stroke-width': stroke ? sw : null,
    'stroke-dasharray': dash,
    'stroke-linecap': cap,
    'stroke-linejoin': join,
    'marker-end': markerEnd,
    opacity,
  })
}

export function circle(o) {
  const { cx, cy, r, fill = 'none', stroke = null, sw = SW.base, opacity = null } = o
  return el('circle', { cx, cy, r, fill, stroke, 'stroke-width': stroke ? sw : null, opacity })
}

export function polyline(o) {
  const {
    points,
    fill = 'none',
    stroke = '#333',
    sw = SW.base,
    dash = null,
    markerEnd = null,
    join = 'round',
    cap = 'butt',
    opacity = null,
  } = o
  const pts = points.map((p) => `${fmtNum(p.x)},${fmtNum(p.y)}`).join(' ')
  return el('polyline', {
    points: pts,
    fill,
    stroke,
    'stroke-width': sw,
    'stroke-dasharray': dash,
    'stroke-linejoin': join,
    'stroke-linecap': cap,
    'marker-end': markerEnd,
    opacity,
  })
}

export function group(o, children) {
  const { id = null, transform = null, opacity = null, clipPath = null, attrs = {} } = o || {}
  return el('g', { id, transform, opacity, 'clip-path': clipPath, ...attrs }, children)
}

/** 带语义的节点分组：check.mjs 靠 data-node-id / data-kind 定位 */
export function nodeGroup(o, children) {
  return el(
    'g',
    {
      'data-node-id': o.id,
      'data-kind': o.kind || 'box',
      'data-panel': o.panel || null,
      'data-x': fmtNum(o.x),
      'data-y': fmtNum(o.y),
      'data-w': fmtNum(o.w),
      'data-h': fmtNum(o.h),
    },
    children,
  )
}

// ---------------------------------------------------------------- 文字

/**
 * 单行文字：y 是基线坐标（不用 dominant-baseline，Illustrator/Inkscape 都稳）。
 * size 用 pt 入参，落盘换算成 mm；同时输出 data-font-pt 供检查器读取。
 */
export function text(o) {
  const {
    x,
    y,
    content,
    size = 7,
    fill = '#1a1a1a',
    anchor = 'middle',
    family = FONT_STACK,
    weight = 'normal',
    style = null,
    opacity = null,
    letterSpacing = null,
    role = null,
    extra = {},
  } = o
  return el(
    'text',
    {
      x,
      y,
      'font-family': family,
      'font-size': fontMm(size),
      'font-weight': weight,
      'font-style': style,
      fill,
      'text-anchor': anchor,
      'letter-spacing': letterSpacing,
      opacity,
      'data-role': role,
      'data-font-pt': size,
      ...extra,
    },
    escXml(content ?? ''),
  )
}

/** 以 (x, centerY) 垂直居中的单行文字 */
export function textCenterY(o) {
  const size = o.size ?? 7
  return text({ ...o, y: (o.centerY ?? 0) + size * 0.352 * PT_TO_MM })
}

/**
 * 多行文字块，整块以 (x, centerY) 垂直居中。
 * leading 单位 mm，默认 1.26 倍字号。
 */
export function textBlock(o) {
  const {
    x,
    centerY,
    lines = [],
    size = 7,
    leading = size * 1.25 * PT_TO_MM,
    fill = '#1a1a1a',
    anchor = 'middle',
    family = FONT_STACK,
    weight = 'normal',
    style = null,
    opacity = null,
    role = null,
    extra = {},
  } = o
  const arr = lines.filter((l) => l !== undefined && l !== null)
  if (!arr.length) return ''
  const n = arr.length
  const firstBase = centerY - ((n - 1) * leading) / 2 + size * 0.352 * PT_TO_MM
  const spans = arr
    .map((l, i) => {
      const dy = i === 0 ? 0 : leading
      const t = String(l ?? '')
      if (!t) return `<tspan x="${fmtNum(x)}" dy="${fmtNum(dy)}"> </tspan>`
      return `<tspan x="${fmtNum(x)}" dy="${fmtNum(dy)}">${escXml(t)}</tspan>`
    })
    .join('')
  return el(
    'text',
    {
      x,
      y: firstBase,
      'font-family': family,
      'font-size': fontMm(size),
      'font-weight': weight,
      'font-style': style,
      fill,
      'text-anchor': anchor,
      'xml:space': 'preserve',
      opacity,
      'data-role': role,
      'data-font-pt': size,
      ...extra,
    },
    spans,
  )
}

// ---------------------------------------------------------------- 箭头 / 折线

/**
 * 箭头 marker：markerUnits="strokeWidth"，箭头大小随线宽自动缩放（0.6pt 线 → 约 1.6mm 长）。
 * 使用时把路径末端往回缩 arrowInset，箭头尖与节点之间留 0.8–0.9mm 缝。
 * @param {{id:string,color?:string,scale?:number}} o scale = 箭头长度等于几个线宽，默认 9
 */
export function arrowMarker(o) {
  const { id, color = '#4a4a4a', scale = 9 } = o
  const w = scale
  const h = scale * 0.78
  return el(
    'marker',
    {
      id,
      viewBox: `0 0 ${fmtNum(w)} ${fmtNum(h)}`,
      refX: fmtNum(w * 0.94),
      refY: fmtNum(h / 2),
      markerWidth: fmtNum(w),
      markerHeight: fmtNum(h),
      markerUnits: 'strokeWidth',
      orient: 'auto',
    },
    el('path', { d: `M0,0 L${fmtNum(w)},${fmtNum(h / 2)} L0,${fmtNum(h)} L${fmtNum(w * 0.32)},${fmtNum(h / 2)} Z`, fill: color }),
  )
}

/** 端点小圆点 marker（「线」型边用） */
export function dotMarker(o) {
  const { id, color = '#4a4a4a', sizePt = 1.6 } = o
  const r = sizePt * PT_TO_MM
  return el(
    'marker',
    {
      id,
      viewBox: `0 0 ${fmtNum(r * 2)} ${fmtNum(r * 2)}`,
      refX: fmtNum(r),
      refY: fmtNum(r),
      markerWidth: fmtNum(r * 2),
      markerHeight: fmtNum(r * 2),
      markerUnits: 'userSpaceOnUse',
      orient: 'auto',
    },
    el('circle', { cx: r, cy: r, r: r * 0.9, fill: color }),
  )
}

/**
 * 把一串折点画成带圆角的路径（mm 坐标）。
 * @param {{x:number,y:number}[]} points
 * @param {number} r 圆角半径（mm）
 */
export function roundedPolyline(points, r = 0.8) {
  if (!points || points.length === 0) return ''
  if (points.length === 1) return `M${fmtNum(points[0].x)},${fmtNum(points[0].y)}`
  const p = points.map((q) => ({ x: Number(q.x), y: Number(q.y) }))
  let d = `M${fmtNum(p[0].x)},${fmtNum(p[0].y)}`
  for (let i = 1; i < p.length - 1; i++) {
    const prev = p[i - 1]
    const cur = p[i]
    const next = p[i + 1]
    const v1 = { x: prev.x - cur.x, y: prev.y - cur.y }
    const v2 = { x: next.x - cur.x, y: next.y - cur.y }
    const l1 = Math.hypot(v1.x, v1.y)
    const l2 = Math.hypot(v2.x, v2.y)
    if (l1 < 1e-6 || l2 < 1e-6) continue
    const rr = Math.min(r, l1 / 2, l2 / 2)
    const a = { x: cur.x + (v1.x / l1) * rr, y: cur.y + (v1.y / l1) * rr }
    const b = { x: cur.x + (v2.x / l2) * rr, y: cur.y + (v2.y / l2) * rr }
    d += ` L${fmtNum(a.x)},${fmtNum(a.y)} Q${fmtNum(cur.x)},${fmtNum(cur.y)} ${fmtNum(b.x)},${fmtNum(b.y)}`
  }
  const last = p[p.length - 1]
  d += ` L${fmtNum(last.x)},${fmtNum(last.y)}`
  return d
}

// ---------------------------------------------------------------- 线型预设（pt → mm）

const dashMm = (s) =>
  s
    .split(' ')
    .map((v) => fmtNum(Number(v) * PT_TO_MM))
    .join(' ')

export const DASH = {
  solid: null,
  dashed: dashMm('3 2'),
  dotted: dashMm('0.9 1.7'),
  dashdot: dashMm('4 1.6 0.9 1.6'),
  fine: dashMm('1.6 1.2'),
}

export function dashFor(kind) {
  if (!kind || kind === 'solid' || kind === 'arrow' || kind === 'line') return DASH.solid
  return DASH[kind] ?? null
}
