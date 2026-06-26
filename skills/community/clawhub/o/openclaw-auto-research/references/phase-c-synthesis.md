# Phase C: Knowledge Synthesis (S7-S8)

## S7: SYNTHESIS — 研究综述

### 输入
- `stage-6/cards/*.md` — 知识卡片（最多读取 24 张）
- `stage-1/goal.md` — 研究目标（用于 topic 提取）

### 产出
- `stage-7/synthesis.md` — 文献综述（主题簇 + 研究空白）

### System Prompt

```
You are a synthesis specialist for literature reviews.
```

### User Prompt 模板

```
Produce merged synthesis output (topic clusters + research gaps).
Output markdown with sections: 
- Cluster Overview
- Cluster 1..N (each with: core sources, synthesis, key convergence points)
- Gap 1..N (each with: description, impact, evidence from literature)
- Prioritized Opportunities (table: Priority, Opportunity, Grounding, Estimated Impact)

Topic: {topic}
Cards context:
{cards_context}
```

### 执行步骤

1. 读取 `stage-6/cards/` 目录下所有 `.md` 文件（最多 24 个），拼接成 cards_context
2. 发送 LLM 请求（max_tokens=8192，内容会很长）
3. 写入 `stage-7/synthesis.md`
4. 推送中文摘要（重点：发现了多少个研究空白）

---

## S8: HYPOTHESIS_GEN — 假设生成（多视角辩论）

### 输入
- `stage-7/synthesis.md` — 研究综述

### 产出
- `stage-8/hypotheses.md` — 综合假设文档
- `stage-8/perspectives/` — 各视角的原始输出

### ⚠️ 特殊：多视角辩论机制

S8 不是一次 LLM 调用，而是**4 次**：
1. 创新派（innovator）生成大胆假设
2. 务实派（pragmatist）生成可行假设
3. 反对派（contrarian）挑战假设
4. 综合者（synthesizer）整合三方观点

### 第 1 轮：创新派（innovator）

**System:**
```
You are a bold, creative researcher who thinks outside the box. You pursue high-risk high-reward ideas, draw cross-domain analogies, and propose counter-intuitive hypotheses that challenge mainstream assumptions.
```

**User:**
```
Generate at least 2 novel, unconventional hypotheses from the synthesis below.
CRITICAL REQUIREMENTS for EVERY hypothesis:
1. NOVELTY: Must go beyond incremental combination of existing methods.
2. FEASIBILITY: Must be testable with limited compute (single GPU, hours not days).
3. FALSIFIABILITY: Must have clear failure conditions.
4. MEASURABLE: Specific quantitative predictions.

Synthesis:
{synthesis}
```

### 第 2 轮：务实派（pragmatist）

**System:**
```
You are a practical ML engineer focused on what actually works. You prioritize computational feasibility, engineering simplicity, reliable baselines, and incremental but solid improvements.
```

**User:**
```
Generate at least 2 feasible, well-grounded hypotheses from the synthesis below.
For each hypothesis provide:
- A concrete, testable claim with clear methodology
- Why this is achievable with limited compute
- Specific baselines to compare against
- Expected effect size

Synthesis:
{synthesis}
```

### 第 3 轮：反对派（contrarian）

**System:**
```
You are a rigorous devil's advocate who challenges assumptions. You find blind spots, hidden failure modes, and counter-evidence. Your value is in finding problems others ignore. Be provocative but always grounded in evidence.
```

**User:**
```
Critically examine the synthesis and generate at least 2 contrarian hypotheses.
For each hypothesis provide:
- A challenge to a widely-held assumption in this area
- Evidence or reasoning for why the assumption might be wrong
- How to test this contrarian view
- What would change if this view is correct

Synthesis:
{synthesis}
```

### 第 4 轮：综合（synthesize）

**System:**
```
You synthesize multiple expert perspectives into actionable research hypotheses.
```

**User:**
```
You have received three perspectives on potential research hypotheses.
Synthesize them into a final set of 2-4 hypotheses that:
1. Preserve the best ideas from each perspective
2. Address the contrarian's challenges
3. Remain feasible and testable
4. Include clear dependency structure and execution order

Perspectives:
{perspectives}
```

（其中 `{perspectives}` 是前三轮输出的拼接）

### 执行步骤

1. 读取 `stage-7/synthesis.md`
2. 依次发送 3 次 LLM 请求（innovator, pragmatist, contrarian），保存到 `perspectives/` 目录
3. 拼接三方输出，发送第 4 次综合请求
4. 最终响应写入 `stage-8/hypotheses.md`
5. 推送中文摘要（生成了多少假设，核心观点）
