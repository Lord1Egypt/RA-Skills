## Description:

Automated paper trading on Polymarket using AI agents. Monitors trends, manages portfolio, and executes trades based on strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to generate Polymarket market monitoring reports, portfolio status summaries, and trade-opportunity notes. It is best treated as a paper-trading report sender unless reviewed and adapted for a real trading workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found the skill suspicious because it appears to send generated reports to a hardcoded Discord channel.

Mitigation: Review and edit the Discord destination before running the skill, or disable outbound notification delivery.

Risk: The security review says the skill looks more like a mock Polymarket report sender than a real trading autopilot.

Mitigation: Treat generated trade opportunities as informational paper-trading output unless the implementation is independently reviewed for real execution.

Risk: The security guidance notes local status is written under a hardcoded path.

Mitigation: Change the status path to an expected workspace location and verify write permissions before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyhot/skills/polymarket-autopilot)
- [Polymarket CLOB API endpoint](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style report text with optional shell command and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports are truncated before Discord delivery.]

## Skill Version(s):

1.0.0 (source: release evidence, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
