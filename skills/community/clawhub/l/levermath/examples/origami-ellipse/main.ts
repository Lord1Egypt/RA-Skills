import '../../src/styles/base.css'
import '../../src/themes/paper.css'
import './fonts.css'
import { Deck } from '../../src/engine/deck'
import { mountInteractives, registerInteractive } from '../../src/engine/interactive'
import { mountMath } from '../../src/engine/math'
import { revealAll } from '../../src/engine/enter'
import { mountOrigami } from './interactive/crease'

import figDef from './figures/def.svg?raw'
import figAxes from './figures/axes.svg?raw'
import figExpr from './figures/expr.svg?raw'
import figB from './figures/b.svg?raw'
import figY from './figures/y.svg?raw'
import figOutside from './figures/outside.svg?raw'
import figFlow from './figures/origami-flow.svg?raw'
import photo from './assets/origami.jpg'

import f01 from './frames/01-cover.html?raw'
import f02 from './frames/02-fold.html?raw'
import f03 from './frames/03-crease.html?raw'
import f04 from './frames/04-trace.html?raw'
import f05 from './frames/05-def.html?raw'
import f06 from './frames/06-axis.html?raw'
import f07 from './frames/07-equation.html?raw'
import f08 from './frames/08-simplify.html?raw'
import f09 from './frames/09-b.html?raw'
import f10 from './frames/10-yaxis.html?raw'
import f11 from './frames/11-compare.html?raw'
import f12 from './frames/12-outside.html?raw'
import f13 from './frames/13-thanks.html?raw'

const FIGS: Record<string, string> = {
  def: figDef,
  axes: figAxes,
  expr: figExpr,
  b: figB,
  y: figY,
  outside: figOutside,
  flow: figFlow,
}

// 帧里写 <!--fig:axes-->，构建时把 SVG 原样塞进去
const fill = (html: string): string =>
  html
    .replace(/<!--fig:(\w+)-->/g, (_, k: string) => FIGS[k] ?? '')
    .replace(/<!--photo-->/g, `<img class="photo-img" src="${photo}" alt="折纸作品">`)

registerInteractive('crease', (el) => mountOrigami(el, 'crease'))
registerInteractive('trace', (el) => mountOrigami(el, 'trace'))

new Deck(document.getElementById('app') as HTMLElement).mount([
  { id: 'cover', name: '封面', html: fill(f01) },
  { id: 'fold', name: '折纸四步', html: fill(f02) },
  { id: 'crease', name: '折痕的包络', html: fill(f03) },
  { id: 'trace', name: '交点描出椭圆', html: fill(f04) },
  { id: 'def', name: '椭圆的定义', html: fill(f05) },
  { id: 'axis', name: '建立坐标系', html: fill(f06) },
  { id: 'equation', name: '列出方程', html: fill(f07) },
  { id: 'simplify', name: '化简', html: fill(f08) },
  { id: 'b', name: 'b 的引入', html: fill(f09) },
  { id: 'yaxis', name: '焦点在 y 轴', html: fill(f10) },
  { id: 'compare', name: '两种标准方程', html: fill(f11) },
  { id: 'outside', name: '圆外取点', html: fill(f12) },
  { id: 'thanks', name: '谢谢', html: fill(f13) },
])

mountMath()
mountInteractives()

// 出图用：?frame=3 只显示第 3 帧，整帧铺满 1280×720，便于无头浏览器截屏
const shotParam = new URLSearchParams(location.search).get('frame')
if (shotParam) {
  const idx = Math.max(0, Math.min(12, Number(shotParam) - 1))
  const root = document.getElementById('app')!
  root.classList.add('shot')
  // 缩略图里也有 .frame 的克隆，必须限定在舞台里取
  const frames = Array.from(root.querySelectorAll<HTMLElement>('.stage > .frame'))
  frames.forEach((f, i) => {
    f.style.display = i === idx ? 'block' : 'none'
  })
  const stage = root.querySelector<HTMLElement>('.stage')!
  stage.style.width = '1280px'
  stage.style.height = '720px'
  stage.style.transform = 'none'
  // 截图要看到完整一页，把后续步骤也放出来
  if (frames[idx]) revealAll(frames[idx])
  frames[idx]?.dispatchEvent(new CustomEvent('frameenter', { bubbles: true }))
  // 出图时手动替老师点一下自动演示，否则截到的是空圆
  frames[idx]?.querySelector<HTMLButtonElement>('[data-act="play"]')?.click()
}
