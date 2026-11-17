import { isScrollableOverflow } from './navigation.js'

const STYLE_KEYS = [
  'width',
  'height',
  'minWidth',
  'minHeight',
  'overflow',
  'overflowX',
  'overflowY',
  'maxWidth',
  'maxHeight',
]

/** 节点当前是否因 overflow 产生可滚动溢出 */
export function isExpandableOverflowNode(el) {
  if (!el || el.nodeType !== 1) return false
  const style = window.getComputedStyle(el)
  const canY = isScrollableOverflow(style.overflowY) && el.scrollHeight > el.clientHeight + 1
  const canX = isScrollableOverflow(style.overflowX) && el.scrollWidth > el.clientWidth + 1
  return canY || canX
}

function depthFrom(rootEl, el) {
  let depth = 0
  let node = el
  while (node && node !== rootEl) {
    depth += 1
    node = node.parentElement
  }
  return depth
}

/**
 * 收集需撑开的节点：可滚动节点 + 上溯到 root 的祖先。
 * 深节点在前，先撑内层再撑外壳（避免 grid / width:100% 把外框卡死）。
 */
export function listExpandableNodes(rootEl) {
  if (!rootEl) return []
  const scrollables = []
  const visit = (node) => {
    const children = node.children ? Array.from(node.children) : []
    for (const child of children) visit(child)
    if (node === rootEl || isExpandableOverflowNode(node)) scrollables.push(node)
  }
  visit(rootEl)

  const set = new Set(scrollables)
  for (const el of scrollables) {
    // root 本身已在集合中；从它的父节点继续上溯会越过 screen 边界，
    // 把 ScreenFrame、canvas、board 甚至 body/html 一并改写。
    if (el === rootEl) continue
    let node = el.parentElement
    while (node) {
      set.add(node)
      if (node === rootEl) break
      node = node.parentElement
    }
  }

  return [...set].sort((a, b) => depthFrom(rootEl, b) - depthFrom(rootEl, a))
}

export function snapshotInlineBox(el) {
  const out = {}
  for (const key of STYLE_KEYS) out[key] = el.style[key] || ''
  return out
}

export function restoreInlineBox(el, snapshot) {
  for (const key of STYLE_KEYS) {
    el.style[key] = snapshot[key] || ''
  }
}

/**
 * offsetTop / offsetLeft 相对 offsetParent，而不一定相对直接父节点。
 * 后台页里连续的 static 容器通常共享 screen root 作为 offsetParent，
 * 因此需要先换算到当前父节点坐标，避免逐层重复累加同一段偏移。
 */
function childStartWithin(el, child, axis) {
  const offsetKey = axis === 'x' ? 'offsetLeft' : 'offsetTop'
  const rectStart = axis === 'x' ? 'left' : 'top'
  const rectSize = axis === 'x' ? 'width' : 'height'
  const layoutSize = axis === 'x' ? 'offsetWidth' : 'offsetHeight'
  const scrollKey = axis === 'x' ? 'scrollLeft' : 'scrollTop'
  const childOffset = child[offsetKey] || 0

  if (child.offsetParent === el) return childOffset
  if (child.offsetParent && child.offsetParent === el.offsetParent) {
    return childOffset - (el[offsetKey] || 0)
  }

  if (typeof el.getBoundingClientRect === 'function'
    && typeof child.getBoundingClientRect === 'function') {
    const parentRect = el.getBoundingClientRect()
    const childRect = child.getBoundingClientRect()
    const renderedSize = parentRect[rectSize]
    const scale = el[layoutSize] > 0 && renderedSize > 0
      ? renderedSize / el[layoutSize]
      : 1
    const start = (childRect[rectStart] - parentRect[rectStart]) / scale
      + (el[scrollKey] || 0)
    if (Number.isFinite(start)) return start
  }

  return childOffset
}

/**
 * overflow:visible 时部分浏览器 scrollWidth ≈ clientWidth，
 * 所以再扫子节点 offset 边界，避免宽表撑不开外框。
 */
export function measureIntrinsicBox(el) {
  let width = Math.max(el.scrollWidth || 0, el.offsetWidth || 0)
  let height = Math.max(el.scrollHeight || 0, el.offsetHeight || 0)
  const children = el.children ? Array.from(el.children) : []
  for (const child of children) {
    width = Math.max(width, childStartWithin(el, child, 'x') + (child.offsetWidth || 0))
    height = Math.max(height, childStartWithin(el, child, 'y') + (child.offsetHeight || 0))
  }
  return { width, height }
}

export function applyExpandedBox(el) {
  el.style.maxWidth = 'none'
  el.style.maxHeight = 'none'
  el.style.overflow = 'visible'
  el.style.overflowX = 'visible'
  el.style.overflowY = 'visible'
  const { width, height } = measureIntrinsicBox(el)
  el.style.width = `${width}px`
  el.style.height = `${height}px`
  el.style.minWidth = `${width}px`
  el.style.minHeight = `${height}px`
}

/** 撑开 root 内所有可滚动区域及其祖先；返回用于收起的快照列表 */
export function expandScreenContent(rootEl) {
  const nodes = listExpandableNodes(rootEl)
  const snapshots = nodes.map((el) => ({ el, style: snapshotInlineBox(el) }))
  for (const { el } of snapshots) applyExpandedBox(el)
  // 子级撑开后，根再量一次，吃掉残余溢出
  applyExpandedBox(rootEl)
  return snapshots
}

export function collapseScreenContent(snapshots) {
  if (!Array.isArray(snapshots)) return
  for (const { el, style } of snapshots) restoreInlineBox(el, style)
}

export function measureContentBox(rootEl) {
  return measureIntrinsicBox(rootEl)
}

/**
 * 工具栏展开/收起目标：
 * 有勾选 → 勾选集合；无勾选 → 全部屏。
 */
export function resolveExpandTargets(selectedIds, allIds) {
  if (selectedIds instanceof Set) {
    if (selectedIds.size > 0) return [...selectedIds]
  } else if (Array.isArray(selectedIds) && selectedIds.length > 0) {
    return [...selectedIds]
  }
  return [...allIds]
}
