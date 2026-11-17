import { createTranslator } from './i18n/context.jsx'

export const ANNOTATION_SCHEMA_VERSION = 1
export const UNSAVED_ANNOTATION_MESSAGE = '注释草稿未能保存在浏览器中，离开页面后会丢失。是否继续？'

const STORAGE_PREFIX = 'wf-annotations:v1:'

function slug(value) {
  return String(value || 'wireframe')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fff]+/g, '-')
    .replace(/^-+|-+$/g, '') || 'wireframe'
}

export function annotationProjectId(project) {
  return String(project?.id || slug(project?.name))
}

export function annotationBaseRevision(project) {
  return String(project?.annotationsRevision || 'annotations-empty')
}

export function annotationStorageKey(project) {
  return `${STORAGE_PREFIX}${annotationProjectId(project)}`
}

export function getAnnotationStorage() {
  try {
    return window.localStorage
  } catch {
    return null
  }
}

export function preventUnsavedAnnotationExit(event, message = UNSAVED_ANNOTATION_MESSAGE) {
  event.preventDefault()
  event.returnValue = message
  return message
}

function normalizeAnchor(anchor) {
  if (anchor?.kind === 'node' && anchor.selector) {
    const fallback = anchor.fallbackPosition
    return {
      kind: 'node',
      selector: String(anchor.selector),
      ...(fallback && Number.isFinite(fallback.x) && Number.isFinite(fallback.y)
        ? { fallbackPosition: {
          x: Math.max(0, Math.min(1, Number(fallback.x))),
          y: Math.max(0, Math.min(1, Number(fallback.y))),
        } }
        : {}),
    }
  }
  return { kind: 'screen' }
}

export function normalizeAnnotation(annotation) {
  if (!annotation?.id || !annotation?.screenId || !String(annotation.content || '').trim()) return null
  const createdAt = annotation.createdAt || new Date().toISOString()
  return {
    id: String(annotation.id),
    screenId: String(annotation.screenId),
    screenTitle: String(annotation.screenTitle || annotation.screenId),
    anchor: normalizeAnchor(annotation.anchor),
    content: String(annotation.content).trim(),
    createdAt: String(createdAt),
    updatedAt: String(annotation.updatedAt || createdAt),
  }
}

export function baseAnnotations(project) {
  if (!Array.isArray(project?.annotations)) return []
  return project.annotations.map(normalizeAnnotation).filter(Boolean)
}

function annotationEqual(left, right) {
  return JSON.stringify(normalizeAnnotation(left)) === JSON.stringify(normalizeAnnotation(right))
}

export function applyAnnotationOperations(base, operations) {
  const byId = new Map((base || []).map((item) => {
    const normalized = normalizeAnnotation(item)
    return normalized ? [normalized.id, normalized] : null
  }).filter(Boolean))

  for (const operation of operations || []) {
    if (operation?.op === 'delete' && operation.id) {
      byId.delete(String(operation.id))
      continue
    }
    if (operation?.op === 'upsert') {
      const annotation = normalizeAnnotation(operation.annotation)
      if (annotation) byId.set(annotation.id, annotation)
    }
  }

  return [...byId.values()].sort((left, right) => {
    const time = left.createdAt.localeCompare(right.createdAt)
    return time || left.id.localeCompare(right.id)
  })
}

export function reconcileAnnotationOperations(base, operations) {
  const baseById = new Map((base || []).map((item) => [item.id, normalizeAnnotation(item)]))
  const latest = new Map()

  for (const operation of operations || []) {
    if (operation?.op === 'delete' && operation.id) {
      latest.set(String(operation.id), { op: 'delete', id: String(operation.id) })
      continue
    }
    if (operation?.op === 'upsert') {
      const annotation = normalizeAnnotation(operation.annotation)
      if (annotation) latest.set(annotation.id, { op: 'upsert', annotation })
    }
  }

  return [...latest.values()].filter((operation) => {
    const baseItem = baseById.get(operation.op === 'delete' ? operation.id : operation.annotation.id)
    if (operation.op === 'delete') return !!baseItem
    return !baseItem || !annotationEqual(baseItem, operation.annotation)
  })
}

export function upsertAnnotationOperation(base, operations, annotation) {
  const normalized = normalizeAnnotation(annotation)
  if (!normalized) return reconcileAnnotationOperations(base, operations)
  return reconcileAnnotationOperations(base, [
    ...(operations || []).filter((operation) => {
      const id = operation.op === 'delete' ? operation.id : operation.annotation?.id
      return id !== normalized.id
    }),
    { op: 'upsert', annotation: normalized },
  ])
}

