// scripts/spec.mjs
// brief.md → figure.json：本地规则解析，不联网、不花一分钱。
//
// 支持的 brief 写法（两种混用都行）：
//   1) YAML-ish 头：--- 开头，里面写 title / type / journal / width / font_size_pt ...
//   2) Markdown 分节：# 标题、## 图注、## 面板、## 节点、## 边、## 布局、## 数据
// 也接受纯自然语言 brief：从关键词猜类型与期刊，段落当图注，剩下的交给 render。
//
// 对外接口（BRIEF §5.3）：buildSpec(workDir, opts) / readSpec(workDir)
// 另给 CLI 用的：writeDefaultSpec / writeDefaultBrief / initWorkspace

import { basename, join } from 'node:path'
import {
  fail,
  warn,
  clamp,
  ensureDir,
  fileExists,
  readJSONFile,
  readTextFile,
  resolve,
  resolveIn,
  safeName,
  writeJSONFile,
  writeTextFile,
} from './lib/util.mjs'
import { defaultPresetId, getPreset, presetIds } from './lib/journal.mjs'
import { defaultPaletteId, getPalette, paletteIds } from './lib/palette.mjs'

/** 六种版式（chart 由 chart.mjs 渲染，这里只做类型归一） */
export const FIGURE_TYPES = ['pipeline', 'architecture', 'mechanism', 'comparison', 'concept', 'chart', 'toc']

export const NODE_KINDS = ['box', 'rounded', 'db', 'note', 'circle']
export const EDGE_KINDS = ['arrow', 'line', 'dashed']

// ================================================================ 默认 spec

/**
 * 内置默认图（也是 init 生成的那一份）：三段式方法框架。
 * @param {object} [overrides]
 */
export function defaultSpec(overrides = {}) {
  const base = {
    name: 'framework-overview',
    caption:
      '图 1  方法总体框架。(a) 双通道输入编码；(b) 跨模态对齐与一致性约束；(c) 下游任务预测。',
    type: 'pipeline',
    journal: 'nature',
    width: 'double',
    font: 'Arial',
    font_size_pt: 7,
    palette: 'okabe-ito',
    panels: [
      {
        id: 'a',
        title: '输入编码与融合',
        caption: '',
        nodes: [
          { id: 'n1', label: '文本编码', sub: 'BERT-base', kind: 'rounded', group: 'a' },
          { id: 'n2', label: '图像编码', sub: 'ViT-B/16', kind: 'rounded', group: 'a' },
          { id: 'n3', label: '跨模态融合', sub: 'cross-attention ×6', kind: 'rounded', group: 'a' },
          { id: 'n4', label: '一致性约束', sub: 'InfoNCE', kind: 'note', group: 'a' },
        ],
        edges: [
          { from: 'n1', to: 'n3', label: '', kind: 'arrow' },
          { from: 'n2', to: 'n3', label: '', kind: 'arrow' },
          { from: 'n3', to: 'n4', label: '对齐', kind: 'dashed' },
        ],
      },
      {
        id: 'b',
        title: '下游任务',
        caption: '',
        nodes: [
          { id: 'n5', label: '分类头', sub: 'linear', kind: 'rounded', group: 'b' },
          { id: 'n6', label: '预测输出', sub: 'top-1 / top-5', kind: 'rounded', group: 'b' },
          { id: 'n7', label: '评估指标', sub: 'Acc / F1', kind: 'box', group: 'b' },
        ],
        edges: [
          { from: 'n5', to: 'n6', label: '', kind: 'arrow' },
          { from: 'n6', to: 'n7', label: '', kind: 'arrow' },
        ],
      },
    ],
    edges: [{ from: 'n4', to: 'n5', label: '', kind: 'arrow' }],
    layout: { direction: 'left-right', gap_mm: 6, node_w_mm: 32, node_h_mm: 13 },
    data: {
      file: 'data/main.csv',
      kind: 'grouped-bar',
      x: 'group',
      y: ['method_a', 'method_b'],
      error: null,
      xlabel: '方法',
      ylabel: '准确率 (%)',
      legend: true,
    },
    notes: '默认示例图，换成自己的内容直接改 figure.json 或 brief.md。',
  }
  return deepMerge(base, overrides)
}

const DEFAULT_BRIEF = `---
name: framework-overview
title: 方法总体框架
type: pipeline
journal: nature
width: double
font_size_pt: 7
palette: okabe-ito
---

# 图注
图 1  方法总体框架。(a) 双通道输入编码后做跨模态融合，并用一致性约束对齐；(b) 下游任务头输出预测并评估。

## 面板
- a | 输入编码与融合
- b | 下游任务

## 节点
- n1 | 文本编码 | BERT-base | a | rounded
- n2 | 图像编码 | ViT-B/16 | a | rounded
- n3 | 跨模态融合 | cross-attention ×6 | a | rounded
- n4 | 一致性约束 | InfoNCE | a | note
- n5 | 分类头 | linear | b | rounded
- n6 | 预测输出 | top-1 / top-5 | b | rounded
- n7 | 评估指标 | Acc / F1 | b | box

## 边
- n1 -> n3
- n2 -> n3
- n3 -> n4 : 对齐 | dashed
- n4 -> n5 : 特征
- n5 -> n6
- n6 -> n7

## 布局
- direction: left-right
- gap_mm: 6
- node_w_mm: 40
- node_h_mm: 13
`

