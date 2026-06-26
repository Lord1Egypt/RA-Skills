---
name: multi-skill-eval
description: |
  集成化多方法技能评估系统。整合静态分析(skill-assessment)、Rubric质量打分(skill-evaluator)和自主基准测试(skill-eval)。用于全面评估、对比、审计或改进OpenClaw技能。覆盖文档完整性、代码质量、25项Rubric打分、多模型基准测试。

  触发词(中文): 评估技能、技能评分、技能审计、对比技能、批量评估、技能质量检查、静态分析、基准测试、触发词检测、幽灵工具检测
  触发词(English): evaluate skill, compare skills, audit skill, benchmark skill, static analysis, skill quality, skill assessment

  Use when you need to evaluate, audit, benchmark, or improve OpenClaw skills.
---

# Multi-Skill-Eval v1.0.0
## Integrated Multi-Method Skill Evaluation System

Combines three evaluation approaches into one unified system:
1. **Skill Assessment** — lightweight static analysis (fast, automated)
2. **Skill Evaluator** — 25-criterion rubric scoring (ISO 25010, OpenSSF, Shneiderman)
3. **Skill-Eval** — autonomous benchmark evaluation with skill card generation

---

## 🚀 快速开始 / Quick Start

```bash
# 完整评估（三种方法）
multi-skill-eval ~/.openclaw/skills/my-skill

# 快速静态分析
multi-skill-eval ~/.openclaw/skills/my-skill --method quick

# 完整评估 + 详细报告
multi-skill-eval ~/.openclaw/skills/my-skill --method full

# 对比两个技能
multi-skill-eval --compare skill-a skill-b

# 批量评估所有本地技能
multi-skill-eval --all

# 指定模型进行基准测试
multi-skill-eval ~/.openclaw/skills/my-skill --method benchmark --model minimax/MiniMax-M2
```

---

## Three Evaluation Methods

### 方法一：静态分析 (快速 — 约30秒)

轻量级自动化检查，覆盖4个维度：

```bash
python3 scripts/static-analyze.py ~/.openclaw/skills/my-skill
python3 scripts/static-analyze.py ~/.openclaw/skills/my-skill --json    # 机器可读格式
```

**检查项目：**
- 文档完整性（SKILL.md、描述质量、示例）
- 代码质量与安全信号（脚本语法、错误处理）
- 配置友好性（环境变量文档化、默认值清晰）
- 维护性信号（版本管理、近期更新）

**输出：** 0-100分数 + 按严重性分类的问题列表。

---

### 方法二：Rubric打分 (详细 — 约10分钟)

25项标准，覆盖8个类别。自动化检查 + 手动评审结合。

**运行自动化结构检查：**
```bash
python3 scripts/eval-skill.py ~/.openclaw/skills/my-skill --json --verbose
```


**然后使用** `references/rubric.md` **进行手动评分**

#### The 25 Criteria (8 Categories)

| # | Category | Framework | Criteria |
|---|----------|-----------|----------|
| 1 | Functional Suitability | ISO 25010 | Completeness, Correctness, Appropriateness |
| 2 | Reliability | ISO 25010 | Fault Tolerance, Error Reporting, Recoverability |
| 3 | Performance / Context | ISO 25010 + Agent | Token Cost, Execution Efficiency |
| 4 | Usability — AI Agent | Shneiderman, Gerhardt-Powals | Learnability, Consistency, Feedback, Error Prevention |
| 5 | Usability — Human | Tognazzini, Norman | Discoverability, Forgiveness |
| 6 | Security | ISO 25010 + OpenSSF | Credentials, Input Validation, Data Safety |
| 7 | Maintainability | ISO 25010 | Modularity, Modifiability, Testability |
| 8 | Agent-Specific | Novel | Trigger Precision, Progressive Disclosure, Composability, Idempotency, Escape Hatches |

**Scoring:** Each criterion 0–4. Total 100 max.

| Score | Verdict | Action |
|-------|---------|--------|
| 90–100 | Excellent | Publish confidently |
| 80–89 | Good | Publishable, note known issues |
| 70–79 | Acceptable | Fix P0s before publishing |
| 60–69 | Needs Work | Fix P0+P1 before publishing |
| <60 | Not Ready | Significant rework needed |

#### Rubric Score Sheet

Copy `assets/EVAL-TEMPLATE.md` to the skill directory as `EVAL.md`.

**P0 Issues (blocks publishing):**
- Missing SKILL.md or invalid frontmatter
- Hardcoded credentials or secrets
- Phantom tooling (referenced scripts not in package)
- No description or description < 50 chars

