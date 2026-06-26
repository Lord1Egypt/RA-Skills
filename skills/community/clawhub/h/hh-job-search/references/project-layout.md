# Project layout

Use a durable workspace project for serious job-search work.

```text
projects/job-search/
  PROFILE.md          # candidate facts only
  TARGET_ROLES.md     # target titles, salary floors, locations, exclusions
  SEARCH_RULES.md     # source order, limits, filters, daily caps
  SOURCES.md          # channel lists, saved searches, URLs
  PIPELINE.md         # master application tracker
  OUTREACH_RULES.md   # whether messaging is allowed and under what conditions
  BLACKLIST.md        # companies, agencies, or patterns to skip
  applications/       # tailored resumes, cover letters, notes per role
  exports/            # csv/json exports
  logs/               # action logs
```

## Minimum required files

For a lightweight setup, create at least:
- `PROFILE.md`
- `TARGET_ROLES.md`
- `PIPELINE.md`

## Pipeline columns

Suggested columns:
- date_found
- source
- company
- title
- url
- fit_label
- fit_score
- salary
- location
- status
- last_action
- next_follow_up
- notes