/** 占位 CSV：init 时放进 data/，保证 chart 开箱能跑 */
export const SAMPLE_CSV = `group,method_a,method_b,method_a_sd,method_b_sd
Baseline,71.2,73.5,1.4,1.2
Ours w/o align,76.8,78.1,1.1,1.3
Ours,82.4,84.9,0.9,1.0
`

// ================================================================ 对外接口

/**
 * 读工作区的 figure.json（已归一化）。
 * @param {string} workDir
 * @returns {object} spec（附加不可枚举的 __warnings）
 */
export function readSpec(workDir) {
  const dir = resolve(workDir || '.')
  const file = join(dir, 'figure.json')
  if (!fileExists(file)) {
    fail(
      `工作区里没有 figure.json：${file}`,
      '先跑 node scripts/fig.mjs init <工作区>，或 node scripts/fig.mjs spec <工作区> 从 brief.md 生成。',
      'MISSING_SPEC',
    )
  }
  const raw = readJSONFile(file, 'figure.json')
  const { spec, warnings } = normalizeSpec(raw, { workDir: dir })
  Object.defineProperty(spec, '__warnings', { value: warnings, enumerable: false, writable: false })
  Object.defineProperty(spec, '__workDir', { value: dir, enumerable: false, writable: false })
  return spec
}

/**
 * brief.md → figure.json（本地规则，不调模型）。
 * @param {string} workDir
 * @param {{brief?:string,out?:string,ai?:boolean,overrides?:object}} [opts]
 * @returns {Promise<{ok:true,specPath:string,spec:object,warnings:object[]}>}
 */
export async function buildSpec(workDir, opts = {}) {
  const dir = resolve(workDir || '.')
  ensureDir(dir)
  const briefFile = opts.brief ? resolveIn(dir, opts.brief) : join(dir, 'brief.md')
  const specFile = opts.out ? resolveIn(dir, opts.out) : join(dir, 'figure.json')

  const warnings = []
  let briefText = ''
  if (fileExists(briefFile)) {
    briefText = readTextFile(briefFile, 'brief.md')
  } else {
    warnings.push(
      warn(
        'BRIEF_MISSING',
        `没找到 ${basename(briefFile)}，先按默认模板生成 figure.json`,
        `在工作区里新建 ${basename(briefFile)}（可参照 examples/brief-example.md），再跑一次 spec。`,
      ),
    )
  }

  if (opts.ai) {
    warnings.push(
      warn(
        'AI_SPEC_SKIPPED',
        '--ai 需要 platform-tools 的 ai.mjs，本地规则已先行解析',
        '等 ai.mjs 落地后再用 --ai；现在这份 figure.json 是规则解析的，可以直接手改。',
      ),
    )
  }

  const parsed = briefText ? parseBrief(briefText) : { spec: {}, warnings: [] }
  const merged = deepMerge(defaultSpec(), parsed.spec, opts.overrides || {})
  const { spec, warnings: normWarn } = normalizeSpec(merged, { workDir: dir })
  spec.name = safeName(spec.name || basename(dir) || 'figure')
  writeJSONFile(specFile, spec)
  return { ok: true, specPath: specFile, spec, warnings: [...warnings, ...parsed.warnings, ...normWarn] }
}

/** 写一份默认 figure.json（init / spec 兜底用） */
export function writeDefaultSpec(workDir, overrides = {}) {
  const dir = resolve(workDir || '.')
  const { spec } = normalizeSpec(defaultSpec(overrides), { workDir: dir })
  const file = join(dir, 'figure.json')
  writeJSONFile(file, spec)
  return { specPath: file, spec }
}

/** 写一份带注释的 brief.md 模板 */
export function writeDefaultBrief(workDir, text = DEFAULT_BRIEF) {
  const dir = resolve(workDir || '.')
  const file = join(dir, 'brief.md')
  writeTextFile(file, text.endsWith('\n') ? text : `${text}\n`)
  return file
}

/**
 * 建工作区：brief.md + figure.json + data/main.csv + out/
 * @returns {{ok:true, workDir:string, files:string[]}}
 */
