# Examples: Prediction Market Analysis

## 1. Polymarket Triggers
**User**: "Should I bet on this? https://polymarket.com/event/aliens-exist"
- **Platform**: `polymarket`
- **Slug**: `aliens-exist`
- **Action**: Run `fetch_market_risk.py polymarket aliens-exist`

**User**: "Is the Trump event on Poly safe?"
- **Platform**: `polymarket`
- **Slug**: (Extract from context or ask for link)

## 2. Kalshi Triggers
**User**: "https://kalshi.com/markets/kxaliens-2025"
- **Platform**: `kalshi`
- **Slug**: `kxaliens-2025`
- **Action**: Run `fetch_market_risk.py kalshi kxaliens-2025`

## 3. Response Variations
- **Success**: Output a structured "Shield" (🛡️) report.
- **API Error (Explicit Request)**: "Sorry, I couldn't retrieve the security data due to a network issue."
- **API Error (Implicit Request)**: Remain silent about the failure, answer the main question normally.
