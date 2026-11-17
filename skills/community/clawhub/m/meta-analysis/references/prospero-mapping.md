# PROSPERO Registration Field Mapping（PROSPERO 注册字段映射）

> Grounding: PROSPERO (NIHR) registration form fields (crd.york.ac.uk/prospero,
> standard registration page, 2026 revision). Map report sections → form
> fields so the 11-section topic report feeds directly into registration.
> ⚠️ Field wording may vary slightly by registry revision — verify against the
> live form before submitting.

## Purpose

If the verdict is recommend/proceed and the user intends to register, the
topic report must map 1:1 to the PROSPERO form, minimizing re-typing and
consistency errors.

## Field mapping table

| PROSPERO form field (section) | Source in topic report | Notes |
|---|---|---|
| Title | Report title | Must state "systematic review" / "meta-analysis" |
| Review question(s) | §2 PICO table (P + I + C + O) | Re-state as a single question sentence |
| Searches (sources + dates) | §6 search strategy | List DBs, dates, grey-lit sources |
| URL to search strategy | §6 (if archived) | Optional but recommended |
| Condition / population | §2 P (Population) | Map to MeSH/controlled vocab |
| Intervention(s) / exposure | §2 I (Intervention) | Enumerate agents; class → drug list |
| Comparator(s) / control | §2 C (Comparator) | Name explicitly (placebo/SOC/active) |
| Types of study to be included | §5 dedup + §7 compliance | RCT / observational; design filters |
| Context | §1 background | Clinical setting, line of therapy |
| Main outcome(s) | §8 outcomes + effect measures | List primary outcomes (pre-specify 1–2 primary) |
| Additional outcome(s) | §8 outcomes (secondary) | Optional |
| Data extraction | §9 sensitivity / §7 PRISMA #9 | Extraction form + pilot plan |
| Risk of bias (quality) assessment | §7 AMSTAR-2 #5 | RoB 2 / ROBINS-I / QUADAS-2 / NOS |
| Strategy for data synthesis | §9 subgroups + sensitivity | Heterogeneity threshold, model (FE/RE), NMA if applicable |
| Analysis of subgroups / subsets | §9 subgroups | Pre-specified ≥3 |
| Type and method of review | §3 meta type | Pairwise / NMA / IPD / DTA / single-group… |
| Anticipated or actual start date | §11 next actions | Registration date |
| Organisation (affiliation) | — | User provides |
| Named contact | — | User provides |
| Review team members | — | User provides |
| Funding sources | — | User provides |
| Conflicts of interest | — | User provides |
| Protocol / previous registration | §5 dedup | Prior protocol link if updating |

## Pre-submission checklist（注册前检查）

- [ ] Title contains "systematic review"
- [ ] Search strategy includes ≥2 databases + dates (AMSTAR-2 critical #2)
- [ ] Primary outcome(s) ≤2 and pre-specified
- [ ] Effect measure per outcome stated (R5 guard)
- [ ] Heterogeneity threshold + subgroup plan pre-set (#19/#9 guards)
- [ ] RoB tool chosen and named (#10 guard)
- [ ] Registration planned **before** data extraction (AMSTAR-2 critical #1)
- [ ] Dedup/increment statement attached (§5) — avoids "duplicate" rejection

## Output (JSON `prospero`)

```json
"prospero": {
  "ready": true,
  "missing": ["affiliation", "named contact", "team members", "funding"],
  "mapping_note": "All 11 report sections map to PROSPERO fields; 4 user-provided fields pending"
}
```
