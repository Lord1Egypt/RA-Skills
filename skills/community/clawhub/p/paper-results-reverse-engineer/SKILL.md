---
name: paper-results-reverse-engineer
version: 3.0.4
description: "心理学论文 Results 反向拆解技能 v3.0.4 稳定版。采用三轴分类（文章类型 × 领域 × 数据模态）、研究画像优先工作流、A–I 九分支自适应架构，覆盖实验、问卷、RCT、心理测量、元分析、神经影像坐标元分析、质性研究（主题分析、IPA、扎根理论、建构主义扎根理论）及方法学模拟等各类研究设计。默认输出为标准模式，可选 Module H Writer Transfer Packet 联动 academic-results-writer。"
metadata:
  emoji: "🔬"
  version: "3.0.4"
  internal_version: "psychology-results-reverse-analysis-v3.0.4-bridge"
  scope: "general psychology literature"
  output_mode: "file-first"
  analysis_mode: "study-profile-first"
---

# Paper Results Reverse Engineer (v3.0.4)

Deconstruct and learn from the Results section of psychology papers across all subfields. The Results section is a guided narrative, not a data dump — this skill reverse-engineers that narrative.

**Supported subfields:** Cognitive / Social / Personality / Developmental / Educational / Clinical / Psychometrics / Cognitive Neuroscience / fMRI / EEG / Meta-analysis / Qualitative / Mixed methods / Methodological / Simulation.

## When to Use

Activate when the user pastes a Results section, uploads a PDF, provides figure captions + paragraphs, or requests "拆这篇结果部分" / "这张图怎么讲" / writing-strategy extraction / PPT scripts / statistical reporting checks.

## Output Depth Modes

| Mode | Trigger | Output |
|------|---------|--------|
| **quick** | "快速看一下" / "大概拆一下" | Study Profile + B + D (core figures) + E + self-check. No Module C or F. |
| **standard** (default) | (no mode specified) / "正常生成" | Study Profile + A–G. Module C: paragraph/cluster level (2–4 clusters per ¶). Module F: PPT page suggestions + one-liners + evidence boundaries only. |
| **close-reading** | "逐句拆解" / "完整精读" / "做 PPT" / "汇报讲稿" | Study Profile + A–G at max depth. Module C: sentence-level. Module F: full verbatim scripts + Q&A + backup slides. Phased execution allowed for long papers. |

**Mode-adaptive chat prompt (mandatory):** After each output, add one line indicating the current mode and available alternatives. See `docs/execution-constraints.md` for the full template.

## Execution Constraints (Hard Limits)

1. **Self-Check:** Max 1 per file. **Auto-Patch:** Max 1 after failed check, then stop and report.
2. **No recursive self-invocation** — prompt user for new analysis rounds.
3. **PDF read limit:** 2 reads per round max.
4. **Chat output: file-first** — only path + 3–5 core findings + self-check + manual-review items.
5. **Context overflow:** stop, prompt user to split into phases.

Full details: `docs/execution-constraints.md`

## Supporting-File Loading Policy (Mandatory)

Before executing any branch-specific rule, module specification, or guardrail that references a `docs/` file, read the corresponding file. The condensed rules in this SKILL.md are summaries; the full validated rule set is in `docs/`.

**Docs reading table — read the file when the trigger condition is met:**

| Trigger | Read |
|---------|------|
| Branch B/C/E/F active | `docs/branch-a-b-c-d-e-f.md` |
| Branch G active | `docs/branch-g-meta-analysis.md` |
| Branch H active | `docs/branch-h-qualitative.md` |
| Branch I active | `docs/branch-i-simulation.md` |
| Module H triggered | `docs/module-h-spec.md` |
| G0–G8 self-check / source verification / B0 heading detection | `docs/source-verification.md` |
| Causal-language audit / PPT three-layer separation | `docs/causal-language-guardrails.md` |
| G3 anti-template contamination check | `docs/anti-template-contamination.md` |
| Long PDF / phased execution / Phase cleanup | `docs/execution-constraints.md` |

**Fail-open rule:** If the required supporting file cannot be accessed, do NOT claim the full detailed rule set was applied. Continue with the condensed SKILL.md rules and explicitly report: `supporting-file unavailable; condensed-rule mode used`.

