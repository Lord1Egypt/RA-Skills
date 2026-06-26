# Outlook CLI

Command-line email client for Microsoft Outlook/Live/Hotmail using Microsoft Graph API.

## Prerequisites

- Python 3.6+
- `requests` library: `pip install requests`
- Azure AD App Registration (see Setup below)

## Setup

### 1. Create Azure AD App

1. Go to https://portal.azure.com
2. Navigate to **App registrations** → **New registration**
3. Set the following:
   - **Name**: `outlook-cli`
   - **Supported account types**: "Personal Microsoft accounts only" (or "Accounts in any organizational directory and personal Microsoft accounts")
   - **Redirect URI**: Select "Web" and enter `http://localhost:8080/callback`
4. Click **Register**
5. Copy the **Application (client) ID**
6. Go to **Certificates & secrets** → **New client secret**
7. Copy the **Secret value** (not the Secret ID)

### 2. Configure CLI

Run the configuration command and enter your credentials:

```bash
./outlook configure
```

Enter the Client ID and Client Secret when prompted.

### 3. Authenticate

```bash
./outlook auth
```

This will open your browser for authentication. Sign in with your Microsoft account and grant permissions.

## Usage

### Check Status

```bash
./outlook status
```

### List Emails

```bash
# List 10 recent emails (default)
./outlook list

# List 20 recent emails
./outlook list 20
```

### Search Emails

```bash
# Search by keyword
./outlook search "meeting"

# Search with operators
./outlook search "from:john@example.com"
./outlook search "subject:invoice"

# Search and limit results
./outlook search "important" 5
```

### Read Email

```bash
# Read email by ID (use short ID from list)
./outlook read abc12345
```

### Send Email

```bash
# Simple email
./outlook send --to "recipient@example.com" --subject "Hello" --body "This is a test"

# Email with CC
./outlook send --to "user1@example.com,user2@example.com" --cc "boss@example.com" --subject "Update" --body "Weekly update"

# Email with body from file
./outlook send --to "recipient@example.com" --subject "Report" --body-file ./report.txt
```

### Reply to Email

```bash
# Reply to sender
./outlook reply abc12345 --body "Thank you!"

# Reply to all
./outlook reply abc12345 --all --body "Thanks everyone!"
```

## Search Operators

When using the `search` command, you can use these operators:

- `from:email@domain.com` - Filter by sender
- `to:email@domain.com` - Filter by recipient
- `subject:keyword` - Search in subject line
- `body:keyword` - Search in email body
- `received:YYYY-MM-DD` - Filter by date
- `hasattachment:yes` - Filter emails with attachments

## Configuration Files

Configuration and tokens are stored in:
- **Config**: `~/.config/outlook-cli/config.json`
- **Token**: `~/.config/outlook-cli/token.json`

## Troubleshooting

### Authentication Issues

If you get authentication errors:

1. Delete token file: `rm ~/.config/outlook-cli/token.json`
2. Re-authenticate: `./outlook auth`

### Permission Errors

Make sure your Azure AD app has the following API permissions:
- `Mail.Read`
- `Mail.Send`
- `Mail.ReadWrite`
- `User.Read`

### Token Expired

The CLI automatically refreshes tokens. If refresh fails, re-authenticate:

```bash
./outlook auth
```

## API Rate Limits

Microsoft Graph API has rate limits. If you hit limits, the CLI will return an error. Wait a few minutes and try again.

## Security Notes

- Never share your Client Secret or token files
- The token file contains sensitive access tokens
- Consider using App-only authentication for production use

## License

MIT License
