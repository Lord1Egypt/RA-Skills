## Description:

Find overnight and late-night departure flights, often 20-40% cheaper than daytime, and support related travel booking tasks through Fliggy-powered flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to find and compare late-night or overnight flight options. The skill guides agents to collect trip parameters, run flyai CLI searches, and present real-time results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install or possibly sudo-install a global CLI.

Mitigation: Use an isolated environment where flyai CLI is preinstalled by a trusted administrator, and avoid automatic global or sudo npm installs.

Risk: The skill runs shell commands built from user travel parameters.

Mitigation: Validate and quote city, airport, date, budget, and class inputs before command execution; do not pass untrusted raw text into a shell.

Risk: The runbook describes persisting raw travel queries locally.

Mitigation: Disable the raw execution log or tightly control access, retention, and contents so sensitive itinerary details are not retained unnecessarily.

## Reference(s):

- [Overnight Flights on ClawHub](https://clawhub.ai/xiejinsong/skills/overnight-flights)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel results; every shown travel result should include a booking link when available.]

## Skill Version(s):

3.2.1 (source: server release metadata; artifact frontmatter reports 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
