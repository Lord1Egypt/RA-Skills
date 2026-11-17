## Description:

Risk Guardian analyzes Paradex account, vault, position, market, funding, and orderbook data to produce margin health, liquidation distance, exposure, funding, stress-test, and P&L risk reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sv](https://clawhub.ai/user/sv)

### License/Terms of Use:

MIT-0

## Use Case:

External Paradex users and agents use this skill to check account and vault risk, understand margin utilization and liquidation buffers, evaluate portfolio concentration and funding costs, and receive protective recommendations before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read sensitive Paradex account, vault, position, balance, market, funding, and orderbook data.

Mitigation: Install and invoke it only when that data access is acceptable, and use it for explicit Paradex risk questions.

Risk: Liquidation, margin, and stress-test values are approximate and can differ from the Paradex UI or live mark-price behavior.

Mitigation: Verify critical liquidation and margin numbers in the Paradex UI before taking action.

Risk: The security evidence notes that trigger wording is broader than clearly necessary.

Mitigation: Limit use to Paradex account or vault risk analysis, margin health, liquidation, exposure, drawdown, and alert-monitoring requests.

## Reference(s):

- [Paradex Margin Model & Risk Scoring Reference](references/margin-model.md)
- [ClawHub Skill Page](https://clawhub.ai/sv/skills/paradex-risk-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown risk reports with metric tables, scenario analysis, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory risk analysis and should not be treated as financial advice.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
