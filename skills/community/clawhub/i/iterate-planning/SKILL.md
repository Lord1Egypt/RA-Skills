---
name: iterate-planning
description: |
  基于 Ralph Loops 三阶段工作流理念，适配 OpenClaw 架构。
  需求迭代工作流：需求讨论 → 计划拆解 → 迭代执行。
  触发条件：用户说"讨论需求"、"开始计划"、"迭代执行"、"需求访谈"
  
---

# 需求迭代工作流 (Iterate Planning)

基于 Ralph Loops 三阶段工作流，适配 OpenClaw 原生实现。

## 核心哲学

> Human roles shift from "telling the agent what to do" to "engineering conditions where good outcomes emerge naturally through iteration."

三个原则：
- **Context is scarce** — 保持每次迭代精简
- **Plans are disposable** — 漂移的计划重新生成比修复更划算
- **Backpressure beats direction** — 工程化环境让错误的输出自动被拒绝

## 三阶段工作流

```
┌─────────────────────────────────────────────────────────────────────┐
│ Phase 1: 需求访谈                                                      │
│ 结构化对话 → 识别JTBD → 拆分Topics → 产出 specs/*.md                    │
├─────────────────────────────────────────────────────────────────────┤
│ Phase 2: 计划                                                          │
│ Gap分析(specs vs code) → 产出 IMPLEMENTATION_PLAN.md                  │
├─────────────────────────────────────────────────────────────────────┤
│ Phase 3: 迭代执行                                                      │
│ 每次一个任务 → 全新上下文 → 验证 → 提交 → 下一任务                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: 需求访谈

**目标**：在动手写代码之前，真正理解要做什么。

**触发**：用户说"讨论需求"、"需求访谈"、"帮我理清需求"

**流程**：
1. 使用 `templates/requirements-interview.md` 模板进行结构化访谈
2. 识别 JTBD（Jobs to Be Done）— 用户真正要解决的Outcome，不是功能列表
3. 把 JTBD 拆分成 Topics of Concern（每个 topic 一个独立维度）
4. 用"一个句子，不带and"测试 — 能说出来的是一个topic，说不出来的是多个
5. 每个 Topic 写一份 `specs/topic-xxx.md`

**完成标志**：
- 每个 Topic 都有 `specs/*.md`
- 每个 spec 包含：需求描述、验收标准、边界情况

**交付物**：
```
project/
└── specs/
    ├── topic-a.md
    ├── topic-b.md
    └── ...
```

---

## Phase 2: 计划

**目标**：生成可执行的任务清单，不写代码。

**触发**：需求完备后，用户说"开始计划"、"可以拆任务了"

**流程**：
1. 读取 `specs/*.md` 所有需求
2. 如有现有代码，研究 codebase
3. 对比 specs vs code（Gap Analysis）
4. 生成 `IMPLEMENTATION_PLAN.md`（带优先级的任务列表）

**模板**：`templates/planning-prompt.md`

**完成标志**：
- `IMPLEMENTATION_PLAN.md` 存在
- 每个任务有优先级标注
- 任务列表完整覆盖所有 specs

**交付物**：
```
project/
├── specs/
├── IMPLEMENTATION_PLAN.md
└── ...
```

---

## Phase 3: 迭代执行

**目标**：每次做一个任务，全新上下文，保持 agent 在"聪明区域"。

**触发**：计划完备后，用户说"开始执行"、"迭代构建"

**核心洞察**：
- **一次一任务** — 保持上下文精简，agent 保持高效
- **全新上下文** — 每次迭代从头开始，之前的错误不累积
- **验证 + 提交** — 每个任务完成后必须验证才能提交

**流程**：
1. 读取 `IMPLEMENTATION_PLAN.md`
2. 选最高优先级任务
3. 研究 codebase（不要假设未实现）
4. 执行任务
5. 运行验证（backpressure）
6. 更新 plan（标记完成）
7. 提交 commit
8. 循环直到 plan 完成

**模板**：`templates/build-prompt.md`

**完成标志**：
- `IMPLEMENTATION_PLAN.md` 所有任务标记 done
- 每次迭代有对应 commit

---

## 触发词指南

| 用户说 | Agent 动作 |
|--------|-----------|
| "讨论需求"、"需求访谈" | 启动 Phase 1 需求访谈 |
| "开始计划"、"可以拆任务了" | 启动 Phase 2 计划生成 |
| "开始执行"、"迭代构建" | 启动 Phase 3 迭代执行 |
| "Ralph Loop"、"迭代" | 询问用户要哪个 phase |

---

## 文件结构

```
iterate-planning/
├── SKILL.md                    # 本文件
├── AGENTS.md                   # 操作员指南
└── templates/
    ├── requirements-interview.md  # 需求访谈模板
    ├── planning-prompt.md          # 计划生成提示词
    └── build-prompt.md            # 构建执行提示词
```

---

## 为什么有效

| 问题 | 解法 |
|------|------|
| 需求不清晰就动手 | Phase 1 强制结构化访谈 |
| 计划赶不上变化 | Plans are disposable — 重新生成比修复更划算 |
| 上下文膨胀导致幻觉 | 一次一任务，全新上下文 |
| 错误累积难以追溯 | 每次验证 + 提交，自然 checkpoint |