export function initWorkspace(workDir, opts = {}) {
  const dir = resolve(workDir || '.')
  ensureDir(dir)
  ensureDir(join(dir, 'data'))
  ensureDir(join(dir, 'out'))
  const files = []
  const briefText = opts.briefText || DEFAULT_BRIEF
  files.push(writeDefaultBrief(dir, briefText))
  const csv = join(dir, 'data', 'main.csv')
  if (!fileExists(csv)) {
    writeTextFile(csv, SAMPLE_CSV)
    files.push(csv)
  } else files.push(csv)
  const specFile = join(dir, 'figure.json')
  if (!fileExists(specFile) || opts.force) {
    files.push(writeDefaultSpec(dir, opts.specOverrides || {}).specPath)
  } else files.push(specFile)
  return { ok: true, workDir: dir, files }
}

// ================================================================ 归一化

/**
 * 把任意来源的 spec 归一成渲染器能吃的形状，并给出可读告警。
 * @returns {{spec:object, warnings:object[]}}
 */
export function normalizeSpec(raw, ctx = {}) {
  const warnings = []
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) {
    fail('figure.json 的根应该是一个对象 {}。', '参照 examples/spec-example.json 的结构重写。', 'BAD_SPEC_ROOT')
  }
  const workDir = ctx.workDir || '.'
  const out = {}

  out.name = safeName(raw.name || basename(resolve(workDir)) || 'figure')

  const typeRes = normalizeType(raw.type, warnings)
  out.type = typeRes

  const journalRes = normalizeJournal(raw.journal, warnings)
  out.journal = journalRes
  const preset = getPreset(journalRes)
  if (preset.fallbackFrom) {
    warnings.push(
      warn('JOURNAL_UNKNOWN', `不认识的期刊「${preset.fallbackFrom}」，已按 custom 兜底`, `可选：${presetIds().join(' / ')}`),
    )
  }

  out.width = raw.width === undefined || raw.width === null || raw.width === '' ? 'single' : raw.width
  out.height_mm = parseMm(raw.height_mm, null, warnings, 'height_mm')
  // dpi 为 null 表示该刊按矢量收稿（如 Nature 主图），不要拿 600dpi 去判它
  const presetDpi = Number.isFinite(Number(preset.dpi)) && preset.dpi !== null ? Number(preset.dpi) : null
  out.dpi =
    raw.dpi === undefined || raw.dpi === null || raw.dpi === ''
      ? presetDpi
      : clampInt(raw.dpi, 72, 2400, presetDpi || 600)
  out.font = typeof raw.font === 'string' && raw.font.trim() ? raw.font.trim() : (preset.fonts && preset.fonts[0]) || 'Arial'
  out.font_size_pt = clampNum(raw.font_size_pt, 4, 24, Math.max(6, Number(preset.min_font_pt) || 7))
  out.palette = normalizePalette(raw.palette, warnings)
  out.caption = typeof raw.caption === 'string' ? raw.caption.trim() : ''
  out.notes = typeof raw.notes === 'string' ? raw.notes.trim() : ''

  const panelRes = normalizePanels(raw.panels, raw.nodes, raw.edges, warnings)
  out.panels = panelRes.panels
  out.edges = panelRes.edges
  out.layout = normalizeLayout(raw.layout, out.type)
  out.data = normalizeData(raw.data)

  if (out.type === 'chart') {
    if (!out.data.file) {
      warnings.push(warn('CHART_NO_DATA', '类型是 chart 但 data.file 没写', '在 figure.json 的 data.file 里指向 data/*.csv。'))
    }
  } else if (!out.panels.length && out.type !== 'concept') {
    warnings.push(
      warn('NO_PANELS', '没有任何面板/节点，图会是空白的', '在 figure.json 里补 panels[].nodes，或用 brief.md 的「## 节点」段。'),
    )
  }
  return { spec: out, warnings }
}

function normalizeType(value, warnings) {
  if (!value) return 'pipeline'
  const s = String(value).trim().toLowerCase()
  const map = {
    pipeline: 'pipeline', 流程: 'pipeline', 流程链: 'pipeline', workflow: 'pipeline', flow: 'pipeline', 框架: 'pipeline',
    architecture: 'architecture', 架构: 'architecture', system: 'architecture', 系统: 'architecture', 结构: 'architecture',
    mechanism: 'mechanism', 机制: 'mechanism', 原理: 'mechanism', 机理: 'mechanism',
    comparison: 'comparison', 对比: 'comparison', 比较: 'comparison', ablation: 'comparison', 消融: 'comparison',
    concept: 'concept', 概念: 'concept', 示意: 'concept', 概念图: 'concept', illustration: 'concept',
    toc: 'toc', 目录图: 'toc', 'graphical abstract': 'toc', 图文摘要: 'toc', 摘要图: 'toc',
    chart: 'chart', 图: 'chart', 数据图: 'chart', 图表: 'chart', plot: 'chart', 数据: 'chart',
  }
  const hit = map[s]
  if (hit) return hit
  warnings.push(warn('TYPE_UNKNOWN', `不认识的图类型「${value}」，已按 pipeline 排`, `可选：${FIGURE_TYPES.join(' / ')}`))
  return 'pipeline'
}

