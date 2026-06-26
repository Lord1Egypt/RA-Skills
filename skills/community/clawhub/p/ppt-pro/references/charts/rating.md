# 评分指示器（5分制）

`chart_type: rating`

> **视觉灵魂**：实心 vs 空心 = 已达到 vs 未达到。人脑对"圆点阵列"的计数速度极快，3/5 和 5/5 的差异一瞬间就能感知。

## 结构原理

用一行圆点表示评分：实心圆 = 已得分，空心圆 = 未得分。

```html
<div style="display:flex; gap:6px;">
  <!-- 实心圆（已得分） -->
  <div style="width:12px; height:12px; border-radius:50%; background:var(--accent-1);"></div>
  <!-- 空心圆（未得分） -->
  <div style="width:12px; height:12px; border-radius:50%; border:2px solid var(--accent-1); background:transparent;"></div>
</div>
```

> 以上为 **结构参考**。实心/空心数量根据实际评分调整。

## 灵动指引

- 圆点不一定要用圆形 -- 条状矩形（4px x 12px）也可以表达评分，且视觉更现代
- 圆点大小可以根据卡片空间调整（8-14px 范围内）
- 如果是半分制（如 4.5/5），可以用半实心圆（左半实心右半空心，用 clip-path 或 overlay div 实现）
- 评分指示器特别适合在 list 卡片中紧跟每条项目后面
