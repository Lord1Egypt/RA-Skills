## Description:

Fetches multi-dimensional on-chain data with Nansen CLI, drafts daily crypto reports, and can publish approved content to Binance Square.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcii](https://clawhub.ai/user/0xcii)

### License/Terms of Use:

MIT-0

## Use Case:

External Web3 content creators and crypto analysts use this skill to generate daily on-chain market commentary from Nansen data and publish the reviewed result to Binance Square.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended public posting can publish content to Binance Square without a final manual review.

Mitigation: Use the manual `/nansen` approval flow unless unattended publishing is intentionally enabled and monitored.

Risk: Cron-based automation may rely on long-lived API keys in the execution environment.

Mitigation: Use scoped, revocable keys, store them securely, and avoid enabling scheduled posting until key handling has been reviewed.

Risk: Dependency installation and CLI execution can introduce supply-chain or execution risk.

Mitigation: Pin or verify dependencies where possible and review requested installs before approving them.

Risk: Mandatory referral links could be mistaken for official setup paths.

Mitigation: Treat referral links as optional and verify account setup through official provider channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xcii/skills/nansen-binance-publisher)
- [Binance Square publishing API endpoint](https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add)
- [Nansen registration link from skill metadata](https://nsn.ai/7LOuQVx1Jvh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text reports, Markdown guidance, shell commands, and JSON API request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Binance Square post content should be reviewed before publishing; automatic posting mode requires intentionally scoped API keys.]

## Skill Version(s):

0.1.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