function normalizeJournal(value, warnings) {
  if (!value) return defaultPresetId()
  const p = getPreset(value)
  return p.id
}

function normalizePalette(value, warnings) {
  const p = getPalette(value || defaultPaletteId())
  if (!p.fallbackFrom) return p.id
  warnings.push(
    warn('PALETTE_UNKNOWN', `不认识的配色「${value}」，已用默认色板`, `可选：${paletteIds().join(' / ')}`),
  )
  return p.id
}

function normalizeLayout(raw, type) {
  const src = raw && typeof raw === 'object' && !Array.isArray(raw) ? raw : {}
  const dirRaw = String(src.direction ?? '').toLowerCase()
  const defaultDir = type === 'mechanism' || type === 'comparison' ? 'top-down' : 'left-right'
  let direction = defaultDir
  if (['top-down', 'topdown', 'vertical', '上下', '纵向', '从上到下'].includes(dirRaw)) direction = 'top-down'
  else if (['left-right', 'leftright', 'horizontal', '左右', '横向', '从左到右'].includes(dirRaw)) direction = 'left-right'
  return {
    direction,
    gap_mm: clampNum(src.gap_mm, 1, 30, 6),
    node_w_mm: clampNum(src.node_w_mm, 10, 200, 32),
    node_h_mm: clampNum(src.node_h_mm, 6, 80, 13),
    group_gap_mm: clampNum(src.group_gap_mm, 1, 30, 4),
  }
}

function normalizeData(raw) {
  const src = raw && typeof raw === 'object' && !Array.isArray(raw) ? raw : {}
  const kinds = ['bar', 'line', 'scatter', 'grouped-bar', 'errorbar']
  let kind = String(src.kind ?? 'bar').trim().toLowerCase()
  const kindMap = { 柱状: 'bar', 柱状图: 'bar', 条形: 'bar', 曲线: 'line', 折线: 'line', 折线图: 'line', 散点: 'scatter', 散点图: 'scatter', 分组柱状: 'grouped-bar', 误差棒: 'errorbar' }
  kind = kindMap[kind] || kind
  if (!kinds.includes(kind)) kind = 'bar'
  return {
    file: typeof src.file === 'string' ? src.file.trim() : '',
    kind,
    x: src.x || null,
    y: Array.isArray(src.y) ? src.y.map(String) : src.y ? [String(src.y)] : [],
    error: src.error ?? null,
    xlabel: src.xlabel || '',
    ylabel: src.ylabel || '',
    legend: src.legend !== false,
    log: src.log === true || src.log === 'y' || src.log === 'log',
    height_mm: src.height_mm === undefined ? null : parseMm(src.height_mm, null, [], 'data.height_mm'),
  }
}

function normalizePanels(rawPanels, rawNodes, rawEdges, warnings) {
  let panels = Array.isArray(rawPanels) ? rawPanels.filter((p) => p && typeof p === 'object') : []
  const rootNodes = Array.isArray(rawNodes) ? rawNodes : []
  const rootEdges = Array.isArray(rawEdges) ? rawEdges : []

  // 容错：用户把 nodes 直接写在根上，自动塞进一个默认面板
  if (!panels.length && rootNodes.length) {
    panels = [{ id: 'a', title: '', nodes: rootNodes, edges: [] }]
  }
  if (!panels.length) return { panels: [], edges: normalizeEdges(rootEdges, [], warnings) }

  const usedPanelIds = new Set()
  const nodeIds = new Set()
  const outPanels = panels.map((p, pi) => {
    let id = safeName(p.id || letters(pi), letters(pi)).toLowerCase()
    if (usedPanelIds.has(id)) {
      const next = `${id}${pi + 1}`
      warnings.push(warn('PANEL_ID_DUP', `面板 id「${id}」重复，已改成「${next}」`, '给每个面板一个唯一 id。'))
      id = next
    }
    usedPanelIds.add(id)
    const nodes = (Array.isArray(p.nodes) ? p.nodes : [])
      .filter((n) => n && typeof n === 'object')
      .map((n, ni) => normalizeNode(n, id, ni, nodeIds, warnings))
    const edges = normalizeEdges(Array.isArray(p.edges) ? p.edges : [], nodes, warnings)
    return {
      id,
      title: str(p.title ?? p.label ?? ''),
      caption: str(p.caption ?? ''),
      nodes,
      edges,
    }
  })

  const allEdges = [...normalizeEdges(rootEdges, null, warnings)]
  for (const p of outPanels) allEdges.push(...p.edges)
  return { panels: outPanels, edges: allEdges }
}

