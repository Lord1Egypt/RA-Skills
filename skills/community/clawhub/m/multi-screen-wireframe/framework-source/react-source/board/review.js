import { createTranslator } from './i18n/context.jsx'

const TYPE_LABELS = {
  comment: '修改建议',
  text: '修改文字',
  order: '调整顺序',
  remove: '删除节点',
}

export function reviewTypeLabels(t) {
  return {
    comment: t('review.type.comment'),
    text: t('review.type.text'),
    order: t('review.type.order'),
    remove: t('review.type.remove'),
  }
}

function escapeSelectorToken(value) {
  if (globalThis.CSS?.escape) return globalThis.CSS.escape(String(value))
  return String(value).replace(/[^a-zA-Z0-9_-]/g, (char) => `\\${char}`)
}

function escapeAttributeValue(value) {
  return String(value).replace(/\\/g, '\\\\').replace(/"/g, '\\"')
}

function classesOf(element) {
  if (!element?.classList) return []
  return Array.from(element.classList).filter(Boolean)
}

export function isBusinessClassName(name) {
  return !!name && !name.startsWith('wf-') && !name.startsWith('is-')
}

function selectorScope(screenId) {
  return `[data-screen-id="${escapeAttributeValue(screenId)}"]`
}

function selectorIsUnique(screenRoot, selector) {
  try {
    return screenRoot.querySelectorAll(selector).length === 1
  } catch {
    return false
  }
}

function elementSegment(element) {
  const tag = (element.tagName || 'div').toLowerCase()
  const classes = classesOf(element)
  const business = classes.filter(isBusinessClassName)
  const usable = business.length > 0 ? business : classes.filter((name) => !name.startsWith('is-'))
  const classPart = usable.slice(0, 2).map((name) => `.${escapeSelectorToken(name)}`).join('')
  const key = element.getAttribute?.('data-wf-key')
  const keyPart = key ? `[data-wf-key="${escapeAttributeValue(key)}"]` : ''
  return `${tag}${classPart}${keyPart}`
}

export function buildReviewSelector(element, contentRoot, screenId) {
  if (!element || !contentRoot || !screenId) return ''
  if (element.id) return `#${escapeSelectorToken(element.id)}`

  const scope = selectorScope(screenId)
  const key = element.getAttribute?.('data-wf-key')
  const keyPart = key ? `[data-wf-key="${escapeAttributeValue(key)}"]` : ''
  const business = classesOf(element).filter(isBusinessClassName)

  for (const name of business) {
    const local = `.${escapeSelectorToken(name)}${keyPart}`
    if (selectorIsUnique(contentRoot, local)) return `${scope} ${local}`
  }

  if (business.length > 1) {
    const local = business.map((name) => `.${escapeSelectorToken(name)}`).join('') + keyPart
    if (selectorIsUnique(contentRoot, local)) return `${scope} ${local}`
  }

  const segments = []
  let current = element
  while (current && current !== contentRoot) {
    if (current.id) {
      segments.unshift(`#${escapeSelectorToken(current.id)}`)
      break
    }
    let segment = elementSegment(current)
    const parent = current.parentElement
    if (parent && parent !== contentRoot) {
      const peers = Array.from(parent.children || []).filter(
        (item) => item.tagName === current.tagName && elementSegment(item) === segment,
      )
      if (peers.length > 1) segment += `:nth-of-type(${peers.indexOf(current) + 1})`
    }
    segments.unshift(segment)
    const local = segments.join(' > ')
    if (selectorIsUnique(contentRoot, local)) return `${scope} ${local}`
    current = parent
  }

  return `${scope} ${segments.join(' > ') || elementSegment(element)}`
}

function displayLabel(element) {
  if (element.id) return `#${element.id}`
  const classes = classesOf(element)
  const semantic = classes.find(isBusinessClassName) || classes.find((name) => !name.startsWith('is-'))
  return semantic ? `.${semantic}` : (element.tagName || 'node').toLowerCase()
}

function readText(element) {
  const value = 'value' in element && typeof element.value === 'string'
    ? element.value
    : element.textContent || ''
  const normalized = value.replace(/\s+/g, ' ').trim()
  return normalized.length > 240 ? `${normalized.slice(0, 237)}...` : normalized
}

export function findReviewTarget(target, contentRoot) {
  let current = target?.nodeType === 1 ? target : target?.parentElement
  while (current && current !== contentRoot) {
    if (current.id || classesOf(current).length > 0) return current
    current = current.parentElement
  }
  return null
}

export function describeReviewElement(element, contentRoot, screen) {
  if (!element || !contentRoot || !screen) return null
  const ancestors = []
  let current = element
  while (current && current !== contentRoot) {
    ancestors.unshift({
      element: current,
      label: displayLabel(current),
      selector: buildReviewSelector(current, contentRoot, screen.id),
    })
    current = current.parentElement
  }

  return {
    element,
    contentRoot,
    screenId: screen.id,
    screenTitle: screen.title,
    sourceHint: `src/screens/${screen.id}.js`,
    selector: buildReviewSelector(element, contentRoot, screen.id),
    tagName: (element.tagName || '').toLowerCase(),
    classNames: classesOf(element),
    currentText: readText(element),
    ancestors,
  }
}

function itemRequest(item, t) {
  if (item.type === 'text') return t('prompt.review.request.text', { instruction: item.instruction })
  if (item.type === 'order') return t('prompt.review.request.order', { instruction: item.instruction })
  if (item.type === 'remove') {
    return t('prompt.review.request.remove', {
      instruction: item.instruction || t('prompt.review.removeDefault'),
    })
  }
  return item.instruction
}

export function reviewTargets(item) {
  if (Array.isArray(item?.targets) && item.targets.length > 0) return item.targets
  if (!item?.selector) return []
  return [{
    screenId: item.screenId,
    screenTitle: item.screenTitle,
    sourceHint: item.sourceHint,
    selector: item.selector,
    currentText: item.currentText,
  }]
}

export function buildReviewPrompt(project, items, t = createTranslator('zh-CN')) {
  const typeLabels = reviewTypeLabels(t)
  const projectName = project?.name || t('prompt.review.unnamedProject')

  const lines = [
    t('prompt.review.intro', { projectName }),
    '',
    t('prompt.review.constraintsTitle'),
    t('prompt.review.constraint1'),
    t('prompt.review.constraint2'),
    t('prompt.review.constraint3'),
    t('prompt.review.constraint4'),
    t('prompt.review.constraint5'),
    t('prompt.review.constraint6'),
  ]

  if (!items?.length) {
    lines.push('', t('prompt.review.noItems'))
    return lines.join('\n')
  }

  items.forEach((item, itemIndex) => {
    const targets = reviewTargets(item)
    const type = typeLabels[item.type] || typeLabels.comment
    lines.push('', t('prompt.review.section', { index: itemIndex + 1, type }))
    targets.forEach((target, targetIndex) => {
      const screenId = target.screenId || item.screenId
      const title = target.screenTitle || item.screenTitle || screenId || t('prompt.review.unnamedScreen')
      const sourceHint = target.sourceHint || item.sourceHint || (
        screenId ? `src/screens/${screenId}.js` : t('prompt.review.searchSelector')
      )
      lines.push(
        '',
        t('prompt.review.target', { index: targetIndex + 1, title }),
        t('prompt.review.screenId', { id: screenId || t('prompt.review.unknownScreenId') }),
        t('prompt.review.sourceHint', { hint: sourceHint }),
        t('prompt.review.selectorTitle'),
        `\`${target.selector}\``,
      )
      if (target.currentText) lines.push('', t('prompt.review.currentContent'), target.currentText)
    })
    lines.push('', t('prompt.review.requestTitle'), itemRequest(item, t))
  })

  lines.push(
    '',
    t('prompt.review.completionTitle'),
    t('prompt.review.completion1'),
    t('prompt.review.completion2'),
    t('prompt.review.completion3'),
  )
  return lines.join('\n')
}

export const REVIEW_TYPE_LABELS = TYPE_LABELS
