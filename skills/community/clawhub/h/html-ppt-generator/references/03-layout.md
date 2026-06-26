# 03 · 布局系统

> **核心原则：** 先分析本页内容结构，自创专属布局 Lc；layout/ 是基因库，不是选项菜单。

---

## ⚡ 按需加载规则

> **禁止一次性读取 layout/ 下的所有文件。**
> 仅在 Step B 确定了父布局后，才读取对应的 1–2 个文件。其余文件本次不加载。

```
需要左大图结构       → 只读 layout/layout-a.md
需要右大图结构       → 只读 layout/layout-l.md
需要四行双栏         → 只读 layout/layout-b.md
需要六格等权网格     → 只读 layout/layout-c.md
需要四格+主视觉      → 只读 layout/layout-d.md
需要顶横幅+三列      → 只读 layout/layout-e.md
需要左导航+主区      → 只读 layout/layout-f.md
需要双列+全宽底部    → 只读 layout/layout-g.md
需要中央突出三列     → 只读 layout/layout-h.md
需要KPI条+双列       → 只读 layout/layout-i.md
需要上1下2品字       → 只读 layout/layout-j.md
需要上2下1倒品字     → 只读 layout/layout-k.md
需要四列等宽         → 只读 layout/layout-m.md
需要三横带结构       → 只读 layout/layout-n.md
两者组合变形         → 读对应2个，其余跳过
```

---

## 🤖 第零步：自创本页专属布局（每页生成必须执行）

> ⚠ **强制要求**：每页开始前，AI 必须先完成此步骤。禁止直接套用 A/B/C/D。

### 执行流程

```
输入：本页要表达的内容结构 + Tc 视觉模板特征
  ↓
Step A · 分析本页内容骨架
  - 有几个平行维度？（2/3/4/5/6…）
  - 有没有一个"主视觉"需要突出？（大图/大数字/大标题）
  - 信息有没有层级关系？（总-分 / 步骤流 / 并列对比）
  - 内容密度偏高还是偏低？（字多 vs 图多）
  ↓
Step B · 按需读取父布局文件（从下表选 1–2 个，只读这几个）
  - 提取：grid 结构 / 列宽比例 / 行高计算 / 变形方向
  - 决定哪些基因要"变异"（列数/跨格/比例调整）
  - 计算各区精确像素，确保总高度 ≤ 580px（ct 区）
  ↓
Step C · 声明本页专属布局 Lc
  - 写出：继承自 / 变异点 / ASCII 结构图 / grid CSS / 空间计算
  ↓
输出：Lc 定义 → 本页以 Lc 为唯一布局生成
```

---

## 📁 layout/ 布局文件索引

| 文件 | 结构基因 | 适用场景 |
|------|---------|---------|
| `layout/layout-a.md` | 左侧主视觉 + 右侧垂直三分 | 技术原理、流程图解、攻击链 |
| `layout/layout-b.md` | 水平横切四行，每行左文右图 | 步骤流程、方法对比、四阶段分析 |
| `layout/layout-c.md` | 均匀网格，六格等权 | 分类对比、六维度分析、案例矩阵 |
| `layout/layout-d.md` | 左侧四小格 + 右侧跨行主视觉 | 执行摘要、综合展示、矩阵分析 |
| `layout/layout-e.md` | 顶部全宽横幅 + 底部三列 | 主题总述、成果亮点展示、章节概览 |
| `layout/layout-f.md` | 左导航栏(160px) + 右侧双行 | 章节索引、带分类标签对比、模块说明 |
| `layout/layout-g.md` | 上方等权双列 + 下方全宽汇聚 | 对比分析+综合结论、双维度+大图表 |
| `layout/layout-h.md` | 三列中央突出（1:2:1 比例） | 核心概念展示、推荐方案对比、前中后流程 |
| `layout/layout-i.md` | KPI 条(90px) + 下方双列内容 | 数据仪表板、业绩报告、指标监控 |
| `layout/layout-j.md` | 品字形：上1宽 + 下2等 | 总-分结构、问题+双方案对比 |
| `layout/layout-k.md` | 倒品字：上2等 + 下1宽 | 双因素对比+综合结论、证据+判断 |
| `layout/layout-l.md` | 左侧垂直三分 + 右侧主视觉（A镜像） | 分析文字+信息图、三步骤+架构图 |
| `layout/layout-m.md` | 全宽等分四列竖排 | 四要素并列、四阶段流程、四维度分析 |
| `layout/layout-n.md` | 三横带（上窄100+中宽1fr+下窄120） | 背景-核心-结论三段式、问题-方案-效果 |

---

## 🧬 Lc 布局定义模板（AI 填写）

```
【本页专属布局 Lc】

继承自：layout/[文件名].md  → 提取：___（grid结构/列宽/行高…）
变异点：___（与父布局不同的结构调整）

ASCII 结构图：
┌─────────┬─────────┐
│         │         │
│         ├─────────┤
│         │         │
└─────────┴─────────┘

grid CSS：
  grid-template-columns: ___
  grid-template-rows: ___
  gap: ___px
  padding-top: ___px

空间计算：
  总高验证：___px + ___px × gaps + ___px padding = ___px ≤ 580px ✓
  每格可用正文高度：___px → 约 ___–___ 字
```

---

## 通用布局基础 CSS

