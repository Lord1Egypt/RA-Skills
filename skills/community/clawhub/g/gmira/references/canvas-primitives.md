## 5. Reusable primitives

Lift these verbatim into a skill library.

### 5.1 `supportsHtmlInCanvas()` + the capture bridge

```ts
type PaintableCanvas = HTMLCanvasElement & {
  onpaint?: (() => void) | null;
  requestPaint?: () => void;
};

type ElementImageContext = CanvasRenderingContext2D & {
  drawElementImage?: (element: Element, x: number, y: number) => void;
};

export function supportsHtmlInCanvas(): boolean {
  if (typeof document === "undefined") return false;
  const probe = document.createElement("canvas") as PaintableCanvas;
  const ctx = probe.getContext("2d") as ElementImageContext | null;
  return Boolean(
    ctx &&
    typeof ctx.drawElementImage === "function" &&
    typeof probe.requestPaint === "function",
  );
}

// wiring, inside the factory:
const sourceCtx = source.getContext("2d") as ElementImageContext | null;
const paintable = source as PaintableCanvas;
const htmlInCanvas = Boolean(
  sourceCtx &&
  typeof sourceCtx.drawElementImage === "function" &&
  typeof paintable.requestPaint === "function",
);

let contentDirty = false;
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
```

### 5.2 The self-stopping RAF state machine

```ts
let raf = 0;
let lastTime = performance.now();
let destroyed = false;
let running = false;
let visible = true;

function frame(now: number) {
  if (destroyed) return;
  if (!visible) { running = false; return; }
  const delta = Math.min(Math.max((now - lastTime) / 1000, 0), 1 / 30);
  lastTime = now;

  const k = reducedMotion ? 1 : 1 - Math.exp(-delta / tau);
  state.value += (state.target - state.value) * k;

  render();

  const settled = Math.abs(state.target - state.value) < EPSILON;
  if (settled && !contentDirty) {
    state.value = state.target;
    running = false;
    return;
  }
  raf = requestAnimationFrame(frame);
}

function start() {
  if (destroyed || running || !visible) return;
  running = true;
  lastTime = performance.now();
  raf = requestAnimationFrame(frame);
}

wake = start;
start();
```

### 5.3 Frame-rate independent exponential easing

The single most reused line in the library. Never use `value += (target - value) * 0.1`, which is frame-rate dependent.

```ts
// tau form: tau is the time constant in seconds, ~63% of the way there per tau
const k = 1 - Math.exp(-delta / Math.max(tau, 1e-4));

// rate form: higher is snappier
const ease = 1 - Math.exp(-delta * Math.max(rate, 0.5));

// per-frame decay constants (matching a "per 60fps frame" authoring value)
const dissipation = Math.pow(config.densityDissipation, delta * 60);
const decay = Math.exp(-dampingRate * delta);
const halfLife = Math.pow(0.5, delta / 0.7);
```

### 5.4 DPR-aware canvas sizing

```ts
let contentMaxX = 1;

function syncCanvasSize() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const width  = Math.max(1, Math.round(output.clientWidth  * dpr));
  const height = Math.max(1, Math.round(output.clientHeight * dpr));
  if (output.width !== width || output.height !== height) {
    output.width = width;
    output.height = height;
  }
  contentMaxX = Math.min(
    1,
    Math.max(0.05, content.clientWidth / Math.max(output.clientWidth, 1)),
  );
  if (htmlInCanvas) {
    const cssWidth  = Math.max(1, Math.round(source.clientWidth));
    const cssHeight = Math.max(1, Math.round(source.clientHeight));
    if (source.width !== cssWidth || source.height !== cssHeight) {
      source.width  = cssWidth;
      source.height = cssHeight;
    }
    paintable.requestPaint!();
  }
}

// at render time, derive DPR back from the canvas:
const dpr = output.width / Math.max(output.clientWidth, 1);
```

### 5.5 The observer trio

```ts
const motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
let reducedMotion = motionQuery.matches;
function onMotionChange() { reducedMotion = motionQuery.matches; start(); }
motionQuery.addEventListener("change", onMotionChange);

const observer = new ResizeObserver(() => { syncCanvasSize(); start(); });
observer.observe(output);
observer.observe(content);

const intersection = new IntersectionObserver((entries) => {
  visible = entries[entries.length - 1]?.isIntersecting ?? true;
  if (visible) start();
});
intersection.observe(output);
```

