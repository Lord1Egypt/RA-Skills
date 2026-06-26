# Manual J Residential Load Calculation

**Platforms:** Claude · Openclaw · Codex
**Domain:** Residential HVAC Design — ACCA Manual J 8th Edition

## Purpose

A residential load-calculation drafting partner for HVAC contractors, energy raters (HERS / RESNET), home-performance auditors, code officials, and design-build firms. Turns a house's geometry, envelope assemblies, climate location, and occupancy profile into a DRAFT ACCA Manual J 8th Edition block + room-by-room load report, with room-by-room cooling CFM targets ready for Manual D duct design and a Manual S equipment-sizing handoff block.

## When to Use

- Sizing a new or replacement central / mini-split / heat-pump system before equipment selection (Manual S) and duct design (Manual D)
- Meeting permit-jurisdiction or rebate-program requirements that mandate an ACCA-approved Manual J on file (e.g., MA, CO, NY, NC, RI, CT utility programs and many IECC-adopting AHJs)
- Reviewing a contractor's submitted load calc for over-sizing or input errors before approving an equipment proposal
- Refreshing a load calc after a major envelope upgrade (air-sealing, window replacement, insulation, additions)
- Building the load-calc artifact that downstream tools (Manual S, Manual D, Manual T, ENERGY STAR / IRA tax-credit documentation) reference

## What It Does

**Phase 1: Project and design conditions**
1. Captures location (city / county / ZIP), ACCA Manual J Table 1A outdoor design conditions (winter 99%, summer 1% dry-bulb / mean-coincident wet-bulb, summer 1% dehumidification grain depression), and elevation
2. Captures indoor design conditions (default: 70 °F heating / 75 °F cooling, 50% RH ceiling)
3. Captures whole-house geometry — conditioned floor area, ceiling heights, number of stories, orientation, and a room schedule
4. Confirms calculation mode — block load only, room-by-room only (required for duct design), or both

**Phase 2: Envelope assemblies**
5. Captures wall assemblies (above-grade, below-grade), ceilings / attics, floors (over crawlspace, slab-on-grade, over conditioned), with U-values
6. Captures fenestration (window U-value, SHGC, area, orientation, internal / external shading) and doors
7. Captures infiltration estimate (blower-door CFM50 → CFMnatural via Manual J, or ACCA tightness class)
8. Captures mechanical ventilation (ASHRAE 62.2 rate, ERV / HRV recovery effectiveness)

**Phase 3: Internal gains and duct effects**
9. Captures occupancy (default 1 per bedroom + 1, max 230 BTU/h sensible + 200 BTU/h latent per person), lighting and appliance gains by room, and any process loads
10. Captures duct system — location (conditioned / unconditioned attic / vented crawlspace / buried), R-value, total leakage to outside (CFM25), and supply / return split

**Phase 4: Computation and report**
11. Computes block + room-by-room sensible / latent heating + cooling loads (BTU/h)
12. Computes total cooling CFM at design ΔT (default 20 °F) and distributes room-by-room CFM for Manual D handoff
13. Emits the Manual S equipment-sizing handoff block — total cooling load, sensible heat ratio, total heating load, design ΔT — and flags equipment-sizing windows (95–115% of total cooling load at design conditions; sensible capacity ≥ design sensible load; heating capacity ≥ design heating load; heat-pump balance-point analysis)
14. Runs an input-sanity audit (oversize indicators, infiltration outliers, missing internal gains, mis-oriented windows, default-versus-measured U-values)

## Output

A DRAFT load-calculation packet with:

- Project + design-conditions block (location, Table 1A values, indoor setpoints)
- Envelope assemblies table (with U-values and source — measured / NREL / manufacturer / Manual J default)
- Infiltration + ventilation block
- Internal gains schedule
- Duct system block
- Block load summary (heating, cooling sensible, cooling latent, cooling total, SHR)
- Room-by-room load table with cooling CFM targets
- Manual S equipment-sizing handoff block
- Input-sanity audit (with red flags and recommended corrections)
- Assumption log (every default used, with citation)
- Licensed-designer review and sign-off block
- Unresolved-information list

## Safety

This skill produces a DRAFT calculation, **not** a stamped design document. Every output is labeled **DRAFT — LICENSED MECHANICAL DESIGNER / ENERGY RATER / RESPONSIBLE PERSON MUST REVIEW AND ACCEPT BEFORE PERMIT SUBMITTAL, REBATE FILING, OR EQUIPMENT PURCHASE**. The skill follows ACCA Manual J 8th Edition methodology, ACCA Manual S equipment-sizing windows (95–115% of design cooling load; ≥100% of design heating load), and the relevant IECC / ASHRAE 62.2 / ENERGY STAR references that apply at the project's jurisdiction. The skill does **not** size equipment, design ducts, or produce a Manual S / Manual D / Manual T output — it produces the inputs those calculations depend on. The skill does not select refrigerant, design refrigerant line-sets, or specify any product. If inputs are missing, the skill logs them as **Unknown — measurement or assumption required** and does not fabricate U-values, leakage rates, or design conditions. Outputs are not stamped engineering deliverables; jurisdictions that require a Professional Engineer's seal still require one.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
