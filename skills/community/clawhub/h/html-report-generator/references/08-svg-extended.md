# 08 · SVG 扩展图表库

> 补充 05-content.md 中6种基础图表未覆盖的高频图表类型。
> 所有图表必须有**真实数据标签**，禁止纯装饰。

---

## 使用原则

```
图表选型规则：
- 占比/构成    → 圆环图（饼图避免超过5块）
- 相关性       → 散点图
- 流程/决策    → 流程图（箭头方框）
- 层级/树状    → 树状图 / 矩阵树图
- 二维密度     → 热力矩阵
- 多指标评分   → 雷达图（已在05中）
- 趋势变化     → 折线/面积图（已在05中）
- 量级对比     → 柱/条形图（已在05中）
```

---

## 图表 7 · 圆环图（Donut，130×130px）

**适用：** 占比分析、完成率、市场份额

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
  <!-- 数据段1：68%（stroke-dasharray: 周长×68% 周长×32%，周长≈301） -->
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
周长 = 2 × π × r = 2 × 3.14159 × 48 ≈ 301.6
某段占比P%的弧长 = 301.6 × P%
dasharray = "弧长 (301.6-弧长)"
dashoffset起始偏移（从顶部12点开始）= -75.4（即 301.6×25%）
```

---

## 图表 8 · 散点图（Scatter，120×90px）

**适用：** 相关性分析、风险矩阵、二维分布

```html
<svg viewBox="0 0 260 110" style="width:100%;height:110px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 坐标轴 -->
  <line x1="30" y1="8" x2="30" y2="85" stroke="#1e293b" stroke-width="1"/>
  <line x1="30" y1="85" x2="250" y2="85" stroke="#1e293b" stroke-width="1"/>
  <!-- 参考线（四象限分割） -->
  <line x1="30" y1="46" x2="250" y2="46" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="3,3"/>
  <line x1="140" y1="8" x2="140" y2="85" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="3,3"/>
  <!-- 数据点（每个圆圈代表一个数据） -->
  <circle cx="55"  cy="70" r="5" fill="var(--p)" opacity="0.8"/>
  <circle cx="80"  cy="58" r="7" fill="var(--p)" opacity="0.8"/>
  <circle cx="105" cy="48" r="5" fill="var(--p)" opacity="0.8"/>
  <circle cx="130" cy="35" r="9" fill="#ef4444" opacity="0.8"/>  <!-- 异常点/重点 -->
  <circle cx="160" cy="30" r="5" fill="var(--p)" opacity="0.8"/>
  <circle cx="185" cy="22" r="6" fill="var(--p)" opacity="0.8"/>
  <circle cx="210" cy="18" r="5" fill="#10b981" opacity="0.8"/>
  <circle cx="235" cy="15" r="7" fill="#10b981" opacity="0.8"/>
  <!-- 趋势线 -->
  <line x1="42" y1="75" x2="245" y2="10" stroke="var(--p)" stroke-width="1" stroke-dasharray="4,2" opacity="0.4"/>
  <!-- 轴标签 -->
  <text x="140" y="99" text-anchor="middle" font-size="8.5" fill="#64748b">X轴：指标A</text>
  <text x="10" y="46" text-anchor="middle" font-size="8.5" fill="#64748b" transform="rotate(-90,10,46)">Y轴：指标B</text>
  <!-- 象限标注 -->
  <text x="85"  y="20" font-size="7.5" fill="#475569">低A·高B</text>
  <text x="170" y="20" font-size="7.5" fill="#475569">高A·高B</text>
  <text x="170" y="80" font-size="7.5" fill="#475569">高A·低B</text>
