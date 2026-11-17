# public_apis — Public APIs Directory

## What this source has

A collective directory of free public APIs for developers. Includes APIs for categories like Animals, Anime, Business, Cryptocurrency, Development, etc. Each entry includes API name, description, authentication requirement, HTTPS support, and CORS info.

Use public_apis to discover available APIs for integration, find specific category APIs, or get metadata about public APIs.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | no published cap; throttle to <1/sec to be respectful |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `entries` | List API entries, optionally filtered by category | `category` (optional) |
| `categories` | List all available categories | none |

## Worked examples

```bash
# Get all API entries (first 10 by default)
python3 scripts/reach.py query public_apis entries '{}'

# Get entries for the "Animals" category
python3 scripts/reach.py query public_apis entries '{"category": "Animals"}'

# Get list of all categories
python3 scripts/reach.py query public_apis categories '{}'
```

## Response shape

- `entries`: returns a JSON object with a `count` and `entries` array. Each entry has `API`, `Description`, `Auth`, `HTTPS`, `CORS`, `Link`, and `Category`.
- `categories`: returns a JSON object with a `count` and a list of category strings.

## Pitfalls

- The API does not require authentication but may rate limit if abused.
- Some listed APIs may have changed or become unavailable; always verify with the provider.
- The `category` filter is case-sensitive as provided by the directory.

## Source links

- Public APIs directory: https://github.com/public-apis/public-apis
- API endpoint: https://api.publicapis.org
