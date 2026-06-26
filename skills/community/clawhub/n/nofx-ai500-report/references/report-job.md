# Report Job — Cron Payload Template

Create with `cron add`:

```json
{
  "name": "NOFX AI500 30-minute Report",
  "schedule": { "kind": "every", "everyMs": 1800000 },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Generate NOFX AI500 periodic report.\n\nSteps:\n1. Call <BASE>/api/ai500/list?auth=<KEY> to get current selected coins\n2. For each coin, fetch the following data:\n   - OI: /api/oi/top-ranking and /api/oi/low-ranking (duration=5m,15m,30m,1h,4h,8h,24h)\n   - Institutional fund flow: /api/netflow/top-ranking and /api/netflow/low-ranking (type=institution, trade=future, same durations)\n   - Delta: /api/delta/list?symbol=XXX\n   - Long-short ratio: /api/long-short-ratio/list?symbol=XXX\n   - Funding rate: /api/funding-rate/top-ranking and /api/funding-rate/low-ranking\n3. K-line analysis: Use Binance public API to get K-line data for each coin\n   - https://fapi.binance.com/fapi/v1/klines?symbol=XXX&interval=15m&limit=10\n   - interval: 15m, 1h, 4h\n   Analysis: trend direction, bullish/bearish candle ratio, MA3 vs MA7, volume change, support/resistance\n4. Report format using box-drawing characters in code block\n5. Each coin includes: AI500 score, OI changes (multi-timeframe), institutional fund flow (multi-timeframe), K-line analysis\n6. OI and fund flow rankings show TOP8/LOW8 each\n7. Finally provide summary and trading suggestions\n\nUse message tool to send to telegram, target: <CHAT_ID>",
    "timeoutSeconds": 300
  },
  "delivery": { "mode": "announce" }
}
```

Replace `<BASE>`, `<KEY>`, `<CHAT_ID>` with actual values.

## Report Structure

```
╔══════════════════════════════════════╗
║   NOFX AI500 Intelligence Report     ║
║   <date> (<timezone>)                ║
║   Selected: N coins                  ║
╚══════════════════════════════════════╝

┌──────────────────────────────────────┐
│ 🪙 COINNAME  Score:XX.X  High:XX.X   │
│ Price:X.XXX Entry:X.XXX Gain:XX.X%   │
│ Funding:0.00X%                       │
├─ OI Changes ─────────────────────────┤
│ 5m:±X.XX% │ 15m:±X.XX% │ ...        │
├─ Institutional Flow ─────────────────┤
│ 1h:±$X.XM │ 4h:±$X.XM │ 24h:±$X.XM │
├─ K-line ─────────────────────────────┤
│ 15m: 📈/📉/↔️ │ MA Bull/Bear │ Vol±XX%│
│      Support:X.XX Resistance:X.XX    │
│ 1h:  ... │ 4h: ...                   │
└──────────────────────────────────────┘

(repeat per coin)

╔══════════════════════════════════════╗
║  OI Increase TOP8 / OI Decrease TOP8 ║
║  Inst. Inflow TOP8 / Outflow TOP8    ║
╚══════════════════════════════════════╝

╔══════════════════════════════════════╗
║  📋 Summary & Trading Suggestions     ║
║  • COIN1: Suggest...                 ║
║  • COIN2: Suggest...                 ║
╚══════════════════════════════════════╝
```
