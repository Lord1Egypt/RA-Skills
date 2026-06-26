# Execution Modes

## Manual

Required path:

1. `prepare --mode manual`
2. If `status=no_release`, reply that no formal release exists
3. If `status=has_updates`, summarize exactly the selected `releases[]`
4. Build `summaries[]`
5. `render --mode manual`
6. Reply with the rendered `message`

Do not:

- read or write state
- call `commit`
- analyze more than the selected latest formal release
- add workflow narration or extra preambles

## Cron

Required path:

1. `prepare --mode cron`
2. If `status=no_release` or `status=no_update`, reply exactly `NO_REPLY`
3. If `status=has_updates`, summarize exactly the selected `releases[]`
4. Keep `prepare` ordering
5. Build `summaries[]`
6. `render --mode cron`
7. Deliver the rendered `message`
8. After successful delivery, `commit`

Do not:

- skip `prepare`
- bypass `render`
- write processed state before delivery succeeds
- when `status=no_update` or `status=no_release`, reply exactly `NO_REPLY`
- emit progress narration, step labels, intermediate JSON, or any workflow text to the delivery target

## Cron prompt shape

Keep cron instructions short and mechanical. The useful constraints are:

- use this skill in cron mode
- run deterministic `prepare` first
- summarize only formal releases selected by `prepare`
- first run: latest only
- later runs: unprocessed only, ordered old to new
- no update: reply exactly `NO_REPLY`
- only emit the final rendered message
- after successful delivery, commit state
