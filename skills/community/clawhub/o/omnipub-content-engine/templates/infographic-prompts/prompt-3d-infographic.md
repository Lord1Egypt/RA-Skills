# AI 信息图提示词 · 3D等距风（即梦/LOVART/ChatGPT 三引擎版）

**用途**：公众号封面（900×383）或内文数据图（900×506）。3D 等距场景视觉冲击力强，适合「行业趋势/市场规模」类核心数据。

---

## 数据输入位（每次生成时替换）

- 主标题（中文，≤12字）：【待填】
- 副标题（中文，≤20字）：【待填】
- 数据卡片1：【数字+单位+标签】
- 数据卡片2：【数字+单位+标签】
- 数据卡片3：【数字+单位+标签】
- 底部洞察（中文，≤20字）：【待填】
- 数据来源：机构名 + 年份
- 场景主题：医院/办公室/家庭/城市（按内容选）

---

## 完整提示词（8要素）

```
INFOPAGE 01/01, 3D ISOMETRIC RENDERING.
MAIN TITLE: "主标题" (Chinese, bold, top center, dark green #639922 on white).
SUBTITLE: "副标题" (Chinese, medium, below title, purple #534AB7).
DATA CARDS: three floating 3D cards, each with large bold number (blue #2196F3) and small Chinese label, arranged diagonally in the mid-ground.
SCENE: 3D isometric scene of 场景主题, soft pastel colors, depth of field, consistent with brand palette (green #639922, purple #534AB7, blue #2196F3, light gray background).
BOTTOM INSIGHT: one sentence in Chinese at bottom-left: "底部洞察".
DATA SOURCE: bottom-right corner, small text: "数据来源：机构名 年份".
BRAND: bottom-left small logo area reserved for "心明增长实验室" (leave clean white space, no actual logo render).
LIGHTING: soft studio lighting, clean shadows, editorial quality, 8k, high detail.
-no text errors, -no watermark, -no border, -no extra text, -no people, -no english words except numbers.
```

## 引擎适配

### 即梦 AI（jimeng.jianying.com）
- 尺寸：图片生成选「自定义」→ 900×383（封面）或 16:9（内文）
- 直接粘贴完整提示词；若中文文字渲染有误，框选文字区域用「局部重绘」修
- 约束补充：`海报排版, 居中构图, 商业级质感`

### LOVART（lovart.net）
- 风格参数：Design → Editorial / Infographic Poster
- 提示词追加：`clean grid layout, data-viz poster style, generous whitespace`
- 中文文字可后置：先生成纯场景，再用其文字工具叠加中文

### ChatGPT / DALL-E 系
- 追加数据清单让它自己排版：
```
Please lay out the following data as an isometric infographic poster in Chinese:
- Title: 主标题
- Subtitle: 副标题
- Data: 数据卡片1; 数据卡片2; 数据卡片3
- Insight: 底部洞察
- Source: 数据来源
- Brand: 心明增长实验室
Use brand colors #639922, #534AB7, #2196F3 on light background.
```

### Midjourney
- 文字弱，仅生成视觉：剥离所有中文，只保留场景描述 + `isometric, pastel, clean, 8k`
- 文字后期用 PS/Canva 叠加

## 常见翻车修正

| 问题 | 修正 |
|---|---|
| 中文乱码 | 换即梦局部重绘 / 剥离文字后期叠加 |
| 数字错误 | 提示词中数字加引号写死，加 `-no number errors` |
| 场景抢戏 | 加 `data cards dominant, scene background soft` |
| 颜色跑偏 | 写死十六进制色值，加 `strict brand palette` |
