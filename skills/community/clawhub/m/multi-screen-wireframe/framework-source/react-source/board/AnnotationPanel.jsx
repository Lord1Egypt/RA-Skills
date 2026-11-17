import {
  annotationProjectId,
  buildAnnotationSyncPrompt,
  createAnnotationExport,
  parseAnnotationImport,
} from './annotations.js'
import { useT } from './i18n/context.jsx'

function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text)
  const area = document.createElement('textarea')
  area.value = text
  area.setAttribute('readonly', '')
  area.style.position = 'absolute'
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

function makeAnnotationId() {
  if (globalThis.crypto?.randomUUID) return `note-${globalThis.crypto.randomUUID()}`
  return `note-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
}

function fallbackPosition(selection) {
  const elementRect = selection?.element?.getBoundingClientRect?.()
  const rootRect = selection?.contentRoot?.getBoundingClientRect?.()
  if (!elementRect || !rootRect || !rootRect.width || !rootRect.height) return undefined
  return {
    x: Math.max(0, Math.min(1, (elementRect.right - rootRect.left) / rootRect.width)),
    y: Math.max(0, Math.min(1, (elementRect.top - rootRect.top) / rootRect.height)),
  }
}

function downloadJson(filename, value) {
  const blob = new Blob([JSON.stringify(value, null, 2)], { type: 'application/json;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.setTimeout(() => URL.revokeObjectURL(url), 1500)
}

function AnnotationItem({ annotation, pending, onUpsert, onDelete }) {
  const t = useT()
  const [editing, setEditing] = React.useState(false)
  const [content, setContent] = React.useState(annotation.content)

  React.useEffect(() => setContent(annotation.content), [annotation.content])

  const commit = () => {
    const normalized = content.trim()
    if (!normalized) return
    onUpsert({ ...annotation, content: normalized, updatedAt: new Date().toISOString() })
    setEditing(false)
  }

  return (
    <li className="wf-annotation-item">
      <div className="wf-annotation-item-meta">
        <strong>{annotation.screenTitle}</strong>
        <span>{annotation.anchor.kind === 'node' ? t('annotation.kindNode') : t('annotation.kindScreen')}</span>
        {pending ? <span className="wf-annotation-pending">{t('annotation.pending')}</span> : <span>{t('annotation.builtin')}</span>}
      </div>
      {annotation.anchor.kind === 'node' ? (
        <code className="wf-annotation-selector">{annotation.anchor.selector}</code>
      ) : null}
      {editing ? (
        <>
          <textarea
            className="wf-annotation-edit"
            value={content}
            onChange={(event) => setContent(event.target.value)}
          />
          <div className="wf-annotation-item-actions">
            <button type="button" onClick={commit} disabled={!content.trim()}>{t('annotation.save')}</button>
            <button type="button" onClick={() => {
              setContent(annotation.content)
              setEditing(false)
            }}>{t('annotation.cancel')}</button>
          </div>
        </>
      ) : (
        <p className="wf-annotation-content">{annotation.content}</p>
      )}
      {!editing ? (
        <div className="wf-annotation-item-actions">
          <button type="button" onClick={() => setEditing(true)}>{t('annotation.edit')}</button>
          <button type="button" onClick={() => onDelete(annotation.id)}>{t('annotation.delete')}</button>
        </div>
      ) : null}
    </li>
  )
}

export function AnnotationPanel({
  project,
  visible = true,
  selection,
  currentScreenId,
  annotations,
  operations,
  storageSaved,
  onAdd,
  onUpsert,
  onDelete,
  onImport,
  onClearDraft,
  onClearSelection,
  onClose,
}) {
  const t = useT()
  const selectedScreenId = selection?.screenId || currentScreenId || project.screens[0]?.id
  const [scope, setScope] = React.useState(selection ? 'node' : 'screen')
  const [screenId, setScreenId] = React.useState(selectedScreenId)
  const [content, setContent] = React.useState('')
  const [filter, setFilter] = React.useState('current')
  const [message, setMessage] = React.useState('')
  const generatedPrompt = React.useMemo(
    () => buildAnnotationSyncPrompt(project, operations, t),
    [operations, project, t],
  )
  const [prompt, setPrompt] = React.useState(generatedPrompt)
  const [promptDirty, setPromptDirty] = React.useState(false)
  const [clearArmed, setClearArmed] = React.useState(false)
  const inputRef = React.useRef(null)

  React.useEffect(() => {
    setScreenId(selectedScreenId)
    if (selection) setScope('node')
  }, [selectedScreenId, selection])

  React.useEffect(() => {
    if (!promptDirty) setPrompt(generatedPrompt)
  }, [generatedPrompt, promptDirty])

  React.useEffect(() => {
    if (!clearArmed) return undefined
    const timer = window.setTimeout(() => setClearArmed(false), 5000)
    return () => window.clearTimeout(timer)
  }, [clearArmed])

  const activeScreen = project.screens.find((screen) => screen.id === screenId) || project.screens[0]
  const pendingIds = new Set((operations || []).map((operation) => (
    operation.op === 'delete' ? operation.id : operation.annotation?.id
  )))
  const visibleAnnotations = annotations.filter((annotation) => {
    if (filter === 'current') return annotation.screenId === selectedScreenId
    return true
  })

  const add = () => {
    const normalized = content.trim()
    if (!normalized || !activeScreen) return
    const useNode = scope === 'node' && selection
    const now = new Date().toISOString()
    onAdd({
      id: makeAnnotationId(),
      screenId: useNode ? selection.screenId : activeScreen.id,
      screenTitle: useNode ? selection.screenTitle : activeScreen.title,
      anchor: useNode
        ? {
          kind: 'node',
          selector: selection.selector,
          fallbackPosition: fallbackPosition(selection),
        }
        : { kind: 'screen' },
      content: normalized,
      createdAt: now,
      updatedAt: now,
    })
    setContent('')
    setMessage(t('annotation.savedLocal'))
  }

  const exportReview = () => {
    const file = createAnnotationExport(project, annotations, operations, t)
    downloadJson(`${annotationProjectId(project)}.wireframe-annotations.json`, file)
    setMessage(t('annotation.exported', { count: annotations.length }))
  }

  const importReview = async (file) => {
    if (!file) return
    try {
      const parsed = parseAnnotationImport(await file.text(), project, t)
      onImport(parsed.annotations, parsed.operations)
      setMessage(t('annotation.imported', { count: parsed.annotations.length }))
    } catch (error) {
      setMessage(error?.message || t('annotation.importFailed'))
    } finally {
      if (inputRef.current) inputRef.current.value = ''
    }
  }

  return (
    <aside className="wf-review-panel wf-annotation-panel" aria-label={t('annotation.panelAria')} hidden={!visible}>
      <header className="wf-review-panel-header">
        <div className="wf-review-panel-heading">
          <strong className="wf-review-panel-title">{t('annotation.title')}</strong>
          <span className="wf-review-panel-count">{t('annotation.count', { count: annotations.length })}</span>
        </div>
        <button type="button" className="wf-review-close" onClick={onClose}>{t('annotation.close')}</button>
      </header>

      <div className="wf-review-panel-body">
        <section className="wf-review-section">
          <h2 className="wf-review-section-heading">{t('annotation.addHeading')}</h2>
          <div className="wf-annotation-scope" role="group" aria-label={t('annotation.scopeAria')}>
            <button
              type="button"
              className={scope === 'screen' ? 'is-active' : ''}
              onClick={() => setScope('screen')}
            >{t('annotation.scopeScreen')}</button>
            <button
              type="button"
              className={scope === 'node' ? 'is-active' : ''}
              disabled={!selection}
              onClick={() => setScope('node')}
            >{t('annotation.scopeNode')}</button>
          </div>
          {scope === 'node' && selection ? (
            <div className="wf-annotation-target">
              <span>{selection.screenTitle}</span>
              <code>{selection.selector}</code>
              <button type="button" onClick={onClearSelection}>{t('annotation.cancelSelection')}</button>
            </div>
          ) : (
            <label className="wf-review-field">
              <span className="wf-review-field-label">{t('annotation.pageLabel')}</span>
              <select value={screenId} onChange={(event) => setScreenId(event.target.value)}>
                {project.screens.map((screen) => (
                  <option value={screen.id} key={screen.id}>{screen.title} · {screen.id}</option>
                ))}
              </select>
            </label>
          )}
          <label className="wf-review-field">
            <span className="wf-review-field-label">{t('annotation.contentLabel')}</span>
            <textarea
              value={content}
              placeholder={scope === 'node' ? t('annotation.placeholderNode') : t('annotation.placeholderScreen')}
              onChange={(event) => setContent(event.target.value)}
            />
          </label>
          <button type="button" className="wf-review-add" disabled={!content.trim()} onClick={add}>
            {t('annotation.addSave')}
          </button>
          <p className={`wf-annotation-save-state${storageSaved ? '' : ' is-error'}`}>
            {storageSaved
              ? t('annotation.pendingSync', { count: operations.length })
              : t('annotation.storageError')}
          </p>
        </section>

        <section className="wf-review-section">
          <div className="wf-review-section-title">
            <h2 className="wf-review-section-heading">{t('annotation.listHeading')}</h2>
            <div className="wf-annotation-filters">
              <button type="button" className={filter === 'current' ? 'is-active' : ''} onClick={() => setFilter('current')}>{t('annotation.filterCurrent')}</button>
              <button type="button" className={filter === 'all' ? 'is-active' : ''} onClick={() => setFilter('all')}>{t('annotation.filterAll')}</button>
            </div>
          </div>
          {visibleAnnotations.length ? (
            <ol className="wf-annotation-items">
              {visibleAnnotations.map((annotation) => (
                <AnnotationItem
                  annotation={annotation}
                  pending={pendingIds.has(annotation.id)}
                  key={annotation.id}
                  onUpsert={onUpsert}
                  onDelete={onDelete}
                />
              ))}
            </ol>
          ) : <p className="wf-review-empty">{t('annotation.emptyList')}</p>}
        </section>

        <section className="wf-review-section">
          <div className="wf-review-section-title">
            <h2 className="wf-review-section-heading">{t('annotation.syncHeading')}</h2>
            {operations.length ? (
              <button className="wf-review-regenerate" type="button" onClick={() => {
                setPrompt(generatedPrompt)
                setPromptDirty(false)
              }}>{t('review.regenerate')}</button>
            ) : null}
          </div>
          {operations.length ? (
            <>
              <p className="wf-review-empty">{t('annotation.syncNote')}</p>
              <textarea
                className="wf-review-prompt wf-annotation-prompt"
                value={prompt}
                onChange={(event) => {
                  setPrompt(event.target.value)
                  setPromptDirty(true)
                }}
              />
              <button type="button" className="wf-review-copy" onClick={() => {
                copyText(prompt).then(() => setMessage(t('annotation.syncCopied')))
              }}>{t('annotation.copySyncPrompt')}</button>
            </>
          ) : <p className="wf-review-empty">{t('annotation.syncEmpty')}</p>}
          <div className="wf-annotation-file-actions">
            <button type="button" onClick={exportReview}>{t('annotation.exportJson')}</button>
            <button type="button" onClick={() => inputRef.current?.click()}>{t('annotation.importJson')}</button>
            {operations.length ? (
              <button type="button" onClick={() => {
                if (!clearArmed) {
                  setClearArmed(true)
                  setMessage(t('annotation.clearConfirmNote'))
                  return
                }
                onClearDraft()
                setClearArmed(false)
                setMessage(t('annotation.draftCleared'))
              }}>
                {clearArmed ? t('annotation.confirmClearDraft') : t('annotation.clearDraft')}
              </button>
            ) : null}
          </div>
          <input
            ref={inputRef}
            className="wf-annotation-file-input"
            type="file"
            accept="application/json,.json"
            onChange={(event) => importReview(event.target.files?.[0])}
          />
          {message ? <p className="wf-annotation-message" role="status">{message}</p> : null}
        </section>
      </div>
    </aside>
  )
}
