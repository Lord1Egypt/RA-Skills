# office-adobe-user-provision

**English** | [中文](./README.zh-CN.md)

> **Type:** Agent Skill (Claude Code / Anthropic-compatible) · **Entry point:** [`SKILL.md`](./SKILL.md)
> **Capability:** provision & manage **Microsoft 365 (世纪互联 / 21Vianet)** and **Adobe Creative Cloud** users — create, license, reset password, delete, inspect, batch, selftest.
> **Credentials:** none in this repo. Ships `.env.example` only; `.env` is git-ignored.

---

## TL;DR for agents

| | |
|---|---|
| **What it is** | A self-contained skill. `SKILL.md` holds the activation triggers and the operating procedure. |
| **Install** | `git clone <this repo> ~/.claude/skills/office-adobe-user-provision` then restart the session. |
| **Configure** | `cp .env.example .env` and fill your own Entra App / Adobe UMAPI / SMTP credentials. |
| **Invoke** | `./oup <provider> <action> ...` (e.g. `./oup adobe create alice@corp.com --product cc`). |
| **Runtime** | Python 3.9+. Use `./oup` or `python3 main.py` — **never bare `python`** (often Python 2). |

## Is this a skill or a plain repo? — A skill.

This repository **is** a Claude Code Skill. The contract:

- [`SKILL.md`](./SKILL.md) begins with YAML frontmatter:
  - `name: office-adobe-user-provision`
  - `description:` one-liner **plus `USE WHEN ...` trigger phrases** that let an agent auto-activate it.
- Claude Code discovers skills by scanning skill directories **at session start**. Placing this repo at
  `~/.claude/skills/office-adobe-user-provision/` (global) or `<project>/.claude/skills/...` (project-scoped)
  registers it. The **directory name is the skill name**, so clone it under that exact folder name.
- It is **also** a standalone Python CLI/HTTP tool, so it works without any agent — handy for testing or scripting.

## Install (clone-to-install)

```bash
# Global (available in every session on this machine)
git clone https://github.com/eggyrooch-blip/office-adobe-user-provision.git \
  ~/.claude/skills/office-adobe-user-provision

# Project-scoped instead:
#   git clone <url> <your-repo>/.claude/skills/office-adobe-user-provision
```

Restart the Claude Code session afterward — the skill list loads at startup.

## Configure

```bash
cd ~/.claude/skills/office-adobe-user-provision
cp .env.example .env          # fill in your own credentials (see template comments)
pip install -r requirements.txt
./oup office365 init          # verify O365 credentials + fetch products
./oup adobe init              # verify Adobe credentials + fetch products
```

Credentials you supply (see [`.env.example`](./.env.example)):

- **Office 365** — Entra App `CLIENT_ID` / `TENANT_ID` / `CLIENT_SECRET` (admin consent for `User.ReadWrite.All`, `LicenseAssignment.ReadWrite.All`, `User-PasswordProfile.ReadWrite.All`), plus `DEFAULT_DOMAIN`.
- **Adobe** — UMAPI `ADOBE_CLIENT_ID` / `ADOBE_CLIENT_SECRET` / `ADOBE_ORG_ID`.
- **Optional** — SMTP block for credential notification emails.

## Capabilities

```bash
./oup <provider> init                                  # verify creds + cache products
./oup <provider> products [--refresh]                  # list / refresh product catalog
./oup office365 create <ldap> --display-name "<Name>"  # create + auto-license + notify
./oup adobe   create <ldap>@<domain> --product cc      # cc=All Apps · ps=Photoshop · acrobat=Acrobat Pro
./oup <provider> assign  <id> --product <p>            # add a license/product
./oup <provider> reset   <id>                          # reset password
./oup <provider> delete  <id>                          # delete user
./oup <provider> inspect <id> --json                   # query (read-only)
./oup <provider> selftest                              # end-to-end (creates→licenses→resets→deletes a temp user)
python3 -m app.api.server                              # HTTP API mirroring the CLI
```

`provider` aliases: `office365` = `o365` = `m365`; `adobe` = `ps`.
`oup` is the bundled CLI wrapper — it self-locates the skill dir, loads `.env`, and runs from any cwd. Equivalent to `python3 main.py ...`.

## Activation triggers

An agent should activate this skill when the user says (any language):

`给 XX 开账号` · `新建用户` · `入职开账号` · `开 Office` · `开 Adobe` · `全家桶 / All Apps` · `重置密码` · `删除用户` · `批量开户` · `查用户` · "create user", "provision account", "add Office/Adobe license"

## Safety rules (enforced in SKILL.md)

- **Never overwrite an existing user** — `inspect` first; if found, confirm reset vs skip.
- **Never echo initial passwords to logs** — they go only into the notification email.
- **Never invent the LDAP** — require it explicitly from the user.
- **`.env` never enters git** — `.gitignore` excludes it; verify `git status` before any commit.

## Architecture

```
entry (main.py CLI · app/api/server.py Flask)
   └─ app/services/user_service.py      ← single business facade (all entry points call this)
        └─ app/providers/office365/     ← Graph API: auth, users, licenses, email
        └─ app/providers/adobe/         ← UMAPI: auth, addAdobeID + group assignment
```

Extend by adding to `user_service.py` first, then exposing via CLI/API. Full procedure, Red Flags table, and per-provider details live in [`SKILL.md`](./SKILL.md).
