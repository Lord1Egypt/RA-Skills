# bump · 排名变化图（颠簸图）

**适用：** 排名随时间变化、名次升降、竞争格局演变
**高度：** 120px

---

## 变体 A · 3时间点排名变化（120px，5条线）

```html
<svg viewBox="0 0 280 120" style="width:100%;height:120px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 列标题 -->
  <text x="50"  y="8" text-anchor="middle" font-size="8" fill="#64748b">2022</text>
  <text x="140" y="8" text-anchor="middle" font-size="8" fill="#64748b">2023</text>
  <text x="230" y="8" text-anchor="middle" font-size="8" fill="#64748b">2024</text>

  <!-- 排名网格线（y间距20px，5个排名位） -->
  <text x="34" y="26" text-anchor="end" font-size="7.5" fill="#475569">#1</text>
  <text x="34" y="46" text-anchor="end" font-size="7.5" fill="#475569">#2</text>
  <text x="34" y="66" text-anchor="end" font-size="7.5" fill="#475569">#3</text>
  <text x="34" y="86" text-anchor="end" font-size="7.5" fill="#475569">#4</text>
  <text x="34" y="106" text-anchor="end" font-size="7.5" fill="#475569">#5</text>

  <!-- 参考点（各列×各排名位的交叉点） -->
  <!-- 列x：50, 140, 230；排名y：22, 42, 62, 82, 102 -->

  <!-- 线A（主色，1→3→1，上升-下降-回升） -->
  <path d="M50,22 C95,22 95,62 140,62 C185,62 185,22 230,22"
        fill="none" stroke="var(--p)" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="50"  cy="22" r="4" fill="var(--p)"/>
  <circle cx="140" cy="62" r="4" fill="var(--p)"/>
  <circle cx="230" cy="22" r="4" fill="var(--p)"/>
  <text x="238" y="25" font-size="8.5" fill="var(--p)" font-weight="700">品牌A</text>

  <!-- 线B（紫，3→1→2） -->
  <path d="M50,62 C95,62 95,22 140,22 C185,22 185,42 230,42"
        fill="none" stroke="#8b5cf6" stroke-width="2"/>
  <circle cx="50"  cy="62" r="3.5" fill="#8b5cf6"/>
  <circle cx="140" cy="22" r="3.5" fill="#8b5cf6"/>
  <circle cx="230" cy="42" r="3.5" fill="#8b5cf6"/>
  <text x="238" y="45" font-size="8.5" fill="#8b5cf6">品牌B</text>

  <!-- 线C（绿，5→4→3，持续上升） -->
  <path d="M50,102 C95,102 95,82 140,82 C185,82 185,62 230,62"
        fill="none" stroke="#10b981" stroke-width="2"/>
  <circle cx="50"  cy="102" r="3.5" fill="#10b981"/>
  <circle cx="140" cy="82"  r="3.5" fill="#10b981"/>
  <circle cx="230" cy="62"  r="3.5" fill="#10b981"/>
  <text x="238" y="65" font-size="8.5" fill="#10b981">品牌C</text>

  <!-- 线D（橙，2→5→4，持续下降） -->
  <path d="M50,42 C95,42 95,102 140,102 C185,102 185,82 230,82"
        fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,2"/>
  <circle cx="50"  cy="42"  r="3.5" fill="#f59e0b"/>
  <circle cx="140" cy="102" r="3.5" fill="#f59e0b"/>
  <circle cx="230" cy="82"  r="3.5" fill="#f59e0b"/>
  <text x="238" y="85" font-size="8.5" fill="#f59e0b">品牌D</text>

  <!-- 线E（红，4→2→5，剧烈波动） -->
  <path d="M50,82 C95,82 95,42 140,42 C185,42 185,102 230,102"
        fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="4,2"/>
  <circle cx="50"  cy="82"  r="3.5" fill="#ef4444"/>
  <circle cx="140" cy="42"  r="3.5" fill="#ef4444"/>
  <circle cx="230" cy="102" r="3.5" fill="#ef4444"/>
  <text x="238" y="105" font-size="8.5" fill="#ef4444">品牌E</text>

  <!-- 左侧起始排名 -->
  <text x="44" y="25"  text-anchor="end" font-size="8" fill="var(--p)"  font-weight="700">1</text>
  <text x="44" y="45"  text-anchor="end" font-size="8" fill="#f59e0b"   font-weight="700">2</text>
  <text x="44" y="65"  text-anchor="end" font-size="8" fill="#8b5cf6"   font-weight="700">3</text>
  <text x="44" y="85"  text-anchor="end" font-size="8" fill="#ef4444"   font-weight="700">4</text>
  <text x="44" y="105" text-anchor="end" font-size="8" fill="#10b981"   font-weight="700">5</text>
</svg>
```

**参数说明：**
- 列x坐标：时间节点等间距分布（3列：50/140/230）
- 排名y坐标：#1→y=22，#2→y=42，...，每级间距20px
- 曲线用 cubic bezier（C命令）使转折平滑
- 控制点x = (起点x + 终点x) / 2；控制点y = 各自端点y
- 上升趋势用实线，下降/波动用虚线 stroke-dasharray
- 主关注线用较粗 stroke-width=2.5，其余2.0
