# Gmail IMAP

OpenClaw skill for reading, searching, sending, and managing Gmail via IMAP.

## Author

Scott Glover <scottgl@gmail.com>  
ClawHub: [@scottgl9](https://clawhub.ai/scottgl9)

## Requirements

Set these environment variables before use:

| Variable | Description |
|----------|-------------|
| `GMAIL_IMAP_USER` | Your Gmail address |
| `GMAIL_IMAP_PASSWORD` | A Google App Password (not your account password) |

Generate an App Password at: https://myaccount.google.com/apppasswords (requires 2FA)

## Usage

```bash
SCRIPT="$SKILL_DIR/scripts/gmail_imap.py"

python3 "$SCRIPT" list                          # List inbox (20 most recent)
python3 "$SCRIPT" list --search UNSEEN          # Unread only
python3 "$SCRIPT" read <uid>                    # Read a message
python3 "$SCRIPT" trash <uid>                   # Delete (move to Trash)
python3 "$SCRIPT" move <uid> "Label"            # Move to folder/label
python3 "$SCRIPT" send --to x@y.com --subject "Hi" --body "Hello"
```

## Notes

- Uses IMAP/SMTP directly — no Google API key required
- Deletion uses `[Gmail]/Trash` (correct Gmail behavior, not IMAP archive)
- See `references/gmail-imap-reference.md` for full search syntax and folder names

## License

MIT-0 — free to use, modify, and redistribute without attribution.
