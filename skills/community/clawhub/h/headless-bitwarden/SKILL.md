---
name: headless-bitwarden
description: "Extension for Bitwarden usage: adds an ephemeral HTTPS web unlock helper for rbw (TTL default 10m) so you can unlock remotely without pasting secrets into chat."
---

# Headless Bitwarden (rbw) — Skill (addon)

Goal: safely retrieve secrets from Bitwarden **without** pasting passwords/tokens into chat.

This skill is intentionally **small and non-overlapping**:
- Use the existing **Bitwarden** skill for installation / account setup.
- This skill only adds an **ephemeral remote unlock web helper** for `rbw`.

This skill standardizes a workflow around:
- `rbw` (local encrypted cache + unlock)
- an **ephemeral unlock web helper** that you can start on-demand and shut down automatically.

## Core rules (must)

1) **Never paste secrets into chat**
- No master password, no session keys, no JSON secrets.

2) **Ephemeral by default**
- Unlock helper must be **localhost-only**, **token-gated**, and **auto-expire**.
- Default TTL: **600s (10 minutes)**.

3) **No secret logging / no secret persistence**
- Do not log request bodies.
- Do not write secrets to disk.

4) **Always restore rbw config**
- If a temporary `pinentry` override is used, it must be restored even on failure.

## Prereqs

1) Follow the workspace Bitwarden skill for setup (install, register/login):
- `skills/bitwarden/SKILL.md`

2) Additional requirements for the unlock helper:
- `rbw` installed and registered/logged-in (device approved)
- `node` available
- `bash`
- Optional (recommended for remote): `cloudflared` (for an ephemeral HTTPS URL)

## Fast paths

### A) If the vault is already unlocked

```bash
rbw unlocked
rbw sync
rbw search "<keyword>"
rbw get "<item name>" --field "<field name>"
```

### B) If the vault is locked: start the ephemeral web unlock helper

From your workspace:

```bash
TTL_SECONDS=600 SYNC_AFTER_UNLOCK=1 \
  skills/headless-bitwarden/scripts/rbw-remote-unlock/start.sh
```

You will see:
- `Local URL: http://127.0.0.1:<port>/<token>/`
- If `cloudflared` exists: a `Public URL: https://<random>.../<token>/`

Open the **Public URL** on your phone/laptop, enter the master password, and press **Unlock**.
The helper will:
- run `rbw unlock`
- respond to the browser as soon as `rbw unlock` finishes
- optionally run `rbw sync` **after** the browser response (so the page shouldn’t spin)
- **exit immediately on success** (or auto-exit on TTL)

## Security notes (residual risk, be explicit)

Even with HTTPS tunnel and no logs, this is not “zero risk”. Remaining risks include:
- password exists briefly in **process memory**
- password is passed briefly to a child process via **env** (in same-user scope)
- token URL leakage during TTL would allow access to the form
- tunnel provider is within the trust boundary (even though traffic is HTTPS)

Mitigations implemented:
- localhost bind only (`127.0.0.1`)
- high-entropy path token
- request body size limit
- no request-body logging
- TTL auto-exit + exit-on-success
- pinentry override always restored

### Treat the Public URL as sensitive

The **Public URL includes the one-time token**. Anyone who obtains it during the TTL window can access the unlock form.

- Do **not** paste the Public URL into GitHub issues, logs, screenshots, or shared channels.
- Share it only to the person who is unlocking, and only for that one session.

### Autofill note

The password input is configured to discourage browser/password-manager autofill (best-effort), but **some managers may still try to fill**.
If you want to avoid accidental autofill, use a private/incognito window or temporarily disable the password manager for that page.

### Retry / “unlock in progress” note

An unlock attempt can take a bit of time. If you submit twice quickly, you may see an “unlock attempt already in progress” message.
Wait for the attempt to finish (default timeout is ~30s) before retrying.

## Files

Implementation lives in:
- `skills/headless-bitwarden/scripts/rbw-remote-unlock/{start.sh,server.mjs,pinentry.sh}`

## Troubleshooting / operational notes

### pinentry restore reliability

The helper **does not call** `rbw config set/unset` (which can hang in non-interactive environments). Instead, it temporarily edits:

- `~/.config/rbw/config.json` → `pinentry: <path-to-pinentry.sh>`

and then restores it back.

If something crashes mid-flight, the quickest manual recovery is:

```bash
rbw config set pinentry pinentry
```

### Agent state

If `rbw unlocked` says `agent not running`, restart/refresh the agent by running:

```bash
rbw stop-agent || true
rbw unlocked
```
