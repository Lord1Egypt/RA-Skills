const EASE = 'cubic-bezier(.4,0,.2,1)'
const DURATION = 650

function delta(el: HTMLElement): [number, number] {
  return [Number(el.dataset.moveX ?? 0), Number(el.dataset.moveY ?? 0)]
}

export function motionSteps(frame: HTMLElement): number[] {
  return Array.from(frame.querySelectorAll<HTMLElement>('[data-move-step]'))
    .map((el) => Number(el.dataset.moveStep))
    .filter((step) => Number.isInteger(step) && step > 1)
}

// 每次进帧前复位；从下一帧回看时直接显示平移后的最终位置。
export function setMotionState(frame: HTMLElement, finished: boolean): void {
  frame.querySelectorAll<HTMLElement>('[data-move-step]').forEach((el) => {
    el.getAnimations().forEach((animation) => animation.cancel())
    const [x, y] = delta(el)
    el.style.transform = finished ? `translate(${x}px, ${y}px)` : ''
  })
}

// 元素在当前帧已经可见，按 PgDn 才从原位平移到目标位置。
export async function playMotion(frame: HTMLElement, step: number): Promise<void> {
  const targets = Array.from(frame.querySelectorAll<HTMLElement>('[data-move-step]'))
    .filter((el) => Number(el.dataset.moveStep) === step)

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  await Promise.all(targets.map(async (el) => {
    const [x, y] = delta(el)
    const finish = `translate(${x}px, ${y}px)`
    if (reduced || typeof el.animate !== 'function') {
      el.style.transform = finish
      return
    }

    const duration = Number(el.dataset.moveDuration ?? DURATION)
    const animation = el.animate(
      [{ transform: getComputedStyle(el).transform }, { transform: finish }],
      { duration, easing: EASE, fill: 'both' },
    )
    try {
      await animation.finished
      el.style.transform = finish
    } finally {
      animation.cancel()
    }
  }))
}
