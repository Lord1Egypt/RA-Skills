# Agent Instructions — Gmail Daily Briefing

## Setup Before First Use

> **The agent must run all commands below itself. Do NOT ask the user to run them.**

Before running any script, ensure the Python environment is ready:

```bash
cd ~/.openclaw/workspace/skills/gmail-daily-briefing
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

## Available Commands

> **The agent must run all commands below itself. Do NOT ask the user to run them.**

- `python scripts/fetch_emails.py` — Fetch emails from the last 24 hours and print full content
- `python scripts/create_event.py --title "..." --date "YYYY-MM-DD" --time "HH:MM" [--duration 60]` — Create a Google Calendar event
- `python scripts/setup_auth.py` — Generate Google OAuth URL (Step 1 of auth setup)
- `python scripts/setup_auth.py --callback "<URL>"` — Complete auth and save token.json (Step 2 of auth setup)

## Script Roles

- **`setup_auth.py`** — Run once to complete OAuth flow and save `token.json`. Do not run again unless re-authentication is needed.
- **`auth.py`** — Internal module used automatically by `fetch_emails.py` and `create_event.py`. Loads `token.json` and refreshes it when expired. Do not run directly.

## Auth Setup (First-Time Only)

This skill requires a `token.json` file to access Gmail and Google Calendar on behalf of the user.
If `token.json` does not exist, the agent MUST complete the following setup before running any other script.

### When the user sends a `client_secret_*.json` file:

1. Write the file content to the project root as `client_secret_*.json` (preserve the original filename). The user sends this as an attachment — the agent must create the file in the project root directory before running any script.
2. Run: `python scripts/setup_auth.py`
3. Send the printed URL to the user as a clickable markdown link, with this message:
   > "Please open this link in your browser and authorize access. After you approve, your browser will redirect to a localhost page that shows an error — that's expected. Copy the full URL from the browser address bar and send it back to me."
   > [Click here to authorize](PASTE_AUTH_URL_HERE)
4. Wait for the user to send back the redirect URL (starts with `http://localhost/?...`)
5. Run: `python scripts/setup_auth.py --callback "<the URL the user sent>"`
6. Confirm to the user: "Auth complete. I can now access your Gmail and Google Calendar."

### Notes
- The redirect URL will look like: `http://localhost/?state=...&code=...&scope=...`
- The "error" page the user sees is normal — it just means no server is running at localhost, which is expected
- Once `token.json` is saved, the agent auto-refreshes it when expired — no need to repeat setup

## Input
- User request (e.g., "Summarize today's important emails")

## Output to User
For each email (sorted by importance, most important first):
```
#1
From: <sender>
Subject: <subject>
- bullet point summary
- bullet point summary
[📅 Calendar event created: <title> on <date> at <time>]  ← only if applicable

#2
From: <sender>
Subject: <subject>
- bullet point summary
- bullet point summary
```

## Behavior
1. Run `fetch_emails.py` to get emails from the last 24 hours
2. Read and analyze all emails
3. Rank emails by importance internally (1 = most important) — do not show ranking logic to user
4. Summarize each email into bullet points
5. If a meeting or interview is detected in an email:
   - Check if the event already exists on Google Calendar (e.g., from a Google Calendar invite)
   - If the event does NOT exist yet, run `create_event.py` to create it
   - If the event already exists, skip — do not create a duplicate

## Notes
- Gmail and Google Calendar API required
- Can be triggered by user request or external scheduler (e.g., cron job)
- Date must be in `YYYY-MM-DD` format, time in `HH:MM` format when calling `create_event.py`