## Input Types

| # | Input | Handle by |
|---|-------|-----------|
| 1 | Full Results section | Study Profile → Modules A–G |
| 2 | Single Results subsection | B–E; flag missing context |
| 3 | Figure caption + paragraph | D + C; brief Study Profile |
| 4 | Abstract + Methods + Results | Study Profile → Full A–G |
| 5 | PDF excerpt (pasted) | Treat as type 1–3 |
| 6 | PDF file upload | `pdftotext` → detect Results → A–G |
| 7 | Figure/table screenshot | Vision model → cross-ref caption/text → D |
| 8 | Open-ended request | Clarify; route to appropriate modules |

Prompt templates: `references/prompt-templates.md`

---

## Workflow: Study Profile First

### Phase 0.3: Three-Axis Classification (Mandatory — Before Study Profile)

Classify every paper on three independent axes before filling the Study Profile. Never use single-axis labels.

| Axis | Name | Values (non-exhaustive) |
|------|------|------------------------|
| **Axis 1** | Article Type | Experiment / Survey / Longitudinal / RCT / Psychometric validation / Meta-analysis / Methodological simulation / Qualitative / Mixed / Review |
| **Axis 2** | Substantive Domain | Cognitive / Social / Developmental / Educational / Clinical / Cognitive Neuroscience / fMRI / EEG / Psychometrics / Health / Sleep / Meta-science |
| **Axis 3** | Data/Method Modality | Behavioral accuracy/RT / Questionnaire scores / Clinical diagnosis / fMRI activation / fMRI RSA/MVPA / ALE coordinates / EEG/ERP / SEM/mediation / Meta-analytic ES / Monte Carlo simulation / Qualitative themes |

**Axis 1 determines Adaptive Branch (A–I).** Axis 2 and 3 are secondary tags guiding terminology, chart types, and interpretation boundaries.

**Critical distinction:** Never conflate Axis 1 with Axis 2. Studying meta-analytic methods ≠ doing a meta-analysis (→ Branch I, not G). fMRI experiment ≠ fMRI coordinate-based meta-analysis (→ Branch F, not G subbranch).

### Study Profile Template

```markdown
## Study Profile

### 三轴分类
| 轴 | 类别 | 值 | 来源 |
|----|------|----|------|
| Axis 1 | Article Type | ... | [原文Methods] |
| Axis 2 | Substantive Domain | ... | [原文推断] |
| Axis 3 | Data/Method Modality | ... | [原文Methods] |
| Primary Branch | Branch A–I | ... | [教学性说明] |

### 基本信息
| 维度 | 内容 | 来源 |
|------|------|------|
| 样本信息 | N, population, age, sex, inclusion/exclusion | [原文Methods] |
| 任务或测量工具 | Task/questionnaire/interview/intervention | [原文Methods] |
| 核心变量 | IV/DV or predictor/outcome or mediator/moderator | [原文Methods] |
| 主要统计方法 | t/ANOVA/regression/SEM/meta-analysis/thematic analysis etc. | [原文Methods] |
| Results 小节标题 | (list all Results subsection titles) | [原文直接报告] |
| 核心表格和图表 | (Table/Figure numbers + brief description) | [caption] |
| 理论/模型预期 | (Introduction 中的理论预测 — NOT study's own hypotheses) | [原文Introduction] |
| 本研究直接检验的问题 | (Author's explicit questions in Introduction/Results) | [原文直接报告] |
| ⚠️ 假设性质说明 | (If "Intriguingly"/"Surprisingly" appear, note possible non-a-priori) | [正文推断] |
| Results 直接发现 | (1-2 sentence summary) | [原文直接报告] |
| Discussion 中的解释 | (Author's interpretation in Discussion) | [原文Discussion] |
```

**Rules:** Every field with source tag. N from Methods, never from df. `[无法确定]` if unavailable. Split hypothesis fields: 理论预期 / 检验问题 / Discussion 解释 are distinct. Task terminology must match paper (recognition ≠ recall).

### Phase 0.5: Evidence Validation Rules (Mandatory)

#### Rule 1: Day/Session Strong Evidence Rule

