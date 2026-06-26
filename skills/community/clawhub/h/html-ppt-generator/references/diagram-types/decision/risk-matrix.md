# risk-matrix · 风险矩阵

**适用：** 风险评估、安全威胁优先级、项目风险登记册
**高度：** 240px（5×5 网格）

**结构公式：** 5×5 热力格，颜色规则：likelihood × impact → 绿/黄/橙/红，风险点用圆圈标注。

```html
<svg viewBox="0 0 320 240" style="width:100%;height:240px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 5×5 热力格（颜色：绿=低风险，黄=中，橙=高，红=极高） -->
  <!-- 行1（impact=5，最高） -->
  <rect x="40" y="10"  width="52" height="40" rx="1" fill="rgba(245,158,11,0.5)"/> <text x="66"  y="34" text-anchor="middle" font-size="8" fill="#fff">5</text>
  <rect x="94" y="10"  width="52" height="40" rx="1" fill="rgba(239,68,68,0.5)"/>  <text x="120" y="34" text-anchor="middle" font-size="8" fill="#fff">10</text>
  <rect x="148" y="10" width="52" height="40" rx="1" fill="rgba(239,68,68,0.7)"/>  <text x="174" y="34" text-anchor="middle" font-size="8" fill="#fff">15</text>
  <rect x="202" y="10" width="52" height="40" rx="1" fill="rgba(239,68,68,0.85)"/> <text x="228" y="34" text-anchor="middle" font-size="8" fill="#fff">20</text>
  <rect x="256" y="10" width="52" height="40" rx="1" fill="rgba(239,68,68,1.0)"/>  <text x="282" y="34" text-anchor="middle" font-size="8" fill="#fff">25</text>
  <!-- 行2（impact=4） -->
  <rect x="40"  y="52" width="52" height="40" rx="1" fill="rgba(16,185,129,0.4)"/> <text x="66"  y="76" text-anchor="middle" font-size="8" fill="#fff">4</text>
  <rect x="94"  y="52" width="52" height="40" rx="1" fill="rgba(245,158,11,0.5)"/> <text x="120" y="76" text-anchor="middle" font-size="8" fill="#fff">8</text>
  <rect x="148" y="52" width="52" height="40" rx="1" fill="rgba(245,158,11,0.7)"/> <text x="174" y="76" text-anchor="middle" font-size="8" fill="#fff">12</text>
  <rect x="202" y="52" width="52" height="40" rx="1" fill="rgba(239,68,68,0.6)"/>  <text x="228" y="76" text-anchor="middle" font-size="8" fill="#fff">16</text>
  <rect x="256" y="52" width="52" height="40" rx="1" fill="rgba(239,68,68,0.8)"/>  <text x="282" y="76" text-anchor="middle" font-size="8" fill="#fff">20</text>
  <!-- 行3（impact=3） -->
  <rect x="40"  y="94" width="52" height="40" rx="1" fill="rgba(16,185,129,0.3)"/> <text x="66"  y="118" text-anchor="middle" font-size="8" fill="#fff">3</text>
  <rect x="94"  y="94" width="52" height="40" rx="1" fill="rgba(16,185,129,0.5)"/> <text x="120" y="118" text-anchor="middle" font-size="8" fill="#fff">6</text>
  <rect x="148" y="94" width="52" height="40" rx="1" fill="rgba(245,158,11,0.5)"/> <text x="174" y="118" text-anchor="middle" font-size="8" fill="#fff">9</text>
  <rect x="202" y="94" width="52" height="40" rx="1" fill="rgba(245,158,11,0.7)"/> <text x="228" y="118" text-anchor="middle" font-size="8" fill="#fff">12</text>
  <rect x="256" y="94" width="52" height="40" rx="1" fill="rgba(239,68,68,0.5)"/>  <text x="282" y="118" text-anchor="middle" font-size="8" fill="#fff">15</text>
  <!-- 行4（impact=2） -->
  <rect x="40"  y="136" width="52" height="40" rx="1" fill="rgba(16,185,129,0.25)"/><text x="66"  y="160" text-anchor="middle" font-size="8" fill="#fff">2</text>
  <rect x="94"  y="136" width="52" height="40" rx="1" fill="rgba(16,185,129,0.4)"/> <text x="120" y="160" text-anchor="middle" font-size="8" fill="#fff">4</text>
  <rect x="148" y="136" width="52" height="40" rx="1" fill="rgba(16,185,129,0.6)"/> <text x="174" y="160" text-anchor="middle" font-size="8" fill="#fff">6</text>
  <rect x="202" y="136" width="52" height="40" rx="1" fill="rgba(245,158,11,0.4)"/> <text x="228" y="160" text-anchor="middle" font-size="8" fill="#fff">8</text>
  <rect x="256" y="136" width="52" height="40" rx="1" fill="rgba(245,158,11,0.6)"/> <text x="282" y="160" text-anchor="middle" font-size="8" fill="#fff">10</text>
  <!-- 行5（impact=1） -->
  <rect x="40"  y="178" width="52" height="40" rx="1" fill="rgba(16,185,129,0.15)"/><text x="66"  y="202" text-anchor="middle" font-size="8" fill="var(--mt)">1</text>
  <rect x="94"  y="178" width="52" height="40" rx="1" fill="rgba(16,185,129,0.25)"/><text x="120" y="202" text-anchor="middle" font-size="8" fill="var(--mt)">2</text>
  <rect x="148" y="178" width="52" height="40" rx="1" fill="rgba(16,185,129,0.35)"/><text x="174" y="202" text-anchor="middle" font-size="8" fill="#fff">3</text>
  <rect x="202" y="178" width="52" height="40" rx="1" fill="rgba(16,185,129,0.5)"/> <text x="228" y="202" text-anchor="middle" font-size="8" fill="#fff">4</text>
  <rect x="256" y="178" width="52" height="40" rx="1" fill="rgba(245,158,11,0.35)"/><text x="282" y="202" text-anchor="middle" font-size="8" fill="var(--mt)">5</text>
  <!-- 轴标签 -->
  <text x="180" y="232" text-anchor="middle" font-size="8.5" fill="#64748b">← 可能性 (Likelihood) →</text>
  <text x="66"  y="232" text-anchor="middle" font-size="8" fill="#64748b">低(1)</text>
  <text x="282" y="232" text-anchor="middle" font-size="8" fill="#64748b">高(5)</text>
  <text x="14"  y="100" text-anchor="middle" font-size="8.5" fill="#64748b" transform="rotate(-90,14,100)">影响度 (Impact)</text>
  <!-- 风险点标注 -->
  <circle cx="174" cy="30" r="8" fill="none" stroke="#fff" stroke-width="2"/>
  <text x="174" y="33" text-anchor="middle" font-size="7.5" fill="#fff" font-weight="700">R1</text>
  <circle cx="228" cy="76" r="8" fill="none" stroke="#fff" stroke-width="2"/>
  <text x="228" y="79" text-anchor="middle" font-size="7.5" fill="#fff" font-weight="700">R2</text>
</svg>
```

**参数说明：**
- 每格 52×40px；行序从上（impact=5）到下（impact=1）
- 颜色编码：1–4=绿(#10b981)，5–9=黄(#f59e0b)，10–16=橙→红(#ef4444)，≥20=深红
- 风险点：空心白圈 r=8，文字 R1/R2 等，叠加在对应格子上
- Y轴标签用 transform="rotate(-90,x,y)" 竖排显示
