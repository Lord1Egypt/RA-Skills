import { useT } from './i18n/context.jsx'

function escapeAttribute(value) {
  return String(value).replace(/\\/g, '\\\\').replace(/"/g, '\\"')
}

function intersectRect(rect, clip) {
  const left = Math.max(rect.left, clip.left)
  const right = Math.min(rect.right, clip.right)
  const top = Math.max(rect.top, clip.top)
  const bottom = Math.min(rect.bottom, clip.bottom)
  if (right <= left || bottom <= top) return null
  return { left, right, top, bottom }
}

function annotationPosition(board, annotation, previous) {
  const screen = board.querySelector(`[data-screen-id="${escapeAttribute(annotation.screenId)}"]`)
  const content = screen?.querySelector('.wf-screen-content')
  if (!content) return null

  let element = content
  if (annotation.anchor?.kind === 'node') {
    try {
      element = board.querySelector(annotation.anchor.selector)
    } catch {
      element = null
    }
  }

  const boardRect = board.getBoundingClientRect()
  const contentRect = content.getBoundingClientRect()
  let baseLeft
  let baseTop
  let orphaned = false

  if (element?.isConnected && content.contains(element)) {
    const visible = intersectRect(element.getBoundingClientRect(), contentRect)
    if (!visible) return null
    baseLeft = visible.right - boardRect.left
    baseTop = visible.top - boardRect.top
  } else {
    const fallback = annotation.anchor?.fallbackPosition || { x: 0.96, y: 0.04 }
    baseLeft = contentRect.left - boardRect.left + contentRect.width * fallback.x
    baseTop = contentRect.top - boardRect.top + contentRect.height * fallback.y
    orphaned = annotation.anchor?.kind === 'node'
  }

  const overlap = previous.filter(
    (item) => Math.abs(item.baseLeft - baseLeft) < 3 && Math.abs(item.baseTop - baseTop) < 3,
  ).length
  return {
    key: annotation.id,
    annotation,
    baseLeft: Math.round(baseLeft),
    baseTop: Math.round(baseTop),
    left: Math.round(baseLeft + overlap * 15),
    top: Math.round(baseTop),
    orphaned,
  }
}

function resolvePositions(board, annotations) {
  if (!board) return []
  const positions = []
  for (const annotation of annotations) {
    const position = annotationPosition(board, annotation, positions)
    if (position) positions.push(position)
  }
  return positions
}

function samePositions(left, right) {
  if (left.length !== right.length) return false
  return left.every((item, index) => {
    const other = right[index]
    return item.key === other.key
      && item.annotation === other.annotation
      && item.left === other.left
      && item.top === other.top
      && item.orphaned === other.orphaned
  })
}

export function AnnotationMarkers({ boardRef, annotations, onOpenPanel }) {
  const t = useT()
  const [positions, setPositions] = React.useState([])
  const [activeKey, setActiveKey] = React.useState(null)
  const frameRef = React.useRef(null)

  const refresh = React.useCallback(() => {
    const next = resolvePositions(boardRef.current, annotations)
    setPositions((current) => samePositions(current, next) ? current : next)
  }, [annotations, boardRef])

  const scheduleRefresh = React.useCallback(() => {
    if (frameRef.current) window.cancelAnimationFrame(frameRef.current)
    frameRef.current = window.requestAnimationFrame(() => {
      frameRef.current = null
      refresh()
    })
  }, [refresh])

  React.useLayoutEffect(() => {
    refresh()
  }, [refresh])

  React.useEffect(() => {
    const options = { capture: true, passive: true }
    window.addEventListener('resize', scheduleRefresh)
    window.addEventListener('scroll', scheduleRefresh, options)
    window.addEventListener('pointermove', scheduleRefresh, options)
    window.addEventListener('wheel', scheduleRefresh, options)
    window.addEventListener('click', scheduleRefresh, true)
    return () => {
      window.removeEventListener('resize', scheduleRefresh)
      window.removeEventListener('scroll', scheduleRefresh, options)
      window.removeEventListener('pointermove', scheduleRefresh, options)
      window.removeEventListener('wheel', scheduleRefresh, options)
      window.removeEventListener('click', scheduleRefresh, true)
      if (frameRef.current) window.cancelAnimationFrame(frameRef.current)
    }
  }, [scheduleRefresh])

  React.useEffect(() => {
    if (activeKey && !positions.some((position) => position.key === activeKey)) setActiveKey(null)
  }, [activeKey, positions])

  const active = positions.find((position) => position.key === activeKey)
  const boardWidth = boardRef.current?.clientWidth || 0
  const boardHeight = boardRef.current?.clientHeight || 0
  const bubbleLeft = active ? Math.max(12, Math.min(active.left + 16, boardWidth - 336)) : 0
  const bubbleTop = active ? Math.max(12, Math.min(active.top + 24, boardHeight - 196)) : 0

  return (
    <div className="wf-annotation-markers" aria-label={t('annotation.markersAria')}>
      {positions.map((position, index) => (
        <button
          type="button"
          className={`wf-annotation-marker${activeKey === position.key ? ' is-active' : ''}${position.orphaned ? ' is-orphaned' : ''}`}
          key={position.key}
          aria-label={t('annotation.markerAria', {
            index: index + 1,
            content: position.annotation.content,
          })}
          style={{ left: position.left, top: position.top }}
          onClick={(event) => {
            event.preventDefault()
            event.stopPropagation()
            setActiveKey((current) => current === position.key ? null : position.key)
          }}
        >
          {index + 1}
        </button>
      ))}
      {active ? (
        <aside
          className="wf-annotation-marker-popover"
          style={{ left: bubbleLeft, top: bubbleTop }}
          aria-label={t('annotation.popoverAria', { title: active.annotation.screenTitle })}
        >
          <header className="wf-review-marker-popover-header">
            <strong className="wf-review-marker-popover-title">
              {active.annotation.screenTitle} · {active.annotation.anchor.kind === 'node'
                ? t('annotation.kindNodeShort')
                : t('annotation.kindScreenShort')}
            </strong>
            <button className="wf-annotation-marker-close" type="button" onClick={() => setActiveKey(null)}>{t('annotation.close')}</button>
          </header>
          {active.orphaned ? <p className="wf-annotation-orphaned">{t('annotation.orphaned')}</p> : null}
          <p className="wf-annotation-marker-content">{active.annotation.content}</p>
          <button className="wf-annotation-marker-more" type="button" onClick={() => {
            setActiveKey(null)
            onOpenPanel(active.annotation)
          }}>{t('annotation.viewAll')}</button>
        </aside>
      ) : null}
    </div>
  )
}
