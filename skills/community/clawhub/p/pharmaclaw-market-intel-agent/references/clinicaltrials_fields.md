# ClinicalTrials.gov API v2 Reference

## Base URL
```
https://clinicaltrials.gov/api/v2/studies
```
No API key required.

## Key Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `query.term` | General search term | `sotorasib` |
| `query.cond` | Condition/disease | `lung cancer` |
| `query.intr` | Intervention/drug | `sotorasib` |
| `filter.overallStatus` | Trial status filter | `RECRUITING` |
| `filter.phase` | Phase filter | `PHASE3` |
| `pageSize` | Results per page (max 100) | `20` |
| `pageToken` | Pagination token | (from response) |
| `format` | Response format | `json` |

## Status Enums
- `RECRUITING` — Currently recruiting participants
- `COMPLETED` — Study completed
- `ACTIVE_NOT_RECRUITING` — Active, no longer recruiting
- `NOT_YET_RECRUITING` — Not yet started recruiting
- `TERMINATED` — Stopped early
- `WITHDRAWN` — Withdrawn before enrollment
- `ENROLLING_BY_INVITATION` — Invitation only
- `SUSPENDED` — Temporarily halted
- `UNKNOWN` — Status unknown

## Phase Enums
- `EARLY_PHASE1`
- `PHASE1`
- `PHASE2`
- `PHASE3`
- `PHASE4`
- `NA` — Not applicable

## Key Response Fields

```
protocolSection.identificationModule
  .nctId          — NCT identifier
  .briefTitle     — Short title
  .officialTitle  — Full title

protocolSection.statusModule
  .overallStatus          — Current status
  .startDateStruct.date   — Start date
  .completionDateStruct.date — Expected completion

protocolSection.designModule
  .studyType              — INTERVENTIONAL, OBSERVATIONAL
  .phases                 — ["PHASE1", "PHASE2"]
  .enrollmentInfo.count   — Target enrollment

protocolSection.conditionsModule
  .conditions             — List of conditions

protocolSection.armsInterventionsModule
  .interventions[].name   — Intervention names
  .interventions[].type   — DRUG, BIOLOGICAL, etc.

protocolSection.sponsorCollaboratorsModule
  .leadSponsor.name       — Lead sponsor name
```

## Pagination
Response includes `nextPageToken` for pagination. Loop until no token or desired count reached.

## Rate Limits
No formal rate limit documented, but be respectful (~1 req/sec for bulk queries).
