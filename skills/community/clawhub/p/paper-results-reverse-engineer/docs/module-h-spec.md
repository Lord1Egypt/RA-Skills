# Module H: Writer Transfer Packet — Full Specification

Module H produces a compressed transfer packet for the academic-results-writer skill's Target-paper Results Style Adaptation Mode.

## Trigger Conditions

Module H is generated when user:
- Requests "给 academic-results-writer 使用"
- Requests "生成写作迁移包"
- Requests "供 Target-paper Results Style Adaptation Mode 使用"
- Requests "把目标文献的 Results 写法迁移到我的数据"
- Explicitly states follow-up use of academic-results-writer for own Results writing

## What Module H Is / Is Not

- ✅ A compressed target-style source for academic-results-writer
- ✅ Abstracted writing patterns, not replicated content
- ❌ NOT a full close-reading
- ❌ NOT a copy of the target paper
- ❌ NOT containing target paper's statistical values for writer to use on user data

## Module H Structure

### H1. Target Source Identity
- Paper title / First author / Year
- Source type: uploaded PDF / pasted Results / web full text / v3.0 output
- Section accessed: Results / Findings / Partial Results
- Extraction coverage: full / partial / insufficient
- Reverse-engineer mode used: quick / standard / close-reading

### H2. Study Design Transfer Summary
- Axis 1 Article Type / Axis 2 Substantive Domain / Axis 3 Data/Method Modality
- Adaptive Branch
- Match relevance for user writing: High / Medium / Low / Design-incompatible
- Reason

### H3. Results Organization Template

Table format:

| Target Results block | Function | Evidence from target paper | Transferability | Notes for writer |
|---|---|---|---|---|

Transferability: `Transfer` / `Partial` / `Do not transfer`.

### H4. Paragraph-Level Writing Pattern
- Opening sentence pattern
- Figure/Table invitation pattern
- Statistical reporting order
- Null-result wording
- Marginal-result wording
- Closing/boundary sentence pattern

### H5. Figure/Table Narrative Pattern
- Figure-first or statistics-first
- Core Figure/Table types
- Caption-to-text strategy
- Error bar / CI / table interpretation cautions
- What writer may transfer
- What writer must not transfer

### H6. Results–Discussion Boundary
- Allowed in Results
- Must stay in Discussion
- Target paper's boundary style
- Safer replacement wording for writer

### H7. Risk Flags to Pass to academic-results-writer

Table format:

| Risk | Source module | Severity | Transfer decision |
|---|---|---|---|

Risk sources: Module E/G causal overclaim, text-table inconsistency, template contamination, Discussion leakage, unsupported mechanism, partial extraction, etc.

Transfer decision: `Do not transfer` / `Transfer with caution` / `Not relevant`.

### H8. Recommended academic-results-writer Mode
- Recommended mode: standard Results writing / target-paper adaptation / design-incompatible fallback
- Suggested output depth: standard-depth / full audit-depth
- Whether Source Ledger is needed: yes / no
- Whether design-incompatible handling is needed: yes / no

## Output Rules

- Module H: 1–2 pages max (unless user requests full bridge).
- Do NOT copy target paper's original sentences — abstract function labels only.
- Do NOT include target paper's statistical values (except brief annotation as "target paper evidence point"); writer must not use these for user's Results.
- H7 must include all target paper risks.
- If Results only partially read: H1 must mark `coverage: partial`; H8 must not recommend full style adaptation unless evidence supports limited adaptation.
- If target paper design is extremely incompatible with user's study: H8 must recommend design-incompatible fallback.

## Chat Output Update

When Module H is generated, add to chat summary:
> "Module H: Writer Transfer Packet attached — can be copied directly for academic-results-writer's Target-paper Results Style Adaptation Mode."
