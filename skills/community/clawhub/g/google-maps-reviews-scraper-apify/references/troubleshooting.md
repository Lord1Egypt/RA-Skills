# Troubleshooting

## No reviews returned

Check:

- the source is an exact place URL, CID URL, review URL, or Place ID
- `maxReviews` is greater than `0`
- `reviewsStartDate` is not too restrictive
- `maxTotalChargeUsd` is high enough for the requested number of reviews

Broad search URLs are not expanded by this reviews-only actor.

## Reviewer data is missing

If `personalData=false`, reviewer fields are intentionally omitted or null. If `personalData=true`, Google may still omit profile details for some reviews.

## Dates are approximate

Google often returns relative dates like `3 months ago`. `publishedAtDate` is a best-effort normalized date.

## Budget stopped early

The actor respects Apify `maxTotalChargeUsd` and reduces or stops review saving when the available budget is exhausted. Check `RUN_SUMMARY`.

## Source-level errors

The actor is designed to suppress source errors into `RUN_SUMMARY` and finish successfully where possible. Inspect `RUN_SUMMARY` before rerunning.