**P1 Issues (should fix):**
- No usage examples
- No error handling in scripts
- Missing dependency documentation
- Unclear trigger conditions

---

### 方法三：自主基准测试 (深度 — 约30分钟/技能)

Full multi-phase evaluation with multi-model support. **Requires AI agent execution.**

```bash
# Spawn benchmark via AI agent
multi-skill-eval /path/to/skill --method benchmark --model claude-sonnet-4
```

> ⚠️ **Note**: The benchmark method requires an AI agent to orchestrate subagent execution. The CLI coordinates the workflow but actual execution happens through AI agent sessions.

> 📋 **Planned**: Self-evolution improvement engine (Phase 7+) is planned but not yet implemented.

#### Phase 1: Pre-flight Analysis

1. Read `SKILL.md` — understand claims, dependencies, target use cases
2. Classify skill type:
   - **Capability uplift** — teaches the agent something it can't do well
   - **Encoded preference** — sequences steps according to specific process
3. Dependency check:
   - Required CLI tools, API keys, env vars
   - Mark `dependency-gated` if credentials missing (skip eval, not fault of skill)
   - Check for **phantom tooling** (referenced scripts not in package)
4. Marketing claims check: flag any metrics ("7.8x faster") without evidence
5. Read knowledge base: `knowledge/lessons.md`, `eval-patterns.md`, `failures.md`
6. Check prior evaluations: `knowledge/skill-profiles/<slug>.md`

#### Phase 2: Test Case Design

Design 2-3 test prompts across four categories:
- **Outcome** — Did the task complete correctly?
- **Process** — Did the agent follow the skill's intended steps?
- **Style** — Does output follow skill-claimed conventions?
- **Efficiency** — Reasonable time/token usage?

**Assertion design (two layers):**

*Layer 1: Deterministic checks* (fast, reproducible)
- File existence, word counts, keyword presence
- Format compliance (valid JSON, SQL, markdown)
- Programmatic verification (run tests, check syntax)

*Layer 2: Rubric-based quality assessment* (LLM-as-judge)
- Judge model (NOT execution model) grades output against specific rubric
- Structured scoring, not pass/fail

**Key assertion patterns:**
- Banned-word checks for style-constrained skills (highly discriminating)
- Methodology/structure assertions for technical domains (baseline already strong on correctness)
- Output-floor assertions: required sections must appear even in error/fallback paths
- Bilingual keyword variants for Chinese-language skills (索引/index, 前导通配符/leading wildcard)

#### Phase 3: Execution

For each test case, spawn two subagents:

**With-skill:**
```
[Model: <execution_model>]
Read the skill at <skill-path>/SKILL.md and follow its instructions.
Task: <prompt>
Save outputs to: <workspace>/iteration-<N>/<test-name>/with_skill/outputs/
```

**Without-skill (baseline):**
```
[Model: <execution_model>]
Complete this task using only built-in capabilities. Do NOT read SKILL.md.
Task: <prompt>
Save outputs to: <workspace>/iteration-<N>/<test-name>/without_skill/outputs/
```

**Multi-model mode:** Run same skill across multiple models to check cross-model consistency.

#### Phase 4: Grading

Programmatic grading for deterministic checks. LLM-based grading for qualitative:

```bash
python3 scripts/grade-assertions.py --workspace /path/to/results
```

Save to `grading.json`:
```json
{
  "expectations": [
    {"text": "assertion text", "passed": true, "evidence": "..."}
  ],
  "summary": {"passed": N, "failed": N, "total": N, "pass_rate": 0.X}
}
```

#### Phase 5: Benchmark Aggregation

```json
{
  "with_skill": {"pass_rate": 0.X, "avg_time": "Ns", "avg_tokens": N},
  "without_skill": {"pass_rate": 0.X, "avg_time": "Ns", "avg_tokens": N},
  "delta": {"pass_rate": "+0.XX", "time": "+Xx"},
  "model_used": "claude-sonnet-4",
  "verdict": "Recommended"
}
```

**Efficiency flags:** Flag skills where quality delta ≈ 0 but cost delta >2x ("high-overhead framework inflation").

#### Phase 6: Skill Card Generation

```bash
python3 scripts/generate_skill_card.py \
  --workspace /path/to/results \
  --skill-name "My Skill" \
  --skill-slug my-skill \
  --eval-model claude-sonnet-4 \
  --output skill-cards/my-skill-v1.md
```

