import JXG from 'jsxgraph'
import katex from 'katex'
import 'katex/dist/katex.min.css'

const INK = '#2a2724'
const GOLD = '#a98342'
const ACCENT = '#b5342a'

const R = 5
const F1X = -4

// 图内默认字体按 docs 统一成 Latin Modern；标签内容仍由 KaTeX 覆盖
// fontFamily 运行时支持，类型声明里没有
;(JXG.Options.text as unknown as { fontFamily: string }).fontFamily = 'Latin Modern Roman'
JXG.Options.text.fontSize = 14

// JSXGraph 的标签是 HTML div，内容交给 KaTeX，斜体与下标才正确
function renderLabel(obj: any, tex: string, color = INK): void {
  const node: HTMLElement | undefined = obj?.label?.rendNode
  if (!node) return
  katex.render(tex, node, { throwOnError: false, displayMode: false, output: 'html' })
  node.style.color = color
  node.style.fontSize = '19px'
  node.style.fontFamily = 'inherit'
}

// 折痕是 PF1 的垂直平分线，求它与圆的交点，圆内那一段就是折痕
function creaseChord(px: number, py: number): [number, number, number, number] | null {
  const mx = (px + F1X) / 2
  const my = py / 2
  const nx = px - F1X
  const ny = py
  const len = Math.hypot(nx, ny)
  if (len < 1e-9) return null
  const tx = -ny / len
  const ty = nx / len
  const b = 2 * (mx * tx + my * ty)
  const c = mx * mx + my * my - R * R
  const disc = b * b - 4 * c
  if (disc < 0) return null
  const s = Math.sqrt(disc) / 2
  const a0 = -b / 2 - s
  const a1 = -b / 2 + s
  return [mx + a0 * tx, my + a0 * ty, mx + a1 * tx, my + a1 * ty]
}

type Mode = 'crease' | 'trace'

