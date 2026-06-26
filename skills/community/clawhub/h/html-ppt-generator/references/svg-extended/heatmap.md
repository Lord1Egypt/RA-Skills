# heatmap · 热力矩阵

**适用：** 二维密度、时间×维度交叉、相关性热图
**高度：** 90px（5列×4行）

```html
<svg viewBox="0 0 300 90" style="width:100%;height:90px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 行标签 -->
  <text x="34" y="22" text-anchor="end" font-size="7.5" fill="#64748b">类别1</text>
  <text x="34" y="40" text-anchor="end" font-size="7.5" fill="#64748b">类别2</text>
  <text x="34" y="58" text-anchor="end" font-size="7.5" fill="#64748b">类别3</text>
  <text x="34" y="76" text-anchor="end" font-size="7.5" fill="#64748b">类别4</text>
  <!-- 列标签 -->
  <text x="54"  y="9" text-anchor="middle" font-size="7.5" fill="#64748b">Q1</text>
  <text x="90"  y="9" text-anchor="middle" font-size="7.5" fill="#64748b">Q2</text>
  <text x="126" y="9" text-anchor="middle" font-size="7.5" fill="#64748b">Q3</text>
  <text x="162" y="9" text-anchor="middle" font-size="7.5" fill="#64748b">Q4</text>
  <text x="198" y="9" text-anchor="middle" font-size="7.5" fill="#64748b">Q5</text>
  <!-- 行1 -->
  <rect x="36" y="12" width="34" height="16" rx="2" fill="var(--p)" opacity="0.9"/><text x="53" y="23" text-anchor="middle" font-size="7" fill="#fff">92</text>
  <rect x="72" y="12" width="34" height="16" rx="2" fill="var(--p)" opacity="0.5"/><text x="89" y="23" text-anchor="middle" font-size="7" fill="#fff">51</text>
  <rect x="108" y="12" width="34" height="16" rx="2" fill="var(--p)" opacity="0.3"/><text x="125" y="23" text-anchor="middle" font-size="7" fill="var(--mt)">28</text>
  <rect x="144" y="12" width="34" height="16" rx="2" fill="var(--p)" opacity="0.7"/><text x="161" y="23" text-anchor="middle" font-size="7" fill="#fff">73</text>
  <rect x="180" y="12" width="34" height="16" rx="2" fill="#ef4444" opacity="0.8"/><text x="197" y="23" text-anchor="middle" font-size="7" fill="#fff">88</text>
  <!-- 行2 -->
  <rect x="36" y="30" width="34" height="16" rx="2" fill="var(--p)" opacity="0.2"/><text x="53" y="41" text-anchor="middle" font-size="7" fill="var(--dt)">18</text>
  <rect x="72" y="30" width="34" height="16" rx="2" fill="var(--p)" opacity="0.8"/><text x="89" y="41" text-anchor="middle" font-size="7" fill="#fff">84</text>
  <rect x="108" y="30" width="34" height="16" rx="2" fill="#10b981" opacity="0.7"/><text x="125" y="41" text-anchor="middle" font-size="7" fill="#fff">76</text>
  <rect x="144" y="30" width="34" height="16" rx="2" fill="var(--p)" opacity="0.4"/><text x="161" y="41" text-anchor="middle" font-size="7" fill="var(--mt)">42</text>
  <rect x="180" y="30" width="34" height="16" rx="2" fill="var(--p)" opacity="0.6"/><text x="197" y="41" text-anchor="middle" font-size="7" fill="#fff">63</text>
  <!-- 行3 -->
  <rect x="36" y="48" width="34" height="16" rx="2" fill="#ef4444" opacity="0.9"/><text x="53" y="59" text-anchor="middle" font-size="7" fill="#fff">95</text>
  <rect x="72" y="48" width="34" height="16" rx="2" fill="var(--p)" opacity="0.3"/><text x="89" y="59" text-anchor="middle" font-size="7" fill="var(--mt)">31</text>
  <rect x="108" y="48" width="34" height="16" rx="2" fill="var(--p)" opacity="0.5"/><text x="125" y="59" text-anchor="middle" font-size="7" fill="#fff">54</text>
  <rect x="144" y="48" width="34" height="16" rx="2" fill="#10b981" opacity="0.5"/><text x="161" y="59" text-anchor="middle" font-size="7" fill="#fff">57</text>
  <rect x="180" y="48" width="34" height="16" rx="2" fill="var(--p)" opacity="0.2"/><text x="197" y="59" text-anchor="middle" font-size="7" fill="var(--dt)">21</text>
  <!-- 行4 -->
  <rect x="36" y="66" width="34" height="16" rx="2" fill="var(--p)" opacity="0.4"/><text x="53" y="77" text-anchor="middle" font-size="7" fill="var(--mt)">44</text>
  <rect x="72" y="66" width="34" height="16" rx="2" fill="var(--p)" opacity="0.9"/><text x="89" y="77" text-anchor="middle" font-size="7" fill="#fff">91</text>
  <rect x="108" y="66" width="34" height="16" rx="2" fill="var(--p)" opacity="0.7"/><text x="125" y="77" text-anchor="middle" font-size="7" fill="#fff">72</text>
  <rect x="144" y="66" width="34" height="16" rx="2" fill="#f59e0b" opacity="0.7"/><text x="161" y="77" text-anchor="middle" font-size="7" fill="#fff">69</text>
  <rect x="180" y="66" width="34" height="16" rx="2" fill="var(--p)" opacity="0.5"/><text x="197" y="77" text-anchor="middle" font-size="7" fill="#fff">52</text>
  <!-- 色阶图例 -->
  <defs>
    <linearGradient id="heatLeg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="var(--p)" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="var(--p)" stop-opacity="1"/>
    </linearGradient>
  </defs>
  <rect x="222" y="14" width="70" height="6" rx="2" fill="url(#heatLeg)"/>
  <text x="222" y="28" font-size="7" fill="#64748b">低</text>
  <text x="288" y="28" font-size="7" fill="#64748b" text-anchor="end">高</text>
  <text x="255" y="10" font-size="7" fill="#64748b" text-anchor="middle">数值密度</text>
</svg>
```

**参数说明：**
- opacity 0.1–0.9 表示数值低→高（主色系）
- 异常高值用 #ef4444，正向高值用 #10b981
- 每格 34×16px，行间距 18px，列间距 36px
