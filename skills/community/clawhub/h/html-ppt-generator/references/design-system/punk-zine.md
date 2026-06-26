# 朋克杂志（Punk Zine）

**气质：** DIY精神、手撕拼贴、无政府主义、地下文化
**适用：** 亚文化报告、独立音乐、街头艺术、反叛创意提案
**推荐字体：** 系统字体故意"丑"用（Impact + Space Mono）
**背景类型：** 亮色系（报纸黄 #f5f0d8 / 复印机白），故意粗糙
**主标题字号：** 60–80px Impact 全大写，故意不对齐，随机旋转
**页眉形式：** 手写风格标注，剪切粘贴感，油墨印章，无固定位置

---

## 设计特征

- **油墨黑**（#0a0a0a）+ **叛逆红**（#e11d48）双色，三色印刷机感
- 报纸黄/复印白背景，颗粒质感
- 文字随机 ±3° 旋转，故意不水平
- 边框用"手撕"效果（不规则 clip-path）
- 删除线、圈注、箭头手绘感装饰

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');

body {
  background: #f5f0d8;
  font-family: Impact,'Arial Black','PingFang SC',sans-serif;
  color: #0a0a0a;
}

/* 复印机颗粒噪点 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:1;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23n)' opacity='0.07'/%3E%3C/svg%3E");
  mix-blend-mode: multiply;
}

/* 展示标题（冲击，故意不居中） */
.display-title {
  font-family: Impact,'Arial Black',sans-serif;
  font-size: 72px; font-weight: 900; text-transform: uppercase;
  letter-spacing: -2px; line-height: 0.88;
  color: #0a0a0a;
  transform: rotate(-1.5deg);
  display: inline-block;
}
.display-title .slash { color: #e11d48; }

/* 涂鸦下划线 */
.display-title::after {
  content:''; display:block; height:6px;
  background: #e11d48; margin-top:4px;
  transform: rotate(0.8deg) skewX(-3deg);
}

/* 卡片（手撕边缘，不对称） */
.card {
  background: rgba(255,255,255,0.85);
  border: 2px solid #0a0a0a;
  border-radius: 0; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  transform: rotate(0.5deg);
  box-shadow: 4px 4px 0 #0a0a0a;
}

/* KPI（冲击大字，叛逆红） */
.stat-num {
  font-family: Impact,sans-serif;
  font-size: 56px; font-weight: 900; line-height: 1; letter-spacing: -2px;
  color: #e11d48;
  -webkit-text-stroke: 2px #0a0a0a;
}

/* 删除线（审查感） */
.censored {
  background: #0a0a0a; color: #0a0a0a;
  user-select: none; display: inline;
}

/* 油墨印章标签 */
.stamp-tag {
  display: inline-flex; align-items: center;
  border: 3px solid currentColor; padding: 2px 8px;
  font-family: Impact,sans-serif;
  font-size: 11px; font-weight: 900; letter-spacing: 2px;
  text-transform: uppercase; transform: rotate(-3deg);
  opacity: 0.85;
}
.stamp-tag.red   { color: #e11d48; }
.stamp-tag.black { color: #0a0a0a; }
.stamp-tag.ok    { color: #16a34a; }

/* 手绘箭头（::after 伪元素） */
.arrow-note {
  font-size: 10px; color: #e11d48;
  font-family: 'Space Mono',monospace;
  transform: rotate(-2deg);
  display: inline-block;
}
.arrow-note::before { content: '→ '; font-size: 12px; }

/* 进度条（手绘格子感） */
.zine-bar {
  height: 12px;
  border: 2px solid #0a0a0a;
  background: repeating-linear-gradient(
    90deg, transparent 0, transparent 7px, rgba(0,0,0,0.1) 7px, rgba(0,0,0,0.1) 8px
  );
}
.zine-fill { height: 100%; background: #e11d48; }

/* 拼贴数据行 */
.zine-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10px; padding: 3px 0; font-family: 'Space Mono',monospace;
  border-bottom: 2px solid #0a0a0a;
}
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #f5f0d8;
  --card: rgba(255,255,255,0.85);
  --p:    #e11d48;
  --pm:   rgba(225,29,72,0.08);
  --bd:   #0a0a0a;
  --t:    #0a0a0a;
  --mt:   #374151;
  --dt:   #9ca3af;
}
```
