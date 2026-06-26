# NBA Playoffs — OpenClaw Skill

**Your full NBA Playoffs companion — from Play-In to the Finals.**

🏀 Game reminders, scores, bracket tracking, predictions, and shareable team banter.

---

**⚠️ Disclaimer: For Entertainment Only**
This skill is for fun, social sports tracking. No betting mechanics. No real gambling. Predictions are just for bragging rights.

---

## What It Does

- ✅ **Game day reminders** — before each playoff game
- ✅ **Final scores** — posted after each game with top stats
- ✅ **Full bracket** — every round from Play-In to Finals
- ✅ **Watch/stream info** — TV channel, streaming options, radio
- ✅ **Predictions** — pick a winner, track your record
- ✅ **Team flair** — playful banter images to share with friends
- ✅ **Your team first** — highlights your selected team across all views

---

## Who It's For

Any NBA fan who wants to stay locked in during the playoffs — whether you're tracking your team, making predictions with friends, or just want game reminders delivered to your chat.

---

## Setup

**Step 1: Install**

```
clawhub install nba-playoffs
```

Or tell your assistant: `setup nba playoffs`

**Step 2: Configure**

Your assistant will ask:
1. **Channel** — where to send reminders (GroupMe, Discord, Telegram, etc.)
2. **Your team** — pick your favorite team(s) from the list

That's it. The skill pulls the full playoff bracket and starts scheduling.

---

## Commands

| Say this | What happens |
|----------|---------------|
| `scores` | Today's games with live scores |
| `schedule` | Full playoffs schedule |
| `bracket` | Full series bracket with your team highlighted |
| `my team` | Your team's games, results, and key stats |
| `predict [Team] for [Game #]` | Lock in your prediction |
| `predictions` | Your prediction record this playoffs |
| `flair` | Generate a shareable banter image for your team |
| `watch [Game #]` | How to watch + stream + radio for that game |
| `remove nba` | Remove skill and all cron jobs |

---

## Flair Examples

After a win, your team gets a fun image with text like:
- "Got the W 🏀"
- "Nothing but net"
- "Victory tastes good"

After a loss:
- "Tough one 🤕"
- "Gonna need a bigger bat"
- "Back to the lab"

Screenshot it, share it — simple.

---

## Watch Info Per Game

Each game reminder includes:
- **TV** — ABC, ESPN, TNT, NBA TV, Prime Video
- **Stream** — ESPN+, NBA League Pass
- **Radio** — local station per team

No more "what channel is the game on?" — it's right there.

---

## Predictions

Before each game, lock in your pick:

```
predict Lakers for game 3
```

Your record builds across the playoffs. At the end, you'll get a prediction accuracy % — see how you did against your friends.

---

## Requirements

- OpenClaw installed and running
- A messaging channel configured (GroupMe, Discord, Telegram, etc.)
- Cron enabled (standard on all OpenClaw installs)
- No API keys needed — uses ESPN's free public NBA API

---

## Data Source

Game data pulled from ESPN's public NBA API:
```
https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard
```

No API key. No subscription. No cost.

---

*Built on OpenClaw. Install from ClawHub.*