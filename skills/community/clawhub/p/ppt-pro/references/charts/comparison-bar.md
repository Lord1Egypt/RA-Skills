# 对比柱（两项对比）

`chart_type: comparison_bar`

> **视觉灵魂**：两根柱子的高度差就是结论 -- 观众一眼就能看出"谁更高"，不需要读数字就能理解对比结果。

## 结构骨架

```html
<!-- 容器：柱体 + 标签 纵向排列 -->
<div style="display:flex; flex-direction:column; gap:0;">
  <!-- 图表区：两根柱体从底部对齐 -->
  <div style="display:flex; gap:8px; align-items:flex-end; height:80px;">
    <div style="flex:1; border-radius:4px 4px 0 0; background:var(--card-bg-from);
                height:40%;"></div>
    <div style="flex:1; border-radius:4px 4px 0 0; background:var(--accent-1);
                height:80%;"></div>
  </div>
  <!-- 标签区 -->
  <div style="display:flex; gap:8px; margin-top:8px;">
    <span style="flex:1; text-align:center; font-size:12px;
                 color:var(--text-secondary);">标签A</span>
    <span style="flex:1; text-align:center; font-size:12px;
                 color:var(--text-secondary);">标签B</span>
  </div>
</div>
```

> 以上代码是**结构参考**，具体的 height 百分比、gap、容器高度都应根据实际数据和所在卡片空间灵活调整。

## 灵动指引

- "赢"的那根柱子用 accent 色，"输"的用 card-bg-from（低存在感），让结论一目了然
- 柱子高度差越大，视觉冲击力越强 -- 可以用数据的比例关系放大差异感
- 柱子顶部可以叠加数据数字（用 HTML 元素叠加，不用 SVG text）
- 容器高度根据卡片空间灵活调整，不要永远 80px
