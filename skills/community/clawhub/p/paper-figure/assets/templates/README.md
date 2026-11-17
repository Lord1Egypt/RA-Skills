# assets/templates —— 可复用的 SVG 片段

这些片段是给「想手改 SVG / 想接自己管线」的人用的参考件，渲染核心本身**不依赖**它们
（`scripts/render.mjs` 与 `scripts/chart.mjs` 直接按 mm 坐标算，不读模板）。

## 约定（跟渲染核心一致，别改）

- **1 用户单位 = 1mm**，根节点 `viewBox="0 0 W H"`，同时给 `width="Wmm" height="Hmm"`；
  导出链路靠 width/height 算物理尺寸，只给 viewBox 会导错大小。
- **字号以 pt 声明**，落盘换算 `×0.3528`（1pt = 25.4/72 mm）。
  例：7pt → `font-size="2.4696"`，同时写 `data-font-pt="7"`。
- **语义属性**（`scripts/check.mjs` 靠它们做字号/溢出校验）：
  - 节点：`<g data-node-id="n1" data-kind="box|rounded|db|note|circle">`
  - 文字：`data-role="node-label|node-sub|edge-label|panel-title|panel-letter|axis-label|legend-label|caption"`
  - 每个 `<text>` 都带 `data-font-pt`
- 线宽：轴线 0.6pt、节点边 0.75pt、细线 0.5pt（换算成 mm 见 `scripts/lib/svg.mjs` 的 `SW`）。
- 箭头用 `markerUnits="strokeWidth"`，大小随线宽缩放；线端点回缩 0.9mm，别插进框里。

## 片段清单

| 文件 | 用途 |
|---|---|
| `node-rounded.svg` | 圆角节点（含主标签 + 子标签）的完整画法 |
| `arrow-marker.svg` | 箭头 marker 定义 + 一条带箭头的连接线 |
| `panel-band.svg` | 面板标题（(a) 粗体 + 标题 + 副标题）的画法 |
| `group-box.svg` | 虚线分组框（architecture 图里圈一组节点） |
| `line-marker.svg` | 折线图数据点 + 误差棒的最小例子 |

## 怎么用

1. 直接拷某个片段里的图形元素，改 `x/y/w/h` 与文字；
2. 或者把这几个文件当「合法输出」的样板，对照着写自己的生成器；
3. 生成的 SVG 丢回 `node scripts/fig.mjs check <工作区>` 就能看合规问题（记得把文件放进 `out/`）。

> 注意：片段里的占位色取自 `assets/palettes.json` 的 okabe-ito；
> 换成别的色板时，节点底色请用 `tint(color, 0.9)` 这种「同色系浅底 + 实色描边」的配法，
> 不要用一个饱和色铺满大色块。
