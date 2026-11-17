import { buildReviewPrompt, reviewTargets, reviewTypeLabels } from './review.js'
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

export function ReviewPanel({
  project,
  visible = true,
  selections,
  multiSelect,
  items,
  onToggleMultiSelect,
  onSelectElement,
  onHoverElement,
  onRemoveSelection,
  onClearSelection,
  onAddItem,
  onRemoveItem,
  onClose,
}) {
  const t = useT()
  const typeLabels = reviewTypeLabels(t)
  const selected = selections[selections.length - 1] || null
  const generatedPrompt = React.useMemo(() => buildReviewPrompt(project, items, t), [project, items, t])
  const [type, setType] = React.useState('comment')
  const [instruction, setInstruction] = React.useState('')
  const [prompt, setPrompt] = React.useState(generatedPrompt)
  const [promptDirty, setPromptDirty] = React.useState(false)
  const [copied, setCopied] = React.useState(false)
  const copyTimer = React.useRef(null)

  React.useEffect(() => {
    if (!promptDirty) setPrompt(generatedPrompt)
  }, [generatedPrompt, promptDirty])

  React.useEffect(() => () => {
    if (copyTimer.current) window.clearTimeout(copyTimer.current)
  }, [])

  const addItem = () => {
    if (selections.length === 0) return
    const normalized = instruction.trim()
    if (!normalized && type !== 'remove') return
    onAddItem({
      type,
      targets: selections.map((selection) => ({
        screenId: selection.screenId,
        screenTitle: selection.screenTitle,
        sourceHint: selection.sourceHint,
        selector: selection.selector,
        currentText: selection.currentText,
      })),
      instruction: normalized,
    })
    setInstruction('')
  }

  const regenerate = () => {
    setPrompt(generatedPrompt)
    setPromptDirty(false)
  }

  const copyPrompt = () => {
    copyText(prompt).then(() => {
      setCopied(true)
      if (copyTimer.current) window.clearTimeout(copyTimer.current)
      copyTimer.current = window.setTimeout(() => setCopied(false), 1400)
    })
  }

  const instructionLabel = type === 'text'
    ? t('review.instruction.text')
    : type === 'order'
      ? t('review.instruction.order')
      : type === 'remove'
        ? t('review.instruction.remove')
        : t('review.instruction.comment')

  return (
    <aside className="wf-review-panel" aria-label={t('review.panelAria')} hidden={!visible}>
      <header className="wf-review-panel-header">
        <div className="wf-review-panel-heading">
          <strong className="wf-review-panel-title">{t('review.title')}</strong>
          <span className="wf-review-panel-count">{t('review.count', { count: items.length })}</span>
        </div>
        <button type="button" className="wf-review-close" onClick={onClose}>{t('review.close')}</button>
      </header>

      <div className="wf-review-panel-body">
        <section className="wf-review-section">
          <div className="wf-review-selection-heading">
            <h2 className="wf-review-section-heading">{t('review.selectedHeading', { count: selections.length })}</h2>
            <div className="wf-review-selection-actions">
              <button
                type="button"
                className={multiSelect ? 'wf-review-multi-select is-active' : 'wf-review-multi-select'}
                aria-pressed={multiSelect}
                onClick={onToggleMultiSelect}
              >
                {t('review.multiSelect')} {multiSelect ? 'ON' : 'OFF'}
              </button>
              {selections.length > 0 ? (
                <button className="wf-review-clear-selection" type="button" onClick={onClearSelection}>{t('review.clear')}</button>
              ) : null}
            </div>
          </div>
          <p className="wf-review-selection-hint">{t('review.selectionHint')}</p>
          {selections.length > 0 ? (
            <ol className="wf-review-selections">
              {selections.map((selection, index) => (
                <li className={selection === selected ? 'wf-review-selection is-active' : 'wf-review-selection'} key={`${selection.screenId}:${selection.selector}`}>
                  <code className="wf-review-selection-selector">{index + 1}. {selection.selector}</code>
                  <button className="wf-review-selection-remove" type="button" onClick={() => onRemoveSelection(selection.element)}>{t('review.remove')}</button>
                </li>
              ))}
            </ol>
          ) : null}
          {selected ? (
            <>
              <div className="wf-review-screen-name">{selected.screenTitle} · {selected.screenId}</div>
              <div className="wf-review-breadcrumbs" aria-label={t('review.breadcrumbAria')}>
                {selected.ancestors.map((ancestor, index) => (
                  <React.Fragment key={ancestor.selector}>
                    {index > 0 ? (
                      <span className="wf-review-breadcrumb-sep" aria-hidden="true">
                        <svg viewBox="0 0 24 24">
                          <path d="m9 18 6-6-6-6" />
                        </svg>
                      </span>
                    ) : null}
                    <button
                      className="wf-review-breadcrumb"
                      type="button"
                      title={ancestor.selector}
                      onMouseEnter={() => onHoverElement?.(ancestor.element)}
                      onMouseLeave={() => onHoverElement?.(null)}
                      onClick={() => onSelectElement(ancestor.element)}
                    >
                      {ancestor.label}
                    </button>
                  </React.Fragment>
                ))}
              </div>
              <code className="wf-review-selector">{selected.selector}</code>
              {selected.currentText ? (
                <p className="wf-review-current-text">{t('review.currentText', { text: selected.currentText })}</p>
              ) : null}
              <label className="wf-review-field">
                <span className="wf-review-field-label">{t('review.typeLabel')}</span>
                <select className="wf-review-type-select" value={type} onChange={(event) => setType(event.target.value)}>
                  {Object.entries(typeLabels).map(([value, label]) => (
                    <option className="wf-review-type-option" value={value} key={value}>{label}</option>
                  ))}
                </select>
              </label>
              <label className="wf-review-field">
                <span className="wf-review-field-label">{instructionLabel}</span>
                <textarea
                  className="wf-review-instruction"
                  value={instruction}
                  placeholder={type === 'order' ? t('review.placeholder.order') : t('review.placeholder.default')}
                  onChange={(event) => setInstruction(event.target.value)}
                />
              </label>
              <button
                type="button"
                className="wf-review-add"
                disabled={!instruction.trim() && type !== 'remove'}
                onClick={addItem}
              >
                {t('review.add', { count: selections.length })}
              </button>
            </>
          ) : (
            <p className="wf-review-empty">{t('review.emptySelect')}</p>
          )}
        </section>

        <section className="wf-review-section">
          <h2 className="wf-review-section-heading">{t('review.listHeading')}</h2>
          {items.length > 0 ? (
            <ol className="wf-review-items">
              {items.map((item, index) => (
                <li className="wf-review-item" key={item.id}>
                  <div className="wf-review-item-content">
                    <strong className="wf-review-item-title">{index + 1}. {typeLabels[item.type]}</strong>
                    <code className="wf-review-item-selector">
                      {reviewTargets(item).map((target) => target.selector).join(t('review.targetSeparator'))}
                    </code>
                    <p className="wf-review-item-instruction">{item.instruction || t('review.removeDefaultInstruction')}</p>
                  </div>
                  <button className="wf-review-item-delete" type="button" onClick={() => onRemoveItem(item.id)}>{t('review.delete')}</button>
                </li>
              ))}
            </ol>
          ) : <p className="wf-review-empty">{t('review.emptyList')}</p>}
        </section>

        <section className="wf-review-section wf-review-prompt-section">
          <div className="wf-review-section-title">
            <h2 className="wf-review-section-heading">{t('review.promptHeading')}</h2>
            <button className="wf-review-regenerate" type="button" onClick={regenerate}>{t('review.regenerate')}</button>
          </div>
          {promptDirty ? <p className="wf-review-manual">{t('review.manualEditNote')}</p> : null}
          <textarea
            className="wf-review-prompt"
            value={prompt}
            onChange={(event) => {
              setPrompt(event.target.value)
              setPromptDirty(true)
            }}
          />
          <button type="button" className="wf-review-copy" onClick={copyPrompt}>
            {copied ? t('review.copied') : t('review.copy')}
          </button>
        </section>
      </div>
    </aside>
  )
}
