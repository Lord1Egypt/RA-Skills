# imap-client

[![Install via ClawHub](https://img.shields.io/badge/install-clawhub-2563eb?style=flat-square)](https://clawhub.ai/aggrrrh/imap-client)
[![License: MIT](https://img.shields.io/github/license/codd-tech/imap-client?style=flat-square)](./LICENSE)
[![Maintained by codd.tech](https://img.shields.io/badge/maintained%20by-codd.tech-f97316?style=flat-square)](https://codd.tech)
[![Stars](https://img.shields.io/github/stars/codd-tech/imap-client?style=flat-square)](https://github.com/codd-tech/imap-client/stargazers)

An agent skill for [OpenClaw](https://openclaw.ai), Claude Code, and other AgentSkills-compatible runtimes. Lets the agent read, search, and download email over IMAP from the command line via the [`myl`](https://github.com/pschmitt/myl) CLI client.

`myl` is a small read-only IMAP client. This skill teaches the agent **when** to reach for it, **how** to install it, **how to source credentials safely** from the runtime's environment-injection mechanism, and **which** flags to use for common tasks — without ever asking for the password mid-session.

## What this skill enables

Once installed and configured once, the agent will recognise prompts like:

- *"check my inbox"*
- *"any new email from Acme today?"*
- *"find the email with the AWS invoice and save the PDF"*
- *"show me the HTML version of the newsletter from yesterday"*
- *"download all unread messages as `.eml` files"*
- *"проверь почту на Яндексе"*
- *"найди письмо от налоговой"*

…and translate them into safe `myl` invocations through the wrapper at `scripts/imap.sh`, summarising the result back in chat.

## Provider support

First-class support, with `IMAP_PROVIDER` shortcuts:

- **Gmail** / Google Workspace (`IMAP_PROVIDER=gmail`)
- **Yandex Mail** — `@yandex.ru`, `@yandex.com`, Yandex 360 custom domains (`IMAP_PROVIDER=yandex`)
- **Mail.ru** — `@mail.ru`, `@bk.ru`, `@inbox.ru`, `@list.ru` (`IMAP_PROVIDER=mailru`)

Plus autodiscovery for most other providers (Fastmail, iCloud, ISPs) and explicit `manual` mode for self-hosted / corporate servers.

## Quick start

### 1. Install `myl`

```bash
pipx install myl
```

(Or `pip install --user myl`, or `nix run github:pschmitt/myl`.)

### 2. Get an app-specific password from your provider

Account settings → app passwords / external app passwords. Direct links per provider in [`references/authentication.md`](./references/authentication.md).

### 3. Install the skill

**Recommended — via ClawHub:**

```bash
clawhub install imap-client
```

**Or clone directly:**

```bash
# OpenClaw
git clone https://github.com/codd-tech/imap-client ~/.openclaw/skills/imap-client

# Claude Code
git clone https://github.com/codd-tech/imap-client ~/.claude/skills/imap-client

# Generic AgentSkills runtime — drop the folder anywhere the runtime scans for SKILL.md
```

Restart the session. OpenClaw picks the skill up automatically. The skill declares `requires.bins: ["myl"]` so it filters itself out if `myl` isn't on `PATH` — you'll never get a half-broken state.

### 4. Configure credentials — pick the method for your runtime

**OpenClaw** (recommended for OpenClaw users) — edit `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "imap-client": {
        "enabled": true,
        "env": {
          "IMAP_USER": "you@yandex.ru",
          "IMAP_PASSWORD": "app-specific-password-here",
          "IMAP_PROVIDER": "yandex"
        }
      }
    }
  }
}
```

```bash
chmod 600 ~/.openclaw/openclaw.json
```

OpenClaw injects these into `process.env` per agent run. You configure once; every subsequent session has them.

**Claude Code / generic shell** — export in `~/.bashrc` / `~/.zshrc`:

```bash
export IMAP_USER='you@yandex.ru'
export IMAP_PASSWORD='app-specific-password-here'
export IMAP_PROVIDER='yandex'
```

**Headless / cron / fallback** — create `~/.config/imap-client/credentials`:

```bash
mkdir -p ~/.config/imap-client
cat > ~/.config/imap-client/credentials <<'EOF'
IMAP_USER='you@yandex.ru'
IMAP_PASSWORD='app-specific-password-here'
IMAP_PROVIDER='yandex'
EOF
chmod 600 ~/.config/imap-client/credentials
```

The wrapper refuses to source this file if its permissions are not `600` or `400`.

### 5. Verify

Ask the agent something like *"check the latest five emails"* — or run the wrapper directly:

```bash
bash ~/.openclaw/skills/imap-client/scripts/imap.sh --count 5
```

## Repo layout

```
imap-client/
├── SKILL.md                       # Frontmatter + workflow + principles
├── README.md                      # This file
├── LICENSE                        # MIT
├── .gitignore
├── references/
│   ├── installation.md            # pipx / pip / nix / source install paths + sandbox
│   ├── authentication.md          # OpenClaw env injection + fallbacks; provider table
│   ├── operations.md              # Full myl flag reference + folder names per provider
│   ├── recipes.md                 # 11 multi-step workflows, including Yandex/Mail.ru
│   └── troubleshooting.md         # Symptom-first error guide
└── scripts/
    ├── imap.sh                    # Credential-aware wrapper around myl
    └── check_myl.sh               # Fast install detection
```

## Security model

The skill is opinionated about credentials. The short version:

- Passwords never appear as literals in commands the agent generates.
- The runtime's environment-injection mechanism (OpenClaw `skills.entries.<key>.env`, or shell `export`, or the `chmod 600` creds file) is the source of truth.
- The `imap.sh` wrapper reads env vars and constructs `myl` flags internally — the password is in the wrapper's process scope, never in the agent's command history.
- App-specific passwords from each provider are the default recommendation; the skill explains where to generate them (Gmail, Yandex, Mail.ru, iCloud, Fastmail, Yahoo).
- The agent is instructed not to echo, summarise, or persist the password anywhere.
- For OpenClaw users, `apiKey` with a `SecretRef` (`{ source, provider, id }`) keeps the literal password out of `openclaw.json` entirely.

See [`references/authentication.md`](./references/authentication.md) for the full ruleset.

## Limitations of `myl` itself

`myl` is intentionally minimal. The skill will tell the user explicitly when their request is out of scope and suggest alternatives:

| Want to… | Use instead |
|---|---|
| Send mail | `msmtp`, `mutt`, scripted SMTP |
| Move / delete / label | `imap-tools`, the provider's web UI |
| Sync to local maildir | `mbsync` (`isync`), `offlineimap`, `getmail` |
| OAuth2 to Gmail / Outlook | Proton Bridge, `mbsync` + XOAUTH2, or app password fallback |

## Contributing

Bug reports and PRs welcome. The skill itself is markdown plus two shell scripts — easy to read, easy to fork.

When proposing changes, prefer:

- additions to `references/` over additions to `SKILL.md` (keep the always-loaded part lean)
- examples that don't paste credentials anywhere
- behaviour changes that fail safely if the user's `myl` version is older than the skill assumes

## Credits

- [`myl`](https://github.com/pschmitt/myl) by Philipp Schmitt — the underlying CLI this skill wraps.
- [OpenClaw](https://openclaw.ai) for the AgentSkills runtime, env injection mechanism, and skills format documented at https://docs.openclaw.ai/tools/skills.
- Anthropic's [Skills documentation](https://docs.claude.com/en/docs/build-with-claude/skills) — structure and best-practice patterns.

## About the maintainer

Built and maintained by **[codd.tech](https://codd.tech)** — a boutique technical consultancy specialising in AI agent infrastructure, distributed systems, and platform engineering. We help product teams ship reliable agentic workflows in production: integration design, custom skill packs, OpenClaw / Claude / MCP deployments, and DevOps audits.

Have a use case for agent-driven email automation, or want a custom skill built for your stack? **[Get in touch](https://codd.tech)**.

## License

MIT — see [`LICENSE`](./LICENSE).
