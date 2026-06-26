# EXAMPLES.md — Compact Implementation Patterns

## 1. Pretext layout and line extraction

```ts
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext'

const prepared = prepareWithSegments(text, {
  font: '700 64px "Space Mono"',
})

const result = layoutWithLines(prepared, maxWidth, lineHeight)

for (const line of result.lines) {
  // line.text, line.width, line.start, line.end, line.ranges, etc.
}
```

Use this when you need manual rendering, line-aware motion, or custom glyph bodies.

---

## 2. Streaming line walk for editorial/custom flow

```ts
import { prepareWithSegments, layoutNextLine } from '@chenglou/pretext'

const prepared = prepareWithSegments(text, { font: '400 20px Georgia' })
let cursor = 0
const lines = []

while (cursor < text.length) {
  const next = layoutNextLine(prepared, cursor, width, lineHeight)
  if (!next) break
  lines.push(next)
  cursor = next.end
}
```

Use this when building pagination, column flow, obstacle-aware editors, or DOM-free layout engines.

---

## 3. Glyph bodies with home positions

```ts
const glyphs = []

for (const glyph of laidOutGlyphs) {
  glyphs.push({
    char: glyph.char,
    homeX: glyph.x,
    homeY: glyph.y,
    x: glyph.x,
    y: glyph.y,
    vx: 0,
    vy: 0,
    rotation: 0,
    vr: 0,
    heat: 0,
  })
}
```

Every dynamic text system should preserve `homeX/homeY` separately from live positions.

---

## 4. Spring-back update

```ts
for (const g of glyphs) {
  const dx = g.homeX - g.x
  const dy = g.homeY - g.y

  g.vx += dx * 0.04
  g.vy += dy * 0.04

  g.vx *= 0.9
  g.vy *= 0.9

  g.x += g.vx
  g.y += g.vy
}
```

This is the minimum viable “tear apart and recover” behavior.

---

## 5. Local blast around cursor

```ts
function blast(cx: number, cy: number, radius: number, force: number) {
  for (const g of glyphs) {
    const dx = g.x - cx
    const dy = g.y - cy
    const d2 = dx * dx + dy * dy
    if (d2 > radius * radius) continue

    const d = Math.max(1, Math.sqrt(d2))
    const power = (1 - d / radius) * force

    g.vx += (dx / d) * power
    g.vy += (dy / d) * power
    g.heat = 1
  }
}
```

Use local force first. It feels better than instantly disturbing the entire composition.

---

## 6. Breaker word boxes from Pretext lines

```ts
const bricks = []

for (const line of result.lines) {
  let x = line.x
  for (const word of line.text.split(/(\s+)/)) {
    const width = measureWord(word)
    if (!word.trim()) {
      x += width
      continue
    }

    bricks.push({
      text: word,
      x,
      y: line.y,
      w: width,
      h: lineHeight,
      hp: 1,
      broken: false,
    })

    x += width
  }
}
```

Use this to build Breaker-style text-as-brick mechanics.

---

## 7. Canvas text rendering for hot paths

```ts
ctx.save()
ctx.font = '700 28px Space Mono'
ctx.textBaseline = 'top'

for (const g of glyphs) {
  ctx.save()
  ctx.translate(g.x, g.y)
  ctx.rotate(g.rotation)
  ctx.globalAlpha = 0.7 + g.heat * 0.3
  ctx.fillText(g.char, 0, 0)
  ctx.restore()
}

ctx.restore()
```

Canvas is often the right choice for text game loops.

---

## 8. Three.js particle morph targets

```js
const count = 2000
const positions = new Float32Array(count * 3)
const home = new Float32Array(count * 3)
const velocity = new Float32Array(count * 3)

geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
geometry.setAttribute('home', new THREE.BufferAttribute(home, 3))
geometry.setAttribute('velocity', new THREE.BufferAttribute(velocity, 3))
```

Keep dynamic arrays flat and update them in one render loop.

---

## 9. Cursor magnet for hero form

```js
for (let i = 0; i < count; i++) {
  const ix = i * 3
  const dx = mouse.x - pos[ix]
  const dy = mouse.y - pos[ix + 1]
  const distSq = dx * dx + dy * dy

  if (distSq < attractRadius * attractRadius) {
    const d = Math.max(0.001, Math.sqrt(distSq))
    const f = (1 - d / attractRadius) * attractForce
    vel[ix] += (dx / d) * f
    vel[ix + 1] += (dy / d) * f
  }

  vel[ix] += (home[ix] - pos[ix]) * spring
  vel[ix + 1] += (home[ix + 1] - pos[ix + 1]) * spring
}
```

This is the simplest way to make a formation feel alive while keeping it readable.

---

## 10. Textura-style block layout separation

```ts
type Block = {
  id: string
  width: number
  height: number
  lines: Line[]
  x: number
  y: number
}

function layoutBlocks(blocks: Block[], container: { width: number; height: number }) {
  // Hand off to Yoga/Textura-style layout logic here.
  // Keep this separate from glyph rendering and animation.
}
```

The key idea is not the exact engine. The key idea is separating **block layout** from **glyph rendering**.

---

## 11. Pinch-to-resize-text state

```ts
let textScale = 1

function setTextScale(next: number) {
  textScale = Math.min(1.8, Math.max(0.75, next))
  prepared = prepareWithSegments(text, {
    font: `${700 * textScale} 64px Space Mono`,
  })
  result = layoutWithLines(prepared, width, lineHeight * textScale)
}
```

Use this pattern to resize the text system itself on mobile instead of zooming the whole page.

---

## 12. Ambient side rail generator

```js
const symbols = ['◆','▓','▒','░','╬','║','│','·']

function makeRailLine(length = 24) {
  let s = ''
  for (let i = 0; i < length; i++) {
    s += symbols[(Math.random() * symbols.length) | 0]
  }
  return s
}
```

Animate offsets, alpha, and occasional glow instead of flooding the screen.

---

## 13. Reduced motion switch

```js
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

const config = {
  spring: reduceMotion ? 0.02 : 0.04,
  attractForce: reduceMotion ? 0.0 : 0.08,
  particleCount: reduceMotion ? 0 : 120,
}
```

Always tune density and force down for reduced motion.
