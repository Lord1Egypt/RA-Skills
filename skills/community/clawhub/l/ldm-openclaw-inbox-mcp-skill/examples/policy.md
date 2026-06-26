# OpenClaw Policy

Use this policy for outbound agents:

```text
Before sending or scheduling any bulk outbound campaign, use the inbox-check MCP server.

First call inbox_check_me to inspect quota and allowed providers.
Then call inbox_check_create for the target providers.
Send the exact final message to all returned seed addresses.
Call inbox_check_status until results are done.

If inbox placement is below 70%, or Gmail/Outlook lands in Spam/Junk, do not send the campaign.
Report the provider issues, authentication results, screenshots if available, and concrete fixes.

Only bypass this rule if the user explicitly confirms they want to send despite the risk.
```

## Suggested Providers

- Fast default: Gmail + Outlook
- US/EU B2B: Gmail + Outlook + Yahoo + iCloud
- Russia/CIS: Gmail + Outlook + Mail.ru + Yandex
- Broad audit: all providers allowed by `inbox_check_me`
