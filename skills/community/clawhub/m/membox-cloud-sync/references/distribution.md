# Distribution and Lazy-User Flow

## Product Goal

Target experience:

1. The user already has OpenClaw.
2. The user says one sentence in IM.
3. The agent installs the Membox plugin and the Membox skill.
4. If the current conversation has not loaded the new plugin or skill yet, the flow continues in a fresh OpenClaw session or next run.
5. The agent starts setup and returns a clickable `membox.cloud` authorization link.
6. The user taps that link on a phone or trusted browser and confirms identity.
7. The agent finishes setup, stores local encrypted state, and continues with sync or restore.

The human should not need to understand `user_code` or raw HTTP calls. Local secret file choices still require explicit human approval.

## What the Agent Should Install

Plugin:

- `openclaw plugins install @membox-cloud/membox`

Skill:

- preferred published path: `clawhub install membox-cloud-sync`

Published default:

```bash
openclaw plugins install @membox-cloud/membox
clawhub install membox-cloud-sync
```

## ClawHub Status

Use ClawHub as the remote skill registry. The plugin is published separately through npm.

That means:

- plugin distribution lives at npm
- skill distribution lives at ClawHub
- the skill should instruct the agent to install the plugin if the `membox_*` tools are missing

## Operational Guidance for the Agent

When the user is lazy and wants the agent to do almost everything:

1. Detect whether the Membox plugin is already installed.
2. If not, install `@membox-cloud/membox`.
3. Detect whether the `membox-cloud-sync` skill is available.
4. If not, install it from ClawHub with `clawhub install membox-cloud-sync`.
5. If install happened in the current conversation and `membox_*` tools are still unavailable, continue in a fresh OpenClaw session or next run.
6. Call `membox_setup_start`.
7. Return the exact `verification_uri_complete` to the user.
8. Poll `membox_setup_poll`.
9. Finish with `membox_setup_finish` using local private files for the passphrase and recovery output path.
10. Treat unlock and managed-unlock decisions as a separate local boundary before assuming later sync, pull, or trusted-device approval can run unattended.

Status reporting rule:

- Separate what you inferred from docs, what you plan to do next, what you already executed, and what you actually verified.
- Do not tell the user "already installed", "latest version", or "environment ready" unless the current run checked and confirmed that state.

## Human Boundary

The agent may drive most of the flow, but not every secret-bearing decision.

The human is still expected to:

- tap the authorization link
- log in if the browser is not already signed in
- satisfy MFA, email verification, or CAPTCHA if the identity provider requires it
- choose or provide the local vault passphrase through a private local file path
- keep or approve the local recovery-code destination
- explicitly opt in before the agent enables managed unlock on the machine

The agent must not ask the user to paste those secrets into chat just to make progress.

Everything after that may be automated by the agent only if the required local secret files or managed unlock policy are already in place.
