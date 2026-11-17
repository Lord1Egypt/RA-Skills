# mx-zixuan Result Fields

Read this only when parsing raw `mx_zixuan_*_raw.json` or explaining watchlist output.

## Query Output

The script writes a CSV for watchlist queries when data is returned. Common user-facing fields include:

- security code
- security name
- latest price
- percentage change
- price change
- turnover rate
- volume ratio

Field names may vary by API response. Prefer the generated CSV headers for presentation.

## Operation Output

Add/delete responses usually include:

- status/code: operation status.
- message: API result message.
- data: optional operation detail.

Only report success when the status/code and message indicate the operation completed.

## Safety Notes

- Add/delete changes the user's account watchlist.
- Do not infer an add/delete action from vague wording like "关注一下" unless the user clearly means self-select/watchlist.
- Do not auto-delete multiple stocks from a broad instruction without explicit confirmation.
