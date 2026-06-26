---
name: mail-summary
description: Fetch Gmail emails from the last 24h, rank by importance, summarize into bullet points, and auto-create Google Calendar events for detected meetings.


# Email & Calendar Assistant Skill

## Description
This skill reads Gmail emails, ranks them by importance, summarizes each email into bullet points, and creates Google Calendar events if an email contains a meeting or interview that is not already on the calendar.

## Capabilities
- Read emails (read-only)
- Rank emails by importance
- Summarize emails into bullet points
- Detect meeting/interview emails
- Create Google Calendar events (only when not already added)
- Auto-refreshes Google OAuth token as needed for uninterrupted access.

## Installation

Via ClawHub (recommended):

```
clawhub install mail-summary
```

Manual:

```
git clone https://github.com/Russidan-Nadee/mail-summary.git ~/.openclaw/workspace/skills/mail-summary
```

## Setup Instructions (First-Time Only)

### Step 1 — Get Google API credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing one)
3. In the left sidebar, go to **APIs & Services** → click **Enable APIs and Services**
4. Search and enable each of the following:
   - **Gmail API**
   - **Google Calendar API**
5. In the left sidebar, go to **APIs & Services → OAuth consent screen**
   - Click **Get Started**
   - Fill in **App name** and **User support email** → click **Save and Continue**
   - Under **Audience** → click **Add Users** → add your Google email → click **Save**
6. In the left sidebar, go to **APIs & Services → Credentials**
7. Click **Create Credentials → OAuth client ID**
8. Under **Application type** select **Desktop app**
9. Give it a name (e.g. `Mail Summary`) → click **Create**
10. Click **Download JSON** → you'll get a file named `client_secret_*.json`

### Step 2 — Connect to the agent

1. Send the `client_secret_*.json` file to the agent as an attachment
   - Via **Telegram**: send as a file (not photo) in your Clawdbot chat
   - Via **Claude Desktop**: drag and drop the file into the chat
   - Via **other platforms**: attach the file the same way you attach any document
2. The agent will print an authorization URL — click it to open in your browser
3. Log in with your Google account and click **Allow**
4. Your browser will redirect to a `localhost` page showing an error — **this is normal**
5. Copy the **full URL** from your browser address bar (starts with `http://localhost/?...`)
6. Paste that URL back to the agent

### Step 3 — Done!

The agent will confirm: *"Auth complete. I can now access your Gmail and Google Calendar."*

From now on just say: **"Summarize today's important emails"**

## Configuration

This skill uses a `config.yaml` file in the project root for runtime configuration. You can edit this file to control timezone, retry behavior, and logging level.

**Example `config.yaml`:**

```yaml
timezone: Asia/Bangkok    # Timezone for calendar events (e.g. Asia/Bangkok, UTC, Asia/Tokyo)
max_retries: 5            # Max retry attempts for authentication and API calls
log_level: INFO           # Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
```


## Agent Instructions

> See [`agent/instructions.md`](agent/instructions.md) for full agent instructions (commands, auth setup, behavior).