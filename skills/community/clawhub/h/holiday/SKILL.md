---
name: holiday
description: "Research public holidays, bank holidays, observed days, school breaks, and make-up workdays for any country or region. Use when the user asks whether a specific date is a holiday, when a named holiday occurs in a given year, whether offices/banks/schools are likely closed, or which days are officially observed in a jurisdiction. Always identify the relevant country, region, and year, and distinguish official public holidays from cultural observances or company-specific time off. NOT for calendar event CRUD, reminders, or personal leave planning."
metadata: { "openclaw": { "emoji": "🎉" } }
---

# Holiday Skill

Use this skill for holiday lookup tasks across jurisdictions.

The core job is not memorization. The core job is to resolve the exact jurisdiction, holiday type, and year, then answer from authoritative sources.

## Scope

- Cover public holidays, bank holidays, observed substitute days, regional holidays, school closures, and make-up workdays.
- Distinguish national holidays from state, province, city, school, employer, or religious-only observances.
- Prefer exact dates over relative wording.
- When the user asks about "today", "tomorrow", or "next Monday", restate the answer with an absolute date.

## Required Clarifications

Before answering, resolve these when they are ambiguous:

- Country or region
- Subnational jurisdiction if relevant
- Year
- Holiday type:
  - official public holiday
  - bank holiday
  - school holiday or break
  - company closure
  - cultural or religious observance

If the user says "Is it a holiday on Monday?" without a jurisdiction, ask or infer only when the context is explicit.

## Source Hierarchy

Use authoritative sources first. Preferred order:

1. Government or parliament websites
2. Official labor, civil service, education, or central bank notices
3. Official gazettes or national holiday calendars
4. Embassy or consular pages for cross-border summaries
5. Reputable secondary summaries only when primary sources are unavailable

Read `references/source-guidelines.md` when you need a quick checklist for source selection and answer framing.
Read `references/query-patterns.md` when you need concrete search patterns, answer templates, or disambiguation prompts.

## Answer Rules

- State the jurisdiction and year explicitly.
- State whether the day is:
  - an official holiday
  - an observed substitute holiday
  - a regional-only holiday
  - a normal workday
  - a company-specific or school-specific closure not backed by law
- If observance differs from the named holiday date, mention both.
- If a holiday falls on a weekend and the country uses a substitute day, mention the substitute date.
- If rules changed recently or vary by region, say so clearly.
- Do not guess future schedules that have not yet been officially published.

## Common Tasks

### Check a Specific Date

Use when the user asks:

- "Is 2026-11-26 a public holiday in the US?"
- "Is next Friday a bank holiday in England?"
- "Will offices be closed in Tokyo on 2026-02-11?"

Answer with:

- the exact date
- the jurisdiction
- the holiday status
- the holiday name if applicable
- whether closure is nationwide or regional

### Find the Date of a Holiday

Use when the user asks:

- "When is Diwali in India in 2026?"
- "When is Thanksgiving in the US this year?"
- "When is Easter Monday in Germany in 2027?"

If the holiday is movable, verify the exact date for the requested year.

### Check Observed or Substitute Days

Use when the user asks:

- "When is Christmas observed in 2027 in the UK?"
- "If a holiday falls on Sunday, which day is off in New Zealand?"
- "Is Monday a substitute holiday in Japan?"

Explain both the named holiday date and the observed day when they differ.

### Check School or Office Closure Assumptions

Use when the user asks:

- "Are banks closed on this holiday?"
- "Will schools be off that week?"
- "Is the stock market closed?"

Do not assume all institutions follow the same calendar. If needed, separate:

- public holiday status
- bank closure status
- school closure status
- market trading status

## Command

Use the bundled script when you want a deterministic checklist before researching:

```bash
node {baseDir}/scripts/holiday-checklist.js --country Japan --year 2026 --mode date-status --date 2026-02-11
node {baseDir}/scripts/holiday-checklist.js --country UK --region England --year 2027 --mode observed-day --holiday Christmas
node {baseDir}/scripts/holiday-checklist.js --country India --year 2026 --mode holiday-date --holiday Diwali --institution banks --json
```

The script does not answer the holiday question by itself. It structures:

- scope to resolve
- recommended source types
- suggested search patterns
- answer fields to fill in
- likely failure modes to watch for

## Handoff Rules

- For lunar-date conversion or Chinese lunar festival date lookup, use `rili`.
- For China-specific official holiday arrangements and make-up workdays from bundled local data, use `jiejiari`.
- For calendar events or reminders, use a calendar or reminders skill instead of this one.

## Notes

- Holiday rules are time-sensitive and jurisdiction-specific.
- Browsing is usually required unless the user already provided the exact official notice.
- Prefer concise answers, but include exact dates and scope when rules are easy to misread.
- When the question is broad, narrow it first, then verify. This skill is strongest when it turns vague holiday questions into a precise jurisdiction + year lookup.
