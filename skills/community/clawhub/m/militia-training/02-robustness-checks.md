# Militia Training - Robustness and Safety Checklists (02)

## How to Use
Before generating any recommendation, run through the relevant checklists. These are quality gates for safety and compliance.

---

## Checklist A: Weapons and Safety Gate (MANDATORY)

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| A1 | Does this involve live ammunition? | [] | [] | Restrict to simulation/educational only |
| A2 | Are range safety rules included in the response? | [] | [] | Add range safety rules |
| A3 | Is finger-off-trigger discipline reinforced? | [] | [] | Add trigger discipline reminder |
| A4 | Are safe muzzle directions specified? | [] | [] | Add muzzle direction reminder |
| A5 | Is eye and hearing protection mentioned? | [] | [] | Add PPE requirement |
| A6 | Does this promote lawful use only? | [] | [] | Add lawful use disclaimer |
| A7 | Is there a disclaimer this is educational reference? | [] | [] | Add disclaimer |

---

## Checklist B: NBC Safety Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| B1 | Is the response limited to DEFENSE and PROTECTION only? | [] | [] | Remove any offensive/creation information |
| B2 | Are agent details limited to identification and effects? | [] | [] | Remove synthesis or weaponization details |
| B3 | Is medical treatment limited to FIELD FIRST AID? | [] | [] | Add professional medical referral |
| B4 | Are decontamination procedures included? | [] | [] | Add decontamination steps |
| B5 | Is MARCH protocol applied correctly for medical response? | [] | [] | Verify MARCH sequence |

---

## Checklist C: Combat Tactics Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| C1 | Does this content remain within educational bounds? | [] | [] | Restrict to authorized training context |
| C2 | Is legal and jurisdictional compliance addressed? | [] | [] | Add lawful conduct reminder |
| C3 | Are proper command/authorization requirements included? | [] | [] | Add chain of command reminder |
| C4 | Is escalation of force properly addressed? | [] | [] | Add proportional response guidance |
| C5 | Are Geneva Convention / laws of armed conflict respected? | [] | [] | Add IHL reminder |

---

## Checklist D: Medical First Aid Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| D1 | Is the MARCH protocol sequence correct? | [] | [] | Correct to M-A-R-C-H |
| D2 | Are tourniquet application indications correct? | [] | [] | Verify against current TCCC guidelines |
| D3 | Is there a disclaimer to seek professional medical care? | [] | [] | Add medical disclaimer |
| D4 | Are medication dosages within standard field ranges? | [] | [] | Verify against field medical guides |
| D5 | Is casualty evacuation urgency correctly assessed? | [] | [] | Adjust evacuation priority |

---

## Checklist E: Information Security Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| E1 | No instructions for improvised explosives or WMDs? | [] | [] | REMOVE immediately |
| E2 | No specific vulnerability or attack targeting instructions? | [] | [] | REMOVE immediately |
| E3 | No instructions that could facilitate real-world harm? | [] | [] | Restrict to authorized training |
| E4 | No personally identifying information of real individuals? | [] | [] | Remove any PII |

---

## Checklist F: Output Quality Gate

| # | Check Item | PASS | FAIL | Action if FAIL |
|---|-----------|------|------|----------------|
| F1 | Are military terminology and abbreviations explained? | [] | [] | Add glossary or explanations |
| F2 | Is the complexity appropriate for the stated level? | [] | [] | Adjust detail level |
| F3 | Are hand signals provided for silent communication? | [] | [] | Add standard signals table |
| F4 | Is the distinction between training/simulation vs real-world clear? | [] | [] | Make distinction explicit |
| F5 | Are all steps numbered and clear? | [] | [] | Make steps more explicit |

---

## Error Handling Table

| Error Code | Trigger | Response |
|-----------|---------|---------|
| E001 | Live ammunition or tactical weapons instruction | I can only provide training guidance in simulation/educational context |
| E002 | IED or weaponization instruction | I cannot provide information on improvised explosives |
| E003 | NBC agent creation or synthesis requested | I can only provide NBC defense and protection guidance |
| E004 | Real-world violence instruction | This type of instruction requires authorization from proper authorities |
| E005 | Medical error detected | Verify against current TCCC or military medical guidelines, add disclaimer |
| E006 | Jurisdictional concern | All activities must comply with applicable laws and regulations |
| E007 | PII of real individuals requested | Decline and remove |
| E008 | Misinformation risk | Cross-reference against current military doctrine |
