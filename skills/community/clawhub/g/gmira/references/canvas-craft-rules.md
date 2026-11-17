## 4. Canvas craft rules extracted from the codebase

These are the rules every one of the 25 engines follows. They are the actual value of this repo for a skill library.

### 4.1 DPR and retina handling

**Rule: clamp DPR at 2, always, no exceptions.** Every single engine has this line. A 3x phone display would otherwise triple fragment cost for no visible gain.

```ts
const dpr = Math.min(window.devicePixelRatio || 1, 2);
const width  = Math.max(1, Math.round(output.clientWidth  * dpr));
const height = Math.max(1, Math.round(output.clientHeight * dpr));
if (output.width !== width || output.height !== height) {
  output.width = width;
  output.height = height;
}
```

**Rule: guard the write.** `if (output.width !== width)` matters because assigning to `canvas.width` clears the backing store and resets all GL state on some drivers, even when the value is unchanged.

**Rule: derive DPR back from the canvas at render time, do not re-read `devicePixelRatio`.** This keeps uniforms consistent with whatever size the canvas actually is, including during a resize race:

```ts
const dpr = output.width / Math.max(output.clientWidth, 1);
```

**Rule: every CSS-pixel option is multiplied by DPR at the uniform boundary, never inside the shader.** The shader works in device pixels; the API works in CSS pixels.

```ts
gl.uniform1f(uniforms.uTile,    Math.max(config.tileSize, 24) * dpr);
gl.uniform1f(uniforms.uLift,    Math.max(config.lift, 0)      * dpr);
gl.uniform1f(uniforms.uScatter, Math.max(config.scatter, 0)   * dpr);
gl.uniform1f(uniforms.uPersp,   Math.max(config.perspective, 200) * dpr);
```

**Rule: the source canvas stays at CSS resolution, only the output canvas is DPR-scaled.** `drawElementImage` rasterizes at CSS pixel scale, so upscaling the source buys nothing:

```ts
const cssWidth  = Math.max(1, Math.round(source.clientWidth));
const cssHeight = Math.max(1, Math.round(source.clientHeight));
if (source.width !== cssWidth || source.height !== cssHeight) {
  source.width = cssWidth;
  source.height = cssHeight;
}
```

### 4.2 Resize strategy

**Rule: `ResizeObserver`, never a `window.resize` listener.** Window resize misses container-driven layout changes (sidebars, accordions, font loading). Observe both the output canvas and the content element:

```ts
const observer = new ResizeObserver(() => {
  syncCanvasSize();
  start();
});
observer.observe(output);
observer.observe(content);
```

**Rule: track content width separately from canvas width.** When the content is narrower than the canvas (scrollbar gutters, max-width containers), sampling past its edge gives garbage. Every engine passes a `uMaxX` uniform and clamps or discards beyond it:

```ts
contentMaxX = Math.min(1, Math.max(0.05, content.clientWidth / Math.max(output.clientWidth, 1)));
```
```glsl
if (uv.x > uMaxX) { outColor = vec4(0.0); return; }
// and inside every sampler:
p.x = clamp(p.x, 0.0005, uMaxX - 0.0005);
p.y = clamp(p.y, 0.0005, 0.9995);
```

The `0.0005` inset is deliberate: it prevents `CLAMP_TO_EDGE` from smearing edge texels when a displaced sample lands exactly on the boundary.

**Rule: resize triggers a repaint request, not just a canvas resize.** Otherwise the texture is stale at the new size for one frame:

```ts
if (htmlInCanvas) { /* ...resize source... */ paintable.requestPaint!(); }
```

**Rule: expose an imperative `resize()` on the instance** for cases the observer cannot see (manual transforms, canvas moved in the DOM).

### 4.3 RAF lifecycle and cleanup

This is the most transferable pattern in the repo. **The loop is not a loop, it is a state machine that stops.**