</svg>
```

---

## 图表 9 · 流程图（带箭头，全宽）

**适用：** 处理流程、决策树、系统架构、攻击链

### 变体 9a · 横向线性流程（4步，60px高）

```html
<svg viewBox="0 0 940 60" style="width:100%;height:60px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#475569"/>
    </marker>
  </defs>
  <!-- 步骤1 -->
  <rect x="0"   y="8" width="190" height="38" rx="5" fill="var(--pm)" stroke="var(--bd)" stroke-width="1"/>
  <text x="95"  y="24" text-anchor="middle" font-size="10" font-weight="700" fill="var(--p)">步骤 01</text>
  <text x="95"  y="38" text-anchor="middle" font-size="9" fill="var(--mt)">阶段名称</text>
  <!-- 箭头 -->
  <line x1="194" y1="27" x2="218" y2="27" stroke="#475569" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- 步骤2 -->
  <rect x="220" y="8" width="190" height="38" rx="5" fill="var(--pm)" stroke="var(--bd)" stroke-width="1"/>
  <text x="315" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="var(--p)">步骤 02</text>
  <text x="315" y="38" text-anchor="middle" font-size="9" fill="var(--mt)">阶段名称</text>
  <!-- 箭头 -->
  <line x1="414" y1="27" x2="438" y2="27" stroke="#475569" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- 步骤3（强调，用实色） -->
  <rect x="440" y="8" width="190" height="38" rx="5" fill="var(--p)"/>
  <text x="535" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">步骤 03</text>
  <text x="535" y="38" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.7)">关键阶段</text>
  <!-- 箭头 -->
  <line x1="634" y1="27" x2="658" y2="27" stroke="#475569" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- 步骤4 -->
  <rect x="660" y="8" width="190" height="38" rx="5" fill="rgba(16,185,129,0.12)" stroke="rgba(16,185,129,0.3)" stroke-width="1"/>
  <text x="755" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="#10b981">步骤 04</text>
  <text x="755" y="38" text-anchor="middle" font-size="9" fill="#6ee7b7">完成</text>
  <!-- 完成标记 -->
  <circle cx="920" cy="27" r="16" fill="rgba(16,185,129,0.15)" stroke="#10b981" stroke-width="1.5"/>
  <text x="920" y="32" text-anchor="middle" font-size="14" fill="#10b981">✓</text>
  <line x1="854" y1="27" x2="900" y2="27" stroke="#475569" stroke-width="1.5" marker-end="url(#arr)"/>
</svg>
```

### 变体 9b · 菱形决策节点（垂直，带分支）

```html
<svg viewBox="0 0 300 200" style="width:100%;height:200px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr2" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto">
      <path d="M0,0 L0,5 L5,2.5 z" fill="#475569"/>
    </marker>
  </defs>
  <!-- 开始 -->
  <rect x="100" y="5" width="100" height="30" rx="15" fill="var(--p)"/>
  <text x="150" y="25" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">开始条件</text>
  <!-- 向下箭头 -->
  <line x1="150" y1="35" x2="150" y2="55" stroke="#475569" stroke-width="1.5" marker-end="url(#arr2)"/>
  <!-- 决策菱形 -->
  <polygon points="150,58 210,85 150,112 90,85" fill="rgba(245,158,11,0.15)" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="150" y="89" text-anchor="middle" font-size="9" font-weight="600" fill="#f59e0b">条件判断?</text>
  <!-- 是：向右 -->
  <line x1="210" y1="85" x2="248" y2="85" stroke="#475569" stroke-width="1.5" marker-end="url(#arr2)"/>
  <text x="228" y="80" text-anchor="middle" font-size="8" fill="#10b981">是</text>
  <rect x="250" y="70" width="46" height="30" rx="4" fill="rgba(16,185,129,0.15)" stroke="#10b981" stroke-width="1"/>
  <text x="273" y="89" text-anchor="middle" font-size="9" font-weight="600" fill="#10b981">执行A</text>
  <!-- 否：向左 -->
  <line x1="90" y1="85" x2="52" y2="85" stroke="#475569" stroke-width="1.5" marker-end="url(#arr2)"/>
  <text x="70" y="80" text-anchor="middle" font-size="8" fill="#ef4444">否</text>
  <rect x="4" y="70" width="46" height="30" rx="4" fill="rgba(239,68,68,0.15)" stroke="#ef4444" stroke-width="1"/>
  <text x="27" y="89" text-anchor="middle" font-size="9" font-weight="600" fill="#ef4444">执行B</text>
  <!-- 两侧向下汇合 -->
  <line x1="273" y1="100" x2="273" y2="160" stroke="#475569" stroke-width="1" stroke-dasharray="3,2"/>
  <line x1="27"  y1="100" x2="27"  y2="160" stroke="#475569" stroke-width="1" stroke-dasharray="3,2"/>
  <line x1="27"  y1="160" x2="150" y2="160" stroke="#475569" stroke-width="1.5"/>
  <line x1="273" y1="160" x2="150" y2="160" stroke="#475569" stroke-width="1.5"/>
  <line x1="150" y1="160" x2="150" y2="172" stroke="#475569" stroke-width="1.5" marker-end="url(#arr2)"/>
  <!-- 结束 -->
  <rect x="100" y="174" width="100" height="24" rx="12" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
  <text x="150" y="190" text-anchor="middle" font-size="9" fill="var(--mt)">结果输出</text>
