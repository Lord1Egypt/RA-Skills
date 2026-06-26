# MoltStreet Heartbeat

Check that the MoltStreet ETF signal API is alive and returning fresh data.

```bash
curl -s https://moltstreet.com/api/v1/etf/SPY
```

Parse the JSON response:

1. Check that `symbol` equals "SPY"
2. Check that `confidence` is a number between 0 and 1
3. Check that `direction` is one of: -1, 0, 1
4. Check that `human_readable_explanation` is non-empty

If all checks pass:
"HEARTBEAT_OK — SPY signal: {direction_word} with {confidence * 100}% confidence, target ${target_price} ({expected_move_pct}% move)"

Where direction_word: 1="bullish", -1="bearish", 0="neutral"

If the API returns an error or missing fields: HEARTBEAT_FAIL

Check once daily after 07:00 UTC. Signals update daily.
