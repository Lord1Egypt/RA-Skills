# Gmail Daily Briefing

An AI agent skill that reads your Gmail, ranks emails by importance, summarizes them into bullet points, and automatically creates Google Calendar events for detected meetings.

## Features

- Fetches emails from the last 24 hours
- Ranks emails by importance
- Summarizes each email into bullet points
- Detects meetings/interviews and creates Google Calendar events automatically
- Skips calendar events that already exist (no duplicates)

## Requirements

- Python 3.x
- [OpenClaw](https://openclaw.ai/) agent

## Setup Before First Use

Before running any script, ensure the Python environment is ready:

```bash
cd ~/.openclaw/workspace/skills/gmail-daily-briefing
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

## Installation

Via ClawHub (recommended):

```
clawhub install gmail-daily-briefing
```

Manual:

```bash
git clone https://github.com/Russidan-Nadee/gmail-daily-briefing.git ~/.openclaw/workspace/skills/gmail-daily-briefing
```

## Setup (First-Time Only)

### Step 1 — Get Google API credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing one)
3. In the left sidebar, go to **APIs & Services** → click **Enable APIs and Services**
4. Search and enable:
   - **Gmail API**
   - **Google Calendar API**
5. In the left sidebar, go to **APIs & Services → OAuth consent screen**
   - Click **Get Started**
   - Fill in **App name** and **User support email** → click **Save and Continue**
   - Under **Audience** → click **Add Users** → add your Google email → click **Save**
6. In the left sidebar, go to **APIs & Services → Credentials**
7. Click **Create Credentials → OAuth client ID**
8. Under **Application type** select **Desktop app**
9. Give it a name → click **Create**
10. Click **Download JSON** → save as `client_secret_*.json`

### Step 2 — Connect to the agent

1. Send the `client_secret_*.json` file to the agent as an attachment
2. The agent will send you an authorization URL — click it
3. Log in with your Google account and click **Allow**
4. Your browser redirects to a `localhost` error page — **this is normal**
5. Copy the full URL from your browser address bar
6. Paste it back to the agent

### Step 3 — Done!

Just say: **"Summarize today's important emails"**

## Project Structure

```
gmail-daily-briefing/
├── SKILL.md                  # Skill definition for ClawHub
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── agent/
│   └── instructions.md       # Agent instructions (commands, auth, behavior)
└── scripts/
    ├── auth.py               # Internal auth module (auto-used by other scripts)
    ├── setup_auth.py         # OAuth setup (run once)
    ├── fetch_emails.py       # Fetch and display emails
    └── create_event.py       # Create Google Calendar events
```

## License

MIT
