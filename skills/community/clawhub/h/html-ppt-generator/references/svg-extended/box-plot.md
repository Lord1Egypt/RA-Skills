# box-plot · 箱线图

**适用：** 统计分布、四分位数分析、异常值检测、多组数据对比
**尺寸：** 160×100px

```html
<svg viewBox="0 0 160 100" style="width:160px;height:100px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bpg1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
    <linearGradient id="bpg2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="bpg3" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#d97706"/>
    </linearGradient>
  </defs>

  <!-- 背景网格 -->
  <line x1="10" y1="20" x2="160" y2="20" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
  <line x1="10" y1="40" x2="160" y2="40" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
  <line x1="10" y1="60" x2="160" y2="60" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
  <line x1="10" y1="80" x2="160" y2="80" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>

  <!-- Y 轴标签 -->
  <text x="5" y="23" font-size="8" fill="var(--dt)">100</text>
  <text x="5" y="43" font-size="8" fill="var(--dt)">75</text>
  <text x="5" y="63" font-size="8" fill="var(--dt)">50</text>
  <text x="5" y="83" font-size="8" fill="var(--dt)">25</text>

  <!-- 箱线图 1：组 A（30-90，中位 60） -->
  <!-- 须线（最小值 -Q1） -->
  <line x1="30" y1="50" x2="30" y2="30" stroke="url(#bpg1)" stroke-width="2"/>
  <!-- 须线（Q3-最大值） -->
  <line x1="30" y1="70" x2="30" y2="90" stroke="url(#bpg1)" stroke-width="2"/>
  <!-- 箱体（Q1-Q3） -->
  <rect x="22" y="50" width="16" height="20" fill="url(#bpg1)" opacity="0.3" stroke="url(#bpg1)" stroke-width="2"/>
  <!-- 中位线 -->
  <line x1="22" y1="60" x2="38" y2="60" stroke="url(#bpg1)" stroke-width="2.5"/>
  <!-- 均值点 -->
  <circle cx="30" cy="58" r="3" fill="#fff" stroke="url(#bpg1)" stroke-width="1.5"/>
  <!-- 异常值 -->
  <circle cx="30" cy="18" r="2.5" fill="#ef4444" stroke="#dc2626" stroke-width="1"/>

  <!-- 箱线图 2：组 B（25-85，中位 55） -->
  <line x1="70" y1="55" x2="70" y2="35" stroke="url(#bpg2)" stroke-width="2"/>
  <line x1="70" y1="75" x2="70" y2="95" stroke="url(#bpg2)" stroke-width="2"/>
  <rect x="62" y="55" width="16" height="20" fill="url(#bpg2)" opacity="0.3" stroke="url(#bpg2)" stroke-width="2"/>
  <line x1="62" y1="65" x2="78" y2="65" stroke="url(#bpg2)" stroke-width="2.5"/>
  <circle cx="70" cy="62" r="3" fill="#fff" stroke="url(#bpg2)" stroke-width="1.5"/>

  <!-- 箱线图 3：组 C（40-95，中位 70） -->
  <line x1="110" y1="40" x2="110" y2="20" stroke="url(#bpg3)" stroke-width="2"/>
  <line x1="110" y1="60" x2="110" y2="80" stroke="url(#bpg3)" stroke-width="2"/>
  <rect x="102" y="40" width="16" height="20" fill="url(#bpg3)" opacity="0.3" stroke="url(#bpg3)" stroke-width="2"/>
  <line x1="102" y1="50" x2="118" y2="50" stroke="url(#bpg3)" stroke-width="2.5"/>
  <circle cx="110" cy="48" r="3" fill="#fff" stroke="url(#bpg3)" stroke-width="1.5"/>
  <!-- 异常值（低） -->
  <circle cx="110" cy="98" r="2.5" fill="#ef4444" stroke="#dc2626" stroke-width="1"/>

  <!-- X 轴标签 -->
  <text x="30" y="108" text-anchor="middle" font-size="9" font-weight="600" fill="var(--t)">A 组</text>
  <text x="70" y="108" text-anchor="middle" font-size="9" font-weight="600" fill="var(--t)">B 组</text>
  <text x="110" y="108" text-anchor="middle" font-size="9" font-weight="600" fill="var(--t)">C 组</text>

  <!-- 图例说明 -->
  <line x1="135" y1="15" x2="145" y2="15" stroke="var(--t)" stroke-width="2"/>
  <text x="148" y="18" font-size="7" fill="var(--dt)">中位数</text>
  <circle cx="140" cy="28" r="2.5" fill="#fff" stroke="var(--t)" stroke-width="1.5"/>
  <text x="148" y="31" font-size="7" fill="var(--dt)">均值</text>
  <circle cx="140" cy="42" r="2.5" fill="#ef4444"/>
  <text x="148" y="45" font-size="7" fill="var(--dt)">异常值</text>

  <!-- 统计摘要 -->
  <text x="135" y="60" font-size="7" fill="var(--dt)">A 组最高</text>
  <text x="135" y="70" font-size="9" font-weight="700" fill="var(--t)">90.2</text>
  <text x="135" y="82" font-size="7" fill="var(--dt)">C 组中位</text>
  <text x="135" y="92" font-size="9" font-weight="700" fill="var(--gold)">70.5</text>
</svg>
```

**箱体结构说明：**
```
箱体 = 四分位距 IQR（Q1 到 Q3，包含 50% 数据）
中位线 = Q2（50 百分位）
须线 = Q1-1.5×IQR 到 Q3+1.5×IQR 范围
异常值 = 超出须线范围的点（单独标记）

坐标映射（示例数据 25-95）：
svgY = 80 - (值 - 25) / (95 - 25) × 60

A 组示例：
最小值 = 30 → y=50
Q1 = 50 → y=70
中位 = 60 → y=60
Q3 = 70 → y=50
最大值 = 90 → y=30
异常值 = 98 → y=18
```

**使用场景：**
```
- 多组数据分布对比（3-6 组）
- 识别异常值和离群点
- 展示数据集中趋势和离散程度
- 实验前后对比分析
- A/B 测试结果分布
```
