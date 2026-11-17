import { Board } from './react-source/board/Board.jsx'
import { PrototypeProvider, usePrototype } from './react-source/core/PrototypeContext.jsx'
import { validateProject } from './react-source/core/validateProject.js'

function VueScreenError({ screenId, error }) {
  return (
    <div className="wf-error-card" role="alert">
      <strong>{`Screen: ${screenId}`}</strong>
      <span>{`Source: src/screens/${screenId}.js`}</span>
      <span>{`Message: ${error.message}`}</span>
      <pre>{error.stack || String(error)}</pre>
    </div>
  )
}

function VueScreenHost({ screenId }) {
  const { viewportKey } = usePrototype()
  const hostRef = React.useRef(null)
  const appRef = React.useRef(null)
  const [runtimeError, setRuntimeError] = React.useState(null)
  const record = window.WireframeVue.getScreen(screenId)

  React.useEffect(() => {
    setRuntimeError(null)
    if (!record || record.error || !record.component || !hostRef.current) return undefined

    const viewportKeyRef = window.Vue.ref(viewportKey)
    const app = window.Vue.createApp(record.component)
    appRef.current = app
    window.WireframeVue.installUi(app)
    app.provide(window.WireframeVue.keys.screenId, screenId)
    app.provide(window.WireframeVue.keys.viewportKey, viewportKeyRef)
    app.config.errorHandler = (error, _instance, info) => {
      const normalized = error instanceof Error ? error : new Error(String(error))
      normalized.message = `${normalized.message} (${info})`
      console.error(`[wireframe:vue-screen:${screenId}]`, normalized)
      setRuntimeError(normalized)
    }
    app.config.warnHandler = (message, _instance, trace) => {
      console.warn(`[wireframe:vue-screen:${screenId}] ${message}${trace || ''}`)
      if (/Failed to resolve component|Invalid prop|Duplicate keys/.test(message)) {
        setRuntimeError(new Error(message))
      }
    }

    try {
      app.mount(hostRef.current)
    } catch (error) {
      const normalized = error instanceof Error ? error : new Error(String(error))
      console.error(`[wireframe:vue-screen-mount:${screenId}]`, normalized)
      setRuntimeError(normalized)
    }

    return () => {
      try {
        app.unmount()
      } catch (error) {
        console.error(`[wireframe:vue-screen-unmount:${screenId}]`, error)
      }
      appRef.current = null
    }
  }, [record, screenId, viewportKey])

  const error = !record
    ? new Error('Screen was not registered')
    : record.error || runtimeError

  return (
    <>
      <div
        ref={hostRef}
        className="wf-vue-screen-host"
        data-vue-screen-id={screenId}
        hidden={Boolean(error)}
      />
      {error ? <VueScreenError screenId={screenId} error={error} /> : null}
    </>
  )
}

function componentFor(screenId) {
  return function RegisteredVueScreen() {
    return <VueScreenHost screenId={screenId} />
  }
}

function mount() {
  const Wireframe = window.WireframeVue
  const sourceProject = Wireframe.getProject()
  const annotationState = Wireframe.getAnnotations()
  Wireframe.validateRegistrations()

  const project = {
    ...sourceProject,
    annotationsRevision: annotationState.annotationsRevision,
    annotations: annotationState.annotations,
    screens: sourceProject.screens.map((screen) => ({
      ...screen,
      component: componentFor(screen.id),
    })),
  }

  validateProject(project)
  const root = document.getElementById('root')
  if (!root) throw new Error('Missing #root mount element')

  ReactDOM.createRoot(root).render(
    <PrototypeProvider project={project}>
      <Board project={project} />
    </PrototypeProvider>,
  )

  window.__WF_VUE_GLOBAL__ = {
    mounted: true,
    project,
    screenIds: project.screens.map((screen) => screen.id),
  }
}

window.WireframeVueBoard = Object.freeze({ mount })
