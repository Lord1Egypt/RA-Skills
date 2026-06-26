# 工程蓝图（Engineering Blueprint）

**气质：** 工程精密、技术图纸、严格规范、结构美学
**适用：** 工程报告、建筑规划、机械设计、项目技术文档
**推荐字体：** FP-3（Space Mono + IBM Plex Sans）
**背景类型：** 暗蓝系（深工程蓝 #0a1628），蓝图纸感
**主标题字号：** 32–40px，等宽或无衬线，精密感
**页眉形式：** 左侧图纸编号 + 标题，右侧比例/版本/日期，等宽字体

---

## 设计特征

- **蓝图蓝**（#1d4ed8 / #3b82f6）作为主强调色，工程蓝图质感
- 深蓝黑背景，模拟工程制图纸
- 网格线纹理（细白线，低透明度）模拟绘图板
- 等宽字体（Space Mono）显示参数与编号
- 卡片用蓝色细边 + 工程标注风格

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

body { background: #0a1628; font-family: 'IBM Plex Sans','PingFang SC',sans-serif; color: #cbd5e1; }

/* 蓝图网格纹理 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:
    linear-gradient(rgba(59,130,246,0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59,130,246,0.06) 1px, transparent 1px);
  background-size: 32px 32px;
}

/* 展示标题（蓝图精密感） */
.display-title {
  font-family: 'Space Mono','PingFang SC',monospace;
  font-size: 34px; font-weight: 700;
  letter-spacing: -0.5px; line-height: 1.05;
  color: #3b82f6;
  text-shadow: 0 0 20px rgba(59,130,246,0.3);
}

/* 卡片（蓝色细边，工程制图框） */
.card {
  background: rgba(15,23,42,0.9);
  border: 1px solid rgba(59,130,246,0.2);
  border-top: 1px solid rgba(59,130,246,0.5);
  border-radius: 2px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  position: relative;
}
/* 卡片角标（制图风格） */
.card::before {
  content:''; position:absolute; top:-1px; left:-1px;
  width:8px; height:8px;
  border-top:2px solid #3b82f6; border-left:2px solid #3b82f6;
}

/* KPI 数字（等宽蓝） */
.stat-num {
  font-family: 'Space Mono', monospace;
  font-size: 38px; font-weight: 700; line-height: 1; letter-spacing: -1px;
  color: #3b82f6;
}

/* 参数行（等宽标注） */
.param-row {
  display: flex; justify-content: space-between; align-items: center;
  font-family: 'Space Mono',monospace; font-size: 9px;
  color: #64748b; padding: 2px 0;
  border-bottom: 1px solid rgba(59,130,246,0.08);
}
.param-row .val { color: #93c5fd; font-weight: 700; }

/* 尺寸标注线 */
.dim-line {
  height: 1px; position: relative;
  background: rgba(59,130,246,0.4);
  margin: 6px 0;
}
.dim-line::before, .dim-line::after {
  content:''; position:absolute; top:-3px;
  width:1px; height:7px; background:#3b82f6;
}
.dim-line::before { left:0; }
.dim-line::after  { right:0; }

/* 规格标签 */
.spec-tag {
  display: inline-flex; align-items: center;
  background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.25);
  border-radius: 2px; padding: 2px 6px;
  font-family: 'Space Mono',monospace; font-size: 8px;
  color: #93c5fd; letter-spacing: 0.5px;
}

/* 进度条（工程进度） */
.eng-bar {
  height: 4px; background: rgba(59,130,246,0.1);
  border-radius: 0; border: 1px solid rgba(59,130,246,0.15);
}
.eng-fill { height: 100%; background: linear-gradient(90deg, #1d4ed8, #3b82f6); }
```

---

## CSS 变量

```css
:root {
  --bg:   #0a1628;
  --card: #0f172a;
  --p:    #3b82f6;
  --pm:   rgba(59,130,246,0.1);
  --bd:   rgba(59,130,246,0.2);
  --t:    #cbd5e1;
  --mt:   #94a3b8;
  --dt:   #475569;
}
```
