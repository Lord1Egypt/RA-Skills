---
name: auto-research
description: |
  OpenClaw 原生的自动化研究 pipeline。从一个研究 topic 出发，经过 23 个 stage 产出完整论文。
  每个 Phase 由独立 sub-agent 执行（context 隔离），Phase 间通过文件系统传递产出。
  触发词：Research X、跑研究、文献调研、写论文、研究 pipeline、auto research。
  灵感来源：AutoResearchClaw，但完全用 OpenClaw 原生能力实现，不依赖外部 Python 包。
---

# Auto Research Pipeline

## 概览

23 个 stage，8 个 phase，从 topic 到论文全自动。

**核心架构**: 主 Agent 作为 orchestrator，每个 Phase spawn 一个 sub-agent 执行（context 隔离）。
- 主 Agent：驱动状态机、spawn sub-agent、处理 Gate 决策、推送飞书通知、与用户讨论
- Sub-agent：执行 Phase 内的 2-4 个 Stage，只看到该 Phase 的 prompt + 前序产出
- `scripts/pipeline_state.py` — 状态机（checkpoint、gate、rollback）
- `scripts/literature_search.py` — 双源文献搜索（arXiv + Semantic Scholar）
- `references/phase-*.md` — 每个 Phase 的 prompt 模板
- `references/domains.yaml` — 8 个研究领域定义（关键词、顶会、评审偏好）

## 产出目录

所有产出写入 `~/.openclaw/workspace/auto-research/artifacts/<run-id>/`

状态文件：
- `checkpoint.json` — 最后完成的 Stage（崩溃恢复用）
- `pipeline_state.json` — 完整运行状态
- `stage_history.jsonl` — 不可变事件日志

## 脚本路径

```
SKILL_DIR=~/.openclaw/workspace/skills/auto-research
SCRIPTS=$SKILL_DIR/scripts
```

## 执行流程（主 Agent / Orchestrator）

收到 "Research <topic>" 指令后，主 Agent 执行以下流程：

### Step 0: 初始化 + 历史经验加载

```bash
RUN_DIR=~/.openclaw/workspace/auto-research/artifacts/ar-$(date +%Y%m%d-%H%M%S)
python3 $SCRIPTS/pipeline_state.py init --run-dir $RUN_DIR
```

**Evolution Overlay（历史经验）**：
用 memory_search 搜索 "auto-research lessons" 或 "research pipeline"，查找之前运行的教训。
如果找到，将相关经验摘要作为额外上下文传给 sub-agent（附在 task 末尾）：
```
## 历史经验（来自之前的运行）
- ⚠️ arXiv API 在公司网络下经常 429，文献搜索优先用 Semantic Scholar
- ⚠️ 实验代码需要 numpy，先确认已安装
- ...
```

### Step 1: 逐 Phase 执行

**每个 Phase 完成后，必须将结果发给用户讨论，用户确认后才继续下一个 Phase。**

```
1. exec: python3 $SCRIPTS/pipeline_state.py status --run-dir $RUN_DIR
   → 获取当前 Phase 和 Stage

2. 构造 sub-agent task（见下方 "Sub-agent Task 模板"）
   → 如果有历史经验，附在 task 末尾

3. sessions_spawn({
     task: <构造的 task>,
     mode: "run",
     runTimeoutSeconds: <见 Phase 索引>,
     label: "research-phase-X"
   })

4. sessions_yield 等待 sub-agent 完成

5. 验证 sub-agent 产出:
   - 检查 stage-{N}/ 目录是否存在预期文件
   - 如果产出缺失 → pipeline_state.py fail

6. 逐个 Stage 更新状态机:
   exec: python3 $SCRIPTS/pipeline_state.py complete --run-dir $RUN_DIR --stage N

7. Phase A 完成后: 执行 Topic 质量自评（见下方）
   Phase F 完成后: 处理 S15 决策（见下方）

8. 将 Phase 结果摘要发给用户，等待用户确认后再继续

9. 用户确认 → 进入下一个 Phase
```

### Step 1.5: Phase A 完成后 — Topic 质量自评 + Domain 识别验证