Only write "Day1/Day2" / "两天实验" when the paper explicitly uses these markers. For procedural "then/after/subsequently" without day markers → use phase-based description. **Also never infer "同一天"** from absence of markers.

#### Rule 2: Stimulus Pool vs Actual Task Exposure

Separate "候选材料池" from "实际任务数量." If Methods says "12 videos created, participants viewed 10" → report "10 videos per house," not "12 videos."

#### Rule 3: Study Design Taxonomy

Use precise labels. Never write "observational" for controlled laboratory tasks. "Within-subject experiment" is valid. Only use "RCT" with random assignment. Only use "observational" with no stimulus/condition manipulation. Distinguish cluster vs individual randomization.

#### Rule 4: Closed-Loop Phase Precision Guardrail

For CL-TMR / closed-loop auditory stimulation papers, always separate into four timing components:
- **(a) Detection phase** — when the algorithm detects a target event (e.g., SO up-state)
- **(b) Stimulus onset delay** — fixed or variable delay between detection and stimulus delivery
- **(c) Stimulus duration** — actual length of the auditory stimulus
- **(d) Actual stimulation phase variability** — where does the sound *actually* fall relative to the ongoing oscillation?

Never infer "down-state stimulation" unless the paper explicitly reports it. Never infer "phase-locked stimulation" unless the paper reports measured phase precision metrics.

**Supplementary guardrail:** If Supplementary material contains phase analysis but was not read in quick/standard mode, mark `⚠️ Supplementary phase analysis not read; actual stimulation phase unverified` in G5 manual review. Never draw conclusions about stimulation phase from the main text alone.

#### Rule 5: Sham-Control Trial Type Distinction

Distinguish between:
- **Physiological sham/control trials** — within-participant control trials where target EEG events are detected but no stimulus is delivered (e.g., "sham" in CL-TMR)
- **Behavioral control conditions** — separate experimental conditions manipulating task parameters during wake
- **Active acoustic control** — a different sound delivered during sleep (e.g., white noise, reversed speech)

If sham = no sound (silent SO detection), do NOT label it as "active control" or "acoustic control." Label it as "physiological sham (no stimulus delivered)." Note the limitation: silent sham cannot control for non-specific arousal effects of sound presentation.

---

## Phase 1: Adaptive Branch Selection

Based on Axis 1 (Article Type):

| Branch | Article Type | Key Focus |
|--------|-------------|-----------|
| **A** | Experiment with random assignment | Manipulation check, main effect, interaction, simple effects, post-hoc, ES |
| **B** | Survey / Correlational | Descriptive, reliability, correlation, regression, mediation, moderation |
| **C** | Intervention / RCT | Baseline, CONSORT flow, primary outcome, secondary, AE, follow-up |
| **D** | Developmental / Educational | Age/grade differences, growth curve, multilevel, measurement invariance |
| **E** | Psychometric / Scale Development | Item analysis, EFA/CFA, reliability, validity (convergent/discriminant/criterion), invariance |
| **F** | Neuroimaging / fMRI / EEG | Task phase, neural measure, ROI/electrode, activation/RSA/ERP, multiple comparison correction |
| **G** | Meta-analysis / Systematic Review | Inclusion/exclusion, k, pooled ES, heterogeneity (Q/I²/τ²), moderator, bias, sensitivity |
| **H** | Qualitative | Coding, themes, subthemes, quotes, saturation, triangulation, reflexivity |
| **I** | Methodological / Simulation | Simulation factors, performance metrics (Type I error, power, RMSE, coverage), method comparison |

### Branch-Specific Key Rules

