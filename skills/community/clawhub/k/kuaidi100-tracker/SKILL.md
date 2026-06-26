# Package Tracker

Track Chinese domestic packages via Kuaidi100 push API with automatic Google Calendar delivery reminders.

## Tools

- `add_tracking_number` — Subscribe to push tracking updates for a package (costs 1 API quota)
- `list_packages` — List all tracked packages from local cache (free, no API call)
- `sync_to_calendar` — Manually sync today's deliveries to Google Calendar
- `remove_tracking_number` — Remove a tracking number from the watch list

## Setup

1. Get API credentials from [Kuaidi100](https://api.kuaidi100.com)
2. Configure `plugins.entries.package-tracker.config.kuaidi100` with your `customer` and `key`
3. (Optional) Add Google Calendar OAuth2 credentials for delivery reminders
4. (Optional) Set up a public webhook URL for push updates

See README.md for full configuration reference.
