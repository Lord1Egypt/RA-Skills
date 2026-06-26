# zoho-mail

![Language](https://img.shields.io/badge/language-Go-00ADD8?logo=go&logoColor=white)
![License](https://img.shields.io/badge/license-MIT--0-green)
![Platform](https://img.shields.io/badge/platform-linux%2Farm64-lightgrey)

A custom OpenClaw skill providing full read/write access to a Zoho Mail account (EU data centre).

## Services

| Service | Scopes | Access |
|---------|--------|--------|
| Mail | `ZohoMail.messages.ALL` | List, read, send, reply, delete, mark read/unread |
| Folders | `ZohoMail.folders.ALL` | List |
| Accounts | `ZohoMail.accounts.READ` | Account ID discovery |

## Installation

```bash
clawhub install panthrocorp-zoho-mail
```

Or build from source:

```bash
GOOS=linux GOARCH=arm64 CGO_ENABLED=0 go build -o zoho-mail .
```

## Deployment guide

Follow these steps in order to deploy the skill to an OpenClaw instance.

### 1. Create a Zoho API Console application

1. Go to the [Zoho API Console](https://api-console.zoho.eu/) (EU region)
2. Create a **Server-based Application**
3. Set the redirect URL to `http://localhost:8080/callback`
4. Note the **Client ID** and **Client Secret**

### 2. Create secrets in Bitwarden Secrets Manager

Create three secrets in Bitwarden SM (EU region, PanthroCorp project):

| Secret key | Value |
|------------|-------|
| `ZOHO_MAIL_TOKEN_KEY_OPENCLAW_AWS_SANDBOX_<INSTANCE>` | Random 64-character hex string (`openssl rand -hex 32`) |
| `ZOHO_CLIENT_ID_OPENCLAW_AWS_SANDBOX_<INSTANCE>` | Client ID from step 1 |
| `ZOHO_CLIENT_SECRET_OPENCLAW_AWS_SANDBOX_<INSTANCE>` | Client secret from step 1 |

### 3. Add Terraform configuration

In the `openclaw` repo, add the Bitwarden secret key references to the instance's tfvars file:

```hcl
bitwarden_secret_key_zoho_mail_token_key = "ZOHO_MAIL_TOKEN_KEY_OPENCLAW_AWS_SANDBOX_<INSTANCE>"  # pragma: allowlist secret
bitwarden_secret_key_zoho_client_id      = "ZOHO_CLIENT_ID_OPENCLAW_AWS_SANDBOX_<INSTANCE>"  # pragma: allowlist secret
bitwarden_secret_key_zoho_client_secret  = "ZOHO_CLIENT_SECRET_OPENCLAW_AWS_SANDBOX_<INSTANCE>"  # pragma: allowlist secret
```

### 4. Deploy

Merge the Terraform changes to `main`. The deploy workflow will:
- Create SSM parameters for the three secrets
- Update the `.env` file on the instance with `ZOHO_MAIL_TOKEN_KEY`, `ZOHO_CLIENT_ID`, and `ZOHO_CLIENT_SECRET`
- Create the `config/credentials/zoho-mail/` directory

### 5. Install the skill on the instance

SSH in via Twingate and install:

```bash
ssh -i ~/.ssh/openclaw-operator ubuntu@<domain>
sudo -u openclaw docker exec -it openclaw-gateway clawhub install panthrocorp-zoho-mail
```

### 6. Set the account email

```bash
sudo -u openclaw docker exec -it openclaw-gateway \
  zoho-mail config set --email your@zoho.com
```

### 7. Authenticate with Zoho

```bash
sudo -u openclaw docker exec -it openclaw-gateway \
  zoho-mail auth login
```

1. Copy the URL printed to the terminal
2. Open it in your local browser and authenticate with your Zoho account
3. After authorisation, copy the full redirect URL from your browser's address bar (it will start with `http://localhost:8080/callback?code=...`)
4. Paste the full URL back into the terminal

### 8. Verify

```bash
sudo -u openclaw docker exec -it openclaw-gateway zoho-mail auth status
sudo -u openclaw docker exec -it openclaw-gateway zoho-mail folders list
```

No container restart is needed. The token is persisted on the host volume and the binary reads it fresh on each invocation.

## Prerequisites

- A Zoho API Console application (EU region) with redirect URL `http://localhost:8080/callback`
- Three environment variables on the host:
  - `ZOHO_CLIENT_ID` and `ZOHO_CLIENT_SECRET` from the API Console application
  - `ZOHO_MAIL_TOKEN_KEY` for encrypting the stored OAuth token (random 64-char hex string)

## Usage

### Configure

```bash
zoho-mail config set --email your@zoho.com
zoho-mail config show
```

### Authenticate

```bash
zoho-mail auth login
```

This prints a URL. Open it in your browser, authorise the requested scopes, then paste the full redirect URL back into the terminal.

### Mail

```bash
# List inbox
zoho-mail mail list
zoho-mail mail list --folder FOLDER_ID --limit 20 --start 0

# Read a message
zoho-mail mail read --id MESSAGE_ID

# Send
zoho-mail mail send --to recipient@example.com --subject "Hello" --body "Message body"
zoho-mail mail send --to recipient@example.com --subject "Hello" --body "<p>HTML body</p>" --html
zoho-mail mail send --to recipient@example.com --cc cc@example.com --subject "Hello" --body "Body"

# Reply
zoho-mail mail reply --id MESSAGE_ID --body "Reply text"
zoho-mail mail reply --id MESSAGE_ID --body "<p>HTML reply</p>" --html

# Search
zoho-mail mail search --query "from:someone@example.com"
zoho-mail mail search --query "subject:invoice" --limit 20

# Delete
zoho-mail mail delete --id MESSAGE_ID --folder FOLDER_ID

# Mark read/unread
zoho-mail mail mark --ids id1,id2,id3 --read
zoho-mail mail mark --ids id1 --unread
```

### Folders

```bash
zoho-mail folders list
```

### Check auth status

```bash
zoho-mail auth status
```

## Token storage

OAuth tokens are encrypted at rest using AES-256-GCM with a key derived via HKDF-SHA256. The encryption key comes from `ZOHO_MAIL_TOKEN_KEY`, injected from an external secret manager. The binary refuses to store tokens if this variable is not set.

Default token location: `~/.openclaw/credentials/zoho-mail/token.enc`

Refreshed tokens are automatically written back to disk by the `persistingTokenSource` wrapper on each token refresh, so the stored token stays current across invocations without requiring manual re-authentication.

## Security

- Token encryption uses a random salt per operation, preventing identical tokens from producing identical ciphertext.
- The binary exits immediately if any required environment variable is absent.
- Running `zoho-mail auth revoke` removes the local token only. To fully revoke access, also visit [Zoho account sessions](https://accounts.zoho.eu/home#sessions).

## Development

```bash
go build -o zoho-mail .
go test ./...
go vet ./...
```

## License

[MIT No Attribution](./LICENSE)
