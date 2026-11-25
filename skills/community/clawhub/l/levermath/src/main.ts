import './styles/base.css'
import '../templates/basic/fonts.css'
import { Deck } from './engine/deck'
import { mountMath } from './engine/math'
import cover from '../templates/basic/frames/01-cover.html?raw'
import coverFig from './assets/figures/cover.svg?raw'
import structure from '../templates/basic/frames/02-structure.html?raw'
import steps from '../templates/basic/frames/03-steps.html?raw'
import translate from '../templates/basic/frames/04-translate.html?raw'

new Deck(document.getElementById('app') as HTMLElement).mount([
  { id: 'cover', name: '封面', html: cover.replace('<!--fig:cover-->', coverFig) },
  { id: 'structure', name: '第二帧', html: structure },
  { id: 'steps', name: '第三帧', html: steps },
  { id: 'translate', name: '帧内平移', html: translate },
])

mountMath()
