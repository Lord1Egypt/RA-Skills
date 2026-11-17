(function loadVueGlobalScreens(global) {
  'use strict'

  const Wireframe = global.WireframeVue
  const project = Wireframe.getProject()

  function injectScript(source, dataset) {
    return new Promise((resolve) => {
      const script = document.createElement('script')
      script.src = source
      script.async = false
      Object.assign(script.dataset, dataset)
      script.onload = () => resolve(true)
      script.onerror = () => resolve(false)
      document.head.appendChild(script)
    })
  }

  async function loadBusinessComponent(entry) {
    const loaded = await injectScript(entry.source, { componentName: entry.name })
    if (!loaded) throw new Error(`Unable to load ${entry.source}`)
    const record = Wireframe.getComponent(entry.name)
    if (!record) throw new Error(`${entry.source} loaded but did not register "${entry.name}"`)
    if (record.error) throw record.error
  }

  async function loadScreen(screen) {
    const id = screen.id
    const source = screen.source || `src/screens/${id}.js`
    const loaded = await injectScript(source, { screenId: id })
    if (!loaded) Wireframe.recordLoadFailure(id, new Error(`Unable to load ${source}`))
    else if (!Wireframe.getScreen(id)) Wireframe.recordLoadFailure(id, new Error(`${source} loaded but did not register "${id}"`))
  }

  async function boot() {
    for (const entry of project.components || []) {
      await loadBusinessComponent(entry)
    }
    for (const screen of project.screens) {
      await loadScreen(screen)
    }
    Wireframe.validateRegistrations()
    if (!global.WireframeVueBoard || typeof global.WireframeVueBoard.mount !== 'function') {
      throw new Error('Vue/React Board bridge was not loaded')
    }
    global.WireframeVueBoard.mount()
  }

  boot().catch((error) => {
    console.error('[wireframe:vue-global-boot]', error)
    const root = document.getElementById('root')
    if (root) {
      root.innerHTML = ''
      const card = document.createElement('div')
      card.className = 'wf-error-card wf-boot-error'
      card.setAttribute('role', 'alert')
      const title = document.createElement('strong')
      title.textContent = 'Vue Global 原型启动失败'
      const message = document.createElement('span')
      message.textContent = error.message || String(error)
      card.append(title, message)
      root.appendChild(card)
    }
  })
})(window)
