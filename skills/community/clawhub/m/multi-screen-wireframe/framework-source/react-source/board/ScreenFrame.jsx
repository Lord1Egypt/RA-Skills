import { usePrototype } from '../core/PrototypeContext.jsx'
import { ErrorBoundary } from '../core/ErrorBoundary.jsx'
import { ScreenIdentityProvider } from '../core/ScreenIdentity.jsx'
import { findFlowTargetId } from '../ui/flow-target.js'
import { findReviewTarget } from './review.js'
import { useT } from './i18n/context.jsx'
import {
  collapseScreenContent,
  expandScreenContent,
  measureContentBox,
} from './expand.js'
import {
  beginContentDragScroll,
  endContentDragScroll,
  moveContentDragScroll,
} from './navigation.js'

export function ScreenFrame({
  screen,
  viewport,
  mode,
  index = 0,
  focused = false,
  onExport,
  expanded = false,
  onToggleExpand,
  canvasLocked = false,
  scale = 1,
  reviewEnabled = false,
  onReviewSelect,
}) {
  const t = useT()
  const { navigate } = usePrototype()
  const contentRef = React.useRef(null)
  const dragRef = React.useRef(null)
  const pointerDownTargetRef = React.useRef(null)
  const expandSnapshotRef = React.useRef(null)
  const hoverReviewElementRef = React.useRef(null)
  const [dragScrolling, setDragScrolling] = React.useState(false)
  const [expandedBox, setExpandedBox] = React.useState(null)

  React.useLayoutEffect(() => {
    const root = contentRef.current
    if (!root || !screen) return undefined

    if (expandSnapshotRef.current) {
      collapseScreenContent(expandSnapshotRef.current)
      expandSnapshotRef.current = null
    }

    if (!expanded) {
      setExpandedBox(null)
      return undefined
    }

    expandSnapshotRef.current = expandScreenContent(root)
    setExpandedBox(measureContentBox(root))

    return () => {
      if (expandSnapshotRef.current) {
        collapseScreenContent(expandSnapshotRef.current)
        expandSnapshotRef.current = null
      }
    }
  }, [expanded, screen?.id, viewport.width, viewport.height])

  React.useEffect(() => {
    if (!reviewEnabled || canvasLocked) {
      hoverReviewElementRef.current?.classList.remove('is-review-hovered')
      hoverReviewElementRef.current = null
    }
    return () => {
      hoverReviewElementRef.current?.classList.remove('is-review-hovered')
      hoverReviewElementRef.current = null
    }
  }, [canvasLocked, reviewEnabled, screen?.id])

  if (!screen) return null

  const Component = screen.component
  const frameClass = [
    'wf-screen-chrome',
    mode === 'canvas' && focused ? 'is-focused' : '',
    expanded ? 'is-expanded' : '',
    `wf-screen-${mode}`,
  ].filter(Boolean).join(' ')

  const onPointerDown = (event) => {
    pointerDownTargetRef.current = event.target
    if (reviewEnabled) return
    // 画布锁定时不接管屏内拖拽滚动，让事件落到画布平移
    if (canvasLocked) {
      event.preventDefault()
      return
    }
    // 已展开无可滚区域，不抢指针
    if (expanded) return
    const state = beginContentDragScroll(event, contentRef.current, { locked: canvasLocked, scale })
    if (!state) return
    dragRef.current = state
    // 等真正拖过阈值再 capture。过早 setPointerCapture 会把 click 重定向到
    // .wf-screen-content，导致 data-flow-to 委托与组件 onClick 全部失效。
  }

  const onPointerMove = (event) => {
    if (reviewEnabled && !canvasLocked) {
      const target = findReviewTarget(event.target, contentRef.current)
      if (target === hoverReviewElementRef.current) return
      hoverReviewElementRef.current?.classList.remove('is-review-hovered')
      target?.classList.add('is-review-hovered')
      hoverReviewElementRef.current = target
      return
    }
    const state = dragRef.current
    if (!state) return
    const wasMoved = state.moved
    moveContentDragScroll(state, event)
    if (!wasMoved && state.moved) {
      setDragScrolling(true)
      try {
        event.currentTarget.setPointerCapture(event.pointerId)
      } catch {
        // ignore: 部分环境在 pointerup 后调用会抛
      }
    }
  }

  const onPointerEnd = (event) => {
    const state = dragRef.current
    if (!state || state.pointerId !== event.pointerId) return
    endContentDragScroll(state, contentRef.current)
    dragRef.current = null
    setDragScrolling(false)
  }

  const onContentClick = (event) => {
    if (reviewEnabled) return
    const root = contentRef.current
    const downTarget = pointerDownTargetRef.current
    pointerDownTargetRef.current = null
    // pointer capture 仍可能把 click.target 改成内容根；回退到 pointerdown 目标
    const startEl = downTarget && root?.contains(downTarget) ? downTarget : event.target
    const to = findFlowTargetId(startEl, root)
    if (!to) return
    event.preventDefault?.()
    event.stopPropagation?.()
    navigate(to)
  }

  const onReviewClick = (event) => {
    if (!reviewEnabled || canvasLocked) return
    const target = findReviewTarget(event.target, contentRef.current)
    if (!target) return
    event.preventDefault()
    event.stopPropagation()
    onReviewSelect?.(target, screen, contentRef.current, {
      additive: event.shiftKey || event.metaKey || event.ctrlKey,
    })
  }

  const clearReviewHover = () => {
    hoverReviewElementRef.current?.classList.remove('is-review-hovered')
    hoverReviewElementRef.current = null
  }

  const contentStyle = expanded && expandedBox
    ? { width: expandedBox.width, height: expandedBox.height, overflow: 'visible' }
    : { width: viewport.width, height: viewport.height }

  const frameWidth = expanded && expandedBox ? expandedBox.width : viewport.width

  return (
    <section
      className={frameClass}
      data-screen-id={screen.id}
      data-expanded={expanded ? 'true' : 'false'}
      style={{ width: frameWidth }}
    >
      <div className="wf-screen-chrome-label">
        <span className="wf-screen-chrome-title">
          <span className="wf-screen-index-num">{index + 1}</span>
          <span className="wf-screen-chrome-screen-title">{screen.title}</span>
        </span>
        <span className="wf-screen-chrome-actions">
          {onToggleExpand ? (
            <button
              type="button"
              className="wf-expand-one"
              onClick={(event) => {
                event.stopPropagation()
                onToggleExpand()
              }}
            >
              {expanded ? t('screen.collapse') : t('screen.expand')}
            </button>
          ) : null}
          {mode === 'canvas' && onExport ? (
            <button
              type="button"
              className="wf-export-one"
              onClick={(event) => {
                event.stopPropagation()
                onExport()
              }}
            >
              {t('screen.exportPng')}
            </button>
          ) : null}
        </span>
      </div>
      <div
        ref={contentRef}
        className={`wf-screen-content${dragScrolling ? ' is-drag-scrolling' : ''}${expanded ? ' is-expanded' : ''}${reviewEnabled && !canvasLocked ? ' is-reviewing' : ''}`}
        style={contentStyle}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerEnd}
        onPointerCancel={onPointerEnd}
        onPointerLeave={clearReviewHover}
        onClickCapture={onReviewClick}
        onClick={onContentClick}
      >
        <ErrorBoundary
          scope="screen"
          resetKey={screen.id}
          screenId={screen.id}
          source={`src/screens/${screen.id}.js`}
        >
          <ScreenIdentityProvider screenId={screen.id}>
            <Component />
          </ScreenIdentityProvider>
        </ErrorBoundary>
      </div>
    </section>
  )
}
