# Time Parsing Rules

## Principles

- Never invent an exact date or time when the user did not imply one.
- Preserve the user's timezone if known. Otherwise use the active locale timezone.
- Convert recurring reminders into `RRULE`.

## Ask follow-up questions for

- "明天提醒我交电费" without a time and it is not clearly all-day
- "下周提醒我开会" without a weekday or date
- "月底提醒我报销" when the exact execution date is ambiguous
- "每周提醒我锻炼" without a weekday or time

## Direct mappings

- "明天下午三点" -> exact timestamp tomorrow 15:00 in the current timezone
- "每周一早上九点" -> `RRULE:FREQ=WEEKLY;BYDAY=MO`
- "每个月 1 号上午 10 点" -> `RRULE:FREQ=MONTHLY;BYMONTHDAY=1`
- "全天提醒" -> `all_day=true`

## Past times

If the parsed reminder is already in the past, ask whether the user means:

- the next occurrence
- a different date or time
- an all-day reminder
