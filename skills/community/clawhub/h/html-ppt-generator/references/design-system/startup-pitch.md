# 创业融资（Startup Pitch）

**气质：** 创业激情、增长故事、VC Pitch Deck、用户规模感
**适用：** 融资路演、创业报告、产品发布、增长分析
**推荐字体：** FP-1（Syne 800 + DM Sans）
**背景类型：** 纯净亮白（#ffffff），极高对比，内容聚焦
**主标题字号：** 52–72px Syne 超大，字距极紧，冲击力最大化
**页眉形式：** 左侧大号轮次标记（SERIES A / SEED），右侧日期，极简

---

## 设计特征

- **品牌黑**（#0a0a0a）+ 可切换品牌强调色（默认：电光蓝 #2563eb）
- 纯白背景，最大留白，内容极度聚焦
- 超大 KPI 数字压迫感，增长数据一目了然
- 箭头 / 趋势符号（↑↓）与数字混排
- 增长曲线图为核心视觉，卡片极简无边框

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

body { background: #ffffff; font-family: 'DM Sans','PingFang SC',sans-serif; color: #0a0a0a; }

/* 融资轮次标记 */
.round-badge {
  font-family: 'Syne',sans-serif;
  font-size: 10px; font-weight: 800; letter-spacing: 3px;
  text-transform: uppercase; color: #2563eb;
  border: 1.5px solid #2563eb;
  border-radius: 4px; padding: 3px 8px; display: inline-block;
}

/* 展示标题（Pitch 大字） */
.display-title {
  font-family: 'Syne','PingFang SC',sans-serif;
  font-size: 62px; font-weight: 800;
  letter-spacing: -3px; line-height: 0.9;
  color: #0a0a0a;
}

/* 增长数字（超大蓝色） */
.stat-num {
  font-family: 'Syne', sans-serif;
  font-size: 56px; font-weight: 800; line-height: 1; letter-spacing: -2px;
  color: #2563eb;
}

/* 增长趋势符号 */
.trend-up   { color: #16a34a; font-size: 11px; font-weight: 700; }
.trend-down { color: #dc2626; font-size: 11px; font-weight: 700; }

/* 卡片（极简，微灰底） */
.card {
  background: #f8faff;
  border: none;
  border-radius: 8px; padding: 12px 16px;
  display: flex; flex-direction: column; gap: 6px;
}

/* 指标行 */
.metric-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 4px 0; border-bottom: 1px solid rgba(0,0,0,0.06); font-size: 10.5px;
}
.metric-row .label { color: #6b7280; }
.metric-row .value { font-weight: 700; color: #0a0a0a; }
.metric-row .delta { font-size: 9px; font-weight: 700; }

/* 里程碑时间线点 */
.milestone-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: #2563eb; flex-shrink: 0;
}

/* 进度/增长条（蓝色渐变） */
.growth-bar {
  height: 5px; border-radius: 5px;
  background: linear-gradient(90deg, #1d4ed8, #2563eb, #60a5fa);
}

/* 竞争优势标签 */
.advantage-tag {
  display: inline-flex; align-items: center;
  background: rgba(37,99,235,0.08); border: none;
  border-radius: 100px; padding: 3px 10px;
  font-size: 9px; font-weight: 700; color: #2563eb;
  letter-spacing: 0.3px;
}
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #ffffff;
  --card: #f8faff;
  --p:    #2563eb;
  --pm:   rgba(37,99,235,0.08);
  --bd:   rgba(37,99,235,0.15);
  --t:    #0a0a0a;
  --mt:   #4b5563;
  --dt:   #9ca3af;
}
/* 替换品牌色只需修改 --p 和相关 rgba */
```
