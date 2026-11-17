---
name: meta-logic-method
description: >-
  Use ONLY when the user explicitly requests thinking-methodology work: 理清混乱思路 / 表达, 问题定义与根因分析, 方案设计与决策, 创新破局, 复盘与思维沉淀, 论证 / 推理 / 方案 Review, 思维质量验收, or mentions 元逻辑, 元法则, 子思维, 思维体系, meta-logic, meta-logic-method. Loads the meta-logic-method thinking system and dispatches tasks per the AGENTS.md 调度表 to meta/ (M-x), sub-skills/ (S-1~S-12), workflows/ (W-1~W-5), and reference/ (F/B/R). Do not use for ordinary coding, build, or debug tasks unless the user invokes this thinking system by name.
---

# Meta-Logic Thinking System (meta-logic-method)

Three-layer thinking rule system: meta-logic laws (`meta/`) > sub-thinking skills (`sub-skills/`) > reference (`reference/`), plus workflow compositions (`workflows/`).

## Entry point

**AGENTS.md is the single rule entry.** Read it before any thinking task; it contains the task-to-document dispatch table and the output protocols.

## How to use

1. Classify the task via the AGENTS.md 调度表, then load ONLY the documents it names (do not load the whole tree).
2. Respect the four-layer constraint: 元法 > 强制/禁止 > 建议 > 可选; resolve conflicts at the stricter level.
3. Output analyses / decisions using the AGENTS.md §4 思维链输出协议（问题 → 概念 → 前提 → 推理 → 反证 → 结论+置信度 → 行动+重审条件）.
4. Review tasks use the AGENTS.md §5 审查输出协议（[Blocking] / [Non-blocking] / [Info]，引用 M-x / S-x / W-x / F-x / B-x 编号）.
5. Before finishing an analysis, self-check the README §六 思维质量验收清单（11 items）.

## Key files

| Purpose | File |
| --- | --- |
| AI dispatch rules & output protocols | AGENTS.md |
| Ten meta laws M-1~M-10 + M-T / M-P / M-L details | meta/ |
| 12 sub-thinking skills S-1~S-12 | sub-skills/ |
| 5 workflows W-1~W-5 | workflows/ |
| Fallacies F-x / biases B-x / CoT templates R-x / glossary | reference/ |
| Numbered rule index (script-generated, do not edit) | INDEX.md |

Maintenance: `meta/` is human-review-only (AI may propose changes via the `体系建议：...` format); see GOVERNANCE.md for versioning, numbering, and change permissions.
