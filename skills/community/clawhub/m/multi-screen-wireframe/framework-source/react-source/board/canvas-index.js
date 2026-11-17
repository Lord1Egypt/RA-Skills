export const CANVAS_INDEX_MARGIN = 16

function finite(value, fallback = 0) {
  return Number.isFinite(value) ? value : fallback
}

export function clampCanvasIndexPosition(position, container, item, margin = CANVAS_INDEX_MARGIN) {
  const containerWidth = Math.max(0, finite(container?.width))
  const containerHeight = Math.max(0, finite(container?.height))
  const itemWidth = Math.max(0, finite(item?.width))
  const itemHeight = Math.max(0, finite(item?.height))
  const maxX = Math.max(margin, containerWidth - itemWidth - margin)
  const maxY = Math.max(margin, containerHeight - itemHeight - margin)
  return {
    x: Math.min(Math.max(finite(position?.x, margin), margin), maxX),
    y: Math.min(Math.max(finite(position?.y, margin), margin), maxY),
  }
}

export function defaultCanvasIndexPosition(container, item, margin = CANVAS_INDEX_MARGIN) {
  return clampCanvasIndexPosition({
    x: (finite(container?.width) - finite(item?.width)) / 2,
    y: finite(container?.height) - finite(item?.height) - margin,
  }, container, item, margin)
}

export function waitForCanvasIndexElements(getElements, onReady, scheduler) {
  let active = true
  let frame = null

  const attempt = () => {
    if (!active) return
    const elements = getElements()
    if (!elements?.container || !elements?.item) {
      frame = scheduler.request(attempt)
      return
    }
    frame = null
    onReady(elements)
  }

  frame = scheduler.request(attempt)
  return () => {
    active = false
    if (frame != null) scheduler.cancel(frame)
  }
}
