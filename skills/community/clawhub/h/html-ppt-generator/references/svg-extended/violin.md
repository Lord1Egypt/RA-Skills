# violin · 小提琴图

**适用：** 概率密度分布、多组数据形状对比、平滑分布可视化
**尺寸：** 140×110px

```html
<svg viewBox="0 0 140 110" style="width:140px;height:110px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="vg1" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.1"/>
      <stop offset="50%" stop-color="#3b82f6" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.1"/>
    </linearGradient>
    <linearGradient id="vg2" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.1"/>
      <stop offset="50%" stop-color="#10b981" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0.1"/>
    </linearGradient>
    <linearGradient id="vg3" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.1"/>
      <stop offset="50%" stop-color="#f59e0b" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.1"/>
    </linearGradient>
  </defs>

  <!-- 背景网格 -->
  <line x1="20" y1="15" x2="20" y2="95" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="50" y1="15" x2="50" y2="95" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="80" y1="15" x2="80" y2="95" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="110" y1="15" x2="110" y2="95" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>

  <!-- 水平参考线 -->
  <line x1="10" y1="25" x2="130" y2="25" stroke="rgba(255,255,255,0.04)" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="10" y1="45" x2="130" y2="45" stroke="rgba(255,255,255,0.04)" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="10" y1="65" x2="130" y2="65" stroke="rgba(255,255,255,0.04)" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="10" y1="85" x2="130" y2="85" stroke="rgba(255,255,255,0.04)" stroke-width="1" stroke-dasharray="2,2"/>

  <!-- Y 轴标签 -->
  <text x="5" y="28" font-size="8" fill="var(--dt)">高</text>
  <text x="5" y="68" font-size="8" fill="var(--dt)">中</text>
  <text x="5" y="88" font-size="8" fill="var(--dt)">低</text>

  <!-- 小提琴 1：单峰分布（偏上） -->
  <!-- 左半边路径 -->
  <path d="M 35 20
           C 25 25, 20 35, 22 45
           C 24 55, 28 60, 35 65
           L 35 20 Z"
        fill="url(#vg1)" stroke="#3b82f6" stroke-width="1.5"/>
  <!-- 右半边路径 -->
  <path d="M 35 20
           C 45 25, 50 35, 48 45
           C 46 55, 42 60, 35 65
           L 35 20 Z"
        fill="url(#vg1)" stroke="#3b82f6" stroke-width="1.5"/>
  <!-- 中位线 -->
  <line x1="30" y1="42" x2="40" y2="42" stroke="#1e3a5f" stroke-width="2"/>
  <!-- 均值点 -->
  <circle cx="35" cy="40" r="2.5" fill="#fff" stroke="#3b82f6" stroke-width="1"/>

  <!-- 小提琴 2：双峰分布 -->
  <path d="M 65 25
           C 52 30, 48 45, 52 55
           C 56 65, 52 75, 65 80
           L 65 25 Z"
        fill="url(#vg2)" stroke="#10b981" stroke-width="1.5"/>
  <path d="M 65 25
           C 78 30, 82 45, 78 55
           C 74 65, 78 75, 65 80
           L 65 25 Z"
        fill="url(#vg2)" stroke="#10b981" stroke-width="1.5"/>
  <!-- 中位线 -->
  <line x1="60" y1="52" x2="70" y2="52" stroke="#064e3b" stroke-width="2"/>
  <circle cx="65" cy="50" r="2.5" fill="#fff" stroke="#10b981" stroke-width="1"/>

  <!-- 小提琴 3：均匀分布（宽） -->
  <path d="M 95 30
           C 75 35, 70 50, 72 60
           C 74 70, 80 78, 95 82
           L 95 30 Z"
        fill="url(#vg3)" stroke="#f59e0b" stroke-width="1.5"/>
  <path d="M 95 30
           C 115 35, 120 50, 118 60
           C 116 70, 110 78, 95 82
           L 95 30 Z"
        fill="url(#vg3)" stroke="#f59e0b" stroke-width="1.5"/>
  <!-- 中位线 -->
  <line x1="90" y1="56" x2="100" y2="56" stroke="#78350f" stroke-width="2"/>
  <circle cx="95" cy="54" r="2.5" fill="#fff" stroke="#f59e0b" stroke-width="1"/>

  <!-- X 轴标签 -->
  <text x="35" y="105" text-anchor="middle" font-size="9" font-weight="600" fill="var(--t)">A 组</text>
  <text x="65" y="105" text-anchor="middle" font-size="9" font-weight="600" fill="var(--t)">B 组</text>
  <text x="95" y="105" text-anchor="middle" font-size="9" font-weight="600" fill="var(--t)">C 组</text>

  <!-- 图例 -->
  <rect x="115" y="20" width="12" height="8" fill="url(#vg1)" stroke="#3b82f6" stroke-width="1"/>
  <text x="130" y="27" font-size="7" fill="var(--dt)">单峰</text>
  <rect x="115" y="32" width="12" height="8" fill="url(#vg2)" stroke="#10b981" stroke-width="1"/>
  <text x="130" y="39" font-size="7" fill="var(--dt)">双峰</text>
  <rect x="115" y="44" width="12" height="8" fill="url(#vg3)" stroke="#f59e0b" stroke-width="1"/>
  <text x="130" y="51" font-size="7" fill="var(--dt)">均匀</text>

  <!-- 统计说明 -->
  <text x="115" y="70" font-size="7" fill="var(--dt)">宽度=密度</text>
  <text x="115" y="80" font-size="7" fill="var(--dt)">— 中位数</text>
  <text x="115" y="90" font-size="7" fill="var(--dt)">○ 均值</text>
</svg>
```

**与箱线图的区别：**
```
箱线图：显示四分位数，离散简洁，适合多组对比
小提琴图：显示完整密度分布，形状信息丰富，适合分析分布形态

小提琴图优势：
- 可识别单峰/双峰/多峰分布
- 可观察数据偏态（左偏/右偏）
- 可比较分布宽窄（离散程度）
```

**路径绘制说明：**
```
小提琴形状 = 左右对称的平滑曲线
宽度 = 该位置的样本密度

左半边：从顶部沿左侧曲线到底部
右半边：从顶部沿右侧曲线到底部

贝塞尔曲线控制点决定形状：
C x1 y1, x2 y2, x y
控制点越远，曲线越平缓
```

**使用场景：**
```
- 实验数据分布形态对比
- 用户行为时间分布
- 考试成绩分布分析
- 收入/房价分布研究
- 多组数据偏态对比
```
