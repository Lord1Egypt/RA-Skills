# Risk Escalation Template

```json
{
  "wallet": "{{wallet}}",
  "trigger": "sybil.circular_flow_detected",
  "severity": "warning",
  "evidence": [
    {
      "chain": "solana",
      "signature": "{{signature}}",
      "slot": 0,
      "timestamp": "{{isoTimestamp}}",
      "counterparty": "{{counterparty}}",
      "metadata": {
        "reason": "Circular flow detected across related wallet cluster"
      }
    }
  ],
  "recommendedAction": "manual_review",
  "autoCap": 699,
  "requiresManualReview": true,
  "createdAt": "{{isoTimestamp}}"
}
```
