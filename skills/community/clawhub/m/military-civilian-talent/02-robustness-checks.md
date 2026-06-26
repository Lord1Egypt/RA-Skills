# Military-Civilian Talent - Robustness and Safety Checklists (02)

## How to Use
Before generating any recommendation, run through the relevant checklists below. These are quality gates to ensure safety and accuracy.

---

## Checklist A: Safety Gate (MANDATORY - Every Response)

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| A1 | Does this involve electrical work? | [] | [] | Add lockout/tagout warning, recommend licensed electrician |
| A2 | Does this involve chemical pesticides or fertilizers? | [] | [] | Add PPE requirements, safe handling, storage warnings |
| A3 | Does this involve machinery operation? | [] | [] | Add pre-operation check reminder, safety procedures |
| A4 | Does this involve structural construction? | [] | [] | Add load-bearing warnings, recommend professional |
| A5 | Does this involve food preservation (canning, fermenting)? | [] | [] | Add botulism and food safety warnings |
| A6 | Is there a disclaimer that this is reference information only? | [] | [] | Add disclaimer |
| A7 | Were all measurements and quantities double-checked? | [] | [] | Verify calculations |

---

## Checklist B: Agricultural Accuracy Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| B1 | Are fertilizer rates within standard agricultural ranges? | [] | [] | Correct to standard rate |
| B2 | Are pesticide recommendations within approved product list? | [] | [] | Replace with approved alternatives |
| B3 | Are planting depths and spacing within standard ranges? | [] | [] | Verify against standard tables |
| B4 | Is the pre-harvest interval respected? | [] | [] | Add required interval |
| B5 | Are seasonal recommendations appropriate for the stated season? | [] | [] | Correct timing |

---

## Checklist C: Machinery Safety Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| C1 | Is the tractor/machinery in safe condition for operation? | [] | [] | Recommend inspection before use |
| C2 | Are lockout/tagout procedures included for maintenance? | [] | [] | Add LOTO steps |
| C3 | Are hot surface warnings included for engine/machinery work? | [] | [] | Add hot surface warning |
| C4 | Is proper PPE specified for the task? | [] | [] | Add PPE requirements |
| C5 | Are procedures for fuel handling included? | [] | [] | Add fuel safety steps |
| C6 | Is the pressure system safety checked (boilers, pressurized vessels)? | [] | [] | Add pressure safety |

---

## Checklist D: Construction Safety Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| D1 | Is structural integrity addressed? | [] | [] | Recommend professional engineer |
| D2 | Are load calculations provided for roofs/floors? | [] | [] | Flag for professional review |
| D3 | Are electrical work recommendations flagged as requiring electrician? | [] | [] | Recommend licensed electrician |
| D4 | Is scaffolding safety addressed for elevated work? | [] | [] | Add scaffolding safety |
| D5 | Is excavation safety addressed for digging/foundation work? | [] | [] | Add shoring/sloping requirements |

---

## Checklist E: Food Safety Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| E1 | For canning: is pressure canning vs. water bath distinction correct? | [] | [] | Correct method |
| E2 | Are pH levels specified for acidified foods? | [] | [] | Add pH testing requirement |
| E3 | Is salt percentage verified for safe preservation? | [] | [] | Correct salt level |
| E4 | Are fermentation temperatures within safe range? | [] | [] | Add temperature control |
| E5 | Are spoilage signs clearly described? | [] | [] | Add spoilage indicators |
| E6 | Are allergens identified where applicable? | [] | [] | Add allergen information |

---

## Checklist F: Output Quality Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| F1 | Are all measurements in standard units (metric preferred)? | [] | [] | Convert to standard units |
| F2 | Is the complexity appropriate for the stated skill level? | [] | [] | Adjust complexity |
| F3 | Are step-by-step instructions numbered and clear? | [] | [] | Make more explicit |
| F4 | Are cost estimates provided or marked as estimates? | [] | [] | Add caveat |
| F5 | Is context (season, location) relevant to the advice? | [] | [] | Add contextual notes |

---

## Error Handling Table

| Error Code | Trigger | Response |
|-----------|---------|---------|
| E001 | Safety-critical procedure requested | Add comprehensive safety warnings |
| E002 | Licensed professional required | Recommend a licensed [electrician/engineer/agricultural expert] |
| E003 | Pesticide/chemical question | Provide only general info, recommend local agricultural extension |
| E004 | Complex structural engineering | This requires a structural engineer |
| E005 | Food preservation safety concern | Provide most conservative safe recommendation |
| E006 | Machinery beyond standard scope | Recommend manufacturer service manual |
| E007 | Financial/legal advice question | Recommend accountant or legal professional |
| E008 | Conflicting information in question | Present multiple scenarios, recommend professional |
| E009 | Medical/health claim in agricultural context | Remove unverified claims, stick to standard practice |
| E010 | Equipment modification question | Recommend against modification without manufacturer approval |
