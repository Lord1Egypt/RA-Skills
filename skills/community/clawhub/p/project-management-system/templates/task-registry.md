# Task Check-in Table

> Prevent multiple executors in same project simultaneously doing same thing.
> Must check this table before starting execution, confirm no conflict then write claim record.
> Detailed rules see `system/docs/task-management.md` Task Claim Mechanism.

## Quick Reference Rules

- Check table before start → Write if no conflict → Update status after completion
- Default expiry time 2 hours, customizable
- After expiry others can take over (mark "Successor")
- Completed records can clean after 24 hours
- Status values: `Claiming` / `In Progress` / `Paused` / `Completed` / `Released`

## Check-in Table

| Task ID | Claimer | Status | Start time | Expire time | Output location | Notes |
|--------|--------|------|----------|----------|----------|------|
| _(None yet)_ | | | | | | |