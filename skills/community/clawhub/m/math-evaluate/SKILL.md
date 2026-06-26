---
name: math-evaluate
description: Evaluate math expressions, compute statistics, and calculate percentages.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🧮"
    homepage: https://math.agentutil.net
    always: false
---

# math-evaluate

Safe math expression evaluation with variables, descriptive statistics (mean, median, mode, stddev, percentiles), and percentage calculations.

## Data Handling

This skill sends expressions to an external API for evaluation. The service does not store or log input data beyond the immediate response.

## Endpoints

### Evaluate Expression

```bash
curl -X POST https://math.agentutil.net/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{"expression": "2 * x + y", "variables": {"x": 20, "y": 2}}'
```

### Statistics

```bash
curl -X POST https://math.agentutil.net/v1/statistics \
  -H "Content-Type: application/json" \
  -d '{"values": [10, 20, 30, 40, 50]}'
```

Returns: count, sum, mean, median, mode, min, max, range, variance, stddev.

### Percentage

```bash
curl -X POST https://math.agentutil.net/v1/percentage \
  -H "Content-Type: application/json" \
  -d '{"operation": "change", "a": 100, "b": 125}'
```

Operations: `of` (a% of b), `change` (% change from a to b), `is_what_percent` (a is what % of b).

## Response Format

```json
{
  "result": 42,
  "expression": "2 * x + y",
  "variables_used": {"x": 20, "y": 2},
  "request_id": "abc-123",
  "service": "https://math.agentutil.net"
}
```

## Pricing

- Free tier: 10 queries/day, no authentication required
- Paid tier: $0.001/query via x402 protocol (USDC on Base)

## Privacy

No authentication required for free tier. No personal data collected. Rate limiting uses IP hashing only.
