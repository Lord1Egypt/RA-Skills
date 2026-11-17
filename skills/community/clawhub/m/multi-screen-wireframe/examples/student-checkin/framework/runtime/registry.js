(function initWireframeVue(global) {
  'use strict'

  if (!global.Vue) throw new Error('Vue Global runtime is required before registry.js')
  if (global.WireframeVue) throw new Error('WireframeVue has already been initialized')

  const Vue = global.Vue
  const supportedFormat = 'vue-global'
  const supportedFormatVersion = 2
  const screenRecords = new Map()
  const componentRecords = new Map()
  const keys = Object.freeze({
    screenId: Symbol('wireframe-screen-id'),
    viewportKey: Symbol('wireframe-viewport-key'),
  })
  let project = null
  let annotationState = { annotationsRevision: 'annotations-r1', annotations: [] }
  let uiInstaller = null

  function fail(message) {
    throw new Error(`[vue-global-wireframe] ${message}`)
  }

  function assertScreenId(id) {
    if (typeof id !== 'string' || !/^[a-z0-9-]+$/.test(id)) {
      fail(`screen id "${String(id)}" must match /^[a-z0-9-]+$/`)
    }
  }

  function sourceFor(id) {
    return `src/screens/${id}.js`
  }

  function assertComponentName(name) {
    if (typeof name !== 'string' || !/^Wf[A-Z][A-Za-z0-9]*$/.test(name)) {
      fail(`business component name "${String(name)}" must start with Wf and use PascalCase`)
    }
  }

  function formatCompilerProblem(problem) {
    if (!problem) return 'Unknown Vue template compiler error'
    const location = problem.loc && problem.loc.start
      ? `:${problem.loc.start.line}:${problem.loc.start.column}`
      : ''
    return `${problem.message || String(problem)}${location}`
  }

  function apiForScreens() {
    return Object.freeze({
      ref: Vue.ref,
      shallowRef: Vue.shallowRef,
      reactive: Vue.reactive,
      readonly: Vue.readonly,
      computed: Vue.computed,
      watch: Vue.watch,
      watchEffect: Vue.watchEffect,
      onMounted: Vue.onMounted,
      onUnmounted: Vue.onUnmounted,
      nextTick: Vue.nextTick,
      useScreenId() {
        const value = Vue.inject(keys.screenId, null)
        if (!value) fail('useScreenId() must be called inside a registered screen setup()')
        return value
      },
      useViewportKey() {
        return Vue.inject(keys.viewportKey, Vue.ref(''))
      },
    })
  }

  function compileDefinition(label, source, factory) {
    try {
      if (typeof factory !== 'function') fail(`${label} must register with a factory function`)
      const definition = factory(apiForScreens())
      if (!definition || typeof definition !== 'object') {
        fail(`${label} factory must return a Vue component object`)
      }
      if (typeof definition.template !== 'string' || !definition.template.trim()) {
        fail(`${label} must provide a non-empty template string`)
      }

      const compilerErrors = []
      const compilerWarnings = []
      const render = Vue.compile(definition.template, {
        onError(problem) {
          compilerErrors.push(problem)
        },
        onWarn(problem) {
          compilerWarnings.push(problem)
        },
      })
      if (compilerErrors.length) {
        fail(`${source} template failed: ${compilerErrors.map(formatCompilerProblem).join('; ')}`)
      }

      return {
        warnings: compilerWarnings.map(formatCompilerProblem),
        component: Object.freeze({
        ...definition,
        template: undefined,
        render,
        }),
      }
    } catch (error) {
      return { error: error instanceof Error ? error : new Error(String(error)) }
    }
  }

  function defineScreen(id, factory) {
    assertScreenId(id)
    if (screenRecords.has(id)) fail(`duplicate screen registration "${id}"`)
    const record = { id, source: sourceFor(id), component: null, error: null, warnings: [] }
    screenRecords.set(id, record)
    const result = compileDefinition(`screen "${id}"`, record.source, factory)
    Object.assign(record, result)
    if (record.component) {
      record.component = Object.freeze({
        ...record.component,
        name: record.component.name || `WireframeScreen_${id.replace(/-/g, '_')}`,
      })
    }
    if (record.error) console.error(`[wireframe:screen-registration:${id}]`, record.error)
  }

  function defineComponent(name, factory) {
    assertComponentName(name)
    if (componentRecords.has(name)) fail(`duplicate business component registration "${name}"`)
    const source = document.currentScript && document.currentScript.src
      ? new URL(document.currentScript.src).pathname.split('/').slice(-3).join('/')
      : name
    const record = { name, source, component: null, error: null, warnings: [] }
    componentRecords.set(name, record)
    const result = compileDefinition(`business component "${name}"`, source, factory)
    Object.assign(record, result)
    if (record.component) record.component = Object.freeze({ ...record.component, name })
    if (record.error) console.error(`[wireframe:component-registration:${name}]`, record.error)
  }

  function recordLoadFailure(id, reason) {
    assertScreenId(id)
    if (screenRecords.has(id)) return
    const error = reason instanceof Error ? reason : new Error(String(reason))
    screenRecords.set(id, {
      id,
      source: sourceFor(id),
      component: null,
      error,
      warnings: [],
    })
    console.error(`[wireframe:screen-load:${id}]`, error)
  }

  function defineProject(value) {
    if (project) fail('project has already been defined')
    if (!value || typeof value !== 'object') fail('project must be an object')
    if (value.format !== supportedFormat || value.formatVersion !== supportedFormatVersion) {
      fail(`project format must be ${supportedFormat}@${supportedFormatVersion}; cross-major framework upgrades are not supported`)
    }
    project = value
  }

  function defineAnnotations(value) {
    if (!value || typeof value !== 'object') fail('annotation state must be an object')
    annotationState = {
      annotationsRevision: value.annotationsRevision || 'annotations-r1',
      annotations: Array.isArray(value.annotations) ? value.annotations : [],
    }
  }

  function setUiInstaller(installer) {
    if (uiInstaller) fail('Vue UI installer has already been defined')
    if (typeof installer !== 'function') fail('Vue UI installer must be a function')
    uiInstaller = installer
  }

  function getProject() {
    if (!project) fail('src/project.js did not call WireframeVue.defineProject()')
    return project
  }

  function getScreen(id) {
    return screenRecords.get(id) || null
  }

  function installUi(app) {
    if (!uiInstaller) fail('framework/runtime/ui.js was not loaded')
    uiInstaller(app)
    for (const record of componentRecords.values()) {
      if (!record.component) fail(`${record.source} failed to register ${record.name}: ${record.error && record.error.message}`)
      app.component(record.name, record.component)
    }
  }

  function validateRegistrations() {
    const value = getProject()
    if (!Array.isArray(value.screens) || value.screens.length === 0) {
      fail('project.screens must contain at least one screen')
    }

    const expected = new Set()
    for (const screen of value.screens) {
      assertScreenId(screen && screen.id)
      if (expected.has(screen.id)) fail(`duplicate project screen "${screen.id}"`)
      expected.add(screen.id)
      if (!screenRecords.has(screen.id)) {
        recordLoadFailure(screen.id, new Error(`${sourceFor(screen.id)} did not register its screen`))
      }
    }

    const orphanIds = [...screenRecords.keys()].filter((id) => !expected.has(id))
    if (orphanIds.length) fail(`orphan screen registrations: ${orphanIds.join(', ')}`)

    return value.screens.map((screen) => screenRecords.get(screen.id))
  }

  global.WireframeVue = Object.freeze({
    keys,
    defineScreen,
    defineProject,
    defineAnnotations,
    recordLoadFailure,
    setUiInstaller,
    getProject,
    getScreen,
    getAnnotations() {
      return annotationState
    },
    installUi,
    validateRegistrations,
    defineComponent,
    getComponent(name) {
      return componentRecords.get(name) || null
    },
  })
})(window)