function normalizeNode(n, panelId, index, seenIds, warnings) {
  let id = safeName(n.id || `n${index + 1}`, `n${index + 1}`)
  if (seenIds.has(id)) {
    const next = `${id}_${index + 1}`
    warnings.push(warn('NODE_ID_DUP', `节点 id「${id}」重复，已改成「${next}」`, '给每个节点一个唯一 id，边靠 id 连。'))
    id = next
  }
  seenIds.add(id)
  let kind = String(n.kind ?? 'rounded').trim().toLowerCase()
  const kindMap = { 圆角: 'rounded', 方框: 'box', 直角: 'box', 数据库: 'db', 仓库: 'db', 注释: 'note', 备注: 'note', 圆: 'circle', 椭圆: 'circle' }
  kind = kindMap[kind] || kind
  if (!NODE_KINDS.includes(kind)) {
    warnings.push(warn('NODE_KIND_UNKNOWN', `节点「${id}」的 kind「${n.kind}」不认识，按 rounded 画`, `可选：${NODE_KINDS.join(' / ')}`))
    kind = 'rounded'
  }
  return {
    id,
    label: str(n.label ?? n.title ?? id),
    sub: str(n.sub ?? n.note ?? ''),
    kind,
    group: str(n.group ?? panelId),
    color: typeof n.color === 'string' ? n.color : null,
  }
}

function normalizeEdges(list, nodes, warnings) {
  const known = nodes ? new Set(nodes.map((n) => n.id)) : null
  const out = []
  for (const e of list) {
    if (!e || typeof e !== 'object') continue
    const from = String(e.from ?? e.source ?? '').trim()
    const to = String(e.to ?? e.target ?? '').trim()
    if (!from || !to) {
      warnings.push(warn('EDGE_BAD', `边缺 from/to：${JSON.stringify(e)}`, '每条边都要有 from 和 to（节点 id）。'))
      continue
    }
    if (known && (!known.has(from) || !known.has(to))) {
      warnings.push(
        warn('EDGE_NODE_MISSING', `边 ${from} → ${to} 指向了本面板里不存在的节点`, '检查节点 id 是否拼错；跨面板的边写在工作区根的 edges 里。'),
      )
      continue
    }
    let kind = String(e.kind ?? 'arrow').trim().toLowerCase()
    const kindMap = { 虚线: 'dashed', 实线: 'line', 箭头: 'arrow' }
    kind = kindMap[kind] || kind
    if (!EDGE_KINDS.includes(kind)) kind = 'arrow'
    out.push({ from, to, label: str(e.label ?? ''), kind })
  }
  return out
}

// ================================================================ brief.md 解析

/**
 * 解析 brief.md，返回可以并入 spec 的部分。
 * @param {string} text
 * @returns {{spec:object, warnings:object[]}}
 */
export function parseBrief(text) {
  const warnings = []
  const spec = {}
  const src = String(text ?? '').replace(/\r\n/g, '\n')
  let body = src

  const fm = src.match(/^---\n([\s\S]*?)\n---[ \t]*\n?/)
  if (fm) {
    Object.assign(spec, parseKeyValueLines(fm[1].split('\n'), warnings))
    body = src.slice(fm[0].length)
  }

  const sections = splitSections(body)
  const rootEdges = []
  let nodes = []
  let panels = []
  let layout = {}
  let data = {}
  let caption = spec.caption || ''
  let title = spec.title || spec.name || ''

  for (const sec of sections) {
    const key = sectionKey(sec.heading)
    if (sec.level === 1 && !key && sec.heading) {
      // 一级标题当图名
      if (!title) title = sec.heading.trim()
      continue
    }
    if (key === 'title') {
      const t = firstText(sec.lines)
      if (t) title = t
    } else if (key === 'caption') {
      caption = firstParagraph(sec.lines) || caption
    } else if (key === 'panels') {
      panels = parsePanels(sec.lines, warnings)
    } else if (key === 'nodes') {
      nodes = parseNodes(sec.lines, warnings)
    } else if (key === 'edges') {
      rootEdges.push(...parseEdges(sec.lines, warnings))
    } else if (key === 'layout') {
      layout = { ...layout, ...parseKeyValueLines(sec.lines, warnings) }
    } else if (key === 'data') {
      data = { ...data, ...parseKeyValueLines(sec.lines, warnings) }
    } else if (key === 'notes') {
      spec.notes = firstParagraph(sec.lines) || spec.notes
    } else if (key === 'meta') {
      Object.assign(spec, parseKeyValueLines(sec.lines, warnings))
    } else if (sec.heading) {
      // 不认识的二级标题：当补充说明
      spec.notes = [spec.notes, firstParagraph(sec.lines)].filter(Boolean).join('\n')
    }
  }

  // 没有显式「## 节点」但写成了列表的，兜底按节点解析
  if (!nodes.length && !panels.length) {
    const intro = sections.find((s) => !s.heading)
    if (intro) {
      const guessed = parseNodes(intro.lines.filter((l) => l.trim().startsWith('- ')), warnings)
      if (guessed.length >= 2) nodes = guessed
      if (!caption) caption = firstParagraph(intro.lines) || caption
    }
  }

  if (title && !spec.name) spec.name = safeName(title)
  if (caption) spec.caption = caption

  // 自然语言兜底：从全文猜类型/期刊/配色
  if (!spec.type) {
    const t = guessType(`${title}\n${caption}\n${src}`)
    if (t) spec.type = t
  }
  if (!spec.journal) {
    const j = guessJournal(src)
    if (j) spec.journal = j
  }
  if (nodes.length || panels.length) {
    // 有面板但节点没写所属面板时，全塞进第一个面板
    if (panels.length && nodes.length) {
      for (const n of nodes) {
        const pid = n.group && panels.some((p) => p.id === n.group) ? n.group : panels[0].id
        const target = panels.find((p) => p.id === pid) || panels[0]
        n.group = target.id
        target.nodes.push({ ...n })
      }
      nodes = []
    }
    spec.panels = panels.length
      ? panels
      : [{ id: 'a', title: '', caption: '', nodes: nodes.map((n) => ({ ...n, group: 'a' })), edges: [] }]
  }
  if (rootEdges.length) spec.edges = rootEdges
  if (Object.keys(layout).length) spec.layout = layout
  if (Object.keys(data).length) spec.data = data

  return { spec: specFromBriefKeys(spec), warnings }
}

