## Description:

LinkFox Amazon Ads helps agents authorize Amazon Ads accounts, manage SP/SB/SD ad entities, and fetch structured advertising reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce advertisers and their agents use this skill to connect Amazon Ads accounts, query and update campaign entities, adjust bids or budgets after confirmation, and retrieve SP/SB/SD performance reports.

### Deployment Geography for Use:

Amazon Ads NA, EU, and FE marketplaces.

## Known Risks and Mitigations:

Risk: The skill handles Amazon Ads account access, credentials, and business reporting data.

Mitigation: Install only when the user trusts LinkFox with Amazon Ads access and store API keys in a secret manager rather than shell startup files.

Risk: Create, update, bid, and budget actions can change advertising spend.

Mitigation: Require explicit user confirmation before any create, update, budget, or bid operation and provide an execution receipt afterward.

Risk: Custom gateway or login environment variables and report-serving behavior can widen exposure paths.

Mitigation: Avoid custom gateway or login environment variables, disable report HTTP serving unless needed, and keep any report serving bound to loopback addresses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-ads)
- [ClawHub Publisher Profile](https://clawhub.ai/user/linkfox-ai)
- [Skill Definition](artifact/SKILL.md)
- [Amazon Ads Authorization Reference](artifact/references/linkfox-amazon-ads-auth.md)
- [Amazon Ads Management Reference](artifact/references/linkfox-amazon-ads-manager.md)
- [Amazon Ads Reporting Reference](artifact/references/linkfox-amazon-ads-report.md)
- [Report Types Index](artifact/references/report-types/index.md)
- [Authentication and Billing Onboarding](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON payloads, tables, file paths, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write complete API responses and report data to workspace files; report retrieval can return local download paths and short-lived extracted-file links.]

## Skill Version(s):

1.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
