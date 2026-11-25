const EASE = 'cubic-bezier(.22,.61,.36,1)'
const DURATION = 480

export function keyedMap(frame: HTMLElement): Map<string, HTMLElement> {
  const map = new Map<string, HTMLElement>()
  frame.querySelectorAll<HTMLElement>('[data-k]').forEach((el) => {
    const k = el.dataset.k
    if (k) map.set(k, el)
  })
  return map
}

export function plainChildren(frame: HTMLElement, shared: Set<string>): HTMLElement[] {
  return Array.from(frame.children).filter((el) => {
    const k = (el as HTMLElement).dataset.k
    // 含 data-enter 的子树交给入场动画，morph 不再做整体淡入，避免透明度叠加
    const hasEnter = el.hasAttribute('data-enter') || !!el.querySelector('[data-enter]')
    return (!k || !shared.has(k)) && !hasEnter
  }) as HTMLElement[]
}

// 帧间 morph：共享 key 的元素带身份飞行，其余元素淡入淡出。
// scale 是整个舞台被 CSS 缩放的比例，rect 差值要除回去。
export function morphFrames(
  from: HTMLElement,
  to: HTMLElement,
  scale: number,
  duration = DURATION,
): Promise<void> {
  const ka = keyedMap(from)
  const kb = keyedMap(to)
  const shared = [...ka.keys()].filter((k) => kb.has(k))
  const sharedSet = new Set(shared)

  to.style.display = 'block'
  to.style.visibility = 'hidden'

  const pairs = shared.map((k) => {
    const A = ka.get(k)!
    const B = kb.get(k)!
    const ra = A.getBoundingClientRect()
    const rb = B.getBoundingClientRect()
    const scaling = A.hasAttribute('data-scale') && ra.width > 0 && rb.width > 0
    return {
      A,
      B,
      dx: (rb.left - ra.left) / scale,
      dy: (rb.top - ra.top) / scale,
      sx: scaling ? rb.width / ra.width : 1,
      sy: scaling ? rb.height / ra.height : 1,
      scaling,
    }
  })

  to.style.visibility = ''

  const anims: Animation[] = []

  for (const p of pairs) {
    const toTransform =
      `translate(${p.dx}px,${p.dy}px)` +
      (p.scaling ? ` scale(${p.sx},${p.sy})` : '')
    const fromTransform =
      `translate(${-p.dx}px,${-p.dy}px)` +
      (p.scaling ? ` scale(${1 / p.sx},${1 / p.sy})` : '')

    anims.push(
      p.A.animate(
        [{ transform: 'none', opacity: 1 }, { transform: toTransform, opacity: 0 }],
        { duration, easing: EASE, fill: 'both' },
      ),
    )
    anims.push(
      p.B.animate(
        [{ transform: fromTransform, opacity: 0 }, { transform: 'none', opacity: 1 }],
        { duration, easing: EASE, fill: 'both' },
      ),
    )
  }

  for (const el of plainChildren(from, sharedSet)) {
    anims.push(
      el.animate([{ opacity: 1 }, { opacity: 0 }], {
        duration: duration / 2,
        easing: 'ease-out',
        fill: 'both',
      }),
    )
  }

  for (const el of plainChildren(to, sharedSet)) {
    anims.push(
      el.animate([{ opacity: 0 }, { opacity: 1 }], {
        duration: 320,
        delay: 140,
        easing: 'ease-out',
        fill: 'both',
      }),
    )
  }

  return Promise.all(anims.map((a) => a.finished.catch(() => undefined))).then(() => {
    anims.forEach((a) => {
      try {
        a.cancel()
      } catch {
        // 元素可能已被移除，忽略
      }
    })
    from.style.display = 'none'
  })
}
