# Integrated Resource Plan Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Utility Regulation

## Purpose

Drafts a Load-Serving Entity (LSE) Integrated Resource Plan (IRP) for filing with a state public utility commission (PUC) or equivalent regulator. Covers filing scoping, load forecast, existing-resource inventory, need assessment, scenario modeling, preferred portfolio selection, resource-adequacy showing, cost & rate impact, risk & sensitivities, and an action plan tied to the regulator's milestone schedule.

**The output is always DRAFT.** A qualified regulatory team at the filing utility must verify every number, model output, citation, and commitment, and the LSE's authorized signatory must sign the filing before it is served on the PUC and parties.

## When to Use

- Investor-owned utility (IOU), municipal utility, electric cooperative, or community choice aggregator (CCA) preparing its triennial / biennial / annual IRP under a state PUC filing requirement (CPUC, WA UTC, OR PUC, MT PSC, NV PUCN, CO PUC, MN PUC, NC UC, VA SCC, etc.)
- IRP-cycle update or amendment filing in an ongoing PUC docket
- Stakeholder-engagement working draft circulated to a TAC, IRP working group, or environmental-justice advisory body before the formal filing
- Internal pre-filing review by regulatory affairs, resource planning, finance, and outside counsel
- Outside counsel or consulting team supporting a utility's IRP filing under a confidentiality protective order

## What It Does

**Phase 1: Filing Scoping**
1. Captures the filing utility, LSE type (IOU / muni / coop / CCA), service-territory profile, jurisdiction, statutory or PUC-decision authority for the IRP filing, prior IRP docket number and decision, filing cycle, and filing due date
2. Locks the planning horizon (typically 10 / 15 / 20 years), the base year, the load year basis (calendar / weather-year-normalized), and the currency, and notes any reliability / capacity standard the IRP must satisfy (e.g., regional resource-adequacy program, NERC standards)

**Phase 2: Load Forecast**
3. Logs the bundled-load forecast (peak MW and annual MWh) by year across the planning horizon, with reference / high / low scenarios and a documented forecasting methodology
4. Tracks end-use composition, EV-adoption assumption, behind-the-meter PV / storage forecast, energy-efficiency program savings, demand-response capability, and any departing-load assumption (CCA migration, direct-access, IOU re-bundling)
5. Reconciles gross load, load-modifying resources, and the managed load served by the LSE; flags any non-conformance with PUC-assigned LSE load

**Phase 3: Existing Resources and Need Assessment**
6. Tabulates the existing-resource inventory: utility-owned generation, PPAs and tolling agreements, capacity / RA contracts, transmission rights, storage, demand-side resources, scheduled retirements, and contracts expiring inside the planning horizon
7. Builds the need assessment: capacity need by year (planning reserve margin applied), energy / RPS / clean-energy need by year, ELCC or capacity-contribution treatment by resource type, and reliability / resource-adequacy program need
8. Reconciles the GHG / RPS / clean-energy compliance trajectory and any equity / disadvantaged-community (DAC) commitment

**Phase 4: Scenario Modeling and Preferred Portfolio**
9. Defines a scenario matrix (reference, high-load, low-load, high-cost, low-cost, policy-stress, fuel-shock, accelerated-retirement) with explicit assumption deltas for each
10. Records candidate portfolio compositions across scenarios with capacity-expansion logic (least-cost dispatch model, capacity-expansion model name, key constraints, MIP / LP runtime caveats)
11. Selects a preferred portfolio with rationale, and lists alternative portfolios that the PUC may want considered
12. Presents the preferred-portfolio cost & rate impact (NPV revenue requirement, rate trajectory, customer-bill impact) and an equity / DAC overlay where required by jurisdiction

**Phase 5: Risk, Resource Adequacy, and Sensitivities**
13. Runs sensitivities on key drivers (load, gas price, carbon price, capital cost, ELCC, transmission availability, hydro condition) and reports portfolio cost / reliability sensitivity bands
14. Documents the resource adequacy (RA) showing: capacity contribution by resource type, planning reserve margin, regional program participation (e.g., WRAP, MISO, PJM, SPP, CAISO), and any reliance on imports
15. Documents portfolio risk: stranded-asset risk, fuel-price risk, policy risk, supply-chain risk, transmission-access risk, climate / extreme-weather risk

**Phase 6: Action Plan and Filing Packet**
16. Builds the action plan: near-term procurements (RFOs, all-source solicitations, capacity contracts), transmission projects, retirements, EE / DR / TOU program commitments, study commitments, and dates each item is required by the PUC's milestone calendar
17. Drafts a regulatory cover letter, executive summary, table of contents, IRP chapters in the regulator's required order, an appendix index for confidential workpapers, and a §1–§9 dated action-item ledger anchored to the filing due date and the next IRP-cycle milestones

## Output

A DRAFT IRP filing packet with: regulatory cover letter, executive summary, table of contents, chapters in the regulator's required order (filing scoping, load forecast, existing resources, need assessment, scenarios & preferred portfolio, resource adequacy, cost & rate impact, risk & sensitivities, action plan), supporting tables (load-forecast trajectories, existing-resource inventory, need-assessment by year, scenario matrix, preferred-portfolio composition, sensitivities), an equity / DAC overlay where required, a confidentiality-treatment table flagging confidential / public / public-with-redactions content, an action-plan ledger anchored to PUC milestones, and an appendices index — labeled `DRAFT — for filing utility regulatory team to verify and sign`.

## Notes

This skill never determines whether the IRP satisfies a particular PUC's statute or decision, never affirms model results without the filing utility's regulatory and resource-planning team verifying the underlying model run, and never opines on whether a portfolio is "least-cost / best-fit" — that determination is the filing utility's and ultimately the PUC's. The skill flags any number, assumption, or commitment that requires verification from the source model (capacity-expansion model output, transmission-study output, load-forecast model output, fuel-price forecast) and explicitly marks any text that depends on confidential workpapers.

It treats load data, contract terms, fuel-price forecasts, customer-rate impact, and disadvantaged-community overlay data as confidential utility work product subject to the docket's protective order. It does not paste customer-identifying information, specific contract pricing, or other protected-order material into examples or external lookups.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
