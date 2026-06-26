# 日式极简（Japanese Minimalism）

**气质：** 侘寂美学、呼吸感、克制留白、东方哲学
**适用：** 高端品牌报告、文化策展、生活方式、极简产品发布
**推荐字体：** FP-6（Fraunces + Nunito）或 FP-2（Playfair Display + Source Sans）
**背景类型：** 亮色系（和纸白 #f8f6f1 / 轻苔灰 #f2f0eb），质感纸张
**主标题字号：** 28–44px，字间距宽松正，绝不拥挤
**页眉形式：** 极简单线，左侧汉字或英文标题，右侧小号灰色编号，大量留白

---

## 设计特征

- **墨色**（#1a1714）+ **朱砂红**（#c0392b / #991b1b）极简双色
- 和纸质感背景，颗粒噪点纹理
- 字距 0.05–0.1em 宽松排版，绝不堆砌
- 卡片极少装饰，仅用细线或颜色区分
- 负空间（留白）作为设计主体，而非填充物

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,700;1,9..144,900&family=Nunito:wght@300;400&display=swap');

body {
  background: #f8f6f1;
  font-family: 'Nunito','Hiragino Kaku Gothic ProN','PingFang SC',sans-serif;
  color: #1a1714; letter-spacing: 0.04em;
}

/* 和纸噪点纹理 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  opacity:0.35;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.15'/%3E%3C/svg%3E");
}

/* 展示标题（宽松克制） */
.display-title {
  font-family: 'Fraunces','Noto Serif SC',serif;
  font-size: 42px; font-weight: 700; font-style: italic;
  letter-spacing: -0.5px; line-height: 1.1;
  color: #1a1714;
}

/* 朱砂强调字 */
.accent-word { color: #991b1b; }

/* 卡片（极简，底线区分） */
.card {
  background: transparent;
  border: none; border-top: 1px solid rgba(26,23,20,0.2);
  border-radius: 0; padding: 10px 0;
  display: flex; flex-direction: column; gap: 8px;
}

/* KPI 数字（克制墨黑） */
.stat-num {
  font-family: 'Fraunces', serif;
  font-size: 48px; font-weight: 700; font-style: italic;
  line-height: 1; color: #1a1714; letter-spacing: -1px;
}

/* 极细分割线（和纸笔触感） */
.washi-rule {
  height: 1px; border: none;
  background: rgba(26,23,20,0.15); margin: 8px 0;
}

/* 注记/说明（小字宽松） */
.notation {
  font-size: 9.5px; color: rgba(26,23,20,0.45);
  letter-spacing: 0.08em; line-height: 1.6;
}

/* 朱砂标注点 */
.beni-dot {
  width: 5px; height: 5px; border-radius: 50%;
  background: #991b1b; flex-shrink: 0;
}

/* 极简数据行 */
.zen-row {
  display: flex; justify-content: space-between; align-items: baseline;
  font-size: 10.5px; padding: 5px 0;
  border-bottom: 1px solid rgba(26,23,20,0.08);
  letter-spacing: 0.05em;
}
.zen-row .label { color: rgba(26,23,20,0.5); font-weight: 300; }
.zen-row .value { color: #1a1714; font-weight: 700; }

/* 极简进度（细线仅） */
.wabi-bar {
  height: 1px; background: rgba(26,23,20,0.15);
}
.wabi-fill { height: 100%; background: #1a1714; }
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #f8f6f1;
  --card: transparent;
  --p:    #1a1714;
  --pm:   rgba(26,23,20,0.06);
  --bd:   rgba(26,23,20,0.15);
  --t:    #1a1714;
  --mt:   rgba(26,23,20,0.55);
  --dt:   rgba(26,23,20,0.35);
}
/* --beni: #991b1b; (朱砂红，唯一强调色) */
```
