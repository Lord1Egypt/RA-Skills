import { usePrototype } from '../core/PrototypeContext.jsx'
import { useT } from './i18n/context.jsx'
import {
  fitDemoScale,
  isDemoBlankExitTarget,
  panFromDragSnapshot,
  resetCanvasViewport,
} from './navigation.js'
import { ScreenFrame } from './ScreenFrame.jsx'
import { useWheelZoom } from './useWheelZoom.js'

const BLANK_EXIT_HINT_KEY = 'demo.blankExitHint'

function readContentBox(el) {
  const style = window.getComputedStyle(el)
  const padX = parseFloat(style.paddingLeft) + parseFloat(style.paddingRight)
  const padY = parseFloat(style.paddingTop) + parseFloat(style.paddingBottom)
  return {
    width: Math.max(0, el.clientWidth - padX),
    height: Math.max(0, el.clientHeight - padY),
  }
}

export function DemoMode({
  project,
  hotspotsVisible,
  canvasLocked,
  wheelZoomOptions,
  scale,
  setScale,
  viewResetKey,
  expandedIds = new Set(),
  onToggleExpand,
  reviewEnabled = false,
  onReviewSelect,
  onCanvasClick,
}) {
  const t = useT()
  const { currentScreenId, viewport, viewportKey, setMode } = usePrototype()
  const screenIndex = project.screens.findIndex((item) => item.id === currentScreenId)
  const screen = screenIndex >= 0 ? project.screens[screenIndex] : null
  const currentExpanded = !!(screen && expandedIds.has(screen.id))
  const [view, setView] = React.useState(() => ({ ...resetCanvasViewport(), scale }))
  const [dragging, setDragging] = React.useState(false)
  const drag = React.useRef(null)
  const viewportRef = React.useRef(null)
  const stageRef = React.useRef(null)

  const exitOnBlankDoubleClick = (event) => {
    if (!isDemoBlankExitTarget(event.target)) return
    setMode('canvas')
  }

  // title 挂在视口上会落到屏内子节点，干扰操作；只在空白处悬停时挂上。
  const syncBlankExitHint = (event) => {
    const el = viewportRef.current
    if (!el) return
    const next = isDemoBlankExitTarget(event.target) ? t(BLANK_EXIT_HINT_KEY) : ''
    if ((el.getAttribute('title') || '') === next) return
    if (next) el.setAttribute('title', next)
    else el.removeAttribute('title')
  }

  const clearBlankExitHint = () => {
    viewportRef.current?.removeAttribute('title')
  }

  const applyFit = React.useCallback(() => {
    const container = viewportRef.current
    const stage = stageRef.current
    if (!container || !stage) return
    const box = readContentBox(container)
    const next = fitDemoScale(box.width, box.height, stage.offsetWidth, stage.offsetHeight)
    setScale(next)
    setView({ ...resetCanvasViewport(), scale: next })
  }, [setScale])

  React.useEffect(() => {
    setView((current) => ({ ...current, scale }))
  }, [scale])

  React.useEffect(() => {
    const container = viewportRef.current
    const stage = stageRef.current
    if (!container || typeof ResizeObserver !== 'function') {
      applyFit()
      return undefined
    }
    const observer = new ResizeObserver(() => applyFit())
    observer.observe(container)
    if (stage) observer.observe(stage)
    applyFit()
    return () => observer.disconnect()
  }, [applyFit, viewport, viewportKey, currentScreenId, viewResetKey, currentExpanded])

  useWheelZoom(viewportRef, scale, setScale, canvasLocked, wheelZoomOptions)

  const startPan = (event) => {
    if (!canvasLocked) return
    if (event.button != null && event.button !== 0) return
    drag.current = { x: event.clientX, y: event.clientY, panX: view.panX, panY: view.panY }
    setDragging(true)
    event.currentTarget.setPointerCapture(event.pointerId)
    event.preventDefault()
  }

  const movePan = (event) => {
    const snapshot = drag.current
    if (!snapshot) return
    const { clientX, clientY } = event
    setView((current) => panFromDragSnapshot(current, snapshot, clientX, clientY))
  }

  const endPan = () => {
    drag.current = null
    setDragging(false)
  }

  return (
    <div className={hotspotsVisible ? 'wf-demo is-showing-hotspots' : 'wf-demo'}>
      <div
        ref={viewportRef}
        className={`wf-demo-viewport${dragging ? ' is-dragging' : ''}${canvasLocked ? ' is-locked' : ''}`}
        onPointerDown={startPan}
        onPointerMove={movePan}
        onPointerUp={endPan}
        onPointerCancel={endPan}
        onMouseMove={syncBlankExitHint}
        onMouseLeave={clearBlankExitHint}
        onClick={onCanvasClick}
        onDoubleClick={exitOnBlankDoubleClick}
      >
        <div
          ref={stageRef}
          className="wf-demo-stage"
          style={{ transform: `translate(${view.panX}px, ${view.panY}px) scale(${view.scale})` }}
        >
          <ScreenFrame
            screen={screen}
            viewport={viewport}
            mode="demo"
            index={screenIndex}
            expanded={currentExpanded}
            onToggleExpand={screen && onToggleExpand ? () => onToggleExpand(screen.id) : undefined}
            canvasLocked={canvasLocked}
            scale={view.scale}
            reviewEnabled={reviewEnabled}
            onReviewSelect={onReviewSelect}
          />
        </div>
      </div>
      <p className="wf-demo-hint">{t('demo.hint')}</p>
    </div>
  )
}
