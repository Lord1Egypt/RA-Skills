# 战略咨询（Consultant Strategy）

**气质：** 咨询框架感、战略高度、麦肯锡风格、专业精炼
**适用：** 战略报告、咨询提案、管理分析、商业框架展示
**推荐字体：** FP-1（Syne + DM Sans）或 FP-2（Playfair + Source Sans）
**背景类型：** 亮色系（冷白 #f8f9fc），极简精炼
**主标题字号：** 28–40px，无衬线粗体，左对齐，精炼权威
**页眉形式：** 左侧项目代号 + 章节名，右侧日期 + 机构，深蓝底线分割

---

## 设计特征

- **深海军蓝**（#0f2d5c）+ **咨询蓝**（#1a56db）双层蓝色系，专业精炼
- 冷白背景，大量留白，内容节奏快准狠
- 矩阵框架图多，2×2、SWOT、BCG 等战略工具感
- 卡片顶线 + 编号角标，框架感十足
- 数据条用蓝色渐变，清晰强调

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

body { background: #f8f9fc; font-family: 'DM Sans','PingFang SC',sans-serif; color: #0f172a; }

/* 展示标题（咨询大标题） */
.display-title {
  font-family: 'Syne','PingFang SC',sans-serif;
  font-size: 36px; font-weight: 800;
  letter-spacing: -1px; line-height: 1.1;
  color: #0f2d5c;
}

/* 洞察副标题 */
.insight-label {
  font-family: 'DM Sans',sans-serif;
  font-size: 9px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  color: #1a56db; opacity: 0.9;
}

/* 卡片（海军蓝顶线 + 编号角标） */
.card {
  background: #ffffff;
  border: 1px solid rgba(15,45,92,0.1);
  border-top: 2px solid #0f2d5c;
  border-radius: 3px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow: 0 1px 6px rgba(15,45,92,0.06);
}

/* 序号/框架编号 */
.framework-num {
  font-family: 'Syne',sans-serif;
  font-size: 9px; font-weight: 800;
  color: #1a56db; letter-spacing: 1px;
  text-transform: uppercase;
}

/* KPI 数字（海军蓝） */
.stat-num {
  font-family: 'Syne', sans-serif;
  font-size: 40px; font-weight: 800; line-height: 1; letter-spacing: -1.5px;
  color: #0f2d5c;
}

/* 战略要点列表 */
.strategy-item {
  display: flex; gap: 8px; padding: 4px 0;
  border-bottom: 1px solid rgba(15,45,92,0.07);
  font-size: 10.5px; align-items: flex-start;
}
.strategy-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: #1a56db; flex-shrink: 0; margin-top: 3px;
}

/* 数据对比条 */
.strategy-bar {
  height: 4px; border-radius: 2px;
  background: linear-gradient(90deg, #0f2d5c, #1a56db, #60a5fa);
}

/* 咨询横线分割 */
.consult-divider {
  height: 1px; border: none;
  background: linear-gradient(90deg, #0f2d5c 20%, rgba(15,45,92,0.2) 60%, transparent);
  margin: 6px 0;
}

/* 数据表格（咨询报告风格） */
.consult-table { width:100%; border-collapse:collapse; font-size:10px; }
.consult-table th { background:#0f2d5c; color:#fff; padding:5px 8px; text-align:left; font-weight:600; font-size:9px; letter-spacing:0.5px; text-transform:uppercase; }
.consult-table td { padding:5px 8px; border-bottom:1px solid rgba(15,45,92,0.08); color:#374151; }
.consult-table tr:hover td { background:rgba(26,86,219,0.04); }
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #f8f9fc;
  --card: #ffffff;
  --p:    #0f2d5c;
  --pm:   rgba(15,45,92,0.07);
  --bd:   rgba(15,45,92,0.1);
  --t:    #0f172a;
  --mt:   #374151;
  --dt:   #9ca3af;
}
/* 辅助色 */
/* --accent-blue: #1a56db; (咨询蓝，链接/强调) */
```
