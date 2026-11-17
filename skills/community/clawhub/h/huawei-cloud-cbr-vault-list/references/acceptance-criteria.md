# Acceptance Criteria

| # | Criterion | How it is met | Verification |
| --- | --- | --- | --- |
| 1 | Query vaults in a specified region | `--region` (default `cn-north-4`); `hcloud CBR ListVault --cli-region=<region>` | live CLI research + unit tests |
| 2 | Output includes name / ID / status / capacity / charging mode | default full-field table flattens `billing` (`status`, `size`, `used`, `allocated`, `charging_mode`, ...) to first-class columns | `render_table` / `normalize_vault` tests |
| 3 | `--json` returns the raw array | prints the parsed `vaults` array unchanged | `test_json_mode` |
| 4 | name / status / object_type / protect_type / enterprise_project_id / vault_id filters work | native server-side parameters + client-side re-filter | `FilterTests` + `BuildCommandTests` |
| 5 | Paging does not repeat or skip rows | count-aware `offset` paging, full-page fallback, duplicate-ID guard, max 100 pages | `PagingTests` |
| 6 | Empty / 403 / missing AK-SK / missing hcloud / API error have clear messages and exit codes | explicit hints, exit 1 on error, exit 0 on empty | `FailureClassificationTests` + `MainTests` |
| 7 | Write intent is blocked | `guard_write_intent` + `guard_operation` before any command | `GuardTests` |
| 8 | `python3 -m unittest discover -s tests -v` is green | 49 offline unit tests | test run |
| 9 | SKILL.md conforms to 华为云Skill检查规范 | creator `validate-skill.sh` zero FAIL | structure validation |
| 10 | Read-only only (no paid / destructive operations) | only `ListVault` GET can be emitted; no create/delete/update path | guard + code review |

## Out of scope (intentionally not implemented)

- Listing individual backups (separate concern).
- Vault quota / usage summary statistics.
- Any mutating vault action (create / delete / update / bind policy / migrate)
  or backup restore / copy — requires a write-capable skill and explicit user
  confirmation.