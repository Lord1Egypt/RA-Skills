---
name: hkipo-profile-watchlist-manager
description: Manage Hong Kong IPO user preferences and watchlists, including risk profile, default output, budget, financing preference, and tracked symbols. Use when the user wants personalized HK IPO settings or a maintained watchlist for later batch decisions.
version: 0.1.0
metadata: {"openclaw":{"emoji":"👤","requires":{"bins":["uv"],"config":["~/.hkipo-next/config/profile.json","~/.hkipo-next/config/watchlist.json"]},"install":[{"id":"install-uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv with Homebrew","os":["darwin","linux"]}]}}
---

# HK IPO Profile and Watchlist Manager

Use this skill for stateful personalization.

## Runtime

This publish bundle includes the required CLI runtime under `runtime/hkipo-next`.

From the skill folder:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next ...
```

By default the CLI stores profile and watchlist state under `~/.hkipo-next`. Read current state before changing it.

## Workflow

1. Use `profile show` before `profile set` when current state matters.
2. Update only the fields the user asked to change.
3. Batch multiple symbol additions or removals in one watchlist command.
4. Use `--format json` if another skill will consume the result.

## Commands

Show the effective profile:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next profile show --format json
```

Set profile fields:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next profile set \
  --risk-profile balanced \
  --default-output-format markdown \
  --max-budget-hkd 80000 \
  --financing-preference auto \
  --format json
```

List the watchlist:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next watchlist list --format json
```

Add symbols:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next watchlist add 2476 2613 --format json
```

Remove symbols:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next watchlist remove 2476 --format json
```

## Output Cues

- `profile.sources` explains where each effective field came from.
- `watchlist.changed_symbols` is the authoritative mutation result.
- `watchlist.symbols` is the final normalized state after the operation.

## Companion Skills

- Use `$hkipo-decision-engine` for `batch --watchlist`.
- Use `$hkipo-parameter-manager` when the user wants personalized score tuning.