| Branch | Key focus | Full spec |
|--------|-----------|-----------|
| B (Survey) | Cross-sectional mediation guardrail, hypothesis direction, measurement quality, internal inconsistency (B1–B9) | `docs/branch-a-b-c-d-e-f.md` |
| C (RCT) | AE/safety, clinical significance 6-layer, active comparator, Module B 14-block (C1–C6, C1a–C1h) | `docs/branch-a-b-c-d-e-f.md` |
| D (Developmental) | Age/group comparisons, longitudinal wording, nesting, measurement invariance | `docs/branch-a-b-c-d-e-f.md` |
| E (Psychometric) | Evidence taxonomy, diagnostic wording, cutoff, classic scale rule, table orientation (Rules 1–9) | `docs/branch-a-b-c-d-e-f.md` |
| F (fMRI/EEG) | Task-phase, correction method, ROI source, brain-behavior wording, mechanism guardrail | `docs/branch-a-b-c-d-e-f.md` |
| G (Meta-analysis) | Moderator guardrail, PRISMA, publication bias, coordinate-based meta subbranch (G1–G17) | `docs/branch-g-meta-analysis.md` |
| H (Qualitative) | Theme detection, reflexivity grading, intercoder reliability, demographic audit, IPA/GT/CGT subtypes (H1–H23) | `docs/branch-h-qualitative.md` |
| I (Simulation) | N/A rule, heatmap precision, evidence boundary, anti-template 4-tier (I1–I6) | `docs/branch-i-simulation.md` |

---

## Phase 2: Modules A–G

All module content references the Study Profile and selected branch. Never carry over terms or statistics from a previous paper.

### Module A: Study Profile Extended

The Study Profile from Phase 0, extended with three-axis fields first, then traditional fields. Always use source tags.

### Module B: Results Structure Map

For each subsection/paragraph cluster: subsection title, question answered, data/analysis used, corresponding table/figure, main result (1–2 sentences), author's intended conclusion, annotation (original heading vs teaching supplement).

**B0: Results Heading Detection Rule (Universal):** Scan for ALL heading signals (bold, standalone phrases, Title Case, functional labels). Do not rely on Markdown `##/###`. Always separate "原文显式小节标题" from "Skill 教学性补充分块 [教学性补充]". Never write "原文无显式小节标题" without full-text scan. Full specification: `docs/source-verification.md`

### Module C: Results Paragraph/Sentence Annotation

Print label legend first. Then annotate per mode: quick → skip; standard → paragraph/cluster level (2–4 clusters per ¶, function label + one note); close-reading → sentence-level with individual annotations.

**14 Function Labels:** 1-Restate aim/Q | 2-Restate method | 3-Overview trend | 4-Invite to view figure/table | 5-Report specific result | 6-Report statistical evidence | 7-Evaluative emphasis | 8-Compare with prior work | 9-Compare with prediction/model | 10-Explain/interpret | 11-Note non-significant/inconsistent | 12-Acknowledge limitation | 13-Hint at implication | 14-Transition to Discussion

**Label Rules:** L1 — "presented in"/"see Fig." → Label 4 takes priority. L2 — missing-data/cannot-compute → Label 11+12. L3 — dual-purpose sentences may carry multiple labels. L4 — "Interestingly"/"Surprisingly" → add Label 7 + flag as potentially exploratory.

Detailed examples: `references/function-labels.md`

### Module D: Table/Figure Explanation

For core figures/tables: question answered, structure, author's guide sentence, key pattern, primary vs auxiliary, PPT narrative logic, 1-minute script (Chinese), easily misinterpreted points.

**Figure analysis modes:** Core hypothesis figures → full image mode (vision model). Supplementary → caption + body text mode. Flag: `⚠️ 未对此图进行图像分析` and use `[caption]` / `[正文推断]` tags only. **Figure fallback rule:** if image recognition fails → `⚠️ 图像识别失败`; describe only what caption/body text confirms; never fabricate visual details.

### Module E: Evidence Strength & Interpretation Boundary

Three layers separated: 原文直接结果 `[原文直接报告]` / 作者解释 `[原文Discussion]` / 教学性总结 `[教学性说明]`.

Seven items: 1) Core claim 2) Evidence type 3) Alternative explanations 4) Evidence chain strength 5) Causal language audit 6) Missing links 7) What this study does NOT prove.

See `docs/causal-language-guardrails.md` for the full causal language ladder and three-layer separation rules.

### Module F: PPT / Presentation Scripts

Output depth per mode. All modes enforce: three-layer separation (Result/Interpretation/Teaching), causal language check, branch-specific presentation angles. **PPT scripts must never present Discussion interpretation as Results fact.**

See `docs/causal-language-guardrails.md` for PPT causal language check rules.

### Module G: Self-Check & Anti-Template Contamination

