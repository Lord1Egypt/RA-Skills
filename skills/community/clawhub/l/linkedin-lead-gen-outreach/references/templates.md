# Templates

## ICP template

- Campaign name:
- Business objective:
- Offer or value proposition:
- Primary audience:
- Seniority:
- Geography:
- Industries:
- Company size:
- Required signals:
- Exclusions:
- Desired CTA:

## Lead object template

```json
{
  "first_name": "",
  "last_name": "",
  "full_name": "",
  "linkedin_url": "",
  "title": "",
  "company": "",
  "location": "",
  "keyword_match": "",
  "business_potential_note": "",
  "personalization_note": "",
  "role_relevance": 0,
  "company_fit": 0,
  "likely_need": 0,
  "timing_signal": 0,
  "personalization_depth": 0,
  "score_total": 0,
  "priority": "medium",
  "score_reason": "",
  "message_v1": "",
  "campaign_name": "",
  "owner": "",
  "source": "LinkedIn",
  "status": "to_review",
  "next_action": "review"
}
```

## Professional message patterns

### Pattern A — role + value

Hi {{first_name}} — your role at {{company}} stood out.
We help teams improve {{outcome}} with a focused and practical approach.
Open to a brief conversation?

### Pattern B — signal + relevance

Hi {{first_name}} — noticed {{signal}} at {{company}}.
That is often when {{problem}} becomes a real operational priority.
Happy to share a few relevant ideas if useful.

### Pattern C — executive tone

Hi {{first_name}} — reaching out because your scope looks highly relevant.
We support teams working on {{priority}} with a low-friction method.
Would it make sense to compare notes briefly?

## Score reason examples

- Strong role match, target company profile, and credible near-term need signal
- Good audience fit with moderate context but limited urgency evidence
- Partial fit only, with weak business potential and minimal personalization context
