# QA 层 — 交付前的两道关

> **本文件自足**：SVG 图形有两类错误。**必然错的**（空行、id 冲突、坐标越界）用脚本抓；**看起来错的**（重叠、错位、留白失衡）只能靠眼睛看。两道关都要过。

## 核心原则

**不要相信「代码看起来对」。**

一段 SVG 源码在编辑器里读起来完全合理，渲染出来可能是文字压线、节点重叠、箭头方向反了。源码审查只能抓语法，抓不了观感。

## 第一关：lint（确定性检查）

```bash
node scripts/svg-lint.mjs deck.marp.md
```

对每个 `<svg>` 块做 6 项检查：

| # | 检查 | 为什么能脚本化 |
|---|---|---|
| 1 | SVG 块内**空行** | 字符串扫描。空行会切断 HTML 块，图形静默消失 |
| 2 | SVG 块内 `---` | 字符串扫描。仍被解析为分页符，一页裂成两页 |
| 3 | `marker` / `clipPath` **id 唯一**，且所有 `url(#id)` 引用都有定义 | 正则提取 id 集合与引用集合做差集 |
| 4 | 元素坐标**越出 viewBox** | 解析 `x/y/cx/cy/width/height`（含 `<rect>` `<circle>` `<text>`）与 viewBox 比对 |
| 5 | 硬编码 `font-size` 属性 | 应走 CSS class，否则改字号时全图不同步 |
| 6 | viewBox 宽度 = **1020** | 数值比对。宽度不统一会导致缩放比例不一致，图形大小参差 |

退出码非 0 表示有 ERROR（阻断交付），WARNING 不阻断但应逐条看一眼。

**lint 不做的事**：元素重叠检测、对比度检测、文字溢出检测。这几项的误报率高于检出率，反而会让人开始无脑忽略告警——那比不 lint 更糟。它们交给第二关。

## 第二关：渲染（肉眼过一遍）

```bash
marp deck.marp.md --html --images png -o check
# 产出 check.001 check.002 …（无扩展名，需重命名）
```

渲染成 PNG 逐页看。**不要在浏览器里看 HTML 就完事**——浏览器有缩放和滚动，容易掩盖实际投影效果。

### 视觉检查清单

| 维度 | 检查项 |
|---|---|
| **几何** | 元素重叠？超出 viewBox？同级对齐？间距一致？连线穿过节点？ |
| **排版** | 文字溢出节点？字号 < 15px？标签互相压？中文基线偏上？多行文字首行没对齐？ |
| **语义** | 有没有孤立的节点（声明了关系却没画线）？不查图例能读懂线的关系吗？ |
| **层级** | 是不是所有节点一样大（= 没有重点）？色相是否超过 3 个？ |
| **对比** | 深底上的文字够亮吗？浅底上的文字够深吗？灰度打印还读得出吗？ |
| **贴底** | 底部元素压到 footer 了吗？（→ 加 `<!-- _class: diagram -->`） |

### 修完要重渲

```
发现问题 → 改 → 重新渲染 → 再看
```

一次渲染发现的问题通常不止一个——看到第一个就该把整页重新扫一遍。

## 排版自查（不用渲染就能查）

这几条在写的时候就该拦住：

- [ ] 节点数 ≤ 7
- [ ] 树的层级 ≤ 3
- [ ] 单节点标签 ≤ 6 个中文字
- [ ] 节点宽度 ≥ 标签宽度 + 24px
- [ ] 多行文字 ≤ 3 行
- [ ] 颜色 ≤ 3 个色相 + 1 个强调色
- [ ] `marker` id 用了本图专属前缀
- [ ] 所有字号走 class

## 单图 HTML 预览

画图阶段不必每次都起 deck。内联 SVG 可以单独放进一个 `.html` 直接在浏览器里迭代：

```html
<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>图名</title>
<style>
  body { background:#FAFAFA; font-family:'PingFang SC','Noto Sans CJK SC',sans-serif; margin:0; padding:40px; }
  .card { max-width:1140px; margin:0 auto; }
  svg { display:block; margin:0 auto; max-width:100%; height:auto; }
  svg text { font-family:'PingFang SC','Noto Sans CJK SC',sans-serif; }
  svg .t { font-size:26px; font-weight:700; }
  svg .tb { font-size:19px; font-weight:700; }
  svg .qt { font-size:20px; font-weight:700; }
  svg .sm { font-size:15px; }
  svg .lbl { font-size:15px; fill:#7f8c8d; }
</style></head><body><div class="card">
<!-- SVG 在这里 -->
</div></body></html>
```