**G0: Source verification** — compare generated claims against original paper (not generated file). Use the verification template with verbatim source quotes. **G1:** File completeness — search for `truncated`/`TODO`/`待补充`. **G2:** Module completeness checklist. **G3:** Anti-template contamination — Tier a (pollution, delete) / b (method background, allow) / c (N/A contrast, allow) / d (audit checklist only, allow). **G4:** Task type confusion check. **G5:** Manual review with Critical/Important/Minor grading. **G6:** Time-structure audit. **G7:** Source verification audit. **G8:** Three-axis classification self-check.

Full specification: `docs/source-verification.md` and `docs/anti-template-contamination.md`

---

## Source Attribution Conventions

| Tag | Meaning |
|-----|--------|
| `[原文直接报告]` | Directly from Results/Methods |
| `[原文Discussion]` | Author's interpretation from Discussion |
| `[原文Methods]` | Factual details from Methods |
| `[图片识别]` | Read from figure via vision model |
| `[正文推断]` | Inferred from body text |
| `[教学性说明]` | Agent's educational commentary |
| `[无法确定]` | Cannot determine from available sources |

**Author-disclosed vs skill-inferred rule:** Never tag a limitation as `[原文Discussion]` unless authors explicitly state it. Full rules: `docs/source-verification.md`.

---

## Statistical Language Rules

- **Derived Clinical Metric Rule:** NNT/NNH/ARR/RR/OR/d calculated by skill → `[Calculated by skill / 教学性计算]`.
- **Standardized Effect Size Precision Rule:** When no Cohen's d/OR/RR reported → "No standardized between-group effect size was reported" (NOT "No effect size reported"). List what clinical effect information WAS reported.
- Never fabricate statistics. Never rewrite one statistic as another (r ≠ t ≠ F). For model fit, report multiple indices, not just χ².
- Full spec: `docs/causal-language-guardrails.md`

---

## Causal Language Ladder (Summary)

| Design | Allowed | Prohibited |
|--------|---------|-----------|
| Cross-sectional / Correlational / Survey | 相关、关联、预测 | 导致、影响、证明机制 |
| Experimental (random assignment) | 操纵X导致Y差异 | (still note boundary conditions) |
| Longitudinal | X预测后续Y | X导致Y变化 (without experiment) |
| RCT | 干预效果显著 | (note attrition, baseline, blinding) |
| Meta-analysis | 总体证据显示、pooled effect 提示 | 单一实验因果证明、证明方案最优 |
| Qualitative | 主题显示、参与者叙述反映 | 统计因果 |
| Simulation | 在这些模拟条件下 | 证明某方法最好、证明某效应不存在 |

**Universal prohibition** (all non-manipulation studies): "证明" / "直接导致" / "确定是因为". Full specification: `docs/causal-language-guardrails.md`

#### Mechanism-Wording Guardrail for EEG/ERP/ERSP Studies

When describing brain-behavior relationships in EEG/ERP/ERSP/MEG/fMRI studies:
- **Prohibited:** "mediate/mediates/mediation" — unless the paper explicitly reports a formal statistical mediation model (e.g., bootstrap indirect effect, Sobel test, SEM path model)
- **Use instead:** "correlate of," "marker of," "associated with," "may be related to," "predictor of" (for within-subject time-frequency analyses), "electrophysiological signature of"
- **When a formal mediation IS reported:** still audit whether temporal precedence can be established (EEG data within same sleep epoch may not satisfy mediation assumptions)
- **Applies to:** Module B (results structure), Module C (paragraph commentary), Module D (figure narration), Module E (evidence strength), Module F (PPT scripts), Study Profile (理论预期 field)

---

## Module H: Writer Transfer Packet (Optional)

Compressed transfer packet for `academic-results-writer` Target-paper Results Style Adaptation Mode. Triggered by user request for "写作迁移包" / "给 academic-results-writer 使用".

Structure: H1-Source Identity, H2-Design Transfer Summary (with compatibility rating), H3-Results Organization Template (Transfer/Partial/Do not transfer), H4-Paragraph Writing Patterns (abstracted), H5-Figure/Table Narrative Patterns, H6-Results–Discussion Boundary, H7-Risk Flags, H8-Recommended Writer Mode.

