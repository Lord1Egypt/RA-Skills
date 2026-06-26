# line-area · 折线面积图

**适用：** 时间序列趋势、增长/衰减曲线
**高度：** 85px（带渐变填充）

```html
<svg viewBox="0 0 290 85" style="width:100%;height:85px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ga" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="var(--p)" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="var(--p)" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <!-- 坐标轴 -->
  <line x1="24" y1="6"  x2="24"  y2="62" stroke="#1e293b" stroke-width="1"/>
  <line x1="24" y1="62" x2="270" y2="62" stroke="#1e293b" stroke-width="1"/>
  <line x1="24" y1="36" x2="270" y2="36" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="3,3"/>
  <!-- 面积填充 + 折线 -->
  <polygon points="24,54 78,44 132,33 186,22 240,14 270,10 270,62 24,62" fill="url(#ga)"/>
  <polyline points="24,54 78,44 132,33 186,22 240,14 270,10" fill="none" stroke="var(--p)" stroke-width="1.8"/>
  <!-- 数据点 -->
  <circle cx="24"  cy="54" r="2.5" fill="var(--p)"/>
  <circle cx="132" cy="33" r="2.5" fill="var(--p)"/>
  <circle cx="270" cy="10" r="2.5" fill="var(--p)"/>
  <!-- 标签 -->
  <text x="24"  y="74" font-size="8.5" fill="#64748b" text-anchor="middle">2020</text>
  <text x="132" y="74" font-size="8.5" fill="#64748b" text-anchor="middle">2022</text>
  <text x="270" y="74" font-size="8.5" fill="#64748b" text-anchor="middle">2024</text>
  <text x="20"  y="54" font-size="8.5" fill="#64748b" text-anchor="end">43%</text>
  <text x="20"  y="10" font-size="8.5" fill="#64748b" text-anchor="end">99%</text>
</svg>
```

**参数说明：**
- 绘图区：x 24–270，y 6–62（高度56px）
- Y 轴：最低值对应 y=54，最高值对应 y=10
- Y 坐标计算：y = 62 - (值/最大值) × 56
- polygon 须在折线终点加封底坐标 `270,62 24,62`
- 多条线时为每条折线单独命名 linearGradient id
