# List Assertions Example

Use this example for paged list APIs where the business check depends on whether a target element appears.

## Best Fit

- page-level list queries
- search results
- resource collections

## Required Variables

- `HOST`
- `AUTH_TOKEN`

## Run

```bash
bash -n './list-assertions.api-verify.sh'
HOST='https://api.example.test' AUTH_TOKEN='token value' bash './list-assertions.api-verify.sh'
```

## What To Check

- whether the projected list contains a required element
- whether a removed or forbidden element is absent
- whether page-level summary fields look correct
