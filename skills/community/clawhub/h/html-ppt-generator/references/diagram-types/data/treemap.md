# treemap · 树图

**适用：** 市场份额/资产组合、分类占比、文件/预算结构可视化
**高度：** 160–200px

**结构公式：** 递归矩形分割（Squarified），父节点=大矩形，子节点=内部小矩形拼贴，面积∝价值。

**布局算法（简化版，适合 4–8 个节点）：**
```
按值从大到小排序
交替水平/垂直切分剩余矩形
每个节点：<rect> + 内部 <text>（名称 + 值）
颜色：按层级用渐变或按分类用色相区分
最小可见节点尺寸：40×30px（小于此不显示标签）
```

```html
<svg viewBox="0 0 600 180" style="width:100%;height:180px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 节点A：38% → 宽228，高180 -->
  <rect x="0"   y="0" width="228" height="180" rx="2" fill="rgba(59,130,246,0.25)" stroke="rgba(59,130,246,0.5)" stroke-width="1"/>
  <text x="114" y="86" text-anchor="middle" font-size="12" font-weight="700" fill="#93c5fd">类别A</text>
  <text x="114" y="102" text-anchor="middle" font-size="10" fill="#64748b">38%</text>
  <!-- 节点B：25% → 宽150，高180 上半 -->
  <rect x="230" y="0" width="150" height="108" rx="2" fill="rgba(139,92,246,0.25)" stroke="rgba(139,92,246,0.5)" stroke-width="1"/>
  <text x="305" y="50" text-anchor="middle" font-size="11" font-weight="700" fill="#c4b5fd">类别B</text>
  <text x="305" y="65" text-anchor="middle" font-size="9.5" fill="#64748b">25%</text>
  <!-- 节点C：18% → 宽150，高180 下半 -->
  <rect x="230" y="110" width="150" height="70" rx="2" fill="rgba(6,182,212,0.25)" stroke="rgba(6,182,212,0.5)" stroke-width="1"/>
  <text x="305" y="149" text-anchor="middle" font-size="10" font-weight="700" fill="#67e8f9">类别C</text>
  <text x="305" y="163" text-anchor="middle" font-size="9" fill="#64748b">18%</text>
  <!-- 节点D：12% -->
  <rect x="382" y="0" width="110" height="108" rx="2" fill="rgba(245,158,11,0.25)" stroke="rgba(245,158,11,0.5)" stroke-width="1"/>
  <text x="437" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="#fcd34d">类别D</text>
  <text x="437" y="64" text-anchor="middle" font-size="9" fill="#64748b">12%</text>
  <!-- 节点E：7% -->
  <rect x="382" y="110" width="110" height="70" rx="2" fill="rgba(16,185,129,0.25)" stroke="rgba(16,185,129,0.5)" stroke-width="1"/>
  <text x="437" y="149" text-anchor="middle" font-size="10" font-weight="700" fill="#6ee7b7">类别E</text>
  <text x="437" y="163" text-anchor="middle" font-size="9" fill="#64748b">7%</text>
  <!-- 右侧补充区 -->
  <rect x="494" y="0" width="106" height="180" rx="2" fill="rgba(239,68,68,0.15)" stroke="rgba(239,68,68,0.3)" stroke-width="1"/>
  <text x="547" y="86" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fca5a5">其他</text>
  <text x="547" y="100" text-anchor="middle" font-size="9" fill="#64748b">合计</text>
  <text x="547" y="113" text-anchor="middle" font-size="9" fill="#64748b">100%</text>
</svg>
```

**参数说明：**
- 各节点宽/高 ∝ 该节点值占总值比例；精确计算：宽 = 总宽 × 节点% / 行占比
- 节点间距 2px（stroke-width=1，矩形间留 2px 间隔）
- 颜色：每个顶层分类用独立色相的 rgba(r,g,b,0.25) + 同色系边框
- 文字：节点面积≥60×40px 才显示双行（名称+值），小节点只显示名称
