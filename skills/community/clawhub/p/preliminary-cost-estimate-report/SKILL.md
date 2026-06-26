---
name: preliminary-cost-estimate-report
description: >
  Use this skill when a quantity surveyor, cost manager, owner's representative,
  or project estimator needs to produce a preliminary (Class D / Schematic Design
  level) construction cost estimate for a new building, renovation, or civil works
  project. Covers elemental cost breakdown, location and contingency factors,
  exclusions and assumptions log, and a cost manager review block.
---

# Preliminary Cost Estimate Report

Converts project brief information into a DRAFT Class D (Schematic Design / Order-of-Magnitude) construction cost estimate report with an elemental cost breakdown, location and market-condition adjustments, tiered contingencies, and a clearly documented assumptions and exclusions list. Produces a report for the cost manager or QS to verify before presenting to the owner or design team.

## Flow

### Phase 1 — Project Intake

Ask one question at a time. Wait for each answer before proceeding.

1. **Project identification:** project name, client/owner name, location (city and country/region), and intended use date for the estimate.
2. **Project type:** select the primary category:
   - New construction vs. renovation/addition (state percentage of existing building affected if renovation)
   - Building type: office, retail, residential multi-family, residential single-family, industrial/warehouse, healthcare, education, hospitality, mixed-use, civil/infrastructure, other (specify)
3. **Gross floor area:** total GFA in m² or ft² (specify unit). For multi-building projects, list each building separately.
4. **Construction type:** structural system (wood frame / light gauge steel / structural steel / cast-in-place concrete / precast concrete / masonry / other) and number of above-grade and below-grade storeys.
5. **Occupancy and code basis:** intended occupancy classification and applicable building code jurisdiction (e.g., IBC 2024, NBCC 2020, AS 1170, Eurocode).
6. **Scope inclusions:** which of the following are in scope? (Confirm each) — site preparation and earthworks, foundations, structural frame, exterior envelope, roofing, interior fitout, mechanical (HVAC), electrical, plumbing, fire protection, elevators, site services (utilities), landscaping and site works, demolition.
7. **Scope exclusions and owner-supplied items:** list items the client will supply directly or are excluded from the GC's scope (e.g., FF&E, owner-procured equipment, telecom, security, art).
8. **Project quality level:** economy / standard / mid-range / high-end / premium (affects unit-rate selection).
9. **Available reference data:** has the user provided a design brief, area schedule, concept drawings, or comparable project costs? If yes, ask the user to share them now.

Confirm the scope summary with the user before proceeding.

### Phase 2 — Location and Market Adjustment

Apply location cost indices to base rates:

1. Identify the cost index region for the project location (use Rider Levett Bucknall, Turner & Townsend, or RSMeans regional indices as the reference framework — state the reference used).
2. Apply a location multiplier relative to the base index city (e.g., 1.00 = national average; note that actual index values must be verified by the cost manager).
3. Note the current market-conditions factor: hot market (escalation > 5% p.a.) / stable / soft. Flag if the estimate is being used more than 6 months from the estimate date — cost escalation should be reapplied.

### Phase 3 — Elemental Cost Build-Up

Produce a table of cost elements. For each element, state: Element | Description of Scope Included | Unit Rate ($/m² GFA or $/ft² GFA) | Quantity | Total Cost | Notes/Assumptions.

Standard elements (include all; mark N/A if confirmed out of scope):

| # | Element |
|---|---------|
| 1 | Demolition and site preparation |
| 2 | Substructure (excavation and foundations) |
| 3 | Superstructure (frame and upper floors) |
| 4 | Roof construction |
| 5 | External walls and cladding |
| 6 | Windows, doors, and glazing |
| 7 | Internal partitions and doors |
| 8 | Floor finishes |
| 9 | Ceiling finishes |
| 10 | Wall finishes |
| 11 | Fittings, fixtures, and equipment (built-in only) |
| 12 | Plumbing and sanitary |
| 13 | HVAC and mechanical ventilation |
| 14 | Electrical and lighting |
| 15 | Fire protection (sprinkler and detection) |
| 16 | Vertical transportation (elevators, escalators) |
| 17 | Hydraulics and specialty piping |
| 18 | Communications and security rough-in |
| 19 | External works and landscaping |
| 20 | Site services and utilities connections |

After each element, note the assumed unit rate source: comparable project data / published cost guide / regional benchmark / cost manager adjustment.

