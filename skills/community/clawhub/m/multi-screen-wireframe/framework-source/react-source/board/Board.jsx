import { usePrototype } from '../core/PrototypeContext.jsx'
import { CanvasMode, runExportWithFeedback } from './CanvasMode.jsx'
import { DemoMode } from './DemoMode.jsx'
import { resolveExpandTargets } from './expand.js'
import { exportSelected } from './export.js'
import { canUseDemo } from './validation.js'
import { clampScale } from './navigation.js'
import { ReviewPanel } from './ReviewPanel.jsx'
import { ReviewMarkers } from './ReviewMarkers.jsx'
import { ReviewLauncher } from './ReviewLauncher.jsx'
import { describeReviewElement } from './review.js'
import { preventUnsavedReviewExit } from './before-unload.js'
import { AnnotationPanel } from './AnnotationPanel.jsx'
import { AnnotationMarkers } from './AnnotationMarkers.jsx'
import {
  applyAnnotationOperations,
  baseAnnotations,
  deleteAnnotationOperation,
  getAnnotationStorage,
  preventUnsavedAnnotationExit,
  readAnnotationDraft,
  saveAnnotationDraft,
  upsertAnnotationOperation,
} from './annotations.js'
import { ShortcutHelp } from './BoardPanels.jsx'
import { LocaleProvider, useLocale, useT } from './i18n/context.jsx'
import {
  getBoardStorage,
  normalizeZoomSensitivity,
  readBoardSettings,
  saveBoardSettings,
} from './board-settings.js'
import { isEditableShortcutTarget, shortcutIdForEvent, shortcutModifierLabel } from './shortcuts.js'

function ZoomControls({ scale, setScale, onReset }) {
  const t = useT()
  return (
    <div className="wf-zoom-controls">
      <button type="button" title={t('zoom.out')} onClick={() => setScale((value) => clampScale(value - 0.1))}>-</button>
      <span className="wf-zoom-value">{Math.round(scale * 100)}%</span>
      <button type="button" title={t('zoom.in')} onClick={() => setScale((value) => clampScale(value + 0.1))}>+</button>
      <button type="button" title={t('zoom.resetTitle')} onClick={onReset}>{t('zoom.reset')}</button>
    </div>
  )
}

/** Lucide 风格工具栏图标。仅用于框架 chrome。 */
function ToolbarIcon({ name }) {
  const paths = {
    edit: <><path d="M12 20h9" /><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" /></>,
    comment: <><path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z" /><path d="M8 9h8M8 13h5" /></>,
    fullscreen: <><path d="M8 3H5a2 2 0 0 0-2 2v3" /><path d="M21 8V5a2 2 0 0 0-2-2h-3" /><path d="M3 16v3a2 2 0 0 0 2 2h3" /><path d="M16 21h3a2 2 0 0 0 2-2v-3" /></>,
    expand: <><path d="m7 15 5 5 5-5" /><path d="m7 9 5-5 5 5" /></>,
    collapse: <><path d="m7 20 5-5 5 5" /><path d="m7 4 5 5 5-5" /></>,
    toolbarExpand: <><path d="M5 5v14" /><path d="m15 18-6-6 6-6" /></>,
    toolbarCollapse: <><path d="M19 5v14" /><path d="m9 18 6-6-6-6" /></>,
    download: <><path d="M12 3v12" /><path d="m7 10 5 5 5-5" /><path d="M5 21h14" /></>,
    settings: <><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06-2.83 2.83-.06-.06A1.7 1.7 0 0 0 15 19.4a1.7 1.7 0 0 0-1 .6 1.7 1.7 0 0 0-.4 1.1V21h-4v-.09A1.7 1.7 0 0 0 8.6 19.4a1.7 1.7 0 0 0-1.88.34l-.06.06-2.83-2.83.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-.6-1 1.7 1.7 0 0 0-1.1-.4H3v-4h.09A1.7 1.7 0 0 0 4.6 8.6a1.7 1.7 0 0 0-.34-1.88l-.06-.06 2.83-2.83.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-.6 1.7 1.7 0 0 0 .4-1.1V3h4v.09A1.7 1.7 0 0 0 15.4 4.6a1.7 1.7 0 0 0 1.88-.34l.06-.06 2.83 2.83-.06.06A1.7 1.7 0 0 0 19.4 9c.2.37.52.7 1 .9.32.13.68.2 1.1.2h.09v4h-.09a1.7 1.7 0 0 0-2.1.9Z" /></>,
    help: <><circle cx="12" cy="12" r="9" /><path d="M9.7 9a2.4 2.4 0 1 1 3.7 2c-.9.6-1.4 1.1-1.4 2" /><path d="M12 17h.01" /></>,
  }

  return (
    <svg className="wf-toolbar-icon" viewBox="0 0 24 24" aria-hidden="true">
      {paths[name]}
    </svg>
  )
}