**Constraints:** 1–2 pages max. No target paper original sentences — abstract function labels only. No target paper statistics for writer to apply. All target paper risks in H7. Partial extraction → H1 must mark `coverage: partial`. Design-incompatible → H8 must recommend fallback.

Full specification: `docs/module-h-spec.md`

---

## File Output Template

→ Module A–H headers listed in Phase 2 above. **Metadata Date Safety Rule:** never fabricate generation date; use `[无法确定]` if not reliably confirmable via `date`/`session_status`.

---

## Do-Not Rules (Core)

See Failure Modes table below for full list. Most critical:

- ❌ Don't invent data / fabricate statistics / pull N from df / fabricate generation date.
- ❌ Don't write Discussion as Results (three-layer separation).
- ❌ Don't write correlation as causation; don't use "mediate" for EEG/ERP without formal mediation model.
- ❌ Don't carry over previous paper terms (G3 anti-template contamination).
- ❌ Don't mislabel: simulation ≠ meta-analysis (I vs G); lab task ≠ observational; sham ≠ active control.
- ❌ Don't infer stimulation phase / day-session / metadata without explicit paper evidence.
- ❌ Don't skip Study Profile, Module G, or label legend in Module C.
- ❌ Don't print full analysis in chat (file-first). Self-check against original paper, not generated output.

---

## Failure Modes (Summary)

| Failure | Prevention |
|---------|------------|
| Fabricated statistics | Enforce `[无法确定]` |
| N from df | Pull from Methods |
| Template pollution | G3 search |
| Discussion → Results | Three-layer separation |
| Correlation → causation | Causal ladder |
| "Mediate" without mediation model | Mechanism-wording guardrail |
| Phase inference without Supplementary | Closed-loop phase precision guardrail |
| Sham = "active control" | Sham-control distinction rule |
| Inferred limitation → [原文Discussion] | Author-disclosed vs skill-inferred rule |
| Fabricated generation date | Metadata date safety rule |
| Wrong branch | Study Profile → Axis 1 |
| Day/Session invented | Rule 1: require explicit markers |
| Stimulus pool = task count | Rule 2: separate pool vs actual |
| Lab task = observational | Rule 3: precise design taxonomy |
| Simulation → meta-analysis | I vs G distinction |
| ALE → pooled ES | G10 |
| Phase titles in merged file | Phase 5 merge back |
| Phase files not cleaned | Cleanup verification |

---

## Output Directory & Naming

```
~/Desktop/OpenClaw_Paper_Analysis/
├── outputs_md/reverse_engineer/{FirstAuthor}_{Year}_Results_Reverse_Analysis.md
├── outputs_md/results_writer/
├── logs/
├── figures_notes/
└── templates/
```

Phase temp files: `temp/{FirstAuthor}_{Year}/`. Final output: only one H1 title, no Phase N titles.

---

## Long PDF: Phased Execution

When PDF > ~20 pages or context is tight:

| Phase | Content | Output |
|-------|---------|--------|
| Phase 1 | Study Profile | Study Profile table |
| Phase 2 | Module A–B | A + B |
| Phase 3 | Module C–D | C + D |
| Phase 4 | Module E–G | E + F + G |
| Phase 5 | Merge + final self-check | Complete Markdown |

Phases write to `temp/`, merged to final output. Clean temp files on success unless `debug_mode: true`.

Full details: `docs/execution-constraints.md`

---

## Patch Mode

When user says "小修改" / "优化一下": modify only pointed-out issues. Append `Revision log` table at file end. Keep original structure.

---

> **Public version:** 3.0.4
> **Internal version:** psychology-results-reverse-analysis-v3.0.4-bridge
> **Scope:** General psychology literature (all subfields)
> **Analysis mode:** Study Profile first, three-axis classification (Article Type × Domain × Data Modality), design-adaptive branching (A–I), source-verified evidence
> **Output mode:** File-first (Markdown to desktop folder; chat = summary only)
> **Key features:** Cross-type validated across all 9 branches (A–I). Default standard mode. Retains quick/standard/close-reading modes. Optional Module H Writer Transfer Packet for academic-results-writer integration.
> **Documentation:** Branch-specific rules in `docs/`, examples in `examples/`, changelog in `CHANGELOG.md`
