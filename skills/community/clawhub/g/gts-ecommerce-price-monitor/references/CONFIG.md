# Advanced Configuration

Read this when the user wants to customize notification channels, set up
scheduled scanning, or export data in custom formats.

## Notification Channels

### Telegram (default)
Price alerts are sent as Telegram messages using `sessions_send`
or direct messaging. No extra setup needed.

### Email
To send reports via email, the user needs to configure SMTP in
their OpenClaw workspace or connect an email service skill.

### Discord
If the user is connected via Discord, alerts route there automatically.

## Scheduled Scanning

The agent should set up a recurring cron job when the user asks for
automatic scanning:

```
Every 6 hours: scan tracked products, check alerts, notify if triggered
Every 24 hours: generate and save a daily summary report
Weekly (Monday): generate weekly comparison report
```

### Setup
```bash
# Example — add to user's crontab or OpenClaw cron
openclaw cron add --name "price-scan" \
  --schedule '{"kind":"every","everyMs":21600000}' \
  --payload '{"kind":"agentTurn","message":"Run scheduled price scan on all tracked products. Check alerts and notify me of any changes."}'
```

## Price History Storage

### Default format: JSONL
```
scripts/price_history.jsonl
```
Each line is a JSON object:
```json
{
  "timestamp": "2026-04-30T10:00:00",
  "product_id": 1,
  "product_name": "iPhone 15 Pro",
  "price": 4899.00,
  "currency": "RM",
  "url": "https://shopee.com.my/...",
  "seller": "Apple Flagship Store",
  "in_stock": true,
  "raw_text": "RM 4,899.00",
  "notes": null
}
```

### Export formats
| Format | Command | Output |
|--------|---------|--------|
| CSV | `python3 scripts/report.py --csv` | `reports/price_report_YYYY-MM-DD.csv` |
| JSON | Direct from history file | `scripts/price_history.jsonl` |

## Multi-Agent Mode

For users tracking 10+ products, recommend splitting work:
- **Scanner agent**: Handles all URL visiting and price extraction
- **Analyst agent**: Generates reports and trend analysis
- **Notifier agent**: Checks alerts and sends notifications

This avoids rate limits and keeps each agent focused.

## FAQ

**Q: Can I track 50+ products?**
A: Yes, but increase check intervals to 12-24h to avoid rate limits.
   Consider multi-agent mode.

**Q: Will this get my IP banned?**
A: Unlikely if you stay within rate limits (1 req/5s default).
   Shopee and Amazon are the most sensitive.

**Q: Can I track Shopee Flash Sale prices?**
A: Yes, but flash sale prices are time-sensitive. Set interval to 5-15 minutes
   during known sale periods.

**Q: What about mobile apps?**
A: This skill works on web versions. Some platforms (Shopee) show different
   prices on mobile web — use `m.shopee.com.my` URLs if needed.

**Q: Can I share my price data with a Google Sheet?**
A: Yes, combine with a Google Sheets skill to auto-append new prices to
   a shared spreadsheet.
