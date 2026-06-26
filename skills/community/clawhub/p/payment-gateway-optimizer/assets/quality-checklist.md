# Payment Gateway Optimization — Quality Checklist

## Business Context (7 items)
- [ ] Monthly transaction volume documented (count and GMV)
- [ ] Average order value and distribution captured
- [ ] All target markets listed with revenue percentages
- [ ] Product type classification identified (physical, digital, subscription, marketplace)
- [ ] Current gateway and effective rate documented
- [ ] Current pain points and switching triggers listed
- [ ] Technical stack and integration constraints noted

## Payment Method Coverage (8 items)
- [ ] Card network requirements mapped per market
- [ ] Local payment methods identified with market share data
- [ ] Digital wallet requirements documented
- [ ] BNPL options evaluated for each market
- [ ] Bank transfer and direct debit options assessed
- [ ] Cash-based payment alternatives considered where relevant
- [ ] Mobile payment apps evaluated for applicable markets
- [ ] Payment method prioritization matches actual customer preferences

## Fee Analysis (8 items)
- [ ] Per-transaction fees broken down (not just headline rates)
- [ ] Cross-border and international card fees calculated separately
- [ ] Currency conversion markups quantified
- [ ] Monthly and annual platform fees included
- [ ] Chargeback and dispute fees compared
- [ ] Hidden fees identified (PCI compliance, AVS, batch fees, etc.)
- [ ] Volume discount thresholds analyzed
- [ ] Refund fee policies compared

## Conversion Performance (7 items)
- [ ] Authorization rates compared by card type and region
- [ ] 3D Secure implementation strategy evaluated
- [ ] Smart exemption capabilities assessed
- [ ] Network tokenization support checked
- [ ] Retry and recovery capabilities compared
- [ ] Checkout UX impact evaluated (redirect vs. embedded vs. drop-in)
- [ ] Revenue impact of conversion rate differences calculated

## Multi-Gateway Strategy (7 items)
- [ ] Primary routing rules defined by transaction characteristics
- [ ] Fallback routing specified for each decline type
- [ ] Geographic routing leverages local acquiring
- [ ] Cost-based routing rules for high-value transactions
- [ ] Gateway timeout and failover thresholds set
- [ ] A/B testing framework designed for ongoing optimization
- [ ] Single point of failure eliminated

## Cost Modeling (6 items)
- [ ] 12-month cost projection completed at current volume
- [ ] Growth scenario projections included (2x, 3x)
- [ ] Migration and integration costs estimated
- [ ] Revenue recovered from improved conversion rates factored in
- [ ] Break-even timeline calculated for migration investment
- [ ] Working capital impact of payout timing differences assessed

## Implementation Planning (6 items)
- [ ] Integration timeline realistic with clear milestones
- [ ] Sandbox testing phase included
- [ ] Staged rollout strategy defined (not big-bang migration)
- [ ] Card-on-file migration plan addressed (for gateway switches)
- [ ] PCI compliance requirements met for new gateways
- [ ] Rollback plan documented in case of issues

## Monitoring and Optimization (6 items)
- [ ] Real-time authorization rate monitoring defined
- [ ] Daily cost tracking by gateway specified
- [ ] Decline reason code analysis planned
- [ ] Failover event alerting configured
- [ ] Monthly fee reconciliation process established
- [ ] Quarterly review cadence for routing rules and gateway performance
