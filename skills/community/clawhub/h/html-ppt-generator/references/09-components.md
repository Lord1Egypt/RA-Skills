# 09 · 组件规范（Design-System 版）

> 所有组件颜色和字体从激活的 **Tc 模板** CSS 变量继承，无独立 HTML 模板。
> 生成时结合 Tc 风格实现各组件，不硬编码非语义色。

---

## Tc 模板必须定义的 CSS 变量

```css
/* 核心颜色（来自所选 design-system 文件） */
--p:    主强调色       /* 进度条、高亮、圆点、标签 */
--pm:   主色 10-15% 透明背景
--bd:   主色 20% 透明描边
--t:    主文字色
--mt:   次文字色（卡片正文、摘要）
--dt:   弱文字色（标注、标签、页码）
--bg:   页面背景色
--card: 卡片背景色

/* 字体（继承自 design-system 文件） */
--font-display: 展示字体栈（含 Google Fonts fallback）
--font-body:    正文字体栈

/* 多系列图表色（AI 根据 design-system 色盘派生） */
--c1: var(--p)          /* 第一数据系列 */
--c2: [互补色1]         /* 第二数据系列，与 --p 形成对比 */
--c3: [互补色2]         /* 第三数据系列 */

/* 语义固定色（不随主题变化，有明确含义） */
--danger:  #ef4444
--warning: #f59e0b
--success: #10b981
--info:    #3b82f6
--neutral: #94a3b8
```

> ⚠ `--c2` / `--c3` 从 design-system 色盘中派生（如 light-novel-isekai 的魔法紫 `--magic: #7c3aed`）。
> 生成 Tc 时必须定义；各 design-system 文件中的注释色可直接复用。

---

## 一、页眉（Header）组件规范

> 高度固定 **72px**（`.hd` 区）。同一报告统一使用一种 HD 变体，不混用。

### HD1 · 标准双行型（最通用）

**结构：** 左侧双行（eyebrow 9px `var(--dt)` + 页面主题 17px bold `var(--t)`）/ 右侧（分类标签 + 状态灯 + 页码）

**背景：** `var(--bg)` + 底部 1px 描边 `rgba(255,255,255,0.06)`

**右侧元素：**
- 标签：`var(--pm)` 背景，`var(--bd)` 描边，`var(--p)` 文字，9px uppercase
- 状态灯：5px 圆点 `var(--p)` + glow `box-shadow: 0 0 8px var(--p)`
- 页码：11px monospace `var(--dt)`（格式 `01/10`）

---

### HD2 · 渐变色条型

**结构：** 左侧竖线装饰（2px `var(--p)` 渐变高光）+ eyebrow 9.5px + 主题 18px bold / 右侧大页码（22px `var(--p)` monospace）

**背景：** `var(--bg)` + 底部渐变线 `linear-gradient(90deg, transparent, var(--p), transparent)`

**适用：** 技术密度高、需要强调当前章节的页面

---

### HD3 · 极简单行型

**结构：** 左侧竖线（3px `var(--p)` border-radius 2px）+ 主题 13px bold / 右侧页码 monospace `var(--dt)`

**背景：** 亮色 `var(--bg)`，底部 1px `var(--bd)`

**适用：** editorial-minimal、japanese-minimalism 等浅色风格

---

### HD4 · 终端路径型

**结构：** `● /report/section.md` 面包屑（● 绿色 `--success`，路径 `--neutral`，文件名 `--info`）+ ACTIVE 徽章 / 右侧 last-updated + 页码

**背景：** `var(--bg)` + 底部 `var(--bd)`，全 monospace 字体

**适用：** terminal-code、developer-tech 专用

---

## 二、摘要栏（Summary Bar）组件规范

> 高度固定 **48px**（`.sm` 区）。不得留空，必须包含核心结论（≤40 字，含具体数字）。

### SM1 · 结论文字型（最通用）

**结构：** 左侧竖线（3px `var(--p)` 高光）+ 核心结论文字（11px `var(--mt)`）/ 右侧 2-3 个标签徽章

**背景：** `rgba(0,0,0,0.25-0.35)` + 顶部 1px `rgba(255,255,255,0.05)`

**数字高亮：** `<b style="color:var(--t)">97%</b>`

---

### SM2 · 多指标横排型

**结构：** 左侧 3 个 KPI 横排（数字 16px bold `var(--p)` 或语义色 + 标注 8px `var(--dt)`）/ 右侧进度条 + 页码

**分隔线：** `rgba(255,255,255,0.06)` 竖线

**适用：** 数据密集页，需要摘要栏呈现关键数字

---

## 三、卡片变体规范

