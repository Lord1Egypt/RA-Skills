## Description: <br>
Surfaces live ranked Superior Trade market-intelligence scans and single-pair setup details across Hyperliquid alts and HIP-3 markets, including bucket fits, engine-selected timeframes, score drivers, and deploy templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, traders, and developers use this skill to inspect live ranked market setups, explain why a pair scored in a bucket, and decide whether to continue into setup review, backtesting, and deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide users from market scans into live automated trading, where losses can occur. <br>
Mitigation: Require explicit user confirmation before backtesting, deployment, or live-trading steps, and present the scan as decision support rather than financial advice. <br>
Risk: Wallet credential submission is part of the deployment workflow. <br>
Mitigation: Handle credentials only through the documented credential endpoint, avoid exposing secrets in conversation or logs, and confirm the user understands the credential model before submission. <br>
Risk: Using stale or improvised market rankings can mislead trading decisions. <br>
Mitigation: Use the live Superior Trade scan or setup endpoints, show the returned computed_at timestamp, and avoid substituting training-data prices or manually reweighting scores. <br>
Risk: Low-liquidity markets may create slippage and unsafe live deployments. <br>
Mitigation: Treat watch-tier pairs as backtest-only, avoid microcap live deployment, and surface liquidity tier and daily volume before recommending next steps. <br>
Risk: A suspicious security verdict notes insufficient guardrails around trading deployment and wallet credentials. <br>
Mitigation: Review the skill carefully before installing and enforce consent gates before backtest, deployment, and credential workflows. <br>


## Reference(s): <br>
- [Intelligence API](references/api.md) <br>
- [The Four Buckets](references/buckets.md) <br>
- [Glossary](references/glossary.md) <br>
- [Intelligence Workflows](references/workflow.md) <br>
- [Superior Trade Intelligence](https://account.superior.trade/intelligence) <br>
- [Superior Trade API](https://api.superior.trade) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, API calls, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with API request details, ranked setup summaries, tables, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live Superior Trade API data and should cite returned snapshot fields, scores, computed_at timestamps, liquidity tier, and AI Critic concerns before any deployment recommendation.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
