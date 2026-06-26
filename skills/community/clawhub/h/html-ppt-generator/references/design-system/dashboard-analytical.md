# 数据仪表盘（Dashboard Analytical）

**气质：** 数据驱动、BI 报表、专业分析
**适用：** 数据分析、检测统计、趋势对比、ROI 计算
**推荐字体：** FP-3（Space Mono 数字 + IBM Plex Sans 正文）或 FP-6（Fraunces + Nunito）
**背景类型：** 亮色系（默认 `#f0f4f8`），可切换暗色变体
**主标题字号：** 14–18px 卡片标题，无超大展示标题
**页眉形式：** 左侧报告标题 + 右侧日期/页码，无装饰元素

---

## 布局规则

ct 区推荐结构：

```
上方 KPI 横排行（固定高度 90–110px，4–5 个 KPI 卡片）
下方图表/数据区（剩余高度，2 列或 3 列网格）
```

---

## CSS 片段

```css
/* 亮色版 */
body { background: #f0f4f8; color: #1e293b; }
/* 暗色变体：body { background: #0a0f1e; color: #e2e8f0; } */

/* KPI 卡片 */
.kpi {
  background: #fff; border-radius: 8px; padding: 12px 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,.08);
  border-top: 3px solid ACCENT;
}
.kpi-n     { font-size: 32px; font-weight: 800; letter-spacing: -1px; line-height: 1; }
.kpi-label { font-size: 9.5px; color: #9ca3af; text-transform: uppercase; letter-spacing:.5px; margin-top:2px; }
.kpi-trend { font-size: 11px; margin-top: 3px; }
.kpi-trend.up   { color: #10b981; }
.kpi-trend.down { color: #ef4444; }

/* 图表容器卡片 */
.chart-card { background: #fff; border-radius: 8px; padding: 14px 16px; box-shadow: 0 1px 3px rgba(0,0,0,.06); }
.chart-card-dark { background: #0f1629; border-radius: 8px; padding: 14px 16px; border: 1px solid rgba(255,255,255,0.06); }
.chart-title { font-size: 11.5px; font-weight: 700; color: #374151; margin-bottom: 8px; }

/* 数据表格 */
.data-table { width:100%; border-collapse:collapse; font-size: 10.5px; }
.data-table th { background:#f8fafc; color:#9ca3af; padding:5px 8px; text-align:left; font-weight:600; border-bottom:2px solid #e5e7eb; }
.data-table td { padding:5px 8px; border-bottom:1px solid #f1f5f9; color:#374151; }
```

---

## 亮色模式 CSS 变量覆盖

```css
/* 覆盖 04-color-font.md 中的 --bg / --card，--p 保留主题配色值 */
:root { --bg:#f0f4f8; --card:#fff; --t:#1e293b; --mt:#6b7280; --dt:#9ca3af; }
```
