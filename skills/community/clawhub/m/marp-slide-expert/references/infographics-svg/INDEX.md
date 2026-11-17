# infographics-svg — 内联 SVG 信息图与关系图

> 本模块讲的是**页级版式之外的图形绘制**：在 marp 幻灯片里用内联 SVG 画信息图和关系图。
>
> 如果你只是要把文字和表格排在一页上，看 [../layout-patterns.md](../layout-patterns.md)（页级版式），不需要进这里。

## 为什么用 SVG 而不是图片

一张 PNG 改一个数字就要重画；内联 SVG 直接写在 `.md` 里，跟着文件走，文字可搜索，PDF 里是矢量不糊，改一个颜色只动一个十六进制值。

## 四层结构

画一张图要依次经过四层，**每层只管一件事**：

```
① structures  选题     这份内容能画哪几张图？每张画什么？
      ↓
② skeletons   体裁     用什么图形承载这个关系？
      ↓
③ metaphors    语气     在同一副骨架上换什么叙事外壳？
      ↓
④ styles      配色     什么颜色、什么字阶？
   ─────────────────────────────────
   craft       笔法     画布多大？间距多少？线怎么连？字怎么排？
              怎么画才不翻车？（横切所有层）
```

一次对照：**structures 是选题，skeletons 是体裁，metaphors 是语气，styles 是配色，craft 是笔法。**

②③ 分开的价值：骨架层可以随需求无限扩充，而 metaphors 表**永远不用动**——新骨架自动继承全部隐喻。

## 文件地图

| 文件 | 什么时候读 |
|---|---|
| [structures.md](structures.md) | 拿到一份文档/材料，不知道能画什么 |
| [skeletons/INDEX.md](skeletons/INDEX.md) | **先读这个**——关系类型 → 骨架的路由表 |
| [metaphors.md](metaphors.md) | 骨架定完之后，选叙事外壳 |
| [styles/INDEX.md](styles/INDEX.md) | 选配色（默认用 deck 调色板，这里是备选） |
| [craft/marp-compat.md](craft/marp-compat.md) | 内联 SVG 的硬约束与静默失败模式 |
| [craft/canvas.md](craft/canvas.md) | 画布坐标系、间距尺度、节点预算 |
| [craft/connectors.md](craft/connectors.md) | 连线语义编码（线型即语义） |
| [craft/typography.md](craft/typography.md) | CJK 字阶与排版避坑 |
| [craft/qa.md](craft/qa.md) | 交付前的两道关（lint + 渲染） |

## 标准流程

```
1. 读骨架路由        问：这些节点之间到底是什么关系？
2. 选骨架文件        拿到坐标公式和完整模板
3. （可选）换外壳     问：这页要什么情绪？查 metaphors 表
4. 填内容            按 craft/typography 的字宽规则估节点尺寸
5. 配色              默认 deck 调色板
6. lint              node scripts/svg-lint.mjs deck.marp.md
7. 渲染肉眼过一遍     marp deck.marp.md --html --images png -o check
8. 贴进 .marp.md      记得加 <!-- _class: diagram -->
```

## 最短路径

已经知道要画什么、只想抄一段改改 → 直接去 [skeletons/](skeletons/)，每个骨架文件末尾都有可运行的完整模板。改文字、换配色、跑 lint、渲染看一眼，四步完事。

## 三条最容易踩的坑

1. **忘了 `--html`** — 内联 SVG 被转义成一整页源码。见 [craft/marp-compat.md](craft/marp-compat.md) §1
2. **`marker` id 重复** — 多张图合并导出时箭头全部串到第一个定义。见 [craft/marp-compat.md](craft/marp-compat.md) §2
3. **字号写死了 `font-size` 属性** — 改字号时这张图不同步。字号只走 class。见 [craft/typography.md](craft/typography.md) §1

## 可运行的样例

| 文件 | 内容 |
|---|---|
| [../../examples/infographic-gallery.marp.md](../../examples/infographic-gallery.marp.md) | **图形与风格总览**——每个骨架、每个隐喻、每套风格一页，选型时先翻这个 |
| [../../examples/infographic-gallery.marp.md](../../examples/infographic-gallery.marp.md) | 页级分栏版式（属另一个模块，但常和图一起用） |

> 图形 deck 由 `node scripts/build-gallery.mjs` 从本目录生成。改完模板重跑一次即可，不要手改。
