# waterfall · 瀑布图

**适用：** 累计变化分解、利润构成、预算增减
**高度：** 80px

```html
<svg viewBox="0 0 400 80" style="width:100%;height:80px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 基准线 -->
  <line x1="20" y1="60" x2="380" y2="60" stroke="#1e293b" stroke-width="1"/>
  <!-- 起始柱（基准） -->
  <rect x="30" y="20" width="40" height="40" rx="2" fill="var(--p)"/>
  <text x="50" y="16" text-anchor="middle" font-size="8" fill="var(--mt)">基准</text>
  <text x="50" y="71" text-anchor="middle" font-size="7.5" fill="#64748b">100</text>
  <line x1="70" y1="20" x2="90" y2="20" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,2"/>
  <!-- 增加柱（绿，浮动） -->
  <rect x="90" y="10" width="40" height="10" rx="2" fill="#10b981"/>
  <text x="110" y="7"  text-anchor="middle" font-size="8" fill="#10b981">+10</text>
  <text x="110" y="71" text-anchor="middle" font-size="7.5" fill="#64748b">+营收</text>
  <line x1="130" y1="10" x2="150" y2="10" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,2"/>
  <!-- 减少柱（红，浮动） -->
  <rect x="150" y="10" width="40" height="18" rx="2" fill="#ef4444"/>
  <text x="170" y="7"  text-anchor="middle" font-size="8" fill="#ef4444">-18</text>
  <text x="170" y="71" text-anchor="middle" font-size="7.5" fill="#64748b">-成本</text>
  <line x1="190" y1="28" x2="210" y2="28" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,2"/>
  <!-- 增加柱 -->
  <rect x="210" y="18" width="40" height="10" rx="2" fill="#10b981"/>
  <text x="230" y="15" text-anchor="middle" font-size="8" fill="#10b981">+10</text>
  <text x="230" y="71" text-anchor="middle" font-size="7.5" fill="#64748b">+其他</text>
  <line x1="250" y1="18" x2="270" y2="18" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,2"/>
  <!-- 减少柱 -->
  <rect x="270" y="18" width="40" height="8" rx="2" fill="#ef4444"/>
  <text x="290" y="15" text-anchor="middle" font-size="8" fill="#ef4444">-8</text>
  <text x="290" y="71" text-anchor="middle" font-size="7.5" fill="#64748b">-税费</text>
  <line x1="310" y1="26" x2="330" y2="26" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="2,2"/>
  <!-- 结果柱 -->
  <rect x="330" y="26" width="40" height="34" rx="2" fill="var(--p)" opacity="0.7"/>
  <text x="350" y="22" text-anchor="middle" font-size="8" fill="var(--mt)">结果</text>
  <text x="350" y="71" text-anchor="middle" font-size="7.5" fill="#64748b">94</text>
  <!-- Y轴 -->
  <text x="18" y="62" font-size="7.5" fill="#64748b" text-anchor="end">0</text>
  <text x="18" y="22" font-size="7.5" fill="#64748b" text-anchor="end">100</text>
</svg>
```

**参数说明：**
- 基准柱从 y=基准线位置向上绘制
- 增加柱（#10b981）：上浮，y = 前一段结束 y - 增量高度
- 减少柱（#ef4444）：下沉，y = 前一段结束 y，高度 = 减量
- 每段间连接虚线：从当前段顶部画到下一柱起点
- 每柱宽40px，间距10px
