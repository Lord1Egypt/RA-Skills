# 国际主义（Swiss International）

**气质：** 瑞士国际主义、网格系统、理性秩序、无装饰功能主义
**适用：** 品牌手册、企业年报、系统规范、设计指南
**推荐字体：** 系统无衬线（DM Sans / IBM Plex Sans）严格网格
**背景类型：** 纯白（#ffffff），无任何纹理，网格即秩序
**主标题字号：** 36–52px 无衬线 700，字距紧，左对齐绝不居中
**页眉形式：** 左对齐章节编号 + 标题，右侧项目名，严格基线对齐

---

## 设计特征

- **原色三角**（#dc2626红 / #2563eb蓝 / #ca8a04黄）按场景取其一，绝不混用
- 纯白背景，网格线即设计（可见或不可见）
- 无任何装饰性元素，形式完全服从功能
- 文字块左对齐，用字号层级区分信息权重
- 进度条/色块用实色，无渐变

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&display=swap');

body { background: #ffffff; font-family: 'DM Sans','Helvetica Neue',sans-serif; color: #0a0a0a; }

/* 展示标题（功能主义，绝不花哨） */
.display-title {
  font-size: 48px; font-weight: 700;
  letter-spacing: -2px; line-height: 0.95;
  color: #0a0a0a; text-align: left;
}

/* 章节编号（大号灰色，网格定位） */
.section-num {
  font-size: 72px; font-weight: 700; line-height: 1;
  color: rgba(0,0,0,0.07); letter-spacing: -3px;
  position: absolute; right: 0; top: 0;
}

/* 强调色（只用一种原色） */
.accent-primary { color: #dc2626; }   /* 红版 */
.accent-blue    { color: #2563eb; }   /* 蓝版 */
.accent-yellow  { color: #ca8a04; }   /* 黄版 */

/* 卡片（无任何装饰，仅边距区分） */
.card {
  background: #f4f4f4;
  border: none; border-radius: 0;
  padding: 12px 14px;
  display: flex; flex-direction: column; gap: 6px;
}

/* KPI 数字（功能主义大数） */
.stat-num {
  font-size: 52px; font-weight: 700; line-height: 1; letter-spacing: -2.5px;
  color: #0a0a0a;
}

/* 实色进度条（无渐变） */
.swiss-bar { height: 4px; background: #e5e5e5; }
.swiss-fill { height: 100%; background: #0a0a0a; }
.swiss-fill.red    { background: #dc2626; }
.swiss-fill.blue   { background: #2563eb; }
.swiss-fill.yellow { background: #ca8a04; }

/* 数据表格（极简） */
.swiss-table { width:100%; border-collapse:collapse; font-size:10px; }
.swiss-table th { border-bottom:2px solid #0a0a0a; padding:4px 8px; text-align:left; font-weight:700; font-size:9px; letter-spacing:1px; text-transform:uppercase; }
.swiss-table td { padding:4px 8px; border-bottom:1px solid #e5e5e5; }

/* 分割（纯黑线，无透明度） */
.swiss-rule { height:2px; background:#0a0a0a; margin:8px 0; }
.swiss-rule.thin { height:1px; background:#e5e5e5; }
```

---

## CSS 变量

```css
:root {
  --bg:   #ffffff;
  --card: #f4f4f4;
  --p:    #0a0a0a;
  --pm:   #f4f4f4;
  --bd:   #e5e5e5;
  --t:    #0a0a0a;
  --mt:   #4a4a4a;
  --dt:   #9a9a9a;
}
/* 原色变体：用 --accent: #dc2626 / #2563eb / #ca8a04 其中之一 */
```
