---
name: prompt-hardening
version: 0.5.0
description: 硬化 agent prompt、system prompt、SOUL.md、AGENTS.md、cron prompt 使 LLM 可靠遵循指令。触发词：agent 不听话、忽略规则、绕过约束、prompt 优化、指令合规、规则强化、prompt 硬化、LLM 不遵守、模型违规、creative circumvention。Use when agent ignores rules, disobeys instructions, bypasses tool constraints, needs prompt optimization, instruction compliance improvement, or rule hardening. 不适用于代码生成、代码审查、测试编写等执行型任务。参见 improvement-orchestrator (用于 skill 质量改进)、code-review-enhanced (用于代码审查)。
license: MIT
triggers:
  - agent 不听话
  - 忽略规则
  - 绕过约束
  - prompt 优化
  - 指令合规
  - 规则强化
  - prompt 硬化
  - LLM 不遵守
  - 模型违规
  - instruction following
  - rule enforcement
  - prompt compliance
  - agent disobeys
author: OpenClaw Team
---

# Prompt Hardening

硬化 agent prompt 使其可靠遵循指令的系统化方法。

> **核心原则：Prompt 不是策略文档，而是错误纠正系统。最可靠的约束不是更好的措辞，而是结构化不可能性。**

## When to Use

- Agent 反复违反同一条规则
- 部署新的 agent system prompt 前需要质量审计
- Agent "创造性地"绕过工具约束或长对话后行为漂移
- 如果不确定是否需要硬化，先用 `scripts/audit.sh` 审计一遍再决定

## When NOT to Use

- 不适用于代码生成、代码审查等执行型任务（用 code-review-enhanced、tdd-workflow）
- 不适用于 skill 质量改进流程（用 improvement-orchestrator）
- 不要把所有 prompt 问题都归为"硬化不够"——有些需要代码级强制（P13）而不是更多文字

<example>
正确用法：对 SOUL.md 中被反复违反的 dispatch 规则进行硬化
输入: "MUST 通过 dispatch.sh 派发"（一句话，模型 3 次无视）
应用: P1+P2+P3+P5+P7+P16 六模式叠加
结果: 合规率从 ~50% → ~90%（配合 EXEC GUARD plugin P13 达到 ~99%）
</example>

<anti-example>
错误用法：用 prompt-hardening 替代代码级强制
只改 SOUL.md 不加 plugin hook → prompt 层面永远不是 100% 可靠
关键约束 MUST 同时有代码级强制（P13）作为备份
</anti-example>

## Quick Reference

| 场景 | 推荐模式 | 强度 |
|------|---------|------|
| 模型反复违反同一条规则 | P1 三重强化 + P13 代码级 | 最强 |
| 模型绕过工具约束 | P2 工具强制 + P3 穷举枚举 | 强 |
| 模型"合理化"违规 | P5 反推理阻断 | 强 |
| 长对话偏离规则 | P9 漂移防护 + P11 Echo-Check | 中 |
| 新规则首次部署 | P4 条件触发 + P7 示例对 | 标准 |

## 16 个硬化模式

详细说明、示例和来源见 `references/patterns.md`。

| # | 模式 | 一句话说明 | 来源 |
|---|------|-----------|------|
| P1 | 三重强化 | MUST/NEVER + good/bad example + I REPEAT | Claude Code, ChatGPT |
| P2 | 工具强制 | Use X (NOT Y) + 失败原因 | Claude Code, Warp |
| P3 | 穷举否定 | ✅/❌ 列出所有允许/禁止行为 | Codex CLI |
| P4 | 条件触发 | 当 X → MUST Y / NEVER Z | Gemini CLI |
| P5 | 反推理阻断 | 预判模型合理化借口并阻断 | Claude.ai |
| P6 | 优先级层级 | 显式声明规则冲突时谁赢 | Gemini, Jules |
| P7 | 行为锚定 | good/bad example + reasoning 标签 | Claude Code |
| P8 | 范围限制 | 做要求的事，不多做 | Claude Code, Warp |
| P9 | 漂移防护 | 长对话中注入提醒 | Claude.ai |
| P10 | 信任边界 | 区分可覆盖/不可覆盖的指令源 | ChatGPT |
| P11 | Echo-Check | 执行前复述约束 | Reddit (40-60% ↑) |
| P12 | 约束优先 | 约束 token > 任务描述 token | sinc-LLM (42.7%) |
| P13 | 结构化不可能 | 代码级强制 > prompt 强制 | Anthropic |
| P14 | 状态机门禁 | 布尔前置条件锁定阶段 | Factory DROID |
| P15 | 自我归因修正 | 第一人称"我刚才做错了"纠正 | CrewAI |
| P16 | 首尾重复 | 关键约束放 prompt 开头+结尾 | Lost in the Middle |

## 可靠性等级

| 防护层级 | 可靠性 | 组合使用 | 可靠性 |
|---------|--------|---------|--------|
| 软约束 | ~40% | P1 + P5 | ~90% |
| MUST/NEVER | ~70% | P1 + P5 + P13 | ~99% |
| MUST + 示例 | ~80% | P1 + P5 + P13 + retry | ~100% |

## CLI

```bash
# 审计现有 prompt（16 项检查）
~/.claude/skills/prompt-hardening/scripts/audit.sh ~/path/to/SOUL.md
```

## 应用清单

| # | 检查项 |
|---|--------|
| 1 | P0 规则用了三重强化（MUST + 反面示例 + 重复）？ |
| 2 | 工具约束用了 `Use X (NOT Y)` + 失败原因？ |
| 3 | 禁止行为穷举列出？ |
| 4 | 关键触发用了 `当 X → MUST Y` 格式？ |
| 5 | 有反推理阻断？ |
| 6 | 优先级层级显式声明？ |
| 7 | 有好/坏示例对？ |
| 8 | 范围边界明确？ |
| 9 | 长对话有漂移防护？ |
| 10 | 信任边界明确？ |
| 11 | 关键操作前有 echo-check？ |
| 12 | 约束 token > 任务描述 token？ |
| 13 | 最关键约束有代码级强制（L5）备份？ |
| 14 | 多步操作有状态机门禁？ |
| 15 | 违规后有自我归因修正模板？ |
| 16 | 关键约束在 prompt 首尾都出现？ |

## Usage

```
1. 读取目标 prompt
2. 识别模型历史违反过的规则（最高优先级硬化）
3. 运行 scripts/audit.sh 获取 16 项检查结果
4. 历史违反 → P1 三重强化 + P13 代码级
5. 重要规则 → P2 + P4 + P5
6. 一般规则 → P3 + P7
7. 验证约束 token 占比 > 40%
```

## Output Artifacts

| 请求 | 交付物 |
|------|--------|
| 硬化 prompt | 重写后的 prompt 文件 |
| 审计 prompt | 16 项检查清单 + 改进建议 |
| 分析违规 | 违规模式分类 + 硬化方案 |

## References

- `references/patterns.md` — 16 个模式的详细说明和代码示例
- `references/sources.md` — 13 个研究来源

## Operator Notes

- Advisory/planning skill. Does not modify target prompts automatically.
- When execution is needed, call out that the operator must apply changes manually or use improvement-executor.
