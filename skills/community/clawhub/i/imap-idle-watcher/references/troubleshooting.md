# Troubleshooting

## Common Errors

### "Auth failed" / "Invalid credentials"
- Using regular password instead of app password
- App password has spaces → remove them or keep them (Gmail accepts both)
- Account has 2FA disabled (required for app passwords on Gmail)
- Typo in email address

### "Connection refused" / timeout
- Wrong IMAP host or port
- Firewall blocking port 993
- Check: `openssl s_client -connect imap.gmail.com:993`

### "IDLE not supported"
- Rare — most major providers support IDLE
- Some corporate IMAP proxies strip IDLE capability
- Fallback: set short `IDLE_TIMEOUT` (e.g. 60s) — daemon polls on timeout

### Service starts but stops immediately
- Check logs: `journalctl -u <service-name> --no-pager -n 50`
- Usually a credential or connection issue
- Env file permissions wrong → must be readable by the service user

### Command runs but does nothing
- Test command manually first: `MAIL_FROM="test" MAIL_SUBJECT="test" your-command`
- Check command path is absolute
- Shell expansion may not work — use full paths

## Useful Commands

```bash
# Test connection without installing
./setup_service.sh --test --account you@gmail.com --password "xxxx xxxx xxxx xxxx"

# Watch logs live
journalctl -u imap-idle-watcher -f

# Restart after config change
systemctl restart imap-idle-watcher

# Check env file
cat /etc/imap-idle-watcher.env
```

## Email Metadata Available to Commands

When `ON_NEW_MAIL_CMD` runs, these env vars are set (if available):

| Variable | Example |
|----------|---------|
| `MAIL_FROM` | `John Doe <john@example.com>` |
| `MAIL_SUBJECT` | `Your order has shipped` |
| `MAIL_DATE` | `Mon, 17 Mar 2026 10:30:00 +0700` |
| `MAIL_UID` | `12345` |
