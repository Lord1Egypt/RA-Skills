# Setup Guide — n8n Instance Configuration

Follow this guide to get your n8n instance ready to work
with the OpenClaw n8n Automation Skill.

---

## Option A — n8n Cloud (Easiest, 5 minutes)

1. Go to app.n8n.cloud and sign up for free trial
2. Your webhook base URL will be:
   `https://[your-username].app.n8n.cloud/webhook`
3. Go to Settings → API → Create API Key
4. Copy the API key
5. Export both in terminal:

```bash
export N8N_WEBHOOK_BASE_URL="https://yourusername.app.n8n.cloud/webhook"
export N8N_API_KEY="your-api-key-here"
```

---

## Option B — Self-Hosted n8n on VPS (Best for Privacy)

**Step 1 — Install n8n on your VPS:**
```bash
npm install -g n8n
```

**Step 2 — Start n8n with a domain:**
```bash
N8N_BASIC_AUTH_ACTIVE=true \
N8N_BASIC_AUTH_USER=admin \
N8N_BASIC_AUTH_PASSWORD=yourpassword \
WEBHOOK_URL=https://your-domain.com \
n8n start
```

**Step 3 — Your webhook base URL:**
`https://your-domain.com/webhook`

**Step 4 — Get API key:**
Go to n8n UI → Settings → API → Generate API Key

**Step 5 — Export variables:**
```bash
export N8N_WEBHOOK_BASE_URL="https://your-domain.com/webhook"
export N8N_API_KEY="your-api-key-here"
```

---

## Option C — n8n with Docker (Most Reliable)

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=yourpassword \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

Access at `http://localhost:5678`

---

## Making Variables Permanent

Add to your shell profile so they survive restarts:

**Mac/Linux (~/.zshrc or ~/.bashrc):**
```bash
echo 'export N8N_WEBHOOK_BASE_URL="https://your-n8n.com/webhook"' >> ~/.zshrc
echo 'export N8N_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**Then restart OpenClaw gateway:**
```bash
openclaw gateway restart
```

---

## Import All 8 Workflow Templates

1. Open your n8n instance
2. For each workflow in `/references/n8n-workflow-templates.md`:
   - Click "New Workflow"
   - Menu → Import from JSON
   - Paste the template JSON
   - Connect your credentials
   - Activate the workflow
3. Your webhook URLs will all follow the pattern:
   `$N8N_WEBHOOK_BASE_URL/[workflow-path]`

---

## Required n8n Credentials

Set up these credentials in n8n (Settings → Credentials):

| Credential | Used By | Where to Get |
|------------|---------|--------------|
| Gmail OAuth2 | Workflows 1, 3, 6 | Google Cloud Console |
| Google Sheets | Workflows 1, 4, 8 | Google Cloud Console |
| LinkedIn | Workflow 2 | LinkedIn Developer Portal |
| Twitter/X | Workflow 2 | Twitter Developer Portal |
| OpenAI or Anthropic | Workflows 5, 7, 8 | Platform API Console |
| Airtable (optional) | Workflow 4 | Airtable Account Settings |

---

## Testing Your Setup

After setup, test each workflow by telling your agent:

```
"n8n status"
```

Should return all 8 workflows as active.

Then test a real trigger:

```
"Send a test lead nurture to test@example.com, name is Test User"
```

Check your n8n execution logs to confirm it received the webhook.

---

## Troubleshooting

**"Connection refused" error:**
- Check your N8N_WEBHOOK_BASE_URL has no trailing slash
- Make sure n8n is running and workflows are activated
- Test the URL directly: `curl $N8N_WEBHOOK_BASE_URL/health`

**"401 Unauthorized" error:**
- Check your N8N_API_KEY is correct
- Regenerate the API key in n8n Settings if needed

**"Workflow not found" error:**
- Make sure the webhook path in n8n matches exactly
- Paths are case-sensitive: `lead-nurture` not `Lead-Nurture`

**Variables not loading:**
- Run `echo $N8N_WEBHOOK_BASE_URL` to verify they are set
- Restart OpenClaw gateway after setting variables
