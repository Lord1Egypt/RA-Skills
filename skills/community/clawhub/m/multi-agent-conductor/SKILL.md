---
name: multi-agent-conductor
display_name: 多智能体编排（Multi-Agent Conductor）
display_name_en: "Multi-Agent Conductor"
description: "当用户说『这个任务好大要拆给多个AI』『多智能体怎么分工』『agent之间怎么不串权限』『编排几个agent协作』，或要把一个大任务拆成多个 agent 并行/串行协作时使用。把任务分解为子任务→分配角色→划清每个 agent 的边界与禁止项（有门禁），输出编排方案+边界清单。可运行脚本（conductor_plan 规划器）。理论根基：LGD 三律之有门禁（任务边界+权限隔离）。触发词：多智能体、multi-agent、agent编排、任务分解、协作agent、agent权限、并行agent、orchestration。"
version: 1.1.1
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Task
category: AI工程方法
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
read_when:
  - 一个大任务要拆给多个 agent 协作
  - 多 agent 出现权限串台/互相改对方产物
  - 要设计 agent 团队的分工与边界
  - 担心某个 agent 越权访问不该碰的资源
tags: [多智能体, multi-agent, 编排, 任务分解, 协作, 有门禁]
slug: multi-agent-conductor
title: 多智能体编排（Multi-Agent Conductor）
copyright: SynomosAI
description_zh: "当用户说『这个任务好大要拆给多个AI』『多智能体怎么分工』『agent之间怎么不串权限』『编排几个agent协作』，或要把一个大任务拆成多个 agent 并行/串行协作时使用。把任务分解为子任务→分配角色→划清每个 agent 的边界与禁止项（有门禁），输出编排方案+边界清单。可运行脚本（conductor_plan 规划器）。理论根基：LGD 三律之有门禁（任务边界+权限隔离）。触发词：多智能体、multi-agent、agent编排、任务分解、协作agent、agent权限、并行agent、orchestration。"
description_en: "Decompose large tasks into multi-agent orchestration: subtask split, role assignment, per-agent permission boundaries, and parallel or serial coordination."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/conductor_plan.py
  runtime: python3
  call_pattern: args
input_schema:
  task:
    type: string
    description: "task"
    required: true
  agents:
    type: int
    description: "agents"
    required: false
  json:
    type: bool
    description: "json"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - multi-agent
  - orchestration
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.1.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
- When the user says a task is too large for a single agent and must be split among multiple AIs ("this task is too big, split it across several AIs").
- When permission isolation and responsibility boundaries between multiple agents matter, to prevent overstepping or collusion ("how do agents not leak permissions into each other").
- When you need to define the orchestration mode (parallel / serial) and the subtask allocation, in a way that complies with the LGD gated principle.

### Usage
- **Tool**: `conductor_plan` (backed by `conductor_plan.py`).
- **Invocation**: `python conductor_plan.py --mode orchestration --input task_description`.
- **Parameters**:
  - `--mode`: `parallel` or `serial`.
  - `--input`: task-description text or structured JSON containing the core goal and constraints.
  - `--permission`: (optional) a prohibited-items list to strengthen the gate rules.

### Workflow
1. **Trigger detection**: spot keywords such as "multi-agent" or "task decomposition" and decide whether to intervene.
2. **Requirement analysis**: extract the core task and assess a single agent's capability boundary and potential risks.
3. **Script execution**: run `conductor_plan.py` to decompose the logic and produce the subtask list and role assignment.
4. **Boundary drawing**: per the LGD gated principle, define each agent's permission scope and prohibited items.
5. **Plan generation**: output the final report containing the orchestration flow and the gate checklist.
6. **Feedback**: return the result to the user and ask whether the execution strategy needs adjustment.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once produced)
- Version: 1.1.1
- Safety: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
- 用户提出任务庞大、单一 Agent 无法完成，需拆分给多个 AI 协同时（如“这个任务好大要拆给多个 AI"）。
- 涉及多智能体间的权限隔离、职责边界划分，防止越权协作或串通风险时（如"agent 之间怎么不串权限”）。
- 需要明确 Agent 的编排模式（并行/串行）及子任务分配方案，且需符合 LGD 三律之有门禁原则时。

### 用法
- **工具**: `conductor_plan` (基于文件 `conductor_plan.py`)。
- **调用命令**: `python conductor_plan.py --mode orchestration --input task_description`.
- **参数说明**:
  - `--mode`: 可选值，指定 `parallel`（并行）或 `serial`（串行）。
  - `--input`: 任务描述文本或结构化 JSON，需包含核心目标与约束。
  - `--permission`: （可选）定义禁止事项清单，用于强化门禁规则。

### 流程
1. **触发检测**: 识别用户输入中的“多智能体”、“任务分解”等关键词，判断是否需要介入。
2. **分析需求**: 提取核心大任务，评估单一 Agent 的能力边界与潜在风险。
3. **执行脚本**: 启动 `conductor_plan.py` 进行逻辑拆解，生成子任务列表及角色分配。
4. **划定边界**: 依据 LGD 三律之有门禁原则，明确每个 Agent 的权限范围与禁止项。
5. **生成方案**: 输出包含编排流程与门禁清单的最终报告。
6. **反馈确认**: 将结果返回给用户并询问是否需要调整执行策略。

### 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
