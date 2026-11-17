# Dispatch-wave closure: email-state file topology

Observed 2026-07-16 during a second-wave email closure (<operator> account, all `is_new:false`).

## The files

Under `commons/data/ocas-dispatch/`, email triage state is spread across MULTIPLE files, not one. A 2026-07-16 scan found seven:

| File | `account` field | `verified_second_wave` (pre-closure) |
|------|----------------|--------------------------------------|
| `last_email_check.json` | null | None |
| `last_email_check_<account-identity>_gmail_com.json` | null | None |
| `last_email_check_owner.json` | <user-google-email> | True |
| `owner/last_email_check.json` | null | True |
| `last_email_check_mx_indigo_karasu_gmail_com.json` | <agent-email> | True |
| `last_email_check_indigo.json` | <agent-email> | True |
| `indigo/last_email_check.json` | <agent-email> | False |

## What the verifier checks

`scripts/closure_closeout_check.py --named <rel> --date <DATE>` only inspects FOUR email-state files for its `[3]` gate:

- `last_email_check.json`
- `last_email_check_<account-identity>_gmail_com.json`
- `last_email_check_mx_indigo_karasu_gmail_com.json`
- `last_email_check_indigo.json`

It does NOT read the per-account dir files (`owner/`, `indigo/`) nor `last_email_check_owner.json`.

## Closure rule

When re-affirming `verified_second_wave=True` for a second-wave email set:

1. Glob ALL `last_email_check*.json` under `commons/data/ocas-dispatch/` (recursive).
2. Set `verified_second_wave=True` on every file that pertains to the affected account.
3. Key on path/filename, NOT the `account` field — it is frequently `null` (the account-mislabel pitfall). The `account` field cannot be trusted to identify the file's owner.

Do not rely on the verifier's 4-name subset; sweep all of them so state is consistently green.

## Caveat

`verified_second_wave` is defensive only. The monitor re-queues email waves regardless of the flag (documented `monitor_email.py` re-fire bug), so the TRUE anti-re-fire gate is (a) every journal registered in both eval stores and (b) `last_ingest_run` + `monitor journal_ingest_state.latest_mtime` advanced past max journal mtime. Re-affirming the flag is belt-and-suspenders, not the load-bearing fix.