```css
/* 卡片通用（各风格会覆盖视觉样式，结构保持一致） */
.card {
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 5px;           /* 卡片内间距上限 5px */
  padding: 8px 10px;  /* 上下 ≤8px，左右 ≤12px */
}
.ch {                 /* 卡片标题 */
  font-size: 12.5px; font-weight: 700;
  flex-shrink: 0;
}
.cb {                 /* 卡片正文 */
  font-size: 11.5px; line-height: 1.45;
  overflow: hidden; flex: 1;
}
.cb b, .cb strong { /* 关键词高亮 */ }
.cb em { font-style: normal; font-family: monospace; font-size: 11px; } /* 公式/代码 */

/* mini 数据卡片行 */
.mini-row { display: flex; gap: 5px; flex-shrink: 0; margin-top: 4px; }
.mini {
  flex: 1; padding: 4px 7px; border-radius: 3px;
  display: flex; flex-direction: column;
}
.mh { font-size: 10.5px; font-weight: 600; }
.ml { font-size: 9.5px; margin-top: 1px; }
```

---

## 🤖 Lc 自创空间计算规则

> 无论 Lc 如何变形，必须满足以下约束：

```
总宽：967px（1017 - 左右 padding 25×2）
总高：580px（ct 区固定高度，padding-top 在布局容器上设，≤12px）

列宽计算：sum(所有列宽) + gap × (列数-1) ≤ 967px
行高计算：sum(所有行高) + gap × (行数-1) + padding-top ≤ 580px

每格最小可用高度（含 padding）：
  格高 - padding上下(≤16px) - 标题行(≤22px) - mini行(≤40px) ≥ 60px
  → 低于 60px 的格不能放正文，只能放纯数字/图标

gap 硬上限：
  主布局 gap ≤ 12px
  卡片内 gap ≤ 5px
```

---

## ⚠️ Grid + Flex 混用的高度约束（铁律）

> 问题根源：布局容器在 `.ct` 内部使用 `height: 100%` + `padding-top` 时，
> 实际高度 = 580px + padding-top，导致内容溢出被摘要栏覆盖。

### 强制 CSS 规则

```css
/* 规则 1：布局容器必须主动减去 padding-top */
.layout-x {
  height: calc(580px - 8px);  /* 主动减去 padding */
  padding-top: 8px;
  /* 或 */
  grid-template-rows: 8px 1fr;  /* 将 padding 作为第一行 */
}

/* 规则 2：flex 容器中的卡片必须允许收缩 */
.left-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.card {
  flex: 1;
  min-height: 0;  /* ← 关键：允许 flex 收缩 */
  overflow: hidden;
  height: 176px;  /* 显式固定高度，非 100% */
}

/* 规则 3:Grid 行高必须显式定义 */
.left-grid {
  display: grid;
  grid-template-rows: repeat(3, 176px);  /* (580 - gap×2) / 3 */
  gap: 8px;
}
```

### 高度计算公式（修正版）

```
布局容器有效高度 = height + padding-top
                 = calc(580px - 8px) + 8px
                 = 580px ✓

卡片总高度 = 卡片数量 × (卡片高度 + gap)
三卡示例：3 × (176px + 8px) - 8px(最后一个无 gap) = 544px ≤ 580px ✓
```

### 内容密度上限

| 卡片类型 | 最大高度 | 适用场景 | 内容建议 |
|---------|---------|---------|---------|
| 标准卡 | 176px | 大多数内容页 | 标题 +60-80 字正文 + 数据块 |
| 紧凑卡 | 120px | 高密度对比页 | 标题 +40-60 字正文 |
| 全高卡 | 520px | 单卡片满屏 | 标题 +200-300 字正文 + 多图 |

**三卡垂直排列示例**：
```
可用高度：580px - padding-top(8px) - gaps(8px×2) = 556px
每卡高度：556px / 3 ≈ 185px（含 gap 则 176px）
```

**内容密度自查**：
```
□ 布局容器 height 是否为 calc(580px - padding-top)？
□ flex 卡片是否有 `min-height: 0` + 显式 height？
□ Grid 行高是否显式定义（非 1fr 自动撑高）？
□ 三卡总高是否 ≤ 556px（留 gap 余量）？
□ 卡片正文是否 ≤ 80 字（避免撑高）？
```

---

## 布局与视觉风格协同规则

| Tc 视觉风格特征 | Lc 对应约束 |
|---------------|------------|
| editorial-split（左暗右亮双区） | 不读 layout/ 文件，Lc 为左栏(280-320px) + 右栏(余量)，内部自由分行 |
| terminal-code（左侧边栏+右主区） | 不读 layout/ 文件，Lc 为左边栏(160px) + 右主区，右主区内再分格 |
| dashboard-analytical（KPI横排+下方图表） | 优先 Lc：上方 KPI 固定高度行(90-110px) + 下方图表区 |
|  Tc  | 按需读取 layout/ 基因文件自由变形 |

---

## 布局多样性检查

```
□ 已完成第零步，Lc 有完整定义（继承来源 + ASCII图 + grid CSS + 空间计算）？
□ Lc 的总行列高度精确计算，不超 580px？
□ 相同 Lc 结构未在报告内连续出现 3 次以上？
□ editorial-split / terminal-code 特殊风格使用了自定义列结构，未读 layout/ 文件？
□ 10 页报告中使用了 ≥4 种不同布局（从 A-N 共 14 种中选择）？
```
