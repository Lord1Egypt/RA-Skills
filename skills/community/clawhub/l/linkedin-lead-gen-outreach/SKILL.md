---
name: linkedin-lead-gen-outreach
description: Lightweight LinkedIn prospecting and outreach workflow for researching qualified leads, applying simple prioritization, drafting concise personalized messages, exporting clean CSV or Google Sheets-ready lead lists, and summarizing campaign activity. Use when preparing a compliant LinkedIn lead generation process, refining ICP-based targeting, building review-ready lead sheets, or generating simple outreach dashboards.
---

# LinkedIn Lead Gen Outreach

Run a clean, review-first LinkedIn prospecting workflow focused on lead quality, concise messaging, and simple export-ready sales operations.

Keep every output structured, evidence-based, and easy to review before outreach.

## Workflow

Use this sequence for complete requests:

1. define targeting
2. collect prospect data
3. apply simple lead scoring
4. draft short personalized outreach
5. export structured lead data
6. summarize campaign metrics

## 1. Define targeting

Capture the search brief before producing leads.

Minimum inputs:

- keywords
- target job titles
- seniority
- industry or company type
- location
- exclusions
- business objective

If the request is underspecified, convert it into a concise ICP before generating leads.

## 2. Collect prospect data

Use visible LinkedIn information, user-provided data, or manually reviewed search results.

Capture these fields whenever possible:

- full name
- LinkedIn URL
- title
- company
- location
- search match
- business potential note
- personalization signal
- source list or query

Useful personalization signals include:

- recent post theme
- recent promotion or job change
- hiring activity
- company growth signal

Do not invent facts. If evidence is weak, mark it clearly and keep the message more general.

## 3. Apply simple lead scoring

Use a lightweight and explainable scoring model.

Default scoring dimensions:

- role relevance: 0-5
- company fit: 0-5
- likely need: 0-5
- timing signal: 0-5
- personalization depth: 0-5

Total score bands:

- 20-25: high priority
- 12-19: medium priority
- 0-11: low priority

Always include a one-line explanation.

## 4. Draft personalized messages

Write opening messages that are:

- professional
- concise
- 2-3 lines max
- easy to review and edit
- grounded in real signals

Recommended structure:

1. relevant opener
2. business relevance
3. soft CTA

Rules:

- keep messages short and polished
- avoid hype, pressure, or artificial urgency
- avoid unsupported claims
- if personalization is weak, prefer a role-based message over forced specificity

## 5. Use message templates

Adapt one of the templates in `references/templates.md`.

Prefer:

- signal-based messages when evidence is strong
- role-based messages when evidence is moderate
- executive-tone messages for senior stakeholders

## 6. Export format

Prefer a flat CSV structure that also imports cleanly into Google Sheets.

Recommended columns:

- first_name
- last_name
- full_name
- linkedin_url
- title
- company
- location
- keyword_match
- business_potential_note
- personalization_note
- score_total
- priority
- score_reason
- message_v1
- campaign_name
- owner
- source
- status
- next_action

Suggested status values:

- to_review
- approved
- ready_for_outreach
- contacted
- replied
- disqualified

## 7. Dashboard and statistics

When the user asks for a dashboard, produce a lightweight summary that can live in Markdown, CSV-derived calculations, or Google Sheets.

Include these default metrics:

- total leads
- high / medium / low priority counts
- leads by title
- leads by geography
- personalization coverage
- leads ready for outreach

Keep it simple and executive-friendly.

## Google Sheets guidance

When preparing a sheet:

- freeze the top row
- apply filters to all headers
- use data validation for `priority`, `status`, and `next_action`
- add a summary section above or in a second tab
- preserve the original raw data columns

## Compliance standard

Operate in a LinkedIn-compliant, review-first manner.

Use this skill to support:

- profile research
- qualification
- message drafting
- structured exports
- reporting

Do not rely on deceptive automation, hidden sending loops, or behavior intended to bypass platform safeguards.

## Deliverable order

For a complete request, produce outputs in this order:

1. targeting summary
2. scoring rubric
3. lead table or CSV-ready rows
4. message variants
5. dashboard summary
6. Google Sheets notes

## Quality bar

A strong result is:

- clean and business-ready
- grounded in visible evidence
- concise enough for sales execution
- easy to export or review
- compliant and professional

## Community edition note

This edition focuses on lightweight prospect research, simple prioritization, concise outreach drafting, and clean CSV or Sheets-ready exports.

## Resources

Use bundled resources when useful:

- `references/templates.md` for ICP, scoring, and message templates
- `scripts/csv_builder.py` to convert JSON leads into CSV
- `scripts/sheets_prep.py` to normalize CSV fields for Google Sheets workflows
- `scripts/dashboard_stats.py` to compute simple campaign metrics from a CSV file
