# MailClaw Heartbeat

Fetch pre-analyzed emails from the server and present a digest to the user. Email analysis (intent, summary, rule matching) is handled server-side — this heartbeat only fetches results and displays them.

## Steps

1. Read `{baseDir}/config.json` to get `api_key`. If missing, reply `HEARTBEAT_FAIL: config.json not found` and stop.

2. Fetch emails:

```
GET /emails?unprocessed_only=true
```

If zero emails → reply `HEARTBEAT_OK` and stop.

3. Generate a processing page link:

```
POST /daily-token/generate
```

Use the `link` and `verify_code` fields from the response.

4. Output the digest using this exact format:

```
☀️ Email Digest · <date>

<N> emails pending:
• <Sender>: <one-line description>
• <Sender>: <one-line description>

[→ Open processing page] (link valid for 24h)
🔑 Verification code: <code>
```

Use the server-provided `summary` field for each email's one-line description. Do not re-analyze email content.
