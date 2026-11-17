## Description:

Helps an agent review a multi-asset portfolio, track market data and transactions, and run a role-based investment committee for a symbol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longsizhuo](https://clawhub.ai/user/longsizhuo)

### License/Terms of Use:

MIT-0

## Use Case:

Portfolio owners use the skill to review holdings, performance and decision history, track assets, record transactions, and request structured investment analysis across stocks, funds, ETFs, crypto and commodities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment or portfolio information may be sent to an external model during model-backed workflows, and the security scan reports that privacy disclosures are missing.

Mitigation: Before using those workflows, decide whether you are comfortable sharing the information and review the selected model provider's data handling.

Risk: The suspicious security assessment is based on partial coverage and degraded tool-misuse analysis, so it does not resolve the skill's full risk profile.

Mitigation: Review the skill and its permissions carefully before installation; do not treat the partial scan as proof that the skill is safe or malicious.

## Reference(s):

- [ClawHub openInvest release](https://clawhub.ai/longsizhuo/skills/openinvest)
- [Committee protocol](references/committee-protocol.md)
- [Two analysis paths](references/two-paths.md)
- [Adding assets](references/adding-assets.md)
- [Project documentation](https://github.com/longsizhuo/openInvest/tree/main/docs/wiki)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [JSON results and Markdown reports, with plain-text guidance where appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by command and depend on user-provided portfolio data, available market data, configured credentials and selected model provider.]

## Skill Version(s):

0.34.5 (source: server-resolved release metadata, SKILL.md frontmatter, CHANGELOG, released 2026-11-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
