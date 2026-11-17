export const MIN_ZOOM_SENSITIVITY = 0.25
export const MAX_ZOOM_SENSITIVITY = 2
export const DEFAULT_ZOOM_SENSITIVITY = 0.6

export function detectMacOS(navigatorLike = typeof navigator === 'undefined' ? null : navigator) {
  const platform = navigatorLike?.userAgentData?.platform || navigatorLike?.platform || ''
  if (/^mac/i.test(platform)) return true
  return /Macintosh|Mac OS X/i.test(navigatorLike?.userAgent || '')
}

function defaultSettings(navigatorLike) {
  return {
    showCanvasIndex: true,
    showAnnotationMarkers: true,
    trackpadZoom: detectMacOS(navigatorLike),
    zoomSensitivity: DEFAULT_ZOOM_SENSITIVITY,
    demoUnlockInteraction: true,
  }
}

export function normalizeZoomSensitivity(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return DEFAULT_ZOOM_SENSITIVITY
  return Math.min(MAX_ZOOM_SENSITIVITY, Math.max(MIN_ZOOM_SENSITIVITY, number))
}

export function getBoardStorage() {
  try {
    return typeof window === 'undefined' ? null : window.localStorage
  } catch {
    return null
  }
}

export function boardSettingsStorageKey(projectName) {
  return `wf-board-settings:${projectName}`
}

export function readBoardSettings(
  storage,
  projectName,
  navigatorLike = typeof navigator === 'undefined' ? null : navigator,
) {
  const defaults = defaultSettings(navigatorLike)
  try {
    const parsed = JSON.parse(storage?.getItem(boardSettingsStorageKey(projectName)))
    if (parsed && typeof parsed === 'object') {
      return {
        showCanvasIndex: parsed.showCanvasIndex !== false,
        showAnnotationMarkers: parsed.showAnnotationMarkers !== false,
        trackpadZoom: typeof parsed.trackpadZoom === 'boolean'
          ? parsed.trackpadZoom
          : defaults.trackpadZoom,
        zoomSensitivity: normalizeZoomSensitivity(parsed.zoomSensitivity),
        demoUnlockInteraction: parsed.demoUnlockInteraction !== false,
      }
    }
  } catch {
    // file:// storage can be unavailable or contain stale data.
  }
  return defaults
}

export function saveBoardSettings(storage, projectName, settings) {
  const normalized = {
    showCanvasIndex: settings.showCanvasIndex !== false,
    showAnnotationMarkers: settings.showAnnotationMarkers !== false,
    trackpadZoom: settings.trackpadZoom === true,
    zoomSensitivity: normalizeZoomSensitivity(settings.zoomSensitivity),
    demoUnlockInteraction: settings.demoUnlockInteraction !== false,
  }
  try {
    storage?.setItem(boardSettingsStorageKey(projectName), JSON.stringify(normalized))
    return true
  } catch {
    // Settings remain usable for the current session without persistence.
    return false
  }
}
