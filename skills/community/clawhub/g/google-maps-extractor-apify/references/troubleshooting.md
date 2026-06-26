# Troubleshooting

## Apify token missing

Set:

```bash
export APIFY_TOKEN='apify_api_xxx'
```

or pass:

```bash
--apify-token 'apify_api_xxx'
```

## Zero rows returned

The actor may finish successfully with zero rows when:

- the search term and location are too narrow
- the location is misspelled or ambiguous
- filters removed all places
- a direct Google Maps URL does not expose a reusable place payload
- `maxTotalChargeUsd` is too low for saved output

Try a broader search term, a concrete city or postal code, lower filters, or a larger budget.

## Missing emails or social links

Google Maps usually does not expose emails directly. Enable `scrapeContacts` to visit public business websites. Emails and social links are still best-effort because some websites use forms, scripts, images, login gates, or blocking.

## Missing opening hours or details

Enable `scrapePlaceDetailPage` when the user needs richer place details. Some places still omit fields because Google Maps does not expose them publicly.

## Budget stopped early

Use `--budget-usd` in the runner or `maxTotalChargeUsd` in Apify run options. The actor respects the run budget and may reduce the target before scraping. Check `RUN_SUMMARY` for `datasetItemBudget`.

## Source-level errors

The actor is designed to suppress source and input errors into dataset items and `RUN_SUMMARY` where possible, then finish successfully. Inspect the default key-value store `RUN_SUMMARY` before rerunning.