### 5.6 Theme-aware background sampling

```ts
let backingRgb: [number, number, number] = [1, 1, 1];
let backingLum = 1;
const probe = document.createElement("canvas");
probe.width = probe.height = 1;
const probeCtx = probe.getContext("2d", { willReadFrequently: true });

function syncBacking() {
  backingRgb = [1, 1, 1];
  if (probeCtx) {
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
  }
  backingLum = 0.299 * backingRgb[0] + 0.587 * backingRgb[1] + 0.114 * backingRgb[2];
}

let themeTimer = 0;
function onThemeShift() {
  syncBacking();
  start();
  window.clearTimeout(themeTimer);
  themeTimer = window.setTimeout(() => { syncBacking(); start(); }, 300);  // catch CSS transitions
}
const themeObserver = new MutationObserver(onThemeShift);
themeObserver.observe(document.documentElement, {
  attributes: true,
  attributeFilter: ["class", "style", "data-theme"],
});
const schemeQuery = window.matchMedia("(prefers-color-scheme: dark)");
schemeQuery.addEventListener("change", onThemeShift);
```

A standalone CSS colour parser, used when the option is a plain string rather than "auto":

```ts
let colorProbe: CanvasRenderingContext2D | null = null;

function parseColor(input: string): [number, number, number] {
  if (typeof document === "undefined") return [0, 0, 0];
  if (!colorProbe) {
    const probe = document.createElement("canvas");
    probe.width = 1;
    probe.height = 1;
    colorProbe = probe.getContext("2d", { willReadFrequently: true });
  }
  if (!colorProbe) return [0, 0, 0];
  colorProbe.fillStyle = "#000000";   // reset so an invalid input does not inherit
  colorProbe.fillStyle = input;
  colorProbe.clearRect(0, 0, 1, 1);
  colorProbe.fillRect(0, 0, 1, 1);
  const data = colorProbe.getImageData(0, 0, 1, 1).data;
  return [data[0] / 255, data[1] / 255, data[2] / 255];
}
```

### 5.7 WebGL boilerplate: compile, link, introspect uniforms, fullscreen quad

```ts
const gl = output.getContext("webgl2", {
  alpha: true,
  depth: false,
  stencil: false,
  antialias: false,
  premultipliedAlpha: true,
});
if (!gl || gl.isContextLost()) return null;

function compile(type: number, text: string): WebGLShader {
  const shader = gl!.createShader(type)!;
  gl!.shaderSource(shader, text);
  gl!.compileShader(shader);
  if (!gl!.getShaderParameter(shader, gl!.COMPILE_STATUS)) {
    console.error("shader error:", gl!.getShaderInfoLog(shader));
  }
  return shader;
}

function link(vertText: string, fragText: string) {
  const vert = compile(gl!.VERTEX_SHADER, vertText);
  const frag = compile(gl!.FRAGMENT_SHADER, fragText);
  const program = gl!.createProgram()!;
  gl!.attachShader(program, vert);
  gl!.attachShader(program, frag);
  gl!.linkProgram(program);
  const uniforms: Record<string, WebGLUniformLocation> = {};
  const count = gl!.getProgramParameter(program, gl!.ACTIVE_UNIFORMS);
  for (let i = 0; i < count; i++) {
    const info = gl!.getActiveUniform(program, i)!;
    uniforms[info.name.replace("[0]", "")] = gl!.getUniformLocation(program, info.name)!;
  }
  return { program, vert, frag, uniforms };
}

// fullscreen quad, no VAO needed if you only have one
const quad = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, quad);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
gl.enableVertexAttribArray(0);
gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
// draw with: gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
```

Standard vertex shader:

```glsl
#version 300 es
precision highp float;
layout(location = 0) in vec2 aPos;
out vec2 vUv;
void main () {
  vUv = aPos * 0.5 + 0.5;
  gl_Position = vec4(aPos, 0.0, 1.0);
}
```

