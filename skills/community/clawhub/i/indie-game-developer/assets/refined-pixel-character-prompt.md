# 精致手绘像素角色提示词模板

把尖括号字段替换为当前任务值；没有输入图时删除 `Reference images`。

```text
Use case: stylized-concept
Asset type: <square character icon / full-body sprite / portrait>

Reference images:
- Image 1 is a pixel-density and craftsmanship reference only. Follow its <logical grid, cluster size, contour, palette relationship>. Do not copy its <character, costume, pose, props, logo, background, grid overlay>.
- Image 2 is the character design reference. Preserve <identity-neutral traits, palette, equipment, action>. Do not inherit <background, rendering artifacts>.

Create exactly ONE original <character> as authentic hand-authored pixel art.
The artwork must look manually constructed on an apparent <28x36> logical character grid and enlarged only with nearest-neighbor scaling.

Pixel construction:
- uniform square logical pixels
- hard 1-cell near-black contour
- staircase diagonals, no smooth curves
- <12-16> total colors
- compact continuous color clusters, no isolated noise
- base, shadow and selective highlight per material
- single-pixel highlights only on <visual focal points>

Character:
- full body <pose and facing direction>
- <skin, hair, clothing, equipment>
- <weapon/prop> must remain clearly readable
- preserve negative space between <hands, weapon, body>
- <brand motif expressed in a few pixels>

Composition:
- strict square 1:1 canvas
- character centered at <65-78%> canvas height
- complete head, boots, weapon and accessories visible
- <12-18%> blank margin around the full silhouette

Background:
- perfectly flat solid pure white #FFFFFF edge to edge

Constraints:
- one character only
- original design; do not copy a referenced character or costume
- no visible grid lines or guide lines
- no floor, platform, pedestal, ground line, cast shadow or reflection
- no border, frame, particles, scenery, text, letters, logo or watermark
- no antialiasing, gradients, blur, glow, painterly texture, vector rendering, 3D or smooth anime illustration

Filename intent: <series>-<character>-<action>-refined-pixel.png
```

## 单变量纠偏追加句

人物过粗：

```text
Change only the logical character density from <16x16> to <28x36>. Preserve identity, pose, palette, silhouette, canvas and background.
```

人物太高清：

```text
Change only pixel construction: merge micro-details into larger color clusters, cap each material at base/shadow/highlight, and remove all sub-cell or antialiased edges.
```

白底不纯：

```text
Change only the background to uniform #FFFFFF. Remove every shadow, floor cue, gradient, reflection and off-white pixel; keep the character unchanged.
```

弓箭不清晰：

```text
Change only the weapon silhouette. Separate bow hand, draw hand, string, arrow and torso with readable negative space; keep character design and pixel density unchanged.
```
