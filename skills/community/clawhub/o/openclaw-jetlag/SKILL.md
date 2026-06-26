---
name: jetlag-planner
description: Scans your Google Calendar for upcoming flights and writes a personalized circadian adjustment plan back to your calendar. Trigger with phrases like "check my flights", "run jetlag planner", "plan my trip adjustment", or "am I ready for my upcoming flight".
---

Run the jetlag planner by following these steps exactly.

## Step 1 — Check for .env

Check whether the file `~/openclaw-jetlag/.env` exists.

If it does not exist, stop immediately and reply:

> ⚠️ No `.env` file found in `~/openclaw-jetlag/`. You need to add your Google OAuth credentials before I can run the planner. Follow the setup instructions in the README — ask me "show me the jetlag setup instructions" if you need them.

## Step 2 — Check for .oauth-token.json

Check whether the file `~/openclaw-jetlag/.oauth-token.json` exists.

If it does not exist, stop immediately and reply:

> ⚠️ Google authorization hasn't been completed yet. Run this once in your terminal to finish setup:
>
> ```
> cd ~/openclaw-jetlag && node index.js
> ```
>
> It will open a browser, ask you to sign in to Google, and save your authorization. After that, just say "check my flights" again and I'll handle it from here.

## Step 3 — Run the planner

Run the following command and capture all output (stdout and stderr):

```bash
cd ~/openclaw-jetlag && node index.js
```

## Step 4 — Report back

Reply with a short, plain-language Telegram-friendly summary. Do not dump raw output. Instead:

- If flights were detected and plans were written, say which flights were found (route and date) and how many calendar events were created total.
- If the output says no flight events were found, reply: "No upcoming flights found in your calendar for the next 90 days. If you have flights coming up, check that your airline confirmation emails are in the Gmail account linked to this calendar."
- If flights were found but all were skipped (under 2-hour timezone shift), reply: "Found [N] flight(s) but all had under a 2-hour timezone shift, so no adjustment plan was needed."
- If the command exited with a non-zero code or printed an error, relay the error message directly and suggest running `cd ~/openclaw-jetlag && node index.js` manually to see the full output.

Keep the reply under 5 sentences. No markdown headers in the Telegram reply — just plain text with line breaks between items if listing multiple flights.
