# Query and Reschedule Playbook

## Find the Right Calendar Source

1. Search for the database or page by title when the user gives only a human name.
2. Resolve `database_id`, then fetch the matching `data_source_id`.
3. Confirm the date property used by the calendar view.

## Query a Time Window

Use bounded filters:

```json
{
  "filter": {
    "and": [
      {"property": "Date", "date": {"on_or_after": "2026-03-01"}},
      {"property": "Date", "date": {"on_or_before": "2026-03-31"}}
    ]
  },
  "sorts": [{"property": "Date", "direction": "ascending"}]
}
```

## Create a Calendar Item

- Confirm title, date semantics, and required status.
- Use `data_source_id` as parent when creating a page for modern integrations.
- Read the created page back and return title, date, status, and URL.

## Reschedule an Existing Item

- Pre-read the exact item inside its current time window.
- Confirm whether only the date changes or status and owner also change.
- Patch only the required properties, then verify with a follow-up read.

## Archive or Cancel

- Prefer status changes such as `Cancelled` over archival when the user wants history preserved.
- Archive only after explicit confirmation and only when the exact page match is verified.
