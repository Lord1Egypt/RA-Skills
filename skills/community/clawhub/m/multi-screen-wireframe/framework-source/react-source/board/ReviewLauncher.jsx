import { useT } from './i18n/context.jsx'

const LAUNCHER_SIZE = 48
const LAUNCHER_MARGIN = 20
const DRAG_THRESHOLD = 4

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), Math.max(min, max))
}

function clampPosition(board, position) {
  if (!board) return position
  return {
    x: clamp(position.x, LAUNCHER_MARGIN, board.clientWidth - LAUNCHER_SIZE - LAUNCHER_MARGIN),
    y: clamp(position.y, LAUNCHER_MARGIN, board.clientHeight - LAUNCHER_SIZE - LAUNCHER_MARGIN),
  }
}

function defaultPosition(board) {
  return clampPosition(board, {
    x: board.clientWidth - LAUNCHER_SIZE - LAUNCHER_MARGIN,
    y: board.clientHeight - LAUNCHER_SIZE - LAUNCHER_MARGIN,
  })
}

function readPosition(storageKey) {
  try {
    const value = JSON.parse(window.localStorage.getItem(storageKey))
    if (Number.isFinite(value?.x) && Number.isFinite(value?.y)) return value
  } catch {
    // localStorage may be unavailable for a directly opened local file.
  }
  return null
}

function savePosition(storageKey, position) {
  try {
    window.localStorage.setItem(storageKey, JSON.stringify(position))
  } catch {
    // Keeping the launcher draggable is more important than persistence.
  }
}

function CommentIcon() {
  return (
    <svg className="wf-review-launcher-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M5 4.5h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-6l-4.5 3v-3H5a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2Z" />
      <path d="M7.5 10.5h9" />
    </svg>
  )
}

export function ReviewLauncher({ boardRef, count, projectName, onOpen }) {
  const t = useT()
  const storageKey = `wf-review-launcher-position:${projectName}`
  const [position, setPosition] = React.useState(null)
  const [dragging, setDragging] = React.useState(false)
  const dragRef = React.useRef(null)
  const positionRef = React.useRef(null)
  const suppressClickRef = React.useRef(false)

  const updatePosition = React.useCallback((next) => {
    const clamped = clampPosition(boardRef.current, next)
    positionRef.current = clamped
    setPosition(clamped)
    return clamped
  }, [boardRef])

  React.useLayoutEffect(() => {
    const board = boardRef.current
    if (!board) return undefined
    updatePosition(readPosition(storageKey) || defaultPosition(board))

    const handleResize = () => {
      const next = updatePosition(positionRef.current || defaultPosition(board))
      savePosition(storageKey, next)
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [boardRef, storageKey, updatePosition])

  const finishDrag = (event) => {
    const drag = dragRef.current
    if (!drag || drag.pointerId !== event.pointerId) return
    suppressClickRef.current = drag.moved
    dragRef.current = null
    setDragging(false)
    if (positionRef.current) savePosition(storageKey, positionRef.current)
    if (event.currentTarget.hasPointerCapture?.(event.pointerId)) {
      event.currentTarget.releasePointerCapture(event.pointerId)
    }
  }

  if (count <= 0) return null

  return (
    <button
      type="button"
      className={dragging ? 'wf-review-launcher is-dragging' : 'wf-review-launcher'}
      style={position ? { left: position.x, top: position.y } : { right: LAUNCHER_MARGIN, bottom: LAUNCHER_MARGIN }}
      aria-label={t('review.launcherAria', { count })}
      data-tooltip={t('review.launcherTooltip')}
      onPointerDown={(event) => {
        if (event.button !== 0) return
        const origin = positionRef.current || defaultPosition(boardRef.current)
        dragRef.current = {
          pointerId: event.pointerId,
          startX: event.clientX,
          startY: event.clientY,
          origin,
          moved: false,
        }
        suppressClickRef.current = false
        event.currentTarget.setPointerCapture(event.pointerId)
      }}
      onPointerMove={(event) => {
        const drag = dragRef.current
        if (!drag || drag.pointerId !== event.pointerId) return
        const deltaX = event.clientX - drag.startX
        const deltaY = event.clientY - drag.startY
        if (!drag.moved && Math.hypot(deltaX, deltaY) < DRAG_THRESHOLD) return
        drag.moved = true
        setDragging(true)
        updatePosition({ x: drag.origin.x + deltaX, y: drag.origin.y + deltaY })
      }}
      onPointerUp={finishDrag}
      onPointerCancel={finishDrag}
      onClick={() => {
        if (suppressClickRef.current) {
          suppressClickRef.current = false
          return
        }
        onOpen()
      }}
    >
      <CommentIcon />
      <span className="wf-review-launcher-count" aria-hidden="true">{count}</span>
    </button>
  )
}