</svg>
```

---

## 图表 10 · 树状层级图（横向，120px高）

**适用：** 组织架构、分类体系、知识树、攻击树

```html
<svg viewBox="0 0 580 120" style="width:100%;height:120px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 根节点 -->
  <rect x="0" y="45" width="100" height="30" rx="4" fill="var(--p)"/>
  <text x="50" y="64" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">根节点</text>
  <!-- 连接线 -->
  <path d="M100,60 C130,60 130,25 160,25" fill="none" stroke="#1e293b" stroke-width="1.5"/>
  <path d="M100,60 C130,60 130,60 160,60" fill="none" stroke="#1e293b" stroke-width="1.5"/>
  <path d="M100,60 C130,60 130,95 160,95" fill="none" stroke="#1e293b" stroke-width="1.5"/>
  <!-- 二级节点 -->
  <rect x="160" y="10" width="100" height="28" rx="4" fill="var(--pm)" stroke="var(--bd)" stroke-width="1"/>
  <text x="210" y="28" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--t)">分类 A</text>
  <rect x="160" y="46" width="100" height="28" rx="4" fill="var(--pm)" stroke="var(--bd)" stroke-width="1"/>
  <text x="210" y="64" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--t)">分类 B</text>
  <rect x="160" y="82" width="100" height="28" rx="4" fill="var(--pm)" stroke="var(--bd)" stroke-width="1"/>
  <text x="210" y="100" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--t)">分类 C</text>
  <!-- A的子节点 -->
  <path d="M260,24 C290,24 290,16 320,16" fill="none" stroke="#1e293b" stroke-width="1"/>
  <path d="M260,24 C290,24 290,32 320,32" fill="none" stroke="#1e293b" stroke-width="1"/>
  <rect x="320" y="6"  width="100" height="22" rx="3" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <text x="370" y="21" text-anchor="middle" font-size="8.5" fill="var(--mt)">子项 A1</text>
  <rect x="320" y="32" width="100" height="22" rx="3" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <text x="370" y="47" text-anchor="middle" font-size="8.5" fill="var(--mt)">子项 A2</text>
  <!-- B的子节点（单个） -->
  <path d="M260,60 H320" fill="none" stroke="#1e293b" stroke-width="1"/>
  <rect x="320" y="49" width="100" height="22" rx="3" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <text x="370" y="64" text-anchor="middle" font-size="8.5" fill="var(--mt)">子项 B1</text>
  <!-- C的子节点 -->
  <path d="M260,96 C290,96 290,85 320,85" fill="none" stroke="#1e293b" stroke-width="1"/>
  <path d="M260,96 C290,96 290,107 320,107" fill="none" stroke="#1e293b" stroke-width="1"/>
  <rect x="320" y="74"  width="100" height="22" rx="3" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <text x="370" y="89"  text-anchor="middle" font-size="8.5" fill="var(--mt)">子项 C1</text>
  <rect x="320" y="99"  width="100" height="22" rx="3" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <text x="370" y="114" text-anchor="middle" font-size="8.5" fill="var(--mt)">子项 C2</text>
