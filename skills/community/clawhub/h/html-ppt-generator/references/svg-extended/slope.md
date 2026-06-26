# slope · 斜率对比图（前后变化）

**适用：** 前后对比、改革前/后、处理前/后、时间节点变化量
**高度：** 100px

---

## 变体 A · 双组斜率图（100px）

```html
<svg viewBox="0 0 260 100" style="width:100%;height:100px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 左右两条垂直基准线 -->
  <line x1="60"  y1="10" x2="60"  y2="82" stroke="#1e293b" stroke-width="1.5"/>
  <line x1="200" y1="10" x2="200" y2="82" stroke="#1e293b" stroke-width="1.5"/>
  <!-- 时间标注 -->
  <text x="60"  y="90" text-anchor="middle" font-size="8.5" fill="#64748b">2022</text>
  <text x="200" y="90" text-anchor="middle" font-size="8.5" fill="#64748b">2024</text>

  <!-- 线1：上升（指标A，主色） -->
  <line x1="60" y1="65" x2="200" y2="25" stroke="var(--p)" stroke-width="2" stroke-linecap="round"/>
  <circle cx="60"  cy="65" r="4" fill="var(--p)"/>
  <circle cx="200" cy="25" r="4" fill="var(--p)"/>
  <text x="52"  y="68" text-anchor="end" font-size="8.5" fill="var(--mt)">43%</text>
  <text x="208" y="28" font-size="8.5" fill="var(--mt)" font-weight="700">78%<tspan font-size="7" fill="#10b981"> ↑+35%</tspan></text>

  <!-- 线2：下降（指标B，红色） -->
  <line x1="60" y1="32" x2="200" y2="58" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-dasharray="5,2"/>
  <circle cx="60"  cy="32" r="4" fill="#ef4444"/>
  <circle cx="200" cy="58" r="4" fill="#ef4444"/>
  <text x="52"  y="35" text-anchor="end" font-size="8.5" fill="#fca5a5">68%</text>
  <text x="208" y="61" font-size="8.5" fill="#fca5a5">41%<tspan font-size="7" fill="#ef4444"> ↓-27%</tspan></text>

  <!-- 图例 -->
  <line x1="60" y1="96" x2="80" y2="96" stroke="var(--p)" stroke-width="2"/>
  <text x="84" y="99" font-size="7.5" fill="#64748b">指标A</text>
  <line x1="120" y1="96" x2="140" y2="96" stroke="#ef4444" stroke-width="2" stroke-dasharray="5,2"/>
  <text x="144" y="99" font-size="7.5" fill="#64748b">指标B</text>
</svg>
```

---

## 变体 B · 多组斜率（3组，110px）

```html
<svg viewBox="0 0 280 110" style="width:100%;height:110px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <line x1="70"  y1="8" x2="70"  y2="88" stroke="#1e293b" stroke-width="1.5"/>
  <line x1="210" y1="8" x2="210" y2="88" stroke="#1e293b" stroke-width="1.5"/>
  <text x="70"  y="96" text-anchor="middle" font-size="8" fill="#64748b">改革前</text>
  <text x="210" y="96" text-anchor="middle" font-size="8" fill="#64748b">改革后</text>

  <!-- 组1 上升 -->
  <line x1="70" y1="70" x2="210" y2="30" stroke="var(--p)" stroke-width="2" stroke-linecap="round"/>
  <circle cx="70"  cy="70" r="3.5" fill="var(--p)"/>
  <circle cx="210" cy="30" r="3.5" fill="var(--p)"/>
  <text x="62"  y="73" text-anchor="end" font-size="8" fill="var(--mt)">52%</text>
  <text x="218" y="33" font-size="8" fill="var(--mt)" font-weight="700">85% <tspan fill="#10b981">↑</tspan></text>

  <!-- 组2 轻微上升 -->
  <line x1="70" y1="55" x2="210" y2="45" stroke="#8b5cf6" stroke-width="2" stroke-linecap="round"/>
  <circle cx="70"  cy="55" r="3.5" fill="#8b5cf6"/>
  <circle cx="210" cy="45" r="3.5" fill="#8b5cf6"/>
  <text x="62"  y="58" text-anchor="end" font-size="8" fill="#a78bfa">63%</text>
  <text x="218" y="48" font-size="8" fill="#a78bfa">71% <tspan fill="#10b981">↑</tspan></text>

  <!-- 组3 下降 -->
  <line x1="70" y1="25" x2="210" y2="68" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-dasharray="4,2"/>
  <circle cx="70"  cy="25" r="3.5" fill="#ef4444"/>
  <circle cx="210" cy="68" r="3.5" fill="#ef4444"/>
  <text x="62"  y="28" text-anchor="end" font-size="8" fill="#fca5a5">88%</text>
  <text x="218" y="71" font-size="8" fill="#fca5a5">55% <tspan fill="#ef4444">↓</tspan></text>

  <!-- 图例 -->
  <line x1="70" y1="104" x2="82" y2="104" stroke="var(--p)" stroke-width="2"/>
  <text x="86" y="107" font-size="7.5" fill="#64748b">项目A</text>
  <line x1="120" y1="104" x2="132" y2="104" stroke="#8b5cf6" stroke-width="2"/>
  <text x="136" y="107" font-size="7.5" fill="#64748b">项目B</text>
  <line x1="175" y1="104" x2="187" y2="104" stroke="#ef4444" stroke-width="2" stroke-dasharray="4,2"/>
  <text x="191" y="107" font-size="7.5" fill="#64748b">项目C</text>
</svg>
```

**参数说明：**
- 左轴 x=70（起点），右轴 x=210（终点）
- Y 区间：顶 y=10，底 y=80（高70px）
- Y坐标 = 80 - (值/最大值) × 70
- 上升线用实线，下降线用虚线 stroke-dasharray 区分
- 数值标注：左侧靠右对齐，右侧左对齐
