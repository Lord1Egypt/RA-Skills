## Description:

Analyzes medical procurement tenders using historical bid data to assess whether to bid, likely competitors, pricing, and qualification risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

Bid teams and medical-device suppliers use the skill to evaluate hospital purchasing opportunities, compare historical awards and prices, and prepare a cited bid-or-no-bid report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bid searches contact Zhiliaobiaoxun services and can consume account credits.

Mitigation: Disclose estimated credit use before analysis, limit queries to the agreed scope, and obtain approval before exceeding the budget.

Risk: Trial registration sends a hashed MAC-derived device identifier and creates an account.

Mitigation: Request explicit consent before collecting device features or registering; use a preconfigured API key to skip registration.

Risk: An automatically issued API key persists in a local configuration file.

Mitigation: Protect access to the configuration file and never include the key in reports or conversation output.

Risk: Account top-ups can use a session-bearing auto-login link.

Mitigation: Share the link only with the account holder and avoid forwarding or logging it.

Risk: Automated bid and pricing recommendations may be incomplete or misleading.

Mitigation: Verify source notices, dates, eligibility requirements, and quoted prices before making a commercial bid decision.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhiliaobiaoxun/skills/medical-device-bid-decision)
- [Bid-analysis workflow](artifact/references/workflow.md)
- [API quick reference](artifact/references/api-quick.md)
- [Report template](artifact/references/report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML files, Guidance]

**Output Format:** [Cited Markdown decision report and local HTML report in full mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bid recommendation, competitor and price analysis, source references, and risk notes.]

## Skill Version(s):

1.0.9 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
