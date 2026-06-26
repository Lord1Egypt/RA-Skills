# 秋叶原电器街（Akihabara Neon）

**气质：** 宅文化圣地、信息过载、霓虹招牌、商品标签密集
**适用：** 御宅数据、ACG市场报告、ACGN活动、二次元消费分析
**推荐字体：** FP-3（Space Mono + IBM Plex Sans），日文等宽感
**背景类型：** 暗色系（夜晚街道黑 #0a0a0f），霓虹招牌多色光
**主标题字号：** 36–50px，混入日文/英文，招牌感，多色块
**页眉形式：** 电器店价格标签感，左右色块，SALE! 闪烁字样，日元符号

---

## 设计特征

- **荧光黄**（#facc15）+ **霓虹粉**（#f472b6）+ **电气蓝**（#38bdf8）+ **lime绿**（#a3e635）四色并用
- 漆黑背景，多彩霓虹灯管光晕效果
- 商品价格标签（POP 标签）为核心卡片组件
- 信息密集，允许拥挤——这就是秋叶原精神
- 日元¥/价格/折扣 等商业元素混入数据

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

body { background: #0a0a0f; font-family: 'IBM Plex Sans','Hiragino Kaku Gothic ProN','PingFang SC',sans-serif; color: #f0e8d8; }

/* 秋叶原霓虹光晕（多色） */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 15% 30%, rgba(244,114,182,0.12) 0%, transparent 35%),
    radial-gradient(ellipse at 80% 20%, rgba(250,204,21,0.08)  0%, transparent 30%),
    radial-gradient(ellipse at 50% 80%, rgba(56,189,248,0.1)   0%, transparent 35%),
    radial-gradient(ellipse at 85% 65%, rgba(163,230,53,0.07)  0%, transparent 30%);
}

/* 展示标题（招牌感） */
.display-title {
  font-family: 'Space Mono',monospace;
  font-size: 42px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 2px; line-height: 1.0;
  color: #facc15;
  text-shadow:
    0 0 20px rgba(250,204,21,0.6),
    0 0 40px rgba(250,204,21,0.3),
    2px 2px 0 rgba(244,114,182,0.5);
}

/* 价格 POP 标签卡片 */
.card {
  background: rgba(10,10,20,0.95);
  border: 2px solid rgba(250,204,21,0.5);
  border-radius: 4px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 4px;
  position: relative;
  box-shadow:
    0 0 12px rgba(250,204,21,0.15),
    inset 0 0 8px rgba(250,204,21,0.03);
}
/* POP 角标 */
.card .pop-corner {
  position: absolute; top: -1px; right: -1px;
  background: #f472b6; color: #ffffff;
  font-size: 7px; font-weight: 700; padding: 2px 6px;
  font-family: 'Space Mono',monospace; letter-spacing: 1px;
}

/* KPI（价格大字感） */
.stat-num {
  font-family: 'Space Mono', monospace;
  font-size: 44px; font-weight: 700; line-height: 1; letter-spacing: 1px;
  color: #facc15;
  text-shadow: 0 0 16px rgba(250,204,21,0.5);
}
.stat-num .yen { font-size: 20px; color: #f472b6; margin-right: 2px; }

/* 商品标签（四色霓虹） */
.akiba-tag {
  display: inline-flex; align-items: center;
  padding: 2px 7px; border-radius: 2px;
  font-family: 'Space Mono',monospace; font-size: 8.5px; font-weight: 700;
  letter-spacing: 1px; text-transform: uppercase;
}
.akiba-tag.yellow { background: #facc15; color: #0a0a0f; }
.akiba-tag.pink   { background: #f472b6; color: #ffffff; }
.akiba-tag.blue   { background: #38bdf8; color: #0a0a0f; }
.akiba-tag.green  { background: #a3e635; color: #0a0a0f; }
.akiba-tag.red    { background: #ef4444; color: #ffffff; }

/* 霓虹进度条（多色） */
.neon-bar {
  height: 5px;
  background: rgba(250,204,21,0.1);
  border: 1px solid rgba(250,204,21,0.2);
  border-radius: 0;
}
.neon-fill {
  height: 100%;
  background: linear-gradient(90deg, #f472b6, #facc15, #a3e635, #38bdf8);
  box-shadow: 0 0 8px rgba(250,204,21,0.4);
}

/* 招牌灯管分割线 */
.neon-rule {
  height: 2px; border: none;
  background: repeating-linear-gradient(
    90deg,
    #facc15 0,  #facc15 20px, transparent 20px, transparent 22px,
    #f472b6 22px, #f472b6 42px, transparent 42px, transparent 44px,
    #38bdf8 44px, #38bdf8 64px, transparent 64px, transparent 66px
  );
  opacity: 0.5; margin: 6px 0;
}

/* 商品数据行（密集） */
.akiba-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 9.5px; padding: 2px 0;
  border-bottom: 1px solid rgba(250,204,21,0.06);
  font-family: 'Space Mono',monospace;
}
.akiba-row .label { color: rgba(240,232,216,0.5); }
.akiba-row .val   { color: #facc15; font-weight: 700; }
.akiba-row .disc  { color: #f472b6; font-size: 8.5px; }
```

---

## CSS 变量

```css
:root {
  --bg:   #0a0a0f;
  --card: rgba(10,10,20,0.95);
  --p:    #facc15;
  --pm:   rgba(250,204,21,0.08);
  --bd:   rgba(250,204,21,0.3);
  --t:    #f0e8d8;
  --mt:   #a09880;
  --dt:   #404038;
}
/* --pink: #f472b6; --blue: #38bdf8; --lime: #a3e635; */
```
