# one-mail - Unified Email Management Tool

English | [中文](./README.md)

A command-line tool for managing multiple email accounts (Gmail, Outlook, NetEase Mail 163/126) from a single interface.

## Installation

### Method 1: Install via ClawHub (Recommended)

```bash
# Install
clawhub install one-mail

# Initialize configuration
bash scripts/setup.sh
```

### Method 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/huangbaixun/one-mail.git
cd one-mail

# Initialize configuration
bash scripts/setup.sh
```

## Quick Start

### 1. Initialize Configuration

```bash
bash scripts/setup.sh
```

Follow the prompts to add your email accounts.

### 2. Fetch Emails

```bash
# Fetch emails from all accounts
bash scripts/fetch.sh

# Unread emails only
bash scripts/fetch.sh --unread

# Search emails
bash scripts/fetch.sh --query "AI agent"

# Specific account
bash scripts/fetch.sh --account gmail
```

### 3. Send Emails

```bash
# Send using default account
bash scripts/send.sh \
  --to "recipient@example.com" \
  --subject "Hello" \
  --body "Email content"

# With attachment
bash scripts/send.sh \
  --to "recipient@example.com" \
  --subject "Report" \
  --body "See attachment" \
  --attach "/path/to/file.pdf"
```

## Supported Email Providers

### Gmail
- ✅ Fetch emails
- ✅ Send emails
- ✅ Attachment support
- ✅ Search & filter
- Requires: `gog` CLI (pre-configured)

### Outlook
- ✅ Fetch emails
- ✅ Send emails
- ✅ Attachment support (< 3MB)
- ✅ Search & filter
- Requires: Microsoft Graph API

### NetEase Mail (163.com / 126.com)
- ✅ Fetch emails
- ✅ Send emails
- ✅ Attachment support
- ✅ Search & filter
- ✅ IMAP ID support (automatic client identification)
- Requires: Python 3 + imaplib
- 163 servers: imap.163.com / smtp.163.com
- 126 servers: imap.126.com / smtp.126.com

## Configuration Files

Configuration files are stored in `~/.onemail/`:

- `config.json` - Account configuration
- `credentials.json` - Sensitive credentials (600 permissions)

## Account Management

```bash
# List all accounts
bash scripts/accounts.sh list

# Add new account
bash scripts/accounts.sh add

# Remove account
bash scripts/accounts.sh remove --name outlook

# Set default account
bash scripts/accounts.sh set-default --name gmail

# Test account connection
bash scripts/accounts.sh test --name gmail
```

## Advanced Usage

### Scheduled Email Checks

Add to crontab:

```bash
# Check unread emails every hour
0 * * * * bash scripts/fetch.sh --unread | jq -r '.[] | "\(.from): \(.subject)"'
```

### Auto-Reply

```bash
# Reply to latest urgent email
bash scripts/fetch.sh --query "urgent" --limit 1 | \
  jq -r '.[0].id' | \
  xargs -I {} bash scripts/send.sh \
    --reply-to {} \
    --body "I'll get back to you soon"
```

### Cross-Account Search

```bash
# Search for "invoice" across all accounts
bash scripts/fetch.sh --query "invoice" | \
  jq -r '.[] | "\(.account) - \(.from): \(.subject)"'
```

## Output Format

All emails are output in JSON format:

```json
[
  {
    "id": "msg_123",
    "account": "gmail",
    "from": "sender@example.com",
    "to": "you@gmail.com",
    "subject": "Meeting tomorrow",
    "date": "2026-03-07T10:30:00Z",
    "unread": true,
    "has_attachments": false,
    "snippet": "Let's meet at 3pm..."
  }
]
```

Use `jq` for filtering and formatting.

## Security

- All credentials stored in `~/.onemail/credentials.json` (600 permissions)
- macOS Keychain support (optional)
- OAuth 2.0 authentication (Gmail, Outlook)
- App-specific passwords (NetEase Mail)

## Troubleshooting

### Gmail Connection Failed

Ensure `gog` CLI is properly configured:

```bash
gog gmail list --limit 1
```

### Outlook Authorization Failed

1. Check Client ID and Client Secret
2. Ensure redirect URI is set to `http://localhost`
3. Ensure authorization scope includes `Mail.ReadWrite` and `Mail.Send`

### NetEase Mail Connection Failed

1. Ensure IMAP/SMTP service is enabled
2. Use app-specific password, not login password
3. Check if firewall blocks ports 993/465
4. **IMAP ID Issue**: one-mail automatically sends IMAP ID command, complying with NetEase Mail requirements

