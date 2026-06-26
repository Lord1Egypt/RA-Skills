# gantt · 甘特条

**适用：** 阶段计划、进度展示、时间分配
**高度：** 38px（单行计划条）

```html
<svg viewBox="0 0 540 38" style="width:100%;height:38px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <rect x="0"   y="4" width="175" height="14" rx="3" fill="rgba(239,68,68,0.8)"/>
  <text x="88"  y="14" text-anchor="middle" font-size="8.5" fill="white">阶段1：W1-2</text>
  <rect x="179" y="4" width="175" height="14" rx="3" fill="rgba(99,102,241,0.8)"/>
  <text x="267" y="14" text-anchor="middle" font-size="8.5" fill="white">阶段2：W3-4</text>
  <rect x="358" y="4" width="175" height="14" rx="3" fill="rgba(16,185,129,0.8)"/>
  <text x="445" y="14" text-anchor="middle" font-size="8.5" fill="white">阶段3：W5-6</text>
  <text x="0"   y="33" font-size="8" fill="#64748b">Week 1</text>
  <text x="175" y="33" font-size="8" fill="#64748b">Week 3</text>
  <text x="354" y="33" font-size="8" fill="#64748b">Week 5</text>
  <text x="530" y="33" font-size="8" fill="#64748b" text-anchor="end">Week 6</text>
</svg>
```

**多行甘特（叠加变体，每行高度 20px）：**
```
行间 y 偏移规则：
  第1行：rect y=4，text y=14
  第2行：rect y=22，text y=32
  第3行：rect y=40，text y=50
  总高 = 行数×18 + 20（底部时间轴）
```

**参数说明：**
- 总可用宽 540px，每单位时间宽 = 540 / 总周期数
- 颜色建议：阶段1=红/橙，阶段2=蓝/紫，阶段3=绿（进展递进感）
- 文字长度超出时缩短标签，保证宽度 > 文字宽度至少 20px
