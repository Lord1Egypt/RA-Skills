# scatter · 散点图

**适用：** 相关性分析、风险矩阵、二维分布
**高度：** 110px

```html
<svg viewBox="0 0 260 110" style="width:100%;height:110px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 坐标轴 -->
  <line x1="30" y1="8" x2="30" y2="85" stroke="#1e293b" stroke-width="1"/>
  <line x1="30" y1="85" x2="250" y2="85" stroke="#1e293b" stroke-width="1"/>
  <!-- 参考线（四象限分割） -->
  <line x1="30" y1="46" x2="250" y2="46" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="3,3"/>
  <line x1="140" y1="8" x2="140" y2="85" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="3,3"/>
  <!-- 数据点 -->
  <circle cx="55"  cy="70" r="5" fill="var(--p)" opacity="0.8"/>
  <circle cx="80"  cy="58" r="7" fill="var(--p)" opacity="0.8"/>
  <circle cx="105" cy="48" r="5" fill="var(--p)" opacity="0.8"/>
  <circle cx="130" cy="35" r="9" fill="#ef4444" opacity="0.8"/>
  <circle cx="160" cy="30" r="5" fill="var(--p)" opacity="0.8"/>
  <circle cx="185" cy="22" r="6" fill="var(--p)" opacity="0.8"/>
  <circle cx="210" cy="18" r="5" fill="#10b981" opacity="0.8"/>
  <circle cx="235" cy="15" r="7" fill="#10b981" opacity="0.8"/>
  <!-- 趋势线 -->
  <line x1="42" y1="75" x2="245" y2="10" stroke="var(--p)" stroke-width="1" stroke-dasharray="4,2" opacity="0.4"/>
  <!-- 轴标签 -->
  <text x="140" y="99" text-anchor="middle" font-size="8.5" fill="#64748b">X轴：指标A</text>
  <text x="10" y="46" text-anchor="middle" font-size="8.5" fill="#64748b" transform="rotate(-90,10,46)">Y轴：指标B</text>
  <!-- 象限标注 -->
  <text x="85"  y="20" font-size="7.5" fill="#475569">低A·高B</text>
  <text x="170" y="20" font-size="7.5" fill="#475569">高A·高B</text>
  <text x="170" y="80" font-size="7.5" fill="#475569">高A·低B</text>
</svg>
```

**参数说明：**
- 绘图区：x 30–250，y 8–85
- 圆点大小（r）可表示第三维度（如市场规模）
- 异常点/重点用 #ef4444，正向点用 #10b981
- 四象限分割线：水平 y=46（中值），垂直 x=140（中值）