export function deleteAnnotationOperation(base, operations, id) {
  const normalizedId = String(id)
  const baseHasItem = (base || []).some((item) => item.id === normalizedId)
  const next = (operations || []).filter((operation) => {
    const operationId = operation.op === 'delete' ? operation.id : operation.annotation?.id
    return operationId !== normalizedId
  })
  if (baseHasItem) next.push({ op: 'delete', id: normalizedId })
  return reconcileAnnotationOperations(base, next)
}

export function readAnnotationDraft(storage, project) {
  const empty = {
    schemaVersion: ANNOTATION_SCHEMA_VERSION,
    projectId: annotationProjectId(project),
    baseRevision: annotationBaseRevision(project),
    operations: [],
  }
  if (!storage?.getItem) return empty
  try {
    const parsed = JSON.parse(storage.getItem(annotationStorageKey(project)) || 'null')
    if (!parsed || parsed.schemaVersion !== ANNOTATION_SCHEMA_VERSION) return empty
    if (parsed.projectId !== empty.projectId || !Array.isArray(parsed.operations)) return empty
    return {
      ...empty,
      baseRevision: String(parsed.baseRevision || empty.baseRevision),
      operations: reconcileAnnotationOperations(baseAnnotations(project), parsed.operations),
    }
  } catch {
    return empty
  }
}

export function saveAnnotationDraft(storage, project, operations) {
  if (!storage?.setItem || !storage?.removeItem) return false
  const key = annotationStorageKey(project)
  try {
    if (!operations?.length) {
      storage.removeItem(key)
      return true
    }
    storage.setItem(key, JSON.stringify({
      schemaVersion: ANNOTATION_SCHEMA_VERSION,
      projectId: annotationProjectId(project),
      baseRevision: annotationBaseRevision(project),
      operations,
    }))
    return true
  } catch {
    return false
  }
}

export function createAnnotationExport(project, annotations, operations = [], t = createTranslator('zh-CN')) {
  return {
    schemaVersion: ANNOTATION_SCHEMA_VERSION,
    projectId: annotationProjectId(project),
    projectName: project?.name || t('prompt.annotation.unnamedProject'),
    baseRevision: annotationBaseRevision(project),
    exportedAt: new Date().toISOString(),
    annotations: (annotations || []).map(normalizeAnnotation).filter(Boolean),
    operations: reconcileAnnotationOperations(baseAnnotations(project), operations),
  }
}

export function parseAnnotationImport(value, project, t = createTranslator('zh-CN')) {
  const parsed = typeof value === 'string' ? JSON.parse(value) : value
  if (!parsed || parsed.schemaVersion !== ANNOTATION_SCHEMA_VERSION) {
    throw new Error(t('import.annotation.unsupportedVersion'))
  }
  if (parsed.projectId !== annotationProjectId(project)) {
    throw new Error(t('import.annotation.wrongProject', {
      name: parsed.projectName || parsed.projectId,
    }))
  }
  if (!Array.isArray(parsed.annotations)) throw new Error(t('import.annotation.missingArray'))
  const annotations = parsed.annotations.map(normalizeAnnotation).filter(Boolean)
  if (annotations.length !== parsed.annotations.length) throw new Error(t('import.annotation.invalidEntries'))
  const operations = reconcileAnnotationOperations(
    baseAnnotations(project),
    Array.isArray(parsed.operations) ? parsed.operations : [],
  )
  return { ...parsed, annotations, operations }
}

export function buildAnnotationSyncPrompt(project, operations, t = createTranslator('zh-CN')) {
  const projectName = project?.name || t('prompt.annotation.unnamedProject')
  const normalized = reconcileAnnotationOperations(baseAnnotations(project), operations)
  const payload = {
    schemaVersion: ANNOTATION_SCHEMA_VERSION,
    projectId: annotationProjectId(project),
    baseRevision: annotationBaseRevision(project),
    operations: normalized,
  }
  return [
    t('prompt.annotation.intro', { projectName }),
    '',
    t('prompt.annotation.constraintsTitle'),
    t('prompt.annotation.constraint1'),
    t('prompt.annotation.constraint2'),
    t('prompt.annotation.constraint3'),
    t('prompt.annotation.constraint4'),
    t('prompt.annotation.constraint5'),
    '',
    t('prompt.annotation.operationsTitle'),
    '```json',
    JSON.stringify(payload, null, 2),
    '```',
  ].join('\n')
}
