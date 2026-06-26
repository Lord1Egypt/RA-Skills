# Google Alerts Monitor — Setup Guide

## Required Environment Variable

**`GOOGLE_ALERT_FEED_ID`** — required for the search script to work.

```bash
export GOOGLE_ALERT_FEED_ID=your_feed_id_here
```

Add this to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) to make it persistent.

## Step 1: Get Your Google Alert Feed ID

1. Go to [google.com/alerts](https://www.google.com/alerts)
2. Create or open an alert
3. Click the RSS icon
4. Copy the feed ID from the URL (the part after `/feeds/`)
   - Example URL: `https://www.google.com/alerts/feeds/your_feed_id_here/123456789`
   - Your feed ID is the string between `/feeds/` and the next `/`

## Step 2: Set the Environment Variable

```bash
export GOOGLE_ALERT_FEED_ID="your_feed_id_here"
```

## Step 3: Edit Keywords

Open `references/keywords.md` and replace placeholders with your own keywords.

## Step 4: Test the Scripts

```bash
# Test search (requires GOOGLE_ALERT_FEED_ID to be set)
bash scripts/search.sh "your keyword" 10

# Test formatter
echo '[]' | python3 scripts/format-results.py --term "test" --source google
```

## Endpoints Called

- `https://www.google.com/alerts/feeds/` — Google Alerts RSS feeds (read-only)

## Notes

- No API key required — Google Alerts is a public service
- Feed IDs are not secret but should be treated as user-specific identifiers
- The search script will exit with an error if `GOOGLE_ALERT_FEED_ID` is not set