/** 线框锁：开锁=可交互，闭锁=不可交互。框架 chrome 可用 SVG。 */
function LockIcon({ open }) {
  return (
    <svg className="wf-lock-icon" viewBox="0 0 14 14" width="14" height="14" aria-hidden="true">
      {open ? (
        // 开锁：梁从左侧立起后向右上悬空，右脚不扣回锁体
        <path
          d="M4.25 6.75V4.35a2.75 2.75 0 0 1 5.35-.2"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
        />
      ) : (
        <path
          d="M4.25 6.75V4.5a2.75 2.75 0 0 1 5.5 0v2.25"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
        />
      )}
      <rect x="2.75" y="6.75" width="8.5" height="5.5" rx="1.25" fill="currentColor" />
    </svg>
  )
}

/** interactive=true 显示开锁「可交互」；false 为上锁，可直接拖拽平移、滚轮缩放 */
function InteractionLock({ interactive, onToggle }) {
  const t = useT()
  const shortcutModifier = shortcutModifierLabel()
  return (
    <button
      type="button"
      className={interactive ? 'wf-interaction-lock' : 'wf-interaction-lock is-locked'}
      onClick={onToggle}
      aria-pressed={!interactive}
      title={interactive
        ? t('interaction.titleInteractive', { modifier: shortcutModifier })
        : t('interaction.titleLocked', { modifier: shortcutModifier })}
    >
      <LockIcon open={interactive} />
      <span>{interactive ? t('interaction.interactive') : t('interaction.locked')}</span>
    </button>
  )
}

function getFullscreenElement() {
  return document.fullscreenElement || document.webkitFullscreenElement || null
}

function requestBoardFullscreen(el) {
  const request = el && (el.requestFullscreen || el.webkitRequestFullscreen)
  if (!request) return Promise.resolve()
  return Promise.resolve(request.call(el)).catch(() => {})
}

function exitBoardFullscreen() {
  if (!getFullscreenElement()) return Promise.resolve()
  const exit = document.exitFullscreen || document.webkitExitFullscreen
  if (!exit) return Promise.resolve()
  return Promise.resolve(exit.call(document)).catch(() => {})
}

export function Board({ project }) {
  return (
    <LocaleProvider>
      <BoardContent project={project} />
    </LocaleProvider>
  )
}

