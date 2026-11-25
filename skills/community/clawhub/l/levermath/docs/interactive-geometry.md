# 交互式几何图形

适用场景：幻灯片里需要一个能拖动点、实时看轨迹的几何构造，而不是一张死图。

## 三条路线

| 路线 | 何时用 | 交互 | 离线 | 体积 |
| --- | --- | --- | --- | --- |
| JSXGraph 重写 | 点、线、圆、垂直平分线、交点、轨迹 | 可拖 | 是 | 约 1 MB |
| GeoGebra API + `ggbBase64` | 复杂构造、CAS、脚本、多视图 | 完整 | 否，依赖远程 App 包 | 运行时十几 MB |
| 静态导出 SVG | 只要一张示意图 | 无 | 是 | 几 KB |

默认走 JSXGraph。原因：能进单文件、离线、体积可控；GeoGebra 的交互更全，但会把“拷走就能播”破坏掉。

## 从 ggb 到 JSXGraph

`.ggb` 是源文件，不是发布物。课程专属的几何源随对应示例或课件保存，不进入通用引擎。流程：

1. 解包读 `geogebra.xml`，确认元素与构造顺序
   ```python
   import zipfile, re
   xml = zipfile.ZipFile("课件的 ggb 源.ggb").read("geogebra.xml").decode()
   ```
   关注 `<element type=...>` 的坐标与 `<command name=...>` 的输入输出
2. 在 `src/interactive/<name>.ts` 用同一组参数重写
3. 帧里放容器 `<div class="fig" data-interactive="<name>"></div>`
4. `src/main.ts` 里 `registerInteractive('<name>', mount<Name>)`

挂载由 `src/engine/interactive.ts` 统一扫描 `[data-interactive]`，用 `data-mounted` 防重复。

## 让 JSXGraph 看起来像 TikZ

- `renderer: 'svg'`，不要用默认 canvas，canvas 缩放会糊
- SVG 输出的文字通常不是可以直接承载 HTML 的容器；JSXGraph 的点标签是 HTML `div`，需要用 `katex.render` 接管。
- 颜色直接取模板的十六进制，与 TikZ 图同一套
- 线宽 1 到 1.6，虚线 `dash: 2` 或 `3`
- 点 `size: 2.5` 到 `3`，不开阴影
- 标签不要写下标 Unicode，如 `F₁` 的 `₁` 不在 Latin Modern 子集里，会回退宋体；Latin Modern 本身也没有 U+2080–2082，改用 KaTeX，写 `F_1`
- 背景 `backgroundColor: 'none'`，让舞台底色透出来
- `showNavigation: false`，隐藏缩放按钮

## 公式与标签

JSXGraph 的标签是 HTML div，默认 Arial，不会自动斜体、不会排下标。用 KaTeX 接管：

```ts
import katex from 'katex'
import 'katex/dist/katex.min.css'

function renderLabel(obj: any, tex: string): void {
  const node = obj?.label?.rendNode
  if (node) katex.render(tex, node, { throwOnError: false, output: 'html' })
}

renderLabel(P, 'P')
renderLabel(F1, 'F_1')
```

- `output: 'html'` 只输出 HTML，不生成隐藏的 MathML 副本
- 不要用 `.JXGtext { font-family: ... !important }` 覆盖字体，会把 KaTeX 的斜体与字体一起压掉
- `perpendicular` 自动生成的辅助点标签是 `visibility:hidden`，不用管；若出现可见的 A、B，改用中点加法向点自己连一条 `line`
- 正文公式同理，`katex.render` 一条即可；公式极多、要求严格 Latin Modern 字形时，改用 MathJax 预渲染 SVG

## 与 morph 的配合

挂载后不要自己起动画循环，也不要在 `frameenter` 里播放，进帧只摆静态起始状态，详见 [默认不自动播放](no-autoplay.md)。


帧切换时容器会做 transform 缩放，SVG 渲染器缩放后仍然清晰，canvas 会发虚。交互组件在首次挂载时初始化一次，之后帧隐藏不影响状态。

## 验证

1. `bun run build`，看 dist 体积
2. 打开 dist，拖动动点，轨迹应实时更新
3. 断开网络再打开一次，确认交互仍然可用

## 折纸示例的参数

示例源见 [`examples/origami-ellipse/geometry/`](../examples/origami-ellipse/geometry/)：

| 对象 | 定义 |
| --- | --- |
| F2 | 圆心，原点 |
| F1 | 圆内定点，(-4, 0) |
| C | 圆上一点，(0, 5)，半径 5 |
| P | 圆上动点，glider |
| 折痕 | PF1 的垂直平分线 |
| Q | 折痕与 OP 的交点 |

Q 满足 `QO + QF1 = QO + QP = OP = 5`，轨迹是以 F2、F1 为焦点、长轴 5 的椭圆。半长轴 `a = 2.5`，半焦距 `c = 2`，半短轴 `b = 1.5`，中心在 `(-2, 0)`。
