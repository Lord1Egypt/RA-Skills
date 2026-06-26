# Admirarr — Agent Reference

Use `admirarr` as the sole interface. Never bypass with raw API calls, curl, or Docker commands.

## Commands

```bash
# Status
admirarr status [-o json] [--live]     admirarr health [-o json]
admirarr disk [-o json]                admirarr docker [-o json]

# Library
admirarr movies [-o json]              admirarr shows [-o json]
admirarr recent [-o json]              admirarr history [-o json]
admirarr missing [-o json]             admirarr requests [-o json]

# Search & Add
admirarr search "<q>" [-o json]        admirarr find "<q>" [-o json]
admirarr add-movie "<q>"               admirarr add-show "<q>"

# Downloads
admirarr downloads [-o json]           admirarr queue [-o json]
admirarr downloads pause [hash|all]    admirarr downloads resume [hash|all]
admirarr downloads remove <hash> [--delete-files]

# Indexers
admirarr indexers [-o json]            admirarr indexers test
admirarr indexers setup                admirarr indexers sync
admirarr indexers add <name>           admirarr indexers remove <name>

# Quality
admirarr recyclarr                     admirarr recyclarr sync [instance]
admirarr recyclarr verify              admirarr recyclarr instances

# Management
admirarr scan                          admirarr restart <service>
admirarr logs <service>

# Diagnostics
admirarr doctor [-o json]              admirarr doctor --fix

# Stack
admirarr setup                         admirarr migrate
```

## Patterns

| Goal | Commands |
|---|---|
| Understand stack state | `status` → `doctor` → `health` |
| Fix an issue | `doctor -o json` → identify → `restart` / fix → `doctor` again |
| Add content | `movies -o json` (check exists) → `add-movie` → `downloads` → `queue` |
| Stuck downloads | `downloads -o json` → `queue -o json` → `health` → `doctor` |
| Missing content | `missing -o json` → `requests -o json` |

## Rules

- `-o json` for structured output when parsing
- Confirm with user before `restart` or `setup`
- Never delete user files or media
- Never modify *Arr databases directly
- `setup` is idempotent — safe to re-run