</svg>
```

---

## 图表 11 · 热力矩阵（Heatmap，5×4，90px高）

**适用：** 风险矩阵、时间×维度交叉、相关性热图

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
  <!-- 单元格（颜色深浅表示值大小，使用主色opacity变化） -->
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

---

## 图表 12 · 瀑布图（Waterfall，80px高）

**适用：** 累计变化、利润分解、预算增减

```html
<svg viewBox="0 0 400 80" style="width:100%;height:80px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 基准线 -->
  <line x1="20" y1="60" x2="380" y2="60" stroke="#1e293b" stroke-width="1"/>
  <!-- 起始柱（基准） -->
  <rect x="30" y="20" width="40" height="40" rx="2" fill="var(--p)"/>
  <text x="50" y="16" text-anchor="middle" font-size="8" fill="var(--mt)">基准</text>
  <text x="50" y="71" text-anchor="middle" font-size="7.5" fill="#64748b">100</text>
  <!-- 连接虚线 -->
  <line x1="70" y1="20" x2="90" y2="20" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,2"/>
  <!-- 增加柱（绿色，浮动） -->
  <rect x="90" y="10" width="40" height="10" rx="2" fill="#10b981"/>
  <text x="110" y="7"  text-anchor="middle" font-size="8" fill="#10b981">+10</text>
  <text x="110" y="71" text-anchor="middle" font-size="7.5" fill="#64748b">+营收</text>
  <!-- 连接虚线 -->
  <line x1="130" y1="10" x2="150" y2="10" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,2"/>
  <!-- 减少柱（红色，浮动） -->
  <rect x="150" y="10" width="40" height="18" rx="2" fill="#ef4444"/>
  <text x="170" y="7"  text-anchor="middle" font-size="8" fill="#ef4444">-18</text>
  <text x="170" y="71" text-anchor="middle" font-size="7.5" fill="#64748b">-成本</text>
  <!-- 连接虚线 -->
  <line x1="190" y1="28" x2="210" y2="28" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,2"/>
  <!-- 增加柱 -->
  <rect x="210" y="18" width="40" height="10" rx="2" fill="#10b981"/>
  <text x="230" y="15" text-anchor="middle" font-size="8" fill="#10b981">+10</text>
  <text x="230" y="71" text-anchor="middle" font-size="7.5" fill="#64748b">+其他</text>
  <!-- 连接虚线 -->
  <line x1="250" y1="18" x2="270" y2="18" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,2"/>
  <!-- 减少柱 -->
  <rect x="270" y="18" width="40" height="8" rx="2" fill="#ef4444"/>
  <text x="290" y="15" text-anchor="middle" font-size="8" fill="#ef4444">-8</text>
  <text x="290" y="71" text-anchor="middle" font-size="7.5" fill="#64748b">-税费</text>
  <!-- 连接虚线 -->
  <line x1="310" y1="26" x2="330" y2="26" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,2"/>
  <!-- 结果柱 -->
  <rect x="330" y="26" width="40" height="34" rx="2" fill="var(--p)" opacity="0.7"/>
  <text x="350" y="22" text-anchor="middle" font-size="8" fill="var(--mt)">结果</text>
  <text x="350" y="71" text-anchor="middle" font-size="7.5" fill="#64748b">94</text>
  <!-- Y轴刻度 -->
  <text x="18" y="62" font-size="7.5" fill="#64748b" text-anchor="end">0</text>
  <text x="18" y="22" font-size="7.5" fill="#64748b" text-anchor="end">100</text>
</svg>
```

---

## 图表 13 · 双轴图（折线+柱状组合，90px高）

**适用：** 不同量级指标叠加（如数量+比率、成本+增速）

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
  <!-- 右Y轴 -->
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

---

## 图表选型速查

| 数据特征 | 推荐图表 | 编号 |
|---------|---------|------|
| 各部分占总体的比例（≤5项） | 圆环图 | 7 |
| 两变量间的相关关系 | 散点图 | 8 |
| 步骤/决策流程 | 流程图 | 9 |
| 分类层级/树状结构 | 树状图 | 10 |
| 两维度交叉密度 | 热力矩阵 | 11 |
| 累计变化分解 | 瀑布图 | 12 |
| 量级不同的两组数据 | 双轴图 | 13 |
| 时间趋势 | 折线/面积图 | 2（05中）|
| 量级对比（同类） | 横条/柱状图 | 1/6（05中）|
| 多维度综合评分 | 雷达图 | 3（05中）|
