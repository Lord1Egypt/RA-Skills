# Safety Level Reference

## Level Summary

| Level | Name | Philosophy | Messaging |
|-------|------|-----------|-----------|
| L1 | Draft & Organize | Do anything to YOUR stuff; nothing outbound | ❌ No |
| L2 | Draft & Collaborate | L1 + collaborative actions (comments, RSVP) | ❌ No |
| L3 | Full Write (No Admin) | Full ops + messaging; no dangerous admin | ✅ Yes |

## What Changes Between Levels

### L1 → L2 (adds collaborative actions)
- Calendar: `respond`, `propose-time` (RSVP)
- Drive/Docs comments: `create`, `update`, `delete`, `reply`
- Gmail settings: `vacation update`
- AppScript: `run`
- Classroom: `coursework create`, `announcements create`

### L2 → L3 (adds direct messaging + admin-lite)
- Gmail: `send`, `drafts send`, `track`
- Chat: `messages send`, `dm send`, `spaces create`
- Gmail settings: `sendas *`
- Classroom: `invitations create`, `guardian-invitations create`
- Aliases: `send`

### Blocked at ALL levels (L4 only)
- `gmail batch delete` (permanent delete)
- `gmail settings delegates *` (account delegation)
- `gmail settings forwarding *` (auto-forwarding)
- `gmail settings autoforward *` (auto-forward rules)
- `gmail settings watch *`

## YAML Profile Files
- `l1-draft.yaml` — L1 profile
- `l2-collaborate.yaml` — L2 profile
- `l3-standard.yaml` — L3 profile

## How It Works
These are compile-time safety profiles using gogcli PR #366 (`steipete/gogcli#366`).
Commands set to `false` in the YAML are **physically removed from the binary** at build time.
There is no runtime flag or env var to bypass — the code literally doesn't exist in the binary.

## Source
- PR: https://github.com/steipete/gogcli/pull/366
- Branch: `compile-time-safety-profiles`
- Gist (L1): https://gist.github.com/BrennerSpear/757e23d62af920c6e86630f2eab57dc9
