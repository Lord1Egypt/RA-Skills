# 视觉系哥特萝莉（Visual Kei Gothic）

**气质：** 哥特萝莉、视觉系摇滚、黑蕾丝、暗玫瑰、优雅黑暗
**适用：** 暗系二次元、视觉系音乐、哥特美学、暗黑奇幻
**推荐字体：** FP-2（Playfair Display + Source Sans 3），衬线哥特感
**背景类型：** 极暗色系（枯玫瑰黑 #0d080e），暗紫血红光晕
**主标题字号：** 38–52px Playfair 斜体，蕾丝边描边，优雅黑暗
**页眉形式：** 黑蕾丝边框纹理，标题居中，两侧十字架/玫瑰装饰，哥特风

---

## 设计特征

- **枯玫瑰**（#881337 / #be123c）+ **哥特紫**（#6b21a8 / #a855f7）双主色
- 极暗紫黑背景，暗血红径向光晕
- 蕾丝纹理（CSS border-image / repeating-gradient 模拟）
- 衬线斜体大标题，优雅而哥特
- 玫瑰花瓣落点、蝴蝶结等装饰符号（Unicode）

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,700;1,900&family=Source+Sans+3:wght@300;400;600&display=swap');

body { background: #0d080e; font-family: 'Source Sans 3','PingFang SC',sans-serif; color: #e8d5d8; }

/* 暗血红光晕 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 50% 30%, rgba(136,19,55,0.15) 0%, transparent 55%),
    radial-gradient(ellipse at 20% 80%, rgba(107,33,168,0.1)  0%, transparent 40%),
    radial-gradient(ellipse at 80% 70%, rgba(136,19,55,0.08)  0%, transparent 35%);
}

/* 蕾丝纹理（顶部装饰） */
body::after {
  content:''; position:fixed; top:0; left:0; right:0; height:3px;
  pointer-events:none; z-index:1;
  background: repeating-linear-gradient(
    90deg,
    #881337 0, #881337 3px, transparent 3px, transparent 6px,
    #6b21a8 6px, #6b21a8 9px, transparent 9px, transparent 12px
  );
  opacity: 0.5;
}

/* 展示标题（哥特斜体衬线） */
.display-title {
  font-family: 'Playfair Display','Noto Serif SC',serif;
  font-size: 46px; font-weight: 900; font-style: italic;
  letter-spacing: 0px; line-height: 1.05;
  color: #e8d5d8;
  text-shadow:
    0 0 30px rgba(136,19,55,0.5),
    0 2px 8px rgba(0,0,0,0.8);
}
.display-title .rose { color: #be123c; }

/* 哥特蕾丝卡片 */
.card {
  background: rgba(13,8,14,0.92);
  border: 1px solid rgba(136,19,55,0.3);
  border-top: 1px solid rgba(190,18,60,0.5);
  border-radius: 2px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow:
    0 0 24px rgba(136,19,55,0.08),
    inset 0 0 20px rgba(0,0,0,0.4);
  position: relative;
}
/* 卡片蕾丝角落 */
.card::before {
  content: '✦'; position: absolute; top: 4px; left: 8px;
  color: rgba(136,19,55,0.4); font-size: 8px;
}
.card::after {
  content: '✦'; position: absolute; top: 4px; right: 8px;
  color: rgba(107,33,168,0.4); font-size: 8px;
}

/* KPI（暗玫瑰红） */
.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 46px; font-weight: 900; font-style: italic; line-height: 1;
  color: #be123c;
  text-shadow: 0 0 20px rgba(190,18,60,0.4), 0 2px 6px rgba(0,0,0,0.7);
}

/* 哥特标签（蕾丝边框感） */
.gothic-tag {
  display: inline-flex; align-items: center; gap: 3px;
  border: 1px solid currentColor; padding: 2px 8px;
  border-radius: 0; font-size: 9px; font-weight: 700;
  letter-spacing: 1px; text-transform: uppercase;
  font-family: 'Source Sans 3',sans-serif;
}
.gothic-tag.rose   { color: #be123c; }
.gothic-tag.violet { color: #a855f7; }
.gothic-tag.black  { color: rgba(232,213,216,0.5); }

/* 玫瑰进度条 */
.rose-bar { height: 3px; background: rgba(136,19,55,0.15); }
.rose-fill {
  height: 100%;
  background: linear-gradient(90deg, #450a14, #881337, #be123c, #f43f5e);
}

/* 哥特蕾丝分割线 */
.lace-rule {
  border: none; height: 1px; margin: 6px 0;
  background: repeating-linear-gradient(
    90deg, transparent, transparent 3px,
    rgba(136,19,55,0.25) 3px, rgba(136,19,55,0.25) 4px
  );
}

/* 数据行（墓志铭感） */
.gothic-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; padding: 4px 0;
  border-bottom: 1px solid rgba(136,19,55,0.08);
  font-family: 'Source Sans 3',sans-serif;
}
.gothic-row .label { color: rgba(232,213,216,0.4); letter-spacing: 0.5px; }
.gothic-row .value { color: #e8d5d8; font-weight: 600; }

/* 诗句引用（哥特风） */
.elegy-box {
  background: rgba(136,19,55,0.06);
  border-left: 2px solid rgba(136,19,55,0.4);
  padding: 6px 10px; font-size: 10.5px;
  font-family: 'Playfair Display',serif; font-style: italic;
  color: rgba(232,213,216,0.6); line-height: 1.6;
}
```

---

## CSS 变量

```css
:root {
  --bg:   #0d080e;
  --card: rgba(13,8,14,0.92);
  --p:    #be123c;
  --pm:   rgba(136,19,55,0.1);
  --bd:   rgba(136,19,55,0.25);
  --t:    #e8d5d8;
  --mt:   #a08090;
  --dt:   #4a2030;
}
/* --violet: #a855f7; */
```