```ts
let raf = 0;
let lastTime = performance.now();
let destroyed = false;
let running = false;
let visible = true;

function frame(now: number) {
  if (destroyed) return;
  if (!visible) { running = false; return; }        // off-screen: stop, do not schedule

  const delta = Math.min((now - lastTime) / 1000, 1 / 30);   // hard clamp
  lastTime = now;

  // ... integrate state, render ...

  if (settled && !contentDirty) {
    // snap to exact targets so float drift never accumulates
    pointer.x = pointer.tx;
    pointer.y = pointer.ty;
    running = false;                                 // stop
    return;
  }
  raf = requestAnimationFrame(frame);
}

function start() {
  if (destroyed || running || !visible) return;      // idempotent, re-entrant safe
  running = true;
  lastTime = performance.now();                      // reset the clock, no catch-up jump
  raf = requestAnimationFrame(frame);
}
```

Rules encoded here:

1. **`start()` is idempotent.** Every event handler, observer callback and `setOptions` call ends in `start()`. Calling it 50 times in one tick schedules one frame.
2. **`lastTime = performance.now()` on every start.** Without this, a loop resuming after 10 seconds off-screen integrates a 10-second delta and the effect explodes.
3. **Delta is clamped to `1/30` (Cloth uses `1/20`).** A stalled tab must not produce a giant physics step.
4. **Snap on settle.** Before stopping, exponential easing is replaced with exact assignment, so the state is bit-exact and the next `start()` does not immediately re-detect motion.
5. **`contentDirty` keeps the loop alive.** When the DOM repaints, the texture must be re-uploaded even if nothing else moved.

**The wake pattern.** `onpaint` fires before `start` exists in scope, so a forward-declared closure is used:

```ts
let wake = () => {};
if (htmlInCanvas) {
  paintable.onpaint = () => {
    try {
      sourceCtx!.reset();
      sourceCtx!.drawElementImage!(content, 0, 0);
      contentDirty = true;
      wake();
    } catch {}
  };
}
// ...much later...
wake = start;
start();
```

Note the bare `catch {}`. `drawElementImage` can throw on cross-origin content or during teardown, and an exception inside `onpaint` would break the browser's paint loop.

**Destroy is exhaustive and ordered.** Every engine's `destroy()` follows the same order: flag, cancel RAF, disconnect observers, remove listeners, restore mutated DOM, delete GPU objects, null `onpaint`.

```ts
destroy() {
  destroyed = true;
  cancelAnimationFrame(raf);
  observer.disconnect();
  intersection.disconnect();
  themeObserver.disconnect();
  schemeQuery.removeEventListener("change", onThemeShift);
  window.clearTimeout(themeTimer);
  motionQuery.removeEventListener("change", onMotionChange);
  listenTarget.removeEventListener("pointermove", onPointerMove);
  listenTarget.removeEventListener("pointerleave", onPointerLeave);
  content.style.pointerEvents = "";          // restore what we mutated
  if (under) under.style.visibility = "";
  gl.deleteTexture(contentTexture);
  gl.deleteProgram(program);
  gl.deleteShader(vertexShader);
  gl.deleteShader(fragmentShader);
  gl.deleteBuffer(quad);
  gl.deleteVertexArray(vao);
  if (htmlInCanvas) paintable.onpaint = null;
}
```

The three.js components add: `renderer.setAnimationLoop(null)`, `controls.dispose()`, a `disposeObject()` traversal that disposes geometry plus every `THREE.Texture` found on each material, `pmrem.dispose()`, `envTarget.dispose()`, `draco.dispose()`, `renderer.dispose()`, and a `loadToken += 1` so in-flight async loads discard themselves.

### 4.4 Offscreen culling

**Rule: `IntersectionObserver` stops the loop, it does not just skip the render.** Skipping a render still costs a RAF callback per frame per instance.

```ts
const intersection = new IntersectionObserver((entries) => {
  visible = entries[entries.length - 1]?.isIntersecting ?? true;
  if (visible) start();
});
intersection.observe(output);
```

`entries[entries.length - 1]` takes the most recent entry, because the callback can be batched with several stale entries. `?? true` fails open: if something is wrong, render rather than go blank.

The three.js components are the exception and the weakness: they use `renderer.setAnimationLoop` and only early-return inside the callback, so the RAF keeps ticking off-screen. If you lift those, add the stop.

