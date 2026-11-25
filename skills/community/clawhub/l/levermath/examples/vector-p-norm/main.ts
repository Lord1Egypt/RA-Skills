import '../../src/styles/base.css'
import './styles/base.css'
import './fonts.css'
import { Deck } from '../../src/engine/deck'
import { mountInteractives, registerInteractive } from '../../src/engine/interactive'
import { mountMath } from '../../src/engine/math'
import { mountPNormLoop } from './interactive/norm'

import cover from './frames/01-cover.html?raw'
import space from './frames/02-space.html?raw'
import inner from './frames/03-inner.html?raw'
import normed from './frames/04-normed.html?raw'
import relation from './frames/05-relation.html?raw'
import pnorm from './frames/06-pnorm.html?raw'
import calc from './frames/07-calc.html?raw'
import loop from './frames/08-loop.html?raw'
import equiv from './frames/09-equiv.html?raw'
import summary from './frames/10-summary.html?raw'

registerInteractive('pnorm-loop', mountPNormLoop)

new Deck(document.getElementById('app') as HTMLElement).mount([
  { id: 'cover', name: '封面', html: cover },
  { id: 'space', name: '向量空间（线性空间）', html: space },
  { id: 'inner', name: '内积空间', html: inner },
  { id: 'normed', name: '赋范线性空间', html: normed },
  { id: 'relation', name: '内积与范数', html: relation },
  { id: 'pnorm', name: 'p-范数', html: pnorm },
  { id: 'calc', name: '算一算', html: calc },
  { id: 'loop', name: '单位圆的形变', html: loop },
  { id: 'equiv', name: '范数等价', html: equiv },
  { id: 'summary', name: '总结', html: summary },
])

mountMath()
mountInteractives()
