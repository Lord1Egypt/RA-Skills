# AI 信息图提示词 · 图表主视觉风（chart-hero）

**用途**：公众号封面（900×383，2.35:1）——封面即数据海报，点击率最高的一类封面。适合「数据硬核风」文章。

---

## 数据输入位（每次生成时替换）

- 主标题（中文，≤8字，封面大字）：【待填】
- 数据对比（2-4组：标签+数值）：【A=XX，B=XX，C=XX】
- 趋势关键词（上升/下降/拐点）：【待填】
- 数据来源：机构名 + 年份

---

## 完整提示词（8要素）

```
DATA POSTER COVER, 2.35:1 WIDE LAYOUT, editorial finance style.
MAIN HEADLINE: "主标题" (Chinese, bold, huge, left-aligned, white text, top area).
CHART: large minimal bar/line chart in the right 60% of the canvas, bars in brand gradient of green #639922 and blue #2196F3, one highlight bar in purple #534AB7.
DATA LABELS: 2-4 data labels (数值 + 中文标签), bold numbers, clean sans-serif.
TREND MARKER: arrow or callout indicating "趋势关键词" (e.g. 上升), purple accent.
SOURCE: bottom-right, small white 60% opacity text: "数据来源：机构名 年份".
BACKGROUND: deep navy #0C447C flat background, subtle grid lines, dark data-viz mood.
-no text errors, -no watermark, -no border, -no people, -no english except numbers.
```

## 引擎适配

### 即梦 AI
- 比例：自定义 900×383
- 深色背景是重点，若渲染偏亮，追加 `dark navy background #0C447C, high contrast`

### LOVART
- 风格：Editorial / Data Visualization
- 追加：`finance dashboard cover, strong typographic hierarchy`

### ChatGPT / DALL-E 系
```
Create a data-viz cover poster in Chinese, 2.35:1:
- Headline: 主标题 (white, bold)
- Chart: bar chart comparing 数据对比 (green/blue bars, one purple highlight)
- Trend: 趋势关键词 callout
- Background: deep navy #0C447C
- Source: 数据来源 (bottom right)
Editorial finance style, high contrast, no other text.
```

## 变体

- **折线版本**：把柱状图换为「陡峭上升的折线」，适合趋势文
- **环形版本**：大圆环图居中，适合占比文（如「90%的人输在第一步」）
- **深色/浅色**：浅色封面（白底+品牌色）适合专业风；深色封面适合硬核风，按所选主题定

## 封面点击率自检

- [ ] 标题 ≤8 字，字号大，远看可读
- [ ] 有 1 个视觉焦点（高亮柱/箭头/大数字）
- [ ] 颜色与文章主题一致
- [ ] 不堆字（封面上除标题外不超过 6 个文字元素）
