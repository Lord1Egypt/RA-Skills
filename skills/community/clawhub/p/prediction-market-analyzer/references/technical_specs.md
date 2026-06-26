# Technical Specifications: Prediction Market Analyzer

## 1. External API Configuration
- **Base URL**: `https://api.secwarex.io`
- **Endpoints**:
    - **Polymarket**: `/api/v1/plugin/polymarket/risk?slug={slug}`
    - **Kalshi**: `/api/v1/plugin/kalshi/risk?eventTicker={eventTicker}` (Case-sensitive)

## 2. Parameter Extraction Heuristics
- **Polymarket**: Use regex or path splitting to find the segment after `/event/`.
- **Kalshi**: Use the segment after `/markets/`. Ensure full ticker name is captured.

## 3. JSON Data Structure
The tool returns a JSON object. Adhere to these parsing rules:
- **Priority**: Use the `result` field first.
- **Root Level**: Check for `tags` and `notices` arrays.
- **Item Fields**:
    - `name`: Technical identifier.
    - `label`: Display name (preferred for reports).
    - `riskLevel`: Integer (1: Safe, 2: Watch, 3: Danger).
    - `description`: Detailed risk explanation.

```json
{
  "result": {
    "tags": [
      {
        "name": "liquidity",
        "label": "Liquidity",
        "riskLevel": 1,
        "description": "..."
      }
    ]
  }
}
```
