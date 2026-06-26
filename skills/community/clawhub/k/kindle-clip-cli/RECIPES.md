# RECIPES.md - Kindle-Clip-CLI

Here are some automated workflows for `kindle-clip-cli`.

## 1. Kindle → Summarize → Telegram
Keep your reading notes actionable by summarizing them and sending them to your telegram immediately.

```bash
# Example chain (using OpenClaw)
kindle-clip search "philosophy" --export-md ./temp.md
summarize ./temp.md --length short > ./summary.md
message send --channel telegram --message "$(cat ./summary.md)"
```

## 2. Weekly Reading Review
Get a weekly summary of what you read in the last 7 days.

```bash
# Get the date 7 days ago
DATE_START=$(date -d "7 days ago" +%Y-%m-%d)

# List books read this week
kindle-clip list --from $DATE_START --verbose
```
