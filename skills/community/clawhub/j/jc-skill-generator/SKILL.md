---
name: skill-generator
description: "Extract completed work into reusable AgentSkills. Ask user after complex task completion whether to generate a skill."
metadata: {"openclawbot":{"emoji":"🧬"}}
---

# Skill Generator

将已跑通的工作流程、工具、经验沉淀为可复用的 Skill。

## 触发规则

**每个对话循环结束时**，扫描本次对话中的工作产出，如果满足任一条件则触发：

- 跑通了一个完整的工作流程（多步骤，有明确输入和输出）
- 新建或优化了一个可复用的工具/脚本
- 完成了一次需要记录经验的任务（踩坑、确认环境、配置等）

**触发方式**：在回复中询问用户 — "要不要把这个工作流程沉淀成一个 Skill？" 

如果用户说不，不追问。如果说要，按下面流程执行。

## 生成流程

1. 确认范围：和用户快速确认要沉淀的核心内容（1-2 句话即可）
2. 创建 `skills/<name>/SKILL.md`，遵循 `skill-creator` 规范
3. 如有脚本/模板，放入 `scripts/` 或 `references/`
4. 用 `skill-creator` 验证格式
5. 告知用户生成完成，说明技能名、触发词、覆盖场景

## SKILL.md 写作要点

- 前面 YAML frontmatter 必须有 `name` + `description`
- `description` 是触发短语，简短精准（如 "Parse local video files into transcript and analysis"）
- 正文只写 AI 需要的关键信息：工作流程、命令、注意事项、坑
- 不要写背景介绍，不要写通用知识
- 命令语法、路径格式等容易出错的地方要精准

## 使用模板

见 `references/skill-template.md`
