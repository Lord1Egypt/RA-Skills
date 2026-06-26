# dual-axis · 双轴图

**适用：** 两组量级不同的数据叠加（如数量+比率、收入+增速）
**高度：** 90px

```html
<svg viewBox="0 0 290 90" style="width:100%;height:90px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="barG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="var(--p)" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="var(--p)" stop-opacity="0.3"/>
    </linearGradient>
  </defs>
  <!-- 左Y轴 -->
  <line x1="28" y1="8" x2="28" y2="70" stroke="#1e293b" stroke-width="1"/>
  <!-- 右Y轴（虚线） -->
  <line x1="272" y1="8" x2="272" y2="70" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,2"/>
  <!-- X轴 -->
  <line x1="28" y1="70" x2="272" y2="70" stroke="#1e293b" stroke-width="1"/>
  <!-- 柱状（左轴） -->
  <rect x="40"  y="30" width="18" height="40" rx="2" fill="url(#barG)"/>
  <rect x="80"  y="20" width="18" height="50" rx="2" fill="url(#barG)"/>
  <rect x="120" y="35" width="18" height="35" rx="2" fill="url(#barG)"/>
  <rect x="160" y="15" width="18" height="55" rx="2" fill="url(#barG)"/>
  <rect x="200" y="25" width="18" height="45" rx="2" fill="url(#barG)"/>
  <rect x="240" y="10" width="18" height="60" rx="2" fill="url(#barG)"/>
  <!-- 折线（右轴，增长率） -->
  <polyline points="49,55 89,38 129,48 169,28 209,35 249,18"
            fill="none" stroke="#f59e0b" stroke-width="2"/>
  <circle cx="49"  cy="55" r="3" fill="#f59e0b"/>
  <circle cx="89"  cy="38" r="3" fill="#f59e0b"/>
  <circle cx="129" cy="48" r="3" fill="#f59e0b"/>
  <circle cx="169" cy="28" r="3" fill="#f59e0b"/>
  <circle cx="209" cy="35" r="3" fill="#f59e0b"/>
  <circle cx="249" cy="18" r="3" fill="#f59e0b"/>
  <!-- X标签 -->
  <text x="49"  y="80" text-anchor="middle" font-size="7.5" fill="#64748b">1月</text>
  <text x="89"  y="80" text-anchor="middle" font-size="7.5" fill="#64748b">2月</text>
  <text x="129" y="80" text-anchor="middle" font-size="7.5" fill="#64748b">3月</text>
  <text x="169" y="80" text-anchor="middle" font-size="7.5" fill="#64748b">4月</text>
  <text x="209" y="80" text-anchor="middle" font-size="7.5" fill="#64748b">5月</text>
  <text x="249" y="80" text-anchor="middle" font-size="7.5" fill="#64748b">6月</text>
  <!-- 图例 -->
  <rect x="30"  y="85" width="8" height="5" rx="1" fill="var(--p)"/>
  <text x="42"  y="90" font-size="7.5" fill="#64748b">数量（左轴）</text>
  <line x1="120" y1="87" x2="132" y2="87" stroke="#f59e0b" stroke-width="2"/>
  <circle cx="126" cy="87" r="2" fill="#f59e0b"/>
  <text x="136" y="90" font-size="7.5" fill="#64748b">增长率（右轴）</text>
</svg>
```

**参数说明：**
- 柱状用主色渐变（左轴量级）
- 折线用对比色 #f59e0b（右轴百分比）
- 右Y轴用虚线与左轴区分
- 折线数据点 cx = 柱中心 x（柱左x + 柱宽/2）
