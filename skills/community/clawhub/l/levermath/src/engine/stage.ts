import { morphFrames } from './morph'
import { hideLaterSteps, playEnter, revealAll, stepsOf } from './enter'
import { motionSteps, playMotion, setMotionState } from './motion'
import type { FrameSpec } from './types'

export interface StageOptions {
  width?: number
  height?: number
  onChange?: (index: number, count: number) => void
}

// 只负责帧的渲染与 morph，不管侧栏、缩放和全屏。
export class Stage {
  readonly width: number
  readonly height: number
  private frames: HTMLElement[] = []
  private cur = 0
  private busy = false
  private step = 1
  private steps: number[] = [1]
  private onChange?: (index: number, count: number) => void

  constructor(
    private container: HTMLElement,
    opts: StageOptions = {},
  ) {
    this.width = opts.width ?? 1280
    this.height = opts.height ?? 720
    this.onChange = opts.onChange
    container.style.width = `${this.width}px`
    container.style.height = `${this.height}px`
  }

  mount(specs: FrameSpec[]): void {
    specs.forEach((spec, i) => {
      const frame = document.createElement('section')
      frame.className = 'frame'
      frame.dataset.frame = spec.id
      frame.dataset.name = spec.name
      frame.innerHTML = spec.html
      frame.style.display = i === 0 ? 'block' : 'none'
      this.container.appendChild(frame)
      this.frames.push(frame)
    })
    this.prepare()
    this.emit()
  }

  // 初次挂载没有经过 go()，也要算好首帧的步骤与隐藏状态。
  prepare(): void {
    const frame = this.frames[this.cur]
    if (!frame) return
    this.steps = [...new Set([...stepsOf(frame), ...motionSteps(frame)])].sort((a, b) => a - b)
    this.step = this.steps[0]
    hideLaterSteps(frame)
    setMotionState(frame, false)
  }

  go(n: number, reveal = false): void {
    if (this.busy || n < 0 || n >= this.frames.length || n === this.cur) return

    const from = this.frames[this.cur]
    const to = this.frames[n]
    // 先让目标帧可见，交互组件（如 JSXGraph）才能量到容器尺寸
    to.style.display = 'block'
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    this.busy = true
    this.cur = n
    this.steps = [...new Set([...stepsOf(to), ...motionSteps(to)])].sort((a, b) => a - b)
    if (reveal) {
      revealAll(to)
      setMotionState(to, true)
      this.step = this.steps[this.steps.length - 1]
    } else {
      this.step = this.steps[0]
      hideLaterSteps(to)
      setMotionState(to, false)
    }
    this.emit()
    // 交互组件可以监听自己所在帧的 frameenter，做自动演示之类的开场
    to.dispatchEvent(new CustomEvent('frameenter', { bubbles: true }))

    if (reduce) {
      from.style.display = 'none'
      to.style.display = 'block'
      this.busy = false
      return
    }

    morphFrames(from, to, this.scaleFactor()).then(() => {
      this.busy = false
    })
  }

  // 翻页时先看本帧还有没有没放出来的步骤，有就先放一步，没有才翻页
  next(): void {
    if (this.busy) return
    const frame = this.frames[this.cur]
    const i = this.steps.indexOf(this.step)
    if (i >= 0 && i < this.steps.length - 1) {
      this.step = this.steps[i + 1]
      playEnter(frame, this.step)
      this.busy = true
      void playMotion(frame, this.step).catch((error: unknown) => {
        console.error('帧内平移动画失败', error)
      }).finally(() => {
        this.busy = false
      })
      return
    }
    this.go(this.cur + 1)
  }

  // 往回翻时把上一帧的步骤全部放出来，免得内容缺一半
  prev(): void {
    if (this.busy) return
    this.go(this.cur - 1, true)
  }

  get index(): number {
    return this.cur
  }

  get count(): number {
    return this.frames.length
  }

  get frameEls(): HTMLElement[] {
    return this.frames.slice()
  }

  private emit(): void {
    this.onChange?.(this.cur, this.frames.length)
  }

  private scaleFactor(): number {
    const w = this.container.getBoundingClientRect().width || this.width
    return w / this.width
  }
}
