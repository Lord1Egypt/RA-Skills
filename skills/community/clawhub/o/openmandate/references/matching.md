# How Matching Works

## The Model

OpenMandate helps founders find cofounders and early teammates beyond their network. Both sides post a mandate — what you need and what you offer. OpenMandate keeps working on your behalf and introduces both sides when there is strong mutual fit.

**One mandate = one match.** OpenMandate keeps looking until it finds the right counterparty. This is not a list of candidates — it's one introduction.

## Matching Flow

1. Mandate goes active — OpenMandate starts working on your behalf (status: `active`)
2. OpenMandate keeps looking across active mandates
3. When there is strong mutual fit, both users are notified via email
4. Both users review the match: compatibility grade, summary, strengths, concerns
5. Each user accepts or declines independently
6. On mutual acceptance, contact information is exchanged

## Compatibility Assessment

Matches include a detailed compatibility assessment:

```json
{
  "grade": "strong",
  "grade_label": "Strong Match",
  "summary": "Both mandates align on distributed systems expertise...",
  "strengths": [
    { "label": "Technical alignment", "description": "Both sides focus on distributed systems with Go/Python stack" },
    { "label": "Stage fit", "description": "Series A company matches the candidate's preference for growth-stage startups" }
  ],
  "concerns": [
    { "label": "Location", "description": "Mandate specifies on-site but candidate prefers remote" }
  ]
}
```

### Score Tiers

| Score Range | Grade | Label | Meaning |
|-------------|-------|-------|---------|
| 60-74 | `good` | Good Match | Solid alignment on core needs |
| 75-89 | `strong` | Strong Match | Strong alignment with complementary strengths |
| 90-100 | `exceptional` | Exceptional Match | Near-perfect mutual fit |

Minimum match threshold is 60. Mandates below this threshold are not surfaced as matches.

## Match Statuses

| Status | Meaning |
|--------|---------|
| `pending` | Match found. Awaiting responses from both parties. |
| `accepted` | You accepted. Waiting for the other party. |
| `confirmed` | Both parties accepted. Contact info revealed. |
| `declined` | One or both parties declined. |
| `expired` | Match expired before both parties responded. |
| `closed` | Match closed (associated mandate was closed). |

## Contact Exchange

Contact information is only revealed after **both parties accept**. Before that, you see the compatibility assessment but not who the other person is.

After mutual acceptance (status: `confirmed`), the match response includes the counterparty's contact:
```json
{
  "contact": {
    "email": "counterparty@example.com",
    "phone": null,
    "telegram": null,
    "whatsapp": null
  }
}
```

Only fields the counterparty provided at mandate creation are populated.

## Outcome Reporting

After both parties accept and contact info is revealed, either side can report how the match went:

```
POST /v1/matches/{match_id}/outcome
{ "outcome": "succeeded" | "ongoing" | "failed" }
```

| Outcome | Effect |
|---------|--------|
| `succeeded` | Match fulfilled its purpose. Associated mandate is closed. |
| `ongoing` | Conversation is still in progress. OpenMandate checks back later. |
| `failed` | Match did not work out. Associated mandate is reactivated for new matches. |
