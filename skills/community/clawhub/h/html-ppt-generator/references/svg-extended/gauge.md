# gauge · 仪表盘/半圆量表

**适用：** 单指标仪表读数、评分、压力/风险等级展示
**尺寸：** 140×80px

---

## 变体 A · 标准半圆仪表（140×80px）

```html
<svg viewBox="0 0 140 80" style="width:140px;height:80px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 轨道渐变：绿→黄→红 -->
    <linearGradient id="gaugeTrack" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#10b981"/>
      <stop offset="50%"  stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#ef4444"/>
    </linearGradient>
    <!-- 裁剪上半圆 -->
    <clipPath id="topHalf">
      <rect x="0" y="0" width="140" height="70"/>
    </clipPath>
  </defs>
  <!-- 灰色背景轨道（半圆） -->
  <circle cx="70" cy="70" r="52" fill="none" stroke="rgba(255,255,255,0.06)"
          stroke-width="12" clip-path="url(#topHalf)"/>
  <!-- 彩色量程轨道 -->
  <circle cx="70" cy="70" r="52" fill="none" stroke="url(#gaugeTrack)"
          stroke-width="12" clip-path="url(#topHalf)"
          stroke-dasharray="163.4 163.4" stroke-dashoffset="0"/>
  <!-- 指针（72%，角度=-90°+(72%×180°)=39.6°） -->
  <line x1="70" y1="70"
        x2="70" y2="23"
        stroke="var(--t)" stroke-width="2" stroke-linecap="round"
        transform="rotate(39.6 70 70)"/>
  <circle cx="70" cy="70" r="4" fill="var(--t)"/>
  <!-- 数值 -->
  <text x="70" y="65" text-anchor="middle" font-size="16" font-weight="800" fill="var(--t)" letter-spacing="-0.5">72</text>
  <text x="70" y="76" text-anchor="middle" font-size="7.5" fill="var(--dt)">综合评分</text>
  <!-- 刻度标注 -->
  <text x="14"  y="73" font-size="7" fill="#10b981" text-anchor="middle">0</text>
  <text x="70"  y="16" font-size="7" fill="#f59e0b" text-anchor="middle">50</text>
  <text x="127" y="73" font-size="7" fill="#ef4444" text-anchor="middle">100</text>
</svg>
```

---

## 变体 B · 分段仪表（5档色阶，140×80px）

```html
<svg viewBox="0 0 140 80" style="width:140px;height:80px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <clipPath id="topHalf2"><rect x="0" y="0" width="140" height="70"/></clipPath>
  </defs>
  <!-- 5段轨道（各36°，总180°，r=52，C=326.7，半C=163.4，每段=32.7px） -->
  <!-- 背景 -->
  <circle cx="70" cy="70" r="52" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="12" clip-path="url(#topHalf2)"/>
  <!-- 段1 危险（深红） -->
  <circle cx="70" cy="70" r="52" fill="none" stroke="#dc2626" stroke-width="12"
          clip-path="url(#topHalf2)"
          stroke-dasharray="32.7 293.9" stroke-dashoffset="0"/>
  <!-- 段2 警告（橙） -->
  <circle cx="70" cy="70" r="52" fill="none" stroke="#f59e0b" stroke-width="12"
          clip-path="url(#topHalf2)"
          stroke-dasharray="32.7 293.9" stroke-dashoffset="-32.7"/>
  <!-- 段3 中性（黄绿） -->
  <circle cx="70" cy="70" r="52" fill="none" stroke="#84cc16" stroke-width="12"
          clip-path="url(#topHalf2)"
          stroke-dasharray="32.7 293.9" stroke-dashoffset="-65.4"/>
  <!-- 段4 良好（绿） -->
  <circle cx="70" cy="70" r="52" fill="none" stroke="#22c55e" stroke-width="12"
          clip-path="url(#topHalf2)"
          stroke-dasharray="32.7 293.9" stroke-dashoffset="-98.1"/>
  <!-- 段5 优秀（深绿） -->
  <circle cx="70" cy="70" r="52" fill="none" stroke="#10b981" stroke-width="12"
          clip-path="url(#topHalf2)"
          stroke-dasharray="32.7 293.9" stroke-dashoffset="-130.8"/>
  <!-- 指针（60分：60%×180=108°，从-90°起=18°） -->
  <line x1="70" y1="70" x2="70" y2="23" stroke="var(--t)" stroke-width="2.5"
        stroke-linecap="round" transform="rotate(18 70 70)"/>
  <circle cx="70" cy="70" r="4.5" fill="var(--t)"/>
  <!-- 文字 -->
  <text x="70" y="64" text-anchor="middle" font-size="15" font-weight="800" fill="var(--t)">60</text>
  <text x="70" y="76" text-anchor="middle" font-size="7" fill="var(--dt)">风险评级</text>
  <text x="14" y="73" font-size="7" fill="#dc2626">高危</text>
  <text x="127" y="73" font-size="7" fill="#10b981" text-anchor="end">优秀</text>
</svg>
```

**指针角度计算：**
```
指针从12点（-90°）开始，顺时针旋转
rotate角度 = -90 + (值/最大值) × 180
示例：72% → rotate = -90 + 72×1.8 = 39.6°
旋转中心 = 圆心 (cx, cy)
```
