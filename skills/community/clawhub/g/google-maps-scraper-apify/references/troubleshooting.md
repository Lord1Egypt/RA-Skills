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
- a direct URL does not expose a reusable Google Maps payload

Try a simpler search, lower filters, or a more concrete location.

## Missing emails

Google Maps usually does not expose emails directly. Enable `scrapeCompanyContacts` to visit public business websites. Emails are still best-effort because some sites use forms, images, scripts, or blocking.

## Missing reviews or images

Review and image extraction is best-effort. Google Maps may expose fewer items than requested, especially for low-volume places or restricted listings.

## Run cost concerns

Use `--budget-usd` for the script or `maxTotalChargeUsd` in Apify run options. Keep tests small before scaling.
