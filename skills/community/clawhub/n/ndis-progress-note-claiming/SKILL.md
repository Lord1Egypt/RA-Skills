---
name: ndis-progress-note-claiming
description: Write audit-safe NDIS progress notes with goal referencing, generate compliant shift note templates, identify correct support catalogue line item codes, and troubleshoot NDIS claiming errors for Australian registered and unregistered providers.
version: 1.0.0
homepage: https://github.com/arbazex/ndis-progress-note-claiming
metadata: { "openclaw": { "emoji": "📋" } }
---

## Overview

This skill makes the AI agent an expert in NDIS progress note writing, goal referencing, and claiming compliance for Australian providers. It covers audit-safe documentation language, SOAP/DAP note structures, line item code selection across all 15 support categories, claiming rules (travel, non-face-to-face, cancellations), and common payment assurance red flags — all grounded in the NDIS Pricing Arrangements and Price Limits 2025–26 (V1.1, effective 24 November 2025) and NDIS Practice Standards under the Quality and Safeguards Commission framework.

---

## When to use this skill

**Trigger on messages containing:**

- "progress note", "shift note", "case note", "support note", "care note"
- "write a note", "draft a note", "help me write", "rewrite my note", "fix my note"
- "NDIS audit", "audit-safe", "audit ready", "non-conformance", "auditor", "payment assurance"
- "goal referencing", "link to goals", "NDIS goals", "plan goals", "participant goals"
- "line item", "support item", "claiming code", "NDIS code", "support catalogue"
- "how do I claim", "can I claim", "claiming rules", "travel claim", "non-face-to-face", "cancellation claim"
- "invoice error", "claim rejected", "payment rejected", "overclaiming", "wrong code"
- "SOAP note", "DAP note", "progress note template"
- "what to write", "what to include in notes", "what do auditors look for"
- Any NDIS support category mention: "daily living", "community access", "community participation", "capacity building", "support coordination", "SIL", "SDA"

**Do NOT use this skill for:**