function BoardContent({ project }) {
  const t = useT()
  const { locale, setLocale } = useLocale()
  const {
    mode,
    setMode,
    setViewportKey,
    viewportKey,
    viewport,
    entryId,
    selectEntry,
    currentScreenId,
    canGoBack,
    goBack,
  } = usePrototype()
  const demoAvailable = canUseDemo(project.screens)
  const viewportOptions = Object.keys(project.viewports)
  const shortcutModifier = shortcutModifierLabel()

  const [selectedIds, setSelectedIds] = React.useState(
    () => new Set(project.screens.map((screen) => screen.id)),
  )
  const [canvasScale, setCanvasScale] = React.useState(1)
  const [demoScale, setDemoScale] = React.useState(1)
  const [demoViewResetKey, setDemoViewResetKey] = React.useState(0)
  const [interactive, setInteractive] = React.useState(true)
  const [spaceHeld, setSpaceHeld] = React.useState(false)
  const [hotspotsVisible, setHotspotsVisible] = React.useState(false)
  const [exportError, setExportError] = React.useState(null)
  const [exporting, setExporting] = React.useState(false)
  const [expandedIds, setExpandedIds] = React.useState(() => new Set())
  const [immersive, setImmersive] = React.useState(false)
  const [immersiveToolbarExpanded, setImmersiveToolbarExpanded] = React.useState(true)
  const [browserFullscreen, setBrowserFullscreen] = React.useState(false)
  const [reviewEnabled, setReviewEnabled] = React.useState(false)
  const [reviewTool, setReviewTool] = React.useState('modify')
  const [reviewPanelVisible, setReviewPanelVisible] = React.useState(false)
  const [reviewSelections, setReviewSelections] = React.useState([])
  const [reviewMultiSelect, setReviewMultiSelect] = React.useState(false)
  const [reviewItems, setReviewItems] = React.useState([])
  const annotationBase = React.useMemo(() => baseAnnotations(project), [project])
  const [annotationOperations, setAnnotationOperations] = React.useState(
    () => readAnnotationDraft(getAnnotationStorage(), project).operations,
  )
  const [annotationStorageSaved, setAnnotationStorageSaved] = React.useState(true)
  const [helpVisible, setHelpVisible] = React.useState(false)
  const [canvasIndexVisible, setCanvasIndexVisible] = React.useState(
    () => readBoardSettings(getBoardStorage(), project.name).showCanvasIndex,
  )
  const [showAnnotationMarkers, setShowAnnotationMarkers] = React.useState(
    () => readBoardSettings(getBoardStorage(), project.name).showAnnotationMarkers,
  )
  const [trackpadZoom, setTrackpadZoom] = React.useState(
    () => readBoardSettings(getBoardStorage(), project.name).trackpadZoom,
  )
  const [zoomSensitivity, setZoomSensitivity] = React.useState(
    () => readBoardSettings(getBoardStorage(), project.name).zoomSensitivity,
  )
  const [demoUnlockInteraction, setDemoUnlockInteraction] = React.useState(
    () => readBoardSettings(getBoardStorage(), project.name).demoUnlockInteraction,
  )
  const [canvasIndexPosition, setCanvasIndexPosition] = React.useState(null)
  const boardRef = React.useRef(null)
  const selectedReviewElementsRef = React.useRef(new Set())
  const breadcrumbHoverElementRef = React.useRef(null)

  const canvasLocked = !interactive || spaceHeld
  const allScreenIds = project.screens.map((screen) => screen.id)
  const isDemo = mode === 'demo' && demoAvailable
  const activeScale = isDemo ? demoScale : canvasScale
  const setActiveScale = isDemo ? setDemoScale : setCanvasScale
  const wheelZoomOptions = { trackpadMode: trackpadZoom, sensitivity: zoomSensitivity }
  const annotations = React.useMemo(
    () => applyAnnotationOperations(annotationBase, annotationOperations),
    [annotationBase, annotationOperations],
  )

  const clearReviewSelection = React.useCallback(() => {
    for (const element of selectedReviewElementsRef.current) {
      element.classList.remove('is-review-selected')
    }
    selectedReviewElementsRef.current.clear()
    setReviewSelections([])
  }, [])

  const selectReviewElement = React.useCallback((element, screen, contentRoot, options = {}) => {
    const primary = reviewSelections[reviewSelections.length - 1]
    const activeScreen = screen || project.screens.find((item) => item.id === primary?.screenId)
    const activeRoot = contentRoot || primary?.contentRoot
    if (!element || !activeScreen || !activeRoot) return
    const nextSelection = describeReviewElement(element, activeRoot, activeScreen)
    const additive = reviewTool === 'modify' && (reviewMultiSelect || options.additive)
    setReviewPanelVisible(true)

    setReviewSelections((current) => {
      if (options.replaceElement) {
        options.replaceElement.classList.remove('is-review-selected')
        selectedReviewElementsRef.current.delete(options.replaceElement)
        if (current.some((item) => item.element === element && item.element !== options.replaceElement)) {
          return current.filter((item) => item.element !== options.replaceElement)
        }
        element.classList.add('is-review-selected')
        selectedReviewElementsRef.current.add(element)
        return current.map((item) => item.element === options.replaceElement ? nextSelection : item)
      }
      const alreadySelected = current.some((item) => item.element === element)
      if (!additive) {
        for (const selectedElement of selectedReviewElementsRef.current) {
          selectedElement.classList.remove('is-review-selected')
        }
        selectedReviewElementsRef.current.clear()
      } else if (alreadySelected) {
        element.classList.remove('is-review-selected')
        selectedReviewElementsRef.current.delete(element)
        return current.filter((item) => item.element !== element)
      }

      element.classList.add('is-review-selected')
      selectedReviewElementsRef.current.add(element)
      return additive ? [...current, nextSelection] : [nextSelection]
    })
  }, [project.screens, reviewMultiSelect, reviewSelections, reviewTool])

  const removeReviewSelection = React.useCallback((element) => {
    element?.classList.remove('is-review-selected')
    selectedReviewElementsRef.current.delete(element)
    setReviewSelections((current) => current.filter((item) => item.element !== element))
  }, [])

  const closeReview = React.useCallback(() => {
    setReviewEnabled(false)
    setReviewPanelVisible(false)
    breadcrumbHoverElementRef.current?.classList.remove('is-review-hovered')
    breadcrumbHoverElementRef.current = null
    clearReviewSelection()
  }, [clearReviewSelection])

  const hoverReviewBreadcrumb = React.useCallback((element) => {
    breadcrumbHoverElementRef.current?.classList.remove('is-review-hovered')
    breadcrumbHoverElementRef.current = element || null
    breadcrumbHoverElementRef.current?.classList.add('is-review-hovered')
  }, [])

  const toggleReview = React.useCallback((tool = 'modify') => {
    if (reviewEnabled && reviewTool === tool) {
      closeReview()
      return
    }
    setInteractive(true)
    setReviewMultiSelect(false)
    setReviewTool(tool)
    setReviewPanelVisible(tool === 'annotation')
    setReviewEnabled(true)
  }, [closeReview, reviewEnabled, reviewTool])

  const openReviewPanel = () => {
    setInteractive(true)
    setReviewTool('modify')
    setReviewEnabled(true)
    setReviewPanelVisible(true)
  }

  const openAnnotationPanel = (annotation) => {
    setInteractive(true)
    setReviewTool('annotation')
    setReviewEnabled(true)
    setReviewPanelVisible(true)
    if (annotation?.screenId) selectEntry(annotation.screenId)
  }

  const closeReviewPanel = React.useCallback(() => {
    setReviewPanelVisible(false)
    hoverReviewBreadcrumb(null)
  }, [hoverReviewBreadcrumb])

  const addReviewItem = (item) => {
    setReviewItems((current) => [
      ...current,
      { ...item, id: `review-${Date.now()}-${current.length + 1}` },
    ])
  }

  const removeReviewItem = (id) => {
    setReviewItems((current) => current.filter((item) => item.id !== id))
  }

  const upsertAnnotation = React.useCallback((annotation) => {
    setAnnotationOperations((current) => (
      upsertAnnotationOperation(annotationBase, current, annotation)
    ))
  }, [annotationBase])

  const deleteAnnotation = React.useCallback((id) => {
    setAnnotationOperations((current) => (
      deleteAnnotationOperation(annotationBase, current, id)
    ))
  }, [annotationBase])

  const importAnnotations = React.useCallback((incoming, importedOperations = []) => {
    setAnnotationOperations((current) => {
      let next = incoming.reduce(
        (operations, annotation) => upsertAnnotationOperation(annotationBase, operations, annotation),
        current,
      )
      for (const operation of importedOperations) {
        if (operation.op === 'delete') {
          next = deleteAnnotationOperation(annotationBase, next, operation.id)
        } else if (operation.op === 'upsert') {
          next = upsertAnnotationOperation(annotationBase, next, operation.annotation)
        }
      }
      return next
    })
  }, [annotationBase])

  const clearAnnotationDraft = React.useCallback(() => setAnnotationOperations([]), [])

  React.useEffect(() => () => {
    for (const element of selectedReviewElementsRef.current) {
      element.classList.remove('is-review-selected')
    }
    breadcrumbHoverElementRef.current?.classList.remove('is-review-hovered')
  }, [])

  React.useEffect(() => {
    if (!reviewEnabled) return
    clearReviewSelection()
    hoverReviewBreadcrumb(null)
    setReviewPanelVisible(false)
  }, [clearReviewSelection, hoverReviewBreadcrumb, mode, viewportKey])

  React.useEffect(() => {
    if (reviewItems.length === 0) return undefined
    const handler = (event) => preventUnsavedReviewExit(event, t('unsaved.review'))
    window.addEventListener('beforeunload', handler)
    return () => window.removeEventListener('beforeunload', handler)
  }, [reviewItems.length, t])

  React.useEffect(() => {
    const draft = readAnnotationDraft(getAnnotationStorage(), project)
    setAnnotationOperations(draft.operations)
  }, [project])

  React.useEffect(() => {
    setAnnotationStorageSaved(saveAnnotationDraft(
      getAnnotationStorage(),
      project,
      annotationOperations,
    ))
  }, [annotationOperations, project])

  React.useEffect(() => {
    if (!annotationOperations.length || annotationStorageSaved) return undefined
    const handler = (event) => preventUnsavedAnnotationExit(event, t('unsaved.annotation'))
    window.addEventListener('beforeunload', handler)
    return () => window.removeEventListener('beforeunload', handler)
  }, [annotationOperations.length, annotationStorageSaved, t])

  const exitImmersive = React.useCallback(() => {
    setImmersive(false)
    setImmersiveToolbarExpanded(true)
    exitBoardFullscreen()
  }, [])

  const enterImmersive = React.useCallback(() => {
    closeReview()
    setHelpVisible(false)
    setImmersiveToolbarExpanded(true)
    setImmersive(true)
  }, [closeReview])

  const toggleImmersive = React.useCallback(() => {
    if (immersive) exitImmersive()
    else enterImmersive()
  }, [enterImmersive, exitImmersive, immersive])

  const toggleBrowserFullscreen = React.useCallback(() => {
    if (getFullscreenElement()) {
      exitBoardFullscreen()
      return
    }
    closeReview()
    setHelpVisible(false)
    setImmersiveToolbarExpanded(true)
    setImmersive(true)
    requestBoardFullscreen(boardRef.current)
  }, [closeReview])

  const updateCanvasIndexVisible = React.useCallback((visible) => {
    setCanvasIndexVisible(visible)
    saveBoardSettings(getBoardStorage(), project.name, {
      showCanvasIndex: visible,
      showAnnotationMarkers,
      trackpadZoom,
      zoomSensitivity,
      demoUnlockInteraction,
    })
  }, [demoUnlockInteraction, project.name, showAnnotationMarkers, trackpadZoom, zoomSensitivity])

  const updateShowAnnotationMarkers = React.useCallback((visible) => {
    setShowAnnotationMarkers(visible)
    saveBoardSettings(getBoardStorage(), project.name, {
      showCanvasIndex: canvasIndexVisible,
      showAnnotationMarkers: visible,
      trackpadZoom,
      zoomSensitivity,
      demoUnlockInteraction,
    })
  }, [canvasIndexVisible, demoUnlockInteraction, project.name, trackpadZoom, zoomSensitivity])

  const updateTrackpadZoom = React.useCallback((enabled) => {
    setTrackpadZoom(enabled)
    saveBoardSettings(getBoardStorage(), project.name, {
      showCanvasIndex: canvasIndexVisible,
      showAnnotationMarkers,
      trackpadZoom: enabled,
      zoomSensitivity,
      demoUnlockInteraction,
    })
  }, [canvasIndexVisible, demoUnlockInteraction, project.name, showAnnotationMarkers, zoomSensitivity])

  const updateZoomSensitivity = React.useCallback((value) => {
    const normalized = normalizeZoomSensitivity(value)
    setZoomSensitivity(normalized)
    saveBoardSettings(getBoardStorage(), project.name, {
      showCanvasIndex: canvasIndexVisible,
      showAnnotationMarkers,
      trackpadZoom,
      zoomSensitivity: normalized,
      demoUnlockInteraction,
    })
  }, [canvasIndexVisible, demoUnlockInteraction, project.name, showAnnotationMarkers, trackpadZoom])

  const updateDemoUnlockInteraction = React.useCallback((enabled) => {
    setDemoUnlockInteraction(enabled)
    saveBoardSettings(getBoardStorage(), project.name, {
      showCanvasIndex: canvasIndexVisible,
      showAnnotationMarkers,
      trackpadZoom,
      zoomSensitivity,
      demoUnlockInteraction: enabled,
    })
  }, [canvasIndexVisible, project.name, showAnnotationMarkers, trackpadZoom, zoomSensitivity])

  // 只在切换项目时清位置。首屏 useEffect 若也 set null，会盖掉 CanvasIndex
  // useLayoutEffect 刚算好的坐标，索引会一直 visibility:hidden。
  const canvasIndexSettingsProjectRef = React.useRef(null)
  const wasDemoRef = React.useRef(false)
  React.useEffect(() => {
    const settings = readBoardSettings(getBoardStorage(), project.name)
    setCanvasIndexVisible(settings.showCanvasIndex)
    setShowAnnotationMarkers(settings.showAnnotationMarkers)
    setTrackpadZoom(settings.trackpadZoom)
    setZoomSensitivity(settings.zoomSensitivity)
    setDemoUnlockInteraction(settings.demoUnlockInteraction)
    const previousName = canvasIndexSettingsProjectRef.current
    canvasIndexSettingsProjectRef.current = project.name
    if (previousName != null && previousName !== project.name) {
      setCanvasIndexPosition(null)
    }
  }, [project.name])

  React.useEffect(() => {
    const enteredDemo = isDemo && !wasDemoRef.current
    wasDemoRef.current = isDemo
    if (!enteredDemo || !demoUnlockInteraction) return
    setInteractive((value) => (value ? value : true))
  }, [demoUnlockInteraction, isDemo])

  React.useEffect(() => {
    setExpandedIds(new Set())
  }, [viewportKey])

  const toggleExpand = (id) => {
    setExpandedIds((current) => {
      const next = new Set(current)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const expandTargets = (shouldExpand) => {
    const targets = resolveExpandTargets(selectedIds, allScreenIds)
    setExpandedIds((current) => {
      const next = new Set(current)
      for (const id of targets) {
        if (shouldExpand) next.add(id)
        else next.delete(id)
      }
      return next
    })
  }

  React.useEffect(() => {
    const down = (event) => {
      if (event.code === 'Space' && !event.repeat && !isEditableShortcutTarget(event.target)) {
        event.preventDefault()
        setSpaceHeld(true)
        return
      }

      const shortcut = shortcutIdForEvent(event)
      if (!shortcut) return
      if (shortcut !== 'escape' && isEditableShortcutTarget(event.target)) return

      if (shortcut === 'demo' && !demoAvailable) return
      if (shortcut === 'hotspots' && !isDemo) return
      if (shortcut === 'escape' && getFullscreenElement()) return
      event.preventDefault()

      if (shortcut === 'canvas') setMode('canvas')
      if (shortcut === 'demo') setMode('demo')
      if (shortcut === 'interaction') setInteractive((value) => !value)
      if (shortcut === 'review') toggleReview()
      if (shortcut === 'immersive') toggleImmersive()
      if (shortcut === 'browser-fullscreen') toggleBrowserFullscreen()
      if (shortcut === 'hotspots') setHotspotsVisible((value) => !value)
      if (shortcut === 'help') {
        setHelpVisible((value) => !value)
      }
      if (shortcut === 'escape') {
        if (helpVisible) setHelpVisible(false)
        else if (reviewEnabled) closeReview()
        else if (immersive) exitImmersive()
      }
    }
    const up = (event) => {
      if (event.code === 'Space') setSpaceHeld(false)
    }
    window.addEventListener('keydown', down)
    window.addEventListener('keyup', up)
    return () => {
      window.removeEventListener('keydown', down)
      window.removeEventListener('keyup', up)
    }
  }, [
    closeReview,
    demoAvailable,
    exitImmersive,
    helpVisible,
    immersive,
    isDemo,
    reviewEnabled,
    setMode,
    toggleBrowserFullscreen,
    toggleImmersive,
    toggleReview,
  ])

  React.useEffect(() => {
    if (mode !== 'demo') setHotspotsVisible(false)
  }, [mode])

  React.useEffect(() => {
    const sync = () => setBrowserFullscreen(!!getFullscreenElement())
    document.addEventListener('fullscreenchange', sync)
    document.addEventListener('webkitfullscreenchange', sync)
    return () => {
      document.removeEventListener('fullscreenchange', sync)
      document.removeEventListener('webkitfullscreenchange', sync)
    }
  }, [])

  const exportIds = (ids) => runExportWithFeedback(async () => {
    setExporting(true)
    try {
      const screens = ids.map((id) => {
        const screen = project.screens.find((item) => item.id === id)
        return {
          id,
          title: screen.title,
          element: document.querySelector(`[data-screen-id="${id}"] .wf-screen-content`),
          viewport,
          expanded: expandedIds.has(id),
          projectName: project.name,
        }
      })
      await exportSelected(screens, t)
    } finally {
      setExporting(false)
    }
  }, setExportError, t)

  const resetDemoView = () => {
    setDemoViewResetKey((value) => value + 1)
  }

  const resetActiveView = isDemo ? resetDemoView : () => setCanvasScale(1)

  return (
    <div
      ref={boardRef}
      className={`wf-board${immersive ? ' is-immersive' : ''}${reviewEnabled ? ' is-reviewing' : ''}`}
    >
      <header className="wf-board-toolbar">
        <div className="wf-toolbar-left">
          <h1 className="wf-project-name">{project.name}</h1>
          <span className="wf-project-meta">{t('toolbar.pageCount', { count: project.screens.length })}</span>
        </div>

        <div className="wf-toolbar-center">
          {demoAvailable ? (
            <div className="wf-mode-switcher" role="group" aria-label={t('toolbar.modeAria')}>
              <button
                type="button"
                className={mode === 'canvas' ? 'is-active' : ''}
                onClick={() => setMode('canvas')}
                title={t('toolbar.canvasTitle', { modifier: shortcutModifier })}
              >
                {t('toolbar.canvas')}
              </button>
              <button
                type="button"
                className={mode === 'demo' ? 'is-active' : ''}
                onClick={() => setMode('demo')}
                title={t('toolbar.demoTitle', { modifier: shortcutModifier })}
              >
                {t('toolbar.demo')}
              </button>
            </div>
          ) : null}

          {viewportOptions.length > 1 ? (
            <div className="wf-viewport-switcher" role="group" aria-label={t('toolbar.viewportAria')}>
              {viewportOptions.map((key) => (
                <button
                  type="button"
                  key={key}
                  className={viewportKey === key ? 'is-active' : ''}
                  onClick={() => setViewportKey(key)}
                >
                  {key === 'mobile' || key === 'desktop' ? t(`viewport.${key}`) : key}
                </button>
              ))}
            </div>
          ) : null}

          {mode === 'canvas' || !demoAvailable ? (
            <>
              <ZoomControls
                scale={canvasScale}
                setScale={setCanvasScale}
                onReset={() => setCanvasScale(1)}
              />
              <InteractionLock
                interactive={interactive}
                onToggle={() => setInteractive((value) => !value)}
              />
            </>
          ) : (
            <>
              <ZoomControls
                scale={demoScale}
                setScale={setDemoScale}
                onReset={resetDemoView}
              />
              <InteractionLock
                interactive={interactive}
                onToggle={() => setInteractive((value) => !value)}
              />
              <button
                type="button"
                className={hotspotsVisible ? 'wf-board-button is-active' : 'wf-board-button'}
                onClick={() => setHotspotsVisible((value) => !value)}
                title={t('toolbar.hotspotsTitle', { modifier: shortcutModifier })}
              >
                {hotspotsVisible ? t('toolbar.hotspotsOn') : t('toolbar.hotspotsOff')}
              </button>
              <div className="wf-demo-entry">
                <label htmlFor="wf-demo-entry">{t('toolbar.entry')}</label>
                <select
                  id="wf-demo-entry"
                  value={entryId}
                  onChange={(event) => selectEntry(event.target.value)}
                  title={t('toolbar.entryTitle')}
                >
                  {project.screens.map((screen, index) => (
                    <option key={screen.id} value={screen.id}>
                      {index + 1}. {screen.title}
                    </option>
                  ))}
                </select>
              </div>
              {canGoBack ? (
                <button type="button" className="wf-board-button" onClick={goBack}>{t('toolbar.back')}</button>
              ) : null}
            </>
          )}
        </div>

        <div className="wf-toolbar-right">
          <button
            type="button"
            className={helpVisible ? 'wf-toolbar-icon-button is-active' : 'wf-toolbar-icon-button'}
            aria-label={t('toolbar.helpAria')}
            aria-expanded={helpVisible}
            aria-controls="wf-board-utility"
            title={t('toolbar.helpTitle')}
            onClick={() => setHelpVisible((value) => !value)}
          >
            <ToolbarIcon name="help" />
            <span className="wf-visually-hidden">{t('toolbar.help')}</span>
          </button>
          <button
            type="button"
            className={reviewEnabled && reviewTool === 'modify' ? 'wf-toolbar-icon-button is-active' : 'wf-toolbar-icon-button'}
            aria-pressed={reviewEnabled && reviewTool === 'modify'}
            aria-label={reviewEnabled && reviewTool === 'modify' ? t('toolbar.reviewActive') : t('toolbar.review')}
            title={t('toolbar.reviewTitle', { modifier: shortcutModifier })}
            onClick={() => toggleReview('modify')}
          >
            <ToolbarIcon name="edit" />
            <span className="wf-visually-hidden">{t('toolbar.review')}</span>
          </button>
          <button
            type="button"
            className={reviewEnabled && reviewTool === 'annotation' ? 'wf-toolbar-icon-button is-active' : 'wf-toolbar-icon-button'}
            aria-pressed={reviewEnabled && reviewTool === 'annotation'}
            aria-label={reviewEnabled && reviewTool === 'annotation' ? t('toolbar.annotationActive') : t('toolbar.annotation')}
            title={t('toolbar.annotationTitle')}
            onClick={() => toggleReview('annotation')}
          >
            <ToolbarIcon name="comment" />
            {annotations.length > 0 ? (
              <span className="wf-toolbar-icon-count">
                {annotations.length}
              </span>
            ) : null}
            <span className="wf-visually-hidden">{t('toolbar.annotation')}</span>
          </button>
          <button
            type="button"
            className="wf-toolbar-icon-button"
            aria-label={immersive ? t('toolbar.immersiveExit') : t('toolbar.immersiveEnter')}
            title={t('toolbar.immersiveTitle', { modifier: shortcutModifier })}
            onClick={toggleImmersive}
          >
            <ToolbarIcon name="fullscreen" />
            <span className="wf-visually-hidden">{t('toolbar.fullscreen')}</span>
          </button>
          <button
            type="button"
            className="wf-toolbar-icon-button"
            aria-label={selectedIds.size > 0 ? t('toolbar.expandSelected') : t('toolbar.expandAll')}
            title={selectedIds.size > 0 ? t('toolbar.expandSelectedTitle') : t('toolbar.expandAllTitle')}
            onClick={() => expandTargets(true)}
          >
            <ToolbarIcon name="expand" />
            <span className="wf-visually-hidden">{t('toolbar.expandAll')}</span>
          </button>
          <button
            type="button"
            className="wf-toolbar-icon-button"
            aria-label={selectedIds.size > 0 ? t('toolbar.collapseSelected') : t('toolbar.collapseAll')}
            title={selectedIds.size > 0 ? t('toolbar.collapseSelectedTitle') : t('toolbar.collapseAllTitle')}
            onClick={() => expandTargets(false)}
          >
            <ToolbarIcon name="collapse" />
            <span className="wf-visually-hidden">{t('toolbar.collapseAll')}</span>
          </button>
          <button
            type="button"
            className="wf-toolbar-icon-button wf-toolbar-icon-button--primary"
            disabled={exporting || selectedIds.size === 0 || mode === 'demo'}
            aria-label={exporting ? t('toolbar.exporting') : t('toolbar.export', { count: selectedIds.size })}
            title={exporting ? t('toolbar.exportingTitle') : t('toolbar.exportTitle', { count: selectedIds.size })}
            onClick={() => exportIds([...selectedIds])}
          >
            <ToolbarIcon name="download" />
            <span className="wf-toolbar-icon-count">{exporting ? '…' : selectedIds.size}</span>
            <span className="wf-visually-hidden">{t('toolbar.download')}</span>
          </button>
        </div>
      </header>

      {exportError ? (
        <div className="wf-toolbar-error" role="alert">{exportError}</div>
      ) : null}

      {immersive ? (
        <div
          className={`wf-immersive-chrome${immersiveToolbarExpanded ? '' : ' is-collapsed'}`}
          role="toolbar"
          aria-label={t('immersive.controlsAria')}
        >
          {immersiveToolbarExpanded ? (
            <div className="wf-immersive-controls">
              <button
                type="button"
                className="wf-board-button"
                title={t('immersive.exitTitle')}
                onClick={exitImmersive}
              >
                {t('immersive.exit')}
              </button>
              <button
                type="button"
                className={browserFullscreen ? 'wf-board-button is-active' : 'wf-board-button'}
                title={browserFullscreen
                  ? t('immersive.browserFullscreenExitTitle', { modifier: shortcutModifier })
                  : t('immersive.browserFullscreenEnterTitle', { modifier: shortcutModifier })}
                onClick={toggleBrowserFullscreen}
              >
                {browserFullscreen ? t('immersive.browserFullscreenOn') : t('immersive.browserFullscreen')}
              </button>
              <ZoomControls
                scale={activeScale}
                setScale={setActiveScale}
                onReset={resetActiveView}
              />
              <InteractionLock
                interactive={interactive}
                onToggle={() => setInteractive((value) => !value)}
              />
              <button
                type="button"
                className={helpVisible ? 'wf-toolbar-icon-button wf-immersive-action-button is-active' : 'wf-toolbar-icon-button wf-immersive-action-button'}
                aria-label={t('toolbar.helpAria')}
                aria-expanded={helpVisible}
                aria-controls="wf-board-utility"
                title={t('toolbar.helpTitle')}
                onClick={() => setHelpVisible((value) => !value)}
              >
                <ToolbarIcon name="help" />
              </button>
              <button
                type="button"
                className="wf-toolbar-icon-button wf-immersive-action-button"
                aria-label={selectedIds.size > 0 ? t('toolbar.expandSelected') : t('toolbar.expandAll')}
                title={selectedIds.size > 0 ? t('toolbar.expandSelectedTitle') : t('toolbar.expandAllTitle')}
                onClick={() => expandTargets(true)}
              >
                <ToolbarIcon name="expand" />
              </button>
              <button
                type="button"
                className="wf-toolbar-icon-button wf-immersive-action-button"
                aria-label={selectedIds.size > 0 ? t('toolbar.collapseSelected') : t('toolbar.collapseAll')}
                title={selectedIds.size > 0 ? t('toolbar.collapseSelectedTitle') : t('toolbar.collapseAllTitle')}
                onClick={() => expandTargets(false)}
              >
                <ToolbarIcon name="collapse" />
              </button>
              {isDemo ? (
                <>
                  {canGoBack ? (
                    <button type="button" className="wf-board-button" onClick={goBack}>{t('toolbar.back')}</button>
                  ) : null}
                  <button
                    type="button"
                    className={hotspotsVisible ? 'wf-board-button is-active' : 'wf-board-button'}
                    onClick={() => setHotspotsVisible((value) => !value)}
                    title={t('toolbar.hotspotsTitle', { modifier: shortcutModifier })}
                  >
                    {hotspotsVisible ? t('toolbar.hotspotsOn') : t('toolbar.hotspotsOff')}
                  </button>
                </>
              ) : null}
            </div>
          ) : null}
          <button
            type="button"
            className="wf-toolbar-icon-button wf-immersive-toolbar-toggle"
            aria-expanded={immersiveToolbarExpanded}
            aria-label={immersiveToolbarExpanded ? t('immersive.collapseToolbar') : t('immersive.expandToolbar')}
            title={immersiveToolbarExpanded ? t('immersive.collapseToolbar') : t('immersive.expandToolbar')}
            onClick={() => setImmersiveToolbarExpanded((value) => !value)}
          >
            <ToolbarIcon name={immersiveToolbarExpanded ? 'toolbarCollapse' : 'toolbarExpand'} />
          </button>
        </div>
      ) : null}

      {mode === 'canvas' ? (
        <CanvasMode
          project={project}
          scale={canvasScale}
          setScale={setCanvasScale}
          canvasLocked={canvasLocked}
          wheelZoomOptions={wheelZoomOptions}
          selectedIds={selectedIds}
          setSelectedIds={setSelectedIds}
          expandedIds={expandedIds}
          onToggleExpand={toggleExpand}
          onExportIds={exportIds}
          reviewEnabled={reviewEnabled}
          onReviewSelect={selectReviewElement}
          onCanvasClick={reviewPanelVisible ? closeReviewPanel : undefined}
          canvasIndexVisible={canvasIndexVisible}
          canvasIndexPosition={canvasIndexPosition}
          onCanvasIndexPositionChange={setCanvasIndexPosition}
          onCloseCanvasIndex={() => updateCanvasIndexVisible(false)}
        />
      ) : (
        <DemoMode
          project={project}
          hotspotsVisible={hotspotsVisible}
          canvasLocked={canvasLocked}
          scale={demoScale}
          setScale={setDemoScale}
          wheelZoomOptions={wheelZoomOptions}
          viewResetKey={demoViewResetKey}
          expandedIds={expandedIds}
          onToggleExpand={toggleExpand}
          reviewEnabled={reviewEnabled}
          onReviewSelect={selectReviewElement}
          onCanvasClick={reviewPanelVisible ? closeReviewPanel : undefined}
        />
      )}
      {reviewEnabled && reviewTool === 'modify' ? (
        <ReviewMarkers boardRef={boardRef} items={reviewItems} onOpenPanel={openReviewPanel} />
      ) : null}
      {showAnnotationMarkers || (reviewEnabled && reviewTool === 'annotation') ? (
        <AnnotationMarkers
          boardRef={boardRef}
          annotations={annotations}
          onOpenPanel={openAnnotationPanel}
        />
      ) : null}
      <ReviewLauncher
        boardRef={boardRef}
        count={reviewItems.length}
        projectName={project.name}
        onOpen={openReviewPanel}
      />
      {helpVisible ? (
        <ShortcutHelp
          demoAvailable={demoAvailable}
          showCanvasIndex={canvasIndexVisible}
          onShowCanvasIndexChange={updateCanvasIndexVisible}
          showAnnotationMarkers={showAnnotationMarkers}
          onShowAnnotationMarkersChange={updateShowAnnotationMarkers}
          trackpadZoom={trackpadZoom}
          onTrackpadZoomChange={updateTrackpadZoom}
          zoomSensitivity={zoomSensitivity}
          onZoomSensitivityChange={updateZoomSensitivity}
          demoUnlockInteraction={demoUnlockInteraction}
          onDemoUnlockInteractionChange={updateDemoUnlockInteraction}
          locale={locale}
          onLocaleChange={setLocale}
          onClose={() => setHelpVisible(false)}
        />
      ) : null}
      <ReviewPanel
        project={project}
        visible={reviewPanelVisible && reviewEnabled && reviewTool === 'modify'}
        selections={reviewSelections}
        multiSelect={reviewMultiSelect}
        items={reviewItems}
        onToggleMultiSelect={() => setReviewMultiSelect((value) => !value)}
        onSelectElement={(element) => selectReviewElement(element, null, null, {
          replaceElement: reviewSelections[reviewSelections.length - 1]?.element,
        })}
        onHoverElement={hoverReviewBreadcrumb}
        onRemoveSelection={removeReviewSelection}
        onClearSelection={clearReviewSelection}
        onAddItem={addReviewItem}
        onRemoveItem={removeReviewItem}
        onClose={closeReview}
      />
      <AnnotationPanel
        project={project}
        visible={reviewPanelVisible && reviewEnabled && reviewTool === 'annotation'}
        selection={reviewSelections[reviewSelections.length - 1] || null}
        currentScreenId={currentScreenId}
        annotations={annotations}
        operations={annotationOperations}
        storageSaved={annotationStorageSaved}
        onAdd={upsertAnnotation}
        onUpsert={upsertAnnotation}
        onDelete={deleteAnnotation}
        onImport={importAnnotations}
        onClearDraft={clearAnnotationDraft}
        onClearSelection={clearReviewSelection}
        onClose={closeReview}
      />
    </div>
  )
}