**Test NetEase Mail connection**:
```bash
python3 scripts/test-163-imap.py your@163.com your_app_password
```

## Dependencies

- `bash` 4.0+
- `jq` - JSON processing
- `curl` - HTTP requests
- `openssl` - SSL/TLS connections
- `python3` - IMAP/SMTP handling (NetEase Mail)
- `gog` - Gmail operations (optional)

## Limitations

- Outlook attachment size limit: < 3MB (direct attach), use OneDrive sharing for larger files
- Exchange Server not supported (Outlook.com only)
- NetEase Mail connection test pending
- HTML email editing not supported (plain text only)

## Changelog

- 2026-03-07: Initial release
  - Support for Gmail, Outlook, NetEase Mail
  - Unified fetch/send interface
  - Account management
  - JSON output format

## License

MIT License

## Author

Huang Baixun ([@huangbaixun](https://github.com/huangbaixun))

---

## Installation

### As OpenClaw Skill

```bash
# Install from ClawHub (coming soon)
clawhub install one-mail

# Or clone manually
git clone https://github.com/yourusername/one-mail.git ~/clawd/skills/one-mail
cd ~/clawd/skills/one-mail
bash setup.sh
```

### Standalone Usage

```bash
# Clone repository
git clone https://github.com/yourusername/one-mail.git
cd one-mail

# Run setup
bash setup.sh

# Use directly
bash fetch.sh --help
bash send.sh --help
```

## Examples

### Example 1: Daily Email Digest

```bash
#!/bin/bash
# daily-digest.sh - Send yourself a daily email summary

TODAY=$(date +%Y-%m-%d)
EMAILS=$(bash scripts/fetch.sh --unread --limit 20)

COUNT=$(echo "$EMAILS" | jq 'length')
SUMMARY=$(echo "$EMAILS" | jq -r '.[] | "- \(.from): \(.subject)"')

bash scripts/send.sh \
  --to "yourself@example.com" \
  --subject "Daily Email Digest - $TODAY" \
  --body "You have $COUNT unread emails:

$SUMMARY"
```

### Example 2: Email Backup

```bash
#!/bin/bash
# backup-emails.sh - Backup all emails to JSON

BACKUP_DIR="$HOME/email-backups"
mkdir -p "$BACKUP_DIR"

for account in gmail outlook 163; do
  echo "Backing up $account..."
  bash scripts/fetch.sh \
    --account "$account" \
    --limit 1000 \
    > "$BACKUP_DIR/$account-$(date +%Y%m%d).json"
done

echo "Backup complete!"
```

### Example 3: Smart Forwarding

```bash
#!/bin/bash
# forward-important.sh - Forward important emails to another account

bash scripts/fetch.sh --query "urgent OR important" | \
  jq -r '.[] | @json' | \
  while IFS= read -r email; do
    SUBJECT=$(echo "$email" | jq -r '.subject')
    FROM=$(echo "$email" | jq -r '.from')
    BODY=$(echo "$email" | jq -r '.snippet')
    
    bash scripts/send.sh \
      --to "backup@example.com" \
      --subject "FWD: $SUBJECT" \
      --body "From: $FROM

$BODY"
  done
```

## API Reference

### fetch.sh

Fetch emails from configured accounts.

**Options:**
- `--account <name>` - Fetch from specific account
- `--unread` - Unread emails only
- `--limit <n>` - Maximum number of emails (default: 10)
- `--query <text>` - Search query
- `--json` - Output in JSON format (default)

**Output:**
JSON array of email objects.

### send.sh

Send email from configured account.

**Options:**
- `--account <name>` - Send from specific account (default: first account)
- `--to <email>` - Recipient email address (required)
- `--subject <text>` - Email subject (required)
- `--body <text>` - Email body (required)
- `--attach <path>` - Attachment file path (optional)
- `--cc <email>` - CC recipient (optional)
- `--bcc <email>` - BCC recipient (optional)

**Output:**
Success/error message.

### accounts.sh

Manage email accounts.

**Commands:**
- `list` - List all configured accounts
- `add` - Add new account (interactive)
- `remove --name <name>` - Remove account
- `set-default --name <name>` - Set default account
- `test --name <name>` - Test account connection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- GitHub Issues: [coming soon]
- OpenClaw Discord: https://discord.com/invite/clawd

## Roadmap

- [ ] Outlook attachment support
- [ ] Exchange Server support
- [ ] More email providers (Yahoo, iCloud, etc.)
- [ ] HTML email support
- [ ] Email templates
- [ ] Batch operations
- [ ] Email rules and filters
- [ ] Calendar integration
- [ ] Contact management