预览更快（不用跑 marp），改一个字刷新就看到。但**最终仍要过 marp 渲染那一步**——deck 环境里的 CSS 继承和 standalone 不完全一样，尤其是 `section` 的字号基准。

**最省事的做法其实是用 marp 自己当预览器**：新建一个只放一张图的 `.marp.md`，渲染出来就是 1:1 的真实效果——`marp one.marp.md --html -o one.pdf`，改一个字重跑一次。这比手搓 standalone HTML 更快，也不会有 CSS 继承差异。

看全部模板用 [../../../examples/infographic-gallery.marp.md](../../../examples/infographic-gallery.marp.md)（每个骨架/隐喻/风格一页，由 `node scripts/build-gallery.mjs` 生成）。

---

# 生成 deck 时的常见坑（实战经验）

**这一节记录的是构建 infographic-gallery.marp.md 这个 deck 实际踩过的坑。** 修一个就加一条，比 lint 抓不到的更隐蔽。

## 1. 路径：从 generator 写相对路径要看 cwd

```js
// 在 build-gallery.mjs 里写的图片路径：
parts.push(`![bg](<../../assets/marp.png>)`);
```

- marp CLI 的工作目录是 **deck 文件所在目录**（这里是 `examples/`）
- `../../` 是从 `examples/` 跳到 skill 根，再 `assets/marp.png`
- 这才对。**但生成器和 markdown 不在工作目录写**——generator 写 markdown 的路径得是相对 markdown 文件本身，不是相对 generator

**修法**：从 generator 写路径时，先回答"marp CLI 会从哪个目录读这张图？"——答：deck 所在目录。然后以那个目录为基准计算。

## 2. 连续 `---` 会产生空白页

```markdown
# 章节

---

<!-- 这里无意写了第二个 --- -->

---

## 下一节
```

**两段连续的 `---` 之间没有内容**，marp 会插入一个空白 slide。看着像垃圾页。

**修法**：脚本生成时用 `\n\n---\n\n` 拼装，不要写 `--- \n---` 紧挨着。本文件用 `writeFileSync(out, parts.join('\n\n---\n\n'))` —— 两个换行夹一个 `---`。

## 3. lint 启发式把表格里的 `<svg>` 字面量当 SVG 块

```markdown
| 手段 | CSS grid + `<div>` | 内联 `<svg>` |
```

这里 `<svg>` 是字面量，但 lint 的正则 `<svg\b[\s\S]*?</svg>` 会把这行当 SVG 块的开始，把整个表格吞掉，触发 "SVG 块内有空行" / "SVG 块内有 ---" 误报。

**修法**：
- 表格里用文字描述代替尖括号："CSS grid + 分栏 div"、"内联 SVG"
- 或者给 lint 加豁免指令 `<!-- svg-lint-ignore: blank-line, page-break -->` 局部禁用某些检查

## 4. 模板里的 `<!-- N=5 时 -->` 注释会引入空行

写示例 SVG 时常会写 `<!-- 这是 N=5 的情况 -->` 加注释。但 SVG 块内**禁止空行**，注释本身或前后空行都会触发 lint。

**修法**：
- 删 SVG 内的注释（注释在 SVG 里没意义）
- 或 generator 后处理：去掉 SVG 块内所有 `<!--...-->`，然后折叠连续空行

## 5. 生成的二级标题提取需要专门设 "## 变体："

`extract()` 用「SVG 之前最近的 `## 二级标题`」做变体名。如果模板用 "## 坐标公式" 这样的通用标题，所有变体都会被命名成 "坐标公式"。

**修法**：每个变体的规格文件，SVG 之前的二级标题必须以 `## 变体：XXX` 或 `## 变体 X：XXX` 开头。Generator 据此取名。

## 6. 飞轮弧线粗细差异 vs 视觉显著性

把 4 段弧的 `stroke-width` 从 2.5/4/5.5/7 改成 2.5/4/6/8——**视觉差异要足够大**，否则肉眼根本看不出"渐变"。粗细差异 < 50% 不可见。

**修法**：
- 要表达"势能自我积累"用渐变粗细时，**最小差距 ≥ 50%**（如 2.5/4/6/8）
- 或者**统一粗细**（推荐），让飞轮的视觉特征落在"4 段弧都有明确箭头"上——粗细一致也行

## 7. 几何要算不要估

飞轮的 4 段弧如果端点估错（比如用节点圆心当终点），画出来会和节点圆重叠或断开。

