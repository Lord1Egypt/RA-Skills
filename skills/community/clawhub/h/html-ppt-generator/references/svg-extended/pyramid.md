# pyramid · 金字塔图

**适用：** 层级结构、漏斗转化、人口年龄结构、优先级排序
**尺寸：** 140×140px

```html
<svg viewBox="0 0 140 140" style="width:140px;height:140px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="pyg1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
    <linearGradient id="pyg2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#06b6d4"/>
      <stop offset="100%" stop-color="#0891b2"/>
    </linearGradient>
    <linearGradient id="pyg3" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="pyg4" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#d97706"/>
    </linearGradient>
  </defs>
  <!-- 层级 1（顶层，最小） -->
  <polygon points="52,20 88,20 80,45 60,45"
           fill="url(#pyg4)" opacity="0.95"/>
  <text x="70" y="37" text-anchor="middle" font-size="8" font-weight="700" fill="#fff">15%</text>
  <text x="95" y="36" font-size="8" fill="var(--mt)">决策层</text>

  <!-- 层级 2 -->
  <polygon points="42,45 98,45 88,70 52,70"
           fill="url(#pyg3)" opacity="0.9"/>
  <text x="70" y="62" text-anchor="middle" font-size="8" font-weight="700" fill="#fff">25%</text>
  <text x="95" y="61" font-size="8" fill="var(--mt)">管理层</text>

  <!-- 层级 3 -->
  <polygon points="32,70 108,70 98,95 42,95"
           fill="url(#pyg2)" opacity="0.85"/>
  <text x="70" y="87" text-anchor="middle" font-size="8" font-weight="700" fill="#fff">35%</text>
  <text x="95" y="86" font-size="8" fill="var(--mt)">执行层</text>

  <!-- 层级 4（底层，最大） -->
  <polygon points="22,95 118,95 108,120 32,120"
           fill="url(#pyg1)" opacity="0.8"/>
  <text x="70" y="112" text-anchor="middle" font-size="8" font-weight="700" fill="#fff">25%</text>
  <text x="95" y="111" font-size="8" fill="var(--mt)">基础层</text>

  <!-- 左侧标签（可选） -->
  <text x="5" y="36" font-size="7" fill="var(--dt)">N=150</text>
  <text x="5" y="61" font-size="7" fill="var(--dt)">N=250</text>
  <text x="5" y="86" font-size="7" fill="var(--dt)">N=350</text>
  <text x="5" y="111" font-size="7" fill="var(--dt)">N=250</text>
</svg>
```

**尺寸计算（4 层示例）：**
```
总宽 140px，总高 140px
每层高度 = 140 / 4 = 35px（含间隔则 28-30px）

顶层宽 = 总宽 × 0.25 ≈ 36px
底层宽 = 总宽 × 0.75 ≈ 108px
每层递增 = (底层宽 - 顶层宽) / (层数 -1)

坐标计算（中心对齐）：
第 N 层左 x = (140 - 层宽 N) / 2
第 N 层右 x = (140 + 层宽 N) / 2
```

**变体用法：**
```
漏斗图（左对齐）：所有层左 x 对齐，右侧递减
转化漏斗：每层标注转化率（如 100% → 60% → 35% → 15%）
人口金字塔：左右对称，左侧男性右侧女性
```
