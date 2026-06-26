---
name: openai-codex-multi-oauth
description: Manage and debug multiple OpenAI Codex OAuth profiles inside OpenClaw, including native multi-profile auth stores and external-router setups where one active slot is backed by a repository of multiple OAuth identities. Use when fixing Codex profile switching, session `authProfileOverride` sync, `/status` or usage mismatches, auth.order behavior, active-slot routing, broken-token recovery, or same-email different-account/workspace selection bugs.
---

# OpenAI Codex Multi OAuth

Support and debug more than one `openai-codex` OAuth login inside OpenClaw.

## Human-facing overview

This skill is also meant to help a human operator understand the setup, not only help an agent patch code.

What humans usually want to know:

- which Codex profile the current chat is using
- whether the current chat has its own pinned profile override
- whether OpenClaw auto-switched after rate limits
- whether `/status` usage matches the profile they expected
- why two profiles may look similar even when they should stay distinct

Common user-facing surfaces in real deployments:

- `/status` — confirm the current chat's selected model, profile semantics, and usage summary
- `/codex_profile` — an optional helper command in some setups for viewing or switching the current Codex profile
- `/codex_usage` — an optional helper command in some setups for comparing live usage across profiles

Treat `/codex_profile` and `/codex_usage` as common patterns, not guaranteed OpenClaw built-ins.

## Start here

1. Run `python3 scripts/summarize_codex_profiles.py`.
2. If usage is involved, also run `python3 scripts/codex_usage_report.py`.
3. Classify the bug before patching anything.
4. Change the smallest wrong layer.
5. Re-test after every change.

If the target setup includes a local helper command or router script, reproduce through that real entrypoint at least once. Synthetic env-injected tests can miss session-sync bugs.

## Mental model

Treat these as separate layers:

- **stored preference** — any saved local pointer such as `codex_profile_id`
- **auth order** — `order.openai-codex` in the auth store
- **session override** — `authProfileOverride` for the current chat/session
- **effective runtime profile** — the profile that actually handled the request after selection or failover
- **usage source** — the token/accountId used by usage-fetch logic
- **display metadata** — the label shown to the user, such as email/workspace
- **optional external profile repo** — a separate file or store that keeps multiple Codex OAuth identities while runtime uses one active slot

Do not assume these layers always match.

## Common architectures

### A. Native auth-store setup

OpenClaw stores multiple `openai-codex:*` profiles directly in `auth-profiles.json`, and runtime resolves selection from auth order plus session override.

### B. External-router setup

A local repo of Codex OAuth identities exists outside normal runtime selection, and a helper/router copies one selected profile into an active slot such as `openai-codex:default`.

In that design, verify all of these separately:
- repo profile selected by the router
- active slot content after routing
- current session `authProfileOverride`
- `/status` oauth label
- `/status` usage source

## Decision tree

### 1) The wrong account is selected

Check in this order:
1. stored preference or helper-selected profile
2. `order.openai-codex`
3. session `authProfileOverride`
4. effective runtime profile
5. whether failover is expected or a bug

### 2) `/codex_profile`-style helper switches profile, but `/status` does not follow

Check:
1. whether the helper changed only the active slot or also the current session override
2. whether the current chat/session was correctly identified
3. whether the environment that invokes the helper is missing chat/session metadata
4. whether the platform keeps companion session entries that also need syncing

If the helper is real, re-test through the real command path, not only manual edits.

### 3) `/status` oauth changes, but usage does not

Check:
1. current session `authProfileOverride`
2. the effective runtime profile for the current chat
3. whether the usage loader resolves auth from generic provider order instead of the current session profile
4. whether the UI is mixing preferred-profile and effective-profile semantics
5. whether the usage fetch hard-pins the exact inspected profile or only passes a soft preference

### 4) Two profiles show the same usage unexpectedly

Check:
1. whether they share the same `accountId` because they are in the same team workspace
2. whether `user_id` is still different in the live `wham/usage` response
3. whether the local code accidentally fetched usage with the wrong token because provider-order fallback overrode the intended profile
4. whether the same-looking result was intermittent, which usually points to local selection/fallback bugs rather than backend quota semantics

### 5) A profile works sometimes but not always

Check:
1. cooldown / last-good logic
2. token expiry
3. soft-pin vs hard-pin semantics
4. whether failover is expected behavior or a bug

### 5) A token or profile entry is broken

Check:
1. whether the same `accountId` exists in another store or backup
2. whether only one profile entry can be restored surgically
3. whether local token parsing fails before request dispatch

### 6) `/status`, display labels, and runtime truth disagree

Decide which semantic each surface should represent:
- preferred profile
- effective runtime profile
- usage source profile
- display metadata label

Then verify every layer against that semantic before patching.

## Stable design rules

- Prefer profile identity by `accountId` before email when possible.
- Preserve different workspaces/accounts as separate profiles even when email matches.
- Keep profile ids stable, for example:
  - `openai-codex:default`
  - `openai-codex:secondary`
  - `openai-codex:tertiary`
  - `openai-codex:account-N`
- Do not blur preferred profile, effective runtime profile, and usage source profile.
- Hard-pin the exact profile credential when implementing per-profile usage inspection; a provider-level preference is not always a guarantee.
- A Telegram menu entry alone does not create a real executable command. Wire any `/codex_usage`-style surface into the actual command handler path.
- If an external repo exists, treat it as a separate layer instead of silently merging it into runtime state.

## Validation checklist

After each change, verify all of these:

1. stored preference or helper-selected profile is what you expect
2. auth order is what you expect
3. current session `authProfileOverride` is what you expect
4. runtime actually uses the intended profile
5. `/status` shows the intended semantic
6. usage matches the intended semantic, or the difference is explicitly understood
7. any helper command resolves the same profile id the runtime is using

## Common operator examples

Use examples like these when explaining the setup to a human:

- "Use `/codex_profile` to inspect or switch the profile for this chat if your deployment exposes that helper."
- "Use `/status` to confirm which profile the current chat prefers and whether usage looks aligned."
- "If a `/codex_usage` helper exists, compare profiles directly when usage looks suspicious."
- "If OpenClaw auto-rotated after rate limits, explain that the runtime may have switched profiles even if the user did not do it manually."

When documenting commands, always say whether they are:

- built into OpenClaw
- local helper commands added by a specific deployment
- examples that another operator may need to adapt

## Bundled resources

- Read `references/runtime-files.md` for the file families that usually matter.
- Read `references/workflows.md` for concrete repair workflows and rollback points.
- Read `references/usage-debugging.md` when the bug involves usage mismatches, same-workspace confusion, or a new `/codex_usage`-style command.
- Run `scripts/summarize_codex_profiles.py` before and after changes.
- Run `scripts/codex_usage_report.py` when you need exact per-profile live usage evidence.

## Guardrails

- Back up auth files or runtime bundles before editing them.
- Prefer surgical patches over broad rewrites.
- Keep version-specific assumptions explicit.
- Do not restart the gateway unless the user asked.
- Commit workspace skill changes after edits.