Note the `info.name.replace("[0]", "")` in `link()`: WebGL reports array uniforms as `uRipples[0]`, so stripping the suffix lets you write `uniforms.uRipples`. Asciify keeps the suffix and indexes `uniforms["uGlyphs[0]"]`; pick one convention.

### 5.8 Content texture upload with flip and mipmaps

```ts
const contentTexture = gl.createTexture()!;
gl.bindTexture(gl.TEXTURE_2D, contentTexture);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);  // or LINEAR
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE,
  new Uint8Array([0, 0, 0, 0]));       // 1x1 transparent placeholder, valid before first paint
gl.generateMipmap(gl.TEXTURE_2D);

function uploadContent() {
  if (!htmlInCanvas || !contentDirty) return;
  contentDirty = false;
  gl.bindTexture(gl.TEXTURE_2D, contentTexture);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, source);
  gl.generateMipmap(gl.TEXTURE_2D);     // only if you need LOD blur
}
```

Shader-side sampler with the Y flip and the content-width guard:

```glsl
vec4 page (vec2 p) {
  p.x = clamp(p.x, 0.0005, uMaxX - 0.0005);
  p.y = clamp(p.y, 0.0005, 0.9995);
  return texture(uContent, vec2(p.x, 1.0 - p.y));
}
```

Derivative-aware minification (from Glass and Magnify), for anything that scales the page down:

```glsl
vec3 pageAA (vec2 px, float minLod) {
  float footprint = max(length(fwidth(px)), 1.0);
  return page(px, max(minLod, log2(footprint)));
}
```

### 5.9 Ping-pong double framebuffer

```ts
interface Target { fbo: WebGLFramebuffer; texture: WebGLTexture; width: number; height: number; }
interface DoubleTarget { read: Target; write: Target; swap: () => void; }

function createDoubleTarget(size, internalFormat, format, filter): DoubleTarget {
  let read  = createTarget(size, internalFormat, format, filter);
  let write = createTarget(size, internalFormat, format, filter);
  return {
    get read()  { return read; },
    get write() { return write; },
    swap() { const t = read; read = write; write = t; },
  };
}

function blit(target: Target | null) {
  if (target) {
    gl.bindFramebuffer(gl.FRAMEBUFFER, target.fbo);
    gl.viewport(0, 0, target.width, target.height);
  } else {
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    gl.viewport(0, 0, output.width, output.height);
  }
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
}

function bindTexture(texture: WebGLTexture, unit: number): number {
  gl.activeTexture(gl.TEXTURE0 + unit);
  gl.bindTexture(gl.TEXTURE_2D, texture);
  return unit;                          // returns the unit so it composes with uniform1i
}
```

Float texture capability probe:

```ts
gl.getExtension("EXT_color_buffer_float");
const supportsLinear = Boolean(gl.getExtension("OES_texture_float_linear"));
const filtering = supportsLinear ? gl.LINEAR : gl.NEAREST;
```

### 5.10 The pointer state object

```ts
const pointer = { x: 0.5, y: 0.5, tx: 0.5, ty: 0.5, active: 0, target: 0 };
const listenTarget = output.parentElement ?? output;

function onPointerMove(event: PointerEvent) {
  const rect = output.getBoundingClientRect();
  pointer.tx = (event.clientX - rect.left) / Math.max(rect.width, 1);
  pointer.ty = 1 - (event.clientY - rect.top) / Math.max(rect.height, 1);
  pointer.target = 1;
  start();
}
function onPointerLeave() { pointer.target = 0; start(); }

listenTarget.addEventListener("pointermove", onPointerMove);
listenTarget.addEventListener("pointerleave", onPointerLeave);
```

### 5.11 Hash functions (verbatim, all used in production here)

