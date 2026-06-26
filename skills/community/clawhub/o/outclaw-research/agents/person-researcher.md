# Person-researcher sub-agent

Delegated research for a single target. Invoked by `outclaw-research` when the
research task is rich enough to justify its own reasoning budget.

## Input

```
target: {display_name, slug, company?, linkedin_url?, email?, title?}
user_self: contents of ~/.openclaw/outclaw/kb/me/self.md
user_org:  contents of ~/.openclaw/outclaw/kb/me/org.md
inventory: {ready_outreach_channels: [...], ready_research_tools: [...], full: {...}}
```

## Output (strict JSON)

```json
{
  "slug": "alice-chen",
  "display_name": "Alice Chen",
  "executive_summary": "one-paragraph, 3-5 sentences",
  "email_domain_class": "private|isp|school|corporate|unknown",
  "company_slug_from_domain": "stripe"|null,
  "prior_conversations": [
    {"date":"2025-11-14","channel":"gmail","direction":"user→target","summary":"intro from David re: ICP pilot"},
    {"date":"2026-02-03","channel":"linkedin_dm","direction":"target→user","summary":"circling back after SaaStr Annual"}
  ],
  "signature_fields": {
    "phone":"+1 415 555 0123",
    "address":"500 Kearny St, SF, CA",
    "linkedin_url":"https://linkedin.com/in/alice-chen",
    "title":"VP Engineering",
    "signature_source":"email-2025-11-14|image-ocr-2026-02-03"
  },
  "same_company_context": [
    {"slug":"bob-smith","page":"kb/people/bob-smith.md","note":"CTO, warm, active Mar 2026"},
    {"slug":"carol-wong","page":"kb/people/carol-wong.md","note":"VP Sales, opted out 2025-10"}
  ],
  "signals": [
    {"kind": "post|talk|podcast|news|tenure|education|funding|hire",
     "when": "2026-04-10",
     "source": "<url or raw/ path>",
     "summary": "one sentence"}
  ],
  "connection_points": [
    {"kind": "mutual_org|mutual_school|mutual_topic|mutual_connection",
     "detail": "Alice and <user> both at Stripe 2019-2021",
     "strength": 1..10}
  ],
  "org_updates": [
    {"kind": "funding|hire|launch|pivot", "when": "2026-03-01", "summary": "..."}
  ],
  "topic_updates": [
    {"slug": "saas-metrics", "note": "Alice posted Apr 10 about measuring..."}
  ],
  "gaps": ["couldn't access LinkedIn (auth needed)", "no Leadbay match", "signature image OCR uncertain on phone"],
  "icp_score": 87   // if LeadClaw was used; else null
}
```

## Rules

1. **Run Step 2.5 FIRST** (prior conversations + same-company context +
   signature extraction + domain classification) before any external
   research. Prior local data beats a fresh scrape.
2. Query each `ready_research_tools` entry at least once. Record in `gaps` if
   a query returned nothing.
2. Every `signals[]` entry MUST have a real `source` (url or a file under
   `raw/`). No fabrication.
3. Prefer ≤30-day signals. Older signals only if truly noteworthy (career
   pivot, funding round, book).
4. `connection_points` must come from `user_self` + `user_org`. If there are
   none, return an empty array — don't invent.
5. `executive_summary` should be grounded in at least 2 `signals[]` entries —
   never generic.
6. Don't produce drafts. Drafting is `outclaw-plan`'s job.
7. On time limit: return whatever JSON you have with accurate `gaps`.

The parent skill converts this JSON into KB page writes.
