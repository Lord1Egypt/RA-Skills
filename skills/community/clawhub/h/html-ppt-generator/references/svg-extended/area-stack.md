# area-stack · 堆叠面积图

**适用：** 多系列累计趋势、总量构成随时间变化、市场结构演变
**高度：** 100px

---

## 变体 A · 三层堆叠面积（100px）

```html
<svg viewBox="0 0 290 100" style="width:100%;height:100px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="as1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="var(--p)" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="var(--p)" stop-opacity="0.4"/>
    </linearGradient>
    <linearGradient id="as2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0.3"/>
    </linearGradient>
    <linearGradient id="as3" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0.2"/>
    </linearGradient>
  </defs>
  <!-- 坐标轴 -->
  <line x1="24" y1="6"  x2="24"  y2="72" stroke="#1e293b" stroke-width="1"/>
  <line x1="24" y1="72" x2="280" y2="72" stroke="#1e293b" stroke-width="1"/>
  <line x1="24" y1="40" x2="280" y2="40" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,3"/>

  <!-- 层3（底层：绿）：从y=72到各点 -->
  <polygon points="24,60 78,56 132,52 186,48 240,44 280,42 280,72 24,72" fill="url(#as3)"/>
  <polyline points="24,60 78,56 132,52 186,48 240,44 280,42" fill="none" stroke="#10b981" stroke-width="1.2"/>

  <!-- 层2（中层：紫）：叠加在层3之上 -->
  <polygon points="24,48 78,42 132,36 186,30 240,26 280,22 280,42 240,44 186,48 132,52 78,56 24,60" fill="url(#as2)"/>
  <polyline points="24,48 78,42 132,36 186,30 240,26 280,22" fill="none" stroke="#8b5cf6" stroke-width="1.2"/>

  <!-- 层1（顶层：主色）：叠加在层2之上 -->
  <polygon points="24,36 78,28 132,22 186,16 240,12 280,10 280,22 240,26 186,30 132,36 78,42 24,48" fill="url(#as1)"/>
  <polyline points="24,36 78,28 132,22 186,16 240,12 280,10" fill="none" stroke="var(--p)" stroke-width="1.5"/>

  <!-- 轴标签 -->
  <text x="24"  y="82" font-size="8" fill="#64748b" text-anchor="middle">2020</text>
  <text x="132" y="82" font-size="8" fill="#64748b" text-anchor="middle">2022</text>
  <text x="280" y="82" font-size="8" fill="#64748b" text-anchor="middle">2024</text>
  <text x="20"  y="72" font-size="7.5" fill="#64748b" text-anchor="end">0</text>
  <text x="20"  y="10" font-size="7.5" fill="#64748b" text-anchor="end">100%</text>

  <!-- 图例 -->
  <rect x="24"  y="90" width="8" height="6" rx="1" fill="var(--p)" opacity="0.7"/>
  <text x="36"  y="96" font-size="7.5" fill="#64748b">系列A</text>
  <rect x="80"  y="90" width="8" height="6" rx="1" fill="#8b5cf6" opacity="0.7"/>
  <text x="92"  y="96" font-size="7.5" fill="#64748b">系列B</text>
  <rect x="136" y="90" width="8" height="6" rx="1" fill="#10b981" opacity="0.6"/>
  <text x="148" y="96" font-size="7.5" fill="#64748b">系列C</text>
</svg>
```

---

## 变体 B · 100% 堆叠面积（90px）

```html
<svg viewBox="0 0 290 90" style="width:100%;height:90px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 坐标轴 -->
  <line x1="24" y1="6"  x2="24"  y2="65" stroke="#1e293b" stroke-width="1"/>
  <line x1="24" y1="65" x2="280" y2="65" stroke="#1e293b" stroke-width="1"/>

  <!-- 层C（底，绿）：占比约30% → y从65到46.5，高18.5px -->
  <polygon points="24,65 280,65 280,47 132,49 24,51" fill="#10b981" opacity="0.6"/>

  <!-- 层B（中，紫）：占比约35% → 从层C顶到层B顶 -->
  <polygon points="24,51 132,49 280,47 280,28 132,30 24,32" fill="#8b5cf6" opacity="0.7"/>

  <!-- 层A（顶，主色）：剩余约35% → 从层B顶到y=6~10 -->
  <polygon points="24,32 132,30 280,28 280,6 132,9 24,10" fill="var(--p)" opacity="0.8"/>

  <!-- Y轴标注（100%/50%/0%） -->
  <text x="20" y="68" font-size="7.5" fill="#64748b" text-anchor="end">0%</text>
  <text x="20" y="37" font-size="7.5" fill="#64748b" text-anchor="end">50%</text>
  <text x="20" y="10" font-size="7.5" fill="#64748b" text-anchor="end">100%</text>

  <!-- X轴标注 -->
  <text x="24"  y="75" font-size="8" fill="#64748b" text-anchor="middle">2020</text>
  <text x="132" y="75" font-size="8" fill="#64748b" text-anchor="middle">2022</text>
  <text x="280" y="75" font-size="8" fill="#64748b" text-anchor="middle">2024</text>

  <!-- 图例 -->
  <rect x="24"  y="82" width="8" height="5" rx="1" fill="var(--p)" opacity="0.8"/>
  <text x="36"  y="87" font-size="7.5" fill="#64748b">系列A</text>
  <rect x="80"  y="82" width="8" height="5" rx="1" fill="#8b5cf6" opacity="0.7"/>
  <text x="92"  y="87" font-size="7.5" fill="#64748b">系列B</text>
  <rect x="136" y="82" width="8" height="5" rx="1" fill="#10b981" opacity="0.6"/>
  <text x="148" y="87" font-size="7.5" fill="#64748b">系列C</text>
</svg>
```

**参数说明：**
- 堆叠顺序：从底到顶（polygon 先画底层，后画顶层）
- 各层 polygon 的上边界点 = 前所有层高度之和对应的 y 坐标
- 100%堆积：将各层占比归一化到总高60px；顶部永远对齐 y=6
- 每层用不同颜色+opacity区分，不同层边界可加 polyline 描边
