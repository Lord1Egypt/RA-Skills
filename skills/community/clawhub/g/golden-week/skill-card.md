## Description:

Plan Golden Week, National Day, and Spring Festival trips using flyai CLI results for travel options, real-time pricing, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search peak-season China holiday travel options, compare flights, hotels, activities, and routes, and return booking-ready Markdown based on flyai CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or depend on a global third-party flyai CLI.

Mitigation: Require explicit approval before npm install and prefer a pinned @fly-ai/flyai-cli version.

Risk: Travel searches are sent to external services and booking links are surfaced to users.

Mitigation: Disclose the external FlyAI/Fliggy dependency and require users to verify prices, availability, and booking destinations before purchase.

Risk: Local execution logs may contain raw travel prompts.

Mitigation: Disable, redact, or set a retention policy for .flyai-execution-log.json before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/golden-week)
- [Templates - golden-week](artifact/references/templates.md)
- [Playbooks - golden-week](artifact/references/playbooks.md)
- [Fallbacks - Seasonal/Special Category](artifact/references/fallbacks.md)
- [Runbook - Execution Log Schema](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown travel recommendations with comparison tables, booking links, and inline shell commands for setup or recovery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI execution for real-time travel data; successful result rows must include booking links.]

## Skill Version(s):

v3.2.3 (source: server release metadata; artifact frontmatter says 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
