# lollipop · 棒棒糖图

**适用：** 排名对比（比柱状图更简洁）、稀疏数据点展示、差异量可视化
**高度：** 80px

---

## 变体 A · 横向棒棒糖（80px）

```html
<svg viewBox="0 0 290 80" style="width:100%;height:80px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 基准线（虚） -->
  <line x1="46" y1="4" x2="46" y2="76" stroke="#1e293b" stroke-width="0.8"/>

  <!-- 条目1 -->
  <text x="42" y="16" text-anchor="end" font-size="8.5" fill="#64748b">类别A</text>
  <line x1="46" y1="12" x2="218" y2="12" stroke="#1e293b" stroke-width="1" stroke-dasharray="2,2" opacity="0.3"/>
  <line x1="46" y1="12" x2="218" y2="12" stroke="var(--p)" stroke-width="1.5"/>
  <circle cx="218" cy="12" r="5" fill="var(--p)"/>
  <text x="226" y="15" font-size="8.5" fill="var(--mt)" font-weight="700">89%</text>

  <!-- 条目2 -->
  <text x="42" y="31" text-anchor="end" font-size="8.5" fill="#64748b">类别B</text>
  <line x1="46" y1="27" x2="194" y2="27" stroke="var(--p)" stroke-width="1.5"/>
  <circle cx="194" cy="27" r="5" fill="var(--p)"/>
  <text x="202" y="30" font-size="8.5" fill="var(--mt)" font-weight="700">77%</text>

  <!-- 条目3（最高亮） -->
  <text x="42" y="46" text-anchor="end" font-size="8.5" fill="#64748b">类别C</text>
  <line x1="46" y1="42" x2="242" y2="42" stroke="#ef4444" stroke-width="1.5"/>
  <circle cx="242" cy="42" r="6" fill="#ef4444"/>
  <text x="251" y="45" font-size="8.5" fill="#fca5a5" font-weight="700">97%</text>

  <!-- 条目4 -->
  <text x="42" y="61" text-anchor="end" font-size="8.5" fill="#64748b">类别D</text>
  <line x1="46" y1="57" x2="155" y2="57" stroke="var(--p)" stroke-width="1.5"/>
  <circle cx="155" cy="57" r="5" fill="var(--p)"/>
  <text x="163" y="60" font-size="8.5" fill="var(--mt)" font-weight="700">62%</text>

  <!-- 条目5 -->
  <text x="42" y="76" text-anchor="end" font-size="8.5" fill="#64748b">类别E</text>
  <line x1="46" y1="72" x2="121" y2="72" stroke="#10b981" stroke-width="1.5"/>
  <circle cx="121" cy="72" r="5" fill="#10b981"/>
  <text x="129" y="75" font-size="8.5" fill="#6ee7b7" font-weight="700">48%</text>
</svg>
```

---

## 变体 B · 纵向棒棒糖（80px）

```html
<svg viewBox="0 0 290 80" style="width:100%;height:80px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 基准线 -->
  <line x1="20" y1="60" x2="280" y2="60" stroke="#1e293b" stroke-width="1"/>

  <!-- 柱1 -->
  <line x1="50"  y1="60" x2="50"  y2="18" stroke="var(--p)" stroke-width="1.5"/>
  <circle cx="50"  cy="18" r="5" fill="var(--p)"/>
  <text x="50"  y="13" text-anchor="middle" font-size="8" fill="var(--mt)" font-weight="700">82%</text>
  <text x="50"  y="70" text-anchor="middle" font-size="8" fill="#64748b">A</text>

  <!-- 柱2 -->
  <line x1="100" y1="60" x2="100" y2="28" stroke="var(--p)" stroke-width="1.5"/>
  <circle cx="100" cy="28" r="5" fill="var(--p)"/>
  <text x="100" y="23" text-anchor="middle" font-size="8" fill="var(--mt)" font-weight="700">72%</text>
  <text x="100" y="70" text-anchor="middle" font-size="8" fill="#64748b">B</text>

  <!-- 柱3（最高，强调） -->
  <line x1="150" y1="60" x2="150" y2="10" stroke="#ef4444" stroke-width="1.5"/>
  <circle cx="150" cy="10" r="6" fill="#ef4444"/>
  <text x="150" y="5"  text-anchor="middle" font-size="8" fill="#fca5a5" font-weight="700">97%</text>
  <text x="150" y="70" text-anchor="middle" font-size="8" fill="#64748b">C</text>

  <!-- 柱4 -->
  <line x1="200" y1="60" x2="200" y2="35" stroke="#10b981" stroke-width="1.5"/>
  <circle cx="200" cy="35" r="5" fill="#10b981"/>
  <text x="200" y="30" text-anchor="middle" font-size="8" fill="#6ee7b7" font-weight="700">63%</text>
  <text x="200" y="70" text-anchor="middle" font-size="8" fill="#64748b">D</text>

  <!-- 柱5 -->
  <line x1="250" y1="60" x2="250" y2="42" stroke="var(--p)" stroke-width="1.5"/>
  <circle cx="250" cy="42" r="5" fill="var(--p)"/>
  <text x="250" y="37" text-anchor="middle" font-size="8" fill="var(--mt)" font-weight="700">54%</text>
  <text x="250" y="70" text-anchor="middle" font-size="8" fill="#64748b">E</text>
</svg>
```

**参数说明：**
- 横向：线长 = (值/最大值) × 244，从 x=46 起；圆点 r=5（强调点 r=6）
- 纵向：线从 y=60 向上，圆点 cy = 60 - (值/最大值) × 50
- 最值/异常用 #ef4444，最优用 #10b981，普通用 var(--p)
