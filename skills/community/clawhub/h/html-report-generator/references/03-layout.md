# 03 · 布局系统

> **核心原则：** 先分析本页内容结构，自创专属布局 Lc；A/B/C/D 是基因库，不是选项菜单。

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
Step B · 从 A/B/C/D 提取基因（组合/变形/新建）
  - 匹配 1–2 个最接近的基础布局作为"父布局"
  - 确定列数、行数、主区比例、是否需要跨行/跨列
  - 计算各区精确像素，确保总高度 ≤ 580px（ct 区）
  ↓
Step C · 声明本页专属布局 Lc
  - 画出 ASCII 结构图
  - 写出精确的 grid-template-columns / rows
  - 计算每格可用高度和文字容量
  ↓
输出：Lc 定义 → 本页以 Lc 为唯一布局生成
```

---

## 通用布局基础 CSS

```css
/* 卡片通用（各模板会覆盖视觉风格，结构保持一致） */
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

## 📚 A/B/C/D 基础布局参考库

> **定位：** 这是 AI 创建 Lc 时的"基因库"，提供可复用的 grid 结构和空间计算方法。
> 每次生成不是从这里"选一个用"，而是"提取基因重组"。

---

### 布局 A · 左大图 + 右三行

**适用：** 技术原理、流程图解、攻击链

```
┌──────────────┬──────────────────────────┐
│              │  ① 文字卡片              │
│  左侧大图    ├──────────────────────────┤
│  366px       │  ② 文字卡片              │
│              ├──────────────────────────┤
│              │  ③ 文字卡片              │
└──────────────┴──────────────────────────┘
```

#### 空间计算

```
左图宽   = 366px
gap      = 12px
右侧宽   = 967 - 366 - 12 = 589px
右侧行高 = (580 - 12×2 - padding-top 12) ÷ 3 ≈ 181px
正文可用 ≈ 181 - 标题 24px - padding 16px = 141px → 约 70–100 字
```

#### CSS

```css
.layout-a {
  display: grid;
  grid-template-columns: 366px 1fr;
  gap: 12px;
  height: 100%;
  padding-top: 12px;
}
.la-right {
  display: grid;
  grid-template-rows: repeat(3, 1fr);
  gap: 12px;
}
```

---

### 布局 B · 上下四行（每行双栏）

**适用：** 步骤流程、方法对比、四阶段分析

```
┌───────────────────────────────────┐
│  行1：左文字(58%)  右图表(42%)    │
├───────────────────────────────────┤
│  行2：左文字       右图表          │
├───────────────────────────────────┤
│  行3：左文字       右图表          │
├───────────────────────────────────┤
│  行4：左文字       右图表          │
└───────────────────────────────────┘
```

#### 空间计算

```
padding-top  = 10px
每行高       = (580 - 10×3 - 10) ÷ 4 = 130px
左文字宽     = 967 × 58% ≈ 561px
右图表宽     = 967 × 42% ≈ 406px
正文可用     ≈ 130 - 标题 22px - padding 16px = 92px → 约 45–55 字
```

> ⚠ 每行必须是左文 + 右图双栏，**禁止纯文字行**

#### CSS

```css
.layout-b {
  display: grid;
  grid-template-rows: repeat(4, 1fr);
  gap: 10px;
  height: 100%;
  padding-top: 10px;
}
.lb-row {
  display: grid;
  grid-template-columns: 58% 42%;
  gap: 10px;
}
```

---

### 布局 C · 3×2 六格网格

**适用：** 分类对比、六维度分析、案例矩阵

```
┌──────────┬──────────┬──────────┐
│  ① 格    │  ② 格    │  ③ 格    │
├──────────┼──────────┼──────────┤
│  ④ 格    │  ⑤ 格    │  ⑥ 格    │
└──────────┴──────────┴──────────┘
```

#### 空间计算

```
padding-top = 10px
每格高      = (580 - 8 - 10) ÷ 2 = 281px
每格宽      = (967 - 8×2) ÷ 3 ≈ 317px
正文可用    ≈ 281 - 标题 22px - mini 40px - padding 16px = 203px → 约 70–90 字
```

#### CSS

```css
.layout-c {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 8px;
  height: 100%;
  padding-top: 10px;
}
```

---

### 布局 D · 2×2 四格 + 右侧大图

**适用：** 执行摘要、综合展示、矩阵分析

```
┌──────────┬──────────┬──────────────┐
│  ① 格    │  ② 格    │              │
├──────────┼──────────┤  右侧大图    │
│  ③ 格    │  ④ 格    │  286px       │
└──────────┴──────────┴──────────────┘
```

#### 空间计算

```
左侧总宽    = 967 - 8×2 - 286 = 665px
每小格宽    = (665 - 8) ÷ 2 ≈ 328px
每小格高    = (580 - 8 - 10) ÷ 2 = 281px
右侧图高    = 580 - 10 = 570px（跨两行）
正文可用    ≈ 281 - 标题 22px - padding 16px = 243px → 约 65–90 字
```

#### CSS

```css
.layout-d {
  display: grid;
  grid-template-columns: 1fr 1fr 286px;
  grid-template-rows: repeat(2, 1fr);
  gap: 8px;
  height: 100%;
  padding-top: 10px;
}
.ld-right {
  grid-column: 3;
  grid-row: 1 / 3;
}
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

## 布局与视觉模板协同规则

| Tc 视觉模板特征 | Lc 对应约束 |
|---------------|------------|
| T2 编辑分割（左暗右亮双区） | 不使用 A/B/C/D，Lc 为左栏(280-320px) + 右栏(余量)，内部自由分行 |
| T3 终端代码（左侧边栏+右主区） | 不使用 A/B/C/D，Lc 为左边栏(160px) + 右主区，右主区内再分格 |
| T4 数据仪表（KPI横排+下方图表） | 优先 Lc：上方 KPI 固定高度行(90-110px) + 下方图表区 |
| T1/T5/T6/Tc 其他 | 自由选择或变形 A/B/C/D 基因 |

---

## 布局多样性检查

```
□ 已完成第零步，Lc 有完整定义（ASCII图 + grid CSS + 空间计算）？
□ Lc 的总行列高度精确计算，不超 580px？
□ 相同 Lc 结构未在报告内连续出现 3 次以上？
□ T2/T3 特殊模板使用了自定义列结构，未套用 A/B/C/D？
□ 10 页报告中使用了 ≥ 4 种不同结构的 Lc（包括变形）？
```
