# GroupMe Skill — Setup Guide

Connect OpenClaw to any GroupMe group for automated messaging and team communication.

## What You Get

- Send messages to your GroupMe group on-demand or on a schedule
- Automate shift reminders, announcements, and alerts via cron
- Broadcast urgent messages instantly
- Perfect for teams, clubs, families, or any group

## Setup (5 Minutes)

### 1. Get Your GroupMe Access Token

Go to https://dev.groupme.com/bots and copy your access token (shown at the top of the page).

### 2. Create a Bot

Go to https://dev.groupme.com/bots/new and create a new bot:
- **Name:** Whatever you want (e.g., "OpenClaw", "Team Bot")
- **Group:** Select the GroupMe group this bot will post to
- **Callback URL:** Leave blank (not needed for sending only)
- Save the **Bot ID** you're given after creation

### 3. Find Your Group ID

Open a terminal and run (replace `YOUR_TOKEN` with your access token):

```bash
curl -s "https://api.groupme.com/v3/groups?token=YOUR_TOKEN&per_page=10"
```

Find your group in the response — the `id` field is your Group ID.

### 4. Save Your Tokens

Create a file at `~/.openclaw/secrets/groupme.env`:

```bash
GROUPME_ACCESS_TOKEN="your_access_token_here"
GROUPME_BOT_ID="your_bot_id_here"
GROUPME_GROUP_ID="your_group_id_here"
```

### 5. Test It

```bash
./scripts/send-message.sh "Hello from OpenClaw!"
```

You should see the message appear in your GroupMe group.

## Usage Examples

Tell OpenClaw things like:
- "Send a reminder to the group for the 3pm shift"
- "Post this announcement to the team: Weekly goals are posted"
- "Send an alert: Kitchen emergency, need backup NOW"

Or set up automatic cron jobs for:
- Daily shift reminders (Mon-Fri at 8am)
- Weekly team updates (Mondays at 9am)
- Monthly recognition posts

## How It Works

The skill uses the GroupMe REST API v3 to post messages via a bot. Messages go from OpenClaw → GroupMe API → your group. Simple, reliable, free.

No server required. No callbacks. Just outbound messages on demand.

## Troubleshooting

**"Error: GROUPME_BOT_ID and GROUPME_ACCESS_TOKEN must be set"**
→ Make sure `~/.openclaw/secrets/groupme.env` exists and is properly formatted

**Message doesn't appear in group**
→ Check that your bot is joined to the correct group in GroupMe
→ Verify your access token is valid at https://dev.groupme.com/bots

**403 or permission errors**
→ The bot must be a member of the group to post messages

## Need Help?

Refer to the full SKILL.md for detailed API documentation and advanced usage patterns.