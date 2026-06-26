# Verification

Use this checklist after creating or repairing the memory pipeline.

## Files and directories

Confirm these exist:

- `MEMORY.md`
- `memory/`
- `memory/inbox.md`
- `memory/projects/`
- `memory/system/`
- `memory/groups/`

## Cron presence

Confirm three cron jobs exist and are enabled:

1. hourly inbox → raw
2. daily summary
3. weekly long-term review

Use `verify_memory_pipeline.py` as a best-effort runtime check. It now checks not only cron names, but also whether each cron payload appears to reference the current workspace path. In slower environments, run it with either:

- `--cron-timeout-seconds 15`
- or `--skip-cron` if you only want to validate filesystem structure first

## Functional acceptance test

### Hourly pipeline

1. Add a test item under `memory/inbox.md` → `## pending`
2. Trigger the hourly job manually
3. Wait for the run to fully finish
4. Confirm:
   - `memory/YYYY-MM-DD-raw.md` now contains the item under the current hour section
   - `memory/inbox.md` pending is cleared or updated

### Daily pipeline

1. Ensure there is meaningful content from the current day
2. Trigger the daily job manually
3. Confirm `memory/YYYY-MM-DD.md` exists and contains a compact summary

### Weekly pipeline

1. Ensure recent daily notes exist
2. Trigger the weekly job manually
3. Confirm `MEMORY.md` is updated with durable information only

## Common failure patterns

### ‘Cron says ok but raw is still empty’
Possible causes:
- the job is still running and you checked too early
- pending was empty by the time you checked
- the prompt cleared inbox without writing due to flawed logic

### ‘Nothing ever reaches raw’
Possible causes:
- no one is writing high-value conversation items into `memory/inbox.md`
- the hourly job exists but reads the wrong source

### ‘MEMORY.md gets noisy’
Possible causes:
- weekly review is promoting daily noise instead of durable rules or preferences
- memory rules are missing or vague

## Success criteria

The pipeline is healthy when:

- new high-value context enters `memory/inbox.md`
- hourly archive moves it into `memory/YYYY-MM-DD-raw.md`
- daily summary condenses the day into `memory/YYYY-MM-DD.md`
- weekly review updates `MEMORY.md` with durable information only
