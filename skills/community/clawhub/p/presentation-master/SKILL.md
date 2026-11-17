---
name: presentation-master
description: >-
  把 AI 变成演示搭档：从大纲构思、模板制作、视觉设计到演讲表达的全流程。
  覆盖演示结构决策、幻灯片内容密度与标题层级 lint、视觉设计原则。
  触发词："演示大纲"、"PPT 模板"、"幻灯片设计"、"演讲表达"、"路演 Pitch"、"字数密度"。
agent_created: true
metadata:
  version: 1.0.0
  category: 演示
  difficulty: 进阶
  architecture: superpower
---

# 演示大师

> 让 AI 帮你做出有结构、有密度、有说服力的演示——从一页纸大纲到台上演讲。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放 `references/` 按需加载，
细粒度能力放 `skills/` 子技能，确定性 lint 交给 `scripts/`，结构模板放 `assets/`。

## 何时使用

- 要搭一页一主张的演示大纲，不确定结构与页数
- 做 PPT 模板或品牌视觉规范
- 需要检查幻灯片字数密度、标题层级、跨页一致性
- 准备路演 Pitch 或技术分享的叙事与表达
- 要做视觉设计（字号阶梯、图表选型、配色对比度）

## 能力索引（超级技能路由）

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 演示结构：时长倒推页数、四段法、钩子/CTA | [references/deck-structure-playbook.md](references/deck-structure-playbook.md) | 演示结构 页数 钩子 CTA 时长 大纲 记忆锚点 |
| 幻灯片内容规则：字数/标题层级/一致性 lint | [references/slide-content-rules.md](references/slide-content-rules.md) | 幻灯片 字数 密度 标题层级 一致性 一页一主张 |
| 视觉设计原则：字号阶梯/图表选型/对比度 | [references/visual-design-principles.md](references/visual-design-principles.md) | 视觉设计 字号阶梯 图表选型 配色 对比度 栅格 |
| 演示创建：大纲构思、内容组织、Slide 编写 | [skills/presentation-creator/SKILL.md](skills/presentation-creator/SKILL.md) | 演示创建 大纲 内容 故事线 全流程 |
| PPT 模板：主题/母版/品牌模板 | [skills/ppt-template-creator/SKILL.md](skills/ppt-template-creator/SKILL.md) | PPT 模板 母版 品牌 样式库 主题 |
| 演示设计：视觉层级、信息图表、排版 | [skills/presentation-design/SKILL.md](skills/presentation-design/SKILL.md) | 演示设计 视觉层级 信息图表 排版 配色 |
| 演讲表达：叙事、节奏、互动、Q&A | [skills/presentation-delivery/SKILL.md](skills/presentation-delivery/SKILL.md) | 演讲表达 叙事 节奏 互动 Q&A Pitch |

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，把内容规范变成可复现的机器检查：

- `scripts/check_presentation.py outline --file <deck.md>` — 检查字数/标题层级/重复标题
- `scripts/check_presentation.py selfcheck` — 校验内置资产（规则+示例大纲）0 ERROR

运行示例：

```bash
python3 scripts/check_presentation.py outline --file deck.md
```

## 模板资源

`assets/` 提供可直接套用的规范与模板：

- [assets/presentation_rules.json](assets/presentation_rules.json) — 内容规则（脚本 `outline` 的规则来源，可自定义）
- [assets/presentation-outline.example.md](assets/presentation-outline.example.md) — 合规大纲示例（脚本 selfcheck 回检 0 ERROR）
- [assets/presentation-structure-template.md](assets/presentation-structure-template.md) — 演示结构模板

## 核心原则（始终遵循）

1. **一页一主张**：每页一句话记忆锚点，观众记不住两件事。
2. **密度红线**：内容页 ≤120 字，段落拆要点，用脚本 lint 而非凭感觉。
3. **结构先行**：先定时长倒推页数，再填内容；钩子开场、CTA 收尾。
4. **渐进式加载**：先读路由表与对应 `references/`，再动手。
5. **明确边界**：脚本只做内容规范自检、出报告，不替你拍板演讲风格、不改你的源文件。
6. **视觉服务信息**：图表只讲一件事，对比度算出来而非看出来。

## 与其他技能协作

- 视觉资产与品牌深度创作 → `skills-repo/visual-designer`
- 创业融资与商业叙事 → `skills-repo/startup-founder`
- 办公效率与 PPT 自动化 → `skills-repo/office-master`