- NDIS plan funding amounts, eligibility, or planning decisions (refer to NDIA directly)
- NDIS registration applications, renewal, or audit preparation beyond documentation
- Legal disputes, complaints to the NDIS Commission, or enforcement actions
- Behaviour Support Plan (BSP) creation — this requires a qualified Behaviour Support Practitioner
- Medical, clinical, or therapeutic clinical decision-making (refer to registered practitioners)
- Specific advice on whether a participant qualifies for particular supports (plan decisions are NDIA's role)
- Financial, accounting, or tax advice for NDIS providers

---

## Instructions

### STEP 1 — Identify what the user needs

When a user first raises a request, determine which of the three core tasks is needed before proceeding. Ask only what is necessary — do not ask all questions at once.

**Three core task types:**

**TASK A — Write or fix a progress note**
Required intake questions:

1. What type of support was delivered? (e.g. daily living assistance, community access, SIL, therapy, support coordination)
2. What is/are the participant's relevant NDIS goals that this support relates to? (Ask for the goal text from the plan if possible, or a brief description)
3. What actually happened during the shift/session? (activities completed, participant's engagement and responses, any incidents)
4. What employment type is the worker? (support worker, allied health professional, support coordinator — affects note structure)
5. How long was the session and when? (date, start time, end time)

**TASK B — Identify the correct line item code**
Required intake questions:

1. What type of support was delivered? (describe in plain language)
2. What support category does it fall under? (ask if unsure)
3. Is the participant NDIA-managed, plan-managed, or self-managed?
4. What day and time was the support delivered? (affects time-of-day line item variants)
5. Is this a group or individual support?

**TASK C — Troubleshoot a claiming error or billing question**
Required intake questions:

1. What line item code did you use?
2. What error message or problem did you receive?
3. What type of support was actually delivered?
4. What is the participant's plan management type (NDIA, plan-managed, self-managed)?
5. Is there a current service agreement in place that covers this support and rate?

---

### STEP 2 — Progress Note Writing (TASK A)

#### 2.1 Mandatory elements of every compliant NDIS progress note

Every progress note, regardless of format, must contain all of the following:

| Element                             | What it means                                                                    |
| ----------------------------------- | -------------------------------------------------------------------------------- |
| **Participant full name**           | Full name, not "the client" or "P"                                               |
| **NDIS number** (where recorded)    | For audit linkage                                                                |
| **Date of support**                 | Full date (dd/mm/yyyy)                                                           |
| **Start and finish time**           | Exact clock times — not "morning" or "2 hours"                                   |
| **Support worker full name**        | The worker who delivered the support                                             |
| **Location of support**             | Home address, community venue, facility name                                     |
| **Support type**                    | e.g. Daily Living, Community Access, Domestic Assistance                         |
| **Summary of activities**           | Specific, factual description of what was done                                   |
| **Participant's response**          | Objective observations (behaviour, mood, engagement, communication)              |
| **Goal linkage**                    | Explicit reference to a named NDIS plan goal                                     |
| **Progress indicator**              | Whether progress toward the goal is on track, improving, declining, or unchanged |
| **Incidents or risks**              | Any safety concerns, incidents, medication issues (factual only)                 |
| **Next steps or continuation note** | What happens at the next session                                                 |
| **Signature/author**                | Worker name (electronic ID in digital systems)                                   |

Notes must be written within 24 hours of the support being delivered. Notes written days later are considered unreliable by auditors.

#### 2.2 Objective language rules — the most critical skill

NDIS auditors and Payment Assurance reviewers are trained to identify subjective, vague, or copy-pasted notes. The following rules are non-negotiable.

**NEVER write:**

- "Client did well" → ❌ (vague, no evidence)
- "Good session today" → ❌ (subjective, not auditable)
- "Participant was happy" → ❌ (you cannot observe happiness — you can observe behaviour)
- "Supported client as usual" → ❌ (generic, could apply to any session)
- "No concerns" alone, without specifying what was observed → ❌
- "Continued to work on goals" → ❌ (which goal? what did you actually do?)
- Copy-pasted entries across multiple shifts → ❌ (major audit red flag)

**ALWAYS write observations, not interpretations:**

- ❌ "Maria was happy" → ✅ "Maria smiled throughout the activity and said 'I really enjoyed that today'"
- ❌ "John was anxious" → ✅ "John paced the room, avoided eye contact, and asked three times when the session would end"
- ❌ "She did well with cooking" → ✅ "Sarah independently chopped vegetables and followed each step of the recipe with one verbal prompt for sequencing"
- ❌ "Participant struggled" → ✅ "Participant required four verbal prompts to initiate the task and asked for the activity to be paused twice"

**Prompting level language (use consistently):**

- Independent — completed without any prompts
- Minimal prompting — 1–2 prompts required
- Moderate prompting — 3–5 prompts or physical guidance at one stage
- Maximum prompting — continuous verbal guidance or full physical assistance throughout
- Declined / Refused — participant chose not to participate (record their exact words if possible)

#### 2.3 Goal referencing — required in every note

Every NDIS progress note must link the support delivered to at least one goal in the participant's NDIS plan. This is assessed under NDIS Practice Standard Outcome 3.2 (Support Delivery) and Outcome 2.4 (Information Management).

**Goal referencing formula:**

```
[Activity performed] + [observation of participant response] + [link to specific NDIS goal] + [progress indicator]
```

**Examples of compliant goal referencing:**

- "Supported Marcus with his morning personal hygiene routine (Goal 2: Increase independence in personal care). Marcus independently managed his lower body washing without prompting — an improvement from the previous two sessions where one prompt was required."
- "Assisted Sarah with grocery shopping at Coles (Goal 1: Build skills for independent community access). Sarah selected 9 of 12 items independently using her shopping list, requiring verbal prompts for 3 items. Progress toward goal is on track."
- "Supported James with meal preparation (Goal 3: Develop independent living skills). James chopped vegetables and followed the recipe with two verbal prompts for sequencing. Demonstrated increased confidence compared to previous session."

**If the user does not know the exact goal wording:** Ask them to describe what the participant is working toward. Use their description to draft goal referencing language, but note in the output that it should be updated to match the exact goal language in the participant's NDIS plan.

#### 2.4 Note formats: SOAP vs DAP vs Standard Shift Note

**Choose the format based on context:**

| Format                  | Best for                                                                  | Structure                                                            |
| ----------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Standard Shift Note** | Routine daily support workers — personal care, domestic, community access | Summary → Activities → Response → Goal Link → Incidents → Next Steps |
| **SOAP**                | Allied health, therapy, and clinical support                              | Subjective → Objective → Assessment → Plan                           |
| **DAP**                 | Support coordination, complex behaviour sessions                          | Data → Assessment → Plan                                             |

---

**Standard Shift Note template (for support workers):**

```
PARTICIPANT: [Full Name] | NDIS No: [XXXXXXXX] | DATE: [dd/mm/yyyy]
SESSION: [Start time] – [End time] | LOCATION: [Location]
WORKER: [Full Name] | SUPPORT TYPE: [Support type from plan]

ACTIVITIES DELIVERED:
[Specific factual description of each activity]

PARTICIPANT RESPONSE:
[Objective observations — engagement, communication, mood indicators by behaviour]

GOAL PROGRESS:
Goal referenced: [Goal name/number from plan]
Evidence: [What was observed that relates to this goal]
Progress: [On track / Improving / Declined / Unchanged]

INCIDENTS / OBSERVATIONS:
[Any safety concerns, changes in condition, medication, behaviours of concern — or state "No incidents observed during this session"]

NEXT SESSION:
[What will be continued, adjusted, or escalated]

COMPLETED BY: [Worker name] | TIME COMPLETED: [Time note was written]
```

---

**SOAP Note template (for allied health / therapy):**

```
PARTICIPANT: [Full Name] | NDIS No: [XXXXXXXX] | DATE: [dd/mm/yyyy]
SESSION: [Start time] – [End time] | LOCATION: [Location]
PRACTITIONER: [Full Name + designation] | SUPPORT TYPE: [e.g. CB Daily Activity / Therapy]

S — SUBJECTIVE:
[What the participant reports — use direct quotes where possible]
e.g. "Participant reported feeling more confident with the task since last session."

O — OBJECTIVE:
[Directly observed facts — measurable, specific behaviours]
e.g. "Participant completed 3 of 5 steps independently. Required moderate prompting for steps 2 and 4."

A — ASSESSMENT:
[Clinical/professional interpretation of objective data in context of goals]
e.g. "Participant demonstrates consistent progress toward Goal 4 (improve communication in community settings). Performance is on track with the therapy plan."

P — PLAN:
[Specific next steps, session adjustments, referrals, review dates]
e.g. "Continue current strategy. Introduce task complexity at next session. Review at 4-week milestone. No changes to supports required at this time."

COMPLETED BY: [Name + designation] | TIME: [Time note was written]
```

---

**DAP Note template (for support coordination / complex cases):**

```
PARTICIPANT: [Full Name] | DATE: [dd/mm/yyyy] | WORKER: [Full Name]
SUPPORT TYPE: Support Coordination / Complex Support

D — DATA:
[Factual record of what happened — who was contacted, what was discussed, what actions were taken]

A — ASSESSMENT:
[Worker's professional interpretation of data — what it means for the participant's situation and goals]

P — PLAN:
[Clear next steps, timelines, responsibilities]

GOAL REFERENCED: [Goal name or number from plan]
COMPLETED BY: [Name] | TIME: [Time note was written]
```

#### 2.5 Audit red flags to avoid in notes

NDIS Commission auditors and NDIA Payment Assurance reviewers specifically look for:

1. **Copy-paste notes** — identical or near-identical language across multiple shifts for the same participant, or across different participants
2. **Vague generic entries** — "supported client with daily tasks" without specifics
3. **No goal linkage** — no reference to the participant's NDIS plan
4. **Missing time stamps** — no start/finish time makes claims unverifiable
5. **Notes completed days after the shift** — this raises accuracy questions
6. **Subjective or emotional language** — "client was lovely today", "difficult session"
7. **Medical interpretations by unqualified staff** — support workers must record observations, not clinical judgements
8. **Missing incident documentation** — incidents must be recorded immediately, separately, and linked to the note
9. **Abbreviations that obscure meaning** — write in full, plain English
10. **Over-claiming language** — notes that imply more time or intensity than the billing claim reflects

---

### STEP 3 — Line Item Code Selection (TASK B)

#### 3.1 NDIS support category structure

NDIS line item codes follow the format:

```
[Category]_[Sequence]_[Registration Group]_[Outcome Domain]_[Support Purpose]
Example: 01_011_0107_1_1
         01 = Category (Assistance with Daily Life)
         011 = Sequence number (specific sub-type)
         0107 = Registration Group
         1 = Outcome Domain
         1 = Support Purpose (1=Core)
```

**All 15 support categories:**

| Code | Category Name                                                | Budget Type       | Shown In Portal As             |
| ---- | ------------------------------------------------------------ | ----------------- | ------------------------------ |
| 01   | Assistance with Daily Life                                   | Core              | Daily Activities               |
| 02   | Transport                                                    | Core              | Transport                      |
| 03   | Consumables                                                  | Core              | Consumables                    |
| 04   | Assistance with Social, Economic and Community Participation | Core              | Social Community Participation |
| 05   | Assistive Technology                                         | Capital           | Assistive Tech                 |
| 06   | Home Modifications                                           | Capital           | Home Mods                      |
| 07   | Support Coordination                                         | Capacity Building | Support Coordination           |
| 08   | Improved Living Arrangements                                 | Capacity Building | CB Home Living                 |
| 09   | Increased Social and Community Participation                 | Capacity Building | CB Social Community            |
| 10   | Finding and Keeping a Job                                    | Capacity Building | CB Employment                  |
| 11   | Improved Relationships                                       | Capacity Building | CB Relationships               |
| 12   | Improved Health and Wellbeing                                | Capacity Building | CB Health Wellbeing            |
| 13   | Improved Learning                                            | Capacity Building | CB Lifelong Learning           |
| 14   | Improved Life Choices                                        | Capacity Building | CB Choice Control              |
| 15   | Improved Daily Living Skills                                 | Capacity Building | CB Daily Activity              |

#### 3.2 High-frequency line item codes reference table

The following are the most commonly used line item codes across the sector. Always verify current price limits in the official NDIS Support Catalogue 2025–26.

**Category 01 — Assistance with Daily Life (Core)**

| Code              | Description                                        | When to use                                                                                 |
| ----------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 01_011_0107_1_1   | Assistance with Self-Care Activities — Weekday     | Personal care, hygiene support, dressing — weekday daytime                                  |
| 01_011_0107_1_1_T | Provider Travel (to/from participant for Cat 01)   | Travel time for daily living supports                                                       |
| 01_015_0107_1_1   | High Intensity Daily Personal Activities — Weekday | Where worker requires complex health care skills (e.g. enteral feeding, complex bowel care) |
| 01_002_0107_1_1   | House Cleaning and Other Household Activities      | Domestic assistance (cleaning, laundry)                                                     |
| 01_004_0107_1_1   | Meal Preparation and Delivery                      | Meal prep support                                                                           |

_Weekend/Evening variants:_ Codes ending in \_S (Saturday), \_U (Sunday), \_P (Public Holiday) or \_N (Evenings/Nights) where listed in catalogue. Always check that the catalogue includes these variants for the specific item.

**Category 04 — Community Participation (Core)**

| Code              | Description                                                              | When to use                                                                                          |
| ----------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| 04_104_0125_6_1   | Access Community Social and Recreational Activities — Standard (Weekday) | 1:1 community access, individual support for social/recreational activities                          |
| 04_104_0125_6_1_S | Saturday variant                                                         | Same — Saturday                                                                                      |
| 04_104_0125_6_1_U | Sunday variant                                                           | Same — Sunday                                                                                        |
| 04_104_0125_6_1_P | Public holiday variant                                                   | Same — public holiday                                                                                |
| 04_105_0125_6_1   | Innovative Community Participation — Weekday                             | Specialised or intensive programs for participants needing more targeted community engagement        |
| 04_210_0125_6_1   | Community, Social and Recreational Activities — Activity Cost            | Claim activity/program costs directly (camps, fees) — equally fractioned among participants in group |

**Category 07 — Support Coordination (Capacity Building)**

| Code            | Description                     | When to use                                                          |
| --------------- | ------------------------------- | -------------------------------------------------------------------- |
| 07_002_0106_8_3 | Support Coordination            | Standard support coordination activities                             |
| 07_004_0132_8_3 | Specialist Support Coordination | For participants with complex needs requiring specialist coordinator |

**Category 09 — Increased Social and Community Participation (Capacity Building)**

| Code            | Description                                               | When to use                                                                        |
| --------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 09_011_0125_6_3 | Skills Development and Training — Community Participation | Structured programs to build skills for community independence                     |
| 09_009_0125_6_3 | Community Participation Activities — Activity Cost        | Program/tuition/activity fees (art classes, sport coaching, skills-based programs) |

**Category 15 — Improved Daily Living Skills (Capacity Building)**

| Code            | Description                                 | When to use                              |
| --------------- | ------------------------------------------- | ---------------------------------------- |
| 15_037_0128_1_3 | Therapeutic Supports — Physiotherapy        | Physio delivered under CB Daily Activity |
| 15_056_0128_1_3 | Therapeutic Supports — Occupational Therapy | OT services                              |
| 15_043_0128_1_3 | Therapeutic Supports — Speech Pathology     | Speech therapy                           |
| 15_054_0128_1_3 | Therapeutic Supports — Psychology           | Psychology services                      |

#### 3.3 Line item selection decision tree

```
Q1: Is this a Core Support (regular day-to-day assistance) or Capacity Building (skill development)?
  → Core: Start at Categories 01–04
  → Capacity Building: Start at Categories 07–15
  → Capital (equipment, home mods): Categories 05–06

Q2: For Core supports — what type of activity?
  → Personal care / hygiene / self-care at home → Cat 01 (Daily Life)
  → Domestic assistance (cleaning, cooking) → Cat 01 (Daily Life)
  → Community access / social activities → Cat 04 (Community Participation)
  → Transport to access supports → Cat 02 (Transport)

Q3: What day and time was support delivered?
  → Monday–Friday daytime: standard code
  → Saturday: _S variant (if listed in catalogue)
  → Sunday: _U variant (if listed in catalogue)
  → Public holiday: _P variant (if listed in catalogue)
  → Evening / overnight: _N or _E variant (if listed — check award-based rates)

Q4: Is this group or individual support?
  → Individual (1:1): standard individual code
  → Group (1:2, 1:3, 1:4+): group code variant with per-participant rate (lower per head)
  → IMPORTANT: Group rates are per-participant, not total. Do not claim the individual rate for group sessions.

Q5: Is there a travel component to claim separately?
  → Refer to claiming rules in Step 4 before selecting travel line items.

Q6: Is this support delivered by a qualified practitioner (OT, physio, speech pathologist, psychologist)?
  → Use Category 15 (Improved Daily Living) therapeutic codes
  → NOT Category 01 (Daily Life) — mixing these is a common audit error
```

#### 3.4 Common line item errors to avoid

1. **Using Cat 01 for therapy sessions** — if a qualified therapist delivers the support, it belongs in Cat 15 (or the relevant registration group)
2. **Using weekday rates on weekends** — incorrect code variant; use \_S, \_U, \_P suffixes
3. **Claiming individual rate for group sessions** — must divide cost proportionally per participant
4. **Using legacy/deactivated codes** — the 2025–26 catalogue removed 35 legacy items; deactivated codes are rejected at the portal
5. **Claiming a line item not in the participant's plan budget type** — Capacity Building codes cannot be claimed against Core budgets and vice versa
6. **Using "Quote" items without a pre-agreed quote** — Quote items have no published price cap; a formal quote and participant/plan manager agreement is required before delivery

---

### STEP 4 — Claiming Rules (TASK C)

#### 4.1 Provider travel claiming rules (2025–26 PAPL V1.1)

Travel claiming is one of the most frequently misunderstood areas and a top audit finding.

**Worker/support worker travel (Category 01, 04, etc.):**

- Provider travel can be claimed only if it is explicitly agreed in the participant's Service Agreement before travel occurs
- Claim using the provider travel line item for the relevant support category (e.g. 01_011_0107_1_1_T)
- Labour travel: claim at the agreed hourly support rate (same rate as the primary support, or lower if agreed)
- Non-labour travel: $0.99 per kilometre (standard vehicle), or actual cost for tolls, parking, public transport
- Non-labour travel uses the separate "Provider Travel — Non-Labour Costs" line item
- Time caps apply (check specific registration group in PAPL)

**Therapy provider travel (Category 15 — from 1 July 2025):**

- Therapy providers can now only claim **50% of their standard hourly rate** for travel time
- This applies to all therapy supports including Early Childhood Early Intervention (ECEI)
- Example: OT at $193.99/hr → travel claim = $96.99/hr (50% rate)
- Travel must be to or from the participant for a face-to-face service
- Telehealth/remote services: no travel claim applies
- Non-labour travel costs (km, tolls, parking) are still claimable at actual cost if agreed in the Service Agreement

**Pre-conditions for any travel claim:**

1. Service Agreement explicitly includes travel time and km reimbursement
2. Travel is directly linked to a face-to-face support delivery
3. Claim does not exceed applicable time caps in the PAPL
4. Non-labour travel claimed separately using the correct line item

#### 4.2 Non-face-to-face (NF2F) claiming

**What can be claimed as non-face-to-face:**

- Writing reports, case notes, and formal documentation related to a specific participant
- Telephone calls with family members, other providers, or services on behalf of a participant
- Research or planning directly related to coordinating a participant's supports

**What CANNOT be claimed as non-face-to-face:**

- Processing invoices or payment claims
- Developing service agreements
- General administrative overhead
- Staff training or supervision (not related to a specific participant)
- Travel time (this is a separate claim type)

**Rules for NF2F claiming:**

- Must be agreed in the Service Agreement before it is claimed
- Must be directly related to a specific participant's support
- Must be documented (note what was done, for whom, and how long it took)
- Administrative overhead is considered included in the price limit — it is not separately claimable

#### 4.3 Short-notice cancellation claiming

**Standard cancellation rules (2025–26 PAPL):**

- Short notice is defined as: less than **2 clear business days** before the scheduled support
- If a participant cancels with less than 2 clear business days' notice without reasonable excuse: provider may claim **100% of the agreed fee** up to the price limit
- This requires: service agreement with a cancellation clause, rostered worker who could not be redirected, and documentation of the cancellation
- Providers must use the correct cancellation line item variant (not the standard service code)
- If the participant provides a reasonable excuse (hospitalisation, emergency), the cancellation rule may not apply — use judgement and document the reason

**Provider-initiated cancellation:** If the provider cancels, no cancellation fee applies.

**Reasonable excuse examples:** Participant hospitalised, family emergency, severe weather making attendance unsafe, sudden illness.

#### 4.4 Claiming for group supports

- Group supports are billed per participant, not per group
- The per-participant rate is lower than individual rates and varies by group size (1:2, 1:3, 1:4, 1:5+)
- The group rate for a 1:3 session will be approximately one-third of an individual session (per participant)
- Rosters must accurately record: participant names, attendance times, actual staff ratio for each shift
- Do not claim for a participant who did not attend
- If a participant arrives late or leaves early, pro-rate the claim for actual time attended

#### 4.5 Service Agreement requirements for compliant claiming

A valid Service Agreement must exist before claiming. A compliant service agreement includes:

1. Participant's full name and NDIS number
2. Specific support types to be delivered
3. NDIS line item codes for each support type
4. Agreed price per hour or session (at or below the price limit)
5. Service delivery schedule (days, times, frequency)
6. Travel agreement (if applicable)
7. Non-face-to-face agreement (if applicable)
8. Cancellation policy referencing the 2-clear-business-day rule
9. Consent and signature (participant or nominee)

**Update the Service Agreement:** Any time rates change (e.g. after 1 July each year), you add new support types, or new claiming rules apply (like therapy travel changes from July 2025) — the Service Agreement must be updated before claiming under the new arrangement.

---

### STEP 5 — Audit Compliance Checklist

Use this checklist to assess if a provider's notes and claiming are audit-ready:

**Progress Notes — Documentation Checklist:**

- [ ] Every session has a note completed within 24 hours
- [ ] Notes link clearly to at least one NDIS plan goal
- [ ] Complex or significant events are documented in separate case notes or incident reports
- [ ] Support logs include: participant name, NDIS number, date, start/finish time, quantity
- [ ] Group rosters accurately reflect staff ratios and actual attendance times
- [ ] Notes reference any health or behaviour support protocols applied
- [ ] Notes are specific to this participant — not copy-pasted across shifts or participants
- [ ] No vague language (e.g. "all good", "as usual", "participant was fine")
- [ ] Incident reporting is timely and separate from routine shift notes
- [ ] Billing records precisely match note documentation (hours, dates, support type)

**Claiming — Compliance Checklist:**

- [ ] Correct line item code used (current 2025–26 catalogue, no deactivated codes)
- [ ] Correct time-of-day variant used (weekday vs Saturday vs Sunday vs public holiday)
- [ ] Group vs individual code matched to actual delivery model
- [ ] Travel claimed only if Service Agreement includes travel provisions
- [ ] Therapy travel claimed at 50% rate (from 1 July 2025)
- [ ] Non-face-to-face only claimed for eligible activities agreed in Service Agreement
- [ ] Cancellation claims have documentation of short-notice cancellation and no reasonable excuse
- [ ] Claim dates match participant's active plan period
- [ ] Participant is listed as a "my provider" for NDIA-managed funding

---

## Rules and Guardrails

1. **Always disclaim at the end of any output:** _"This is general guidance for documentation and claiming practice based on publicly available NDIS rules. It is not legal, clinical, regulatory, or compliance advice. For complex situations, consult the NDIS Quality and Safeguards Commission (1800 035 544 / ndiscommission.gov.au) or a registered NDIS compliance consultant."_

2. **Never write or suggest clinical or medical content in notes.** Support workers are not clinicians. Do not include clinical diagnoses, medication recommendations, or medical assessments in notes. Record observations only. If the user asks the agent to include clinical interpretations for a support worker note, decline and explain the boundary.

3. **Never advise on legal action, complaints, or Commission disputes.** If a user raises enforcement matters, non-compliance disputes, or Commission proceedings, direct them to the NDIS Commission (1800 035 544) or a lawyer. Do not provide legal analysis.

4. **Never fabricate line item codes or price limits from memory.** Present known codes as reference examples and always direct users to verify current rates and codes in the official NDIS Support Catalogue 2025–26 at ndis.gov.au/providers/pricing-arrangements.

5. **Never suggest how to structure a claim or note to conceal a non-compliance.** If a user's situation appears designed to make a non-compliant claim appear compliant, do not assist. Explain that the NDIS Support Catalogue and PAPL set rules that cannot be worked around.

6. **Never assist with claiming for a service that was not delivered.** If the user's description implies they want to claim for hours not worked or supports not provided, refuse clearly and note that this constitutes fraud under NDIS rules.

7. **Do not provide Behaviour Support Plan content.** Behaviour support is a restricted practice under the NDIS. Only a qualified Behaviour Support Practitioner can create or amend a BSP. If asked to write BSP content, decline and refer to a registered BSP.

8. **Do not advise on participant eligibility or plan decisions.** Plan funding levels, support category allocations, and eligibility are determined by the NDIA. If a user asks whether a participant should have funding for something, direct them to their NDIA planner or Local Area Coordinator (LAC).

9. **Protect participant privacy.** Do not ask for or use real participant names, addresses, or identifying information beyond what is needed to draft a note example. If real identifying details are provided, use them only to complete the note and do not repeat them unnecessarily.

10. **Do not advise on registration group requirements or NDIS registration.** Registration rules, approved registration groups, and audit processes are NDIS Commission matters. General guidance is appropriate; specific registration advice is not.

---

## Output Format

### For progress note drafting (TASK A):

Present the drafted note using the appropriate template (Standard Shift Note, SOAP, or DAP) as defined in Step 2. Use the exact field structure from the template. After the note, include a brief **Note Quality Check** section:

```
NOTE QUALITY CHECK:
✅ Mandatory elements present: [list which are included]
⚠️ Suggested improvements: [list any gaps, e.g. "Goal number not provided — update to match exact plan language"]
📋 Goal link: [confirm goal was referenced, or flag if missing]
🕐 Timeliness reminder: Complete this note within 24 hours of the session
```

### For line item identification (TASK B):

Present as:

```
RECOMMENDED LINE ITEM:
Code: [XX_XXX_XXXX_X_X]
Description: [Official support item name]
Category: [Category number and name]
Applies to: [When this code should be used]
Day/time variant: [Confirm weekday/weekend/PH variant used]
Price limit: [State "Verify current limit at ndis.gov.au/providers/pricing-arrangements" — do not fabricate dollar amounts]

ALTERNATIVE TO CONSIDER: [If a second code may also apply, present with explanation]

⚠️ VERIFY: Always confirm the code is active and the price limit is current in the 2025–26 Support Catalogue before claiming.
```

### For claiming troubleshooting (TASK C):

Present as:

```
ISSUE IDENTIFIED: [Plain-language description of what went wrong]
LIKELY CAUSE: [Specific reason — wrong code, wrong variant, no Service Agreement, etc.]
RECOMMENDED FIX: [Step-by-step resolution]
PREVENTION: [What to put in place to avoid this next time]

⚠️ If the error involves a pattern of incorrect claims, seek compliance advice before resubmitting.
```

---

## Error Handling

**User doesn't know the participant's NDIS goals:**
→ Ask: "Can you describe in your own words what this participant is working toward in their plan?" Use the description to draft approximate goal referencing and flag clearly: _"Update this to match the exact goal language in the participant's current NDIS plan before finalising."_

**User provides vague activity description:**
→ Ask specific follow-up questions: "What specific tasks did you help with? Did the participant do any of it independently? What prompting did you provide? Did anything unusual happen?" Do not draft a note until sufficient detail is collected.

**User asks for a note for a session that occurred more than 24 hours ago:**
→ Draft the note but add a note quality flag: _"⚠️ TIMELINESS: This note is being written more than 24 hours after the session. During audits, delayed notes may be questioned. Record the actual time of writing accurately and avoid reconstructing details you cannot clearly recall."_

**User asks for a code but the support type is ambiguous:**
→ Present two candidate codes with clear explanations of when each applies and ask the user to confirm which description better matches what was delivered. Do not guess.

**User reports a claim was rejected with "multiple business validations failed":**
→ Walk through the NDIS claiming troubleshooting checklist: (1) verify code is not deactivated, (2) confirm participant plan is active for the claim dates, (3) check provider is registered as "my provider" for NDIA-managed participants, (4) confirm budget type matches line item category, (5) verify no funding balance issues. Direct user to the NDIS Portal troubleshooting page: ndis.gov.au/providers/working-provider/getting-paid/claims-and-payments-troubleshooting.

**User asks about behaviour support strategies for a participant:**
→ Note-taking of factual behavioural observations is within scope. Writing or suggesting behaviour support strategies, PBS plans, or restrictive practices guidance is not. Decline the strategy component and refer to a registered Behaviour Support Practitioner.

**User appears to be a participant (not a provider):**
→ Adjust tone to participant perspective. Explain that progress notes are written by their support workers and providers. For participant-facing questions about what should be in their notes or whether they can see their notes, direct to the NDIS website: ndis.gov.au/participants/using-your-plan/managing-your-funding.

---

## Examples

### Example 1 — Support worker shift note (daily living, community access)

**User:** "Can you help me write a shift note? I took Maria to the shops today, she bought some food. She seemed in a good mood. I'm not sure how to write it properly."

**Agent intake questions asked:** "What time did the shift start and finish? What are Maria's NDIS goals — specifically any goals around community access or independence? Did Maria do anything independently? Did anything unusual happen?"

**User provides:** "9am to 11:30am. Her goal is to increase independence in community access and shopping. She selected most items herself from a list. Nothing unusual happened."

**Agent output:**

```
PARTICIPANT: Maria [Surname] | NDIS No: [XXXXXXXX] | DATE: [dd/mm/yyyy]
SESSION: 09:00 – 11:30 | LOCATION: [Shopping centre name], [Suburb]
WORKER: [Worker full name] | SUPPORT TYPE: Community Access — Shopping

ACTIVITIES DELIVERED:
Supported Maria with grocery shopping at [Store name]. Maria used her shopping list to select items throughout the store. Worker accompanied Maria for safety and navigation assistance.

PARTICIPANT RESPONSE:
Maria selected 10 of 13 items on her shopping list independently. Required verbal prompting for 3 items (worker directed Maria to the correct aisle for each). Maria initiated conversation with a store assistant independently when asking about a product's location. No distress observed. Maria stated "I like doing this myself" when completing the checkout process.

GOAL PROGRESS:
Goal referenced: [Goal name/number] — Increase independence in community access and shopping.
Evidence: Maria independently selected the majority of her shopping list items with minimal prompting. Independently initiated communication with store staff.
Progress: On track / Improving [confirm with plan reviewer]

INCIDENTS / OBSERVATIONS:
No incidents observed during this session. No changes in behaviour, mood, or health noted.

NEXT SESSION:
Continue community access shopping support. Consider increasing complexity by reducing list detail to build further independent decision-making.

COMPLETED BY: [Worker name] | TIME COMPLETED: [Time written]
```

**Note Quality Check:**

- ✅ All mandatory elements present
- ⚠️ Update NDIS number and participant surname before filing
- ⚠️ Update goal number/name to match exact language in Maria's NDIS plan
- 📋 Goal link: Present and specific
- 🕐 Write this note within 24 hours of the session

---

### Example 2 — SOAP note (allied health / OT session)

**User:** "I'm an OT. Can you help me write a SOAP note for a home visit where I assessed a client's kitchen setup? His goal is to improve meal preparation independently."

**Agent output:**

```
PARTICIPANT: [Full Name] | NDIS No: [XXXXXXXX] | DATE: [dd/mm/yyyy]
SESSION: [Start] – [End] | LOCATION: Participant's home — kitchen
PRACTITIONER: [Name], Occupational Therapist | SUPPORT TYPE: CB Daily Activity — Therapeutic Supports (OT)

S — SUBJECTIVE:
Participant reported that he finds meal preparation "really tiring, especially standing for long periods." Participant expressed a goal of preparing simple meals three times per week independently. Reports current confidence with meal preparation as 4/10.

O — OBJECTIVE:
Home visit conducted to assess kitchen environment and functional capacity for meal preparation. Participant demonstrated ability to navigate kitchen safely. Observed difficulty maintaining standing posture at the bench for more than 8 minutes. Required two rest breaks during a 15-minute cooking simulation. Grip strength adequate for utensil use. Kitchen layout assessed: benchtop height appropriate; storage requires reaching above shoulder height for frequently used items.

A — ASSESSMENT:
Participant's fatigue and postural limitations are the primary barriers to achieving independent meal preparation. Functional capacity is consistent with plan goal of increasing independence in daily living skills. Current kitchen setup creates unnecessary strain. Evidence of motivation and willingness to engage. Goal is achievable with appropriate environmental modifications and energy conservation strategies.

P — PLAN:
1. Provide written fatigue management and energy conservation strategies to participant and support worker within 5 business days.
2. Recommend relocation of frequently used kitchen items to waist-height storage.
3. Assess suitability of perching stool to reduce standing fatigue — trial at next session.
4. Review at next session in [date range] to assess impact of strategies.
5. Goal 3 (Improve independent meal preparation) remains current and progress is on track.

COMPLETED BY: [Name], OT | TIME: [Time written]
```

---

### Example 3 — Line item code selection

**User:** "What code do I use when my support worker takes a participant to a social group on a Saturday morning?"

**Agent output:**

```
RECOMMENDED LINE ITEM:
Code: 04_104_0125_6_1_S
Description: Access Community Social and Recreational Activities — Saturday
Category: 04 — Assistance with Social, Economic and Community Participation (Core Supports)
Applies to: Individual (1:1) support worker accompanying a participant to a social activity on a Saturday
Day/time variant: Saturday (_S suffix)
Price limit: Verify current Saturday limit in the 2025–26 NDIS Support Catalogue at ndis.gov.au/providers/pricing-arrangements

ALTERNATIVE TO CONSIDER:
If the activity is a structured skills-based group program (not just accompanying to a social outing), the Capacity Building code 09_011_0125_6_3 (Increased Social and Community Participation) may be more appropriate — but only if this is funded under the participant's CB budget, not Core.

⚠️ VERIFY: Confirm the _S Saturday variant is listed and active for this code in the current Support Catalogue. Confirm the participant's plan includes Core Social Participation funding. If this is a group session (1:2 or more), use the group variant at the per-participant group rate.
```

---

### Example 4 — Claiming error troubleshooting

**User:** "My claim for a Saturday session was rejected. I used code 01_011_0107_1_1 but it won't go through."

**Agent output:**

```
ISSUE IDENTIFIED:
You have used the standard weekday code (01_011_0107_1_1) for a Saturday session. This code applies to weekday daytime rates only.

LIKELY CAUSE:
The NDIS portal validates claim codes against the day of service. Saturday sessions require the Saturday variant of the code, which has a higher price limit and different suffix.

RECOMMENDED FIX:
1. Resubmit the claim using the Saturday variant: 01_011_0107_1_1_S
2. Confirm that the Saturday rate is within the price limit in the 2025–26 Support Catalogue
3. Confirm the participant's Service Agreement authorises Saturday support at the Saturday rate
4. Confirm funding is available in the participant's plan for this claim date

PREVENTION:
Check the day of service before selecting a line item code. Set up a reference sheet of weekday vs weekend code variants for the support types your organisation delivers. Review your Service Agreements to ensure they explicitly cover Saturday, Sunday, and public holiday support and the applicable rates.

⚠️ If you notice a pattern of weekday codes being used for weekend sessions, this could be underclaiming (you may be owed more) or a systemic setup issue in your billing system. Review recent claims for accuracy.
```

---

### Example 5 — Non-compliant note rewrite

**User:** "My auditor flagged this note. Can you help me fix it? The original says: 'Took John to shops. He was happy and did okay. Good session.'"

**Agent action:** Collect missing information: session times, location, participant's goals, what specifically happened, what John did independently.

**Agent output after collecting details:**

_Original note (non-compliant):_ "Took John to shops. He was happy and did okay. Good session."

_Why it fails audit:_

- No start/finish time
- No goal reference
- "Happy" is subjective — not an observed behaviour
- "Did okay" is vague — no evidence of support delivered or participant response
- No next steps

_Rewritten compliant note (using detail provided):_

```
PARTICIPANT: John [Surname] | DATE: [dd/mm/yyyy]
SESSION: 10:00 – 12:00 | LOCATION: [Store name], [Suburb]
WORKER: [Worker name] | SUPPORT TYPE: Community Access

ACTIVITIES DELIVERED:
Supported John with grocery shopping. John used a prepared list to navigate the store. Worker provided supervision and verbal prompts as needed.

PARTICIPANT RESPONSE:
John selected 7 of 10 items on his list independently. Required verbal prompts for 3 items (aisle location guidance). John smiled and said "I got most of them myself today" at checkout. No distress or incidents observed.

GOAL PROGRESS:
Goal referenced: [Goal name/number] — Build independence in community access.
Evidence: John independently selected the majority of shopping items with minimal prompting. Demonstrated self-directed navigation through most of the store.
Progress: On track.

INCIDENTS / OBSERVATIONS:
No incidents observed. No changes in health or behaviour noted.

NEXT SESSION:
Continue community access shopping support. Consider introducing self-checkout with support next session.

COMPLETED BY: [Worker name] | TIME: [Time written]
```
