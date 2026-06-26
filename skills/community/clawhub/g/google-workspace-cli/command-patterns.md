# Command Patterns - Google Workspace CLI

## Fast Discovery Loop

```bash
gws --help
gws drive --help
gws schema drive.files.list
```

Use this sequence before first use of an unfamiliar resource.

## Read-Only Patterns

```bash
# List latest Drive files
gws drive files list --params '{"pageSize": 10}'

# Read Gmail messages metadata
gws gmail users messages list --params '{"userId":"me","maxResults":20}'

# Get upcoming events
gws calendar events list --params '{"calendarId":"primary","maxResults":10}'
```

## Write Patterns with Safety

```bash
# Draft request first
gws chat spaces messages create \
  --params '{"parent":"spaces/AAA"}' \
  --json '{"text":"Deploy complete"}' \
  --dry-run

# Apply only after confirmation
gws chat spaces messages create \
  --params '{"parent":"spaces/AAA"}' \
  --json '{"text":"Deploy complete"}'
```

## Pagination and Extraction

```bash
gws drive files list --params '{"pageSize":100}' --page-all --page-limit 5 | jq -r '.files[]?.name'
```

Use bounded page limits to avoid runaway calls.

## Upload and Download

```bash
# Multipart upload
gws drive files create --json '{"name":"report.pdf"}' --upload ./report.pdf

# Binary output to file
gws drive files export --params '{"fileId":"FILE_ID","mimeType":"application/pdf"}' --output ./out.pdf
```