### Phase 4 — Contingency and Risk Loading

Apply three tiers of contingency:

| Tier | Purpose | Typical Range | Applied Rate |
|------|---------|---------------|--------------|
| Design contingency | Incomplete design definition at schematic stage | 15–25% of construction cost | State applied % |
| Construction contingency | Unforeseen conditions and minor scope changes | 5–10% of construction cost | State applied % |
| Escalation contingency | Cost movement between estimate date and tender/award | Depends on program | State applied % and basis period |

State the reasoning for each applied rate. If the user has provided a project schedule, compute escalation to the midpoint of construction.

### Phase 5 — Cost Summary and Report Assembly

Produce the DRAFT report:

```
DRAFT — FOR COST MANAGER REVIEW
PRELIMINARY COST ESTIMATE REPORT

Project:         [PROJECT NAME]
Client:          [CLIENT NAME]
Location:        [CITY, COUNTRY]
Building Type:   [TYPE]
GFA:             [X] m² / ft²
Estimate Class:  Class D — Schematic Design / Order of Magnitude
Estimate Date:   [DATE]
Prepared by:     [NAME / FIRM — to be completed by cost manager]
Status:          DRAFT — Not for owner distribution until cost manager review

─────────────────────────────────────────────────────────────────────────
ELEMENTAL COST PLAN
─────────────────────────────────────────────────────────────────────────
[Elements table: # | Element | $/m² GFA | Quantity (m²) | Total ($) | Notes]

SUBTOTAL — CONSTRUCTION COST (ELEMENTS 1–20):       $XXX,XXX
─────────────────────────────────────────────────────────────────────────
CONTINGENCIES
  Design Contingency           [X]%     $XXX,XXX
  Construction Contingency     [X]%     $XXX,XXX
  Escalation Contingency       [X]%     $XXX,XXX

TOTAL CONSTRUCTION COST (INCL. CONTINGENCY):        $XXX,XXX
─────────────────────────────────────────────────────────────────────────
PROJECT COST ADDITIONS (excluded from GC contract — for reference only)
  Professional fees (design + QS)    [%]     $XXX,XXX
  Authority fees and permits                  $XXX,XXX (allow)
  FF&E and owner-supplied items               [Stated scope exclusion]
  Land (if applicable)                        [Not included]

TOTAL PROJECT COST (ORDER OF MAGNITUDE):            $XXX,XXX
─────────────────────────────────────────────────────────────────────────
COST RATE SUMMARY
  Construction cost / m² GFA:     $X,XXX / m²
  Construction cost / ft² GFA:    $XXX / ft²
─────────────────────────────────────────────────────────────────────────
ASSUMPTIONS AND EXCLUSIONS LOG
[Numbered list]

INFORMATION GAPS AND OPEN ITEMS
[Numbered list — items that must be resolved before upgrading to Class C]

COST MANAGER REVIEW BLOCK
This report is a DRAFT Class D estimate. It must be reviewed and signed by
a qualified QS or cost manager before owner presentation or budget-setting.
Reviewer: ________________   Firm: ________________   Date: ________
Signature: ________________
```

### Phase 6 — Quality Gate

Before outputting the report, confirm:

- Every element with a significant cost driver has a stated assumption
- The estimate class (Class D) and DRAFT status are clearly labelled
- No element is marked "TBC" without a placeholder value and a corresponding open item
- The cost manager review block is present and unsigned

## Key Rules

- Never present this estimate as a final tender price, guaranteed maximum price, or construction contract sum.
- Always state the estimate class and date prominently — Class D estimates become stale after 6 months without escalation reapplication.
- If the user provides comparable project data, incorporate it and note the source; do not invent unit rates from training knowledge alone.
- Ask one question at a time during intake. Do not front-load all questions.
- Flag any element where insufficient information prevents a reliable estimate — do not silently set it to zero.
- Never include contingency figures as a substitute for proper scope definition.

## Output Format

Single markdown document structured per the Phase 5 template. Use tables for the elemental cost plan, contingency build-up, and cost summary. Flag all open items and information gaps in a numbered list at the end before the review block.

## Feedback

If this skill did not meet your needs or you encountered a gap, please open an issue at [https://github.com/archlab-space/Open-Skill-Hub/issues](https://github.com/archlab-space/Open-Skill-Hub/issues). Surface this link only when the user expresses an unmet need or dissatisfaction — never in normal interactions.
