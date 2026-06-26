# Resource Detail Example

Use this example for resource-detail or configuration-detail endpoints that return a stable JSON payload.

## Best Fit

- detail pages
- feature switch lookup
- config lookup by identifier

## Required Variables

- `HOST`
- `RESOURCE_ID`
- `COOKIE`

## Run

```bash
bash -n './resource-detail.api-verify.sh'
COOKIE='full Cookie header' HOST='https://api.example.test' RESOURCE_ID='sample-123' bash './resource-detail.api-verify.sh'
```

## What To Check

- `data.status`
- `data.id`
- whether the missing resource case returns the expected marker
