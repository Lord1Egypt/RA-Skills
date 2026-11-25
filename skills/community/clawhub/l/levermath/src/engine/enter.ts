const EASE = 'cubic-bezier(.22,.61,.36,1)'
const DIST = 18

type Direction = 'up' | 'down' | 'left' | 'right' | 'fade'

function offset(dir: Direction): [number, number] {
  switch (dir) {
    case 'down':
      return [0, -DIST]
    case 'left':
      return [DIST, 0]
    case 'right':
      return [-DIST, 0]
    case 'fade':
      return [0, 0]
    default:
      return [0, DIST]
  }
}

// 帧内元素的分步序号，没写就算第一步
export function stepOf(el: HTMLElement): number {
  return Number(el.dataset.step ?? 1) || 1
}

export function stepsOf(frame: HTMLElement): number[] {
  const set = new Set<number>([1])
  frame.querySelectorAll<HTMLElement>('[data-enter]').forEach((el) => set.add(stepOf(el)))
  return [...set].sort((a, b) => a - b)
}

// 进入一帧时先把后面的步骤按住，等 PgDn 再放出来
export function hideLaterSteps(frame: HTMLElement): void {
  frame.querySelectorAll<HTMLElement>('[data-enter]').forEach((el) => {
    if (stepOf(el) > 1) el.style.opacity = '0'
  })
}

export function revealAll(frame: HTMLElement): void {
  frame.querySelectorAll<HTMLElement>('[data-enter]').forEach((el) => {
    el.style.opacity = ''
    el.style.transform = ''
  })
}

// 只播一批：帧里写 data-enter，data-step="2" 表示第二步才出现
export function playEnter(frame: HTMLElement, step?: number): void {
  const els = Array.from(frame.querySelectorAll<HTMLElement>('[data-enter]')).filter(
    (el) => step === undefined || stepOf(el) === step,
  )
  if (els.length === 0) return

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduce) {
    els.forEach((el) => {
      el.style.opacity = ''
      el.style.transform = ''
    })
    return
  }

  els.forEach((el, i) => {
    const dir = (el.dataset.enter || 'up') as Direction
    const delay = Number(el.dataset.enterDelay ?? i * 70)
    const duration = Number(el.dataset.enterDuration ?? 420)
    const [dx, dy] = offset(dir)

    const anim = el.animate(
      [
        { opacity: 0, transform: `translate(${dx}px, ${dy}px)` },
        { opacity: 1, transform: 'none' },
      ],
      { duration, delay, easing: EASE, fill: 'both' },
    )

    anim.finished
      .then(() => {
        anim.cancel()
        el.style.opacity = ''
        el.style.transform = ''
      })
      .catch(() => {
        el.style.opacity = ''
        el.style.transform = ''
      })
  })
}
