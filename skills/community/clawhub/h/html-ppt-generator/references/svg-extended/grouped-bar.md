# grouped-bar · 分组柱状图

**适用：** 多组同类指标对比（如A/B两方案各项指标、多年份同维度比较）
**高度：** 90px

---

## 变体 A · 双组对比（90px，5项指标）

```html
<svg viewBox="0 0 290 90" style="width:100%;height:90px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 坐标轴 -->
  <line x1="20" y1="65" x2="280" y2="65" stroke="#1e293b" stroke-width="1"/>
  <line x1="20" y1="45" x2="280" y2="45" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,3"/>
  <line x1="20" y1="25" x2="280" y2="25" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,3"/>
  <text x="16" y="68" font-size="7.5" fill="#64748b" text-anchor="end">0</text>
  <text x="16" y="48" font-size="7.5" fill="#64748b" text-anchor="end">50</text>
  <text x="16" y="28" font-size="7.5" fill="#64748b" text-anchor="end">100</text>

  <!-- 组1（x=30）：A=75%，B=58% -->
  <rect x="30" y="25" width="14" height="40" rx="2" fill="var(--p)" opacity="0.9"/>
  <rect x="46" y="37" width="14" height="28" rx="2" fill="#8b5cf6" opacity="0.85"/>
  <text x="45" y="75" text-anchor="middle" font-size="7.5" fill="#64748b">Q1</text>

  <!-- 组2（x=84） -->
  <rect x="84"  y="18" width="14" height="47" rx="2" fill="var(--p)" opacity="0.9"/>
  <rect x="100" y="30" width="14" height="35" rx="2" fill="#8b5cf6" opacity="0.85"/>
  <text x="99" y="75" text-anchor="middle" font-size="7.5" fill="#64748b">Q2</text>

  <!-- 组3（x=138，强调） -->
  <rect x="138" y="15" width="14" height="50" rx="2" fill="var(--p)"/>
  <rect x="154" y="32" width="14" height="33" rx="2" fill="#ef4444" opacity="0.9"/>
  <text x="153" y="75" text-anchor="middle" font-size="7.5" fill="#64748b">Q3</text>

  <!-- 组4（x=192） -->
  <rect x="192" y="28" width="14" height="37" rx="2" fill="var(--p)" opacity="0.9"/>
  <rect x="208" y="22" width="14" height="43" rx="2" fill="#10b981" opacity="0.85"/>
  <text x="207" y="75" text-anchor="middle" font-size="7.5" fill="#64748b">Q4</text>

  <!-- 组5（x=246） -->
  <rect x="246" y="32" width="14" height="33" rx="2" fill="var(--p)" opacity="0.9"/>
  <rect x="262" y="40" width="14" height="25" rx="2" fill="#8b5cf6" opacity="0.85"/>
  <text x="261" y="75" text-anchor="middle" font-size="7.5" fill="#64748b">Q5</text>

  <!-- 图例 -->
  <rect x="20" y="82" width="8" height="6" rx="1" fill="var(--p)"/>
  <text x="32" y="88" font-size="7.5" fill="#64748b">方案A</text>
  <rect x="80" y="82" width="8" height="6" rx="1" fill="#8b5cf6"/>
  <text x="92" y="88" font-size="7.5" fill="#64748b">方案B</text>
</svg>
```

---

## 变体 B · 三组对比（90px，4项指标）

```html
<svg viewBox="0 0 290 90" style="width:100%;height:90px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <line x1="20" y1="65" x2="280" y2="65" stroke="#1e293b" stroke-width="1"/>
  <line x1="20" y1="40" x2="280" y2="40" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,3"/>

  <!-- 组1（x=25，3柱×12px，间距3px） -->
  <rect x="25" y="35" width="12" height="30" rx="2" fill="var(--p)" opacity="0.9"/>
  <rect x="40" y="45" width="12" height="20" rx="2" fill="#8b5cf6" opacity="0.85"/>
  <rect x="55" y="28" width="12" height="37" rx="2" fill="#10b981" opacity="0.85"/>
  <text x="46" y="75" text-anchor="middle" font-size="7.5" fill="#64748b">Q1</text>

  <!-- 组2（x=90） -->
  <rect x="90"  y="22" width="12" height="43" rx="2" fill="var(--p)" opacity="0.9"/>
  <rect x="105" y="38" width="12" height="27" rx="2" fill="#8b5cf6" opacity="0.85"/>
  <rect x="120" y="32" width="12" height="33" rx="2" fill="#10b981" opacity="0.85"/>
  <text x="111" y="75" text-anchor="middle" font-size="7.5" fill="#64748b">Q2</text>

  <!-- 组3（x=155） -->
  <rect x="155" y="28" width="12" height="37" rx="2" fill="var(--p)" opacity="0.9"/>
  <rect x="170" y="18" width="12" height="47" rx="2" fill="#ef4444" opacity="0.9"/>
  <rect x="185" y="40" width="12" height="25" rx="2" fill="#10b981" opacity="0.85"/>
  <text x="176" y="75" text-anchor="middle" font-size="7.5" fill="#64748b">Q3</text>

  <!-- 组4（x=220） -->
  <rect x="220" y="32" width="12" height="33" rx="2" fill="var(--p)" opacity="0.9"/>
  <rect x="235" y="30" width="12" height="35" rx="2" fill="#8b5cf6" opacity="0.85"/>
  <rect x="250" y="25" width="12" height="40" rx="2" fill="#10b981" opacity="0.85"/>
  <text x="241" y="75" text-anchor="middle" font-size="7.5" fill="#64748b">Q4</text>

  <!-- 图例 -->
  <rect x="20"  y="82" width="8" height="6" rx="1" fill="var(--p)"/>
  <text x="32"  y="88" font-size="7.5" fill="#64748b">2022</text>
  <rect x="70"  y="82" width="8" height="6" rx="1" fill="#8b5cf6"/>
  <text x="82"  y="88" font-size="7.5" fill="#64748b">2023</text>
  <rect x="120" y="82" width="8" height="6" rx="1" fill="#10b981"/>
  <text x="132" y="88" font-size="7.5" fill="#64748b">2024</text>
</svg>
```

**参数说明：**
- 双组：每组2柱，柱宽14px，组内间距2px，组间距42px
- 三组：每组3柱，柱宽12px，组内间距3px，组间距55px
- Y轴范围：y=65（底）到 y=15（顶），高度50px
- 柱高 = (值/100) × 50；柱y = 65 - 柱高
- 第二组用对比色；异常值用 #ef4444
