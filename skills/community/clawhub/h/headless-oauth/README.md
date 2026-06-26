# 🔐 headless-oauth

> **AgentSkill for [OpenClaw](https://openclaw.ai)** — Authorize any OAuth CLI on a headless server, no browser required.

[![clawhub](https://img.shields.io/badge/clawhub-headless--oauth-blue)](https://clawhub.ai/skills/headless-oauth)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green.svg)](https://opensource.org/licenses/MIT-0)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-purple)](https://openclaw.ai)

---

## The Problem

OAuth requires a browser. On a headless VPS or server, there is no browser. Most CLI tools hang or crash with an unhelpful error when you try to authenticate.

## The Solution

Split the OAuth flow across two machines:

```
VPS / Server                    Your Local Machine
────────────────                ──────────────────
1. Generate auth URL    ──────► 2. Open URL in browser
                                3. Log in + grant permissions
                                4. Copy redirect URL or code
5. Exchange for token   ◄──────
6. Token stored locally ✓
```

This skill teaches your OpenClaw agent exactly how to do this for the most common CLI tools.

---

## Three Patterns

| Pattern | How it works | Example tools |
|---------|-------------|---------------|
| **Generate URL / paste back** | CLI prints auth URL, user opens locally, pastes redirect URL back | gog, gcloud |
| **Device flow** | CLI prints a short code + URL, user enters code, CLI polls automatically | gh (GitHub CLI) |
| **Manual callback relay** | CLI starts a local HTTP server for callback; user copies the failed redirect URL from browser, agent forwards it via curl | mcporter, MCP servers |

---

## Install

```bash
npx clawhub@latest install headless-oauth
```

Or clone manually and place in your OpenClaw `workspace/skills/` directory.

---

## Quick Example: GitHub CLI on a VPS

```bash
gh auth login --hostname github.com --git-protocol https --no-launch-browser
# → Prints a one-time code like: ABCD-1234
# → Open https://github.com/login/device on your local machine
# → Enter the code — gh polls and completes automatically
```

---

## Keyring Note

Some CLIs store tokens in a system keyring that requires an interactive terminal to unlock.
Check the CLI's documentation for a non-interactive option. Set any required credential
only for the duration of the auth step — do not persist it in shell configs.

---

## Common Errors

| Error | Fix |
|-------|-----|
| `redirect_uri_mismatch` | Use **Desktop app** OAuth client, not Web application |
| Keyring unlock fails | Check CLI docs for a non-interactive keyring option |
| `Access blocked` | Add your email as test user in Google consent screen |
| Commands fail silently | Check CLI docs for a required account identifier option |

---

## Files

```
headless-oauth/
└── SKILL.md    # AgentSkill instructions (all three patterns)
```

---

## About AgentSkills

This is an [AgentSkill](https://openclaw.ai) — a Markdown-based instruction set for OpenClaw agents. When installed, the agent automatically knows how to handle headless OAuth flows for you.

Built by [Igor Ivanter](https://igorivanter.com) · Published on [ClawHub](https://clawhub.ai/skills/headless-oauth)
