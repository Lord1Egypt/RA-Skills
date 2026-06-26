# Troubleshooting

## No email leads returned

Check:

- the search term and location are specific enough
- `website` is set to `withWebsite` or the source places actually have websites
- `contactResultMode` is `emailsOnly` when email leads are required
- `maxCrawledPlacesPerSearch` is greater than `0`
- `maxTotalChargeUsd` is high enough for the requested saved leads
- `contactPagesLimit` is high enough for the niche

Some businesses publish only contact forms, booking widgets, or social profiles instead of direct emails.

## Fewer leads than requested

This can happen when the area has fewer matching businesses with public emails, when filters are too strict, or when the run budget is reached. Inspect `RUN_SUMMARY`.

## Personal emails are missing

If `includePersonalData=false`, person-like emails and personal LinkedIn profile URLs are intentionally excluded. If it is true, the business website still may not publish personal contacts.

## Results include phones or social links but no email

This is expected in `contactsOnly` or `allPlaces`. Use `emailsOnly` when the dataset should contain only email leads.

## Budget stopped early

The actor respects Apify `maxTotalChargeUsd`. The script passes this as `--budget-usd`. Check `RUN_SUMMARY.datasetItemBudget`.

## Source-level errors

The actor is designed to suppress individual place or website errors into `RUN_SUMMARY` and finish successfully where possible. Inspect `RUN_SUMMARY` before rerunning.
