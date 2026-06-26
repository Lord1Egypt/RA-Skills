# polar-area · 极坐标面积图（玫瑰图）

**适用：** 周期性数据对比、多维度带量级、比雷达图更强调数值差异
**尺寸：** 150×150px

```html
<svg viewBox="0 0 150 150" style="width:150px;height:150px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="pag1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#2563eb" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="pag2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0891b2" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="pag3" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#059669" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="pag4" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#d97706" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="pag5" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ef4444" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#dc2626" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="pag6" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#7c3aed" stop-opacity="0.9"/>
    </linearGradient>
  </defs>
  <!-- 背景同心圆网格 -->
  <circle cx="75" cy="75" r="60" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
  <circle cx="75" cy="75" r="40" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
  <circle cx="75" cy="75" r="20" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>

  <!-- 扇形 1:85 (0°~60°, 半径按比例) -->
  <path d="M 75 75 L 75 15 A 60 60 0 0 1 127 45 Z"
        fill="url(#pag1)" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>

  <!-- 扇形 2:62 (60°~120°) -->
  <path d="M 75 75 L 127 45 A 60 60 0 0 1 127 105 Z"
        fill="url(#pag2)" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>

  <!-- 扇形 3:45 (120°~180°) -->
  <path d="M 75 75 L 127 105 A 60 60 0 0 1 75 135 Z"
        fill="url(#pag3)" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>

  <!-- 扇形 4:73 (180°~240°) -->
  <path d="M 75 75 L 75 135 A 60 60 0 0 1 23 105 Z"
        fill="url(#pag4)" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>

  <!-- 扇形 5:58 (240°~300°) -->
  <path d="M 75 75 L 23 105 A 60 60 0 0 1 23 45 Z"
        fill="url(#pag5)" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>

  <!-- 扇形 6:91 (300°~360°) -->
  <path d="M 75 75 L 23 45 A 60 60 0 0 1 75 15 Z"
        fill="url(#pag6)" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>

  <!-- 外圈数值标签 -->
  <text x="75" y="8" text-anchor="middle" font-size="9" font-weight="700" fill="var(--t)">85</text>
  <text x="138" y="48" font-size="9" font-weight="700" fill="var(--t)">62</text>
  <text x="138" y="108" font-size="9" font-weight="700" fill="var(--t)">45</text>
  <text x="75" y="148" text-anchor="middle" font-size="9" font-weight="700" fill="var(--t)">73</text>
  <text x="12" y="108" font-size="9" font-weight="700" fill="var(--t)">58</text>
  <text x="12" y="48" font-size="9" font-weight="700" fill="var(--t)">91</text>

  <!-- 底部图例（横向排列） -->
  <rect x="10" y="135" width="6" height="6" rx="1" fill="url(#pag1)"/>
  <text x="19" y="141" font-size="7" fill="var(--dt)">A</text>
  <rect x="28" y="135" width="6" height="6" rx="1" fill="url(#pag2)"/>
  <text x="37" y="141" font-size="7" fill="var(--dt)">B</text>
  <rect x="46" y="135" width="6" height="6" rx="1" fill="url(#pag3)"/>
  <text x="55" y="141" font-size="7" fill="var(--dt)">C</text>
  <rect x="64" y="135" width="6" height="6" rx="1" fill="url(#pag4)"/>
  <text x="73" y="141" font-size="7" fill="var(--dt)">D</text>
  <rect x="82" y="135" width="6" height="6" rx="1" fill="url(#pag5)"/>
  <text x="91" y="141" font-size="7" fill="var(--dt)">E</text>
  <rect x="100" y="135" width="6" height="6" rx="1" fill="url(#pag6)"/>
  <text x="109" y="141" font-size="7" fill="var(--dt)">F</text>
</svg>
```

**与雷达图的区别：**
```
雷达图：顶点连线形成多边形，强调轮廓
极坐标面积图：每个扇形独立，半径=数值，强调量级差异

适用场景：
- 雷达图：多维度综合评分（如能力六边形）
- 极坐标面积图：周期性数据（如 12 月销售额）、分类量级对比
```

**计算公式：**
```
中心点 (75, 75)，最大半径 R=60
每扇形角度 = 360° / 分类数

扇形半径 ri = R × (值 i / 最大值)

6 分类示例（每扇 60°）：
值：85, 62, 45, 73, 58, 91
最大值：91
r1 = 60 × (85/91) ≈ 56px
r2 = 60 × (62/91) ≈ 41px
...
```
