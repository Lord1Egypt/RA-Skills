## Description:

InvAssistant is a multi-asset investment portfolio management framework for disciplined US, A-share, and Hong Kong stock reviews, with asset-class rules, portfolio risk controls, and quality scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this agent to review a portfolio, classify holdings, check risk limits, and assess candidates under the framework's US, A-share, and Hong Kong stock rules. Its reports support decisions and require human review before any trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gaps in investment checks could produce misleading portfolio recommendations.

Mitigation: Check input data and rule outcomes, and require human review of every proposed action before any trade.

Risk: Runtime file and network permissions, including optional webhook notifications, need review before use.

Mitigation: Inspect the scripts and configured endpoints before running them; leave webhook helpers unconfigured unless report delivery is intentionally enabled.

Risk: Dependency versions are unpinned, and the security scan was partial because a referenced local path was missing.

Mitigation: Review and pin dependencies, resolve the missing path, and complete a full review before installation.

## Reference(s):

- [InvAssistant release on ClawHub](https://clawhub.ai/haiyangchenbj/skills/invassistant)
- [US stock strategy](artifact/references/us_stock_strategy.md)
- [A-share strategy](artifact/references/a_share_strategy.md)
- [Risk controls and overrides](artifact/references/risk_control_and_overrides.md)
- [Candidate admission gates](artifact/references/candidate_admission_gates.md)
- [Capital plan audit](artifact/references/capital_plan_audit.md)
- [Derived price governance](artifact/references/derived_price_governance.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Configuration, Guidance]

**Output Format:** [Structured Markdown portfolio reviews and risk reports; YAML configuration when initializing settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision support requires sourced, current data and human review; bundled scripts do not place trades autonomously.]

## Skill Version(s):

2.3.22 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
