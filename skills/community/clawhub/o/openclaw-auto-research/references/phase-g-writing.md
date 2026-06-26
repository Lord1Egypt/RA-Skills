# Phase G: Paper Writing (S16-S19)

## S16: PAPER_OUTLINE — 论文大纲

### 输入
- `stage-7/synthesis.md`
- `stage-8/hypotheses.md`
- `stage-14/analysis.md`

### 产出
- `stage-16/outline.md` — 论文大纲

### System Prompt

```
You are an academic writing planner for top-tier AI conferences.
```

### User Prompt 模板

```
Create a detailed paper outline in markdown.
Include per-section goals, word count targets, and evidence links.
The outline MUST include a catchy method name (2-5 chars) for the paper title.
Propose 3 candidate titles following the 'MethodName: Subtitle' format.

Required sections:
- Title + Abstract (150-250 words)
- Introduction (800-1000 words): motivation, gap, contribution
- Related Work (600-800 words): position vs prior art
- Method (1000-1500 words): formal description
- Experiments (800-1200 words): setup, baselines, metrics
- Results (600-800 words): tables, key findings
- Discussion (400-600 words): implications, broader impact
- Limitations (200-300 words)
- Conclusion (200-300 words)

Synthesis: {synthesis_text}
Hypotheses: {hypotheses_text}
Experiment analysis: {analysis_text}
```

### 执行步骤

1. 读取 synthesis.md, hypotheses.md, analysis.md
2. 发送 LLM 请求（max_tokens=8192）
3. 写入 `stage-16/outline.md`
4. 推送中文摘要

---

## S17: PAPER_DRAFT — 论文初稿

### 输入
- `stage-16/outline.md`
- `stage-14/experiment_summary.json` — 实验数据
- `stage-7/synthesis.md` — 文献背景

### 产出
- `stage-17/paper_draft.md` — 完整论文初稿（5000-8000 词）

### ⚠️ 反编造检查

**如果 stage-14 没有有效的实验 metrics，此 stage 应该拒绝生成论文。**
检查 `experiment_summary.json` 是否包含真实数据，如果没有则报错并建议回到 Phase E。

### System Prompt

```
You are a top-tier academic paper author writing for leading venues.

KEY PRINCIPLES:
1. NOVELTY: A good paper has 1-2 key ideas and keeps the rest simple.
2. NARRATIVE: Every section drives toward the core contribution.
3. EVIDENCE: Every claim has data support. Never fabricate results.
4. FLOW: Prose paragraphs, not bullet lists. Academic but readable.
5. CITATIONS: Reference real papers from the literature review.
```

### 执行方式：分 3 次 LLM 调用

单次生成 8000 词很容易截断。分 3 段写：

**调用 1** (max_tokens=16384)：Title + Abstract + Introduction + Related Work + Method
**调用 2** (max_tokens=16384)：Experiments + Results
**调用 3** (max_tokens=16384)：Discussion + Limitations + Broader Impact + Conclusion + References

每次调用都传入 outline 和前序段落作为上下文。

### 执行步骤

1. 检查实验数据是否存在（反编造）
2. 读取 outline.md, experiment_summary.json, synthesis.md
3. 分 3 次 LLM 调用生成论文
4. 拼接为完整 paper_draft.md
5. 推送中文摘要（论文标题、字数、核心方法名）

---

## S18: PEER_REVIEW — 同行评审

### 输入
- `stage-17/paper_draft.md`

### 产出
- `stage-18/reviews.md` — 模拟评审意见

### System Prompt

```
You are a balanced conference reviewer.
```

### User Prompt 模板

```
Simulate peer review from at least 3 reviewer perspectives.
Output markdown with:
- Reviewer A (methodology expert): strengths, weaknesses, actionable revisions
- Reviewer B (domain expert): strengths, weaknesses, actionable revisions  
- Reviewer C (statistics/rigor expert): strengths, weaknesses, actionable revisions

Check specifically:
1. TOPIC ALIGNMENT: Does the paper address what the title/abstract promise?
2. EVIDENCE QUALITY: Are claims supported by data? Any fabricated-looking results?
3. BASELINE FAIRNESS: Are baselines modern and competitive?
4. STATISTICAL RIGOR: Proper confidence intervals, effect sizes, multiple seeds?
5. WRITING QUALITY: Clear prose, no bullet lists in body, proper academic tone?
6. NOVELTY: Is the contribution genuinely new?
7. REPRODUCIBILITY: Could someone replicate from the paper alone?

For each reviewer, provide:
- Overall score (1-10, NeurIPS scale)
- Confidence (1-5)
- Summary recommendation (accept/weak-accept/borderline/weak-reject/reject)

Paper:
{paper_draft}
```

### 执行步骤

1. 读取 `stage-17/paper_draft.md`
2. 发送 LLM 请求（max_tokens=8192）
3. 写入 `stage-18/reviews.md`
4. 推送中文摘要（评审分数、主要问题）

---

## S19: PAPER_REVISION — 论文修订

### 输入
- `stage-17/paper_draft.md` — 初稿
- `stage-18/reviews.md` — 评审意见

### 产出
- `stage-19/paper_revised.md` — 修订后的论文

### System Prompt

```
You are a paper revision expert.

CRITICAL RULES:
- UPDATE the title if results do not support the original claim.
- Transform bullet-point lists into flowing prose paragraphs.
- Address EVERY weakness raised by reviewers.
- Preserve all experimental data and citations.
- The revised paper must be at least as long as the draft (no shrinking).
```

### User Prompt 模板

```
Revise the paper draft to address all review comments.
Return revised markdown only.

REVISION RULES:
- For each reviewer weakness, either fix it or explain in a rebuttal note why it's addressed.
- Strengthen weak sections, add missing citations, improve statistical reporting.
- Ensure narrative coherence from introduction through conclusion.

Original draft:
{paper_draft}

Reviews:
{reviews_text}
```

### ⚠️ 长度检查

修订后的论文不能比初稿短。如果短了，提示 LLM "The revision is shorter than the draft. Please expand sections that address reviewer comments."

### 执行步骤

1. 读取 paper_draft.md 和 reviews.md
2. 发送 LLM 请求（max_tokens=16384）
3. 检查修订稿长度 ≥ 初稿长度
4. 如果太短，要求 LLM 扩展（最多重试 1 次）
5. 写入 `stage-19/paper_revised.md`
6. 推送中文摘要（修订了多少问题、最终字数）
