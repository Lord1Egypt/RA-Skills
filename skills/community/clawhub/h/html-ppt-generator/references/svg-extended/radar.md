# radar · 雷达图

**适用：** 多维度综合评分、方案对比
**尺寸：** 190×180px
> ⚠ 每份报告雷达图最多出现 **2 次**。

> 颜色使用 Tc CSS 变量：数据集 A 用 `var(--p)`，数据集 B 用 `var(--c2)`。

```html
<svg viewBox="0 0 200 190" style="width:190px;height:180px;" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景网格（3层六边形） -->
  <polygon points="100,12 170,54 170,138 100,180 30,138 30,54"   fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="1.5"/>
  <polygon points="100,36 146,62 146,114 100,140 54,114 54,62"   fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
  <polygon points="100,60 122,74 122,98 100,112 78,98  78,74"    fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="0.8"/>
  <!-- 数据集 A（主色） -->
  <polygon points="100,18 164,60 155,132 100,172 38,126 44,56"
           fill-opacity="0.15" fill="var(--p)" stroke="var(--p)" stroke-width="1.5"/>
  <!-- 数据集 B（第二色，可选） -->
  <polygon points="100,38 136,62 135,106 100,130 64,106 62,58"
           fill-opacity="0.12" fill="var(--c2,#6366f1)" stroke="var(--c2,#6366f1)" stroke-width="1" stroke-dasharray="3,2"/>
  <!-- 轴标签 -->
  <text x="100" y="7"   text-anchor="middle" font-size="8.5" fill="var(--dt)">维度A</text>
  <text x="178" y="57"  font-size="8.5" fill="var(--dt)">维度B</text>
  <text x="178" y="142" font-size="8.5" fill="var(--dt)">维度C</text>
  <text x="100" y="192" text-anchor="middle" font-size="8.5" fill="var(--dt)">维度D</text>
  <text x="2"   y="142" font-size="8.5" fill="var(--dt)" text-anchor="end">维度E</text>
  <text x="2"   y="57"  font-size="8.5" fill="var(--dt)" text-anchor="end">维度F</text>
  <!-- 图例 -->
  <line x1="18" y1="162" x2="32" y2="162" stroke="var(--p)" stroke-width="1.5"/>
  <text x="35" y="165" font-size="8" fill="var(--dt)">方案A</text>
  <line x1="64" y1="162" x2="78" y2="162" stroke="var(--c2,#6366f1)" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="81" y="165" font-size="8" fill="var(--dt)">方案B</text>
</svg>
```

**六边形顶点坐标（中心100,96，半径84）：**
```
上：    (100, 12)
右上：  (170, 54)
右下：  (170, 138)
下：    (100, 180)
左下：  (30,  138)
左上：  (30,  54)
```
数据点坐标 = 中心 + 方向向量 × (值/最大值) × 84
