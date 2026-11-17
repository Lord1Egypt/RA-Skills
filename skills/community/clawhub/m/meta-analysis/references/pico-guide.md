# PICO / PECO Decomposition Guide（PICO/PECO 解构规范）

> Grounding: Cochrane Handbook for Systematic Reviews of Interventions v6.x,
> PRISMA-S (Rethlefsen ML et al., 2021) for search reporting.
> ⚠️ Claims without source → `⚠️ official verify`.

## Purpose

Operationalize a research question into **searchable** components. A
meta-analysis topic is only viable if every PICO element can be expressed as
a search term / MeSH / free-text block.

## Four elements

| Element | Question | Must be expressible as |
|---|---|---|
| **P** Population | 研究对象是谁？(disease, stage, prior lines, age…) | diagnosis + population filters |
| **I** Intervention / Exposure | 干预/暴露是什么？(drug, dose, route, combo…) | drug name(s) + delivery form |
| **C** Comparator | 对照组是什么？(placebo, SOC, active, none…) | comparator drug / "placebo" |
| **O** Outcome | 结局是什么？(ORR, PFS, OS, AE, QoL…) | outcome terms (only if needed to scope) |

**PECO** (exposure-based, for observational meta): replace I→E (exposure),
C→comparison cohort / no-exposure.

## Decomposition rules

1. **Concrete over class**: "PD-1 抑制剂" is NOT searchable as a pool → must
   list drugs (nivolumab, pembrolizumab, sintilimab, tislelizumab,
   toripalimab, camrelizumab…) + MeSH "Programmed Cell Death 1 Receptor".
2. **Complex interventions** (multicomponent, e.g. "exercise + diet +
   counselling"): decompose to each active component; each component gets its
   own search block; the combination may be a separate block with AND/OR logic.
3. **Dose / route / timing** matter when they define the question (e.g.
   "every-2-weeks vs every-3-weeks"): include dose in the I block.
4. **Outcome terms** usually go to screening (title/abstract) rather than the
   core search to avoid over-restricting sensitivity.
5. Every element must map to ≥1 search term — if an element cannot, the topic
   is not operationally viable → revise PICO (Gate 2 fail).

## Self-check list (Gate 2)

- [ ] P: every qualifier (stage/line/age) has a search term or documented reason to omit
- [ ] I: active agent(s) enumerated; class terms expanded to drug names
- [ ] C: comparator(s) named (placebo/SOC/active); if "any comparator", said explicitly
- [ ] O: primary outcome(s) listed; effect measure chosen (RR/OR/HR/MD/SMD)
- [ ] Search blocks drafted for each element (AND between elements, OR within)
- [ ] MeSH + free-text both planned (or rationale to skip MeSH)
- [ ] Language / time window / study design filters decided
- [ ] If observational → PECO form used, confounding / effect-measure-modifier noted

All checked → Stage 3.

## Output — PICO block (goes into report JSON `pico.search_terms`)

```json
"pico": {
  "P": "Non-small cell lung cancer, stage IV, 2nd-line",
  "I": "PD-1/PD-L1 inhibitors (nivolumab, pembrolizumab, atezolizumab, durvalumab, sintilimab, tislelizumab, toripalimab, camrelizumab)",
  "C": "Docetaxel monotherapy",
  "O": "Overall survival (HR), progression-free survival (HR), ORR (RR)",
  "search_terms": {
    "P": "carcinoma, non-small-cell lung[Mesh] AND (second-line OR previously treated)",
    "I": "nivolumab OR pembrolizumab OR atezolizumab OR durvalumab OR sintilimab OR tislelizumab OR toripalimab OR camrelizumab",
    "C": "docetaxel",
    "O": "survival OR response",
    "filters": "Meta-Analysis[pt] OR Randomized Controlled Trial[pt], 2021-2026"
  }
}
```

## Common failure modes

- Population so broad that heterogeneity is guaranteed (fix: narrow to a
  decision-relevant subset).
- Intervention = whole class with wildly different mechanisms (fix: separate
  questions per mechanism, or plan subgroup by drug).
- Comparator omitted ("vs placebo" implied but not stated — review bias).
- Outcome list empty → no effect measure possible (R5 triggers).
