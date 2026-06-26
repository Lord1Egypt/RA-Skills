---
name: openclaw-openai-multi-account
description: Manage multiple OpenAI OAuth login accounts inside OpenClaw, including OpenAI Codex OAuth account snapshots, switching, real active-account detection, 5-hour and weekly quota inspection via Codex CLI cache, ACTIVE metadata repair, auto-enrollment of newly logged-in accounts, same-model auto-rotation near exhaustion, and fallback to a backup model such as Bailian when all OpenAI accounts are unavailable. Use when the user asks about multiple OpenAI OAuth accounts in OpenClaw, OpenAI/Codex account switching, the current real active account, local saved accounts, 5h or weekly remaining quota, OAuth re-login, automatic account rotation, or fallback behavior in OpenClaw.
---

# OpenClaw OpenAI Account Switcher

Use this skill for **multiple OpenAI OAuth login accounts managed inside OpenClaw**, especially OpenClaw's own `openai-codex` OAuth accounts, not just plain Codex CLI account files.

## What this skill does

- Save the current OpenClaw `openai-codex:default` OAuth profile as a named snapshot
- Add a new account by running `openclaw models auth login --provider openai-codex`
- Switch all agents to a named snapshot
- Show the current active account (email/account id when available)
- Show cached/observed **5-hour** and **weekly** usage when quota data can be collected
- Auto-switch to the account with remaining quota
- Fall back to a backup model when all accounts are exhausted

## Files

- Main script: `scripts/openclaw-openai-accounts.py`
- Regression test script: `scripts/test_openclaw_openai_accounts.py`
- State store: `~/.openclaw/openai-codex-accounts/`

Run the bundled regression suite with:

```bash
python3 scripts/test_openclaw_openai_accounts.py
```

Daily local check command:

```bash
/home/djy/.openclaw/workspace-taizi/bin/check-openai-multi-account
```

It writes timestamped logs under:

- `/home/djy/.openclaw/workspace-taizi/data/openai-multi-account-checks/`

## First use

List current snapshots:

```bash
python3 scripts/openclaw-openai-accounts.py list
```

> `list`, `add`, `use`, `auto`, and `cron-check` all reconcile the **current live OpenClaw login** back into the saved account list before reporting or switching, so out-of-band `openclaw models auth login --provider openai-codex` changes are picked up automatically.
>
> The same reconciliation also keeps related OpenClaw auth metadata in sync:
>
> - add missing `auth.profiles` email aliases in `openclaw.json`
> - keep `auth.order.openai-codex` aligned with the saved account list and current active account
> - add/remove matching named email profiles in each agent `auth-profiles.json`
> - prune stale aliases that no longer correspond to any saved account

Probe real quota via Codex CLI and show it in the list:

```bash
python3 scripts/openclaw-openai-accounts.py list --verbose --probe
```

Add an account (interactive OAuth login):

```bash
python3 scripts/openclaw-openai-accounts.py add --name work
```

Switch account:

```bash
python3 scripts/openclaw-openai-accounts.py use work
```

Auto-pick best account or fall back:

```bash
python3 scripts/openclaw-openai-accounts.py auto
```

Auto-check mode for cron/systemd (single-line notification-friendly output):

```bash
python3 scripts/openclaw-openai-accounts.py cron-check
```

## Important behavior

### 1. Canonical auth source

This skill treats OpenClaw agent auth files as the source of truth:

- `~/.openclaw/agents/<agent>/agent/auth-profiles.json`

It updates **all configured agents** to keep `openai-codex:default` aligned.

### 2. Quota collection

Quota collection works in two modes:

- **Preferred**: if a matching Codex CLI account snapshot exists and `codex` is installed, collect real 5-hour / weekly rate-limit data
- **Fallback**: if no Codex CLI snapshot exists, keep local observations and report that quota is unknown

### 3. Fallback model

Default backup model is:

- `bailian/qwen3.5-plus`

You can also override defaults via environment variables:

- `OPENCLAW_HOME` — OpenClaw data root (default `~/.openclaw`)
- `OPENCLAW_PRIMARY_AGENT` — canonical agent whose auth file is treated as the real active auth (default `taizi`)
- `OPENCLAW_FALLBACK_MODEL` — backup model to use when all OpenAI accounts are exhausted (default `bailian/qwen3.5-plus`)

Override it with:

```bash
python3 scripts/openclaw-openai-accounts.py auto --fallback-model bailian/glm-5
```

### 4. Automatic checks

Run periodically with cron/systemd/loop. Example one-shot command:

```bash
python3 scripts/openclaw-openai-accounts.py auto --json
```

A good interval is every 10-15 minutes.

For unattended auto-switching, prefer a two-stage threshold with a short inactivity guard. The bundled script now supports:

```bash
python3 scripts/openclaw-openai-accounts.py auto --five-hour-switch-at 80 --five-hour-hard-switch-at 90 --weekly-switch-at 90 --weekly-hard-switch-at 95 --inactive-minutes 3
python3 scripts/openclaw-openai-accounts.py cron-check --five-hour-switch-at 80 --five-hour-hard-switch-at 90 --weekly-switch-at 90 --weekly-hard-switch-at 95 --inactive-minutes 3
```

This means:

- when 5-hour usage reaches **80%** (about 20% left), attempt switching only if no non-cron session across configured agents has been active within the last **3 minutes**
- when 5-hour usage reaches **90%** (about 10% left), switch **immediately** to avoid hitting rate limits, even if sessions are active
- when weekly usage reaches **90%** (about 10% left for the week), attempt switching only if no non-cron session across configured agents has been active within the last **3 minutes**
- when weekly usage reaches **95%** (about 5% left for the week), switch **immediately** to preserve the remaining weekly quota

## Recommended policy

Use this policy by default:

- Check every 10 minutes
- At 5-hour usage **80%**: try switching only when all non-cron sessions have been inactive for 3 minutes
- At 5-hour usage **90%**: switch immediately to avoid rate limits
- At weekly usage **90%**: try switching only when all non-cron sessions have been inactive for 3 minutes
- At weekly usage **95%**: switch immediately to preserve the remaining weekly quota
- Prefer staying on the current account if it is still under both soft thresholds
- Prefer same-model account rotation (`openai-codex/gpt-5.4` → another `openai-codex/gpt-5.4` account)
- Fall back to a backup model only when all accounts are above threshold or quota is unknown

Default thresholds in the script:

- 5-hour soft switch threshold: `80%`
- 5-hour hard switch threshold: `90%`
- weekly soft switch threshold: `90%`
- weekly hard switch threshold: `95%`
- inactivity guard: `3` minutes

## Recommended workflow

1. Add at least two accounts
2. Run `list --verbose` to verify identities
3. Run `auto` to validate selection logic
4. When the user wants automation, schedule `auto` periodically
5. When switching happens, report:
   - active account name
   - email
   - 5-hour usage
   - weekly usage
   - current primary model / fallback model

## Health states

The script now distinguishes these states:

- `healthy`: token works and rate limits were read successfully
- `auth-invalid`: token/refresh/login is invalid and the account should be re-logged-in
- `plan-unavailable`: token exists but the workspace/plan/model is not usable
- `quota-unknown`: quota could not be determined yet

These states appear in `list --verbose` and `status`.

## Important implementation note

After inspecting OpenClaw source (`/tmp/openclaw/src/commands/models/auth.ts` and `/tmp/openclaw/src/commands/onboard-auth.credentials.ts`) plus live runtime files, the built-in `openclaw models auth login --provider openai-codex` has these practical semantics:

1. the live credential is used via `openai-codex:default`
2. switching accounts writes the new token into `openai-codex:default`
3. email-specific profiles such as `openai-codex:user@example.com` are kept as named records
4. sibling agent auth stores are synced together
5. existing `usageStats` and `lastGood` are preserved instead of being cleared

This skill now mirrors that model:

- real active-account detection keys off the live `openai-codex:default` credential
- snapshots keep a stable email-based identity instead of relying on ambiguous `:default`
- switching rewrites `:default` across all agents while also retaining/upserting the email-specific profile entry
- metadata migration repairs older snapshot records that incorrectly treated `:default` as a unique account id
- **email is the canonical human identity** for deduplication; `accountId` may change when the same email moves to a different workspace/team, so same-email re-logins update the existing saved account instead of creating a duplicate

## Notes

- This skill stores sensitive OAuth tokens under `~/.openclaw/openai-codex-accounts/`
- Treat those files like credentials
- Prefer `list --verbose` or `status` before making risky changes
- Active account display is derived from the real OpenClaw auth file (`~/.openclaw/agents/<agent>/agent/auth-profiles.json`), then synced back into skill metadata. This avoids stale `ACTIVE` markers after manual `openclaw models auth login` or other out-of-band auth changes.
- During periodic checks, if the real current OpenClaw auth is not present in the list yet, the skill will auto-enroll it as a new `accountN` snapshot and mark it active.
