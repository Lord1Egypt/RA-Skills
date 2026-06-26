# NBA Playoffs Skill

**⚠️ Disclaimer**
This skill is for entertainment purposes only. Sports predictions are for fun — no betting or real gambling mechanics included.

---

**Skill ID:** `nba-playoffs`
**Version:** 1.0.0
**Author:** Brian Goodwin

---

## What It Does

Full NBA Playoffs coverage — from Play-In through the Finals. Tracks your team, sends game day reminders, posts final scores, and lets you make predictions.

**Setup:**
- User picks their channel (GroupMe, Discord, Telegram, etc.)
- User selects their favorite team(s)
- Skill pulls full playoff bracket from ESPN's public NBA API

**Game Day Flow:**
- Reminder before each game → matchup, time, watch/stream info
- Final score + top performer stats after each game

**Bracket:**
- Full playoff bracket (all rounds)
- User's team highlighted
- Drill into team → full schedule + results

**Watch/Stream Info:**
- TV channel (ABC, ESPN, TNT, etc.)
- Streaming (ESPN+, NBA League Pass, etc.)
- Radio station per team

**Predictions:**
- `predict [winner]` before each game
- Tracks record in `nba-predictions.md`
- End of playoffs: prediction accuracy %

**Flair:**
- SVG image with team colors + playful banter
- "Got the W 🏀", "Tough one 🤕", "Back to the lab", etc.
- Shareable in Discord, GroupMe, etc.

---

## Data Source

All game data pulled from ESPN's public NBA API:
- Scoreboard: `https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard`
- No API key required
- No cost

---

## Credentials

**⚠️ Important — How Channel Credentials Work**

This skill uses your **existing OpenClaw channel configuration**. It does NOT request, store, or create new credentials.

When you configure a channel in OpenClaw (GroupMe, Discord, Telegram, etc.), those credentials are already stored in your OpenClaw config. This skill sends messages through the `message` tool using whatever channels are already configured — no additional token or webhook needed.

If you have not set up a messaging channel yet, you must do so before using this skill. The skill will prompt you to configure one during `setup nba playoffs`.

---

## Files Written

The following files are created in your workspace:

| File | Purpose |
|------|---------|
| `nba-predictions.md` | Your prediction record (date, game, pick, result) |
| `nba-config.md` | Your team selection and channel preference |

These files are created on first run and updated as games happen. You can delete them with `remove nba`.

---

## Cron Jobs

**What gets created:**
- 1 reminder cron per playoff game your team is in (fires ~2 hours before game time)
- 1 post-score cron per playoff game (fires ~15 minutes after game ends)
- All crons run Mon-Sat during playoffs
- All crons are timezone-aware (uses America/New_York)

**How to see what crons are active:**
```
openclaw tasks
```

**How to remove all crons:**
```
remove nba
```
This command deletes all NBA-related cron jobs and removes the config files.

---

## Commands

| Command | What it does |
|---------|--------------|
| `setup nba playoffs` | Start setup, pick channel + team(s) |
| `scores` | Today's games + scores |
| `schedule` | Full playoffs schedule |
| `bracket` | Full series bracket |
| `my team` | Your team's games + stats |
| `predict [winner] for [game#]` | Log your prediction |
| `predictions` | Show your prediction record |
| `flair` | Generate team banter image |
| `watch [game#]` | Watch + stream + radio info |
| `remove nba` | Remove skill + all cron jobs + config files |

---

## Flair Messages

Win messages:
- "Got the W 🏀"
- "Nothing but net"
- "Victory tastes good"
- "Bucket secured"
- "Championship energy"

Loss messages:
- "Tough one 🤕"
- "Back to the lab"
- "See you next season"
- "On to the next one"

---

## Technical Notes

- API: ESPN public NBA scoreboard (no key needed)
- Channel: Uses OpenClaw's existing channel config — no new credentials stored
- Cron jobs created per game, removed with `remove nba`
- All data stored locally in workspace
- No betting odds — betting mechanics explicitly excluded
- Predictions stored in `~/.openclaw/workspace/nba-predictions.md`
- Config stored in `~/.openclaw/workspace/nba-config.md`