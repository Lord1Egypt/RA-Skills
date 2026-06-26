# 像素8位（Pixel 8-bit）

**气质：** 复古游戏机、FC红白机、像素艺术、老式街机
**适用：** 游戏数据、像素艺术展示、复古科技、极客怀旧报告
**推荐字体：** 等宽字体模拟像素（Space Mono），禁止任何曲线
**背景类型：** 暗色系（像素黑 #0f0f0f），像素格子渐变背景
**主标题字号：** 28–36px，必须 letter-spacing: 4px+，模拟位图字形
**页眉形式：** 全大写等宽，像素分隔线（= = = =），左侧生命♥♥♥

---

## 设计特征

- **像素绿**（#39ff14 / #00ff41）+ **经典白**（#ffffff）双主色
- 所有圆角=0（border-radius:0 强制）
- 像素格子背景（4px 网格）
- 数字必须等宽对齐，模拟七段数码管或位图字体
- 装饰只用 █ ▓ ░ ♥ ★ ◄ ► 等 ASCII 符号

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');

body {
  background: #0f0f0f;
  font-family: 'Space Mono','Courier New',monospace;
  color: #39ff14; image-rendering: pixelated;
}

/* 像素格子背景 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:
    linear-gradient(rgba(57,255,20,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(57,255,20,0.04) 1px, transparent 1px);
  background-size: 4px 4px;
}

/* CRT 弯曲光晕 */
body::after {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.5) 100%);
}

/* 展示标题（像素大字） */
.display-title {
  font-family: 'Space Mono',monospace;
  font-size: 30px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 6px; line-height: 1.2;
  color: #39ff14;
  text-shadow:
    0 0 8px rgba(57,255,20,0.8),
    0 0 20px rgba(57,255,20,0.4);
}

/* INSERT COIN 闪烁感标注 */
.pixel-blink {
  animation: none; /* 静态版，部署时可加 blink 动画 */
  color: #ffffff; font-weight: 700;
  letter-spacing: 4px; text-transform: uppercase; font-size: 10px;
}

/* 卡片（像素边框，无圆角） */
.card {
  background: #0a0a0a;
  border: 2px solid #39ff14;
  border-radius: 0; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow: 0 0 12px rgba(57,255,20,0.2), inset 0 0 8px rgba(57,255,20,0.03);
  image-rendering: pixelated;
}

/* KPI 数字（数码管感） */
.stat-num {
  font-family: 'Space Mono', monospace;
  font-size: 44px; font-weight: 700; line-height: 1;
  letter-spacing: 4px; color: #39ff14;
  text-shadow: 0 0 16px rgba(57,255,20,0.7);
}

/* 像素进度条（格子填充） */
.pixel-bar {
  height: 10px;
  background: repeating-linear-gradient(
    90deg, rgba(57,255,20,0.12) 0, rgba(57,255,20,0.12) 7px,
    transparent 7px, transparent 8px
  );
  border: 1px solid rgba(57,255,20,0.3);
  border-radius: 0;
}
.pixel-fill {
  height: 100%;
  background: repeating-linear-gradient(
    90deg, #39ff14 0, #39ff14 7px,
    #16a34a 7px, #16a34a 8px
  );
}

/* 生命值♥（ASCII 装饰） */
.lives {
  font-size: 12px; color: #ff4444; letter-spacing: 4px;
}
.lives .dead { color: #333; }

/* 状态标签（SELECT/START 感） */
.pixel-tag {
  display: inline-flex; border: 1px solid currentColor;
  padding: 1px 6px; font-size: 8px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase; border-radius: 0;
}
.pixel-tag.green  { color: #39ff14; }
.pixel-tag.yellow { color: #ffff00; }
.pixel-tag.red    { color: #ff4444; }

/* ASCII 分割线 */
.pixel-rule {
  color: rgba(57,255,20,0.4); font-size: 10px; letter-spacing: 1px;
  overflow: hidden; white-space: nowrap;
  font-family: 'Space Mono',monospace;
}
/* 内容：████████████████████ */

/* 数据行（命令行感） */
.cli-data-row {
  display: flex; gap: 8px; font-size: 9.5px; padding: 2px 0;
  border-bottom: 1px solid rgba(57,255,20,0.08);
}
.cli-data-row .k { color: rgba(57,255,20,0.5); }
.cli-data-row .v { color: #39ff14; margin-left: auto; font-weight: 700; }
```

---

## CSS 变量

```css
:root {
  --bg:   #0f0f0f;
  --card: #0a0a0a;
  --p:    #39ff14;
  --pm:   rgba(57,255,20,0.08);
  --bd:   rgba(57,255,20,0.3);
  --t:    #39ff14;
  --mt:   rgba(57,255,20,0.6);
  --dt:   rgba(57,255,20,0.25);
}
/* 变体：--p: #00bfff (GBA蓝) / #ffff00 (街机黄) */
```
