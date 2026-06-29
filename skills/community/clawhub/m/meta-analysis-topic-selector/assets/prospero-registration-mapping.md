# PROSPERO Registration Form Field Mapping

This file maps the 11 sections of this Skill's topic report to the fields of the PROSPERO online registration form (https://www.crd.york.ac.uk/prospero/), so the user can fill them in directly during registration and avoid omissions.

## When to use

- The topic report is generated and the recommendation is "proceed"
- The user is about to submit a PROSPERO registration
- The protocol is not yet complete, but PROSPERO registration can proceed in parallel with protocol writing

## PROSPERO form fields ↔ topic-report fields

The PROSPERO form (as of 2024) has 22 required/optional fields. The table below gives the corresponding report field and fill tips for each.

| # | PROSPERO field | Required | Corresponding report field | Fill tip |
|---|---|---|---|---|
| 1 | Title | Required | Report title + Section 2 research question | Use "... : a systematic review and meta-analysis" format; include P/I/C keywords |
| 2 | Original language title | Optional | Non-English title (if registering in another language) | Fill if non-English; leave blank if English |
| 3 | Registration number | Auto | — | PROSPERO auto-assigns; format CRDXXXXXXXXXXXXX |
| 4 | Anticipated or actual start date | Required | meta.get('start_date') (add to JSON) | Registration date = start date; if data extraction has begun, use the actual start |
| 5 | Anticipated completion date | Required | meta.get('expected_completion_date') (add to JSON) | Estimate 6–12 months; PROSPERO accepts extensions |
| 6 | Contact person | Required | meta.researcher | Registration lead; ORCID recommended |
| 7 | Email address | Required | meta.contact_email (add to JSON) | Contact email |
| 8 | Affiliation | Required | meta.affiliation | Primary contact institution |
| 9 | Country | Required | meta.country (add to JSON) | Country of the primary contact institution |
| 10 | Review question(s) | Required | Section 2 "Research-question statement" (pico.research_question) | Copy the PICO statement directly; list multiple questions one by one |
| 11 | Searches | Required | Section 6 "Pre-search strategy" + Section 5 dedup queries | List databases + time range; attach at least one complete query |
| 12 | Types of study to be included | Required | Implied study design in Section 2 PICO | Explicit RCT/NRSI/cohort/case-control/mixed; if RCT-only, write "randomized controlled trials" |
| 13 | Condition or domain being studied | Required | Disease in Section 2 pico.population | Use standardized nomenclature (e.g., ICD-10, MeSH) |
| 14 | Participants/population | Required | Section 2 pico.population | Copy P fully; include age/sex/stage/comorbidities/exclusions |
| 15 | Intervention(s), exposure(s) | Required | Section 2 pico.intervention or exposure | Copy I/E fully; include dose/duration/route/follow-up; for complex interventions, follow Section 6 of the PICO guide |
| 16 | Comparator(s)/control | Required | Section 2 pico.comparator | Copy C fully; match I in granularity |
| 17 | Types of outcome measures | Required | Section 8 primary outcomes + secondary outcomes | Primary outcomes ≤2; each outcome specify measurement tool, timepoint, effect size |
| 18 | Secondary outcome(s) | Optional | Section 8 secondary outcomes table | List separately from primary; PROSPERO does not allow post-hoc additions |
| 19 | Data extraction | Required | Section 7 PRISMA #8 data items | Describe data-extraction form fields; note whether two-reviewer extraction |
| 20 | Risk of bias assessment | Required | Section 7 PRISMA #9 risk of bias | State RoB tool (RoB 2/ROBINS-I/QUADAS-2) + whether two-reviewer assessment |
| 21 | Strategy for data synthesis | Required | Section 3 meta type + Section 9 subgroups and sensitivity | State synthesis model (fixed/random), effect size, subgroups, sensitivity, heterogeneity threshold, publication-bias method |
| 22 | Subgroup analysis | Optional | Section 9 prespecified subgroups | List each subgroup variable + rationale; PROSPERO encourages prespecification |
| 23 | Sensitivity analysis | Optional | Section 9 sensitivity analyses | List each sensitivity analysis plan |
| 24 | Language restrictions | Required | Section 6 presearch.languages | Explicit "English only" / "English + Chinese" / "No restriction" |
| 25 | Other metadata | Optional | — | Funding source, conflict of interest, IP |

## Required fields not directly in the topic report

These fields need to be added in the JSON (recommend extending the meta section):

```json
{
  "meta": {
    "researcher": "John Doe",
    "affiliation": "XX Medical School",
    "country": "China",
    "contact_email": "researcher@example.edu",
    "start_date": "2026-06-22",
    "expected_completion_date": "2027-06-30"
  }
}
```

## Common PROSPERO registration errors

1. **Title missing "systematic review" or "meta-analysis"** → title must include one, otherwise returned
2. **Search string only PubMed** → attach at least one complete query; for other DBs write "adapted from PubMed"
3. **Primary outcome >2** → PROSPERO accepts but most journals will question it; recommend ≤2
4. **Study design not stated** → field 12 must explicitly state RCT/NRSI etc.; "all studies" is not acceptable
5. **RoB tool mismatched to study type** → using ROBINS-I for RCTs is a common error
6. **Language restriction not stated** → leaving blank defaults to "no restriction", which may not match the actual search string
7. **Too few prespecified subgroups** → only "by sex" is insufficient; recommend ≥3 subgroups
8. **Adding/removing outcomes after registration** → PROSPERO allows "modifications" but you cannot "delete an already-declared primary outcome"; additions must be marked "added post-hoc"

## PROSPERO registration flow

1. Register an account at https://www.crd.york.ac.uk/prospero/
2. Click "Register a review" → choose "Health-related"
3. Fill in each field per the table above
4. A registration number is assigned within about 1–2 weeks
5. After assignment, you can cite in the paper: "This systematic review is registered with PROSPERO (CRDXXXXXXXXXXXXX)"
6. For major changes later (e.g., primary outcome adjustment), update in the PROSPERO backend and note the change date

## Synchronization requirements after PROSPERO registration

After registration, the following changes must be synchronized promptly:
- Primary outcome added/removed → update immediately
- Eligibility criteria adjusted → update immediately
- Completion date extended → update immediately
- Data extraction started/completed → update as appropriate
- Protocol version changed → update as appropriate

Failure to synchronize promptly may lead reviewers to question registration-vs-study inconsistency at submission.

## Pre-registration self-check list

Before submitting to PROSPERO, self-check:

- [ ] Title contains "systematic review" or "meta-analysis"
- [ ] All 22 required fields filled
- [ ] Primary outcomes ≤2
- [ ] At least 1 complete search string pasted
- [ ] RoB tool matched to study type
- [ ] ≥3 prespecified subgroups
- [ ] Language restriction consistent with the search string
- [ ] Contact email valid
- [ ] Completion date reasonable (recommend 6–12 months)
- [ ] Field content cross-checked with all collaborators
