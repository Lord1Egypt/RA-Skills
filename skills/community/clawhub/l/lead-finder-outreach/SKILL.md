---
name: lead-finder-outreach
description: Use when the user wants to find agency-ready prospects, build a company shortlist by niche and geography, or extract public contact paths. Also use when the user asks for prospect packs, lead lists, agency prospecting, local business targets, contact-path research, or a 50-company outbound shortlist.
metadata:
  version: 1.0.0
---

# Lead Finder Outreach

Build a defensible company shortlist by niche and geography. The default deliverable is a `50 companies` list with public-source evidence, public contact paths, and CSV-friendly fields. Outreach copy is optional in this first version.

## When to Use

Use this skill when the user wants:

- a niche + geography-based prospect list
- public contact-path research
- a ready-to-contact shortlist for outbound or CRM import
- optional outreach copy tied to verified public signals

Do not use this skill for:

- private-data enrichment
- mass email scraping
- guaranteed direct email lists
- vague "just get me leads" requests without at least a niche or geography

## Inputs

Collect the minimum viable request before researching:

- `niche` or industry
- `location` or geography
- `fit criteria` in one sentence

Optional:

- target company count
- exclusions
- output format preference
- seller context if outreach copy is needed

If the user does not specify a count, default to `50 companies`.

## Rules

- Use public-source evidence only.
- Prioritize official websites, public profiles, directories, and visible contact paths.
- Do not fabricate emails, phone numbers, headcount, clients, or performance claims.
- Do not include a company unless you can explain why it fits.
- If fewer than 50 defensible companies exist, return the strongest list and explain the gap.

## Workflow

1. Parse the request into niche, location, fit criteria, and count.
2. Research candidates from public sources only.
3. Validate each company against the fit criteria.
4. Capture the required fields in a consistent schema.
5. Rank and trim to the final shortlist.
6. Generate outreach variants only if the user asks for them.
7. Present the pack in a skimmable, reusable format.

For detailed source selection and validation rules, read:

- [research-workflow.md](references/research-workflow.md)

For the exact output schema, read:

- [output-format.md](references/output-format.md)

For the minimum JSON input, read:

- [input-template.json](references/input-template.json)

For outreach copy shapes, read:

- [outreach-templates.md](references/outreach-templates.md)

## Output Expectations

The final answer should include:

- a short request summary
- a clearly structured shortlist
- public source-backed company entries
- contact paths
- notes on coverage gaps or confidence where needed

If the user explicitly asks for outreach copy, include 2-3 cold outreach email variants.

If the user asks for CSV-style output, keep field names stable and machine-friendly.

## Quality Bar

Before finalizing:

- verify every company has a public URL
- verify every company has at least one usable contact path
- verify every outreach angle is tied to a real public signal when outreach is requested
- remove duplicates and weak borderline entries

The result should feel like a clean, defensible prospect shortlist, not a scraped dump.
