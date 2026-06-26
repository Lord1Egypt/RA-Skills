# 创意工作室（Creative Studio）

**气质：** 设计感强、创意驱动、品牌美学、视觉实验
**适用：** 设计报告、品牌策略、创意提案、视觉调研
**推荐字体：** FP-1（Syne 800 + DM Sans）或 FP-6（Fraunces + Nunito）
**背景类型：** 近黑暖灰（#111110），高对比，留白大胆
**主标题字号：** 52–72px 超大展示标题，字距极紧，视觉突破
**页眉形式：** 大号编号 + 简洁标题，右侧品牌/客户名，极简分割

---

## 设计特征

- **亮粉紫**（#d946ef / #a855f7）或用户自定义品牌色作为强调色
- 近黑背景，最大化视觉对比
- 超大字号展示标题，字间距 -3px 极紧排版
- 卡片近无边框，背景微差，高度留白感
- 彩色标记点/色块用于视觉节奏

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

body { background: #111110; font-family: 'DM Sans','PingFang SC',sans-serif; color: #e8e4dc; }

/* 展示标题（超大紧排，视觉冲击） */
.display-title {
  font-family: 'Syne','PingFang SC',sans-serif;
  font-size: 64px; font-weight: 800;
  letter-spacing: -3px; line-height: 0.92;
  color: #e8e4dc;
}

/* 强调色词（粉紫渐变） */
.accent-word {
  background: linear-gradient(135deg, #d946ef, #a855f7);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 卡片（微差背景，无边框） */
.card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 8px; padding: 12px 16px;
  display: flex; flex-direction: column; gap: 6px;
  backdrop-filter: blur(4px);
}

/* KPI 数字（超大 Syne） */
.stat-num {
  font-family: 'Syne', sans-serif;
  font-size: 52px; font-weight: 800; line-height: 1; letter-spacing: -2px;
  background: linear-gradient(135deg, #d946ef, #a855f7);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 创意标签（圆角全满，彩色） */
.creative-tag {
  display: inline-flex; align-items: center; gap: 4px;
  border-radius: 100px; padding: 3px 10px;
  font-size: 9px; font-weight: 700; letter-spacing: 0.5px;
  text-transform: uppercase;
}
.creative-tag.pink   { background: rgba(217,70,239,0.15); color: #d946ef; }
.creative-tag.purple { background: rgba(168,85,247,0.15); color: #a855f7; }
.creative-tag.amber  { background: rgba(245,158,11,0.15); color: #f59e0b; }
.creative-tag.cyan   { background: rgba(6,182,212,0.15);  color: #06b6d4; }

/* 色块装饰（视觉节奏） */
.color-dot {
  display: inline-block; border-radius: 50%;
  width: 8px; height: 8px; flex-shrink: 0;
}

/* 进度条（渐变创意感） */
.creative-bar {
  height: 3px; border-radius: 3px;
  background: linear-gradient(90deg, #d946ef, #a855f7, #6366f1);
}

/* 分割线（极细，低对比） */
.studio-divider {
  height: 1px; border: none;
  background: rgba(255,255,255,0.08); margin: 6px 0;
}

/* 引用框（品牌洞察） */
.insight-box {
  background: rgba(217,70,239,0.06);
  border-left: 2px solid rgba(217,70,239,0.5);
  padding: 6px 10px; font-size: 11px;
  font-style: italic; color: #c4bdb4;
}
```

---

## CSS 变量

```css
:root {
  --bg:   #111110;
  --card: rgba(255,255,255,0.04);
  --p:    #d946ef;
  --pm:   rgba(217,70,239,0.12);
  --bd:   rgba(255,255,255,0.08);
  --t:    #e8e4dc;
  --mt:   #a09b94;
  --dt:   #5a5650;
}
/* 辅助色 */
/* --p2: #a855f7; (紫，双主色可搭配) */
```
