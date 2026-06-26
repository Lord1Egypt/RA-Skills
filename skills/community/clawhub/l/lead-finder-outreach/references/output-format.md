# Output Format

This skill produces a draft `50-company prospect shortlist` for teams that need defensible company records and public contact paths.

## Required Output Contract

The final deliverable should be a single Markdown report with an embedded machine-readable summary block.

### Top-level sections

1. `# Prospect Summary`
1. `# Research Method`
1. `# Qualification Rules`
1. `# Company Shortlist`
1. `# Notes / Gaps`

Include `# Outreach Angles` only when the user explicitly asks for outreach copy.

### Summary block

Include a compact YAML or JSON block near the top so downstream tools can parse the result.

Example fields:

```json
{
  "pack_id": "optional-stable-id",
  "generated_at": "2026-03-19T00:00:00+08:00",
  "request": {
    "target_count": 50,
    "niche": "dental clinics",
    "location": "California, United States"
  },
  "results": {
    "qualified_companies": 50,
    "shortlisted_companies": 50,
    "excluded_companies": 18
  },
  "source_coverage": {
    "company_websites": true,
    "directories": true,
    "public_case_studies": true,
    "social_or_profile_pages": true
  }
}
```

## Company Record Schema

Each company entry should use the same field order.

Required fields:

- `rank`
- `company_name`
- `website`
- `company_location`
- `category_label`
- `public_contact_path`
- `fit_cue`
- `recommended_outreach_angle`
- `confidence`
- `score`

Optional fields:

- `source_profile_url`
- `public_phone`
- `linkedin_or_social`
- `source_links`
- `notes`

Human-readable column labels should map cleanly to:

- company name
- website
- geography
- category or niche label
- public contact path
- fit cue or notes
- LinkedIn or relevant social profile

### Field definitions

- `company_location`: the public geography tied to the company record, usually the requested market or a visible location hint.
- `category_label`: a normalized label for the business type or niche.
- `public_contact_path`: a same-site contact, booking, appointment, or consultation URL when visible. Fall back to the homepage only when no stronger public path is available.
- `fit_cue`: one concise sentence on why the company appears to match the request.
- `recommended_outreach_angle`: one sentence on the hook most likely to resonate if outreach is needed.
- `confidence`: `high`, `medium`, or `low` depending on how strong the public evidence is.
- `score`: numeric ranking value used to sort stronger shortlist entries above weaker ones.

## Pack-Level Rules

- Produce exactly 50 qualified companies when possible.
- If fewer than 50 can be validated, output the largest defensible list and explain the gap in `# Notes / Gaps`.
- Do not invent employees, phone numbers, emails, budgets, or client names.
- Do not include a company unless it has a public website and at least one usable public contact path or an explicit homepage fallback.
- Sort the list by score, then by specificity of match.
- Keep the shortlist skimmable: one company per row or block, one concise reason, one concise outreach angle.
