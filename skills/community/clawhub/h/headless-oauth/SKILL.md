---
name: headless-oauth
description: >
  Authorize any OAuth CLI on a headless server where the agent and the user are on
  separate machines. Use when a CLI tool requires OAuth login on a VPS or server
  without a display. Covers three patterns: (1) generate auth URL on server, user
  opens in local browser, pastes back redirect URL or code; (2) device flow — user
  enters a short code at a URL, CLI polls automatically; (3) manual callback relay —
  CLI starts a local HTTP server for the callback, user copies the failed redirect URL
  from their browser and the agent forwards it via curl. Includes agent-specific
  guidance on communicating the remote/local split to the user.
version: 1.3.0
metadata:
  openclaw:
    emoji: "🔐"
    homepage: https://github.com/IgorIvanter/headless-oauth
    requires:
      bins: []
      env: []
---

# Headless OAuth

Authorize CLI tools that require OAuth on a headless server — no browser needed on the server side.

## ⚠️ Agent Context: You Are on a Remote Server

**You (the agent) are running on a remote VPS. The user is on a separate local machine with a browser.**

This means:
- You cannot open a browser yourself
- The server's `localhost` is NOT accessible from the user's browser
- The user must open all auth URLs on their own machine
- When a redirect goes to a local address like `http://127.0.0.1:PORT/callback?code=...`, it will **fail to load** in the user's browser — that is expected and normal
- The user should copy the full URL from the address bar (even if the page shows an error) and send it to you
- You then forward that URL to the waiting server process via `curl`

Always make this explicit when asking the user to authorize. Example:
> "Open this URL in your browser, log in, and approve. The page will likely fail to load — that's fine. Copy the full URL from the address bar and send it to me."

---

## The Pattern

Split the browser flow across two machines:

```
SERVER                          LOCAL MACHINE
------                          -------------
1. Generate auth URL    →       2. Open URL in browser
                                3. Log in + grant permissions
                                4. Copy redirect URL or code
5. Exchange for token   ←
6. Store token locally
```

Most OAuth CLIs support this via flags like:
- `--no-launch-browser` — gh (GitHub CLI), gcloud
- `--remote --step 1/2` — gog (Google Workspace CLI)
- `--manual` — some generic CLIs
- Device flow (code + URL, no redirect) — gh, some others

---

## Keyring on Headless Servers

Many CLIs store tokens in a system keyring that requires an interactive terminal session to unlock.
Check the CLI's documentation for a flag or environment variable that sets the keyring password
non-interactively. Set it only for the duration of the auth step — do not persist it in shell
configs or agent-global environment. Prefer injecting it from a secrets manager or an ephemeral
shell session.

---

## Google Workspace — gog CLI

gog supports headless auth via `--remote --step 1/2`. See the [official gog docs](https://github.com/steipete/gogcli) for setup details.

> **Important:** Use **Desktop app** OAuth client type in Google Cloud Console — not Web application.
> gog uses a random port for the callback, which Web clients reject with `redirect_uri_mismatch`.

---

## GitHub CLI — gh

```bash
gh auth login --hostname github.com --git-protocol https --no-launch-browser
# → prints a one-time code and a URL
# Open https://github.com/login/device locally, enter the code
# gh polls and completes automatically once you approve
```

---

## gcloud (Google Cloud CLI)

```bash
gcloud auth login --no-launch-browser
# → prints a URL
# Open in local browser, log in, copy the verification code shown, paste back
```

---

## Generic Device Flow

If a CLI supports device flow (prints a short code + URL):

1. Note the code and URL printed by the CLI
2. Open the URL on any device
3. Enter the code
4. CLI polls and completes automatically — no redirect URL to copy

---

## Manual Callback Relay (mcporter, custom OAuth servers)

Some tools (e.g. `mcporter`) start a local HTTP server on the server to catch the OAuth callback,
but the user's browser can't reach that address on the remote server.

**How to handle it:**

1. Start the auth command with a longer timeout so it doesn't expire while waiting for the user.
   Check the tool's docs for a timeout flag or environment variable.
2. The tool usually prints a message like:
   ```
   If the browser did not open, visit https://... manually.
   ```
   Send that URL to the user.
3. Tell the user:
   > "Open this URL, log in and approve. The page will fail to load — that's normal. Copy the full URL from the address bar and send it to me."
4. The user sends back something like:
   `http://127.0.0.1:PORT/callback?code=...&state=...`
5. Forward it to the waiting server with curl:
   ```bash
   curl -s "http://127.0.0.1:PORT/callback?code=...&state=..."
   ```
6. The tool receives the code, exchanges it for a token, and completes authorization.

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `redirect_uri_mismatch` | Use Desktop app OAuth client, not Web application |
| No TTY / keyring unlock fails | Check the CLI's docs for a non-interactive keyring option |
| `Access blocked` (testing mode) | Add your email as test user in Google consent screen settings |
| Commands fail silently | Check if the CLI requires an account env var to be set |
| Token expired | Re-run auth steps; most CLIs handle refresh automatically |

---

## Applying This Pattern to Any CLI

1. Check `--help` for flags like `--no-launch-browser`, `--remote`, `--manual`, or `--headless`
2. Check docs for "device flow" or "offline access"
3. If the tool starts a local callback server but has no headless flag — use the Manual Callback Relay pattern above
4. If none of the above work: use `ssh -L` port forwarding to tunnel the callback to your local machine
