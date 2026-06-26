# post-update-awareness

A ClawHub skill that makes your OpenClaw agent **read its own release notes** after an update.

## What it does

When OpenClaw is updated, the agent has no built-in mechanism to consume the release notes — so optional-dependency surprises (e.g. a new release expects `sharp` to be installed) are discovered the hard way: when an unrelated workflow fails, in front of someone you care about.

This skill closes that loop:

1. Detects a version change between current `openclaw -V` and a small per-profile JSON state file the skill maintains.
2. Fetches the CHANGELOG entry **pinned to the installed version's tag** (`v<version>`), not `main`. So the agent reads the changelog that matches what's actually running.
3. Distills the entry into three buckets the user actually cares about — new tools, breaking changes, optional native deps to verify.
4. Probes known-flaky native modules (`sharp`, `ffmpeg-static`, `node-pty`) to flag missing ones.
5. **Detects plugin version drift** — catches the case where the gateway is on `vNew` but an externalized npm-installed plugin (`@openclaw/whatsapp`, `@openclaw/discord`, etc.) is still on `vOld`.
6. **Verifies channel health** post-restart (`channels status`) and surfaces any `disconnected` / `unhealthy` / `degraded` channel.
7. **Surfaces config rewrites** when `plugins update` overwrites `openclaw.json`, including the path to the auto-saved `.bak`.
8. **Yields to the update-guard** when one is already watching the same transition, so the user isn't notified twice for the same bump.
9. Sends one brief surfaced message via the active channel, then — **only on confirmed delivery** — persists the new version so subsequent heartbeats stay quiet.

## What's new in 0.4.0

- **Strict read-only posture.** All mutation paths (offering to update drifted plugins, cleaning stale config entries) have been removed. This skill now only reads and notifies. For the mutation flow, see the companion skill **[post-update-maintenance](https://clawhub.ai/skills/post-update-maintenance)**, which is explicitly scoped for changes.
- This split was made in response to security scanner feedback flagging the previous combined behavior as scope-contradictory. Trust posture is now clear: this skill is safe to install and run on any heartbeat.

## What's new in 0.3.x

- **Profile-aware state file.** Multi-profile setups (`main` + `noura-moi` + …) no longer share a single state file, which was silencing the skill on profile B after surfacing on profile A.
- **Surface-then-persist ordering.** State is now written only after the channel acknowledges the message, with a retry cap. Channel blips no longer eat the notification.
- **Update-guard awareness.** When an external update-guard already announced the version change, the skill skips the redundant header and goes straight into the CHANGELOG distillation.
- **`scripts/resolve.sh`.** Stable resolver for callers outside the skill (safe-update wrappers, cron jobs) so they stop hardcoding install paths.
- **Broader changelog discovery.** `find-local-changelog.sh` now resolves pnpm, volta, nvm, and fnm global installs in addition to npm.

## Install

```bash
openclaw skills install post-update-awareness
```

Or via the ClawHub CLI:

```bash
clawhub install post-update-awareness
```

## When the skill triggers

- The user asks "what changed in this update?" or similar
- An update flow finishes (`openclaw update`, `openclaw plugins update`)
- `openclaw -V` returns a value different from the version on file

It does **not** run on every heartbeat — only on actual version transitions.

## What it does not do

- Apply updates (that's `openclaw update`)
- Update drifted plugins (that's `post-update-maintenance`)
- Modify configuration (that's `post-update-maintenance`)
- Install missing dependencies — only flags them
- Roll back versions (that's your update-guard)
- Restart the gateway

This skill is **strictly read-only**. If you want the issues it surfaces to be acted on automatically, install **[post-update-maintenance](https://clawhub.ai/skills/post-update-maintenance)** — a separate skill that takes the diagnostics from this one and runs the corresponding mutations with explicit user confirmation.

## Files

- `SKILL.md` — the skill instructions the agent reads
- `scripts/find-local-changelog.sh` — locates the bundled CHANGELOG.md if available (npm / pnpm / volta / nvm / fnm)
- `scripts/probe-optional-dep.sh` — non-blocking native-dep loadability check
- `scripts/check-plugin-drift.sh` — lists externalized plugins whose installed version doesn't match the gateway
- `scripts/resolve.sh` — stable resolver for callers outside the skill (safe-update wrappers, cron, CI)

## Feedback / issues

Found a bug? An install layout the resolver misses? A CHANGELOG section the
distillation flattened poorly? Open an issue on the source repo and tag it
`post-update-awareness`. There's no in-band telemetry — the only signal the
author gets is what users say out loud.

If you're building on top of this skill (custom wrapper, alternative
notification surface, profile-specific filters), the resolver in
`scripts/resolve.sh` is the supported integration point. Patterns and edge
cases welcome.

## Why a skill rather than core

OpenClaw's project direction (per `VISION.md`) is that new skills publish through ClawHub first; bundled promotion happens later if a clear product, security, or maintainer-ownership reason emerges. This is that ClawHub-first version of the idea.

## Privacy

The skill reads:
- `openclaw -V` (local CLI output)
- The pinned CHANGELOG via `raw.githubusercontent.com` (one HTTPS request per detected version change, no auth, no telemetry)

Nothing is sent anywhere else. The local state file lives under one of:

- `$OPENCLAW_PROFILE_DIR/state/` when the runtime exports it
- `~/.openclaw-<profile>/state/` for multi-profile installs
- `~/.openclaw/state/` for the default single-profile case

and contains only the version string, a timestamp, and the profile name.

## License

MIT-0 — free to use, modify, redistribute. No attribution required.
