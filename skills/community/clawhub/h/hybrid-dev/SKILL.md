---
name: hybrid-dev
description: "Hybrid development workflow: local model plans, Copilot codes, local model validates. Use when: starting a new project iteration, generating a Copilot task pack, running phase-a/b/c workflow, doing requirements analysis with local model, handing off to Copilot for coding, running test validation with local model. Triggers on: task pack, hybrid workflow, local model planning, Copilot handoff, phase-a, phase-b, phase-c, iteration, validation."
metadata: { "openclaw": { "emoji": "🔄" } }
---

# Hybrid Dev Workflow Skill

## 目标
将本地模型与线上 Copilot 组合为稳定的三阶段协作流程：
1. 本地模型做需求分析、功能规划、开发计划。
2. Copilot 按任务包进行编码实现。
3. 本地模型按验收标准执行测试验证与回归评估。

## 产物目录约定
- 阶段 A 产物: openclaw/output/phase-a
- 阶段 B 产物: openclaw/output/phase-b
- 阶段 C 产物: openclaw/output/phase-c

## 流程
1. 使用 prompts/customer-registry.md 中的 A1-A3 提示词生成阶段 A 产物。
2. 将阶段 A 产物粘贴到 B1 提示词，交给 Copilot 实现代码。
3. 收集代码变更摘要、测试输出、日志，喂给 C1 提示词执行测试评审。
4. 若 C1 结论为不通过，生成缺陷清单并回到 B1 修复。

## 关卡规则
- Gate 1: 没有量化验收标准，不允许进入编码。
- Gate 2: 没有覆盖矩阵，不允许给出测试通过结论。
- Gate 3: 未关闭 P0/P1 缺陷，不允许标记迭代完成。

## 最小可执行节奏
- 每轮迭代只做 1 到 3 个功能点。
- 每轮必须输出：需求变更、实现说明、测试结论。
