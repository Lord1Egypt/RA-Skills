const PrototypeContext = React.createContext(null)

function getInitialScreenId(project) {
  return project.screens.find((screen) => screen.entry)?.id || project.screens[0].id
}

export function PrototypeProvider({ project, children }) {
  const initialScreenId = getInitialScreenId(project)
  const [state, setState] = React.useState({
    mode: 'canvas',
    viewportKey: project.defaultViewport,
    entryId: initialScreenId,
    currentScreenId: initialScreenId,
    history: [],
  })

  const navigate = React.useCallback((id) => {
    if (!project.screens.some((screen) => screen.id === id)) {
      throw new Error(`Navigation target "${id}" does not exist`)
    }
    setState((current) => {
      if (current.mode === 'demo' && id !== current.currentScreenId) {
        const screen = project.screens.find((item) => item.id === current.currentScreenId)
        if (!screen.links.includes(id)) {
          throw new Error(`Screen "${current.currentScreenId}" links do not include "${id}"`)
        }
      }
      return {
        ...current,
        currentScreenId: id,
        history:
          current.mode === 'demo' && id !== current.currentScreenId
            ? [...current.history, current.currentScreenId]
            : current.history,
      }
    })
  }, [project])

  const selectEntry = React.useCallback((entryId) => {
    const entry = project.screens.find((screen) => screen.id === entryId)
    if (!entry) throw new Error(`Navigation target "${entryId}" does not exist`)
    setState((current) => ({
      ...current,
      entryId,
      currentScreenId: entryId,
      history: [],
    }))
  }, [project])

  const goBack = React.useCallback(() => {
    setState((current) => {
      if (current.history.length === 0) return current
      return {
        ...current,
        currentScreenId: current.history[current.history.length - 1],
        history: current.history.slice(0, -1),
      }
    })
  }, [])

  const reset = React.useCallback(() => {
    setState((current) => ({
      ...current,
      currentScreenId: current.entryId,
      history: [],
    }))
  }, [initialScreenId])

  const setMode = React.useCallback((mode) => {
    if (mode !== 'canvas' && mode !== 'demo') throw new Error(`Unknown mode "${mode}"`)
    setState((current) => ({
      ...current,
      mode,
      history: [],
    }))
  }, [])

  /** 画板双击某页：进入演示并落在该页 */
  const enterDemo = React.useCallback((screenId) => {
    if (!project.screens.some((screen) => screen.id === screenId)) {
      throw new Error(`Navigation target "${screenId}" does not exist`)
    }
    setState((current) => ({
      ...current,
      mode: 'demo',
      currentScreenId: screenId,
      history: [],
    }))
  }, [project])

  const setViewportKey = React.useCallback((viewportKey) => {
    if (!Object.hasOwn(project.viewports, viewportKey)) {
      throw new Error(`Unknown viewport "${viewportKey}"`)
    }
    setState((current) => ({ ...current, viewportKey }))
  }, [project])

  const value = React.useMemo(() => ({
    mode: state.mode,
    viewportKey: state.viewportKey,
    viewport: project.viewports[state.viewportKey],
    entryId: state.entryId,
    currentScreenId: state.currentScreenId,
    navigate,
    goBack,
    reset,
    selectEntry,
    setMode,
    enterDemo,
    setViewportKey,
    canGoBack: state.history.length > 0,
  }), [enterDemo, goBack, navigate, project, reset, selectEntry, setMode, setViewportKey, state])

  return <PrototypeContext.Provider value={value}>{children}</PrototypeContext.Provider>
}

export function usePrototype() {
  const context = React.useContext(PrototypeContext)
  if (!context) throw new Error('usePrototype must be used inside PrototypeProvider')
  return context
}
