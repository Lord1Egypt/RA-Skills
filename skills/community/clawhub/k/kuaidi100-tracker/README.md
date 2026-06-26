# 📦 Package Tracker for OpenClaw

Track Chinese domestic packages via [Kuaidi100](https://api.kuaidi100.com) push API. Automatically detects same-day deliveries and creates Google Calendar reminders.

## Features

- **Push-based tracking** — Subscribe to Kuaidi100 push API for real-time status updates (no polling needed)
- **Auto carrier detection** — Set carrier to `auto` and Kuaidi100 detects it for you
- **Today delivery detection** — Automatically identifies packages arriving today based on status keywords
- **Google Calendar reminders** — Creates/updates a "取快递" calendar event before your off-work time
- **Webhook support** — Receives Kuaidi100 push callbacks with signature verification
- **Local state** — Package data stored locally, `list_packages` costs zero API quota

## Tools

| Tool | Description | API Cost |
|------|-------------|----------|
| `add_tracking_number` | Subscribe to push updates for a tracking number | 1 quota |
| `list_packages` | List all tracked packages from local cache | Free |
| `sync_to_calendar` | Manually sync today's deliveries to Google Calendar | Free |
| `remove_tracking_number` | Remove a tracking number from watch list | Free |

## Requirements

- **Python 3.10+** (for `tracker_core.py` execution)
- **Kuaidi100 API account** — Get credentials at <https://api.kuaidi100.com>
- **Google Calendar OAuth2 credentials** (optional, for calendar reminders)
- **Public webhook URL** (optional but recommended, for receiving push updates — e.g. via Cloudflare Tunnel)

## Configuration

Add to your OpenClaw config under `plugins.entries`:

```json5
{
  "package-tracker": {
    "enabled": true,
    "config": {
      "kuaidi100": {
        "customer": "YOUR_CUSTOMER_ID",
        "key": "YOUR_API_KEY"
      },
      // Optional: Google Calendar integration
      "calendar": {
        "client_id": "YOUR_GOOGLE_CLIENT_ID",
        "client_secret": "YOUR_GOOGLE_CLIENT_SECRET",
        "refresh_token": "YOUR_REFRESH_TOKEN",
        "calendar_id": "primary"
      },
      // Optional: Customize reminder timing
      "schedule": {
        "off_work_time": "18:30",
        "reminder_minutes_before": 30,
        "timezone": "Asia/Shanghai"
      },
      // Optional: Webhook for push updates
      "webhook": {
        "baseUrl": "https://your-public-url.example.com",
        "token": "YOUR_WEBHOOK_SECRET",
        "salt": "YOUR_KUAIDI100_SALT",
        "signatureMode": "soft"
      }
    }
  }
}
```

## Usage Examples

```
# Track a new package
"帮我追踪这个快递 SF1234567890"

# List all packages
"我有哪些快递？今天有到的吗？"

# Sync to calendar
"帮我加到日历提醒"

# Remove tracking
"删除快递 SF1234567890"
```

## How It Works

1. **Subscribe**: `add_tracking_number` calls Kuaidi100 subscribe API (costs 1 quota per package)
2. **Receive**: Kuaidi100 pushes status updates to your webhook URL whenever the package moves
3. **Detect**: Plugin checks if the package is arriving today (派送中, 已到驿站, etc.)
4. **Remind**: If today delivery detected, automatically creates/updates a Google Calendar event

## Webhook Setup

For push updates to work, you need a publicly accessible URL. We recommend [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/):

```bash
cloudflared tunnel --url http://localhost:18789
```

Then set `webhook.baseUrl` to the tunnel URL. The webhook path includes your `token` for authentication.

## Signature Verification

Kuaidi100 supports callback signature verification. Configure `webhook.salt` and set `signatureMode`:
- `soft` (default): Accept all callbacks, log verification result
- `strict`: Reject callbacks with invalid or missing signatures

## License

MIT
