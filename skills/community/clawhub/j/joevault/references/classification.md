# Classification guide

Use this when deciding whether a stale path should be quarantined immediately or left in place.

## Quarantine now

Good candidates:
- old `.openclaw` or `.claude` state directories
- stale cache directories
- old logs, completions, or ephemeral session state
- any path that is small, clearly inactive, and not referenced by current config

Checklist:
- not referenced by active config or workspace
- not a current symlink target
- small enough to move safely
- easy to reverse if needed

## Leave for inventory

Do not move blindly:
- large workspaces
- model directories
- training outputs
- voice or avatar assets
- media renders
- old repos with recent activity
- anything with unclear ownership

Checklist:
- get top-level sizes first
- check latest modified files
- decide whether it is reference, cold archive, or deletion candidate

## Keep active

Do not quarantine:
- current home directories
- current `.openclaw` or active config roots
- symlink targets in active use
- any path still referenced by services, scripts, or env files

## Archive naming

Prefer explicit, timestamped archive roots such as:

- `C:\Users\<user>\Archives\profile-switch-2026-03-31`
- `C:\Users\<user>\Archives\reset-cleanup-2026-03-31`

Inside the archive, use labels that explain what moved:

- `old-joe-openclaw`
- `old-claude-state`
- `legacy-agent-cache`

## Safety rule

If there is uncertainty, do not move the path yet. Inventory it first.