**Skill Card Contents:**
- Metadata: name, source, eval date, model, engine version
- Overall score 0-10 (Quality 0-5 + Delta 0-3 + Efficiency 0-2)
- With-skill vs without-skill comparison table
- Per-test-case breakdown with assertions, timing, grading
- Strengths / Weaknesses
- Recommendation: Recommended / Conditional / Marginal / Not Recommended

#### Phase 7: Leaderboard Update

```bash
python3 scripts/generate_leaderboard.py --cards-dir skill-cards --output leaderboard/index.html
```

---

## Self-Evolution Improvement Engine

> ⚠️ **Planned — Not Yet Implemented**
>
> The self-evolution improvement engine is designed but not yet implemented. The knowledge base (`knowledge/improve/`) contains proven patterns and lessons that inform manual skill improvement, but automatic skill rewriting is not available.

### Planned Improvement Process (Phase 7-12)

1. **Read knowledge base:**
   - `knowledge/improve/lessons.md` — proven strategies
   - `knowledge/improve/patterns.md` — category-specific playbooks
   - `knowledge/improve/failures.md` — what NOT to try

2. **Diagnose root cause:**
   - Skill too vague? (Doesn't specify enough to change model behavior)
   - Skill redundant? (Teaches things model already knows)
   - Skill too heavy? (Adds overhead without proportional quality gain)
   - Missing structure? (No clear output format)
   - Phantom tooling? (References tools that don't exist)
   - Reference manual anti-pattern? (>200 lines of educational content)
   - Library-as-skill anti-pattern? (Contains code instead of instructions)

3. **Select improvement strategy** from patterns:
   - Reference Manual Slim-Down: Delete 70%+ redundant content, add MUST/ALWAYS/NEVER mandates
   - Library-to-Instructions: Convert code to behavioral instructions
   - Phantom Tooling Replacement: Replace missing tool references with inline instructions
   - Overhead Routing: Add quick-mode vs full-framework routing
   - Assertion-Aligned Rewrite: Rewrite to pass specific failed assertions

4. **Rewrite SKILL.md** with selected strategy:
   - Default: Remove > Add (delete 60-80% first, then add behavioral mandates)
   - Add specific, enforceable conventions
   - Remove redundant content model already handles
   - Save as `SKILL-improved.md`

5. **Update assertions** to match improved skill

6. **Re-evaluate** with improved version

### Planned Re-Eval (Phase 10-11)

Run same eval against `SKILL-improved.md`:
- Score improved by >= 1.5 points → Success
- Less than 50% of previously-failed assertions fixed → Document limitation, move on

### Planned Improvement Knowledge Update (Phase 12)

After each improvement batch:
- Update `knowledge/improve/lessons.md` with what worked
- Update `knowledge/improve/patterns.md` with reusable patterns
- Update `knowledge/improve/failures.md` with failed attempts
- Fold proven patterns back into this SKILL.md

---

## Scoring Summary

| Method | Speed | Coverage | Best For |
|--------|-------|---------|----------|
| Static Analysis | ~30s | 4 dimensions | Quick comparison, batch scan |
| Rubric Scoring | ~10min | 25 criteria | Pre-publish audit, detailed report |
| Benchmark Eval | ~30min | Full + self-evolution | Production evaluation, skill improvement |

| Overall Score | Verdict |
|--------------|---------|
| 7-10 | Recommended |
| 5-6.9 | Conditional |
| 3-4.9 | Marginal |
| 0-2.9 | Not Recommended |

---

## Anti-Patterns to Detect

- **Reference manual anti-pattern**: SKILL.md >200 lines of educational content (not behavioral instructions)
- **Library-as-skill anti-pattern**: SKILL.md contains Python/JS class definitions instead of instructions
- **Phantom tooling**: SKILL.md references scripts/binaries not in the package
- **Phantom tooling framework skills**: Evaluate template/output structure separately from real data execution
- **Unsubstantiated claims**: Skill claims specific metrics without evidence — do not use self-reported numbers
- **High-overhead framework inflation**: Quality delta ≈ 0 but cost delta >2x — penalize efficiency

---

## Deeper Security Scanning

For thorough security audits, complement with [SkillLens](https://www.npmjs.com/package/skilllens):
```bash
npx skilllens scan /path/to/skill
```
Checks: exfiltration, code execution, persistence, privilege bypass, prompt injection.

---

## Dependencies

- Python 3.6+ (for eval-skill.py, static-analyze.py, grade-assertions.py)
- PyYAML (`pip install pyyaml`) — frontmatter parsing
- Node.js (for SkillLens security scanning)