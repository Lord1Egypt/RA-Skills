# Idea to Prompt · 想法 → 结构化提示词 Agent Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 把用户杂乱无章、语序不清、可能重复或自相矛盾的原始想法，整理成清晰、结构化、可直接执行的提示词。
> Convert rambling, disorganized user thoughts into a clear, structured, actionable prompt — for coding tasks, content creation, or any general request.

## 它解决什么问题 Why

用户常常直接倒出一堆零散想法（"我有一堆想法"、"帮我整理一下"、"转成提示词"），如果 AI 直接开干，很容易方向跑偏。这个 skill 提供一套可复用的整理流程：

1. **判断想法类型**：开发任务 / 内容创作 / 决策规划 / 其他
2. **拆解检查**：核心目标、多诉求混在一起、自相矛盾、隐含假设、范围边界
3. **决定是否追问**：只在"会根本性跑偏"时问 1–3 个选择题，否则用"假设说明"让用户快速纠正
4. **按类型产出结构化提示词**：每种类型有对应的提示词模板

**核心原则：宁可多问一句关键的，不要瞎猜；但也不要为了显得谨慎而每次都问一堆无关痛痒的问题。**

## 使用场景 Use cases

- 用户用口语/碎片化方式描述需求，想转成能用的提示词
- 一句话里揉了好几个诉求，需要拆开
- 需要给 Claude Code / 其他 AI 写清晰的任务描述

## 触发词 Trigger phrases

"我有一堆想法" / "帮我整理一下" / "转成提示词" / "我想说的是" —— 或任何明显非结构化的头脑风暴式输入。

## 输出模板 Templates

**类型 A（开发任务）**：
```
【目标】一句话说清楚要做什么
【涉及范围】具体文件/模块（不确定先只读定位，不要猜路径）
【风险分类】纯UI/文案 → 可直接改；计算逻辑/金额/权限 → 先排查影响面；范围不确定 → 先确认
【约束】明确哪些不要动
【假设说明】未追问时列出所做假设
```

**类型 B（内容创作）**：`【目标】【风格/语气】【必须包含】【避免】【格式】【假设说明】`

**类型 C（决策/规划）**：`【要决定的事情】【已知约束】【用户倾向/顾虑】【希望AI提供什么】【假设说明】`

完整流程与判断依据见 `SKILL.md`。

## 安装 Install

```bash
# ClawHub
openclaw skills install idea-to-prompt

# 或手动复制到 skills 目录（Claude Code / OpenClaw / pi 等）
git clone https://github.com/BlackCorvu/idea-to-prompt.git
cp -r idea-to-prompt ~/.pi/agent/skills/idea-to-prompt
```

## 边界 Boundaries

- 职责止于"产出清晰的提示词"，**不自动往下执行**，除非用户明确说"直接照这个做"
- 类型 A 且信息完整无歧义时，可直接建议"这个可以直接执行了"，避免走流程而本末倒置

## License

[MIT](LICENSE)

---

*If this skill helps you organize your thinking, consider giving it a ⭐.*
