# Command templates

This file contains copy/paste-friendly templates for each `parallel-cli` capability.

## Naming outputs

Use a short slug for filenames: lowercase, hyphens, no spaces. Examples:
- `ai-chip-news-2026`
- `ev-battery-report`
- `company-enrichment`

## Search

Simple:

```bash
parallel-cli search "$OBJECTIVE" --json
```

Objective + keyword probes + constraints:

```bash
parallel-cli search "$OBJECTIVE"   --mode agentic   --max-results 10   --after-date 2026-01-01   --include-domains docs.vendor.com github.com   -q "exact error message"   -q "product name release notes"   --json
```

## Extract

Basic:

```bash
parallel-cli extract "$URL" --json
```

With focus:

```bash
parallel-cli extract "$URL" --objective "Find pricing + plan limits" --json
```

Full content:

```bash
parallel-cli extract "$URL" --full-content --json
```

## Research (deep reports)

Start async:

```bash
parallel-cli research run "$QUESTION" --processor pro-fast --no-wait --json
```

Poll to files:

```bash
parallel-cli research poll "$RUN_ID" -o "/tmp/$SLUG" --timeout 540
```

## Enrich

Suggest schema:

```bash
parallel-cli enrich suggest "$INTENT" --json
```

Plan a YAML config (requires `parallel-web-tools[cli]` install):

```bash
parallel-cli enrich plan -o config.yaml   --source-type csv   --source input.csv   --target /tmp/enriched.csv   --source-columns '[{"name":"company","description":"Company name"}]'   --intent "$INTENT"
```

Run a YAML config async:

```bash
parallel-cli enrich run config.yaml --no-wait --json
parallel-cli enrich poll "$TASKGROUP_ID" --timeout 540 --json
```

## FindAll

Dry run (preview schema):

```bash
parallel-cli findall run "$OBJECTIVE" --dry-run --json
```

Run async:

```bash
parallel-cli findall run "$OBJECTIVE" --generator core --match-limit 25 --no-wait --json
```

Poll + fetch results:

```bash
parallel-cli findall status "$RUN_ID" --json
parallel-cli findall poll "$RUN_ID" --json
parallel-cli findall result "$RUN_ID" --json
```

Cancel:

```bash
parallel-cli findall cancel "$RUN_ID"
```

## Monitor

Create:

```bash
parallel-cli monitor create "$OBJECTIVE" --cadence daily --json
```

With webhook:

```bash
parallel-cli monitor create "$OBJECTIVE"   --cadence hourly   --webhook "https://example.com/hook"   --json
```

Events:

```bash
parallel-cli monitor events "$MONITOR_ID" --json
```

Simulate:

```bash
parallel-cli monitor simulate "$MONITOR_ID" --json
```
