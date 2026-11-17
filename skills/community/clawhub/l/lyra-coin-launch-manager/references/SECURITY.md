# SECURITY — lyra-coin-launch-manager v1.2.0

## Declared permissions

| Capability | Allowed |
|------------|---------|
| Filesystem write | `state/`, `reference/` under `--workspace` (or cwd) |
| Network | HTTPS GET: `clawn.ch`, `base.blockscout.com`, `api.dexscreener.com` |
| Process spawn / shell | **No** |
| GitHub tokens / git push / repo create | **No** (removed from skill package) |
| Wallet private keys | **Never** store in skill tree |

## Operator-only tools (not in ClawHub skill)

If present on steward disk under `operator_tools/`:

- `push_github_auto.py`
- `create_github_repo.ps1`
- `scan_for_secrets.py`

These are **not** part of this skill. Agents must not invoke them.

## Consent

- Writing receipts is expected; use dedicated workspace folders.  
- No auto-overwrite of unrelated project files outside `--workspace`.
