import { usePrototype } from '../core/PrototypeContext.jsx'
import { focusCanvasScreen, resetCanvasViewport, panFromDragSnapshot } from './navigation.js'
import { ScreenFrame } from './ScreenFrame.jsx'
import { useWheelZoom } from './useWheelZoom.js'
import { canUseDemo } from './validation.js'
import { useT } from './i18n/context.jsx'
import {
  clampCanvasIndexPosition,
  defaultCanvasIndexPosition,
  waitForCanvasIndexElements,
} from './canvas-index.js'

const INDEX_DRAG_THRESHOLD = 4

function elementSize(element) {
  return { width: element?.offsetWidth || 0, height: element?.offsetHeight || 0 }
}

function CanvasIndex({
  canvasRef,
  project,
  currentScreenId,
  demoAvailable,
  position,
  onPositionChange,
  onClose,
  navigate,
  enterDemo,
}) {
  const t = useT()
  const indexRef = React.useRef(null)
  const dragRef = React.useRef(null)
  const [dragging, setDragging] = React.useState(false)

  const constrain = React.useCallback((nextPosition, useDefault = false) => {
    const canvas = canvasRef.current
    const index = indexRef.current
    if (!canvas || !index) return nextPosition
    const container = { width: canvas.clientWidth, height: canvas.clientHeight }
    const item = elementSize(index)
    return useDefault
      ? defaultCanvasIndexPosition(container, item)
      : clampCanvasIndexPosition(nextPosition, container, item)
  }, [canvasRef])

  // position == null 表示尚未落点（或项目切换被清掉）；必须再跑一遍布局，
  // 否则会一直卡在 visibility:hidden。
  const needsDefaultPosition = position == null
  React.useLayoutEffect(() => {
    let disconnectResize = () => {}
    const stopWaiting = waitForCanvasIndexElements(
      () => ({ container: canvasRef.current, item: indexRef.current }),
      ({ container: canvas, item: index }) => {
        const update = () => onPositionChange((current) => constrain(current, current == null))
        update()

        if (typeof ResizeObserver === 'function') {
          const observer = new ResizeObserver(update)
          observer.observe(canvas)
          observer.observe(index)
          disconnectResize = () => observer.disconnect()
          return
        }
        window.addEventListener('resize', update)
        disconnectResize = () => window.removeEventListener('resize', update)
      },
      {
        request: (callback) => window.requestAnimationFrame(callback),
        cancel: (frame) => window.cancelAnimationFrame(frame),
      },
    )

    return () => {
      stopWaiting()
      disconnectResize()
    }
  }, [canvasRef, constrain, needsDefaultPosition, onPositionChange])

  const finishDrag = (event) => {
    const drag = dragRef.current
    if (!drag || drag.pointerId !== event.pointerId) return
    dragRef.current = null
    setDragging(false)
    if (event.currentTarget.hasPointerCapture?.(event.pointerId)) {
      event.currentTarget.releasePointerCapture(event.pointerId)
    }
    event.stopPropagation()
  }

  return (
    <div
      ref={indexRef}
      className={dragging ? 'wf-canvas-index is-dragging' : 'wf-canvas-index'}
      style={position ? { left: position.x, top: position.y } : { visibility: 'hidden' }}
    >
      <button
        type="button"
        className="wf-canvas-index-handle"
        aria-label={t('canvas.indexHandleAria')}
        title={t('canvas.indexHandleAria')}
        onPointerDown={(event) => {
          if (event.button !== 0) return
          const origin = position || constrain(null, true)
          dragRef.current = {
            pointerId: event.pointerId,
            startX: event.clientX,
            startY: event.clientY,
            origin,
            moved: false,
          }
          event.currentTarget.setPointerCapture(event.pointerId)
          event.preventDefault()
          event.stopPropagation()
        }}
        onPointerMove={(event) => {
          const drag = dragRef.current
          if (!drag || drag.pointerId !== event.pointerId) return
          const deltaX = event.clientX - drag.startX
          const deltaY = event.clientY - drag.startY
          if (!drag.moved && Math.hypot(deltaX, deltaY) < INDEX_DRAG_THRESHOLD) return
          drag.moved = true
          setDragging(true)
          onPositionChange(constrain({ x: drag.origin.x + deltaX, y: drag.origin.y + deltaY }))
          event.preventDefault()
          event.stopPropagation()
        }}
        onPointerUp={finishDrag}
        onPointerCancel={finishDrag}
      >
        <span className="wf-canvas-index-grip" aria-hidden="true"><i /><i /><i /></span>
        <span>{t('canvas.indexLabel')}</span>
      </button>
      <div className="wf-canvas-index-list">
        {project.screens.map((screen, index) => (
          <button
            type="button"
            key={screen.id}
            className={screen.id === currentScreenId ? 'wf-canvas-index-dot is-active' : 'wf-canvas-index-dot'}
            onClick={(event) => {
              event.stopPropagation()
              navigate(screen.id)
            }}
            onDoubleClick={(event) => {
              event.stopPropagation()
              enterDemo(screen.id)
            }}
            aria-label={`${index + 1}. ${screen.title}`}
            title={demoAvailable ? t('canvas.doubleClickDemo') : undefined}
          >
            <span>{index + 1}</span>
            <span className="wf-canvas-index-tooltip" aria-hidden="true">
              <span className="wf-canvas-index-tooltip-title">{screen.title}</span>
              <span className="wf-canvas-index-tooltip-file">src/screens/{screen.id}.js</span>
            </span>
          </button>
        ))}
      </div>
      <button
        type="button"
        className="wf-canvas-index-close"
        aria-label={t('canvas.indexCloseAria')}
        title={t('canvas.indexCloseAria')}
        onClick={(event) => {
          event.stopPropagation()
          onClose()
        }}
      >
        <svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 4 8 8M12 4l-8 8" /></svg>
      </button>
    </div>
  )
}