Phase A sub-agent 完成后，主 Agent 执行以下检查（不 spawn sub-agent，主 Agent 自己做）：

**1. 验证 Domain 识别**：
读取 stage-1/goal.md 中的 "## Domain" section，确认领域识别是否合理。
如果领域明显不对，告诉用户并建议修正。

**2. Topic 质量自评**：
读取 stage-1/goal.md，以**顶会审稿人视角**评估选题质量：
- novelty (1-10): 研究角度是否新颖？
- specificity (1-10): 范围是否聚焦？
- feasibility (1-10): 在约束条件下是否可行？
- overall (1-10): 综合评分

评分规则：
- overall ≥ 7: 选题优秀，建议继续
- overall 5-6: 选题可以，但可以更好，给出改进建议
- overall < 5: 选题需要调整，给出具体的 refined topic 建议

**3. 将结果一起发给用户**：
```
✅ Phase A 完成

📊 选题自评: {overall}/10 (novelty={n}, specificity={s}, feasibility={f})
{如果 < 5: ⚠️ 选题质量不够，建议调整: {suggestion}}

🏷️ 领域: {domain_name} → 推荐投稿: {top_venues}

{Phase A 内容摘要}

确认继续吗？
```

### Step 2: 恢复中断的运行

```bash
python3 $SCRIPTS/pipeline_state.py status --run-dir $RUN_DIR
# 根据 checkpoint 确定当前 Phase，从该 Phase 开始重新执行
```

### Step 3: Pipeline 结束后 — 记录经验

整个 pipeline 完成后（无论成功/失败），主 Agent 将本次运行的关键教训写入 memory：
```
用 memory_search 查找现有的 research lessons，然后更新或创建 memory/research-lessons.md：
- 哪些 Stage 失败了？为什么？
- 哪些搜索源有效/无效？
- 实验代码遇到了什么环境问题？
- 论文质量评分是多少？评审的主要意见？
```

这些经验会在下次运行时通过 Step 0 加载。

## Sub-agent Task 模板

每个 Phase 的 sub-agent task 按以下模板构造。**主 Agent 负责读取 prompt 文件和前序产出，拼入 task。**

### Phase A: Research Scoping (S1-S2)

```
sessions_spawn({
  task: `你是一个研究规划专家。执行以下阶段：

## 环境
- 产出目录: {RUN_DIR}

## 领域识别（必须先做）
读取以下领域定义，将研究主题的关键词与各领域 keywords 匹配，选择命中最多的领域。
不要自己编造领域信息，必须从以下定义中查找。

{读取 references/domains.yaml 的完整内容，粘贴在此}

## S1: 选题初始化
研究主题: {topic}

{读取 references/phase-a-scoping.md 中 S1 的 prompt 内容}

**额外要求**: 在 goal.md 开头加一个 "## Domain" section，包含:
- detected_domain: 匹配到的领域 ID
- domain_name: 领域展示名
- top_venues: 推荐投稿会议
- review_preferences: 该领域的评审偏好（从 domains.yaml 复制）

将产出写入: {RUN_DIR}/stage-1/goal.md

## S2: 问题分解
读取 {RUN_DIR}/stage-1/goal.md，然后：
{读取 references/phase-a-scoping.md 中 S2 的 prompt 内容}

将产出写入: {RUN_DIR}/stage-2/problem_tree.md

{如果有历史经验，附在此处}

## 完成标志
两个文件都写入后，你的任务完成。`,
  mode: "run",
  runTimeoutSeconds: 300,
  label: "research-phase-a"
})
```

### Phase B: Literature Discovery (S3-S6)

```
sessions_spawn({
  task: `你是一个文献检索专家。执行以下四个阶段：

## 环境
- 产出目录: {RUN_DIR}
- 脚本目录: {SCRIPTS}

## 前序输入
{粘贴 stage-1/goal.md 的内容，包含 Domain section}

### S3: 搜索策略
{phase-b-literature.md 中 S3 的 prompt}
产出: {RUN_DIR}/stage-3/search_plan.yaml

