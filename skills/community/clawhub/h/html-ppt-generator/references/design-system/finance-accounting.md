# 财务会计（Finance Accounting）

**气质：** 精准规范、数字权威、财务专业、报表感
**适用：** 财务报告、会计分析、预算报表、审计摘要
**推荐字体：** FP-4（Cormorant Garamond + Outfit）或 FP-2（Playfair + Source Sans）
**背景类型：** 亮色系（账本白 #fafafa），数字优先，简洁规整
**主标题字号：** 28–38px，衬线或无衬线，数字对齐严格
**页眉形式：** 左侧公司名 + 报告期，右侧编制人/审核，底部深线分割

---

## 设计特征

- **账本深绿**（#065f46 / #059669）作为主强调色，财务专业感
- 白色/账本白背景，数字信息密集，行高适当
- 衬线大标题展示关键财务指标
- 卡片方正无圆角，绿色顶线，表格感强
- 正数用绿色，负数/亏损用红色（语义明确）

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Cormorant+Garamond:wght@600;700;800&display=swap');

body { background: #fafafa; font-family: 'Outfit','PingFang SC',sans-serif; color: #111827; }

/* 展示标题（账务权威） */
.display-title {
  font-family: 'Cormorant Garamond','Noto Serif SC',serif;
  font-size: 38px; font-weight: 800;
  letter-spacing: -1px; line-height: 1.0;
  color: #065f46;
}

/* 报告期标注 */
.period-label {
  font-size: 9px; font-weight: 600;
  letter-spacing: 1.5px; text-transform: uppercase;
  color: #059669; opacity: 0.9;
}

/* 卡片（方正，绿色顶线） */
.card {
  background: #ffffff;
  border: 1px solid rgba(6,95,70,0.12);
  border-top: 2px solid #065f46;
  border-radius: 0; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

/* KPI 财务数字 */
.stat-num {
  font-family: 'Cormorant Garamond', serif;
  font-size: 42px; font-weight: 800; line-height: 1; letter-spacing: -1px;
  color: #065f46;
}

/* 正/负值色彩语义 */
.positive { color: #059669; }
.negative { color: #dc2626; }

/* 财务数据行（账单感） */
.account-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; padding: 3px 0;
  border-bottom: 1px solid rgba(6,95,70,0.06);
}
.account-row .item  { color: #374151; }
.account-row .amount { font-family: 'Outfit',monospace; font-weight: 600; color: #065f46; }
.account-row.total  { border-top: 1px solid rgba(6,95,70,0.3); font-weight:700; }

/* 财务表格 */
.fin-table { width:100%; border-collapse:collapse; font-size:10px; }
.fin-table th { background:#065f46; color:#fff; padding:5px 8px; text-align:left; font-size:9px; font-weight:600; letter-spacing:0.5px; }
.fin-table td { padding:4px 8px; border-bottom:1px solid rgba(6,95,70,0.06); color:#374151; text-align:right; }
.fin-table td.label { text-align:left; color:#111827; }
.fin-table td.pos   { color:#059669; }
.fin-table td.neg   { color:#dc2626; }
.fin-table tr.subtotal td { font-weight:600; border-top:1px solid rgba(6,95,70,0.2); background:rgba(6,95,70,0.03); }

/* 进度条（预算执行率） */
.budget-bar {
  height: 4px; background: rgba(6,95,70,0.1); border-radius: 0;
}
.budget-fill { height: 100%; background: linear-gradient(90deg, #065f46, #059669); }
.budget-fill.over { background: linear-gradient(90deg, #dc2626, #f87171); }
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #fafafa;
  --card: #ffffff;
  --p:    #065f46;
  --pm:   rgba(6,95,70,0.07);
  --bd:   rgba(6,95,70,0.12);
  --t:    #111827;
  --mt:   #374151;
  --dt:   #9ca3af;
}
/* 语义色 */
/* --ok:  #059669; --err: #dc2626; */
```
