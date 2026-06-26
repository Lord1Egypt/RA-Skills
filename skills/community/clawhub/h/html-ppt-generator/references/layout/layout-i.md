# 布局 I · 上方 KPI 条 + 下方双列内容

**适用：** 数据仪表板、业绩分析报告、关键指标监控
**结构基因：** 顶部多格指标行（固定高） + 底部双栏详细内容

---

## 结构图

```
┌─────┬─────┬─────┬─────┬─────┐
│KPI1 │KPI2 │KPI3 │KPI4 │KPI5 │  ← 90px
├──────────────────┬──────────────────┤
│  ① 左侧详细内容  │  ② 右侧图表/数据  │
│  (55%)           │  (45%)           │
└──────────────────┴──────────────────┘
```

> ⚠ KPI 格只放数字 + 标签，禁止长文字

---

## 空间计算

```
padding-top  = 8px
KPI 行高      = 90px
gap          = 10px
内容区高      = 580 - 8 - 90 - 10 = 472px
KPI 每格宽    = (967 - 8×4) ÷ 5 ≈ 187px
左列宽        = 967 × 55% ≈ 532px
右列宽        = 967 - 532 - 8 = 427px
正文可用      ≈ 472 - 标题 22px - padding 16px = 434px → 约 150–180 字
```

---

## CSS

```css
.layout-i {
  display: grid;
  grid-template-rows: 90px 1fr;
  gap: 10px;
  height: 100%;
  padding-top: 8px;
}
.li-kpi {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}
.li-content {
  display: grid;
  grid-template-columns: 55% 1fr;
  gap: 8px;
}
```

---

## 变形方向

- KPI 格数可改为 3/4/6（匹配实际指标数，列数等分）
- KPI 行高可调为 70–110px（指标内容多寡）
- 内容区可改为单列全宽（展示大型图表）
- 内容区可改为三列（各 ~320px，文字精简至 10.5px）