/** 把 brief 里的中文/别名键翻译成 spec 字段名 */
function specFromBriefKeys(raw) {
  const out = { ...raw }
  const map = {
    标题: 'name', 图名: 'name', title: 'name',
    图注: 'caption', 图题: 'caption', caption: 'caption',
    类型: 'type', 图类型: 'type', type: 'type',
    期刊: 'journal', journal: 'journal',
    宽度: 'width', 图宽: 'width', width: 'width',
    高度: 'height_mm', 图高: 'height_mm', height: 'height_mm', height_mm: 'height_mm',
    字号: 'font_size_pt', 字体大小: 'font_size_pt', font_size: 'font_size_pt', font_size_pt: 'font_size_pt',
    字体: 'font', font: 'font',
    配色: 'palette', 色板: 'palette', palette: 'palette',
    dpi: 'dpi',
  }
  for (const [k, v] of Object.entries(out)) {
    if (!map[k] || map[k] === k) continue
    // title 只是人看的标题：已经写了 name 就以 name 为准（name 决定输出文件名）
    if (map[k] === 'name' && out.name) {
      delete out[k]
      continue
    }
    out[map[k]] = v
    delete out[k]
  }
  // 简单键值里可能出现字符串数字
  if (typeof out.height_mm === 'string') out.height_mm = out.height_mm
  if (typeof out.font_size_pt === 'string') out.font_size_pt = Number(out.font_size_pt.replace(/pt$/i, ''))
  if (typeof out.width === 'string' && /^\d+$/.test(out.width)) out.width = Number(out.width)
  return out
}

