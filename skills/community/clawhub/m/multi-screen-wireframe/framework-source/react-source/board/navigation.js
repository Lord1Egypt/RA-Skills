export function clampScale(scale) {
  return Math.min(2, Math.max(0.2, scale))
}

/**
 * 演示模式：按容器内容区把整页缩放到完整可见。
 * container* 为去掉 padding 后的可用尺寸；content* 为未缩放的 stage 宽高。
 */
export function fitDemoScale(containerWidth, containerHeight, contentWidth, contentHeight) {
  if (containerWidth <= 0 || containerHeight <= 0 || contentWidth <= 0 || contentHeight <= 0) {
    return 1
  }
  return clampScale(Math.min(containerWidth / contentWidth, containerHeight / contentHeight))
}

/**
 * 演示视口双击目标是否为屏外空白。
 * 点在 .wf-screen-chrome（标题栏 / 内容）内不算空白，避免误退出。
 */
export function isDemoBlankExitTarget(target) {
  if (!target || typeof target.closest !== 'function') return true
  return !target.closest('.wf-screen-chrome')
}

export function resetCanvasViewport() {
  return { scale: 1, panX: 0, panY: 0 }
}

const FOCUS_PADDING = 40

/**
 * 画板 focus：把整块 screen（含 meta）移到容器中心。
 * 仅当当前 scale 放不下时缩小；不放大。尺寸非法时返回 null。
 */
export function focusCanvasScreen({
  containerWidth,
  containerHeight,
  screenLeft,
  screenTop,
  screenWidth,
  screenHeight,
  currentScale,
  padding = FOCUS_PADDING,
}) {
  if (
    containerWidth <= 0
    || containerHeight <= 0
    || screenWidth <= 0
    || screenHeight <= 0
    || !Number.isFinite(currentScale)
  ) {
    return null
  }

  const availWidth = containerWidth - padding * 2
  const availHeight = containerHeight - padding * 2
  if (availWidth <= 0 || availHeight <= 0) return null

  const fitScale = Math.min(availWidth / screenWidth, availHeight / screenHeight)
  const scale = clampScale(Math.min(currentScale, fitScale))
  return {
    scale,
    panX: containerWidth / 2 - (screenLeft + screenWidth / 2) * scale,
    panY: containerHeight / 2 - (screenTop + screenHeight / 2) * scale,
  }
}

/**
 * 拖拽平移：只用调用方提前截获的 snapshot，禁止在 setState updater 里读 drag ref。
 * React 18 会在 endPan 清空 ref 后重放 updater；读 null.panX 即 Board 报错根因。
 */
export function panFromDragSnapshot(view, snapshot, clientX, clientY) {
  if (!snapshot) return view
  return {
    ...view,
    panX: snapshot.panX + clientX - snapshot.x,
    panY: snapshot.panY + clientY - snapshot.y,
  }
}

export function isScrollableOverflow(value) {
  return value === 'auto' || value === 'scroll' || value === 'overlay'
}

/** 在 root 内向上找可滚动祖先（含 root 自身，如屏内内容区） */
export function findScrollableAncestor(startEl, rootEl) {
  let node = startEl && startEl.nodeType === 3 ? startEl.parentElement : startEl
  while (node) {
    if (node.nodeType === 1) {
      const style = window.getComputedStyle(node)
      const canY = isScrollableOverflow(style.overflowY) && node.scrollHeight > node.clientHeight + 1
      const canX = isScrollableOverflow(style.overflowX) && node.scrollWidth > node.clientWidth + 1
      if (canY || canX) return node
    }
    if (node === rootEl) break
    node = node.parentElement
  }
  return null
}

const CONTENT_DRAG_THRESHOLD = 3

function isEditableTarget(target) {
  if (!target || typeof target.closest !== 'function') return false
  return !!target.closest('input, textarea, select, [contenteditable="true"]')
}

/**
 * 在可滚动区域内按住拖拽 → 滚动内容。
 * 画布锁定（可交互关闭 / 空格）时返回 null，交给画布平移。
 * 返回 null 表示不应接管该次 pointerdown。
 */
