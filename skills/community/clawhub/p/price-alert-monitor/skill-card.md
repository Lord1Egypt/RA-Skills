## Description:

Price Alert Monitor helps agents manage a local command-line list of product price alerts and check simulated price changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to add product URLs, set target prices, list monitored products, and run local checks. The current implementation uses simulated prices and local terminal output rather than reliable retailer data or real notification delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake simulated price checks for reliable live retailer prices.

Mitigation: Treat results as local test data until real price retrieval is implemented through vetted retailer APIs or a compliant data source.

Risk: Product URLs and target prices are stored in ~/.price-monitor.json on the local machine.

Mitigation: Avoid adding sensitive shopping or account-specific URLs on shared systems, review file permissions, and delete the local state file when it is no longer needed.

Risk: The documentation describes email and webhook notifications, but the current script only prints local messages.

Mitigation: Do not rely on the skill for time-sensitive purchase decisions until notification delivery is implemented and tested.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sxliuyu/skills/price-alert-monitor)
- [Publisher Profile](https://clawhub.ai/user/sxliuyu)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Command-line text and local JSON state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores monitored product URLs, last simulated prices, and target prices in ~/.price-monitor.json.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release evidence, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
