# Payment Gateway Optimization — Output Template

## 1. Executive Summary
- Current gateway setup and identified pain points
- Recommended gateway configuration (primary + secondary)
- Projected annual savings (fees + recovered revenue)
- Implementation timeline and migration cost

## 2. Business Profile
- Monthly transaction volume: [count] transactions, $[amount] GMV
- Average order value: $[amount] (range: $[min]–$[max])
- Target markets: [list with percentage breakdown]
- Product type: [physical / digital / subscription / marketplace]
- Current gateway: [name], effective rate: [percentage]
- Technical stack: [platform and relevant integrations]

## 3. Payment Method Coverage Matrix

| Market | Population | Cards | Local Methods | Wallets | BNPL |
|---|---|---|---|---|---|
| [Market 1] | [% of revenue] | [supported networks] | [methods + market share] | [supported wallets] | [providers] |
| [Market 2] | [% of revenue] | [supported networks] | [methods + market share] | [supported wallets] | [providers] |

## 4. Gateway Fee Comparison

### 4a. Per-Transaction Cost Breakdown

| Fee Component | Gateway A | Gateway B | Gateway C |
|---|---|---|---|
| Base rate (% + fixed) | | | |
| Cross-border surcharge | | | |
| Currency conversion markup | | | |
| Chargeback fee | | | |
| Refund fee | | | |
| 3DS authentication fee | | | |
| Network tokenization fee | | | |
| **Effective total rate** | | | |

### 4b. Monthly Fixed Costs

| Component | Gateway A | Gateway B | Gateway C |
|---|---|---|---|
| Platform/subscription fee | | | |
| PCI compliance fee | | | |
| Account maintenance | | | |
| Reporting/analytics | | | |
| **Monthly fixed total** | | | |

### 4c. Projected Monthly Cost at Current Volume

| Scenario | Gateway A | Gateway B | Multi-Gateway |
|---|---|---|---|
| Domestic transactions | | | |
| International transactions | | | |
| Fixed fees | | | |
| **Monthly total** | | | |
| **Annual total** | | | |

## 5. Conversion Performance Analysis

| Metric | Current | Gateway A | Gateway B | Multi-Gateway |
|---|---|---|---|---|
| Overall authorization rate | | | | |
| Domestic authorization rate | | | | |
| International authorization rate | | | | |
| 3DS challenge rate | | | | |
| Smart retry recovery rate | | | | |
| Projected revenue recovered | | | | |

## 6. Multi-Gateway Routing Rules

### Primary Routing

| Transaction Characteristic | Route To | Reason |
|---|---|---|
| [Card type / region / amount] | [Gateway] | [Cost / conversion / method support] |

### Fallback Routing

| Decline Scenario | Fallback Action | Delay |
|---|---|---|
| Soft decline (insufficient funds) | [Retry same gateway after X hours] | |
| Hard decline (do not honor) | [Route to alternate gateway] | |
| Gateway timeout | [Immediate failover to backup] | |

## 7. Total Cost of Ownership

| Component | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| Processing fees | | | |
| Revenue lost to declines | | | |
| Migration/integration cost | | | |
| Ongoing maintenance | | | |
| **Net annual cost** | | | |
| **Cumulative savings vs. current** | | | |

## 8. Implementation Roadmap

| Phase | Timeline | Activities | Success Criteria |
|---|---|---|---|
| Phase 1: Setup | Weeks 1-2 | [Sandbox, API keys, testing] | [All test transactions pass] |
| Phase 2: Integration | Weeks 3-4 | [Development, QA, certification] | [End-to-end flow working] |
| Phase 3: Staged Rollout | Weeks 5-6 | [% traffic migration] | [Auth rate meets threshold] |
| Phase 4: Full Migration | Weeks 7-8 | [Complete cutover, monitoring] | [All KPIs green for 2 weeks] |

## 9. Monitoring Dashboard Metrics
- Real-time authorization rate by gateway and region
- Daily transaction cost per gateway
- Decline reason code distribution
- Failover trigger frequency
- Conversion rate by payment method
- Revenue recovery from smart retries

## 10. Review Schedule
- Weekly: Authorization rates, decline reasons, failover events
- Monthly: Fee reconciliation, volume tier check, routing rule effectiveness
- Quarterly: Gateway contract review, new payment method evaluation, market expansion planning
