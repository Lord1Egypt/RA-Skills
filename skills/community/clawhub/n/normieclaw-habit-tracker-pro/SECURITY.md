# Habit Tracker Pro — Security Considerations

## Data Handling

Habit Tracker Pro stores habit definitions, completion logs, streak data, and
pattern analysis results as JSON files. This data includes:

- Habit names and descriptions
- Daily completion/skip records with timestamps
- Skip reasons (freeform text)
- Notes attached to completions
- Pattern analysis results and behavioral insights

This is personal behavioral data. Treat it accordingly.

## What We Don't Guarantee

- We make no claims about where your data is stored or who can access it.
- Data handling depends on your OpenClaw configuration, hosting environment,
  and channel setup.
- Cross-tool sync shares habit data with other NormieClaw tools in your
  environment.

## What We Do

- All data is stored in flat JSON files — no external databases, no cloud sync,
  no third-party analytics.
- No data is transmitted to NormieClaw, normieclaw.ai, or any external service
  as part of normal operation.
- Export scripts produce local CSV/markdown files.
- No telemetry, no usage tracking, no analytics collection.

## User Responsibilities

- **Backups:** Run `scripts/export-habits.sh` periodically. We don't backup
  your data for you.
- **Access control:** The data directory (`~/.normieclaw/habit-tracker-pro/`)
  has standard file permissions. Manage access to your machine accordingly.
- **Sensitive notes:** If you include sensitive information in habit notes or
  skip reasons, that data exists in plaintext JSON files.
- **Channel security:** Check-in messages go through your configured chat
  channel (Telegram, Discord, etc.). Those channels have their own security
  properties — we don't control them.

## Deletion

- Delete specific habits: tell your agent to delete a habit (requires confirmation).
- Delete all data: remove the `~/.normieclaw/habit-tracker-pro/` directory.
- Exported files in the `exports/` subdirectory must be deleted separately.

## Cross-Tool Sync Security

When cross-tool sync is enabled, other NormieClaw tools can:
- Write completion signals to Habit Tracker Pro (e.g., Trainer Buddy logging a workout).
- Read habit completion data (e.g., a reporting tool generating a wellness overview).

This sync happens locally through shared file paths. No network requests are made
for cross-tool communication.

## Reporting Issues

Security concerns: support@normieclaw.ai

---

*NormieClaw · normieclaw.ai*
