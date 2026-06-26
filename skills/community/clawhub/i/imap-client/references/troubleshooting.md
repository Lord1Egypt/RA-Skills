# Troubleshooting

Symptom-first lookup. When the skill misbehaves, find the closest match below before guessing.

## Wrapper says "missing credentials" but I configured them

The wrapper checks `$IMAP_USER` and `$IMAP_PASSWORD` in process env. If they're missing in the agent's process, OpenClaw's injection didn't fire. Likely causes:

1. **You edited `~/.openclaw/openclaw.json` mid-session.** OpenClaw snapshots eligible skills *when a session starts*. Restart the agent session (or rely on the skills watcher if `skills.load.watch: true`).
2. **The skill key in config doesn't match.** Under `skills.entries`, the key must be `imap-client` exactly (or whatever `metadata.openclaw.skillKey` declares — this skill doesn't override it). Hyphens require quoting in JSON5: `"imap-client": { ... }`.
3. **`skills.entries.imap-client.enabled` is `false`** or the skill is disabled by `skills.allowBundled` allowlist.
4. **The agent has a per-agent skill allowlist that excludes `imap-client`.** Check `agents.list[].skills` in `openclaw.json`.
5. **You're not on OpenClaw.** Methods B (`export`) and C (`~/.config/imap-client/credentials`) are the right paths for Claude Code or generic AgentSkills runtimes. See `authentication.md`.

To verify what env the agent actually sees, run:

```bash
env | grep -E '^IMAP_' || echo "no IMAP_* env vars in this process"
```

If that shows nothing in an OpenClaw agent run, the injection isn't reaching the exec context — file a bug against OpenClaw with `metadata.openclaw` excerpt + your `skills.entries` config (passwords redacted).

## `myl: command not found` (non-OpenClaw)

OpenClaw shouldn't load this skill without `myl` because of `requires.bins: ["myl"]`. If you see this on Claude Code or another runtime:

1. Installed via `pip install --user` but `~/.local/bin` is not in `PATH`. Add it:
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
   ```
2. Installed via `pipx` but `pipx ensurepath` was never run, or the shell wasn't restarted.
3. Installed in a virtualenv that isn't currently activated.
4. Not actually installed. `pip show myl` or `pipx list` to confirm.

## `AUTHENTICATIONFAILED` / `Invalid credentials` / `LOGIN failed`

The username + password combination was rejected. In order of likelihood:

1. **Wrong credential type.** For Gmail, Yandex, Mail.ru, iCloud, Fastmail, Yahoo — the user must use an **app-specific password**, not the account password. See `authentication.md` for the per-provider links.
2. **IMAP not enabled at the provider.** The classic Yandex/Mail.ru gotcha:
   - **Yandex Mail:** web UI → Settings → "Почтовые программы" → tick "С сервера imap.yandex.ru по протоколу IMAP". Without this, login fails even with a correct app password.
   - **Mail.ru:** "Все настройки" → "Почтовые программы" → enable IMAP.
   - **Gmail Workspace:** the org admin sometimes disables IMAP org-wide.
3. **Wrong username form.** Most providers want the full email (`alice@example.com`). Yandex 360 / business accounts: use the full address on the custom domain, not just the local part.
4. **2FA without app password.** Provider has 2FA on but the user generated no app password.
5. **Typo or expired/rotated app password.** Update `IMAP_PASSWORD` in the runtime's config.

## `SSL: CERTIFICATE_VERIFY_FAILED` / `[SSL: WRONG_VERSION_NUMBER]`

TLS handshake problem.

- `WRONG_VERSION_NUMBER` usually means the wrong port + transport combination. Trying STARTTLS against an IMAPS port (993), or implicit TLS against a STARTTLS port (143), produces this. With `IMAP_PROVIDER=manual`:
  - port 993, no `IMAP_STARTTLS` (implicit TLS) — the default
  - port 143 with `IMAP_STARTTLS=1` (explicit upgrade)
- `CERTIFICATE_VERIFY_FAILED` on a self-hosted server usually means the server uses a self-signed cert. There is no documented `--insecure` flag in `myl`. The proper fix is to add the server's CA to the system trust store. Don't work around this for a third party's server without confirming with the user — it's a real warning.

## `imaplib.error: command SEARCH illegal in state AUTH`

`myl` tried to search before selecting a folder. Pass `--folder INBOX` (or whichever folder) explicitly.

## `BAD [CLIENTBUG]` / `Search criteria not supported`

The IMAP search expression is malformed or the server doesn't support that key. Simplify to a single quoted word and re-test:

```bash
bash scripts/imap.sh --search "invoice" --count 20
```

If a single word works, build complexity back up gradually. See the supported-keys table in `operations.md`.

## Autodiscovery (`IMAP_PROVIDER=auto`) fails

`myl --auto` couldn't determine server + port from the username domain. Switch to a specific provider mode or `manual`:

```bash
# In config:
"IMAP_PROVIDER": "yandex"   # or "gmail", "mailru", or "manual" + IMAP_SERVER
```

Common providers with their IMAP endpoints:

| Provider | Server | Port | `IMAP_PROVIDER` |
|---|---|---|---|
| Gmail | imap.gmail.com | 993 | `gmail` |
| Yandex | imap.yandex.com | 993 | `yandex` |
| Mail.ru | imap.mail.ru | 993 | `mailru` |
| iCloud | imap.mail.me.com | 993 | `manual` |
| Fastmail | imap.fastmail.com | 993 | `auto` (works) or `manual` |
| Outlook.com | outlook.office365.com | 993 | basic auth deprecated; check provider |
| Yahoo | imap.mail.yahoo.com | 993 | `manual` |
| Proton (Bridge) | 127.0.0.1 | 1143 | `manual` |

## Connection times out / hangs

- The IMAP port is blocked by a network firewall (common on corporate / hotel WiFi). Test with `nc -vz <host> 993` or `openssl s_client -connect <host>:993`.
- The server is reachable but slow. Add a timeout wrapper:
  ```bash
  timeout 30 bash scripts/imap.sh --count 5
  ```
- The server is geo-blocking. Yandex and Mail.ru sometimes throttle / block traffic from certain regions. Try from a different network or via VPN.

## "Folder not found" / `NO Mailbox does not exist`

Folder names are case-sensitive and provider-specific. Run with no `--folder` and inspect what the listing surfaces. Common gotchas:

- **Gmail:** `[Gmail]/All Mail` — exact, including brackets and space.
- **Yandex:** prefer English aliases `Sent` / `Drafts` / `Trash` over the Russian `Отправленные` / `Черновики` / `Удалённые`. Both work, but Cyrillic is sometimes UTF-7 encoded in IMAP.
- **Mail.ru:** internal IMAP names are English even when the web UI shows Russian.
- **Custom Cyrillic folders:** pass the exact string `myl` shows in listings, not the human-readable name from the web client.

## Large mailbox is slow

`--count 1000` against a large folder is going to be slow. Server response times for IMAP `FETCH` of message metadata scale roughly linearly. Cap requests at 50–100 and paginate if the user needs more.

## Wrapper says perms warning, ignores creds file

The wrapper refuses to source `~/.config/imap-client/credentials` (or `$IMAP_CREDENTIALS_FILE`) unless it's `chmod 600` or `chmod 400`. Fix:

```bash
chmod 600 ~/.config/imap-client/credentials
```

This is intentional. A world-readable creds file would be a bigger security regression than the slight inconvenience.

## `myl --version` works but commands fail mysteriously

Could be a stale install. Reinstall:

```bash
pipx reinstall myl
# or
pip install --user --upgrade --force-reinstall myl
```

If reinstall doesn't fix it, file the bug upstream at https://github.com/pschmitt/myl/issues with the failing command (passwords redacted) and `myl --version`.

## Nothing matches the symptom

Run `myl --help` to confirm the version supports the flag the user expects. Then run the command again with shell tracing on:

```bash
set -x
bash scripts/imap.sh --count 5
set +x
```

If the issue is server-side, raw `openssl s_client` against the IMAP port often surfaces the actual error:

```bash
( set +o history; openssl s_client -connect imap.yandex.com:993 -crlf )
# Then type:  a1 LOGIN you@yandex.ru app-specific-password
# CTRL+D to disconnect
```

The `set +o history` keeps the password out of the shell history file. The session itself is TLS-encrypted to the server.