function splitSections(body) {
  const lines = body.split('\n')
  const out = [{ heading: '', level: 0, lines: [] }]
  for (const line of lines) {
    const m = line.match(/^(#{1,6})\s+(.+?)\s*$/)
    if (m) {
      out.push({ heading: m[2].trim(), level: m[1].length, lines: [] })
    } else {
      out[out.length - 1].lines.push(line)
    }
  }
  return out
}

function sectionKey(heading) {
  const h = String(heading || '').trim().toLowerCase()
  if (!h) return ''
  const table = [
    ['title', ['标题', '图名', 'title', 'figure title']],
    ['caption', ['图注', '图题', 'caption', 'legend', 'figure caption']],
    ['panels', ['面板', '分栏', 'panels', 'panel', '子图']],
    ['nodes', ['节点', '模块', 'nodes', 'node', 'blocks']],
    ['edges', ['边', '连线', '关系', 'edges', 'edge', 'links', 'arrows']],
    ['layout', ['布局', '排版', 'layout']],
    ['data', ['数据', 'data', 'dataset']],
    ['notes', ['说明', '备注', '补充', 'notes', 'note', 'comment']],
    ['meta', ['参数', '设置', 'meta', 'spec', 'settings']],
  ]
  for (const [key, words] of table) {
    if (words.some((w) => h === w || h.includes(w))) return key
  }
  return ''
}

function parseKeyValueLines(lines, warnings) {
  const out = {}
  for (const raw of lines) {
    const line = raw.trim().replace(/^[-*+]\s*/, '')
    if (!line || line.startsWith('#')) continue
    const m = line.match(/^([\w\u4e00-\u9fa5-]+)\s*[:：]\s*(.+)$/)
    if (!m) continue
    out[m[1].trim()] = coerceScalar(m[2].trim(), warnings)
  }
  return out
}

function coerceScalar(v, warnings) {
  const s = String(v).trim().replace(/^["'「]|["'」]$/g, '')
  if (/^(true|yes|on|是)$/i.test(s)) return true
  if (/^(false|no|off|否)$/i.test(s)) return false
  if (/^-?\d+(\.\d+)?$/.test(s)) return Number(s)
  if (/^\d+(\.\d+)?mm$/i.test(s) || /^\d+(\.\d+)?(in|cm|pt)$/i.test(s)) return s
  if (/^\[(.*)\]$/.test(s)) {
    return s
      .slice(1, -1)
      .split(/[,，]/)
      .map((x) => coerceScalar(x, warnings))
      .filter((x) => x !== '')
  }
  return s
}

function parsePanels(lines, warnings) {
  const out = []
  for (const raw of lines) {
    const line = raw.trim()
    if (!line || /^[-=*]{3,}$/.test(line)) continue
    const cells = splitCells(line)
    if (!cells.length) continue
    const obj = cells.length >= 2 && cells.length <= 6 && !line.includes(':')
      ? { id: cells[0], title: cells[1], caption: cells[2] || '' }
      : null
    const kv = parseInlineKv(line)
    const panel = obj || (kv ? { id: kv.id || letters(out.length), title: kv.title || kv.label || '', caption: kv.caption || '' } : null)
    if (!panel) {
      // 只有标题：自动编号
      out.push({ id: letters(out.length), title: line.replace(/^[-*+]\s*/, ''), caption: '', nodes: [], edges: [] })
      continue
    }
    panel.id = safeName(panel.id || letters(out.length), letters(out.length)).toLowerCase()
    panel.title = str(panel.title)
    panel.caption = str(panel.caption)
    // 节点/边稍后挂进来（parseBrief 里按 group 分配）
    out.push({ id: panel.id, title: panel.title, caption: panel.caption, nodes: [], edges: [] })
  }
  return out
}

function parseNodes(lines, warnings) {
  const out = []
  let auto = 0
  for (const raw of lines) {
    const line = raw.trim()
    if (!line || line.startsWith('#') || /^[-=*]{3,}$/.test(line)) continue
    const kv = parseInlineKv(line)
    const cells = splitCells(line)
    let node = null
    if (kv && (kv.id || kv.label)) {
      node = {
        id: kv.id,
        label: kv.label || kv.title,
        sub: kv.sub || kv.note || '',
        group: kv.group || kv.panel || kv.g || null,
        kind: kv.kind || kv.type || 'rounded',
      }
    } else if (cells.length >= 2) {
      node = { id: cells[0], label: cells[1], sub: cells[2] || '', group: cells[3] || null, kind: cells[4] || 'rounded' }
    } else {
      auto++
      node = { id: `n${auto}`, label: line.replace(/^[-*+]\s*/, ''), sub: '', group: null, kind: 'rounded' }
    }
    node.id = safeName(node.id || `n${out.length + 1}`, `n${out.length + 1}`)
    node.label = str(node.label || node.id)
    out.push(node)
  }
  return out
}

function parseEdges(lines, warnings) {
  const out = []
  for (const raw of lines) {
    const line = raw.trim().replace(/^[-*+]\s*/, '')
    if (!line || line.startsWith('#')) continue
    const kv = parseInlineKv(line)
    if (kv && (kv.from || kv.source) && (kv.to || kv.target)) {
      out.push({
        from: String(kv.from || kv.source).trim(),
        to: String(kv.to || kv.target).trim(),
        label: str(kv.label || ''),
        kind: str(kv.kind || 'arrow'),
      })
      continue
    }
    // 形式：n1 -> n2 : 说明 | dashed
    const m = line.match(/^(.+?)\s*(?:->|→|=>|-->|—>)\s*([^:|]+?)\s*(?::\s*([^|]+))?\s*(?:\|\s*(\w+))?\s*$/)
    if (!m) {
      warnings.push(warn('EDGE_UNPARSED', `没看懂这条边：「${line}」`, '写法：n1 -> n2 : 说明，或 from: n1, to: n2。'))
      continue
    }
    const arrow = /-->|—>|虚线/.test(line)
    out.push({
      from: m[1].trim(),
      to: m[2].trim(),
      label: (m[3] || '').trim(),
      kind: (m[4] || (arrow ? 'dashed' : 'arrow')).trim(),
    })
  }
  return out
}

/** 「id: n1, label: 编码器」这类行内键值 */
function parseInlineKv(line) {
  const cleaned = line.replace(/^[-*+]\s*/, '')
  const parts = cleaned.split(/\s*[,;，；]\s*/)
  const obj = {}
  let recognized = 0
  const keys = ['id', 'label', 'sub', 'kind', 'type', 'group', 'panel', 'g', 'title', 'caption', 'from', 'to', 'source', 'target', 'note']
  for (const part of parts) {
    const m = part.match(/^([\w\u4e00-\u9fa5-]+)\s*[:：]\s*(.*)$/)
    if (!m) continue
    const k = m[1].trim().toLowerCase()
    if (!keys.includes(k)) continue
    obj[k] = m[2].trim()
    recognized++
  }
  return recognized ? obj : null
}

function splitCells(line) {
  const cleaned = line.replace(/^[-*+]\s*/, '')
  if (!/[|｜]/.test(cleaned)) return []
  return cleaned
    .split(/[|｜]/)
    .map((s) => s.trim())
    .filter((s) => s !== '')
}

function firstText(lines) {
  for (const l of lines) {
    const t = l.trim()
    if (t && !t.startsWith('#') && !/^[-=*]{3,}$/.test(t)) return t.replace(/^[-*+]\s*/, '')
  }
  return ''
}

function firstParagraph(lines) {
  const buf = []
  for (const l of lines) {
    const t = l.trim()
    if (!t) {
      if (buf.length) break
      continue
    }
    if (/^[-=*]{3,}$/.test(t)) continue
    buf.push(t.replace(/^[-*+]\s*/, ''))
  }
  return buf.join(' ').trim()
}

// ---------------------------------------------------------------- 自然语言猜测

const TYPE_HINTS = [
  ['toc', ['toc', '目录图', '图文摘要', 'graphical abstract', '图文概要']],
  ['comparison', ['对比', '比较', '消融', 'ablation', 'baseline', '优于']],
  ['mechanism', ['机制', '原理', '机理', 'mechanism', '如何工作']],
  ['architecture', ['架构', '系统结构', '模块图', 'architecture', 'pipeline 结构']],
  ['chart', ['实验数据', '实验图', '柱状', '折线', '散点', '准确率', '误差棒', 'chart']],
  ['concept', ['概念', '示意', '概念图', 'concept', 'idea']],
  ['pipeline', ['流程', '框架', '流程图', 'pipeline', 'workflow', '方法总体']],
]

function guessType(text) {
  const s = String(text || '').toLowerCase()
  for (const [type, words] of TYPE_HINTS) {
    if (words.some((w) => s.includes(w.toLowerCase()))) return type
  }
  return ''
}

const JOURNAL_HINTS = [
  ['nature', ['nature', '自然']],
  ['science', ['science', '科学']],
  ['cell', ['cell', '细胞']],
  ['ieee', ['ieee', 'transactions']],
  ['elsevier', ['elsevier', '爱思唯尔']],
  ['springer', ['springer', '施普林格', 'lncs']],
  ['acm', ['acm', 'chi', 'sigconf']],
  ['plos', ['plos']],
  ['thesis-cn', ['学位论文', '毕业论文', '硕士论文', '博士论文', '开题']],
]

function guessJournal(text) {
  const s = String(text || '').toLowerCase()
  for (const [id, words] of JOURNAL_HINTS) {
    if (words.some((w) => s.includes(w.toLowerCase()))) return id
  }
  return ''
}

// ================================================================ 小工具

function letters(i) {
  return String.fromCharCode(97 + (i % 26))
}

function str(v) {
  if (v === undefined || v === null) return ''
  return String(v).trim()
}

function clampNum(v, lo, hi, dflt) {
  const n = Number(v)
  if (!Number.isFinite(n)) return dflt
  return clamp(n, lo, hi)
}

function clampInt(v, lo, hi, dflt) {
  const n = Math.round(Number(v))
  if (!Number.isFinite(n)) return dflt
  return clamp(n, lo, hi)
}

/** '62mm' / '2.4in' / 62 → 毫米 */
export function parseMm(v, dflt = null, warnings = [], field = '') {
  if (v === undefined || v === null || v === '') return dflt
  if (typeof v === 'number' && Number.isFinite(v)) return v
  const s = String(v).trim().toLowerCase()
  const m = s.match(/^([\d.]+)\s*(mm|cm|in|pt)?$/)
  if (!m) {
    if (warnings) warnings.push(warn('BAD_MM', `${field} 看不懂「${v}」，忽略`, '写数字（毫米）或 60mm / 2.4in。'))
    return dflt
  }
  const unit = m[2] || 'mm'
  const n = Number(m[1])
  const factor = { mm: 1, cm: 10, in: 25.4, pt: 25.4 / 72 }[unit]
  return Math.round(n * factor * 100) / 100
}

function deepMerge(...objs) {
  const out = {}
  for (const o of objs) {
    if (!o || typeof o !== 'object') continue
    for (const [k, v] of Object.entries(o)) {
      if (v === undefined) continue
      if (Array.isArray(v)) out[k] = v.map((x) => (x && typeof x === 'object' ? { ...x } : x))
      else if (v && typeof v === 'object') out[k] = deepMerge(out[k], v)
      else out[k] = v
    }
  }
  return out
}

// 让 `node scripts/fig.mjs spec` 知道这些符号存在（避免 bundler 误判未使用）
export const _internal = { parseBrief, deepMerge }
