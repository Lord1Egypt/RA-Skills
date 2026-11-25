import JXG from 'jsxgraph'
import katex from 'katex'
import 'katex/dist/katex.min.css'

const INK = '#1b1b24'
const MUTED = '#8a8a95'
const BLUE = '#2b5fa8'
const NAVY = '#20206e'
const GOLD = '#b07d00'
const RED = '#b03a2e'
const GREEN = '#1e7a45'
const GRID = '#c9c9d4'

;(JXG.Options.text as any).fontFamily = 'Latin Modern Roman, Noto Serif SC'
;(JXG.Options.text as any).fontSize = 14

function renderLabel(obj: any, tex: string): void {
  const node: HTMLElement | undefined = obj?.label?.rendNode
  if (!node) return
  katex.render(tex, node, { throwOnError: false, displayMode: false, output: 'html' })
}

function renderText(obj: any, tex: string): void {
  const node: HTMLElement | undefined = obj?.rendNode
  if (!node) return
  obj.setText?.('')
  katex.render(tex, node, { throwOnError: false, displayMode: false, output: 'html' })
}

function normFactor(t: number, p: number): number {
  const c = Math.abs(Math.cos(t))
  const s = Math.abs(Math.sin(t))
  if (p >= 100) return Math.max(c, s)
  if (p > 50) {
    const rf = Math.pow(Math.pow(c, p) + Math.pow(s, p), 1 / p)
    const w = (p - 50) / 50
    return (1 - w) * rf + w * Math.max(c, s)
  }
  return Math.pow(Math.pow(c, p) + Math.pow(s, p), 1 / p)
}

function boardIn(el: HTMLElement, box: number[]): any {
  return JXG.JSXGraph.initBoard(el, {
    renderer: 'svg',
    boundingbox: box,
    axis: false,
    showNavigation: false,
    showCopyright: false,
    keepaspectratio: true,
    backgroundColor: 'none',
  } as never)
}

function playButton(el: HTMLElement): HTMLButtonElement | null {
  return (el.closest('.frame')?.querySelector('[data-act="play"]') as HTMLButtonElement | null) ?? null
}

// 三种 p-范数的单位球与同一向量的三种读数。
export function mountPNormThree(el: HTMLElement): void {
  const board = boardIn(el, [-3.5, 2, 3.5, -2])
  const centers = [
    [-2.2, 0.15],
    [0, 0.15],
    [2.2, 0.15],
  ]
  const ps = [1, 2, 100]
  const colors = [BLUE, GOLD, RED]
  const tags = ['p=1', 'p=2', 'p=\\infty']
  const values = ['1.4', '1.0', '0.8']
  const valuePos = [
    [-2.2 + 0.62, 0.88],
    [0.62, 0.88],
    [2.2 - 0.12, 0.84],
  ]

  centers.forEach((c, i) => {
    board.create(
      'curve',
      [
        (t: number) => c[0] + (0.9 * Math.cos(t)) / normFactor(t, ps[i]),
        (t: number) => c[1] + (0.9 * Math.sin(t)) / normFactor(t, ps[i]),
        0,
        2 * Math.PI,
      ],
      { strokeColor: colors[i], strokeWidth: 2 },
    )
    const tag = board.create('text', [c[0], c[1] - 1.12, ''], {
      fontSize: 18,
      strokeColor: colors[i],
      anchorX: 'middle',
      anchorY: 'middle',
    })
    renderText(tag, tags[i])

    board.create('arrow', [[c[0], c[1]], [c[0] + 0.54, c[1] + 0.72]], {
      strokeColor: GREEN,
      strokeWidth: 2,
    })
    const value = board.create('text', [valuePos[i][0], valuePos[i][1], ''], {
      fontSize: 18,
      strokeColor: GREEN,
      anchorX: 'left',
      anchorY: 'middle',
    })
    renderText(value, values[i])
  })
}

// p 从 1 到 100 再回到 1；滑块可拖，按钮自动演示。
export function mountPNormLoop(el: HTMLElement): void {
  const board = boardIn(el, [-4, 2.25, 4, -2.25])

  board.create('axis', [[0, 0], [1, 0]], {
    strokeColor: '#b9b9c6',
    strokeWidth: 1,
    ticks: { visible: false },
    labels: { visible: false },
  })
  board.create('axis', [[0, 0], [0, 1]], {
    strokeColor: '#b9b9c6',
    strokeWidth: 1,
    ticks: { visible: false },
    labels: { visible: false },
  })

  // 滑块位置 t∈[0,1]：1→5 占前 50%，5→15 占 20%，15→100 占后 30%。
  const pFromT = (t: number): number => {
    if (t <= 0.5) return 1 + 4 * (t / 0.5)
    if (t <= 0.7) return 5 + 10 * ((t - 0.5) / 0.2)
    return 15 + 85 * Math.pow((t - 0.7) / 0.3, 2)
  }
  const tFromP = (p: number): number => {
    if (p <= 5) return (0.5 * (p - 1)) / 4
    if (p <= 15) return 0.5 + (0.2 * (p - 5)) / 10
    return 0.7 + 0.3 * Math.sqrt((p - 15) / 85)
  }

  const slider = board.create('slider', [[-3.2, -1.92], [3.2, -1.92], [0, 0, 1]], {
    name: '',
    snapWidth: 0.001,
    strokeColor: NAVY,
    fillColor: NAVY,
    highlightStrokeColor: BLUE,
    highlightFillColor: BLUE,
    label: { visible: false },
  }) as any

  board.create(
    'curve',
    [
      (t: number) => (1.8 * Math.cos(t)) / normFactor(t, pFromT(slider.Value())),
      (t: number) => (1.8 * Math.sin(t)) / normFactor(t, pFromT(slider.Value())),
      0,
      2 * Math.PI,
    ],
    { strokeColor: GOLD, strokeWidth: 2.5 },
  )

  const readout = board.create('text', [2.55, 1.95, 'p=1.00'], {
    fontSize: 18,
    strokeColor: NAVY,
    anchorX: 'left',
    anchorY: 'middle',
  }) as any

  const syncReadout = (): void => {
    const p = pFromT(slider.Value())
    readout.setText(p >= 99.5 ? 'p=\u221e' : `p=${p.toFixed(2)}`)
  }
  slider.on('drag', syncReadout)
  syncReadout()

  const btn = playButton(el)
  const jumps = Array.from(
    el.closest('.frame')?.querySelectorAll<HTMLButtonElement>('.p-jump') ?? [],
  )
  let raf = 0
  let running = false
  let start = 0

  const tick = (now: number): void => {
    if (!running) return
    const phase = ((now - start) / 5000) % 2
    const t = phase < 1 ? phase : 2 - phase
    slider.setValue(t)
    board.update()
    syncReadout()
    raf = requestAnimationFrame(tick)
  }

  const stop = (): void => {
    running = false
    cancelAnimationFrame(raf)
    if (btn) btn.textContent = '自动演示'
  }

  btn?.addEventListener('click', () => {
    if (running) {
      stop()
      return
    }
    running = true
    start = performance.now()
    btn.textContent = '暂停'
    raf = requestAnimationFrame(tick)
  })

  jumps.forEach((jump) => {
    jump.addEventListener('click', () => {
      stop()
      const p = Number(jump.dataset.p ?? '1')
      slider.setValue(tFromP(p))
      board.update()
      syncReadout()
    })
  })

  el.addEventListener('pointerdown', () => {
    if (running) stop()
  })
}