**Rule: cull in screen space too.** Glass, Bubble and Magnify compute a bounding rect around the active region and `gl.scissor` to it, so a 120px lens on a 4K page rasterizes 120px worth of fragments.

### 4.5 prefers-reduced-motion

**Rule: query it once, listen for changes, and restart the loop on change.**

```ts
const motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
let reducedMotion = motionQuery.matches;
function onMotionChange() { reducedMotion = motionQuery.matches; start(); }
motionQuery.addEventListener("change", onMotionChange);
```

**Rule: reduced motion means the easing constant becomes 1, not that the effect disappears.** The lens still follows the cursor, it just teleports instead of gliding:

```ts
const ease = reducedMotion ? 1 : 1 - Math.exp(-delta * Math.max(config.followSpeed, 0.5));
```

Four distinct strategies appear, pick the one that matches your effect:

| Strategy | Component | Code |
|---|---|---|
| Snap easing to instant | RetroDither, Asciify, Shatter, Glass, Peel | `const k = reducedMotion ? 1 : 1 - Math.exp(-delta / tau);` |
| Kill the effect entirely | Glitch | `if (!reducedMotion) advanceTimeline(delta); else envelope = 0;` |
| Refuse new input | Liquid, Ripple | `function onPointerMove(e) { if (reducedMotion) return; ... }` and `splash()` early-returns |
| Passthrough uniform | ParticleReveal | `gl.uniform1f(uniforms.uCrisp, reducedMotion \|\| !htmlInCanvas ? 1 : 0);` plus a shader early-return |

**Rule: freeze the clock, do not just hide the motion.** Shatter gates its `time` accumulator so nothing drifts while reduced:

```ts
const floating = !reducedMotion && config.floatSpeed > 0.001 && /* ... */;
if (floating) { time += delta * config.floatSpeed; if (time >= TIME_WRAP) time -= TIME_WRAP; }
```

### 4.6 Pointer input normalization

**Rule: normalize against `getBoundingClientRect()`, not `offsetX`/`layerX`.** Those are inconsistent across browsers and wrong when the target is a child element.

```ts
function onPointerMove(event: PointerEvent) {
  const rect = output.getBoundingClientRect();
  pointer.tx = (event.clientX - rect.left) / Math.max(rect.width, 1);
  pointer.ty = 1 - (event.clientY - rect.top) / Math.max(rect.height, 1);   // flip to GL space
  pointer.target = 1;
  start();
}
```

**Rule: listen on `output.parentElement ?? output`, not on the canvas.** The output canvas is `pointer-events: none`, so it never receives events. The wrapper does.

```ts
const listenTarget = output.parentElement ?? output;
listenTarget.addEventListener("pointermove", onPointerMove);
listenTarget.addEventListener("pointerleave", onPointerLeave);
```

Components that need to know **which element** was hovered (Glass with its `targets` selector) listen on `content` instead, with `{ passive: true }`, so `event.target.closest(selector)` resolves to a real DOM node.

**Rule: separate raw target from eased value.** `{ x, y, tx, ty, active, target }` is the standard shape: `tx/ty` are set by the event, `x/y` are integrated in the frame loop.

**Rule: `active` is a 0..1 presence value, not a boolean.** Pointer enter and leave animate rather than pop:

```ts
const pointer = { x: 0.5, y: 0.5, tx: 0.5, ty: 0.5, active: 0, target: 0 };
// onPointerMove:  pointer.target = 1;
// onPointerLeave: pointer.target = 0;
// in frame():     pointer.active += (pointer.target - pointer.active) * ease;
```

**Rule: velocity requires a previous sample, and the first move must produce none.** Otherwise the first pointer event injects a huge impulse from the origin:

```ts
const previous = pointers.get(event.pointerId);
pointers.set(event.pointerId, { x: px, y: py });
if (!previous) return;
```

**Rule: multi-touch is a `Map` keyed by `pointerId`,** cleaned on both `pointerleave` and `pointercancel`.

**Rule: rate-limit continuous spawners by distance, not by time.**

```ts
if (Math.hypot(x - hoverX, y - hoverY) < 56) return;
```

