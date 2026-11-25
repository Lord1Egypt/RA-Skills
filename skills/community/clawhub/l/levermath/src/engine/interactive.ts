export type InteractiveMounter = (el: HTMLElement) => void

const registry = new Map<string, InteractiveMounter>()

export function registerInteractive(name: string, mount: InteractiveMounter): void {
  registry.set(name, mount)
}

// 帧挂载完成后调用一次，把 [data-interactive] 的容器交给对应的挂载函数。
export function mountInteractives(root: ParentNode = document): void {
  root.querySelectorAll<HTMLElement>('[data-interactive]').forEach((el) => {
    const name = el.dataset.interactive
    if (!name || el.dataset.mounted === '1') return
    const mount = registry.get(name)
    if (!mount) {
      console.warn(`[interactive] 未注册的挂载名：${name}`)
      return
    }
    el.dataset.mounted = '1'
    mount(el)
  })
}
