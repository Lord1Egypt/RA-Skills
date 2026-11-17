---
name: long-horizon-planner
description: |
  长程自主规划引擎（超越性元能力）。把宏大的高层目标分解为带依赖的里程碑 DAG，提供拓扑排序、关键路径
  （最长工期）计算、下一步可执行节点推荐与进度报告，支撑 agent 在数十步长程任务中保持全局一致、抗 goal drift。
  当用户/agent 需要「制定多阶段计划」「排依赖与工期」「找关键路径」「长程任务不跑偏」时调用。
agent_created: true
visibility: "public"
---

# 长程自主规划引擎（long-horizon-planner）

让 agent 从「走一步看一步」升级为「先有全局蓝图、再逐步兑现」。核心：把高层目标拆成**带依赖的里程碑 DAG**，
用确定性的图算法（拓扑序、关键路径）做可复跑的进度推演。

## 能力依据（主流研究）
- **HiPlan**：分层规划，分离「全局里程碑 (Milestone Action Guide)」与「局部分步提示 (Step-Wise Hints)」。
- **Plan-and-Act / Plan-and-Execute**：PLANNER 管「做什么」、EXECUTOR 管「怎么做」，解耦以抗目标漂移。
- **LaMMA-P**：LLM 语义理解 + 经典规划器 (PDDL) 融合，把高层意图拆成带依赖子任务，成功率 +105%。
- 最佳实践：显式层次分解 / 模块化解耦上下文 / rubric(plan anchor)防级联错误 / 闭环动态重规划 / 关键路径与依赖 DAG。

## 标准工作流
```bash
# 1. 初始化一份长程计划（默认 5 阶段里程碑骨架）
python scripts/planner.py init --goal "交付 AIDC 供配电方案" --out plan.json --horizon 21
# 2. 增删里程碑、连依赖
python scripts/planner.py add plan.json --id collect --name "采集负荷数据" --dep discover --est 4
# 3. 看依赖图与拓扑序（检测环）
python scripts/planner.py graph plan.json
# 4. 关键路径（决定总工期的最短必经链）
python scripts/planner.py critical plan.json
# 5. 推荐下一步可执行里程碑（依赖已满足）
python scripts/planner.py next plan.json
# 6. 推进进度 + 出 Markdown 报告
python scripts/planner.py advance plan.json --id discover --done
python scripts/planner.py report plan.json --out plan.md
```

## 设计要点
- **确定性可复跑**：规划原语全部本地算法实现，无外部依赖，每次结果一致、可审计。
- **全局一致**：始终持有完整 DAG 视图，局部失败只改后续，不重头（Plan-and-Execute 思想）。
- **关键路径优先**：缩短关键路径上的里程碑最能提前交付，规划资源应优先投入。
- **闭环重规划**：环境变化时改 `deps`/`est` 或 `add` 新节点，`critical`/`next` 立即反映新最优解。

## 质量门禁
- [ ] 目标是否可拆分为可验收的里程碑（每个有名称 + 工期 + 依赖）
- [ ] 是否检测过依赖环（graph 无 ❌ 环提示）
- [ ] 关键路径是否识别清楚、资源是否优先压在关键路径上
- [ ] 下一步推荐是否真的依赖已满、可立即开工

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）
```bash
python scripts/learner.py record <本技能目录> --capability 长程规划
python scripts/learner.py record <本技能目录> --capability 长程规划 --fail --error 依赖成环 --note "新增节点未检查环"
python scripts/learner.py insight <本技能目录>
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
