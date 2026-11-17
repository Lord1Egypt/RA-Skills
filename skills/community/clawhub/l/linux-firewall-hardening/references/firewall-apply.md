# firewall-apply.sh

## Purpose

Applies a declarative firewall policy to the host in an idempotent, reversible manner. Builds a complete ruleset, swaps it in atomically via `iptables-restore` (per family), and supports automated rollback on failure.

## Inputs

| Input | Source | Required | Default | Notes |
|---|---|---|---|---|
| `--policy-dir <dir>` | CLI | No | `./policy.d` | Policy fragments applied in lexical order |
| `--approved-plan <token>` | CLI | **Yes** | — | Hash from `firewall-plan.sh --json`. Reject if missing/mismatch (exit 41) |
| `--dry-run` | CLI | No | off | Render + diff only; zero kernel changes |
| `--family <v4\|v6\|both>` | CLI | No | `both` | Which address families to apply |
| `POLICY_DIR` | env | No | `./policy.d` | Override policy directory |
| `LOG_LEVEL` | env | No | `info` | `debug` emits full generated ruleset |
| `LOCK_PATH` | env | No | `/run/fw.lock` | Advisory lock file |
| stdin | pipe | No | — | If policy piped, `POLICY_DIR` is ignored |

All inputs validated before any mutation. Unknown flags → exit code 2, zero changes.

## Idempotency Guarantees

- Running N times with same policy produces identical final ruleset (no duplicate rule accumulation)
- Builds complete ruleset in temp file, swaps via `iptables-restore` (atomic per family)
- IPv4 and IPv6 generated from same policy source → both families stay in sync
- No-op run (live state = desired state) makes zero kernel changes, exits 0
- `--dry-run` exits 0 when no diff, 10 when diff exists
- Advisory lock prevents interleaved concurrent invocations

## Exit Codes

| Code | Meaning | Changes Applied? | Operator Action |
|---|---|---|---|
| 0 | Success (applied or already OK) | Maybe | None |
| 2 | Usage / invalid argument | No | Fix invocation |
| 3 | Policy validation failed | No | Correct policy fragment |
| 4 | Lock acquisition failed | No | Retry after current run completes |
| 5 | Ruleset generation failed | No | Inspect logs; likely template/syntax error |
| 6 | Apply failed, rollback succeeded | No (reverted) | Investigate apply error; host on prior ruleset |
| 7 | Apply failed, rollback FAILED | Partial/unknown | **Manual intervention required** |
| 10 | `--dry-run`: drift detected | No | Review diff; re-run without `--dry-run` |
| 41 | Plan approval token missing/mismatch | No | Re-run PLAN to get current token |

Codes 0–5: pre-mutation, host untouched. Codes 6–7: live state may have been altered.

## Rollback Contract

1. Before applying, snapshots current live ruleset via `iptables-save` / `ip6tables-save` to `${BACKUP_DIR}/pre-apply-<timestamp>.{v4,v6}`
2. Swap is atomic per family. If IPv4 apply succeeds but IPv6 fails → restores IPv4 from snapshot before exiting. Host is never left in mixed-family state.
3. On apply failure:
   - Restore succeeds → exit 6, host on exact prior ruleset
   - Restore fails → exit 7. Snapshot paths printed to stderr. Operator restores manually: `iptables-restore < <snapshot>.v4`
4. Snapshots retained for `BACKUP_RETENTION` runs (default 10), pruned oldest-first. Failed-run snapshots exempt from pruning until manually cleared.
5. Script never deletes active ruleset without verified replacement. No window where host has no firewall loaded.

## Side Effects

- Creates `${BACKUP_DIR}/pre-apply-*.{v4,v6}` backup files
- Writes to `${LOCK_PATH}` advisory lock
- Modifies kernel netfilter state (iptables/ip6tables)
- May trigger systemd-run for auto-rollback timer
