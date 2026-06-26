# Authentication & Connection

This is the most security-sensitive part of the skill. Read it before configuring credentials anywhere.

## The model in one paragraph

Credentials live as **environment variables** that the runtime injects per agent run. The wrapper at `scripts/imap.sh` reads those env vars, picks the right `myl` connection flags, and never echoes the password. **You configure once, you read mail forever.**

## Setting up credentials — pick one method

### Method A — OpenClaw (recommended for OpenClaw users)

OpenClaw injects `skills.entries.<key>.env` into `process.env` for the duration of each agent turn, then restores the original environment. This is documented behaviour: see https://docs.openclaw.ai/tools/skills under "Environment injection (per agent run)".

Edit `~/.openclaw/openclaw.json` and add an entry under `skills.entries`:

```json
{
  "skills": {
    "entries": {
      "imap-client": {
        "enabled": true,
        "env": {
          "IMAP_USER": "you@example.com",
          "IMAP_PASSWORD": "app-specific-password-here",
          "IMAP_PROVIDER": "auto"
        }
      }
    }
  }
}
```

Then restart the agent session (or wait for the skills watcher to pick it up if `skills.load.watch` is enabled). The next time the agent runs the skill, `IMAP_USER` and `IMAP_PASSWORD` are already in the environment.

**Permissions matter.** `~/.openclaw/openclaw.json` should not be world-readable:

```bash
chmod 600 ~/.openclaw/openclaw.json
```

**Use `apiKey` with a SecretRef for stronger isolation.** OpenClaw supports pulling the password from a separate source rather than inlining it as plaintext in the JSON:

```json
{
  "skills": {
    "entries": {
      "imap-client": {
        "enabled": true,
        "apiKey": { "source": "env", "provider": "default", "id": "MY_IMAP_PASSWORD" },
        "env": {
          "IMAP_USER": "you@example.com",
          "IMAP_PROVIDER": "auto"
        }
      }
    }
  }
}
```

The `apiKey` field maps to whatever env var name is declared in `metadata.openclaw.primaryEnv` of `SKILL.md` — for this skill that's `IMAP_PASSWORD`. So OpenClaw reads `MY_IMAP_PASSWORD` from your shell env (or another secret backend) and exposes it as `IMAP_PASSWORD` to the wrapper. The literal password never appears in `openclaw.json`.

### Method B — Generic shell `export`

For Claude Code and other AgentSkills runtimes that don't have OpenClaw's injection mechanism, just export the variables in the shell that launches the agent:

```bash
export IMAP_USER='you@example.com'
export IMAP_PASSWORD='app-specific-password-here'
export IMAP_PROVIDER='auto'
```

Put this in `~/.bashrc` / `~/.zshrc` if you want it to persist. The downside compared to Method A is that the variables are global to that shell, not scoped to the agent run. The upside is no extra config file.

### Method C — Credentials file fallback

When neither Method A nor B is convenient (e.g. cron jobs, headless workflows, CI), drop a credentials file at `~/.config/imap-client/credentials`:

```bash
mkdir -p ~/.config/imap-client
cat > ~/.config/imap-client/credentials <<'EOF'
IMAP_USER='you@example.com'
IMAP_PASSWORD='app-specific-password-here'
IMAP_PROVIDER='auto'
EOF
chmod 600 ~/.config/imap-client/credentials
```

The wrapper sources this file when `IMAP_USER`/`IMAP_PASSWORD` are not in the env, **but only if permissions are 600 or 400**. World-readable creds files are ignored with a warning.

To use a different path, set `IMAP_CREDENTIALS_FILE` in env.

## Per-account: switching mailboxes

For multiple accounts, declare each one as a separate OpenClaw skill entry under a different agent (per-agent skill allowlists make this clean), or scope the env per shell:

```bash
# Work
( export IMAP_USER='kirill@codd.tech' \
         IMAP_PASSWORD="$WORK_APP_PASSWORD" \
         IMAP_PROVIDER='auto' ; \
  bash scripts/imap.sh --count 5 )

# Personal
( export IMAP_USER='kirill@yandex.ru' \
         IMAP_PASSWORD="$YANDEX_APP_PASSWORD" \
         IMAP_PROVIDER='yandex' ; \
  bash scripts/imap.sh --count 5 )
```

The parentheses create a subshell so the exports don't pollute your main session.

## `IMAP_PROVIDER` — what to set

