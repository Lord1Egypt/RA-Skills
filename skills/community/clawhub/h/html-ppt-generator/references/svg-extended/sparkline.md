# sparkline · 迷你走势线

**适用：** 卡片内嵌趋势辅助、数字卡旁边的小型趋势线
**高度：** 30px（超紧凑，不占主内容空间）

---

## 变体 A · 单线上升趋势（30px）

```html
<svg viewBox="0 0 200 30" style="width:100%;height:30px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="spk1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="var(--p)" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="var(--p)" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <polygon points="0,22 25,18 50,20 75,14 100,16 125,10 150,8 175,5 200,3 200,28 0,28" fill="url(#spk1)"/>
  <polyline points="0,22 25,18 50,20 75,14 100,16 125,10 150,8 175,5 200,3"
            fill="none" stroke="var(--p)" stroke-width="1.5"/>
  <circle cx="200" cy="3" r="2.5" fill="var(--p)"/>
</svg>
```

---

## 变体 B · 双线对比（35px）

```html
<svg viewBox="0 0 200 35" style="width:100%;height:35px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 线A（主色，上升） -->
  <polyline points="0,28 33,22 66,20 100,14 133,12 166,8 200,5"
            fill="none" stroke="var(--p)" stroke-width="1.5"/>
  <!-- 线B（对比色，下降） -->
  <polyline points="0,10 33,14 66,16 100,18 133,22 166,24 200,27"
            fill="none" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,2"/>
  <circle cx="200" cy="5"  r="2.5" fill="var(--p)"/>
  <circle cx="200" cy="27" r="2.5" fill="#ef4444"/>
  <!-- 图例 -->
  <line x1="0" y1="33" x2="10" y2="33" stroke="var(--p)" stroke-width="1.5"/>
  <text x="13" y="35" font-size="7" fill="#64748b">指标A</text>
  <line x1="50" y1="33" x2="60" y2="33" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="63" y="35" font-size="7" fill="#64748b">指标B</text>
</svg>
```

---

## 变体 C · 带异常高亮（30px）

```html
<svg viewBox="0 0 200 30" style="width:100%;height:30px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="spk3" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="var(--p)" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="var(--p)" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <polygon points="0,20 28,18 57,22 85,16 114,24 142,8 171,12 200,10 200,27 0,27" fill="url(#spk3)"/>
  <polyline points="0,20 28,18 57,22 85,16 114,24 142,8 171,12 200,10"
            fill="none" stroke="var(--p)" stroke-width="1.5"/>
  <!-- 异常峰值高亮 -->
  <circle cx="142" cy="8"  r="3.5" fill="#ef4444"/>
  <line x1="142" y1="8" x2="142" y2="27" stroke="#ef4444" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.5"/>
  <text x="142" y="6" text-anchor="middle" font-size="7" fill="#ef4444">峰值</text>
  <!-- 末尾最新值 -->
  <circle cx="200" cy="10" r="2.5" fill="var(--p)"/>
</svg>
```

**参数说明：**
- Y 可用区间 3–27px（高度24px）
- Y坐标 = 27 - (值/最大值) × 24
- 末尾圆点高亮最新数据；异常点用 #ef4444
- 适合放在数字卡下方作趋势辅助，不占独立行
