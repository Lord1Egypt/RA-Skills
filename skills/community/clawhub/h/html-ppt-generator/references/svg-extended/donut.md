# donut · 圆环图

**适用：** 占比分析、完成率、市场份额（≤5 个分类）
**尺寸：** 130×130px

```html
<svg viewBox="0 0 130 130" style="width:130px;height:130px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="dg1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="var(--p)"/>
      <stop offset="100%" stop-color="#8b5cf6"/>
    </linearGradient>
  </defs>
  <!-- 背景轨道 -->
  <circle cx="65" cy="65" r="48" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="14"/>
  <!-- 数据段1：68%（周长≈301.6） -->
  <circle cx="65" cy="65" r="48" fill="none" stroke="url(#dg1)" stroke-width="14"
          stroke-dasharray="204.7 96.3" stroke-dashoffset="75.4"
          stroke-linecap="round"/>
  <!-- 数据段2：22% -->
  <circle cx="65" cy="65" r="48" fill="none" stroke="#10b981" stroke-width="14"
          stroke-dasharray="66.2 234.8" stroke-dashoffset="-129.3"
          stroke-linecap="round"/>
  <!-- 数据段3：10% -->
  <circle cx="65" cy="65" r="48" fill="none" stroke="#f59e0b" stroke-width="14"
          stroke-dasharray="30.1 270.9" stroke-dashoffset="-195.5"
          stroke-linecap="round"/>
  <!-- 中心数字 -->
  <text x="65" y="61" text-anchor="middle" font-size="20" font-weight="800"
        fill="var(--t)" letter-spacing="-1">68%</text>
  <text x="65" y="74" text-anchor="middle" font-size="8" fill="var(--dt)">主要类别</text>
  <!-- 图例 -->
  <rect x="10" y="115" width="8" height="8" rx="2" fill="url(#dg1)"/>
  <text x="22" y="123" font-size="8" fill="var(--dt)">类别A 68%</text>
  <rect x="68" y="115" width="8" height="8" rx="2" fill="#10b981"/>
  <text x="80" y="123" font-size="8" fill="var(--dt)">类别B 22%</text>
</svg>
```

**圆弧计算公式：**
```
周长 C = 2 × π × r = 2 × 3.14159 × 48 ≈ 301.6
某段弧长 = C × 占比%
dasharray = "弧长  (C - 弧长)"
dashoffset 起始（12点方向）= C × 25% = 75.4

累计偏移计算（从第1段结束开始）：
  段1结束位置 = -(C × 68%) = -204.7
  段2 dashoffset = -(75.4 + 204.7 × 0) → 实际 = -129.3（75.4 - 204.7）
  段3 dashoffset = 段2结束 → -195.5
```
