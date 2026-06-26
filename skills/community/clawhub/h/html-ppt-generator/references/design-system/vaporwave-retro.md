# 蒸汽波（Vaporwave Retro）

**气质：** 80年代幻境、霓虹梦境、日落都市、怀旧未来主义
**适用：** 音乐报告、创意提案、娱乐数据、潮流文化分析
**推荐字体：** 等宽 / 早期 Mac 字体感（Space Mono + Syne）
**背景类型：** 暗色系（深紫夜空 #1a0533），霓虹渐变光晕
**主标题字号：** 48–70px，混用英文大写 + 全角中文，字间距宽
**页眉形式：** 日文假名混排英文，居中或怪异左偏，彩色双线边框

---

## 设计特征

- **霓虹粉**（#ff71ce）+ **赛博紫**（#b967ff）+ **水晶蓝**（#01cdfe）三色并驾
- 深紫背景 + 日落渐变光晕（橙→粉→紫→深蓝）
- 棋盘格透视地板（svg pattern）
- 闪烁感边框（双层发光），故意不对齐
- 全角字符、日文混入，ａｅｓｔｈｅｔｉｃ 全角英文

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&display=swap');

body { background: #1a0533; font-family: 'Space Mono',monospace; color: #ff71ce; }

/* 蒸汽波渐变背景 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 50% 0%,  rgba(255,113,206,0.25) 0%, transparent 50%),
    radial-gradient(ellipse at 0%  80%, rgba(185,103,255,0.2)  0%, transparent 45%),
    radial-gradient(ellipse at 100% 60%,rgba(1,205,254,0.15)   0%, transparent 40%);
}

/* 棋盘格透视地板 */
body::after {
  content:''; position:fixed; bottom:0; left:0; right:0; height:200px;
  pointer-events:none; z-index:0;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 19px,
    rgba(185,103,255,0.3) 20px
  ),
  repeating-linear-gradient(
    90deg, transparent, transparent 39px,
    rgba(185,103,255,0.3) 40px
  );
  transform: perspective(200px) rotateX(40deg);
  transform-origin: bottom;
  opacity:0.4;
}

/* 展示标题（全角霓虹） */
.display-title {
  font-family: 'Syne',monospace;
  font-size: 58px; font-weight: 800;
  letter-spacing: 6px; line-height: 1.1; text-transform: uppercase;
  background: linear-gradient(90deg, #ff71ce, #b967ff, #01cdfe);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: none; filter: drop-shadow(0 0 20px rgba(255,113,206,0.5));
}

/* 卡片（双层霓虹发光边框） */
.card {
  background: rgba(26,5,51,0.8);
  border: 1px solid rgba(255,113,206,0.4);
  box-shadow:
    0 0 8px rgba(255,113,206,0.3),
    inset 0 0 8px rgba(185,103,255,0.1);
  border-radius: 0; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 6px;
}

/* KPI 数字（三色轮换） */
.stat-num {
  font-family: 'Space Mono', monospace;
  font-size: 48px; font-weight: 700; line-height: 1; letter-spacing: 4px;
  color: #01cdfe;
  text-shadow: 0 0 20px rgba(1,205,254,0.6), 0 0 40px rgba(1,205,254,0.3);
}

/* 蒸汽波标签（全角感） */
.vapor-tag {
  display: inline-flex; align-items: center;
  border: 1px solid currentColor; padding: 2px 8px;
  font-size: 9px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase;
  border-radius: 0;
}
.vapor-tag.pink   { color: #ff71ce; box-shadow: 0 0 6px rgba(255,113,206,0.4); }
.vapor-tag.purple { color: #b967ff; box-shadow: 0 0 6px rgba(185,103,255,0.4); }
.vapor-tag.cyan   { color: #01cdfe; box-shadow: 0 0 6px rgba(1,205,254,0.4); }

/* 霓虹进度条 */
.vapor-bar { height: 4px; background: rgba(255,113,206,0.1); }
.vapor-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff71ce, #b967ff, #01cdfe);
  box-shadow: 0 0 8px rgba(185,103,255,0.5);
}

/* 双线分割（蒸汽波经典） */
.vapor-divider {
  border: none;
  border-top: 1px solid rgba(255,113,206,0.3);
  border-bottom: 1px solid rgba(1,205,254,0.3);
  height: 3px; margin: 8px 0;
}
```

---

## CSS 变量

```css
:root {
  --bg:   #1a0533;
  --card: rgba(26,5,51,0.8);
  --p:    #ff71ce;
  --pm:   rgba(255,113,206,0.12);
  --bd:   rgba(255,113,206,0.3);
  --t:    #ffe4f6;
  --mt:   #b967ff;
  --dt:   #5c2d80;
}
/* --cyan: #01cdfe; --yellow: #fffb96; */
```
