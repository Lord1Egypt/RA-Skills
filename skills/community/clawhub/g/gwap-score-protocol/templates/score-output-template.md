# Score Output Template

```json
{
  "wallet": "{{wallet}}",
  "protocolScore": 742,
  "tier": "trusted",
  "confidence": "moderate",
  "scoreVersion": "gwapscore-v2",
  "categories": [
    {
      "name": "wallet_maturity",
      "weight": 0.12,
      "rawScore": 81,
      "weightedImpact": 9.72,
      "summary": "Wallet has long-term activity and stable funding history."
    },
    {
      "name": "counterparty_quality",
      "weight": 0.2,
      "rawScore": 76,
      "weightedImpact": 15.2,
      "summary": "Mostly clean counterparties with some low-risk exposure."
    }
  ],
  "riskFlags": [
    {
      "type": "thin_lending_history",
      "severity": "warning",
      "summary": "Limited borrowing and repayment evidence."
    }
  ],
  "capsApplied": [],
  "explanation": "This wallet shows consistent activity, reputable counterparty interactions, and no severe unresolved risk events.",
  "lastUpdated": "{{isoTimestamp}}"
}
```