**修法**：
- 节点圆半径 r_node，弧半径 R
- 弧端点是节点圆周上的切点：圆心方向旋转 `asin(r_node/R)` 角
- 距离圆心 `R + r_node` 处
- 端点 `(cx + (R+r_node)·cos(α ± θ), cy + (R+r_node)·sin(α ± θ))`

```python
import math
def tangent_arc(fx, fy, tx, ty, cx, cy, R, r_node):
    theta = math.asin(r_node / R)
    af = math.atan2(fy-cy, fx-cx); at = math.atan2(ty-cy, tx-cx)
    delta = (at-af) % (-2*math.pi)
    if -math.pi < delta < 0:
        s_ang = af-theta; e_ang = at+theta
    else:
        s_ang = af+theta; e_ang = at-theta
    return cx+(R+r_node)*math.cos(s_ang), cy+(R+r_node)*math.sin(s_ang), \
           cx+(R+r_node)*math.cos(e_ang), cy+(R+r_node)*math.sin(e_ang)
```

## 8. markerUnits 默认是 strokeWidth

这是 SVG 1.1 的隐性坑：marker 会按线粗整体缩放。`stroke-width="8"` 的 marker 是默认 8 倍大。

**修法**：**所有 marker 必须显式写 `markerUnits="userSpaceOnUse"`**——这是写 SVG marker 的第一行铁律，不要忘。

## 9. 漏斗层宽不能用等差

10000 → 1200 → 380 → 96 的真实比例，如果画 4 层等差梯形（顶宽 760 → 底宽 96），看上去是 12% 的关系，但实际比例是 0.96%——**几何在说谎**。

**修法**：
- 用平方根尺度：宽度 ∝ `√v`，保留排序和大致落差
- 或者在底部明确写 "层宽为示意形状，量级以数字为准"
- 要精确比例用桑基，ribbon 宽度严格正比于数值

## 10. frontmatter 里的 HTML 注释会摧毁整个 style 块

```yaml
---
marp: true
<!-- 渲染命令 -->
style: |-
  ...
---
```

frontmatter 是 YAML。HTML 注释 `<!-- ... -->` 会破坏解析，导致整个 `style:` 块被静默丢弃——分栏失效、配色全丢、不报错。

**修法**：
- 注释写在 frontmatter 的 `---` 之外
- 渲染命令贴在 deck 末尾或单独 README
- 如果 deck 是 generator 生成的，把命令注释也放在 generator 输出里

## 11. lint 不需要写死严格硬规则

第一批 lint 我写了 viewBox 宽度 = 1020 的硬检查，后来加了风格预览（480 宽），于是不得不引入豁免机制。**lint 的规则要么是真正不能违反的（id 冲突、空行），要么是默认严格但允许显式豁免。** 严格且不让豁免的 lint 会在第一个反例出现时把整份 deck 误报成错。

**修法**：每条 lint 规则要回答：
- 这是真正不能违反的（ERROR）还是值得警告（WARNING）？
- 如果是硬规则，需要文件级豁免（如 `<!-- svg-lint-ignore: codes -->`）

## 12. 生成器幂等性

build-gallery.mjs 必须能反复跑出同样的 deck（byte-equal）。**任何输出中夹带 ID 计数、时间戳、随机数都会破坏幂等**。

**修法**：用确定性算法（按出现顺序重编号 marker id），不依赖环境变量、文件 mtime、网络。

## 13. 渲染 PNG 验证时一定要逐页看

lint 通过、build 通过，不代表 deck 就是好的。**`p.020` 的金字塔三角离第二层太远、`p.039` 的飞轮弧粗细看不见差异、`p.042` 的冰山六边形太规则**——这些都是 lint 抓不到的「看起来错」。

**修法**：
- 每改一次骨架，重新生成 deck，重新渲染 PNG
- 抽查每个新图（这次抽查了 6 张关键页：金字塔/飞轮/冰山/波浪/icon-rail/卡片组）
- 修一个就更新骨架文件本身——下次跑 lint 才能一直过

## 14. 删除调试临时文件

rendering PNG 到 `/tmp/gall/p.001` 是临时调试用的，**别 commit 进 git**。commit 之前 `git status --short` 过一遍。

## 15. 「用法」章节放最前面

用户拿到一个 skill，第一反应是"我能拿它干嘛"。所以 ① 用法（4 步选型 + 笔法）应当是 deck 第一章节，而不是穿插在中间。生成器里用 `parts.push()` 顺序就是 deck 顺序。
