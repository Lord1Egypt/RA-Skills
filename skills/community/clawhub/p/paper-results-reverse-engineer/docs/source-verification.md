# Source Verification & Self-Check — Full Specification

## G0: Source Verification (Mandatory)

Self-check must compare against **original paper source text** (not generated file).

**Universal high-risk fields:**
- Sample size (N, n, k)
- Study design (random assignment type, cluster vs individual)
- Randomization unit (person-level, class-level, school-level)
- Session/Day (exact wording from Methods)
- Core statistics (B, t, p, ES exact values)
- Figure axis labels and units
- Moderator manipulated vs measured
- Preregistration status

**Source Verification Template:**
```
- Claim: [generated claim text]
- Exact source phrase: [verbatim quote from original]
- Location: [Methods/Results paragraph]
- Interpretation: [correctly interpreted?]
- Confidence: high / medium / low
- Needs manual check: yes / no
```

**Rule:** Without a verbatim source quote, confidence cannot be "high." If evidence only exists in generated file (not original paper), cannot mark ✅ — flag for revision.

**Verification table:**

| High-risk field | Source to check | Common hallucination |
|----------------|-----------------|---------------------|
| Days/sessions | Methods Procedure / Figure 1 caption | Inventing "Day1/Day2" when paper says "then"/"after" |
| Sample N + exclusions | Methods Participants | Inferring N from df |
| Actual trial count / stimulus pool | Methods Materials/Procedure | Collapsing candidate pool into task count |
| Task type labels | Methods Procedure | Calling controlled lab task "observational" |
| Core statistics | Results section | Fabricating F when only χ² reported |
| Figure axis labels/units | Figure caption + image recognition | Rewriting "r" as "t-value" |
| Causal mechanism language | Results vs Discussion boundary | Writing Discussion interpretation as Results |
| Day/Session wording | Methods Procedure | (See G6 time-structure audit) |

## G1: File Completeness Self-Check

Re-read output file. Search for: `truncated`, `后略`, `省略`, `未完待续`, `TODO`, `待补充`. If found → log to `logs/selfcheck_failed_log.md`, flag in chat.

## G2: Module Completeness Checklist

| Check | Pass? | Evidence (must reference original paper, not generated text) |
|-------|-------|----------|
| Study Profile complete | ✅/❌ | ... |
| Module A complete with source column | ✅/❌ | ... |
| Module B covers all Results subsections | ✅/❌ | ... |
| Module C covers core Results sentence clusters | ✅/❌ | ... |
| Module D: core tables/figures explained | ✅/❌ | ... |
| Module E: all 7 items filled | ✅/❌ | ... |
| Module F: depth matches current mode | ✅/❌ | (quick: none; standard: condensed; close-reading: full) |
| Module F PPT respects three-layer separation | ✅/❌ | ... |
| Study Profile hypothesis field split (theory vs question) | ✅/❌ | ... |
| Task terminology matches scanned task (recognition ≠ recall) | ✅/❌ | ... |
| Hypothesis/Result/Interpretation three-layer separation correct | ✅/❌ | ... |
| Causal language matches study design | ✅/❌ | ... |
| No fabricated statistics | ✅/❌ | ... |
| Paper's original terminology used throughout | ✅/❌ | ... |
| Study design label accurate (non-intervention experiment ≠ observational) | ✅/❌ | ... |
| Stimulus pool vs actual task exposure separated | ✅/❌ | ... |

## G4: Task Type Confusion Check

| Pair | Check |
|------|-------|
| recognition vs recall | Correctly identified? |
| experiment vs survey | Design matches Methods? |
| cross-sectional vs longitudinal | Time dimension correct? |
| intervention vs observational | Manipulation status correct? |
| neural vs behavioral evidence | Data type correct? |
| correlation vs regression vs mediation | Analysis type correct? |
| statistical vs clinical significance | Reported where applicable? |
| meta-analysis vs simulation study | Correctly distinguished (I vs G)? |

## G5: Manual Review Priority Levels

All manual-review items must use three-tier grading:

| Level | Definition | Example |
|-------|-----------|---------|
| **Critical** | Directly affects core conclusion interpretation or statistical reliability | Text-table contradiction (B7), J-N direction conflict (B4), conditional indirect effect anomaly (B3) |
| **Important** | Affects effect size interpretation or model stability, but doesn't overturn core conclusion | Low α < .70 (B5), CFA fit RMSEA > .08, table layout unclear |
| **Minor** | Doesn't affect substantive conclusions, but correction improves precision | Image recognition unavailable, caption inference, display details to verify |

Format: table with #, problem description, triggered rule, severity (Critical/Important/Minor). Critical items must be separately listed in chat summary.

## G6: Time-Structure Audit

If output contains Day1/Day2/Session/两天/第一天/第二天 etc., verify against original Methods/Procedure/Figure 1 caption. If no evidence → replace with phase-based description. Also remove "同一天"/"same day" inferences — absence of day markers ≠ same-day completion.

## G7: Source Verification Audit

For each ✅ in G2, locate supporting sentence in original paper. If not found → change to ❌ and fix.

**Minimal check items (must verify against original):**
- Sample N + exclusions → Methods Participants
- Task trial counts → Methods Procedure
- Experiment phases/days → Methods Procedure + Figure 1 caption
- Study design label → Methods Procedure
- Core statistics → Results section
- Figure axis labels → Figure caption + image recognition
- Causal verbs in PPT → Discussion section

## G8: Three-Axis Classification Self-Check

| Check | Pass? |
|-------|-------|
| Axis 1 independent of Axis 2 (article type ≠ domain) | ✅/❌ |
| Adaptive Branch determined by Axis 1 | ✅/❌ |
| Simulation study NOT mislabeled as meta-analysis | ✅/❌ |
| fMRI meta-analysis NOT mislabeled as single fMRI experiment | ✅/❌ |
| Psychometric validation NOT mislabeled as survey/correlational | ✅/❌ |
| Intervention RCT NOT mislabeled as clinical just because clinical sample | ✅/❌ |
| Real data synthesis (G) vs simulated data comparison (I) distinguished | ✅/❌ |
| Single fMRI experiment (F) vs fMRI coordinate meta-analysis (G subbranch) distinguished | ✅/❌ |
| ALE convergence ≠ pooled ES (G10) | ✅/❌ |
| Functional decoding ≠ moderator analysis (G11) | ✅/❌ |
| Axis 3 matches paper's actual method | ✅/❌ |
| Module D chart types match Axis 3 | ✅/❌ |

**Common axis-confusion patterns:**
- Paper studies meta-analytic methods → Axis 1 = Methodological simulation, NOT Meta-analysis
- fMRI coordinate-based meta-analysis → Axis 1 = Meta-analysis, Axis 2 = fMRI, NOT Branch F
- Clinical sample education RCT → Axis 1 = Intervention/RCT, Axis 2 = Educational, NOT clinical
- Scale validation without factor analysis → Axis 1 = Psychometric validation, NOT survey/correlational
