# cycle · 循环图/飞轮模型

**适用：** 正向循环、增长飞轮、业务闭环、价值循环、PDCA 循环
**高度：** 240px

**结构公式：** N 个弧形色块环绕圆心排列，弧间用弯曲箭头连接，圆心放核心概念。

---

## 变体 A · 4步循环（飞轮，240px）

```html
<svg viewBox="0 0 400 240" style="width:100%;height:240px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="cy-arr" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L7,3.5 z" fill="var(--p)"/>
    </marker>
  </defs>

  <!-- 圆心核心概念 -->
  <circle cx="200" cy="120" r="42" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>
  <text x="200" y="116" text-anchor="middle" font-size="11" font-weight="800" fill="var(--t)">增长</text>
  <text x="200" y="130" text-anchor="middle" font-size="11" font-weight="800" fill="var(--t)">飞轮</text>

  <!-- 4个弧形扇区（各约80°，间隔10°） -->
  <!-- 上：用户增长（顶部）-->
  <path d="M200,120 L200,25 A95,95 0 0,1 285,72 Z"
        fill="rgba(59,130,246,0.18)" stroke="rgba(59,130,246,0.5)" stroke-width="1.5"/>
  <text x="224" y="60" text-anchor="middle" font-size="9.5" font-weight="700" fill="#93c5fd">用户增长</text>
  <text x="224" y="73" text-anchor="middle" font-size="8" fill="#60a5fa">+35% YoY</text>

  <!-- 右：口碑传播 -->
  <path d="M200,120 L295,72 A95,95 0 0,1 295,168 Z"
        fill="rgba(16,185,129,0.15)" stroke="rgba(16,185,129,0.5)" stroke-width="1.5"/>
  <text x="276" y="116" text-anchor="middle" font-size="9.5" font-weight="700" fill="#6ee7b7">口碑传播</text>
  <text x="276" y="129" text-anchor="middle" font-size="8" fill="#34d399">NPS 72</text>

  <!-- 下：产品优化 -->
  <path d="M200,120 L295,168 A95,95 0 0,1 115,168 Z"
        fill="rgba(245,158,11,0.15)" stroke="rgba(245,158,11,0.5)" stroke-width="1.5"/>
  <text x="200" y="196" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fcd34d">产品优化</text>
  <text x="200" y="209" text-anchor="middle" font-size="8" fill="#fbbf24">迭代×24/年</text>

  <!-- 左：数据积累 -->
  <path d="M200,120 L115,168 A95,95 0 0,1 115,72 Z"
        fill="rgba(139,92,246,0.15)" stroke="rgba(139,92,246,0.5)" stroke-width="1.5"/>
  <text x="124" y="116" text-anchor="middle" font-size="9.5" font-weight="700" fill="#c4b5fd">数据积累</text>
  <text x="124" y="129" text-anchor="middle" font-size="8" fill="#a78bfa">10亿条/天</text>

  <!-- 上→右循环箭头 -->
  <path d="M270,62 A95,95 0 0,1 300,120" fill="none" stroke="var(--p)" stroke-width="2.5"
        marker-end="url(#cy-arr)"/>
  <!-- 右→下循环箭头 -->
  <path d="M300,180 A95,95 0 0,1 248,210" fill="none" stroke="var(--p)" stroke-width="2.5"
        marker-end="url(#cy-arr)"/>
  <!-- 下→左循环箭头 -->
  <path d="M152,210 A95,95 0 0,1 105,180" fill="none" stroke="var(--p)" stroke-width="2.5"
        marker-end="url(#cy-arr)"/>
  <!-- 左→上循环箭头 -->
  <path d="M105,62 A95,95 0 0,1 155,30" fill="none" stroke="var(--p)" stroke-width="2.5"
        marker-end="url(#cy-arr)"/>
</svg>
```

---

## 变体 B · PDCA 循环（4步，210px）

```html
<svg viewBox="0 0 380 210" style="width:100%;height:210px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="pdca-arr" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L7,3.5 z" fill="#475569"/>
    </marker>
  </defs>
  <!-- 4个圆角方块，环形排列 -->
  <!-- P（左上） -->
  <rect x="40"  y="20"  width="120" height="70" rx="8" fill="rgba(59,130,246,0.12)" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="100" y="50" text-anchor="middle" font-size="18" font-weight="900" fill="#3b82f6">P</text>
  <text x="100" y="66" text-anchor="middle" font-size="9.5" fill="#93c5fd" font-weight="700">Plan · 计划</text>
  <text x="100" y="80" text-anchor="middle" font-size="8" fill="var(--dt)">制定目标与方案</text>

  <!-- D（右上） -->
  <rect x="220" y="20"  width="120" height="70" rx="8" fill="rgba(16,185,129,0.12)" stroke="#10b981" stroke-width="1.5"/>
  <text x="280" y="50" text-anchor="middle" font-size="18" font-weight="900" fill="#10b981">D</text>
  <text x="280" y="66" text-anchor="middle" font-size="9.5" fill="#6ee7b7" font-weight="700">Do · 执行</text>
  <text x="280" y="80" text-anchor="middle" font-size="8" fill="var(--dt)">按计划实施行动</text>

  <!-- C（右下） -->
  <rect x="220" y="120" width="120" height="70" rx="8" fill="rgba(245,158,11,0.12)" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="280" y="150" text-anchor="middle" font-size="18" font-weight="900" fill="#f59e0b">C</text>
  <text x="280" y="166" text-anchor="middle" font-size="9.5" fill="#fcd34d" font-weight="700">Check · 检查</text>
  <text x="280" y="180" text-anchor="middle" font-size="8" fill="var(--dt)">对比目标核查</text>

  <!-- A（左下） -->
  <rect x="40"  y="120" width="120" height="70" rx="8" fill="rgba(239,68,68,0.12)" stroke="#ef4444" stroke-width="1.5"/>
  <text x="100" y="150" text-anchor="middle" font-size="18" font-weight="900" fill="#ef4444">A</text>
  <text x="100" y="166" text-anchor="middle" font-size="9.5" fill="#fca5a5" font-weight="700">Act · 改进</text>
  <text x="100" y="180" text-anchor="middle" font-size="8" fill="var(--dt)">总结经验标准化</text>

  <!-- 顺时针箭头 -->
  <path d="M160,55 Q190,55 220,55" fill="none" stroke="#475569" stroke-width="1.8" marker-end="url(#pdca-arr)"/>
  <path d="M280,90 Q280,105 280,120" fill="none" stroke="#475569" stroke-width="1.8" marker-end="url(#pdca-arr)"/>
  <path d="M220,155 Q190,155 160,155" fill="none" stroke="#475569" stroke-width="1.8" marker-end="url(#pdca-arr)"/>
  <path d="M100,120 Q100,105 100,90" fill="none" stroke="#475569" stroke-width="1.8" marker-end="url(#pdca-arr)"/>
</svg>
```

**参数说明：**
- 变体A：扇区路径用 SVG arc（`A rx,ry 0 large-arc-flag,sweep x,y`）
- 每扇区约 80°，间隔 10°；圆心 r=42，外圆 r=95
- 变体B：方块间用简单直线箭头（更清晰，适合 PDCA/OODA 等4步框架）
- 循环感：箭头颜色用主色，加粗 stroke-width=2.5