> 所有卡片遵循三层内容结构：标题行 + 正文（≥60字，≥2数字）+ 第三层组件（数据块/SVG/进度条）

### CARD-STD · 标准内容卡（默认）

**背景：** `var(--card)` / 描边 `var(--bd)` / 圆角 6-8px

**结构：** 标题（12.5px bold `var(--t)`）+ 正文（11.5px line-height 1.45 `var(--mt)`）+ 第三层

**间距：** padding 8px 10px，内部 gap 5px

---

### CARD-A · 全色强调卡

**背景：** `var(--p)` 实色填充

**文字：** 标题 `rgba(255,255,255,0.9)` / 正文 `rgba(255,255,255,0.75)` / 大数字 #fff

**限制：** 每页最多 **1 个**，用于放置最重要数字或核心结论

---

### CARD-B · 无边框色条卡（内容主导）

**背景：** 透明，左侧 3px 竖线 `var(--p)`，padding-left 14px

**适用：** editorial-minimal、editorial-split 右栏、japanese-minimalism

---

### CARD-C · 图标+数字三件套

**结构：** 顶部图标方块（28×28px `var(--pm)` 背景 + `var(--bd)` 描边）+ 大数字（26px bold `var(--p)`）+ 说明文（10.5px `var(--mt)`）

**适用：** 特性/KPI 展示，每卡聚焦一个指标

---

### CARD-D · 横向跨列宽卡

**结构：** 左侧大数字块（80px 宽，44px bold `var(--p)`）+ 渐变分隔线（`rgba(--p,0.3)`）+ 右侧标题+正文

**跨列：** `grid-column: span 2`

**适用：** 需突出单个最重要指标，搭配右侧详细说明

---

### CARD-E · 语义状态卡

**颜色规则：** 危险=`var(--danger)` / 成功=`var(--success)` / 警告=`var(--warning)` / 信息=`var(--info)`

**结构：** 左侧 3px 竖线（语义色）+ 状态标签行（6px 圆点 + uppercase，8-9px）+ 说明文

**背景：** `rgba(语义色, 0.08)` / 描边 `rgba(语义色, 0.2)` / 圆角 0 6px 6px 0

---

## 四、标签/徽章规范

| 变体 | 背景 | 描边 | 文字 | 圆角 | 用途 |
|------|------|------|------|------|------|
| 实色填充 | `var(--p)` | 无 | #fff | 2px | 一级分类/强调 |
| 描边型 | 透明 | `var(--p)` 1px | `var(--p)` | 2px | 次级标签 |
| Pill 型 | `var(--pm)` | `var(--bd)` | `var(--p)` | 10px | 类别/分组 |
| 状态含点 | 语义色 10% | 语义色 25% | 语义色 | 10px | 在线/离线/异常 |
| 数字徽章 | `var(--p)` | 无 | #fff | 圆形 min-w 18px | 计数/排名 |
| Callout 引用 | `var(--pm)` | 左侧 3px `var(--p)` | `var(--mt)` | 0 4px 4px 0 | 补充说明/引用 |

---

## 五、数字排版规范

### 单位格式

```
国内报告（中文）：
  < 1万      → 直接写数字：8,234
  1万~1亿    → 万为单位：2.3万 / 156万
  > 1亿      → 亿为单位：1.2亿 / 34.5亿

国际报告（英文混排）：
  < 1K       → 直接写：834
  1K~1M      → K 单位：23.4K
  > 1M       → M/B 单位：1.2M / 3.4B

禁止：1,234,567（正文中过长）→ 改为 123.5万 / 1.2M
```

### 正负变化颜色

```
正增长   → var(--success)  ↑ +34%
负变化   → var(--danger)   ↓ -12%
持平     → var(--neutral)  →  0%
语义颠倒（下降=好事）→ 手动指定 var(--success) ↓ -8% 漏洞减少
```

### 关键词高亮

```html
数字/百分比 → <b style="color:var(--t)">97%</b>
公式/代码   → <em style="color:var(--p);font-style:normal;font-family:monospace">δ=ε·sign</em>
专有名词    → <b style="color:var(--t)">PGD-AT</b>
```

---

## 组件使用检查

```
□ 同一报告内页眉使用统一的 HD 变体（不混用 HD1/HD2/HD3）？
□ 摘要栏包含核心结论（含具体数字，≤40字），不为空？
□ CARD-A 全色强调卡每页最多 1 个？
□ CARD-E 语义状态卡颜色与语义一致（危险=红，安全=绿，警告=橙）？
□ 数字单位格式正确（万/亿 或 K/M/B）？
□ 正负变化使用语义色（--success / --danger）？
□ 所有颜色来自 Tc CSS 变量或语义固定色，无硬编码非语义色？
```
