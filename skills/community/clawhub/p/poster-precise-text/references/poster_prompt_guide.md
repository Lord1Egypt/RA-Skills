# 海报生成 Prompt 参考

## 纯文字海报 Prompt 模板

```
Create a Chinese health/education poster. Clean, professional medical style.
Color scheme: teal (#00857C) + white + orange accents.
Vertical scroll layout, 9:16 aspect ratio.

MAIN TITLE: [标题文字]
SUBTITLE: [副标题/来源]

SECTION 1 - [板块1标题]
Layout: 3 cards side by side with icons
Card 1: [标题] | [内容]
Card 2: [标题] | [内容]
Card 3: [标题] | [内容]

SECTION 2 - [板块2标题]
Layout: 4x2 numbered grid with medical icons
[数字] [文字内容]
... (8 items)

SECTION 3 - [板块3标题]
Layout: 4 numbered items with icons
[数字] [文字内容]
... (4 items)

SECTION 4 - [板块4标题]
Left box (white): [内容]
Right box (teal): [内容]

Style: Clean infographic, all text in Chinese, clear typography.
```

## 配色速查

| 场景 | 主色 | 辅色 |
|------|------|------|
| 医疗健康 | #00857C | #F5A623 |
| 政务宣传 | #C41E3A | #FFD700 |
| 教育科普 | #2563EB | #10B981 |
| 金融投资 | #1A1A2E | #F5A623 |
| 社区服务 | #00857C | #10B981 |

## 图像生成注意事项

1. **中文精准度**：MiniMax / 图像生成工具对中文渲染有限，复杂文字（8字以上）容易变形
2. **长文本**：超过20字的内容建议用 HTML 层处理
3. **多字号层级**：标题/正文/注释至少三个字号层级
4. **图标风格**：医学类图标用线性图标，禁用表情符号
