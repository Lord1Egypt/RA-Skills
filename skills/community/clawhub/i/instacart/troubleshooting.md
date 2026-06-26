# Troubleshooting - Instacart

## 400 Errors

Likely causes:
- missing required fields
- invalid measurement quantity
- invalid health filters
- `product_ids` and `upcs` both present on one item
- duplicate product ids or UPCs across items

Action:
- inspect the error key path
- fix payload structure locally
- retry only after the payload is corrected

## 401 or 403

Likely causes:
- wrong API key
- wrong environment
- insufficient key permission or endpoint access
- production key still pending review

Action:
- verify the key source
- verify dev vs prod host
- check approval and permission status in the dashboard

## Weak Product Matches

Common causes:
- product name includes brand, size, and diet text all together
- unsupported or vague units
- filter spelling does not match Instacart expectations
- poor UPC quality

Action:
- simplify `name`
- move brand and health intent to filters
- use supported units
- test fewer constraints first, then add specificity

## No Good Retailers

Common causes:
- wrong postal code or country
- market with low assortment coverage
- assuming retailer lookup equals ingredient coverage

Action:
- re-run nearby retailer lookup
- confirm `country_code`
- compare multiple markets if the user operates in more than one region

## Retry Policy

Retry only for transient conditions such as:
- `429`
- `5xx`
- obvious network transport failures

Use exponential backoff. Do not blindly retry payload-validation failures.

## Launch and Messaging Issues

If production or public messaging is blocked:
- check approval status first
- confirm the production key is active
- review Instacart messaging and trademark requirements before changing copy or logos