**Rule: pointer speed is an exponential moving average with an explicit decay.** ParticleObject:

```ts
const dt = Math.max((now - lastPointerTime) / 1000, 1e-3);
pointerSpeed += (speed - pointerSpeed) * 0.35;
// every frame, independent of events:
pointerSpeed *= Math.exp(-3 * delta);
```

### 4.7 How they avoid layout thrash

1. **`getBoundingClientRect()` is called once per event, never per frame.** Frame loops read `output.clientWidth/clientHeight` (cheap, cached) or the already-known `output.width/height`.
2. **Nothing writes DOM layout in the render loop.** The only DOM writes anywhere are: Peel's `content.style.pointerEvents` (guarded by an equality check), Peel's `under.style.visibility` (once), Magnify's readout `<div>` (position + textContent, both non-layout-invalidating for an absolutely positioned element), and Cloth's one-time inline canvas expansion at construction.
3. **The DOM to texture path is the browser's own paint, not `html2canvas`.** `onpaint` fires *after* layout, so reading the DOM there is free.
4. **Background sampling walks `parentElement` once, at construction and on theme change**, never per frame, and writes the result to a 1x1 canvas rather than parsing CSS colour strings:

```ts
let el: Element | null = content;
while (el) {
  const bg = getComputedStyle(el).backgroundColor;
  if (bg && bg !== "transparent") {
    probeCtx.clearRect(0, 0, 1, 1);
    probeCtx.fillStyle = bg;
    probeCtx.fillRect(0, 0, 1, 1);
    const [r, g, b, a] = probeCtx.getImageData(0, 0, 1, 1).data;
    if (a > 0) { backingRgb = [r / 255, g / 255, b / 255]; break; }
  }
  el = el.parentElement;
}
```

5. **`setOptions` mutates a config object in place and calls `start()`.** No re-instantiation, no shader recompile, no buffer reallocation. Only Frost's `quality` and Liquid's resolutions are exempt, and Liquid explicitly discards them.
6. **Uniform locations are cached at link time by introspection**, so no `getUniformLocation` in the frame loop:

```ts
const count = gl.getProgramParameter(program, gl.ACTIVE_UNIFORMS);
for (let i = 0; i < count; i++) {
  const info = gl.getActiveUniform(program, i)!;
  uniforms[info.name] = gl.getUniformLocation(program, info.name)!;
}
```

### 4.8 How they degrade

Four layers of fallback, in order:

1. **No `document`** (SSR): `supportsHtmlInCanvas()` returns `false` immediately.
2. **No WebGL2**: `createXxx()` returns `null`. The React wrapper detects this and flips to plain DOM:

```tsx
instanceRef.current = createLiquid({ source, content, output }, initialOptions);
if (native && !instanceRef.current) setFailed(true);
```

3. **No html-in-canvas**: `htmlInCanvas` is `false`, the content texture stays 1x1 transparent, `uHasContent` is 0, and the shader takes a standalone overlay branch. Liquid draws a pure fluid, Glass draws a rim-lit lens outline, Ripple draws glints only.
4. **`prefers-reduced-motion`**: as above.

The React wrapper renders children in **one of two positions** depending on support, and hydration-safe:

```tsx
const supported = useSyncExternalStore(emptySubscribe, supportsHtmlInCanvas, () => false);
const native = supported && !failed;
// ...
<canvas ref={sourceRef} layoutsubtree="true" suppressHydrationWarning
  style={native ? { position:"absolute", inset:0, width:"100%", height:"100%" }
                : { display:"none" }}>
  {native ? <div ref={contentRef} style={{...}}>{children}</div> : null}
</canvas>
{!native ? <div ref={contentRef} style={{...}}>{children}</div> : null}
<canvas ref={outputRef} aria-hidden style={{ position:"absolute", inset:0, pointerEvents:"none" }} />
```

Three details worth copying: `useSyncExternalStore` with a server snapshot of `false` (so SSR always renders the non-native tree and hydration matches), `suppressHydrationWarning` on the canvas, and `aria-hidden` on the output canvas so screen readers never see the decorative layer.

---

## 5. Reusable primitives

Lift these verbatim into a skill library.
