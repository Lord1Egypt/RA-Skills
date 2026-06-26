---
name: gmail-gog-setup
description: Set up Gog CLI for Gmail access and authenticate agent mailboxes.
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "bins": ["gog"] },
        "install": [],
      },
  }
---

# Gmail + Gog Setup

Use this skill when you need to give an agent (e.g., Facet, competitions agent) access to a Gmail inbox via Gog CLI.

## When to use

- Creating a new agent mailbox (e.g., facet.ai.oc@gmail.com)
- Setting up Gmail reading capability for an existing agent
- Troubleshooting Gog auth failures
- Adding new OAuth clients or test users

## Prerequisites

### 1. Google Cloud OAuth client
- Create a **Desktop app** OAuth client in Google Cloud Console
- Enable **Gmail API**
- Add target Gmail address as a **test user** in OAuth consent screen
- Download the client JSON file

### 2. Gog installed
```bash
# Install Gog from latest release
cd /tmp
curl -L -o gogcli_0.12.0_linux_amd64.tar.gz https://github.com/steipete/gogcli/releases/download/v0.12.0/gogcli_0.12.0_linux_amd64.tar.gz
tar -xzf gogcli_0.12.0_linux_amd64.tar.gz
install -m 0755 gog /usr/local/bin/gog
```

## Steps

### 1. Store OAuth credentials
```bash
gog auth credentials /path/to/client_secret_....json
```

### 2. Authenticate the Gmail account
```bash
export GOG_KEYRING_PASSWORD='your-keyring-password'
gog auth add agent@gmail.com --services gmail --manual
```
- Open the provided auth URL in browser
- Log in as the target Gmail account
- Approve requested permissions
- Copy the redirect URL (localhost) after Google redirects
- Paste it into the waiting Gog prompt

### 3. Verify access
```bash
gog auth list
gog gmail messages search 'newer_than:7d' --account agent@gmail.com --json
```

### 4. Check spam
New senders often land in spam:
```bash
gog gmail messages search 'in:spam newer_than:7d' --account agent@gmail.com --json
```

## Common issues

### "No auth for gmail"
- Verify test user is added in Google Cloud OAuth consent screen
- Re-run auth with `--force-consent` if needed

### "state mismatch"
The auth session restarted. Use the latest auth URL and callback.

### "no TTY available for keyring file backend"
Set `GOG_KEYRING_PASSWORD` environment variable before running `gog auth add`.

### Emails going to spam
- Move from spam to inbox: `gog gmail messages modify <msg_id> --remove SPAM --add INBOX`
- Consider training Gmail by marking as "Not spam"

## Notes

- Store OAuth client JSON in `~/.openclaw/credentials/google/`
- Keep `GOG_KEYRING_PASSWORD` in a secure environment variable or secret manager
- For production, consider service account with domain-wide delegation instead of OAuth
- Always check spam folder for important verification/API emails

## References

- [Gog CLI](https://gogcli.sh/)
- [Google Cloud OAuth setup](https://console.cloud.google.com/)
- [OpenClaw Gmail Pub/Sub docs](/automation/gmail-pubsub.md)
