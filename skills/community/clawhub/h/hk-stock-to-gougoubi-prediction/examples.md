# Example: Tencent 00700

This example shows how to turn a liquid Hong Kong stock catalyst into a Gougoubi-ready prediction draft.

## Input

```json
{
  "symbol": "00700",
  "horizon": "event"
}
```

## Analysis Snapshot

- Company: Tencent Holdings
- HK code: `00700`
- Reference close: around `HK$559.50` on `2026-03-16`
- Catalyst: FY2025 annual results expected on `2026-03-18`
- Context:
  - Tencent had mixed southbound flow in early March 2026, with both large inflow and outflow days.
  - The stock had recently rebounded after weakness.
  - An earnings event gives a cleaner resolution path than a loose directional thesis.

## Chosen Prediction

```json
{
  "title": "Will 00700 close above HK$580 on 2026-03-20?",
  "type": "direction",
  "deadlineIsoUtc": "2026-03-20T09:00:00Z",
  "resolutionSource": "Yahoo Finance 0700.HK historical data, fallback HKEX market data",
  "confidence": 0.58
}
```

Why this one:

- high-liquidity underlying
- near-dated catalyst
- simple binary wording
- externally resolvable from public market data

## Gougoubi Payload Draft

```json
{
  "marketName": "Will 00700 close above HK$580 on 2026-03-20?",
  "deadlineIsoUtc": "2026-03-20T09:00:00Z",
  "rules": "Resolution source:\n- Primary: Yahoo Finance historical data for 0700.HK\n- Fallback: HKEX official quote data\n\nResolution rule:\n- This market resolves YES if Tencent Holdings (00700 / 0700.HK) official closing price on 2026-03-20 is strictly greater than HK$580.00.\n- This market resolves NO otherwise.\n\nMeasurement details:\n- Timezone: Asia/Hong_Kong\n- Observation time: Regular Hong Kong market close on 2026-03-20\n- Metric: Official closing price in HKD\n- Tie handling: A closing price equal to HK$580.00 resolves NO.",
  "tags": [
    "hong-kong-stocks",
    "finance",
    "tech",
    "earnings",
    "event"
  ]
}
```

## Minimal Create Input

```json
{
  "marketName": "Will 00700 close above HK$580 on 2026-03-20?",
  "deadlineIsoUtc": "2026-03-20T09:00:00Z"
}
```

## Notes

- This is a preparation example only. Do not submit automatically.
- If newer price action materially changes the setup, update the strike and deadline before creation.
