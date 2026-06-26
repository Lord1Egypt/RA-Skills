# 科学实验室（Science Lab）

**气质：** 实验精密、数据严谨、科研过程、测量可重复
**适用：** 实验报告、科学数据、检测分析、研发总结
**推荐字体：** FP-3（Space Mono + IBM Plex Sans）
**背景类型：** 亮色系（实验室白 #f8fafb），冷色调，干净精确
**主标题字号：** 28–36px，等宽或无衬线，数值精确感
**页眉形式：** 左侧实验编号（EXP-2024-001），右侧样本量/检测日期，等宽字体

---

## 设计特征

- **精密蓝青**（#0e7490 / #0891b2）+ **数据紫**（#7c3aed）双主色
- 冷白背景，类似实验室灯光感
- 等宽字体显示测量值、误差范围（±）、置信区间
- 表格密集，带单位标注，数据对齐精确
- 误差条/置信区间可视化

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

body { background: #f8fafb; font-family: 'IBM Plex Sans','PingFang SC',sans-serif; color: #0f172a; }

/* 展示标题（精密实验标题） */
.display-title {
  font-family: 'IBM Plex Sans','PingFang SC',sans-serif;
  font-size: 32px; font-weight: 600;
  letter-spacing: -0.5px; line-height: 1.15;
  color: #0e7490;
}

/* 实验编号/样品标签 */
.exp-id {
  font-family: 'Space Mono',monospace;
  font-size: 9px; color: #7c3aed;
  letter-spacing: 1px; background: rgba(124,58,237,0.08);
  padding: 2px 6px; border-radius: 2px;
}

/* 卡片（实验台白，精密细边） */
.card {
  background: #ffffff;
  border: 1px solid rgba(14,116,144,0.15);
  border-top: 2px solid #0891b2;
  border-radius: 2px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
}

/* 测量值（等宽精确） */
.stat-num {
  font-family: 'Space Mono', monospace;
  font-size: 36px; font-weight: 700; line-height: 1;
  color: #0e7490; letter-spacing: -0.5px;
}
.stat-unit { font-family: 'Space Mono',monospace; font-size: 12px; color: #6b7280; }
.stat-error { font-family: 'Space Mono',monospace; font-size: 11px; color: #94a3b8; }

/* 数据表格（实验室记录） */
.lab-table { width:100%; border-collapse:collapse; font-size:9.5px; }
.lab-table th {
  background:#0e7490; color:#fff; padding:4px 8px;
  font-family:'Space Mono',monospace; font-size:8px; letter-spacing:0.5px;
  text-align:left; font-weight:700;
}
.lab-table td { padding:3px 8px; border-bottom:1px solid rgba(14,116,144,0.08); font-family:'Space Mono',monospace; }
.lab-table td.val { color:#0e7490; font-weight:700; }
.lab-table td.err { color:#7c3aed; }
.lab-table td.pass { color:#16a34a; }
.lab-table td.fail { color:#dc2626; }

/* 置信区间条 */
.confidence-bar {
  height: 8px; position: relative; background: rgba(14,116,144,0.1);
  border-radius: 0; margin: 2px 0;
}
.confidence-range {
  position: absolute; height: 100%;
  background: rgba(14,116,144,0.4);
}
.confidence-point {
  position: absolute; width: 2px; height: 100%;
  background: #0e7490; top: 0;
}

/* 参数行 */
.param-row {
  display:flex; justify-content:space-between; font-size:9.5px;
  font-family:'Space Mono',monospace; padding:2px 0;
  border-bottom:1px dotted rgba(14,116,144,0.15);
}
.param-row .key { color:#64748b; }
.param-row .val { color:#0e7490; font-weight:700; }
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #f8fafb;
  --card: #ffffff;
  --p:    #0891b2;
  --pm:   rgba(8,145,178,0.08);
  --bd:   rgba(14,116,144,0.15);
  --t:    #0f172a;
  --mt:   #475569;
  --dt:   #94a3b8;
}
/* --p2: #7c3aed; (数据紫，误差/辅助量) */
```
