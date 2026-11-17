function fail(path, message) {
  throw new Error(`${path} ${message}`)
}

export function validateProject(project) {
  if (!project || typeof project !== 'object') fail('project', 'must be an object')
  if (!project.viewports || typeof project.viewports !== 'object') {
    fail('project.viewports', 'must be an object')
  }

  const viewportEntries = Object.entries(project.viewports)
  if (viewportEntries.length === 0) fail('project.viewports', 'must contain at least one viewport')
  for (const [key, viewport] of viewportEntries) {
    if (!viewport || typeof viewport !== 'object') fail(`project.viewports.${key}`, 'must be an object')
    for (const dimension of ['width', 'height']) {
      if (!Number.isFinite(viewport[dimension]) || viewport[dimension] <= 0) {
        fail(`project.viewports.${key}.${dimension}`, 'must be a positive number')
      }
    }
  }

  if (!Object.hasOwn(project.viewports, project.defaultViewport)) {
    fail('project.defaultViewport', `references missing viewport "${project.defaultViewport}"`)
  }
  if (!Array.isArray(project.screens) || project.screens.length === 0) {
    fail('project.screens', 'must contain at least one screen')
  }

  const ids = new Set()
  project.screens.forEach((screen, index) => {
    const path = `project.screens[${index}]`
    if (!screen || typeof screen !== 'object') fail(path, 'must be an object')
    if (typeof screen.id !== 'string' || !/^[a-z0-9-]+$/.test(screen.id)) {
      fail(`${path}.id`, 'must match /^[a-z0-9-]+$/')
    }
    if (ids.has(screen.id)) fail(`${path}.id`, `is duplicate "${screen.id}"`)
    ids.add(screen.id)
    if (typeof screen.component !== 'function') fail(`${path}.component`, 'must be a function')
    if (!Array.isArray(screen.links)) {
      fail(`${path}.links`, 'must be an array')
    }
  })

  project.screens.forEach((screen, screenIndex) => {
    screen.links.forEach((target, linkIndex) => {
      if (!ids.has(target)) {
        fail(
          `project.screens[${screenIndex}].links[${linkIndex}]`,
          `references missing screen "${target}"`,
        )
      }
    })
  })

  if (project.annotations != null) {
    if (!Array.isArray(project.annotations)) fail('project.annotations', 'must be an array')
    if (typeof project.annotationsRevision !== 'string' || !project.annotationsRevision) {
      fail('project.annotationsRevision', 'must be a non-empty string when annotations are provided')
    }
    const annotationIds = new Set()
    project.annotations.forEach((annotation, index) => {
      const path = `project.annotations[${index}]`
      if (!annotation || typeof annotation !== 'object') fail(path, 'must be an object')
      if (typeof annotation.id !== 'string' || !annotation.id) fail(`${path}.id`, 'must be a non-empty string')
      if (annotationIds.has(annotation.id)) fail(`${path}.id`, `is duplicate "${annotation.id}"`)
      annotationIds.add(annotation.id)
      if (!ids.has(annotation.screenId)) {
        fail(`${path}.screenId`, `references missing screen "${annotation.screenId}"`)
      }
      if (typeof annotation.content !== 'string' || !annotation.content.trim()) {
        fail(`${path}.content`, 'must be a non-empty string')
      }
      if (!annotation.anchor || !['screen', 'node'].includes(annotation.anchor.kind)) {
        fail(`${path}.anchor.kind`, 'must be "screen" or "node"')
      }
      if (annotation.anchor.kind === 'node' && !annotation.anchor.selector) {
        fail(`${path}.anchor.selector`, 'must be provided for a node annotation')
      }
    })
  }
}
