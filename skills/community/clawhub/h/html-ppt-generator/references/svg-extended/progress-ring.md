# progress-ring · 圆形进度环

**适用：** 单指标完成率、目标达成度、KPI 环形展示
**尺寸：** 90×90px（小）/ 120×120px（标准）

---

## 变体 A · 单环标准（90px）

```html
<svg viewBox="0 0 90 90" style="width:90px;height:90px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="rg1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="var(--p)"/>
      <stop offset="100%" stop-color="#8b5cf6"/>
    </linearGradient>
  </defs>
  <!-- 背景轨道 -->
  <circle cx="45" cy="45" r="36" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="8"/>
  <!-- 进度弧（78%：周长=2π×36≈226.2，弧长=176.4） -->
  <circle cx="45" cy="45" r="36" fill="none" stroke="url(#rg1)" stroke-width="8"
          stroke-dasharray="176.4 49.8" stroke-dashoffset="56.5"
          stroke-linecap="round"/>
  <!-- 中心文字 -->
  <text x="45" y="41" text-anchor="middle" font-size="16" font-weight="800" fill="var(--t)" letter-spacing="-0.5">78%</text>
  <text x="45" y="53" text-anchor="middle" font-size="7" fill="var(--dt)">完成率</text>
</svg>
```

---

## 变体 B · 双环对比（120px）

```html
<svg viewBox="0 0 120 120" style="width:120px;height:120px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="rg2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="var(--p)"/>
      <stop offset="100%" stop-color="#6366f1"/>
    </linearGradient>
  </defs>
  <!-- 外环轨道（r=50） -->
  <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="7"/>
  <!-- 外环进度（85%：C=314.2，弧=267.1） -->
  <circle cx="60" cy="60" r="50" fill="none" stroke="url(#rg2)" stroke-width="7"
          stroke-dasharray="267.1 47.1" stroke-dashoffset="78.5"
          stroke-linecap="round"/>
  <!-- 内环轨道（r=37） -->
  <circle cx="60" cy="60" r="37" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="6"/>
  <!-- 内环进度（62%：C=232.5，弧=144.1） -->
  <circle cx="60" cy="60" r="37" fill="none" stroke="#10b981" stroke-width="6"
          stroke-dasharray="144.1 88.4" stroke-dashoffset="58.1"
          stroke-linecap="round"/>
  <!-- 中心文字 -->
  <text x="60" y="55" text-anchor="middle" font-size="18" font-weight="800" fill="var(--t)" letter-spacing="-1">85%</text>
  <text x="60" y="67" text-anchor="middle" font-size="8" fill="var(--dt)">目标A</text>
  <!-- 图例 -->
  <line x1="15" y1="105" x2="28" y2="105" stroke="url(#rg2)" stroke-width="3" stroke-linecap="round"/>
  <text x="32" y="108" font-size="8" fill="#94a3b8">指标A 85%</text>
  <line x1="70" y1="105" x2="83" y2="105" stroke="#10b981" stroke-width="3" stroke-linecap="round"/>
  <text x="87" y="108" font-size="8" fill="#94a3b8">指标B 62%</text>
</svg>
```

**圆弧计算公式：**
```
周长 C = 2 × π × r
弧长 = C × 占比
dasharray = "弧长  (C - 弧长)"
dashoffset（12点起）= C × 25%
```
