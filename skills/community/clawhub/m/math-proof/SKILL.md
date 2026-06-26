# 🧮 math-proof — 数学定理证明与审查

Automated mathematical proof generation with built-in A/B review loop. Given a theorem statement, spawns Agent A to produce a proof and Agent B to review it. If B rejects, A revises — loop continues until B accepts or a configurable retry limit is reached.

## When to Use

Activate when the user asks to prove a mathematical statement (theorem, proposition, lemma). Trigger keywords: "证明", "求证", "prove", "proof", "定理", "theorem", "推导", "demonstrate".

## How It Works

```
User: "prove that the medians of a triangle are concurrent"

┌─────────────────────────────────────────────────────────┐
│  1. Ask user for configurations (feedback mode, refs)  │
│  2. Agent A produces a proof (spawned as subagent)     │
│  3. Agent B reviews the proof (spawned as subagent)    │
│  4. If B rejects → send feedback to A → revise         │
│  5. If B accepts → present final proof to user         │
│  6. Loop up to configurable max retries (default: 50)  │
└─────────────────────────────────────────────────────────┘
```

## Pre-loop Configuration

Before spawning the first agent, ask the user for the following:

### 1. Feedback Mode

| Mode | Description |
|------|-------------|
| 🔍 **Hint-only** | Only pass *direction-level hints* to A (e.g., "Step 3 was rejected because it assumed what needs to be proved"). A must figure out the fix independently. |
| 📝 **With history** | Direction hint + A's own previous proof text. A can base revisions on what it wrote before instead of starting from scratch. |
| 📋 **Full disclosure** | Direction hint + A's previous proof + B's complete review (error locations, suggestions, fix directions). Most informative for A. |

Default: Hint-only. If user doesn't specify, use hint-only.

### 2. Reference Materials (optional)

Ask: *"Do you want A and B to reference any local files or folders? (e.g., textbook chapters, lecture notes, theorem references)"*

If yes, the user specifies a path (file or folder). Its contents will be included in every spawn prompt sent to both A and B as context/reference material.

## Constraints & Rules

### User-Supplied Constraints

The user may supply constraints that must be passed to **both** A and B:

- Proof method restrictions: "纯几何" / "综合法" / "不能用向量" / "不能用塞瓦定理" / "解析几何" / "代数法" / "数学归纳法"等
- Tool restrictions: "不能用坐标" / "不能用微积分" / "初等方法"等
- Format requirements: "用 LaTeX" / "用中文" / "step by step"等

These constraints must be included verbatim in every spawn prompt sent to both A and B.

### Built-In Rules (for this skill)

- **A (producer)**: Must produce a self-contained proof following all user-supplied constraints. Proof must be complete, step-by-step, with each step justified.
- **B (reviewer)**: Must check for logical gaps, hidden assumptions, circular reasoning, missing steps, and constraint violations. B's review must be specific: point to exact line/step numbers where issues exist.
- **Loop termination**: Loop ends when B marks the proof as "通过" / "passed" / "accepted", or when the retry limit is reached.

## Implementation

### Spawn A (first attempt)

```
{
  "mode": "run",
  "task": "请严格证明以下定理：\n\n[定理陈述]\n\n[参考材料（如有）]\n\n要求：\n[用户约束，逐条列出]\n\n用 LaTeX 格式输出完整证明。"
}
```

### Spawn B (review)

```
{
  "mode": "run",
  "task": "请严格审查以下证明。\n\n[证明全文]\n\n[参考材料（如有）]\n\n请逐行检查：\n1. 每一步的推理是否正确？\n2. 有没有逻辑漏洞或循环论证？\n3. 有没有违反用户要求的约束（[约束列表]）？\n4. 整体逻辑链是否完整？\n5. 评价：通过 / 需要修改（说明理由）"
}
```

### Spawn A (revision, n > 1)

**Hint-only mode** (默认):
```
{
  "mode": "run",
  "task": "请重新证明以下定理。之前的版本被驳回，需要修改。\n\n[定理陈述]\n\n[参考材料（如有）]\n\n你上一轮写的证明原文：\n[A上一轮的完整证明]\n\n提示：上一轮被驳回的原因是[方向性提示，不包含B的完整审查]。\n\n要求：\n[用户约束，逐条列出]\n\n用 LaTeX 格式输出完整证明。"
}
```

**With-history mode**:
```
{
  "mode": "run",
  "task": "请重新证明以下定理。之前的版本被驳回，需要修改。\n\n[定理陈述]\n\n[参考材料（如有）]\n\n你上一轮写的证明原文：\n[A上一轮的完整证明]\n\n提示：上一轮被驳回的原因是[方向性提示]。你可以参考自己之前写的证明进行修改。\n\n要求：\n[用户约束，逐条列出]\n\n用 LaTeX 格式输出完整证明。"
}
```

**Full disclosure mode**:
```
{
  "mode": "run",
  "task": "请重新证明以下定理。之前的版本被驳回，需要根据审查意见修改。\n\n[定理陈述]\n\n[参考材料（如有）]\n\n你上一轮写的证明原文：\n[A上一轮的完整证明]\n\n审查意见原文：\n[B的完整审查结果]\n\n要求：\n[用户约束，逐条列出]\n\n用 LaTeX 格式输出完整证明。"
}
```

## Output Format

### Success (B accepts)

```
🎉 证明通过！

[完整证明文本]
```

### Failure (retry limit reached)

```
😿 已达到最大重试次数（N次），证明未能通过审查。

最后一份证明的问题：[概述]
```

## Example Run

### Theorem
> 三角形的三条中线交于一点（重心定理）

### User Constraints
- 纯欧几里得几何方法
- 不能使用向量、坐标、解析几何
- 不能使用塞瓦定理、梅涅劳斯定理

### Pre-loop Config
- Feedback mode: Hint-only
- Reference: None

### Trace

| Round | A Action | B Action | Result |
|-------|----------|----------|--------|
| 1 | 向量法证明 | B审查 | ❌ 违反约束（用了向量） |
| 2 | 综合法，相似三角形 | B审查 | ❌ 第三步逻辑漏洞 |
| 3 | 修正第三步 | B审查 | ❌ 循环论证 |
| 4 | 平行四边形构造 | B审查 | ❌ 未定义符号 |
| 5 | 新思路尝试 | B审查 | ❌ 方向错误 |
| 6 | 平行四边形+比例 | B审查 | ❌ 共线未证明 |
| 7 | 相似+唯一性 | B审查 | ❌ 论证不完整 |
| 8 | 修正表述 | B审查 | ❌ 根本逻辑问题 |
| 9 | 倍长中线法 | B审查 | ✅ 通过 |

## Notes

- Keep the loop summary updated between rounds so the user can see progress
- After each round, report which round (N/10) and a quick status
- For long-running proofs, consider asking the user if they want to continue after ~5 rounds
- If B's rejection is about a trivial formatting issue, fix and re-submit without counting it as a full round