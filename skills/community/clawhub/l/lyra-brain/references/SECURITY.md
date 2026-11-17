# lyra-brain — security (v2.1.0)

## Declared permissions

| Capability | Scope |
|------------|--------|
| Env | Read `LYRA_CORE_ROOT` / `LYRA_CORE` (directory path only) |
| Filesystem read | `$LYRA_CORE_ROOT/modules`, existing memory (for recall) |
| Filesystem write | `$LYRA_CORE_ROOT/memory/**` and grow graph — **only with `--i-consent`** |
| Network | **None** in skill scripts |
| Process spawn / shell | **None** |
| Publish (git/HF/ClawHub/social) | **Never** auto |

## Persistent storage warning

Using write CLIs stores session-derived text **on disk** under your `LYRA_CORE_ROOT`.  
That data remains until you delete it. Treat memory as a journal you own.

## Secrets

Never pass API keys, Discord tokens, wallet keys, or `moltx_sk_*` into:

- `brain_grow_cli.py`
- `session_log_snip.py --lines`

## Path safety

- Set `LYRA_CORE_ROOT` yourself to a tree you control.  
- Do not point grow at another user’s tree on a shared host without their consent.  
- v2.1.0 does **not** auto-scan arbitrary drive letters for `LYRA_CORE`.

## Consent

| Action | Flag |
|--------|------|
| Write snip / daily index / ref | `--i-consent` on `session_log_snip.py` |
| Grow graph | `--i-consent` on `brain_grow_cli.py` or on snip with `--grow` |
| Recall | read-only; no consent flag |

Agents must obtain **explicit user request** for persistent memory before invoking write CLIs.

## Disable / purge

1. Stop invoking write scripts.  
2. Delete or archive `$LYRA_CORE_ROOT/memory` and graph files as you choose.  
3. Unset `LYRA_CORE_ROOT` if you no longer want this machine path used.
