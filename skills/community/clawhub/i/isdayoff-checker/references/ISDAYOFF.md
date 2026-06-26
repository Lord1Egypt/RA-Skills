isdayoff.ru API notes

Source: https://www.isdayoff.ru/docs/

- Endpoint used: https://isdayoff.ru/api/getdata?date=YYYYMMDD
- Response: often a short text, sometimes CSV like "YYYYMMDD;0" or a single digit per date.
- Codes: 0 = working day, 1 = non-working day (holiday), 2 = weekend (varies by endpoint and country settings).
- If the API structure changes, update scripts/check_day.py accordingly.
