# AI 信息图提示词 · 扁平极简风（即梦/LOVART/ChatGPT 三引擎版）

**用途**：公众号内文配图（900×506 / 900×450）、头条正文图。扁平风文字承载能力强，适合「方法步骤/流程/清单类」内容，也是最不容易翻车的风格。

---

## 数据输入位（每次生成时替换）

- 主标题（中文，≤10字）：【待填】
- 流程/步骤（3-5步，每步≤8字）：【步骤1/步骤2/步骤3】
- 关键数字（1-3个）：【数字+单位】
- 底部一句话（≤16字）：【待填】
- 数据来源：机构名 + 年份

---

## 完整提示词（8要素）

```
FLAT DESIGN INFOGRAPHIC, 16:9 LAYOUT, clean white background.
MAIN TITLE: "主标题" (Chinese, bold, large, top-left, dark #2C2C2A).
PROCESS: horizontal 3-5 step flow (icons + short Chinese labels: 步骤1 → 步骤2 → 步骤3), each step in a rounded square tile, green #639922 outline.
KEY NUMBERS: 1-3 large flat number badges (blue #2196F3), with small Chinese unit labels, placed in a row.
BOTTOM LINE: one sentence in Chinese at bottom: "底部一句话".
SOURCE: bottom-right corner, small gray text: "数据来源：机构名 年份".
STYLE: flat vector, minimal, generous whitespace, 2px strokes, no gradients, no shadows, no 3D.
-no text errors, -no watermark, -no border, -no extra elements, -no english words except numbers.
```

## 引擎适配

### 即梦 AI
- 比例：16:9（900×506）或 2:1（900×450）
- 直接粘贴；步骤图标若乱，指定 `linear icons, minimal line icons`

### LOVART
- 风格：Flat / Minimal / Infographic
- 追加：`modular grid, tile layout, san-serif Chinese font friendly`

### ChatGPT / DALL-E 系
```
Design a flat infographic poster in Chinese with a clean white background:
- Title: 主标题
- Process: 步骤1 → 步骤2 → 步骤3 (tile icons)
- Key numbers: 数字+单位 (blue badges)
- Bottom line: 底部一句话
- Source: 数据来源
Color: green #639922, blue #2196F3, dark gray text. Flat vector style, no gradients, no 3D.
```

## 变体

- **清单风**：步骤换为「要点清单」（圆点+短句），适合「XX的5个误区」
- **对比风**：左右两栏（红/绿 或 蓝/灰），适合「XX vs XX」
- **时间轴风**：横向时间轴，适合「行业大事记/我的转型路径」
