# timeline · 时间轴

**适用：** 历史节点、事件序列、发展脉络
**高度：** 38px（紧凑横向）

```html
<svg viewBox="0 0 540 38" style="width:100%;height:38px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <line x1="10" y1="12" x2="530" y2="12" stroke="#1e293b" stroke-width="1.5"/>
  <!-- 节点 1 -->
  <circle cx="60"  cy="12" r="5" fill="var(--p)"/>
  <text x="60"  y="27" text-anchor="middle" font-size="8.5" fill="#64748b">2016</text>
  <text x="60"  y="37" text-anchor="middle" font-size="8" fill="var(--mt)">事件A · 88%</text>
  <!-- 节点 2 -->
  <circle cx="200" cy="12" r="5" fill="var(--p)"/>
  <text x="200" y="27" text-anchor="middle" font-size="8.5" fill="#64748b">2018</text>
  <text x="200" y="37" text-anchor="middle" font-size="8" fill="var(--mt)">事件B · 91%</text>
  <!-- 节点 3（警示色） -->
  <circle cx="360" cy="12" r="5" fill="#ef4444"/>
  <text x="360" y="27" text-anchor="middle" font-size="8.5" fill="#64748b">2020</text>
  <text x="360" y="37" text-anchor="middle" font-size="8" fill="#fca5a5">事件C · 100%</text>
  <!-- 节点 4（正向色） -->
  <circle cx="500" cy="12" r="5" fill="#10b981"/>
  <text x="500" y="27" text-anchor="middle" font-size="8.5" fill="#64748b">2023</text>
  <text x="500" y="37" text-anchor="middle" font-size="8" fill="#6ee7b7">事件D · 76%</text>
</svg>
```

**参数说明：**
- 节点 cx 均匀分布，可按时间比例分配 x 坐标
- 节点颜色：普通=var(--p)，警示=#ef4444，积极=#10b981
- 节点下方：y=27 显示时间标签，y=37 显示事件简述
- 节点间距最小 100px，避免标签重叠
