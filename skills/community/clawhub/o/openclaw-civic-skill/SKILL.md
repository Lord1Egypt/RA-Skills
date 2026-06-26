---
name: civic
description: "Connect to Civic MCP for 100+ integrations."
metadata: {"openclaw":{"requires":{"env":["CIVIC_URL","CIVIC_TOKEN"],"anyBins":["mcporter","npx"]},"primaryEnv":"CIVIC_TOKEN"}}
---

# Civic MCP Bridge

> **⚠️ DISCLAIMER: Use at your own risk. For official documentation, visit [docs.civic.com](https://docs.civic.com).**

Connect to [Civic](https://nexus.civic.com) for 100+ integrations including Gmail, PostgreSQL, MongoDB, Box, and more.

## Setup

### 1. Get your Civic credentials

1. Go to [nexus.civic.com](https://nexus.civic.com) and sign in
2. Get your **MCP URL** and **access token** from your profile settings

### 2. Configure in OpenClaw

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "civic": {
        "enabled": true,
        "env": {
          "CIVIC_URL": "https://nexus.civic.com/hub/mcp?accountId=YOUR_ACCOUNT_ID&profile=YOUR_PROFILE",
          "CIVIC_TOKEN": "your-access-token"
        }
      }
    }
  }
}
```

### 3. (Optional) Configure mcporter

If you have mcporter installed (`npm install -g mcporter`), add to `~/.openclaw/workspace/config/mcporter.json`:

```json
{
  "mcpServers": {
    "civic": {
      "baseUrl": "https://nexus.civic.com/hub/mcp?accountId=YOUR_ACCOUNT_ID&profile=YOUR_PROFILE",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN",
        "User-Agent": "openclaw/1.0.0"
      }
    }
  }
}
```

## Instructions for the Agent

When the user asks to interact with external services through Civic, try mcporter first. If it fails, fall back to the TypeScript script.

### Using mcporter

```bash
# List tools
mcporter list civic

# Search tools
mcporter list civic | grep gmail

# Call a tool
mcporter call 'civic.google-gmail-search_gmail_messages(query: "is:unread")'
```

### Fallback: TypeScript script

```bash
# List tools
npx tsx {baseDir}/civic-tool-runner.ts --list

# Search tools
npx tsx {baseDir}/civic-tool-runner.ts --search gmail

# Get tool schema
npx tsx {baseDir}/civic-tool-runner.ts --schema google-gmail-search_gmail_messages

# Call a tool
npx tsx {baseDir}/civic-tool-runner.ts --call google-gmail-search_gmail_messages --args '{"query": "is:unread"}'
```

### Authorization flows

Some tools require OAuth on first use. When you see an authorization URL:

1. Show the URL to the user
2. After they authorize, continue:
   ```bash
   # mcporter
   mcporter call 'civic.continue_job(jobId: "JOB_ID")'

   # script
   npx tsx {baseDir}/civic-tool-runner.ts --call continue_job --args '{"job_id": "JOB_ID"}'
   ```

## Notes

- API calls can take 10-15 seconds (server-side latency)
- Tokens expire after ~30 days — regenerate from Civic if needed
- Gmail batch requests limited to 5-25 messages per call

---