### S4: 文献收集
使用脚本搜索:
exec: python3 {SCRIPTS}/literature_search.py --plan {RUN_DIR}/stage-3/search_plan.yaml --output {RUN_DIR}/stage-4/ --year-min 2023 --limit 30

如果脚本结果不够（< 15 篇），用 web_search 工具补充，追加到 candidates.jsonl。

### S5: 文献筛选
{phase-b-literature.md 中 S5 的 prompt}
产出: {RUN_DIR}/stage-5/shortlist.jsonl

### S6: 知识提取
{phase-b-literature.md 中 S6 的 prompt}
产出: {RUN_DIR}/stage-6/cards/*.md（每篇论文一张卡片）

{如果有历史经验，附在此处}`,
  mode: "run",
  runTimeoutSeconds: 600,
  label: "research-phase-b"
})
```

### Phase C-H: 模板结构同上

Phase C-H 的 task 模板结构与 B 类似：
1. 角色定义
2. 环境信息
3. 前序输入（从文件读取粘贴）
4. 各 Stage 的 prompt（从 references/phase-*.md 读取）
5. 历史经验（如果有）

**前序产出传递规则**：

| Phase | 需要读取并传入 task 的文件 |
|-------|------------------------|
| A | 无（只需 topic） + domains.yaml |
| B | stage-1/goal.md |
| C | stage-1/goal.md, stage-6/cards/*.md |
| D | stage-7/synthesis.md, stage-8/hypotheses.md, stage-1/goal.md (Domain section) |
| E | stage-10/experiment.py（路径即可，sub-agent 会 exec） |
| F | stage-12 实验结果 JSON, stage-8/hypotheses.md |
| G | stage-7/synthesis.md, stage-8/hypotheses.md, stage-14/analysis.md, stage-1/goal.md (Domain for venue) |
| H | stage-19/paper_revised.md（前 500 字摘要即可） |

## Gate 阶段处理

每个 Phase 完成后都要跟用户讨论确认，Gate 阶段的确认更正式：

| Gate | Phase | 处理方式 |
|------|-------|---------|
| S5 | B | 展示筛选结果摘要，询问用户是否认可文献覆盖度 |
| S9 | D | 展示实验设计摘要，询问用户是否认可方案可行性 |
| S20 | H | 读取 quality_report.json，score ≥ 6 建议通过，< 6 建议回退重写 |

## S15 决策处理

Phase F sub-agent 完成后，主 Agent：
1. 读取 `stage-15/decision.md` 第一行
2. 解析出 PROCEED / PIVOT / REFINE
3. 告诉用户决策结果和理由，让用户确认
4. 确认后调用 `pipeline_state.py decide`
5. 如果 PIVOT → 从 Phase C 重新 spawn（回到 S8）
6. 如果 REFINE → 从 Phase E 重新 spawn（回到 S13）
7. 最多 2 次 pivot/refine

## 飞书通知

每个 Phase 完成后，主 Agent 发送结果摘要并等待用户确认：
```
✅ Phase {X}: {名称} — 完成 (S{start}-S{end})

{300-500字中文摘要：该 Phase 做了什么、核心发现}

📂 产出: stage-{start}/ ~ stage-{end}/
⏭️ 下一步: Phase {Y}: {下一个名称}

确认继续吗？
```

## Phase 索引

| Phase | Stages | Prompt 文件 | Sub-agent 超时 |
|-------|--------|------------|--------------|
| A Scoping | S1-S2 | `references/phase-a-scoping.md` | 300s |
| B Literature | S3-S6 | `references/phase-b-literature.md` | 600s |
| C Synthesis | S7-S8 | `references/phase-c-synthesis.md` | 600s |
| D Design | S9-S11 | `references/phase-d-design.md` | 600s |
| E Execution | S12-S13 | `references/phase-e-execution.md` | 600s |
| F Analysis | S14-S15 | `references/phase-f-analysis.md` | 300s |
| G Writing | S16-S19 | `references/phase-g-writing.md` | 900s |
| H Finalize | S20-S23 | `references/phase-h-finalize.md` | 600s |