| Value | Effect | When to use |
|---|---|---|
| `auto` (default) | `myl --auto` — autodiscovery from username domain | Most modern providers (Fastmail, iCloud, ISPs) |
| `gmail` | `myl --google` — hardcoded Gmail IMAP | `@gmail.com` / Google Workspace accounts |
| `yandex` | `--server imap.yandex.com --port 993` | Yandex Mail (`@yandex.ru`, `@yandex.com`, custom domains) |
| `mailru` | `--server imap.mail.ru --port 993` | Mail.ru (`@mail.ru`, `@bk.ru`, `@inbox.ru`, `@list.ru`) |
| `manual` | `--server $IMAP_SERVER --port $IMAP_PORT [--starttls]` | Self-hosted, corporate, or anything autodiscovery doesn't recognise |

## App passwords — the credential the user actually needs

Almost no major provider accepts the account password over IMAP anymore when 2FA is enabled. They require an **app-specific password** generated from the account settings.

| Provider | Where to generate | Notes |
|---|---|---|
| **Gmail / Google Workspace** | https://myaccount.google.com/apppasswords | Requires 2-Step Verification on. If the link 404s, your account or organisation has app passwords disabled — switch provider or ask admin. |
| **Yandex Mail** | https://id.yandex.ru/security/app-passwords | Pick "Mail (IMAP/POP3, SMTP)". Works for `@yandex.ru`, `@yandex.com`, and custom domains hosted on Yandex 360. |
| **Mail.ru** | Account → "Пароли для внешних приложений" / "Passwords for external applications" | Same password works for `@mail.ru`, `@bk.ru`, `@inbox.ru`, `@list.ru`. |
| **Fastmail** | Settings → Privacy & Security → App Passwords | Can scope to "IMAP only" for least privilege. |
| **iCloud** | https://appleid.apple.com → Sign-In and Security → App-Specific Passwords | Username is your Apple ID email, even if you use an `@icloud.com` alias. |
| **Yahoo** | Account Security → Generate app password | |
| **Proton Mail** | Requires Proton Bridge running locally | Use `IMAP_PROVIDER=manual`, `IMAP_SERVER=127.0.0.1`, `IMAP_PORT=1143`. |
| **Outlook.com** | Microsoft has been deprecating basic auth | If app passwords are disabled, use `mbsync` with XOAUTH2 instead. `myl` does not do OAuth2. |

When the IMAP server returns `AUTHENTICATIONFAILED` and the username is one of the providers above, the cause is almost always that the user is trying their account password instead of an app password. Direct them to the relevant URL and explain why.

## Yandex specifics

Yandex Mail is widely used in Russian-speaking contexts and has a few quirks worth knowing:

- **Two server hostnames exist.** `imap.yandex.com` and `imap.yandex.ru` both work; `IMAP_PROVIDER=yandex` defaults to `.com` which serves both account types correctly. To force `.ru`, set `IMAP_SERVER=imap.yandex.ru`.
- **Mailbox features must be enabled in Yandex web UI.** Settings → "Почтовые программы" → tick "С сервера imap.yandex.ru по протоколу IMAP". Without this, IMAP login fails with `AUTHENTICATIONFAILED` even with the right app password.
- **Yandex 360 / business accounts (`@your-company.ru` hosted on Yandex)** use the same `imap.yandex.com:993` endpoint and the same app password mechanism.
- **Folder names are localised.** See `references/operations.md` for the Russian folder name table.

## Mail.ru specifics

- **One app password covers the whole domain group** — the same credential works against `@mail.ru`, `@bk.ru`, `@inbox.ru`, `@list.ru` if you own multiple addresses on the platform.
- **IMAP must be explicitly enabled in account settings.** Mail.ru settings → "Все настройки" → "Почтовые программы" → enable IMAP. Same gotcha as Yandex.

## What to do if the user pastes a password into chat

Treat it as compromised. The password may now sit in:

- the chat transcript / conversation log
- any analytics or telemetry the runtime captured
- the user's clipboard history

**Tell the user explicitly:** "That password is now in the chat history. Rotate it (regenerate the app password from the provider) and put the new one into your `~/.openclaw/openclaw.json` config — not into chat." Then walk them through Method A above.

Do not echo the password back, do not write it to any file, do not include it in a summary, and do not silently reuse it for the rest of the session.

## Smoke test

Once credentials are configured, confirm the connection works with a minimal call:

```bash
bash scripts/imap.sh --count 1 >/dev/null && echo "connection OK"
```

If this prints `connection OK`, every other operation in `references/operations.md` will work the same way.
