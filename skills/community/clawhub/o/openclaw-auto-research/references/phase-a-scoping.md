# Phase A: Research Scoping (S1-S2)

## S1: TOPIC_INIT — 选题初始化

### 输入
- 用户提供的研究 topic（自然语言）

### 产出
- `stage-1/goal.md` — 完整的研究目标文档

### System Prompt

```
You are a rigorous research planner who identifies NOVEL, TIMELY research angles. You follow recent trends from top venues in the relevant domain and propose research that advances the frontier rather than repeating known results.

NOVELTY PRINCIPLES:
- A good research angle addresses a GAP not yet covered by existing work.
- Avoid pure benchmark/comparison studies unless the methodology is novel.
- Prefer angles that combine existing techniques in new ways, apply methods to underexplored domains, or challenge common assumptions.
- The research must be FEASIBLE with limited compute (single GPU, hours not days).
- Check: would a reviewer say 'this is already well-known'? If so, find a sharper angle.
```

### User Prompt 模板

```
Create a SMART research goal in markdown.
Topic: {topic}
Domains: {domains}

Required sections:
- **Topic**: The broad area
- **Novel Angle**: What specific aspect has NOT been well-studied? Why is this timely NOW (2024-2026)? What recent development creates an opportunity? How does this differ from standard approaches?
- **Scope**: Focused enough for a single paper
- **SMART Goal**: Specific, Measurable, Achievable, Relevant, Time-bound
- **Constraints**: Compute budget, available tools, data access
- **Success Criteria**: What results would make this publishable?

IMPORTANT: The 'Novel Angle' section must convincingly argue why this specific research direction is NOT already covered by existing work.

TREND VALIDATION (MANDATORY):
- Identify 2-3 recent papers (2024-2026) that establish the relevance of this research direction.
- Name the specific benchmark/dataset that will be used for evaluation.
- If no standard benchmark exists, explain how results will be measured.
- State whether SOTA results exist on this benchmark and what they are.
- Add a 'Benchmark' subsection listing: name, source, metrics, current SOTA (if known).
```

### 执行步骤

1. 将用户 topic 和 domains 填入 User Prompt
2. 发送 LLM 请求（无需 json_mode）
3. 将响应写入 `stage-1/goal.md`
4. 推送中文摘要到飞书

### Topic 质量评估（可选）

完成 goal.md 后，可额外调用一次 LLM 评估 topic 质量：

```
System: You are a research topic evaluator.
User: Rate this research topic 1-10 for novelty, feasibility, and impact.
Topic: {topic}
Goal: {goal_md_content}

Output a JSON object: {"score": N, "feedback": "...", "refined_topic": "..."}
```

如果分数 < 5，在飞书通知中建议用户考虑精化方向。

---

## S2: PROBLEM_DECOMPOSE — 问题分解

### 输入
- `stage-1/goal.md` — S1 的产出

### 产出
- `stage-2/problem_tree.md` — 研究问题分解文档

### System Prompt

```
You are a senior research strategist.
```

### User Prompt 模板

```
Decompose this research problem into at least 4 prioritized sub-questions.
Topic: {topic}

Output markdown with these sections:
- **Source**: Where this decomposition derives from
- **Sub-questions**: Each with RQ number, main question, sub-components
- **Priority Ranking**: Table with Priority, Research Question, Rationale, Dependencies
- **Risks**: Technical risks, mitigation strategies
- **Critical Path**: The minimum set of RQs needed for a publishable result

Goal context:
{goal_text}
```

### 执行步骤

1. 读取 `stage-1/goal.md` 内容
2. 填入 User Prompt 的 `{goal_text}` 占位符
3. 发送 LLM 请求
4. 将响应写入 `stage-2/problem_tree.md`
5. 推送中文摘要到飞书
