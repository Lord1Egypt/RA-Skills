import { reviewTargets, reviewTypeLabels } from './review.js'
import { useT } from './i18n/context.jsx'

function samePositions(left, right) {
  if (left.length !== right.length) return false
  return left.every((item, index) => {
    const other = right[index]
    return item.key === other.key
      && item.item === other.item
      && item.itemIndex === other.itemIndex
      && item.left === other.left
      && item.top === other.top
  })
}

function intersectRect(rect, clip) {
  const left = Math.max(rect.left, clip.left)
  const right = Math.min(rect.right, clip.right)
  const top = Math.max(rect.top, clip.top)
  const bottom = Math.min(rect.bottom, clip.bottom)
  if (right <= left || bottom <= top) return null
  return { left, right, top, bottom }
}

function resolvePositions(board, items) {
  if (!board) return []
  const boardRect = board.getBoundingClientRect()
  const positions = []

  items.forEach((item, itemIndex) => {
    reviewTargets(item).forEach((target, targetIndex) => {
      let element = null
      try {
        element = board.querySelector(target.selector)
      } catch {
        return
      }
      if (!element?.isConnected) return
      const screenContent = element.closest('.wf-screen-content')
      if (!screenContent) return
      const visible = intersectRect(element.getBoundingClientRect(), screenContent.getBoundingClientRect())
      if (!visible) return
      const baseLeft = Math.round(visible.right - boardRect.left)
      const baseTop = Math.round(visible.top - boardRect.top)
      const overlapCount = positions.filter(
        (position) => Math.abs(position.baseLeft - baseLeft) < 2 && Math.abs(position.baseTop - baseTop) < 2,
      ).length
      positions.push({
        key: `${item.id}:${targetIndex}`,
        item,
        itemIndex,
        targetIndex,
        baseLeft,
        baseTop,
        left: baseLeft + overlapCount * 15,
        top: baseTop,
      })
    })
  })

  return positions
}

export function ReviewMarkers({ boardRef, items, onOpenPanel }) {
  const t = useT()
  const typeLabels = reviewTypeLabels(t)
  const [positions, setPositions] = React.useState([])
  const [activeKey, setActiveKey] = React.useState(null)
  const frameRef = React.useRef(null)

  const refresh = React.useCallback(() => {
    const next = resolvePositions(boardRef.current, items)
    setPositions((current) => samePositions(current, next) ? current : next)
  }, [boardRef, items])

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
  const bubbleTop = active ? Math.max(12, Math.min(active.top + 24, boardHeight - 180)) : 0

  return (
    <div className="wf-review-markers" aria-label={t('review.markersAria')}>
      {positions.map((position) => (
        <button
          type="button"
          className={activeKey === position.key ? 'wf-review-marker is-active' : 'wf-review-marker'}
          key={position.key}
          aria-label={t('review.markerAria', {
            index: position.itemIndex + 1,
            type: typeLabels[position.item.type],
          })}
          style={{ left: position.left, top: position.top }}
          onClick={(event) => {
            event.preventDefault()
            event.stopPropagation()
            setActiveKey((current) => current === position.key ? null : position.key)
          }}
        >
          {position.itemIndex + 1}
        </button>
      ))}
      {active ? (
        <aside
          className="wf-review-marker-popover"
          style={{ left: bubbleLeft, top: bubbleTop }}
          aria-label={t('review.markerPopoverAria', { index: active.itemIndex + 1 })}
        >
          <header className="wf-review-marker-popover-header">
            <strong className="wf-review-marker-popover-title">
              {active.itemIndex + 1}. {typeLabels[active.item.type]}
            </strong>
            <button className="wf-review-marker-popover-close" type="button" onClick={() => setActiveKey(null)}>{t('review.close')}</button>
          </header>
          <p className="wf-review-marker-popover-instruction">
            {active.item.instruction || t('review.removeDefaultInstruction')}
          </p>
          <div className="wf-review-marker-popover-targets">
            {reviewTargets(active.item).map((target) => (
              <code className="wf-review-marker-popover-selector" key={target.selector}>{target.selector}</code>
            ))}
          </div>
          <button
            className="wf-review-marker-popover-more"
            type="button"
            onClick={() => {
              setActiveKey(null)
              onOpenPanel?.()
            }}
          >
            {t('review.viewMore')}
          </button>
        </aside>
      ) : null}
    </div>
  )
}
