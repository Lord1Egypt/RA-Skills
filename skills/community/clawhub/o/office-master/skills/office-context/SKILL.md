---
name: office-context
description: 办公生产上下文记忆：捕获并复用用户的品牌色板、字体、模板路径与版式骨架，让 Markdown→Office/PPT 自动化在多会话中保持统一品牌与版式
source:
  type: original
  repo: skills-repo/office-master
  path: skills/office-context/SKILL.md
  version: "1.0"
  updated: "2026-08-12"
metadata:
  category: 办公效率
  platform: 通用
  difficulty: 入门
---

# 办公上下文记忆

> 把用户的品牌与版式偏好固化成一个可复用上下文，让每次文档 / PPT 产出都自动对齐，不必反复交代。

## 能力

- 捕获品牌五件套：主色、辅色、强调色（均 HEX）、标题字体、正文字体、logo 路径
- 登记模板与规范资产路径：`reference-doc.docx`、PPT 母版、本仓库 [assets/doc-style-rules.json](../../assets/doc-style-rules.json)、演示 brief 模板
- 记录常用文档 / 演示骨架（月度报告、周报、提案）与固定章节顺序
- 在 `md-to-office` / `ppt-automation` 调用前注入上下文，保证跨会话一致

## 何时使用

- 需要反复生成同一品牌的 Word 报告 / PPT 时
- 团队要统一 Office 交付物的配色与版式时
- 新会话 / 新 Agent 接手既有文档项目，需快速对齐品牌时

## 工作流

1. 首次：与用户确认品牌五件套 + 模板路径，写入 `assets/office-context.json`（模板见 [references/office-context-playbook.md](../../references/office-context-playbook.md)）
2. 每次转换前：读取上下文 → 把品牌色 / 字体 / 模板传入 `md-to-office`（Pandoc `--reference-doc` / variables）或 `ppt-automation`（python-pptx 套色）
3. 漂移检测：对比上下文与产出，发现色板 / 字体不一致即回查上下文是否过期
4. 变更：品牌更新时只改 `office-context.json`，不动既有已生成文档

## 与兄弟技能协作

- 品牌 / 模板注入 → [skills/md-to-office](../md-to-office/SKILL.md)（Pandoc reference-doc）、[skills/ppt-automation](../ppt-automation/SKILL.md)（python-pptx 模板）
- 版式结构规范 → [references/doc-style-quality-gates.md](../../references/doc-style-quality-gates.md) + [assets/doc-style-rules.json](../../assets/doc-style-rules.json)
- 演示骨架 → [assets/presentation-brief-template.md](../../assets/presentation-brief-template.md)

## 边界

- 只管「用什么品牌 / 模板」，不替你写内容
- 上下文是约定文件，需人工确认后落地
- 不覆盖 `doc-style-rules.json`（那是结构门禁，非品牌库）
- 与 `productivity-master` 的 `memory-keeper`（个人知识 / 第二大脑）正交：本技能只管办公交付物的品牌与版式上下文
