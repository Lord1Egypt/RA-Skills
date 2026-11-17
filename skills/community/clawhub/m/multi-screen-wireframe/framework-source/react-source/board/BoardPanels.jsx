import { SUPPORTED_LOCALES } from './i18n/detect.js'
import { getBoardShortcuts } from './shortcuts.js'
import { useT } from './i18n/context.jsx'

const LOCALE_LABELS = {
  'zh-CN': '简体中文',
  'zh-TW': '繁體中文',
  en: 'English',
}

function PanelShell({ id, title, ariaLabel, onClose, children }) {
  const t = useT()
  const closeRef = React.useRef(null)
  const returnFocusRef = React.useRef(null)

  React.useEffect(() => {
    returnFocusRef.current = document.activeElement
    closeRef.current?.focus()
    return () => returnFocusRef.current?.focus?.()
  }, [])

  return (
    <div
      className="wf-board-panel-layer"
      onPointerDown={(event) => {
        if (event.target === event.currentTarget) onClose()
      }}
    >
      <section id={id} className="wf-board-panel" role="dialog" aria-modal="true" aria-label={ariaLabel}>
        <header className="wf-board-panel-header">
          <strong>{title}</strong>
          <button ref={closeRef} type="button" className="wf-board-panel-close" onClick={onClose} aria-label={t('panel.closeAria', { title })}>{t('panel.close')}</button>
        </header>
        <div className="wf-board-panel-body">{children}</div>
      </section>
    </div>
  )
}

export function ShortcutHelp({
  demoAvailable,
  showCanvasIndex,
  onShowCanvasIndexChange,
  showAnnotationMarkers,
  onShowAnnotationMarkersChange,
  trackpadZoom,
  onTrackpadZoomChange,
  zoomSensitivity,
  onZoomSensitivityChange,
  demoUnlockInteraction,
  onDemoUnlockInteractionChange,
  locale,
  onLocaleChange,
  onClose,
}) {
  const t = useT()
  const shortcuts = getBoardShortcuts(undefined, t)
  return (
    <PanelShell id="wf-board-utility" title={t('help.title')} ariaLabel={t('help.ariaLabel')} onClose={onClose}>
      <dl className="wf-shortcut-list">
        {shortcuts.map((shortcut) => (
          <div className={shortcut.id === 'demo' && !demoAvailable ? 'is-disabled' : ''} key={shortcut.id}>
            <dt><kbd>{shortcut.keys}</kbd></dt>
            <dd>{shortcut.label}{shortcut.id === 'demo' && !demoAvailable ? t('help.demoUnavailable') : ''}</dd>
          </div>
        ))}
      </dl>
      <p className="wf-board-panel-note">{t('help.shortcutNote')}</p>
      <section className="wf-board-panel-section" aria-labelledby="wf-board-index-setting-title">
        <h2 id="wf-board-index-setting-title">{t('settings.title')}</h2>
        <label className="wf-board-setting-row">
          <span>
            <strong>{t('settings.language')}</strong>
          </span>
          <select value={locale} onChange={(event) => onLocaleChange(event.target.value)}>
            {SUPPORTED_LOCALES.map((value) => (
              <option value={value} key={value}>{LOCALE_LABELS[value]}</option>
            ))}
          </select>
        </label>
        <label className="wf-board-setting-row">
          <span>
            <strong>{t('settings.showCanvasIndex')}</strong>
            <small>{t('settings.showCanvasIndexDesc')}</small>
          </span>
          <input
            type="checkbox"
            checked={showCanvasIndex}
            onChange={(event) => onShowCanvasIndexChange(event.target.checked)}
          />
        </label>
        <label className="wf-board-setting-row">
          <span>
            <strong>{t('settings.showAnnotationMarkers')}</strong>
            <small>{t('settings.showAnnotationMarkersDesc')}</small>
          </span>
          <input
            type="checkbox"
            checked={showAnnotationMarkers}
            onChange={(event) => onShowAnnotationMarkersChange(event.target.checked)}
          />
        </label>
        <label className="wf-board-setting-row">
          <span>
            <strong>{t('settings.demoUnlockInteraction')}</strong>
            <small>{t('settings.demoUnlockInteractionDesc')}</small>
          </span>
          <input
            type="checkbox"
            checked={demoUnlockInteraction}
            onChange={(event) => onDemoUnlockInteractionChange(event.target.checked)}
          />
        </label>
        <label className="wf-board-setting-row">
          <span>
            <strong>{t('settings.trackpadZoom')}</strong>
            <small>{t('settings.trackpadZoomDesc')}</small>
          </span>
          <input
            type="checkbox"
            checked={trackpadZoom}
            onChange={(event) => onTrackpadZoomChange(event.target.checked)}
          />
        </label>
        <label className={`wf-board-setting-range${trackpadZoom ? '' : ' is-disabled'}`}>
          <span>
            <strong>{t('settings.zoomSensitivity')}</strong>
            <output>{Math.round(zoomSensitivity * 100)}%</output>
          </span>
          <input
            type="range"
            min="0.25"
            max="2"
            step="0.05"
            value={zoomSensitivity}
            disabled={!trackpadZoom}
            onChange={(event) => onZoomSensitivityChange(Number(event.target.value))}
            aria-label={t('settings.zoomSensitivityAria')}
          />
          <small><span>{t('settings.zoomLess')}</span><span>{t('settings.zoomMore')}</span></small>
        </label>
      </section>
    </PanelShell>
  )
}
