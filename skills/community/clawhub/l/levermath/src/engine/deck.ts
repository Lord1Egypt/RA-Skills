import { Stage } from './stage'
import { mountInteractives } from './interactive'
import { mountMath } from './math'
import { playEnter } from './enter'
import type { FrameSpec } from './types'

// 应用外壳：左侧关键帧总览、右侧舞台、底部工具条、全屏演示。
export class Deck {
  private stage: Stage
  private root: HTMLElement
  private stageWrap: HTMLElement
  private stageEl: HTMLElement
  private thumbsEl: HTMLElement
  private pageEl: HTMLElement
  private presentBtn: HTMLButtonElement
  private thumbs: HTMLElement[] = []
  private ready = false

  constructor(root: HTMLElement) {
    this.root = root
    root.classList.add('deck')
    root.innerHTML = `
      <aside class="deck-side"><div class="deck-thumbs"></div></aside>
      <main class="deck-main">
        <div class="deck-stage-wrap"><div class="stage"></div></div>
        <div class="deck-bar">
          <span class="deck-page"></span>
          <span class="deck-actions">
            <button type="button" data-act="prev">上一页</button>
            <button type="button" data-act="next">下一页</button>
            <button type="button" data-act="present">演示</button>
          </span>
        </div>
      </main>`

    this.stageWrap = root.querySelector('.deck-stage-wrap')!
    this.stageEl = root.querySelector('.stage')!
    this.thumbsEl = root.querySelector('.deck-thumbs')!
    this.pageEl = root.querySelector('.deck-page')!
    this.presentBtn = root.querySelector('[data-act="present"]')!

    this.stage = new Stage(this.stageEl, {
      onChange: (index, count) => this.sync(index, count),
    })

    root.querySelector('[data-act="prev"]')!.addEventListener('click', () => this.stage.prev())
    root.querySelector('[data-act="next"]')!.addEventListener('click', () => this.stage.next())
    this.presentBtn.addEventListener('click', () => void this.togglePresent())

    document.addEventListener('fullscreenchange', () => {
      const on = document.fullscreenElement === this.root
      this.root.classList.toggle('presenting', on)
      this.presentBtn.textContent = on ? '退出演示' : '演示'
      this.fit()
    })

    new ResizeObserver(() => this.fit()).observe(this.stageWrap)
    this.bindKeys()
  }

  mount(specs: FrameSpec[]): this {
    this.stage.mount(specs)
    // 缩略图是克隆出来的，公式要在克隆之前渲染，否则侧栏一片空
    mountMath()

    // 缩略图直接克隆帧内容并整体缩放，比壳的 iframe 缩略图轻。
    this.stage.frameEls.forEach((frame, i) => {
      const thumb = document.createElement('button')
      thumb.type = 'button'
      thumb.className = 'thumb'
      thumb.dataset.index = String(i)
      thumb.setAttribute('aria-label', frame.dataset.name ?? `第 ${i + 1} 帧`)

      const inner = document.createElement('div')
      inner.className = 'thumb-inner'
      const clone = frame.cloneNode(true) as HTMLElement
      clone.style.display = 'block'
      clone.removeAttribute('data-frame')
      inner.appendChild(clone)

      thumb.appendChild(inner)
      thumb.addEventListener('click', () => this.stage.go(i))
      this.thumbsEl.appendChild(thumb)
      this.thumbs.push(thumb)
    })

    this.fit()
    this.ready = true
    mountInteractives(this.stage.frameEls[0])
    playEnter(this.stage.frameEls[0], 1)
    return this
  }

  private sync(index: number, count: number): void {
    const pad = (n: number) => String(n).padStart(2, '0')
    this.pageEl.textContent = `${pad(index + 1)} / ${pad(count)}`
    this.thumbs.forEach((t, i) => t.classList.toggle('active', i === index))
    // 目标帧此时已显示，可以安全地给隐藏时无法测量的交互组件初始化
    if (this.ready) {
      mountInteractives()
      playEnter(this.stage.frameEls[index], 1)
    }
  }

  private fit(): void {
    const rect = this.stageWrap.getBoundingClientRect()
    const pad = this.root.classList.contains('presenting') ? 0 : 24
    const w = Math.max(0, rect.width - pad * 2)
    const h = Math.max(0, rect.height - pad * 2)
    const s = Math.min(w / this.stage.width, h / this.stage.height)
    this.stageEl.style.transform = `scale(${Math.max(0.05, s)})`
  }

  private async togglePresent(): Promise<void> {
    if (document.fullscreenElement) {
      await document.exitFullscreen().catch(() => undefined)
      return
    }
    await this.root.requestFullscreen().catch(() => undefined)
  }

  private bindKeys(): void {
    document.addEventListener(
      'keydown',
      (e) => {
        const t = e.target as HTMLElement | null
        const tag = t?.tagName?.toLowerCase() ?? ''
        if (tag === 'input' || tag === 'textarea' || tag === 'select' || t?.isContentEditable) return

        if (e.key === 'PageDown' || e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
          e.preventDefault()
          this.stage.next()
        } else if (e.key === 'PageUp' || e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          e.preventDefault()
          this.stage.prev()
        }
      },
      true,
    )
  }
}
