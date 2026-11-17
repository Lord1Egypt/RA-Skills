# Audit Checklist — Quick-Pass Compliance

Run this checklist for a fast pre-check before the full critique pipeline, or
as a post-fix verification step. Each item should be a clear yes/no.

## Structure

- [ ] SKILL.md exists and is under 500 lines (`wc -l SKILL.md`)
- [ ] Frontmatter has `name` field (lowercase, hyphens, 1-64 chars)
- [ ] Frontmatter has `description` field (1-1024 chars, third person imperative)
- [ ] `license:` is a top-level frontmatter field (not nested in `metadata`)
- [ ] `includes:` lists `references/**` if references/ directory exists
- [ ] Name matches the directory name

## Description

- [ ] Description states what the skill does
- [ ] Description states when to use it
- [ ] Description includes trigger keywords users would actually type
- [ ] Description includes a NOT clause (exclusions)
- [ ] Description is under 1024 characters
- [ ] Description uses third-person imperative voice (no "I" or "you")

## Content

- [ ] "When to Use" section present with specific trigger keywords
- [ ] "When NOT to Use" section present with explicit boundaries
- [ ] Standard heading format: `## When to Use` and `## When NOT to Use` (not "Trigger conditions", lowercase variants, or embedded in other sections)
- [ ] Gotchas/Pitfalls section present (at least 2 non-obvious issues)
- [ ] Consistent terminology throughout (one term per concept)
- [ ] No time-sensitive information (dates, version-specific notes)
- [ ] No inline credential paths or API key values
- [ ] No stale data counts in storage layout sections
- [ ] No inline storage layout tree diagrams (should be in `references/storage-layout.md`)
- [ ] No inline OKR YAML blocks (should be in `references/okrs.md`)
- [ ] No inline decision invariant lists (should be in `references/decision-invariants.md`)
- [ ] No inline function definition blocks (should be in `references/functions.md`)

## Progressive Disclosure

- [ ] Support file map present with "When to read" column (not "Purpose")
- [ ] Every file in the support file map actually exists (no phantoms)
- [ ] All reference files are pointed to from SKILL.md body with trigger conditions
- [ ] Code ratio under 20% (fenced-block lines / total lines)
- [ ] No deeply nested references (A -> B -> C)

## Workflow Quality

- [ ] Feedback loops present (verify, validate, read-back, confirm)
- [ ] Multi-step workflows have checklists
- [ ] Error handling section or table present
- [ ] Scripts (if any) have --help, structured output, meaningful exit codes
- [ ] Scripts are idempotent where possible

## OCAS-Specific

- [ ] Responsibility boundary section present (for system skills)
- [ ] Ontology types section present or explicitly omitted (for system skills)
- [ ] Journal outputs section present (for system skills)
- [ ] Storage layout uses `{agent_root}/commons/` paths (no data in skill dir)
- [ ] Background tasks section present if skill has cron jobs
- [ ] Self-update command present (for skills synced from GitHub)

## Scoring Summary

| Category | Pass | Total |
|----------|------|-------|
| Structure | _/6 | 6 |
| Description | _/6 | 6 |
| Content | _/8 | 8 |
| Progressive Disclosure | _/5 | 5 |
| Workflow Quality | _/5 | 5 |
| OCAS-Specific | _/6 | 6 |
| **Total** | **_/36** | **36** |

Quick threshold: 30/36 = acceptable, 33/36 = good, 36/36 = excellent.
Below 25/36 triggers a full critique pipeline run.