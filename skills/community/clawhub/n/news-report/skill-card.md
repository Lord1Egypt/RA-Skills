## Description:

Collects topic-specific news from multiple search engines, guides LLM analysis, and generates a self-contained dark dashboard HTML report for delivery to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to collect news about a keyword or topic, synthesize findings with an LLM, and produce a browser-openable HTML intelligence report for user delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External news fetching has known security concerns in the provided scan evidence, including disabled normal TLS verification.

Mitigation: Restore standard TLS certificate and hostname verification before installing or running the skill.

Risk: Generated HTML reports may include unsafe or untrusted report fields.

Mitigation: Escape or strictly sanitize every report field and add a restrictive content security policy for generated reports.

Risk: The skill may search external engines using sensitive internal project names or keywords.

Mitigation: Avoid sensitive keywords until the external-search and privacy behavior is clearly documented and approved.

Risk: Report output and message delivery targets may be inappropriate if fixed or unreviewed paths and destinations are used.

Mitigation: Use user-approved per-run output locations and confirm any Feishu or message delivery target before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallkeyboy/skills/news-report)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown instructions with bash commands and JSON schema; scripts produce JSON data and self-contained HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The fetch step requires network access, and generated reports are local HTML files intended for browser viewing or user delivery.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
