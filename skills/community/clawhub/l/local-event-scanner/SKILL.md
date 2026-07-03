---
name: local-event-scanner
description: Use when the user wants to discover real-world events and gatherings in a specific city, area, or region, within an upcoming date range. Also triggers when the user asks to scan, shortlist, or find events matched to their interests. Does not handle meeting planning.
version: 1.1.4
metadata:
  short-description: Find and shortlist events for the user
---

# Event Scanner

Use this skill when the user wants event suggestions or asks what's happening in their area. It discovers real events from configured sources, scores them against the user's taste profile, and returns a ranked shortlist with source links and caveats.

## Procedure

0. Locate the root directory of this skill in the workspace (which may be `.agents/skills/local-event-scanner/`, `skills/local-event-scanner/`, or another path containing this `SKILL.md`). In this document, we refer to this path as `<skill_dir>`.
1. Follow the boot sequence in `<skill_dir>/references/operating-model.md`.
2. Create a new empty run note in `<skill_dir>/runs/` before discovery starts.
3. Add `local-event-scanner` to the run note's `Skills used` list immediately.
4. Apply these pipeline steps in order:
   - `<skill_dir>/steps/step-1-discovery.md`
   - `<skill_dir>/steps/step-2-scoring.md`
   - `<skill_dir>/steps/step-3-calendar-review.md`
   - `<skill_dir>/steps/step-4-shortlist-review.md`
5. Produce the ranked shortlist.

For explicit requests to add a specific suggested event to Google Calendar, follow `<skill_dir>/steps/step-5-add-to-calendar.md`.

Read and write only within this skill's folder.

## Run Note Template

Create the run note from this empty template, using a filename like `YYYY-MM-DD-topic.md`:

```md
# Run: YYYY-MM-DD Topic

## Context

- Geography:
- Window:
- Sources checked:
- Skills used:
  -

## Candidate Events

- Pending discovery.

## Scored Candidates

- Pending scoring.

## Calendar Review

- Pending calendar-aware review.

## Ranked Shortlist

- Pending shortlist review.

## Privacy Check

- Pending final review.
```

Pass this run note path through the rest of the scan. Do not wait until the end to create the run note.

## Output

When invoked, explicitly say: "[Using local-event-scanner skill]"