export function mountOrigami(el: HTMLElement, mode: Mode): void {
  const frame = el.closest('.frame') as HTMLElement | null
  const readout = frame?.querySelector<HTMLElement>('[data-readout]')
  const playBtn = frame?.querySelector<HTMLButtonElement>('[data-act="play"]')
  const clearBtn = frame?.querySelector<HTMLButtonElement>('[data-act="clear"]')

  const board = JXG.JSXGraph.initBoard(el, {
    renderer: 'svg',
    boundingbox: [-6.4, 5.8, 6.4, -5.8],
    axis: false,
    showNavigation: false,
    showCopyright: false,
    keepaspectratio: true,
    pan: { enabled: false },
    zoom: { enabled: false },
    backgroundColor: 'none',
  } as never)

  const O = board.create('point', [0, 0], {
    name: 'F_2',
    fixed: true,
    size: 3,
    strokeColor: INK,
    fillColor: INK,
    highlight: false,
    label: { offset: [-4, 16], strokeColor: INK },
  })

  const F1 = board.create('point', [F1X, 0], {
    name: 'F_1',
    fixed: true,
    size: 3,
    strokeColor: ACCENT,
    fillColor: ACCENT,
    highlight: false,
    label: { offset: [-24, -18], strokeColor: ACCENT },
  })

  const C = board.create('point', [0, R], { visible: false, fixed: true })
  const circle = board.create('circle', [O, C], {
    strokeColor: INK,
    strokeWidth: 1.3,
    fillOpacity: 0,
    highlight: false,
  })

  const startAngle = mode === 'trace' ? 120 : 50
  const P = board.create(
    'glider',
    [R * Math.cos((startAngle * Math.PI) / 180), R * Math.sin((startAngle * Math.PI) / 180), circle],
    {
      name: 'P',
      size: 3,
      strokeColor: GOLD,
      fillColor: GOLD,
      label: { offset: [10, 6], strokeColor: GOLD },
    },
  )

  renderLabel(O, 'F_2')
  renderLabel(F1, 'F_1', ACCENT)
  renderLabel(P, 'P', GOLD)

  // PF₁ 用虚线牵着，折痕才看得出是谁的垂直平分线
  board.create('segment', [P, F1], {
    strokeColor: INK,
    strokeWidth: 1,
    dash: 2,
    strokeOpacity: 0.5,
    highlight: false,
  })

  // trace 模式只要一道折痕，用函数点让它跟着 P 走
  if (mode === 'trace') {
    const A = board.create(
      'point',
      [
        () => creaseChord(P.X(), P.Y())?.[0] ?? 0,
        () => creaseChord(P.X(), P.Y())?.[1] ?? 0,
      ],
      { visible: false, fixed: true },
    )
    const B = board.create(
      'point',
      [
        () => creaseChord(P.X(), P.Y())?.[2] ?? 0,
        () => creaseChord(P.X(), P.Y())?.[3] ?? 0,
      ],
      { visible: false, fixed: true },
    )
    board.create('segment', [A, B], {
      strokeColor: GOLD,
      strokeWidth: 1.4,
      strokeOpacity: 0.9,
      highlight: false,
    })
  }

  const creases: any[] = []
  let shown: any[] = []
  let lastAngle = -99
  let running = false
  let raf = 0
  let envelope: any = null

  const angleOf = (): number => Math.atan2(P.Y(), P.X())

  function addCrease(): void {
    if (mode === 'trace') return
    const ch = creaseChord(P.X(), P.Y())
    if (!ch) return
    const seg = board.create('segment', [[ch[0], ch[1]], [ch[2], ch[3]]], {
      strokeColor: GOLD,
      strokeWidth: mode === 'crease' ? 1.05 : 1.25,
      strokeOpacity: mode === 'crease' ? 0.62 : 0.85,
      fixed: true,
      highlight: false,
    })
    creases.push(seg)
    if (creases.length > 34 && !envelope) {
      const a = 2.5
      const b = 1.5
      const cx = (F1X + 0) / 2
      envelope = board.create(
        'curve',
        [
          (t: number) => cx + a * Math.cos(t),
          (t: number) => b * Math.sin(t),
          0,
          2 * Math.PI,
        ],
        { strokeColor: ACCENT, strokeWidth: 1, dash: 3, strokeOpacity: 0.5, highlight: false },
      )
    }
  }

  // 第四帧：折痕与 PF₂ 的交点 M，M 满足 |MF₁| = |MP|，所以 |MF₁| + |MF₂| = |PF₂| = R
  let M: any = null
  let trail: any[] = []
  let lastTrail = -99

  if (mode === 'trace') {
    board.create('segment', [P, O], {
      strokeColor: INK,
      strokeWidth: 1,
      strokeOpacity: 0.45,
      highlight: false,
    })
    M = board.create('point', [0, 0], {
      name: 'M',
      size: 3,
      strokeColor: ACCENT,
      fillColor: ACCENT,
      fixed: true,
      highlight: false,
      label: { offset: [10, -14], strokeColor: ACCENT },
    })
    renderLabel(M, 'M', ACCENT)
    // M 到 F₁ 也画出来，定义里的两段和才算数
    board.create('segment', [M, F1], {
      strokeColor: INK,
      strokeWidth: 1,
      highlight: false,
    })
  }

  function updateM(): void {
    if (!M) return
    const ch = creaseChord(P.X(), P.Y())
    if (!ch) return
    // 折痕与直线 PF₂ 的交点：折痕法向 n 过中点 mid
    const px = P.X()
    const py = P.Y()
    const nx = px - F1X
    const ny = py
    const midx = (px + F1X) / 2
    const midy = py / 2
    // PF₂ 的参数式 Q = P + t(O - P)
    const dx = -px
    const dy = -py
    const den = nx * dx + ny * dy
    if (Math.abs(den) < 1e-9) return
    const t = (nx * (midx - px) + ny * (midy - py)) / den
    const mx = px + t * dx
    const my = py + t * dy
    M.setPosition(JXG.COORDS_BY_USER, [mx, my])
    const mf1 = Math.hypot(mx - F1X, my)
    const mf2 = Math.hypot(mx, my)
    if (readout) readout.textContent = `${mf1.toFixed(2)} + ${mf2.toFixed(2)} = ${(mf1 + mf2).toFixed(2)}`
    const ang = angleOf()
    if (Math.abs(ang - lastTrail) > 0.05) {
      lastTrail = ang
      trail.push(
        board.create('point', [mx, my], {
          size: 1.1,
          strokeColor: ACCENT,
          fillColor: ACCENT,
          fixed: true,
          withLabel: false,
          highlight: false,
        }),
      )
    }
  }

  function step(): void {
    if (!running) return
    const a = angleOf() + 0.016
    P.moveTo([R * Math.cos(a), R * Math.sin(a)])
    afterMove()
    raf = requestAnimationFrame(step)
  }

  function afterMove(): void {
    const a = angleOf()
    if (Math.abs(a - lastAngle) > 0.05) {
      lastAngle = a
      addCrease()
      if (mode === 'trace') updateM()
    }
    board.update()
  }

  P.on('drag', () => {
    stop()
    afterMove()
  })

  function stop(): void {
    running = false
    cancelAnimationFrame(raf)
    playBtn?.classList.remove('on')
    if (playBtn) playBtn.textContent = '自动演示'
  }

  function start(): void {
    if (running) return
    running = true
    playBtn?.classList.add('on')
    if (playBtn) playBtn.textContent = '暂停'
    step()
  }

  playBtn?.addEventListener('click', () => (running ? stop() : start()))

  clearBtn?.addEventListener('click', () => {
    creases.forEach((o) => board.removeObject(o))
    creases.length = 0
    shown = []
    trail.forEach((o) => board.removeObject(o))
    trail = []
    if (envelope) {
      board.removeObject(envelope)
      envelope = null
    }
    lastAngle = -99
    lastTrail = -99
  })

  // 默认不自动演示：进帧只摆好圆圈和 P，等老师点按钮或直接拖

  if (mode === 'trace') {
    updateM()
    board.update()
  }
}
