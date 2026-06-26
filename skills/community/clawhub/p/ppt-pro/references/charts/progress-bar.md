# 进度条（百分比/完成度）

`chart_type: progress_bar`

> **视觉灵魂**：一条横向的"已完成 vs 未完成"对比 -- 填充长度就是答案，观众瞬间理解"到了哪里"。

## 结构骨架

```css
.progress-bar {
  height: 8px; border-radius: 4px;
  background: var(--card-bg-from);
  overflow: hidden;
}
.progress-bar .fill {
  height: 100%; border-radius: 4px;
  background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
  /* width 用内联 style 设置百分比 */
}
```

## 灵动指引

- 进度条的高度不必永远 8px -- 在大面积卡片中可以用 12-16px 制造更强的存在感
- 填充色可以根据数据语义变化：高值用 accent 色（积极），低值用红色（警示）
- 进度条左上方叠加百分比数字可以增强信息量
- 多个进度条竖排列时，可以给每条设置不同的 accent 色 + 递增延迟动画（HTML 预览增强）
