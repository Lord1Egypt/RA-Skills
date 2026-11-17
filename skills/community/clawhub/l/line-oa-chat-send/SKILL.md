---
name: line-oa-chat-send
description: Send explicitly authorized LINE Official Account Chat messages through a persistent Chromium session; user-operated LINE login or reauthentication may use a temporary remote noVNC handoff that grants interactive browser control.
---

# LINE OA Chat: send a message

## Use when

A user provides or has already opened a LINE OA Chat URL and asks to send a
specific message to a named chat recipient.

## Prerequisites

- The persistent Chromium profile is already authenticated to LINE by the user.
- A browser session is running with its loopback CDP endpoint reachable.
- The user has explicitly authorized the outgoing message. Do not infer a
  message other than an unambiguous test message.

## Security boundary

- Normal message work uses local CDP only. It does not expose a browser, CDP,
  VNC, screenshots, cookies, or profile data to the network.
- The optional noVNC handoff is **only** for a user to complete LINE login or
  reauthentication. It grants whoever holds its URL interactive control of the
  browser, so treat the URL as a high-risk bearer secret—not as a general
  browsing or support channel.
- Start a handoff only after the user explicitly requests this
  login/reauthentication route. It has a default 15-minute TTL (configurable only
  from 60 to 3600 seconds), must be shared only in a direct private channel, and
  must be revoked immediately after login. Do not use it to send messages, browse
  unrelated sites, or perform autonomous actions.
- Never request, handle, record, or transmit LINE passwords, OTPs, or other
  credentials. The user completes every authentication step themselves.
- Never log, commit, reuse, or relay a handoff URL.

Revoking a handoff removes external reachability only; the browser session keeps
running. That narrows the cost of revoking promptly — it does not narrow what the
handoff grants while it is armed.

## Quick start

```bash
# 1. Check the environment. Exit 0 = ready; 3 = usable but not logged in; 1 = blocked.
bash scripts/doctor.sh

# 2. Start the browser session if one is not running.
#    Owns the display, Chromium, and a loopback-only screen-sharing stack.
#    Nothing is externally reachable.
bash scripts/start_line_oa_chromium.sh

# 3. ONLY when the user explicitly asks to log in or re-authenticate.
#    Prints one URL, already verified reachable, or fails non-zero.
export LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login
export LINE_OA_SEND_CHAT_HANDOFF_TTL_SECONDS=900   # 60-3600, default 900
bash scripts/start_line_oa_vnc_handoff.sh

# 4. Revoke as soon as the user says login is done. Session keeps running.
bash scripts/stop_line_oa_vnc_handoff.sh

# 5. Find and open the chat without sending. This is the safe default.
bash scripts/run_line_oa_chat.sh --recipient "<exact recipient>" --message "<message>"

# 6. Send, only after the user authorized this exact recipient and message.
bash scripts/run_line_oa_chat.sh --recipient "<exact recipient>" --message "<message>" --send

# 7. Stop the session when the work is finished. The profile is preserved.
bash scripts/stop_line_oa_chromium.sh
```

Provision a Python runtime only if `doctor.sh` reports one missing:

```bash
bash scripts/setup_line_oa_runtime.sh --runtime-dir <private-dir> --skip-browser-install
export LINE_OA_PYTHON=<private-dir>/venv/bin/python
```

## What the scripts guarantee

You do not need to re-check these by hand.

- **The handoff prints a URL only after verifying it.** It fetches the public URL
  and requires HTTP 200 with noVNC content. On failure it prints no URL, revokes
  what it started, and exits non-zero naming the phase that failed. Do not
  construct or share a URL yourself.
- **Arming refuses** with no session, with stale session state, without the login
  purpose, with an out-of-range TTL, and when a handoff is already armed.
- **Nothing is externally reachable between handoffs.** The front end answers 404
  until a token route is armed.
- **The send CLI refuses ambiguous recipients**, requires `--send` for the
  external side effect, and verifies the message landed before reporting success.
- **Shutdown is scripted.** It revokes any armed handoff first, terminates the
  recorded process gracefully, and reports rather than force-killing on timeout.

## When to stop and ask the user

- **The recipient search matched more than one chat.** Stop. Ask which
  conversation to use. Never guess which person receives a message.
- **Post-send verification failed.** Do **not** retry. LINE may have accepted the
  message already, so a retry risks sending it twice. Inspect the browser first,
  then report what you found.
- **LINE asks for a password, QR confirmation, MFA, OTP, or a security prompt.**
  Only the user resolves these, through the handoff. Do not read, type, store,
  relay, or log any credential or verification code.
- **The session expired or was revoked mid-task.** Pause and ask the user to
  reauthenticate through the handoff, then re-check before continuing.
- **`doctor.sh` reports a blocker.** Report the exact missing pieces and its
  remediation. Do not invoke `sudo` or a package manager, and never weaken a
  network binding to work around a failure.
- **The profile is locked by another hostname.** Another Chromium may genuinely
  hold it. Report it; do not clear the lock.

## Reference material

Read these when you need depth; they are not needed for a normal send.

| File | Read it when |
| --- | --- |
| [references/line-oa-ui-selectors.md](references/line-oa-ui-selectors.md) | The send flow fails to find the search box, the chat, or the composer |
| [references/handoff-operations.md](references/handoff-operations.md) | Changing the session or handoff scripts, or diagnosing a handoff that will not verify |
| [references/public-repository-checklist.md](references/public-repository-checklist.md) | Making the repository public |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Changing this repository |
| [containers/README.md](containers/README.md) | Running the scripts in the Linux test environment |

`scripts/send_line_oa_chat.py` is the only implementation of the send flow. Do
not write a second one.