export async function runExportWithFeedback(task, setError, t = (key, vars) => key) {
  setError(null)
  try {
    await task()
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    setError(t('canvas.exportFailed', { message }))
  }
}

/** file:// 不是 secure context，clipboard API 常不可用，execCommand 兜底 */
function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(text)
  }
  const area = document.createElement('textarea')
  area.value = text
  area.setAttribute('readonly', '')
  area.style.position = 'fixed'
  area.style.left = '-9999px'
  document.body.appendChild(area)
  area.select()
  try {
    document.execCommand('copy')
  } finally {
    document.body.removeChild(area)
  }
  return Promise.resolve()
}

export function CanvasMode({
  project,
  scale,
  setScale,
  canvasLocked,
  wheelZoomOptions,
  selectedIds,
  setSelectedIds,
  expandedIds = new Set(),
  onToggleExpand,
  onExportIds,
  reviewEnabled = false,
  onReviewSelect,
  onCanvasClick,
  canvasIndexVisible = true,
  canvasIndexPosition,
  onCanvasIndexPositionChange,
  onCloseCanvasIndex,
}) {
  const t = useT()
  const { currentScreenId, navigate, viewport, viewportKey, enterDemo: enterDemoMode } = usePrototype()
  const [view, setView] = React.useState(() => ({ ...resetCanvasViewport(), scale }))
  const [dragging, setDragging] = React.useState(false)
  const [sidebarCollapsed, setSidebarCollapsed] = React.useState(false)
  const [copiedKey, setCopiedKey] = React.useState(null)
  const [copyToast, setCopyToast] = React.useState(null)
  const drag = React.useRef(null)
  const canvasRef = React.useRef(null)
  const stageRef = React.useRef(null)
  const copiedTimer = React.useRef(null)
  const scaleRef = React.useRef(scale)
  const draggingRef = React.useRef(false)
  const demoAvailable = canUseDemo(project.screens)
  scaleRef.current = scale
  draggingRef.current = dragging

  React.useEffect(() => {
    setView((current) => ({ ...resetCanvasViewport(), scale: current.scale }))
  }, [viewportKey])

  React.useEffect(() => {
    setView((current) => ({ ...current, scale }))
  }, [scale])

  React.useEffect(() => {
    if (draggingRef.current) return undefined

    const apply = () => {
      const canvas = canvasRef.current
      const stage = stageRef.current
      if (!canvas || !stage) return false
      const screenEl = stage.querySelector(`[data-canvas-screen-id="${currentScreenId}"]`)
      if (!screenEl) return false
      const currentScale = scaleRef.current
      if (currentScale <= 0) return false
      const stageBox = stage.getBoundingClientRect()
      const screenBox = screenEl.getBoundingClientRect()
      const next = focusCanvasScreen({
        containerWidth: canvas.clientWidth,
        containerHeight: canvas.clientHeight,
        screenLeft: (screenBox.left - stageBox.left) / currentScale,
        screenTop: (screenBox.top - stageBox.top) / currentScale,
        screenWidth: screenBox.width / currentScale,
        screenHeight: screenBox.height / currentScale,
        currentScale,
      })
      if (!next) return false
      setScale(next.scale)
      setView(next)
      return true
    }

    if (apply()) return undefined
    const frame = window.requestAnimationFrame(() => {
      apply()
    })
    return () => window.cancelAnimationFrame(frame)
  }, [currentScreenId, viewportKey, setScale])

  React.useEffect(() => () => {
    if (copiedTimer.current) window.clearTimeout(copiedTimer.current)
  }, [])

  useWheelZoom(canvasRef, scale, setScale, canvasLocked, wheelZoomOptions)

  const startPan = (event) => {
    if (!canvasLocked) return
    if (event.button != null && event.button !== 0) return
    // 画板索引是框架 chrome，锁交互只禁屏内内容，不抢索引点击 / 拖拽
    if (event.target.closest?.('.wf-canvas-index')) return
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

  const enterDemo = (screenId) => {
    // 锁交互时 stage 已 pointer-events:none；索引仍可双击进演示
    if (!demoAvailable) return
    enterDemoMode(screenId)
  }

  const copyMeta = (key, text, event) => {
    event.stopPropagation()
    event.preventDefault()
    copyText(text).then(() => {
      setCopiedKey(key)
      setCopyToast(t('canvas.copied'))
      if (copiedTimer.current) window.clearTimeout(copiedTimer.current)
      copiedTimer.current = window.setTimeout(() => {
        setCopiedKey(null)
        setCopyToast(null)
      }, 1200)
    })
  }

  const toggleSelected = (id) => {
    setSelectedIds((current) => {
      const next = new Set(current)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const toggleAll = () => {
    setSelectedIds((current) => {
      if (current.size === project.screens.length) return new Set()
      return new Set(project.screens.map((screen) => screen.id))
    })
  }

  return (
    <div className="wf-canvas-shell">
      <aside className={`wf-screen-sidebar${sidebarCollapsed ? ' is-collapsed' : ''}`} aria-hidden={sidebarCollapsed}>
        <div className="wf-sidebar-header">
          <label>
            <input
              type="checkbox"
              checked={selectedIds.size === project.screens.length && project.screens.length > 0}
              onChange={toggleAll}
              tabIndex={sidebarCollapsed ? -1 : undefined}
            />
            {t('canvas.selectAll')}
          </label>
          <button
            type="button"
            className="wf-sidebar-toggle"
            aria-label={t('canvas.collapseSidebar')}
            title={t('canvas.collapseSidebar')}
            tabIndex={sidebarCollapsed ? -1 : undefined}
            onClick={() => setSidebarCollapsed(true)}
          >
            <svg className="wf-sidebar-toggle-icon" viewBox="0 0 24 24" aria-hidden="true">
              <rect width="18" height="18" x="3" y="3" rx="2" />
              <path d="M9 3v18" />
              <path d="m16 15-3-3 3-3" />
            </svg>
          </button>
        </div>
        <ul className="wf-screen-list">
          {project.screens.map((screen, index) => (
            <li
              className={screen.id === currentScreenId ? 'is-active' : ''}
              key={screen.id}
              onClick={() => navigate(screen.id)}
              onDoubleClick={() => enterDemo(screen.id)}
              title={demoAvailable ? t('canvas.doubleClickDemo') : undefined}
            >
              <input
                type="checkbox"
                checked={selectedIds.has(screen.id)}
                onChange={(event) => {
                  event.stopPropagation()
                  toggleSelected(screen.id)
                }}
                onClick={(event) => event.stopPropagation()}
                aria-label={t('canvas.selectScreen', { title: screen.title })}
                tabIndex={sidebarCollapsed ? -1 : undefined}
              />
              <span className="wf-screen-index-num">{index + 1}</span>
              <span className="wf-screen-title">{screen.title}</span>
            </li>
          ))}
        </ul>
        <div className="wf-sidebar-tips" aria-label={t('canvas.tipsAria')}>
          <div className="wf-sidebar-tip">
            <span>{t('canvas.tipLocked')}</span>
          </div>
          <div className="wf-sidebar-tip">
            <span>{t('canvas.tipInteractive')}</span>
          </div>
        </div>
      </aside>
      {sidebarCollapsed ? (
        <button
          type="button"
          className="wf-sidebar-expand"
          aria-label={t('canvas.expandSidebar')}
          title={t('canvas.expandSidebar')}
          onClick={() => setSidebarCollapsed(false)}
        >
          <svg className="wf-sidebar-toggle-icon" viewBox="0 0 24 24" aria-hidden="true">
            <rect width="18" height="18" x="3" y="3" rx="2" />
            <path d="M9 3v18" />
            <path d="m14 9 3 3-3 3" />
          </svg>
        </button>
      ) : null}
      <main
        ref={canvasRef}
        className={`wf-canvas${dragging ? ' is-dragging' : ''}${canvasLocked ? ' is-locked' : ''}`}
        onPointerDown={startPan}
        onPointerMove={movePan}
        onPointerUp={endPan}
        onPointerCancel={endPan}
        onClick={onCanvasClick}
      >
        <div
          ref={stageRef}
          className="wf-canvas-stage"
          style={{ transform: `translate(${view.panX}px, ${view.panY}px) scale(${view.scale})` }}
        >
          {project.screens.map((screen, index) => {
            const titleText = `${index + 1}. ${screen.title}`
            const fileText = `src/screens/${screen.id}.js`
            const titleKey = `${screen.id}:title`
            const fileKey = `${screen.id}:file`
            return (
              <div
                className={screen.id === currentScreenId ? 'wf-canvas-screen is-focused' : 'wf-canvas-screen'}
                data-canvas-screen-id={screen.id}
                key={screen.id}
                title={demoAvailable ? t('canvas.doubleClickDemo') : undefined}
                onClick={(event) => {
                  if (event.target.closest('.wf-export-one, .wf-expand-one, .wf-screen-meta-copy')) return
                  navigate(screen.id)
                }}
                onDoubleClick={(event) => {
                  if (event.target.closest('.wf-export-one, .wf-expand-one, .wf-screen-meta-copy')) return
                  event.preventDefault()
                  enterDemo(screen.id)
                }}
              >
                <div className="wf-screen-meta">
                  <div
                    className={`wf-screen-meta-title wf-screen-meta-copy${copiedKey === titleKey ? ' is-copied' : ''}`}
                    title={copiedKey === titleKey ? t('canvas.copied') : t('canvas.clickCopy')}
                    onClick={(event) => copyMeta(titleKey, titleText, event)}
                  >
                    {titleText}
                  </div>
                  {screen.description ? <div>{screen.description}</div> : null}
                  <div
                    className={`wf-meta-line wf-screen-meta-copy${copiedKey === fileKey ? ' is-copied' : ''}`}
                    title={copiedKey === fileKey ? t('canvas.copied') : t('canvas.clickCopy')}
                    onClick={(event) => copyMeta(fileKey, fileText, event)}
                  >
                    <strong>{t('canvas.fileLabel')}</strong>
                    {fileText}
                  </div>
                </div>
                <ScreenFrame
                  screen={screen}
                  viewport={viewport}
                  mode="canvas"
                  index={index}
                  focused={screen.id === currentScreenId}
                  expanded={expandedIds.has(screen.id)}
                  onToggleExpand={() => onToggleExpand(screen.id)}
                  onExport={() => onExportIds([screen.id])}
                  canvasLocked={canvasLocked}
                  scale={view.scale}
                  reviewEnabled={reviewEnabled}
                  onReviewSelect={onReviewSelect}
                />
              </div>
            )
          })}
        </div>
        {canvasIndexVisible ? (
          <CanvasIndex
            canvasRef={canvasRef}
            project={project}
            currentScreenId={currentScreenId}
            demoAvailable={demoAvailable}
            position={canvasIndexPosition}
            onPositionChange={onCanvasIndexPositionChange}
            onClose={onCloseCanvasIndex}
            navigate={navigate}
            enterDemo={enterDemo}
          />
        ) : null}
      </main>
      {copyToast ? (
        <div className="wf-board-toast" role="status">{copyToast}</div>
      ) : null}
    </div>
  )
}