export function beginContentDragScroll(event, rootEl, { locked = false, scale = 1 } = {}) {
  if (locked) return null
  if (event.button != null && event.button !== 0) return null
  if (!rootEl || !rootEl.contains(event.target)) return null
  if (isEditableTarget(event.target)) return null
  const scrollable = findScrollableAncestor(event.target, rootEl)
  if (!scrollable) return null
  return {
    el: scrollable,
    pointerId: event.pointerId,
    startX: event.clientX,
    startY: event.clientY,
    scrollLeft: scrollable.scrollLeft,
    scrollTop: scrollable.scrollTop,
    scale: scale > 0 ? scale : 1,
    moved: false,
  }
}

export function moveContentDragScroll(state, event) {
  if (!state || state.pointerId !== event.pointerId) return state
  const dx = (event.clientX - state.startX) / state.scale
  const dy = (event.clientY - state.startY) / state.scale
  if (!state.moved && (Math.abs(dx) > CONTENT_DRAG_THRESHOLD || Math.abs(dy) > CONTENT_DRAG_THRESHOLD)) {
    state.moved = true
  }
  state.el.scrollLeft = state.scrollLeft - dx
  state.el.scrollTop = state.scrollTop - dy
  return state
}

/** 拖拽超过阈值后吞掉随后的 click，避免误触跳转 */
export function endContentDragScroll(state, rootEl) {
  if (!state || !state.moved || !rootEl) return
  const preventClick = (event) => {
    event.preventDefault()
    event.stopPropagation()
    rootEl.removeEventListener('click', preventClick, true)
  }
  rootEl.addEventListener('click', preventClick, true)
}

/** 该方向是否还能继续滚 */
export function canScrollInDirection(el, deltaX, deltaY) {
  const eps = 1
  if (deltaY) {
    const maxY = el.scrollHeight - el.clientHeight
    if (maxY > eps) {
      if (deltaY < 0 && el.scrollTop > eps) return true
      if (deltaY > 0 && el.scrollTop < maxY - eps) return true
    }
  }
  if (deltaX) {
    const maxX = el.scrollWidth - el.clientWidth
    if (maxX > eps) {
      if (deltaX < 0 && el.scrollLeft > eps) return true
      if (deltaX > 0 && el.scrollLeft < maxX - eps) return true
    }
  }
  return false
}

/**
 * 画布锁定时任意滚轮缩放；未锁定时仅 Ctrl/Meta + 滚轮
 *（触控板 pinch 在浏览器里通常带 ctrlKey）。未锁定时普通滚轮留给屏内滚动。
 */
export function shouldZoomOnWheel(event, { locked = false } = {}) {
  if (locked) return true
  return !!(event.ctrlKey || event.metaKey)
}

export function inferEntryId(screens) {
  return screens.find((screen) => screen.entry)?.id || null
}

export function createDemoState(screens) {
  const entryId = inferEntryId(screens)
  if (!entryId) throw new Error('Demo mode requires at least one entry screen')
  return {
    entryId,
    currentScreenId: entryId,
    history: [],
    hotspotsVisible: false,
  }
}

export function navigateDemo(state, targetId, screens) {
  if (!screens.some((screen) => screen.id === targetId)) {
    throw new Error(`Navigation target "${targetId}" does not exist`)
  }
  const currentScreen = screens.find((screen) => screen.id === state.currentScreenId)
  if (!currentScreen.links.includes(targetId)) {
    throw new Error(`Screen "${state.currentScreenId}" links do not include "${targetId}"`)
  }
  if (targetId === state.currentScreenId) return state
  return {
    ...state,
    currentScreenId: targetId,
    history: [...state.history, state.currentScreenId],
  }
}

export function selectDemoEntry(state, entryId, screens) {
  const entry = screens.find((screen) => screen.id === entryId)
  if (!entry) throw new Error(`Navigation target "${entryId}" does not exist`)
  return {
    ...state,
    entryId,
    currentScreenId: entryId,
    history: [],
    hotspotsVisible: false,
  }
}

export function goBackDemo(state) {
  if (state.history.length === 0) return state
  const history = state.history.slice(0, -1)
  return {
    ...state,
    currentScreenId: state.history[state.history.length - 1],
    history,
  }
}

export function resetDemo(state) {
  return {
    ...state,
    currentScreenId: state.entryId,
    history: [],
    hotspotsVisible: false,
  }
}
