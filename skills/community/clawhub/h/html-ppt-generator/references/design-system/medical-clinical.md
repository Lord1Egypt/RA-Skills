# 医疗临床（Medical Clinical）

**气质：** 医疗精准、临床数据、健康科学、专业可信
**适用：** 医疗报告、临床研究、健康数据分析、医院管理
**推荐字体：** FP-2（Playfair Display + Source Sans 3）或 FP-1（Syne + DM Sans）
**背景类型：** 亮色系（医白 #f7fafc），干净无菌感
**主标题字号：** 28–38px，无衬线或轻衬线，专业简洁
**页眉形式：** 左侧机构名 + 报告类型，右侧患者/研究编号 + 日期，蓝绿底线

---

## 设计特征

- **医疗青蓝**（#0891b2 / #0e7490）作为主强调色，专业可信
- 纯白/医白背景，干净无菌，信息优先
- 生命体征数字大而清晰（stat-num 突出）
- 卡片白底 + 青蓝顶线，无过度装饰
- 绿色用于正常/健康，红色用于异常/风险

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;600;700&display=swap');

body { background: #f7fafc; font-family: 'Source Sans 3','PingFang SC',sans-serif; color: #1a202c; }

/* 展示标题（专业清晰） */
.display-title {
  font-size: 34px; font-weight: 700; letter-spacing: -0.5px; line-height: 1.1;
  color: #0e7490;
}

/* 卡片（白色，青蓝顶线） */
.card {
  background: #ffffff;
  border: 1px solid rgba(14,116,144,0.12);
  border-top: 2px solid #0891b2;
  border-radius: 4px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow: 0 1px 4px rgba(14,116,144,0.08);
}

/* KPI / 生命体征数字 */
.stat-num {
  font-size: 44px; font-weight: 700; line-height: 1; letter-spacing: -1.5px;
  color: #0891b2;
}

/* 状态标签（正常/异常/注意） */
.status-tag {
  display: inline-flex; align-items: center; gap: 4px;
  border-radius: 100px; padding: 2px 8px;
  font-size: 9px; font-weight: 700; letter-spacing: 0.3px;
}
.status-tag.normal   { background: rgba(16,185,129,0.1); color: #059669; }
.status-tag.abnormal { background: rgba(239,68,68,0.1);  color: #dc2626; }
.status-tag.caution  { background: rgba(245,158,11,0.1); color: #d97706; }

/* 临床数据行 */
.clinical-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; padding: 3px 0;
  border-bottom: 1px solid rgba(14,116,144,0.07);
}
.clinical-row .label { color: #4a5568; }
.clinical-row .value { color: #0e7490; font-weight: 600; }
.clinical-row .range { color: #a0aec0; font-size: 9px; }

/* 进度条（健康/指标范围） */
.health-bar {
  height: 5px; border-radius: 5px;
  background: rgba(8,145,178,0.1);
}
.health-fill { height: 100%; border-radius: 5px;
  background: linear-gradient(90deg, #0e7490, #22d3ee); }
.health-fill.warn { background: linear-gradient(90deg, #d97706, #fbbf24); }
.health-fill.risk { background: linear-gradient(90deg, #dc2626, #f87171); }

/* 医疗数据表格 */
.med-table { width:100%; border-collapse:collapse; font-size:10px; }
.med-table th { background:#0e7490; color:#fff; padding:5px 8px; text-align:left; font-size:9px; font-weight:600; }
.med-table td { padding:4px 8px; border-bottom:1px solid rgba(14,116,144,0.08); color:#374151; }
.med-table td.normal   { color:#059669; }
.med-table td.abnormal { color:#dc2626; }
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #f7fafc;
  --card: #ffffff;
  --p:    #0891b2;
  --pm:   rgba(8,145,178,0.08);
  --bd:   rgba(14,116,144,0.12);
  --t:    #1a202c;
  --mt:   #4a5568;
  --dt:   #a0aec0;
}
/* 辅助语义色 */
/* --ok: #059669; --warn: #d97706; --err: #dc2626; */
```
