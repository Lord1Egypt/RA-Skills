---
name: linkedin-cli
description: Post to LinkedIn using the official API v2. Uses OAuth tokens so only post when explicitly asked or scheduled.
homepage: https://github.com/0xmythril/linkedin-cli
metadata: {"openclaw":{"emoji":"💼","requires":{"bins":["linkedin-cli"],"env":["LINKEDIN_CLIENT_ID","LINKEDIN_CLIENT_SECRET","LINKEDIN_ACCESS_TOKEN"]},"install":[{"id":"npm","kind":"shell","command":"npm install -g github:0xmythril/linkedin-cli#v1.0.0","bins":["linkedin-cli"],"label":"Install linkedin-cli v1.0.0 (npm)"}]}}
---

# linkedin-cli

Post to LinkedIn using the official API v2. This tool is rate-limited by LinkedIn, so **only use it when the user explicitly asks you to post, or during scheduled cron tasks**. Do not speculatively draft and post content.

## Setup

1. Install (pinned to release tag):
```bash
npm install -g github:0xmythril/linkedin-cli#v1.0.0
```
2. Create a LinkedIn app at https://www.linkedin.com/developers/apps
   - Enable **Sign In with LinkedIn using OpenID Connect** and **Share on LinkedIn** products
   - Add `http://localhost:8585/callback` to **Authorized redirect URLs**
3. Configure credentials (file is created with restricted permissions):
```bash
mkdir -p ~/.config/linkedin-cli
touch ~/.config/linkedin-cli/.env
chmod 600 ~/.config/linkedin-cli/.env
cat > ~/.config/linkedin-cli/.env << 'EOF'
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
EOF
```
4. Authenticate (opens browser for OAuth):
```bash
linkedin-cli auth
```
5. Verify: `linkedin-cli whoami`

## Security

- **Credentials**: Stored in `~/.config/linkedin-cli/.env` (read by `dotenv` at runtime). Set `chmod 600` to restrict access.
- **No postinstall scripts**: The package has zero install scripts — verify via `npm pack --dry-run` or inspect `package.json`.
- **No telemetry or network calls** except to the official LinkedIn API (`api.linkedin.com`) and OAuth (`www.linkedin.com`) when you run a command.
- **Pinned install**: The install command pins to a specific release tag. Audit the source at https://github.com/0xmythril/linkedin-cli before installing.
- **Dependencies**: Only 3 runtime deps — `commander` (CLI parsing), `dotenv` (env file loading), `open` (browser launch for OAuth). No transitive dependencies beyond these.

## Commands

### Verify auth
```bash
linkedin-cli whoami
```

### Authenticate
```bash
linkedin-cli auth
```

### Post a text update
```bash
linkedin-cli post "Your post text here"
```

### Share a URL with commentary
```bash
linkedin-cli share "https://example.com/article" "Your commentary here"
```

### Delete a post
```bash
linkedin-cli delete <post-id-urn-or-url>
linkedin-cli delete https://www.linkedin.com/feed/update/urn:li:activity:7654321/
```

## Important rules

- **Do NOT post unless the user explicitly asks or a cron job triggers it.** LinkedIn rate-limits API usage.
- **Always confirm with the user** before posting or sharing. Show them the text first.
- **Keep posts professional** — LinkedIn is a professional network.
- linkedin-cli accepts raw numeric IDs, full URNs, and LinkedIn post URLs.
- If you get a 401 error, the token has expired (~60 days). Ask the user to run `linkedin-cli auth` to re-authenticate.
- This tool is for **posting only**. It cannot read feeds, search profiles, or send messages.