```glsl
// 1 float from vec2, best quality/cost tradeoff, from Dave Hoskins
float hash12 (vec2 p) {
  vec3 p3 = fract(vec3(p.xyx) * 0.1031);
  p3 += dot(p3, p3.yzx + 33.33);
  return fract((p3.x + p3.y) * p3.z);
}

// vec2 from vec2
vec2 hash22 (vec2 p) {
  vec3 q = fract(vec3(p.xyx) * vec3(0.1031, 0.1030, 0.0973));
  q += dot(q, q.yzx + 33.33);
  return fract((q.xx + q.yz) * q.zy);
}

// cheap classic, fine for non-critical jitter
float hash21 (vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

// interleaved gradient noise, ideal for temporal/spatial dithering
float ign (vec2 v) {
  return fract(52.9829189 * fract(0.06711056 * v.x + 0.00583715 * v.y));
}

// bayer 4x4 ordered dither threshold
float bayer (ivec2 p) {
  int b[16] = int[16](0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5);
  return (float(b[(p.y % 4) * 4 + (p.x % 4)]) + 0.5) / 16.0;
}

// exponential smooth-min: metaballs
float smoothMin (float d1, float d2, float k) {
  float h = exp(-k * d1) + exp(-k * d2);
  return -log(max(h, 1e-12)) / k;
}

// polynomial smooth-min: rounded SDF unions
float smin (float a, float b, float k) {
  float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
  return mix(b, a, h) - k * h * (1.0 - h);
}

// rounded box SDF
float sdf (vec2 p, vec2 half_, float corner) {
  vec2 q = abs(p) - (half_ - vec2(corner));
  return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - corner;
}
```

### 5.12 sRGB / linear conversion (do all blending in linear)

```glsl
vec3 toLinear (vec3 c) {
  return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(0.04045, c));
}
vec3 toSrgb (vec3 c) {
  return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(0.0031308, c));
}
```
```ts
function srgbToLinear(value: number): number {
  return value <= 0.04045 ? value / 12.92 : Math.pow((value + 0.055) / 1.055, 2.4);
}
```

The cheap approximation used by Glass and Magnify when exactness is not needed: `pow(texel, 2.2)` on read, `pow(color, 1.0/2.2)` on write.

### 5.13 The React wrapper (all 22 html-in-canvas components share it)

```tsx
"use client";
import { useEffect, useRef, useState, useSyncExternalStore, type ReactNode } from "react";
import { createLiquid, supportsHtmlInCanvas, type LiquidInstance, type LiquidOptions } from "./LiquidVanilla";

export interface LiquidProps extends LiquidOptions {
  children: ReactNode;
  className?: string;
  style?: React.CSSProperties;
}

const emptySubscribe = () => () => {};

export function Liquid({ children, className, style, ...options }: LiquidProps) {
  const sourceRef   = useRef<HTMLCanvasElement>(null);
  const contentRef  = useRef<HTMLDivElement>(null);
  const outputRef   = useRef<HTMLCanvasElement>(null);
  const instanceRef = useRef<LiquidInstance | null>(null);
  const [initialOptions] = useState(options);      // freeze construction-time options
  const [failed, setFailed] = useState(false);

  const supported = useSyncExternalStore(emptySubscribe, supportsHtmlInCanvas, () => false);
  const native = supported && !failed;

  useEffect(() => {
    const source = sourceRef.current, content = contentRef.current, output = outputRef.current;
    if (!source || !content || !output) return;
    instanceRef.current = createLiquid({ source, content, output }, initialOptions);
    if (native && !instanceRef.current) setFailed(true);
    return () => { instanceRef.current?.destroy(); instanceRef.current = null; };
  }, [initialOptions, native]);

  useEffect(() => { instanceRef.current?.setOptions(options); });   // no dep array: runs every render
  // ...JSX as shown in 4.8...
}
```

Two subtleties: `useState(options)` freezes the initial options so the construction effect does not re-run on every prop change, and the second effect has **no dependency array**, so live prop updates always reach `setOptions` without needing to enumerate 20 props.

### 5.14 Instance contract

Every engine returns the same shape. Keep this for any new component:

```ts
export interface XxxInstance {
  /** Update effect options live. */
  setOptions: (options: XxxOptions) => void;
  /** Re-read canvas size. Call when the element is resized. */
  resize: () => void;
  /** Stop the loop and release all GPU resources. */
  destroy: () => void;
  /** Optional: an imperative trigger, e.g. Glitch.burst(), Ripple.splash(x,y), Liquid.splat(...), Frost.melt(x,y) */
}
```

Options are always `Partial`, merged over a `Required<XxxOptions>` DEFAULTS object, with every property JSDoc'd including its unit and valid range. That JSDoc is what the docs site auto-generates the API table from, and it is what makes the components MCP-friendly.

---

## 6. Where each component fits a real commercial site
