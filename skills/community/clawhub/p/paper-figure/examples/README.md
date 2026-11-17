# examples —— 能直接跑通的样例

这堆文件不是摆设：`node scripts/fig.mjs init <dir>` 造出来的工作区，跟这里的内容一模一样。
想改自己的图，照着改 brief.md 或 figure.json 就行。

| 文件 | 是什么 | 怎么用 |
|---|---|---|
| `brief-example.md` | 人写的一段说明（标题/图注/面板/节点/边） | 当成工作区的 `brief.md`，跑 `spec` 就变成 figure.json |
| `spec-example.json` | 上面那份 brief 解析出来的 figure.json | 当工作区的 `figure.json`，直接跑 `render` / `chart` |
| `data-example.csv` | 示例数据：三种方法 × 两种指标 + 标准差列 | 放进工作区 `data/main.csv`，跑 `chart` |
| `framework-overview.svg` | 渲染出的结构图（Nature 双栏 183mm，7pt，Okabe-Ito） | 用浏览器/Illustrator/Inkscape 打开，或投稿前再跑 `check` |
| `framework-overview.png` | 上面那张的 300dpi 位图（2161×735） | README 首图；也可以直接丢进 PPT |
| `framework-overview-chart.svg` | 数据图：分组柱状图 + 误差棒 | 同上 |
| `framework-overview-chart.png` | 数据图 300dpi 位图（2161×850） | 同上 |

## 30 秒复现

```bash
node scripts/fig.mjs init /tmp/demo          # 造工作区（brief.md + figure.json + data/main.csv + out/）
node scripts/fig.mjs spec /tmp/demo          # brief.md → figure.json
node scripts/fig.mjs render /tmp/demo        # → out/framework-overview-diagram.svg
node scripts/fig.mjs chart /tmp/demo         # → out/framework-overview-chart.svg
node scripts/fig.mjs check /tmp/demo         # 合规检查（零成本）
node scripts/fig.mjs export /tmp/demo --formats png,pdf --dpi 300
```

## 两张图分别是怎么来的

**结构图**（`framework-overview.svg`）：`type: pipeline`，两个面板 (a)(b)。
节点按边做拓扑分层，跨面板的边会自动走面板之间的空档，不穿节点；
字号只用 7pt / 6.5pt 两档；画布按内容自动裁高，四边留 3mm 白边。

**数据图**（`framework-overview-chart.svg`）：`data.kind: grouped-bar`，
`y` 点两列（`method_a` / `method_b`），误差列自动按 `method_a_sd` 这类命名找到；
配色走 `palettes.json` 的 `chart_colors`——**黑色只留给坐标轴和文字**，柱/线/点用蓝橙绿。

## 已知问题（别当成 bug，记在这里）

1. **边标签位置**：标签贴在折线（按弧长）中点上方 1mm。当两条边在很近的地方交叉时，
   标签的白色底板可能盖住另一条线一小段——不影响读数，但图上看着会有一点断线感。
2. **跨面板的长边**：绕行车道是「离理想位置最近、且不穿节点」的那条，所以偶尔会贴着
   某个节点的边框走（间距 ≥0.5mm）。节点特别多时建议把跨面板的边删掉，改用面板标题说明。
3. **导出文件名**：`export` 目前按 `figure.json` 的 `name` 命名输出（`<name>@300dpi.png`），
   所以先导结构图再导数据图会覆盖同名位图。要两张都留，导出时用 `--svg` 指定并分批拷走，
   或者把 `name` 改成不同值。
4. **PDF 导出**：走 Chrome headless；没装 Chrome 的机器会退到 ImageMagick，再没有就只给 SVG。
5. **中文字体**：SVG 里写的是 `Arial, Helvetica, PingFang SC, Noto Sans CJK SC, Microsoft YaHei`
   字体栈，靠系统字体渲染。投稿要求字体嵌入时，用 `export` 出的 PDF（Chrome 会嵌入子集）。
