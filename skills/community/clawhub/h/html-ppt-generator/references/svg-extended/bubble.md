# bubble · 气泡图

**适用：** 三维度对比（X 轴 + Y 轴 + 气泡大小）、四象限分析、市场定位
**尺寸：** 160×120px

```html
<svg viewBox="0 0 160 120" style="width:160px;height:120px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#2563eb" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="bg2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#059669" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="bg3" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#d97706" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="bg4" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ef4444" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#dc2626" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="bg5" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#7c3aed" stop-opacity="0.8"/>
    </linearGradient>
  </defs>

  <!-- 背景网格线 -->
  <line x1="30" y1="10" x2="30" y2="100" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <line x1="80" y1="10" x2="80" y2="100" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <line x1="130" y1="10" x2="130" y2="100" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <line x1="30" y1="100" x2="130" y2="100" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <line x1="30" y1="55" x2="130" y2="55" stroke="rgba(255,255,255,0.08)" stroke-width="1" stroke-dasharray="3,2"/>

  <!-- 象限标签 -->
  <text x="35" y="25" font-size="8" fill="var(--dt)">高增长·低份额</text>
  <text x="85" y="25" font-size="8" fill="var(--dt)">明星</text>
  <text x="35" y="85" font-size="8" fill="var(--dt)">瘦狗</text>
  <text x="85" y="85" font-size="8" fill="var(--dt)">现金牛</text>

  <!-- 气泡 1: 高 X 高 Y 大 -->
  <circle cx="105" cy="30" r="18" fill="url(#bg1)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="105" cy="33" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">A</text>

  <!-- 气泡 2: 中 X 中 Y 中 -->
  <circle cx="75" cy="55" r="12" fill="url(#bg2)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="75" y="58" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">B</text>

  <!-- 气泡 3: 低 X 高 Y 小 -->
  <circle cx="45" cy="25" r="8" fill="url(#bg3)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="45" y="28" text-anchor="middle" font-size="8" font-weight="700" fill="#fff">C</text>

  <!-- 气泡 4: 高 X 低 Y 中 -->
  <circle cx="110" cy="80" r="14" fill="url(#bg4)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="110" y="83" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">D</text>

  <!-- 气泡 5: 低 X 中 Y 小 -->
  <circle cx="50" cy="60" r="6" fill="url(#bg5)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="50" y="63" text-anchor="middle" font-size="7" font-weight="700" fill="#fff">E</text>

  <!-- X 轴标签 -->
  <line x1="30" y1="105" x2="130" y2="105" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
  <text x="30" y="115" text-anchor="middle" font-size="8" fill="var(--dt)">0</text>
  <text x="80" y="115" text-anchor="middle" font-size="8" fill="var(--dt)">50</text>
  <text x="130" y="115" text-anchor="middle" font-size="8" fill="var(--dt)">100</text>
  <text x="80" y="118" text-anchor="middle" font-size="8" fill="var(--dt)">市场份额 (%)</text>

  <!-- Y 轴标签 -->
  <text x="8" y="15" font-size="8" fill="var(--dt)">100</text>
  <text x="8" y="60" font-size="8" fill="var(--dt)">50</text>
  <text x="8" y="105" font-size="8" fill="var(--dt)">0</text>
  <text x="5" y="60" font-size="8" fill="var(--dt)" transform="rotate(-90, 15, 60)">增长率 (%)</text>

  <!-- 图例（气泡大小说明） -->
  <circle cx="145" cy="25" r="8" fill="url(#bg1)" opacity="0.6"/>
  <text x="158" y="28" font-size="7" fill="var(--dt)">高营收</text>
  <circle cx="145" cy="40" r="5" fill="url(#bg1)" opacity="0.6"/>
  <text x="158" y="43" font-size="7" fill="var(--dt)">中营收</text>
  <circle cx="145" cy="55" r="3" fill="url(#bg1)" opacity="0.6"/>
  <text x="158" y="58" font-size="7" fill="var(--dt)">低营收</text>
</svg>
```

**坐标计算：**
```
绘图区：X[30-130]，Y[10-100]
X 轴范围：0-100（市场份额%）
Y 轴范围：0-100（增长率%）

数据点 (x, y) → SVG 坐标：
svgX = 30 + (x / 100) × 100
svgY = 100 - (y / 100) × 90

气泡半径计算（营收）：
r = 5 + (营收 / 最大营收) × 15
最小半径 5px，最大半径 20px
```

**典型应用场景：**
```
1. BCG 矩阵：份额 (X) × 增长 (Y)，气泡=营收
2. 风险评估：概率 (X) × 影响 (Y)，气泡=暴露金额
3. 产品分析：用户数 (X) × 留存率 (Y)，气泡=ARPU
4. 市场分析：覆盖率 (X) × 满意度 (Y)，气泡=市场份额
```
