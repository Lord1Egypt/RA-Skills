# 少年热血（Anime Shounen）

**气质：** 热血少年漫画、破限突围、速度线冲击、友情与战斗
**适用：** 游戏对战数据、体育运动、竞技分析、激励型报告
**推荐字体：** FP-1（Syne 800 + DM Sans），粗体冲击
**背景类型：** 暗色系（漫画黑 #0c0c0c）或亮白（决战模式互换）
**主标题字号：** 60–80px Syne 极粗，速度线背景，字体带描边
**页眉形式：** 大号集气条，章节名（第×章），爆炸音效字（BOOM/CLASH），斜切角

---

## 设计特征

- **燃烧橙**（#ea580c / #f97316）+ **极限金**（#fbbf24）+ **决斗蓝**（#1d4ed8）三色
- 暗背景 + 速度线（radial-gradient 辐射线）
- 文字带 `-webkit-text-stroke` 描边，漫画感
- 斜切角卡片（`clip-path: polygon` 平行四边形）
- 爆炸音效字（PLUS ULTRA / MAX POWER）

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

body { background: #0c0c0c; font-family: 'DM Sans','PingFang SC',sans-serif; color: #f5f0e8; }

/* 速度线辐射背景 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background: repeating-conic-gradient(
    from 0deg at 50% 50%,
    rgba(234,88,12,0.04) 0deg 1deg,
    transparent 1deg 5deg
  );
}

/* 展示标题（热血描边大字） */
.display-title {
  font-family: 'Syne','PingFang SC',sans-serif;
  font-size: 68px; font-weight: 800; text-transform: uppercase;
  letter-spacing: -2px; line-height: 0.88;
  color: #f97316;
  -webkit-text-stroke: 2px #ffffff;
  text-shadow:
    4px 4px 0 rgba(0,0,0,0.8),
    0 0 40px rgba(249,115,22,0.4);
}

/* 卡片（斜切平行四边形感） */
.card {
  background: rgba(15,10,5,0.95);
  border: 2px solid rgba(234,88,12,0.4);
  border-left: 4px solid #ea580c;
  border-radius: 0;
  clip-path: polygon(0 0, calc(100% - 6px) 0, 100% 6px, 100% 100%, 6px 100%, 0 calc(100% - 6px));
  padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
}

/* KPI（燃烧金） */
.stat-num {
  font-family: 'Syne', sans-serif;
  font-size: 56px; font-weight: 800; line-height: 1; letter-spacing: -2px;
  color: #fbbf24;
  -webkit-text-stroke: 1px rgba(234,88,12,0.8);
  text-shadow: 0 0 30px rgba(251,191,36,0.5), 3px 3px 0 rgba(0,0,0,0.6);
}

/* 集气/能量条（粗壮燃烧感） */
.power-bar {
  height: 12px;
  background: rgba(234,88,12,0.1);
  border: 2px solid rgba(234,88,12,0.3);
  border-radius: 0;
  clip-path: polygon(4px 0, 100% 0, calc(100% - 4px) 100%, 0 100%);
}
.power-fill {
  height: 100%;
  background: linear-gradient(90deg, #c2410c, #ea580c, #fbbf24);
  box-shadow: 0 0 12px rgba(234,88,12,0.5);
}

/* 爆炸音效字 */
.sfx-word {
  font-family: 'Syne',sans-serif;
  font-size: 11px; font-weight: 800; letter-spacing: 3px;
  text-transform: uppercase; color: #fbbf24;
  -webkit-text-stroke: 0.5px #ea580c;
  transform: rotate(-3deg); display: inline-block;
}

/* 状态标签（战斗力等级） */
.power-tag {
  display: inline-flex; align-items: center;
  border: 2px solid currentColor; border-radius: 0;
  padding: 1px 7px;
  font-family: 'Syne',sans-serif; font-size: 9px; font-weight: 800;
  letter-spacing: 1.5px; text-transform: uppercase;
  clip-path: polygon(3px 0, 100% 0, calc(100% - 3px) 100%, 0 100%);
}
.power-tag.max  { color: #fbbf24; background: rgba(251,191,36,0.1); }
.power-tag.high { color: #ea580c; background: rgba(234,88,12,0.1); }
.power-tag.low  { color: #6b7280; background: rgba(107,114,128,0.1); }

/* 章节分割线（速度线感） */
.battle-rule {
  height: 2px; border: none;
  background: linear-gradient(90deg, transparent, #ea580c 20%, #fbbf24 50%, #ea580c 80%, transparent);
  margin: 6px 0;
}

/* 战斗数据行 */
.battle-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; padding: 3px 0;
  border-bottom: 1px solid rgba(234,88,12,0.1);
}
.battle-row .label { color: rgba(245,240,232,0.5); }
.battle-row .val   { color: #fbbf24; font-weight: 700; font-family: 'Syne',sans-serif; }
```

---

## CSS 变量

```css
:root {
  --bg:   #0c0c0c;
  --card: rgba(15,10,5,0.95);
  --p:    #ea580c;
  --pm:   rgba(234,88,12,0.1);
  --bd:   rgba(234,88,12,0.3);
  --t:    #f5f0e8;
  --mt:   #a8a098;
  --dt:   #4a4038;
}
/* --gold: #fbbf24; --blue: #1d4ed8; */
```
