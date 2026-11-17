## Description:

InvAssistant applies a multi-asset portfolio framework with A/B/C asset classes, portfolio risk controls, and quality scoring across US, A-share, and Hong Kong stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Investors can use the skill to review portfolio holdings, apply asset-class and risk rules, score candidates, and examine trade records across US, A-share, and Hong Kong stocks. Its reports support human decisions and do not place trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found recommendation-logic flaws that may produce misleading financial guidance.

Mitigation: Check outputs against current, sourced portfolio and market data, and require human review before acting.

Risk: Review coverage is partial because a referenced path was missing.

Mitigation: Review or restore the missing reference before relying on conclusions that depend on it.

Risk: The security review did not establish that dependency versions are safe.

Mitigation: Review the dependencies and installation environment before installing the bundled scripts.

Risk: When optional notifications are enabled, report content is sent to a user-configured webhook.

Mitigation: Verify the endpoint and report contents before configuring or sending notifications.

## Reference(s):

- [InvAssistant release on ClawHub](https://clawhub.ai/haiyangchenbj/skills/invassistant)
- [US stock strategy](artifact/references/us_stock_strategy.md)
- [A-share strategy](artifact/references/a_share_strategy.md)
- [Risk control and overrides](artifact/references/risk_control_and_overrides.md)
- [Candidate admission gates](artifact/references/candidate_admission_gates.md)
- [Capital plan audit](artifact/references/capital_plan_audit.md)
- [Derived price governance](artifact/references/derived_price_governance.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured portfolio review with classification and risk tables, observations, and data-source annotations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on supplied portfolio information and available market data; outputs require human review and do not execute trades.]

## Skill Version(s):

2.3.21 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
