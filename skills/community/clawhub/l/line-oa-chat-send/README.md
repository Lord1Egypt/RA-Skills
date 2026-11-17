# line-oa-chat-send

A safety-first CLI for sending messages through an already authenticated
[LINE Official Account Chat](https://chat.line.biz/) browser session.

The send command attaches to a local Chromium DevTools (CDP) endpoint. It does
not start a browser, log in to LINE, or collect credentials.

> **Optional login handoff — high-risk capability:** when a user explicitly asks
> to complete LINE login or reauthentication through a remote GUI,
> `scripts/start_line_oa_vnc_handoff.sh` arms a temporary Cloudflare noVNC URL
> that grants its holder interactive control of the browser. It attaches to a
> running session rather than starting one, requires the explicit
> `LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login` scope, defaults to a 15-minute
> TTL, keeps VNC and CDP loopback-only, and must be revoked as soon as login
> ends. Revoking it leaves the browser session running.

## What it does

- Searches for a chat recipient and refuses ambiguous matches.
- Opens the selected conversation and confirms the composer is available.
- Defaults to a no-send dry run; requires an explicit `--send` to transmit.
- After a send, checks that the composer cleared and the exact message appears in
  the active transcript.

## Requirements

1. A user-authenticated LINE OA Chat session in Chromium.
2. Chromium exposing a loopback CDP endpoint (default `http://127.0.0.1:9222`).
3. Python with the `playwright` package. No browser download is needed — the tool
   attaches to an existing Chromium.
4. Explicit authorization for the recipient and the outgoing message.

Linux is the supported platform. `containers/` provides a reproducible Linux
environment for running the scripts from another OS.

> **Authentication:** complete LINE login, password entry, QR confirmation, MFA,
> OTP, and security prompts yourself in the interactive browser. This project
> never accepts, stores, or transmits those secrets.

## Check the environment first

```bash
bash scripts/doctor.sh
```

| Exit | Meaning |
| --- | --- |
| 0 | Ready; a send can run |
| 3 | Environment usable, LINE authentication required — a checkpoint, not a failure |
| 1 | Blocked; the missing pieces and their remediation are printed |

It reports what the launcher will actually do, and never suggests widening a
network binding. It invokes no package manager and no `sudo`.

If it reports no Python runtime:

```bash
bash scripts/setup_line_oa_runtime.sh --runtime-dir <private-dir> --skip-browser-install
export LINE_OA_PYTHON=<private-dir>/venv/bin/python
```

## Usage

```bash
# Start the browser session. Owns the display, Chromium, and a loopback-only
# screen-sharing stack. Nothing is externally reachable.
bash scripts/start_line_oa_chromium.sh

# Safe default: find and open a uniquely matched chat, send nothing.
bash scripts/run_line_oa_chat.sh --recipient "Recipient name" --message "Message text"

# Send, only after the recipient and exact text have been authorized.
bash scripts/run_line_oa_chat.sh --recipient "Recipient name" --message "Message text" --send

# Stop the session. The persistent profile is preserved.
bash scripts/stop_line_oa_chromium.sh
```

Use `--cdp-url` if the endpoint is not the default. `--help` lists all options.

## Login / reauthentication handoff

Only after the user explicitly requests an interactive login session. It is a
login-only capability; do not use it to send messages or for unrelated browser
control.

```bash
export LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login
export LINE_OA_SEND_CHAT_HANDOFF_TTL_SECONDS=900   # optional; 60-3600
bash scripts/start_line_oa_vnc_handoff.sh

# When the user says login is done:
bash scripts/stop_line_oa_vnc_handoff.sh
```

The script attaches to the running session, arms a private high-entropy route,
starts the tunnel, and **verifies the public URL is reachable before printing
it**. On failure it prints no URL, revokes what it started, and exits non-zero
naming the failing phase. It refuses to arm with no session, with stale session
state, without the login purpose, with an out-of-range TTL, or when a handoff is
already armed.

The printed URL is a bearer secret. Share it only with that user in a private
channel, never log or reuse it, and revoke as soon as login ends. TTL expiry is a
backstop, not a substitute for prompt revocation.

Arming takes roughly 20–25 seconds, most of it a deliberate quiet window before
the first DNS lookup. See
[references/handoff-operations.md](references/handoff-operations.md) for why
probing sooner makes it slower.

## Safety behavior

- A run without `--send` never transmits a message.
- If more than one chat may match the recipient, the command stops instead of
  guessing.
- If the authenticated UI, chat selection, composer, or post-send verification
  fails, the command exits non-zero.
- Do not retry a failed post-send verification automatically: LINE may have
  accepted the message even if verification did not complete.
- CDP, VNC, websockify, and the HTTP front end stay on loopback. The front end
  answers 404 until a handoff is armed. Nothing is externally reachable between
  handoffs.

## Testing

```bash
containers/build.sh                                  # four dependency variants
containers/test/default.sh                           # no external exposure
LINE_OA_TEST_ALLOW_TUNNEL=1 containers/test/tunnel.sh 60   # opt-in; exposes a browser
```

See [containers/README.md](containers/README.md), including what the container is
and is not authoritative for.

## Documentation

- [SKILL.md](SKILL.md) — what an agent needs to decide and act
- [references/](references/) — UI selectors, handoff operations, publication checklist
- [CONTRIBUTING.md](CONTRIBUTING.md) — development and release process
