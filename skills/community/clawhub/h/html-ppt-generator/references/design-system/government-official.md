# 政府公务（Government Official）

**气质：** 庄重权威、党政机关、正式公文
**适用：** 政府报告、政策解读、行政汇报、规划文件
**推荐字体：** FP-2（Playfair Display + Source Sans 3）或无衬线简洁方案
**背景类型：** 亮色系（纸白/浅灰）为主，深蓝封面变体
**主标题字号：** 20–28px 深蓝，规整庄重，不用渐变裁剪
**页眉形式：** 左侧机构名+文件类型，右侧文号/日期，底部红线分割

---

## 设计特征

- **深蓝**（#1e3a8a）+ **中国红**（#dc2626）双主色，庄重权威
- 亮色背景（#f5f5f0），接近公文纸白感
- 无装饰纹理，严格对齐，内容优先
- 红色横线用于节点标注和标题强调
- 表格多，数据清晰，无动效感

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;600;700&display=swap');

body { background: #f5f5f0; font-family: 'Source Sans 3','PingFang SC','Microsoft YaHei',sans-serif; color: #1a1a1a; }

/* 展示标题（深蓝庄重） */
.display-title {
  font-size: 26px; font-weight: 700; letter-spacing: 1px;
  color: #1e3a8a; line-height: 1.2;
  border-left: 4px solid #dc2626; padding-left: 12px;
}

/* 卡片（极简白色，细边） */
.card {
  background: #ffffff;
  border: 1px solid #dde0e8;
  border-top: 2px solid #1e3a8a;
  border-radius: 2px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

/* 红色标注横线 */
.gov-section-bar {
  height:2px;
  background: linear-gradient(90deg, #dc2626 40%, transparent);
  margin-bottom: 8px;
}

/* KPI 数字（深蓝权威） */
.stat-num {
  font-size: 36px; font-weight: 700; line-height: 1;
  color: #1e3a8a; letter-spacing: -1px;
}

/* 公文表格 */
.gov-table { width:100%; border-collapse:collapse; font-size:10.5px; }
.gov-table th { background:#1e3a8a; color:#fff; padding:5px 8px; text-align:left; font-weight:600; font-size:9.5px; }
.gov-table td { padding:5px 8px; border:1px solid #dde0e8; color:#374151; }
.gov-table tr:nth-child(even) td { background:#f0f4f8; }

/* 政策要点列表 */
.policy-item {
  display:flex; gap:8px; padding:5px 0;
  border-bottom:1px solid rgba(30,58,138,0.08);
}
.policy-num { color:#dc2626; font-weight:700; font-size:11px; flex-shrink:0; width:18px; }
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #f5f5f0;
  --card: #ffffff;
  --p:    #1e3a8a;
  --pm:   rgba(30,58,138,0.08);
  --bd:   #dde0e8;
  --t:    #1a1a1a;
  --mt:   #4b5563;
  --dt:   #9ca3af;
}
/* 辅助强调色 */
/* --accent-red: #dc2626; */
```
