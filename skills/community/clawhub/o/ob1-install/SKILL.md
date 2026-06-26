---
name: ob1-install
description: Install and authenticate OB1 (OpenBlock One), a multi-model terminal coding agent. Use when asked to install OB1, set up ob1, or when ob1 authentication/login is needed. Covers macOS/Linux install, device code authentication flow, and post-install verification.
---

# OB1 Install & Authentication

## Install

```bash
curl -fsSL https://dashboard.openblocklabs.com/install | bash
```

Installs to `~/.ob1/bin/ob1`, symlinks to `~/.local/bin/ob1`.

Verify: `ob1 --version`

## Authentication

OB1 uses device code flow. Run `ob1` and it will display:

```
To sign in: https://auth.openblocklabs.com/device
Enter code: XXXX-XXXX
```

**Headless/server workflow:**
1. Start ob1 with PTY: the auth URL and code appear in terminal
2. Send the code to user (via chat) — they open the URL in their browser
3. User signs in and approves
4. OB1 shows "Authentication Successful!" and asks to confirm organization
5. Press Enter to confirm — auth token saved to `~/.ob1/`

**Important:** Each `ob1` process generates a unique code. If the process dies, a new code is needed. Keep the process alive until user confirms.

After first auth, all subsequent runs skip login.

## Post-Install

- Default model: Claude Opus 4.6
- Default mode: Safe YOLO
- Config: `~/.ob1/settings.json`
- Non-interactive: `ob1 -p "task" -y -o text`
