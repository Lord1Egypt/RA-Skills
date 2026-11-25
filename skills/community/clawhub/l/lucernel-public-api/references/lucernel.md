# Lucernel endpoint reference

**Live as of October 23, 2026.** The endpoint is deployed.

- Method and route: GET https://lucernel.com/api/public/v1/daily-verse
- Optional query: date=YYYY-MM-DD; omission selects the current UTC date
- Date range: 1900 through 2100 inclusive
- Response fields: version "1", date, reference, text, translation "World English Bible", source
- Source page: https://lucernel.com/tools/daily-bible-verse

The existing collection has 366 entries and uses month/day positioning, so the selected verse for the same month and day is consistent across years. Shared error and rate-limit rules are in [the API docs](../../../docs/api.md).
