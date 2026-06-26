# SFTP on macOS

macOS already ships with OpenSSH and SFTP support. For local staging, that is usually enough.

## Recommended Pattern

- enable Remote Login
- use a dedicated staging user when possible
- keep project files in a path that user owns
- use SFTP for upload/sync jobs
- keep shell access narrower than file access when the workflow allows it

## Enablement

GUI path:

- System Settings
- General
- Sharing
- Remote Login

CLI path:

```bash
sudo systemsetup -setremotelogin on
```

## Verification

```bash
systemsetup -getremotelogin
nc -z 127.0.0.1 22
sftp user@127.0.0.1
```

## Security Notes

- Do not expose the Mac staging server directly to the public internet
- Prefer LAN-only or Tailscale access
- Avoid sharing your primary admin account for routine deploys
- If a deploy process only needs file sync, use SFTP instead of broader remote automation
