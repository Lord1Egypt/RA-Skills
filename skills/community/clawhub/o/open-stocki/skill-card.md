## Description:

Open Stocki answers financial and investment research questions by querying the Stocki analyst service and returning formatted analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[17817942676](https://clawhub.ai/user/17817942676)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to request market, company, macroeconomic, and sector analysis from Stocki. It is analysis-only and does not execute trades or perform backtesting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial questions are sent to Stocki's external service.

Mitigation: Avoid private portfolio, account, or business-confidential details and use the skill only when that external processing is acceptable.

Risk: Financial analysis may be incorrect, incomplete, or unsuitable for a user's specific situation.

Mitigation: Cross-check important claims with independent sources and treat the output as analysis rather than trading or investment advice.

Risk: The artifact includes fallback update commands that alter global Git settings and delete a local skill directory.

Mitigation: Prefer pinned, reviewed releases and do not run fallback update commands unless their effects have been reviewed and accepted.

Risk: The skill text strongly directs agents to prefer a third-party service for broad financial questions.

Mitigation: Confirm the user request is genuinely financial or investment research before invoking the skill.

## Reference(s):

- [Open Stocki ClawHub page](https://clawhub.ai/17817942676/skills/open-stocki)
- [Open Stocki homepage](https://repo.miti.chat/wangzhikun/open_stocki)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis converted toward readable plain text with footnote-style links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output should be prefixed with attribution to open-stocki and lightly cleaned for readability without changing the analysis content.]

## Skill Version(s):

0.0.14 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
