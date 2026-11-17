const SHORTCUT_DEFINITIONS = [
  { id: 'canvas', suffix: '1' },
  { id: 'demo', suffix: '2' },
  { id: 'interaction', suffix: 'I' },
  { id: 'review', suffix: 'M' },
  { id: 'immersive', suffix: '3' },
  { id: 'browser-fullscreen', suffix: 'Shift+F' },
  { id: 'hotspots', suffix: 'H' },
  { id: 'space', keys: 'Space' },
  { id: 'escape', keys: 'Esc' },
  { id: 'help', keys: '?' },
]

export function isMacPlatform() {
  if (typeof navigator === 'undefined') return false
  return /Mac|iPhone|iPad|iPod/i.test(`${navigator.platform || ''} ${navigator.userAgent || ''}`)
}

export function shortcutModifierLabel(isMac = isMacPlatform()) {
  return isMac ? 'Ctrl' : 'Alt'
}

export function getBoardShortcuts(isMac = isMacPlatform(), t = (key) => key) {
  const modifier = shortcutModifierLabel(isMac)
  return SHORTCUT_DEFINITIONS.map((shortcut) => ({
    ...shortcut,
    label: t(`shortcut.${shortcut.id}`),
    keys: shortcut.keys || `${modifier}+${shortcut.suffix}`,
  }))
}

export function isEditableShortcutTarget(target) {
  if (!target) return false
  const element = target.nodeType === 3 ? target.parentElement : target
  if (!element) return false
  const tag = element.tagName
  if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return true
  if (element.isContentEditable) return true
  return !!element.closest?.('[contenteditable]:not([contenteditable="false"])')
}

export function shortcutIdForEvent(event, isMac = isMacPlatform()) {
  if (!event || event.repeat) return null
  const key = String(event.key || '').toLowerCase()
  const modifier = isMac ? event.ctrlKey : event.altKey

  if (!modifier) {
    if (!event.shiftKey && key === 'escape') return 'escape'
    if (event.key === '?') return 'help'
    return null
  }

  if (event.shiftKey) return key === 'f' ? 'browser-fullscreen' : null
  if (key === '1') return 'canvas'
  if (key === '2') return 'demo'
  if (key === 'i') return 'interaction'
  if (key === 'm') return 'review'
  if (key === '3') return 'immersive'
  if (key === 'h') return 'hotspots'
  return null
}
