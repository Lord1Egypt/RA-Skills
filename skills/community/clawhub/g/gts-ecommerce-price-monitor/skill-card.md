## Description:

Monitor competitor product prices across major e-commerce platforms, set up automated tracking and alerts, and generate comparison reports for pricing decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, dropshippers, and small business owners use this skill to track competitor product URLs, monitor price changes, receive alerts, and create reports that support pricing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores product URLs, price history, and alert settings in local files.

Mitigation: Track only marketplace URLs you are comfortable storing locally and remove old history or alert files when they are no longer needed.

Risk: Scheduled browser scans and external notifications may run repeatedly or send updates to unintended channels.

Mitigation: Review scan intervals and notification destinations before enabling automated scans.

Risk: Generated CSV reports can carry spreadsheet-handling risk when opened in office tools.

Mitigation: Open generated CSV files cautiously and inspect exported values before sharing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ericlooi504/skills/gts-ecommerce-price-monitor)
- [Platform-Specific Notes](references/PLATFORMS.md)
- [Advanced Configuration](references/CONFIG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands plus JSON, JSONL, CSV, and terminal report outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local tracking files, price history, alert configuration, scheduled scan setup, and CSV reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
