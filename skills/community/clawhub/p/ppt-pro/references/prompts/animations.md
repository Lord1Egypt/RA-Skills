## 6. HTML 预览专属动画效果（可选增强）

> 以下 CSS 动画仅在 HTML 预览中生效。导出 PPTX 时（PNG 整页截图或可编辑管线的截图阶段）动画属性会被自动忽略，不影响最终输出。
> 建议在 Prompt #4 生成 HTML 时，选择性嵌入以下动画以提升预览观感。

### 卡片渐入动画

在 `<style>` 中添加：
```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

在每个卡片 `<div>` 上添加 style：
```
animation: fadeInUp 0.6s ease forwards;
animation-delay: 0.1s; /* 每张卡片递增 0.1s */
opacity: 0;
```

### 数据数字计数动画

使用 CSS `@property` 实现纯 CSS 计数动画：
```css
@property --num {
  syntax: '<integer>';
  inherits: false;
  initial-value: 0;
}
.counter {
  animation: count 1.5s ease forwards;
  counter-reset: num var(--num);
}
.counter::after {
  content: counter(num);
}
@keyframes count {
  to { --num: 2847; }
}
```

**提示**：`::after` 伪元素在 HTML 预览中工作正常。导出 PPTX 时（管线 A 截图或管线 C 文本提取阶段），`::after` 可能丢失，可选择性保留一个真实 `<span>` 作为 fallback：

```html
<!-- 正确写法：动画 + fallback 共存 -->
<div class="counter" style="position:relative;">
  <!-- fallback: PPTX 导出时显示此 span -->
  <span style="opacity:0; animation: showFallback 0s 1.5s forwards;">2847</span>
</div>
```
```css
/* HTML 预览中：::after 动态计数，span 隐藏 */
/* PPTX 导出时：::after 丢失，span 显示最终值 */
@keyframes showFallback { to { opacity: 1; } }
.counter::after ~ span { opacity: 0 !important; } /* 有动画时隐藏 fallback */
```

> 这个方案让 HTML 预览有酷炫的计数效果，同时 PPTX 中不会丢失数字。

### 进度条填充动画

```css
@keyframes fillBar {
  from { width: 0%; }
  to { width: var(--target-width); }
}
.bar-fill {
  animation: fillBar 1s ease-out 0.3s forwards;
  width: 0%;
}
```

在进度条 div 上设置 `--target-width: 73%;` 并添加 class="bar-fill"。

### 折线图描边动画

```css
@keyframes drawLine {
  from { stroke-dashoffset: var(--total-length); }
  to { stroke-dashoffset: 0; }
}
```

在 SVG polyline/path 上设置：
```
stroke-dasharray: 300;
stroke-dashoffset: 300;
animation: drawLine 1.5s ease forwards 0.5s;
```

### 使用原则

1. **不超过 3 种动画/页**：避免过度花哨
2. **延迟递增**：卡片按从左到右、从上到下的顺序递增 0.1-0.15s
3. **数据页优先**：数据数字和进度条的动画效果最好，优先使用
4. **章节封面不加动画**：保持呼吸页的安静感

