# 文化博物（Culture Museum）

**气质：** 人文气息、博物馆展览、艺术典藏
**适用：** 文化活动、艺术报告、非遗展示、博物馆策展
**推荐字体：** FP-2（Playfair Display 900 + Source Sans 3）或 FP-6（Fraunces + Nunito）
**背景类型：** 暖米色系（#faf7f2 / #f5f0e8），温润有质感
**主标题字号：** 40–54px 衬线大标题，优雅气度
**页眉形式：** 细衬线标题 + 展览编号，底部细线分割，留白优先

---

## 设计特征

- **暖赭棕色**（#92400e / #78350f）作为主强调色，典雅古朴
- 高对比衬线展示标题（Playfair Display 900）
- 大量留白，内容节奏舒缓
- 卡片用米色背景 + 棕色细边，无阴影
- 可加手绘感分隔线装饰

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Sans+3:wght@300;400;600&display=swap');

body { background: #faf7f2; font-family: 'Source Sans 3','Noto Sans SC',sans-serif; color: #2c2416; }

/* 展示标题（高对比衬线） */
.display-title {
  font-family: 'Playfair Display','Noto Serif SC',serif;
  font-size: 48px; font-weight: 900;
  letter-spacing: -1.5px; line-height: 1.0;
  color: #1c1409;
  font-style: italic;
}

/* 副标题（轻衬线） */
.subtitle {
  font-family: 'Playfair Display',serif;
  font-size: 16px; font-weight: 700; font-style: italic;
  color: #92400e;
}

/* 卡片（米色无阴影，棕色细边） */
.card {
  background: #f5f0e8;
  border: 1px solid rgba(120,53,15,0.15);
  border-top: 2px solid rgba(146,64,14,0.5);
  border-radius: 2px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
}

/* 展品/条目标注 */
.artifact-label {
  font-family: 'Playfair Display',serif;
  font-size: 9px; letter-spacing: 2px;
  text-transform: uppercase; color: #92400e; opacity: 0.7;
}

/* KPI 数字 */
.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 42px; font-weight: 900; font-style: italic;
  line-height: 1; color: #92400e;
}

/* 手绘感分隔线 */
.culture-divider {
  height:1px; border:none;
  background: repeating-linear-gradient(90deg, #92400e 0, #92400e 3px, transparent 3px, transparent 8px);
  opacity: 0.3; margin: 8px 0;
}

/* 引用框（展览说明牌感） */
.exhibit-note {
  background: rgba(146,64,14,0.06);
  border-left: 2px solid rgba(146,64,14,0.4);
  padding: 6px 10px; font-size: 10.5px; color: #5c3b1a;
  font-family: 'Playfair Display',serif; font-style: italic;
}
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #faf7f2;
  --card: #f5f0e8;
  --p:    #92400e;
  --pm:   rgba(146,64,14,0.08);
  --bd:   rgba(120,53,15,0.15);
  --t:    #2c2416;
  --mt:   #5c3b1a;
  --dt:   #9a7c5e;
}
```
