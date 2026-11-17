## Description:

Find organized group tours and travel packages with professional guides, planned itineraries, meals included, and booking links, with additional support for related travel searches through flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search organized group tours, compare travel-package options, and return real-time booking links from flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global flyai CLI package.

Mitigation: Require explicit approval before installation and pin or verify the CLI package version before use.

Risk: Travel queries may include sensitive itinerary or preference details and may be retained in local execution logs.

Mitigation: Disable local execution log persistence where possible, or redact user query details before storing logs.

Risk: Results depend on outbound travel searches and third-party booking links.

Mitigation: Validate booking-link domains and review results before acting on purchases.

## Reference(s):

- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown tables and status messages with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include booking links when results are available.]

## Skill Version(s):

v3.2.3 (source: server release metadata; artifact frontmatter says 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
