# PRISMA 2020 / AMSTAR-2 Compliance Pre-check（合规预检）

> Grounding: PRISMA 2020 — Page MJ et al., BMJ 2021;372:n71 (checklist of 27
> items); AMSTAR-2 — Shea BJ et al., BMJ 2017;358:j4008 (16-item critical
> appraisal tool, 7 critical domains). GRADE — Guyatt GH et al., J Clin
> Epidemiol 2011. ⚠️ Claims without source → `⚠️ official verify`.

## Purpose

Identify methodological risks **at topic-selection stage** — before time and
money are spent — so the final review is publishable/registerable.

## PRISMA 2020 — key items pre-check（选题期重点条目）

Full checklist has 27 items; at topic stage we pre-check the 11 that depend on
upfront design (status: ✅ ok / ⚠️ plan needed / ❌ gap).

| # | Item | Topic-stage question | Typical status at topic stage |
|---|---|---|---|
| 1 | Title | Title identifies it as a systematic review | ✅ decide at report |
| 2 | Abstract | Structured abstract plan | ✅ |
| 3 | Rationale | Existing evidence summarized (incl. dedup findings) | ⚠️ needs dedup layer |
| 4 | Objectives | PICO-objectives aligned | ✅ after Gate 2 |
| 5 | Eligibility | Inclusion/exclusion pre-specified | ⚠️ draft at topic stage |
| 6 | Information sources | Databases listed (PubMed/Embase/Cochrane/…non-English) | ⚠️ depends on scope |
| 7 | Search strategy | Full strategy reported (PRISMA-S) | ⚠️ draft search blocks |
| 8 | Selection process | Duplicate screening + AI/LLM-assisted screening declared | ⚠️ declare if used |
| 9 | Data collection | Extraction form + pilot | ❌ gap at topic stage → plan |
| 10 | Risk of bias | RoB 2 / ROBINS-I / QUADAS-2 / NOS chosen per design | ✅ choose with meta type |
| 11 | Effect measures | Effect measure per outcome (RR/OR/HR/MD/SMD) | ✅ after Gate 2 (R5 guard) |
| 16 | Equity (PROGRESS-Plus) | Consideration of equity-relevant dimensions | ⚠️ consider at topic stage |
| 19 | Synthesis methods | Heterogeneity threshold + subgroup plan pre-specified | ⚠️ pre-set I² trigger |

> Items 12–15, 17–18, 20–27 (results/risk of bias across studies, certainty,
> discussion, registration) are confirmed at write-up — not topic-stage gates.

## AMSTAR-2 — 7 critical domains（7 个关键弱点规避）

| Critical domain | Topic-stage action |
|---|---|
| 1. Protocol registered (PROSPERO) before data extraction | Register or at least commit to pre-registration in next actions |
| 2. Comprehensive search (≥2 databases + reference lists + grey) | Draft multi-DB plan (dedup layer already covers 3) |
| 3. Duplicate study selection & extraction | Pre-specify dual-review process (or AI-assisted with human audit) |
| 4. Excluded studies justified | Plan a PRISMA flow with reasons |
| 5. Risk of bias assessed & incorporated | Choose RoB tool now (RoB 2 / ROBINS-I / QUADAS-2 / NOS) |
| 6. Meta-analysis methods appropriate (heterogeneity, I²) | Pre-set heterogeneity strategy (I² >50% → subgroup/regression) |
| 7. Publication bias investigated | Pre-plan Egger/Begg/trim-fill (this skill's `analyze_publication_bias`) |

## Overall compliance risk

| Risk | Meaning | Topic-stage action |
|---|---|---|
| 🟢 Low | All 11 PRISMA items ✅/⚠️ with plan; 7 AMSTAR-2 domains addressable | Proceed to Stage 5 |
| 🟡 Medium | 1–2 ⚠️/❌ gaps with clear fixes | Fix in report; delay verdict if gate-blocking |
| 🔴 High | Dedup duplicate, PICO not searchable, or effect measure mismatch | **Stop** — rework topic (back to Stage 1/2) |

## Output fields (JSON `compliance`)

```json
"compliance": {
  "prisma": [
    {"item": "1", "status": "ok", "note": "title identifies SR"},
    {"item": "5", "status": "plan", "note": "draft eligibility at topic stage"},
    {"item": "9", "status": "gap", "note": "extraction form to be built"}
  ],
  "amstar2": [
    {"domain": "protocol", "status": "plan", "note": "PROSPERO before extraction"},
    {"domain": "publication_bias", "status": "ok", "note": "Egger/Begg/trim-fill via skill"}
  ],
  "overall_risk": "yellow",
  "note": "2 gaps with clear fixes; re-check at protocol stage"
}
```

## Related skill resources

- RoB tools: `references/rob2-plot.md`, `references/review_workflow.md` (PRISMA flow)
- Publication bias: SKILL.md Core Functions → `analyze_publication_bias`
- GRADE: SKILL.md Core Functions → Quality module
