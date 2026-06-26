# Formatter

Rules for structuring the output into a Feishu cloud document.

## Document Name

Use one single Feishu document named:
`🤖 Robot Paper Daily Brief`

## Document Structure

Use this structure:

```md
🤖 Robot Paper Daily Brief
├── 📌 使用说明
├── 2026.04.06 周一
│   ├── 今日编辑按语
│   ├── Paper 01
│   ├── Paper 02
│   ├── Paper 03
│   ├── Paper 04
│   └── Paper 05
├── 2026.04.05 周日
├── 2026.04.04 周六
└── 📈 本周趋势回顾
```

Rules:
- the pinned header stays fixed at the top
- the newest day is inserted directly below the pinned header
- older days remain below in reverse chronological order
- each day is a level-1 heading
- each paper is a level-2 heading
- use horizontal rules between papers when useful

## Pinned Header

Create this once and do not overwrite it:

```md
# 📌 使用说明

**这是什么：** 每日更新的人形机器人论文简报，面向工业设计师与产品团队。
**更新时间：** 每天早上 8:00
**每日内容：** 5 篇前一日最值得关注的人形机器人论文，翻译为设计师友好语言。
**怎么读：**
- 赶时间：看「⚡ 一句话人话」和「📊 评分表」
- 有 10 分钟：加看「🎨 设计师必读」
- 深入了解：看完整内容和延伸链接
```

## Formatting Rules

- use Markdown compatible with Feishu
- tables must use pipe syntax
- use `★` and `☆` for ratings
- use emoji sparingly but consistently
- use bold for structure, not decoration

## Length Guidelines

| Section | Target Length |
|---|---|
| 一句话人话 | ≤ 40 中文字 |
| 核心内容 | 180-320 字 |
| 设计师必读 | 150-280 字 |
| 每篇论文总长 | 450-750 字 |
| 每日编辑按语 | 80-150 字 |
| 每日文档总长 | 2500-4500 字 |
