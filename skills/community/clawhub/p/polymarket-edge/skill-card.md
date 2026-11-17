## Description:

Polymarket Edge lets agents browse Polymarket markets, inspect prices and order books, run BTC EMA crossover signals, view portfolio positions, and optionally operate a live auto-trader with per-call SkillPay billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icloud-git](https://clawhub.ai/user/icloud-git)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to give an agent access to Polymarket market data, BTC-focused trading signals, portfolio lookups, and optional automated trading workflows. It is suited for deployments where prediction-market analysis and billing controls are reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billing and auto-trader controls are exposed without real authentication.

Mitigation: Deploy only behind authenticated access, scope auto-trader controls to the owning user, and require explicit trade confirmations before enabling live trading.

Risk: A hardcoded SkillPay API key fallback is present.

Mitigation: Rotate and remove the embedded key, require SKILL_BILLING_API_KEY from the deployment environment, and audit logs for unexpected billing use.

Risk: Live trading can use an EVM private key and place market orders when enabled.

Mitigation: Use a dedicated low-balance wallet, set spending limits, verify user identity, and keep live trading disabled until operational controls are reviewed.

Risk: Dependencies are declared with broad lower bounds.

Mitigation: Pin and review dependency versions before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/icloud-git/skills/polymarket-edge)
- [Publisher Profile](https://clawhub.ai/user/icloud-git)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)
- [SkillPay Billing API](https://skillpay.me/api/v1/billing)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON API responses with market data, strategy signals, portfolio values, billing status, and top-up links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include BUY_YES, BUY_NO, HOLD, or SKIP recommendations, order-book snapshots, OHLCV history, auto-trader status, and billing outcomes.]

## Skill Version(s):

1.0.0 (source: server release metadata and FastAPI app version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
