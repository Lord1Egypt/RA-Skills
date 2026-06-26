---
name: gis-site-suitability-analysis
description: >
  Use this skill when a GIS analyst, urban planner, environmental consultant, or
  site selection professional needs to draft a multi-criteria site suitability
  analysis (MCSA) report documenting spatial data layers, weighting rationale,
  analysis methodology, and results interpretation. Covers criteria definition,
  weighted overlay or Boolean screening, data source documentation, and a defensible
  methodology narrative. Produces a DRAFT report for analyst and stakeholder review.
---

# GIS Site Suitability Analysis

Produces a structured, methodology-first DRAFT multi-criteria site suitability analysis report from the analyst's inputs — covering criteria, weights, spatial data sources, analysis workflow, results, and limitations in a format defensible for public planning, environmental review, and site selection decision-making.

## Flow

1. **Project intake** — Collect: project name, study area description (polygon boundary, jurisdiction, or coordinate envelope), coordinate reference system, map scale, project type (renewable energy siting / transit-oriented development / facility location / conservation priority / logistics hub / hazard zone mapping / other), analysis purpose, intended decision-maker or audience, and any prior or parallel analyses to align with.

2. **Suitability objective definition** — Ask: what does "suitable" mean for this project? Confirm the optimization goal (e.g., maximize solar exposure while minimizing environmental conflict; minimize travel time while maximizing workforce access). Produce a one-paragraph Suitability Objective Statement for inclusion in the report.

3. **Criteria definition** — For each suitability criterion, collect: criterion name, rationale (why it matters for this project type), data layer(s) used (name, source, resolution or scale, vintage date), criterion type (exclusion / scored), scoring logic (e.g., distance decay, binary reclassification, reclassified raster), and weight. Offer a standard starter criteria set by project type if the user wants a template. Organize all criteria into a criteria framework table.

4. **Exclusion screening** — Identify absolute exclusion layers (binary / Boolean) that remove parcels or cells from the analysis entirely before weighted scoring: protected areas, floodways, existing developed land, restricted ownership, utility easements, etc. Produce an Exclusion Layer Summary table.

5. **Weighted overlay methodology** — Document: scoring schema (1–5 or 0–100 scale), normalization method, weight assignment rationale (equal weights / AHP / stakeholder-consensus process), final composite score formula. Ask whether sensitivity analysis was performed; if so, collect results. If not, flag it as strongly recommended and offer to draft a sensitivity analysis plan.

6. **Data source documentation** — Produce a data catalog table: Layer Name | Source Organization | Date | Resolution | Format | Projection | Known Limitations. Highlight any layers with accuracy limitations, projection mismatches, or temporal gaps that could affect results.

7. **Results and interpretation** — Ask the user to describe or provide results: top-scoring zones or parcels, area by suitability tier (High / Moderate / Low / Excluded), spatial distribution patterns, key constraint areas, and any anomalies. Draft a results narrative paragraph and a suitability area summary table. Do not invent spatial results — if the analysis has not been run, produce a results section template with placeholders and flag it clearly.

8. **Limitations and uncertainty** — Document standard caveats: data resolution limits, projection distortion, temporal mismatch between layers, criteria omitted due to data availability, sensitivity of results to weight assumptions, and the requirement for field verification of high-suitability areas before any site commitment.

9. **DRAFT report assembly** — Produce the full report with: executive summary, project description, suitability objective statement, criteria framework table, exclusion layer summary, weighted overlay methodology, data catalog, results narrative and area summary table, limitations, and next-steps recommendations. End with an unsigned GIS analyst / project manager review block.

## Key Rules

- Never claim a suitability score is a regulatory determination, environmental clearance, or zoning approval — always label results as a DRAFT planning and decision-support aid.
- Never omit a data source — label any user-provided layer without a public citation as "Source: User-provided; independent verification recommended."
- If criteria weights do not sum correctly or appear inconsistent, flag immediately and ask the user to confirm before continuing.
- Ask one topic at a time when building the criteria table — do not request all criteria attributes in a single question.
- Flag explicitly if a critical layer (land ownership, protected areas, infrastructure buffers) is absent from the criteria set — recommend adding it or documenting the omission with rationale.
- Always include a sensitivity analysis recommendation in every report that uses subjective weight assignments.
- Do not produce results statistics (area calculations, parcel counts) without explicit confirmation from the user that the analysis has been run — use placeholder templates instead.

## Output Format

```
GIS SITE SUITABILITY ANALYSIS REPORT — DRAFT
Project: [Name] | Study Area: [Description] | Date: [Date]
Analyst: [Name / Role] | CRS: [Coordinate Reference System]
DRAFT — For analyst and stakeholder review.
Not a regulatory, permitting, or environmental clearance determination.

EXECUTIVE SUMMARY
[3–4 sentences: objective, top criteria, highest-suitability areas, key constraints]

1. PROJECT DESCRIPTION AND OBJECTIVE
[Study area, purpose, audience, Suitability Objective Statement]

2. CRITERIA FRAMEWORK
[Table: Criterion | Layer | Type | Scoring Logic | Weight | Rationale]

3. EXCLUSION LAYERS
[Table: Layer | Source | Rationale | Area Excluded (if known)]

4. WEIGHTED OVERLAY METHODOLOGY
[Scoring schema | Normalization method | Composite score formula]

5. DATA CATALOG
[Table: Layer | Source | Date | Resolution | Format | Known Limitations]

6. RESULTS
[Suitability area summary table + narrative paragraph]
[Or: PLACEHOLDER — analysis not yet run; populate after GIS processing]

7. LIMITATIONS AND UNCERTAINTY
[Bulleted list]

8. NEXT STEPS AND RECOMMENDATIONS
[Field validation plan | Stakeholder review process | Sensitivity analysis recommendation]

REVIEW BLOCK
This DRAFT suitability analysis is a planning and decision-support aid.
Results require field verification and professional review before use in
regulatory, investment, or permitting decisions.
GIS Analyst / PM: ________________ Date: ________
```

## Feedback

Surface the contribution link only if the user expresses an unmet need or dissatisfaction.
Direct them to: https://github.com/archlab-space/Open-Skill-Hub/issues
