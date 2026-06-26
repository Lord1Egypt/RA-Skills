# pie · 饼图

**适用：** 占比分析、市场份额、构成比例（≤5 个分类，总和 100%）
**尺寸：** 130×130px

```html
<svg viewBox="0 0 130 130" style="width:130px;height:130px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="pg1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#2563eb"/>
    </linearGradient>
    <linearGradient id="pg2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="pg3" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#d97706"/>
    </linearGradient>
    <linearGradient id="pg4" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="100%" stop-color="#dc2626"/>
    </linearGradient>
  </defs>
  <!-- 扇形 1:35% (0°~126°) -->
  <path d="M 65 65 L 65 17 A 48 48 0 0 1 108.5 40 Z"
        fill="url(#pg1)" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  <!-- 扇形 2:28% (126°~227°) -->
  <path d="M 65 65 L 108.5 40 A 48 48 0 0 1 30 95 Z"
        fill="url(#pg2)" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  <!-- 扇形 3:22% (227°~306°) -->
  <path d="M 65 65 L 30 95 A 48 48 0 0 1 50 25 Z"
        fill="url(#pg3)" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  <!-- 扇形 4:15% (306°~360°) -->
  <path d="M 65 65 L 50 25 A 48 48 0 0 1 65 17 Z"
        fill="url(#pg4)" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  <!-- 中心白色圆形（可选，变圆环饼图） -->
  <!-- <circle cx="65" cy="65" r="20" fill="var(--bg)"/> -->
  <!-- 中心数字（可选） -->
  <text x="65" y="61" text-anchor="middle" font-size="18" font-weight="800"
        fill="var(--t)" letter-spacing="-1">35%</text>
  <text x="65" y="74" text-anchor="middle" font-size="8" fill="var(--dt)">最大份额</text>
  <!-- 图例 -->
  <rect x="8" y="110" width="8" height="8" rx="1.5" fill="url(#pg1)"/>
  <text x="20" y="118" font-size="8" fill="var(--dt)">A 35%</text>
  <rect x="50" y="110" width="8" height="8" rx="1.5" fill="url(#pg2)"/>
  <text x="62" y="118" font-size="8" fill="var(--dt)">B 28%</text>
  <rect x="88" y="110" width="8" height="8" rx="1.5" fill="url(#pg3)"/>
  <text x="100" y="118" font-size="8" fill="var(--dt)">C 22%</text>
  <rect x="8" y="122" width="8" height="8" rx="1.5" fill="url(#pg4)"/>
  <text x="20" y="130" font-size="8" fill="var(--dt)">D 15%</text>
</svg>
```

**扇形角度计算：**
```
总角度 360°，半径 r=48
扇形角度 = 360° × 占比%

35% → 126°
28% → 101°
22% → 79°
15% → 54°

圆弧终点坐标计算：
x = 65 + r × cos(θ)
y = 65 + r × sin(θ)

角度从 12 点方向顺时针计算（SVG 坐标系）：
0°   → (65, 17)
90°  → (113, 65)
180° → (65, 113)
270° → (17, 65)
```

**使用建议：**
- 分类 ≤5 个，超过则用圆环图或堆积条
- 最大占比建议放在 12 点方向（12 点钟位置）
- 可配合中心数字显示最大类别占比
