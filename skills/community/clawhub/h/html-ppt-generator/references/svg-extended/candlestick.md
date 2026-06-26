# candlestick · K 线图/蜡烛图

**适用：** 金融价格走势、股票/加密货币、涨跌分析、交易数据
**尺寸：** 180×120px

```html
<svg viewBox="0 0 180 120" style="width:180px;height:120px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 涨（红色） -->
    <linearGradient id="cg1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="100%" stop-color="#dc2626"/>
    </linearGradient>
    <!-- 跌（绿色） -->
    <linearGradient id="cg2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
  </defs>

  <!-- 背景网格线 -->
  <line x1="20" y1="10" x2="20" y2="100" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="50" y1="10" x2="50" y2="100" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="80" y1="10" x2="80" y2="100" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="110" y1="10" x2="110" y2="100" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="140" y1="10" x2="140" y2="100" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="170" y1="10" x2="170" y2="100" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>

  <!-- 价格水平参考线 -->
  <line x1="10" y1="20" x2="180" y2="20" stroke="rgba(255,255,255,0.04)" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="10" y1="55" x2="180" y2="55" stroke="rgba(255,255,255,0.04)" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="10" y1="90" x2="180" y2="90" stroke="rgba(255,255,255,0.04)" stroke-width="1" stroke-dasharray="2,2"/>

  <!-- Y 轴价格标签 -->
  <text x="5" y="15" font-size="8" fill="var(--dt)">100</text>
  <text x="5" y="58" font-size="8" fill="var(--dt)">80</text>
  <text x="5" y="93" font-size="8" fill="var(--dt)">60</text>

  <!-- K 线 1: 阳线（涨）开 70 收 85 高 90 低 68 -->
  <!-- 实体：开=85px, 收=70px（注意 SVG Y 坐标向下增大） -->
  <line x1="35" y1="32" x2="35" y2="23" stroke="url(#cg1)" stroke-width="1.5"/> <!-- 上影线 -->
  <rect x="30" y="32" width="10" height="15" fill="url(#cg1)"/> <!-- 实体 -->
  <line x1="35" y1="47" x2="35" y2="52" stroke="url(#cg1)" stroke-width="1.5"/> <!-- 下影线 -->

  <!-- K 线 2: 阴线（跌）开 85 收 75 高 88 低 72 -->
  <line x1="65" y1="26" x2="65" y2="32" stroke="url(#cg2)" stroke-width="1.5"/> <!-- 上影线 -->
  <rect x="60" y="32" width="10" height="10" fill="url(#cg2)"/> <!-- 实体 -->
  <line x1="65" y1="42" x2="65" y2="48" stroke="url(#cg2)" stroke-width="1.5"/> <!-- 下影线 -->

  <!-- K 线 3: 阳线（涨）开 75 收 92 高 95 低 73 -->
  <line x1="95" y1="18" x2="95" y2="25" stroke="url(#cg1)" stroke-width="1.5"/>
  <rect x="90" y="25" width="10" height="17" fill="url(#cg1)"/>
  <line x1="95" y1="42" x2="95" y2="47" stroke="url(#cg1)" stroke-width="1.5"/>

  <!-- K 线 4: 阴线（跌）开 92 收 80 高 94 低 78 -->
  <line x1="125" y1="16" x2="125" y2="25" stroke="url(#cg2)" stroke-width="1.5"/>
  <rect x="120" y="25" width="10" height="12" fill="url(#cg2)"/>
  <line x1="125" y1="37" x2="125" y2="42" stroke="url(#cg2)" stroke-width="1.5"/>

  <!-- K 线 5: 阳线（涨）开 80 收 88 高 92 低 78 -->
  <line x1="155" y1="18" x2="155" y2="29" stroke="url(#cg1)" stroke-width="1.5"/>
  <rect x="150" y="29" width="10" height="8" fill="url(#cg1)"/>
  <line x1="155" y1="37" x2="155" y2="42" stroke="url(#cg1)" stroke-width="1.5"/>

  <!-- K 线 6: 大阳线（暴涨）开 88 收 98 高 99 低 86 -->
  <line x1="185" y1="11" x2="185" y2="19" stroke="url(#cg1)" stroke-width="1.5"/>
  <rect x="180" y="19" width="10" height="10" fill="url(#cg1)"/>
  <line x1="185" y1="29" x2="185" y2="34" stroke="url(#cg1)" stroke-width="1.5"/>

  <!-- X 轴日期标签 -->
  <text x="35" y="112" text-anchor="middle" font-size="8" fill="var(--dt)">01/15</text>
  <text x="65" y="112" text-anchor="middle" font-size="8" fill="var(--dt)">01/16</text>
  <text x="95" y="112" text-anchor="middle" font-size="8" fill="var(--dt)">01/17</text>
  <text x="125" y="112" text-anchor="middle" font-size="8" fill="var(--dt)">01/18</text>
  <text x="155" y="112" text-anchor="middle" font-size="8" fill="var(--dt)">01/19</text>
  <text x="185" y="112" text-anchor="middle" font-size="8" fill="var(--dt)">01/20</text>

  <!-- 右上角统计 -->
  <text x="120" y="8" font-size="8" fill="var(--dt)">最高：</text>
  <text x="148" y="8" font-size="9" font-weight="700" fill="var(--gold)">99.2</text>
  <text x="120" y="18" font-size="8" fill="var(--dt)">最低：</text>
  <text x="148" y="18" font-size="9" font-weight="700" fill="var(--dt)">68.5</text>
  <text x="120" y="28" font-size="8" fill="var(--dt)">涨跌：</text>
  <text x="148" y="28" font-size="9" font-weight="700" fill="url(#cg1)">+40.6%</text>
</svg>
```

**坐标计算：**
```
绘图区：X[10-180]，Y[10-100]
价格范围：60-100（根据数据动态调整）

价格 → SVG Y 坐标：
svgY = 100 - (价格 - 最低价) / (最高价 - 最低价) × 90

K 线结构：
- 实体高度 = |开盘 - 收盘| 按比例
- 上影线 = 最高价 - max(开盘，收盘)
- 下影线 = min(开盘，收盘) - 最低价
- 实体宽度 = 8-10px

阳线（涨）：收盘 > 开盘，红色填充
阴线（跌）：收盘 < 开盘，绿色填充（或空心）
```

**变体用法：**
```
- 美式 K 线：涨红跌绿（如上）
- 亚式 K 线：涨绿跌红（交换颜色）
- 空心 K 线：阴线用空心矩形，阳线实心
- 美国线（Bar Chart）：竖线 + 左右横线表示开收
```
