# Monitor Job — Cron Payload Template

Create with `cron add`:

```json
{
  "name": "NOFX AI500 15-minute Monitor",
  "schedule": { "kind": "every", "everyMs": 900000 },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run monitoring script:\n1. Execute `bash <skill-dir>/scripts/monitor.sh`\n2. If output starts with NEW:, means new coin joined AI500:\n   a. Use message tool to send Telegram notification:\n      🚨🚨🚨 AI500 New Coin Selected!\n      🆕 Coin name\n      ⭐ Score: xx\n      💰 Entry price: $xx\n   b. Perform complete analysis for new coin (OI, institutional fund flow, K-line) and send\n3. If output REMOVED:xxx → send: ⚠️ AI500 Coin Removed: xxx\n4. If output NO_CHANGE → end silently\n\nAPI Base: <BASE>  Key: <KEY>\nAuth: ?auth=KEY",
    "timeoutSeconds": 180
  },
  "delivery": { "mode": "none" }
}
```

Replace `<skill-dir>`, `<BASE>`, `<KEY>` with actual values.

## Alert Format

New coin alert (send via message tool to Telegram):

```
🚨🚨🚨 AI500 New Coin Selected!
🆕 XXXUSDT
⭐ Score: 75.3
💰 Entry price: $1.234
⏰ Just selected
```

Follow up with a detailed analysis code block including OI, fund flows, K-line for all timeframes.
