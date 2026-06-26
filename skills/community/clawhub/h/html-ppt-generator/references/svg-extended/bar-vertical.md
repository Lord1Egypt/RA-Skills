# bar-vertical · 柱状图

**适用：** 分类数值对比（同类指标，不同组别）
**高度：** 75px

```html
<svg viewBox="0 0 290 75" style="width:100%;height:75px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 基准线 -->
  <line x1="20" y1="55" x2="280" y2="55" stroke="#1e293b" stroke-width="1"/>
  <line x1="20" y1="35" x2="280" y2="35" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,3"/>
  <line x1="20" y1="15" x2="280" y2="15" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,3"/>
  <!-- 柱 -->
  <rect x="30"  y="20" width="30" height="35" rx="2" fill="var(--p)" opacity="0.9"/>
  <rect x="80"  y="10" width="30" height="45" rx="2" fill="var(--p)"/>
  <rect x="130" y="25" width="30" height="30" rx="2" fill="#ef4444"/>
  <rect x="180" y="5"  width="30" height="50" rx="2" fill="var(--p)"/>
  <rect x="230" y="15" width="30" height="40" rx="2" fill="#10b981"/>
  <!-- X标签 -->
  <text x="45"  y="65" text-anchor="middle" font-size="8" fill="#64748b">A</text>
  <text x="95"  y="65" text-anchor="middle" font-size="8" fill="#64748b">B</text>
  <text x="145" y="65" text-anchor="middle" font-size="8" fill="#64748b">C</text>
  <text x="195" y="65" text-anchor="middle" font-size="8" fill="#64748b">D</text>
  <text x="245" y="65" text-anchor="middle" font-size="8" fill="#64748b">E</text>
  <!-- Y轴 -->
  <text x="16"  y="58" font-size="8" fill="#64748b" text-anchor="end">0%</text>
  <text x="16"  y="38" font-size="8" fill="#64748b" text-anchor="end">50%</text>
  <text x="16"  y="18" font-size="8" fill="#64748b" text-anchor="end">100%</text>
</svg>
```

**参数说明：**
- 绘图区底线 y=55，顶线 y=15（高度40px）
- 柱高 = (值/最大值) × 40，柱 y = 55 - 柱高
- 柱宽 30px，柱间间距 20px，第一柱 x=30
- 强调某柱：用 #ef4444（异常）或 #10b981（最优）替换主色
