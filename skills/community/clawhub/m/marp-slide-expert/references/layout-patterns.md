# Slide Layout Patterns

Reference: [marpit.marp.app/directives-and-comment](https://marpit.marp.app/directives-and-comment) and [slide-layouts](https://marpit.marp.app/slide-layouts).

> **本文件讲「页级版式」**——一页的内容块怎么排（分栏、分区、纯文字、纯表格）。
> 要在页面上**画图**（信息图、关系图），那是另一层，见 [infographics-svg/INDEX.md](infographics-svg/INDEX.md)。
> 两者不交叉：内容多就排版式，要表达关系才画图。

## 四族速查

| 族 | 版式 | 什么时候用 |
|---|---|---|
| **A 全幅** | [cover](#cover-slide) / [divider](#divider-slide) / [end](#end-of-deck-slide) | 封面、章节分隔、收尾 |
| **B 单栏** | [content](#content-slide) / 文字+表格 / 大表为主 | 默认。内容线性、一次读完 |
| **C 分栏** | [cols-2](#column-layouts) / `cols-3` / `cols-main` / `split-h` / `cols-2-table` | 并列信息多，单栏会溢出或太长 |
| **D 混合** | [multi-image](#multi-image-content-slide) / [text+image](#text--supporting-images) / [split-v](#5-图位上下分区-split-vflex) | 有截图/配图要放 |

**选择顺序**：先试 B（单栏），超 15 行再考虑 C（分栏），有图再进 D。**分栏不是默认解**——三栏塞三段话，不如拆成三页，每页一个论点。

## Slide separators

Marp uses `---` on its own line as the slide separator. Frontmatter sits at the top, before the first `---`.

```markdown
---
marp: true
theme: default
---

# First slide

---

# Second slide
```

## Special classes

Apply a class to a single slide using an HTML comment directive **before** the slide content:

```markdown
<!-- _class: cover -->

# Title slide
```

Common classes (defined in CSS):

| Class | Purpose |
|---|---|
| `cover` | Title slide, often full-screen gradient |
| `divider` | Section break, often dark and centered |
| `lead` | First content slide after cover, can have larger text |

For class definitions to work, your frontmatter `style:` block must define them.

## Cover slide

Standard pattern:

```markdown
<!-- _class: cover -->

# Main Title

## Subtitle

> Optional description or quote

**Speaker:** Name
**Date:** YYYY
```

CSS template:

```css
section.cover {
  background: linear-gradient(135deg, #1a1a2e 0%, #c0392b 100%);
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}
section.cover h1 { color: white; border-bottom: 3px solid rgba(255,255,255,0.4); }
section.cover h2 { color: rgba(255,255,255,0.85); }
```

## Divider slide

```markdown
<!-- _class: divider -->

# Chapter X

## Section name
```

CSS template:

```css
section.divider {
  background: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
section.divider h1 { color: #e74c3c; border-bottom: 3px solid #e74c3c; font-size: 2.4em; }
```

## Content slide

Default. Just markdown content; CSS applies the body font, table, and code styling.

```markdown
## Topic title

Body paragraph...

- Bullet 1
- Bullet 2

| Col A | Col B |
|---|---|
| A1   | B1   |
```

## Column layouts

**C 族。** 用 CSS grid + `<div>` 包裹实现，**不需要 `--html`**（内联 SVG 才需要那个开关，div 两种模式都渲染）。

### 坐标与行数预算

| 栏数 | 栏宽（可用宽 1140px） | 每栏行数预算 | 栏内表格列数上限 |
|---|---|---|---|
| 2 栏 | ~558px | 7 行 | 3 列 |
| 主次 2:1 | 740 / 370 | 7 / 5 行 | 2 列（窄栏） |
| 3 栏 | ~367px | **5 行** | **2 列** |

**15 行上限是整页的，不是每栏的。** 三栏版式每栏只有约 5 行预算，还要扣掉 `##` 标题那 1 行。这是分栏最容易翻车的地方——三栏各塞 8 行，投影上就是一堵字墙。

### 必需 CSS

追加进 frontmatter 的 `style:` 块（`style-bootstrap.md` 里已有完整版）：

```css
/* ---- 页级分栏版式 ---- */
.cols { display: grid; align-items: start; }
.cols-2  { grid-template-columns: 1fr 1fr;      gap: 24px; }
.cols-3  { grid-template-columns: repeat(3,1fr); gap: 20px; }
.cols-main  { grid-template-columns: 2fr 1fr;   gap: 24px; }   /* 主次 2:1，反过来写 1fr 2fr */
.split-h { display: grid; grid-template-rows: auto auto; gap: 24px; align-items: start; }
/* D 族：文/图上下分区（flex column）；图位放真实 <img>，max-width/max-height 约束缩放 */
.split-v    { display: flex; flex-direction: column; gap: 18px; min-height: 380px; }
.split-v > div { border-radius: 6px; padding: 16px 20px; }
.split-v .up   { background: #eef1f4; flex: 1; }
.split-v .down { background: #1a1a2e; color: #fff; display: flex; flex-direction: column; justify-content: center; align-items: center; flex: 1; }
.split-v img   { max-width: 100%; max-height: 100%; border-radius: 4px; display: block; }
.cols h3, .split-h h3 { color: #c0392b; font-size: 1.05em; margin: 0 0 6px; }
.cols p, .split-h p   { font-size: 0.8em; line-height: 1.5; margin: 0 0 8px; }
.cols ul, .split-h ul { font-size: 0.82em; margin: 0 0 8px; }
.cols table, .split-h table { font-size: 0.66em; }   /* 栏内表格要更小，否则横向撑爆 */
```

`align-items: start` 不能省——否则短栏被拉伸，底部参差。

### 1. 等宽双栏 `cols-2`

两个并列论点、两套方案、一页讲两件事。

```markdown
<div class="cols cols-2">
<div class="col">

### 方案 A：自建

<p>团队已有基础，掌控力强。</p>

- 周期 9 个月
- 成本高
- 可控性完全

</div>
<div class="col">

### 方案 B：采购

<p>上线快，但受限于厂商。</p>

- 周期 2 个月
- 成本中
- 可控性受限

</div>
</div>
```

**div 前后各留一个空行**，div 内部的 markdown 才不会被当成正文。

### 2. 等宽三栏 `cols-3`

三元结构：演进-挑战-对策、现状-原因-对策、Before-Now-After。**每栏 ≤ 5 行。**

### 3. 主次分栏 `cols-main`

左主右次（2:1），或反过来 `1fr 2fr`。**最常用的一种**——左边是要点，右边是佐证表/细节/注。

```markdown
<div class="cols cols-main">
<div class="col">

### 核心结论

<p>把数据中台提到集团级，先统一口径再谈分析。</p>

</div>
<div class="col">

| 维度 | 现状 | 目标 |
|---|---|---|
| 覆盖 | 3 团队 | 全公司 |
| 时延 | 5 天 | 1 天 |

</div>
</div>
```

### 4. 上下分区 `split-h`

上结论下证据、上表下注、上现状下目标。

```markdown
<div class="split-h">
<div>

**结论**：2026 年完成全量迁移，Q4 之前不停留在试点。

</div>
<div>

| 阶段 | 时间 | 负责 |
|---|---|---|
| 试点 | 2025 Q3 | 平台组 |
| 扩面 | 2026 Q1 | 各业务线 |

</div>
</div>
```

### 5. 图位上下分区 `split-v`（flex）

**「上文下图」**——上半文字、下半图片。marp 的 `bg` 关键字只有整页和左右半幅，**做不了上下分区**；用 `<div>` + flex column 自己写。

```markdown
<div class="split-v">
<div class="up">

### 上文

结论先行。上下比例用 `flex` 调：`flex:1` 等高，图位更大就写 `flex:2`。

</div>
<div class="down">

<img src="assets/demo.png" alt="图位">

</div>
</div>
```

`.down` 深色是图位容器，`<img>` 居中显示。**横图**靠 `max-width:100%` 收窄就够了；**竖图**要给 `max-height` 一个具体值（如 `style="max-height:230px"`）——`max-height:100%` 的百分比高度在 flex 分格里不可靠，图会撑爆格子。把 `flex-direction` 换成 `row`，同一套写法就是左右分区。

### 6. 双栏各带表 `cols-2-table`

两张对照表并排。**每张表 ≤ 2–3 列**——分栏后宽度只有原来的 1/2，4 列的表在栏里会横向溢出。

### 分栏的坑

| 现象 | 原因 | 修法 |
|---|---|---|
| 栏内表格只有半宽 | 丢了 `display: table !important` 修复 | 该修复在同一个 `style:` 块里，确认没删 |
| 栏内表格横向撑爆 | 栏宽减半，列数没减 | 减列，或加 `font-size: 0.66em` |
| 短栏底部参差 | 缺 `align-items: start` | 加上 |
| 栏内 `h3` 上边距吃掉一行 | marp 默认 `h3` 边距在窄栏里被放大 | 栏内 `h3 { margin: 0 0 6px }` |
| 文字挤成三堵墙 | 每栏塞了 8+ 行 | 拆页。三栏各讲一个论点，比一页三栏更好 |
| div 之后的裸段落没渲染 | div 块结束了 markdown 上下文 | 后续内容另起一个 div，或放到 div 之前 |
| 分栏后 deck 导出异常 | 误以为分栏需要 `--html` | 分栏**不需要** `--html`；只有内联 SVG 需要 |

### 要不要分栏？

**分栏的价值是「并置对比」。** 如果两栏内容有先后顺序、读者不该同时看，就不要并排——那是列表，不是对比。

判断问句：**「读者会来回看这两栏做比较吗？」** 会 → 分栏；不会 → 拆成两页或用单栏列表。

## Multi-image content slide

For a row of related images (screenshots, diagrams):

```markdown
## Topic

Brief intro sentence.

![bg](<shot1.png>)
![bg](<shot2.png>)
```

If images are tall/portrait:

```markdown
## Topic

![bg vertical](<shot1.png>)
![bg vertical](<shot2.png>)
```

## Text + supporting images

When text needs prominence and images are illustrative:

```markdown
## Topic

Lead paragraph explaining the concept.

Detailed point 1.
Detailed point 2.
Detailed point 3.

![bg right w:60%](<illustration.png>)
```

Wait — `bg right w:60%` is NOT valid marp syntax (the `w:` shortcut doesn't combine with `bg right`). Use the split pattern instead:

```markdown
## Topic

Lead paragraph explaining the concept.

Detailed point 1.
Detailed point 2.
Detailed point 3.

![bg right vertical](<illustration1.png>)
![bg](<illustration2.png>)
```

The first image takes the right column (stacks vertically with other right images); the second image fills the left area as a background; content overlays on the left.

## End-of-deck slide

Common patterns:

```markdown
---

## Q&A

Thanks!
```

Or a divider-style closing:

```markdown
<!-- _class: divider -->

# Thanks

Questions?
```

## Header / footer (paginate)

Add page numbers via frontmatter:

```yaml
paginate: true
```

Style the page number with:

```css
footer {
  position: absolute;
  left: 900px;
  bottom: 25px;
}
```

Or hide it on cover/divider:

```yaml
_paginate: skip
```

(place this as a directive on the slide where you want to skip)
