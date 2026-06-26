# bar-horizontal · 横向条形图

**适用：** 多项并列对比，显示各类别数值大小
**高度：** 55px（卡片内嵌）

> 颜色使用 Tc CSS 变量：单系列用 `var(--p)`，多系列用 `var(--c1)/var(--c2)/var(--c3)`。

```html
<svg viewBox="0 0 290 55" style="width:100%;height:55px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <text x="0"   y="11" font-size="9" fill="var(--dt)">系列A</text>
  <rect x="46"  y="2"  width="122" height="9" rx="2" fill="var(--p)"/>
  <text x="172" y="11" font-size="9" fill="var(--mt)">63%</text>

  <text x="0"   y="28" font-size="9" fill="var(--dt)">系列B</text>
  <rect x="46"  y="19" width="188" height="9" rx="2" fill="var(--c2,#8b5cf6)"/>
  <text x="238" y="28" font-size="9" fill="var(--mt)">97%</text>

  <text x="0"   y="45" font-size="9" fill="var(--dt)">系列C</text>
  <rect x="46"  y="36" width="169" height="9" rx="2" fill="var(--c3,#ef4444)"/>
  <text x="219" y="45" font-size="9" fill="var(--mt)">87%</text>
</svg>
```

**参数说明：**
- 标签列宽约 46px，数值从 x=46 开始
- 条宽 = 总可用宽 244px × 百分比（如 63% → 122px）
- 每行占 17px（bar 9px + 上下各 4px）
- 单系列：全部用 `var(--p)`；多系列：`var(--c1)`/`var(--c2)`/`var(--c3)`
- 轴标签统一用 `var(--dt)`，数值标注用 `var(--mt)`
