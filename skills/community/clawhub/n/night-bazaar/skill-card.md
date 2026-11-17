## Description:

Finds night markets, food streets, local culinary hotspots, and related travel options using flyai CLI output powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search for night markets, street food, local attractions, and travel booking options from real-time flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt installation and execution of a third-party CLI.

Mitigation: Review before installing, run only in a sandbox or controlled environment, and do not allow automatic global npm installation.

Risk: CLI commands may be built from user-provided city or keyword text.

Mitigation: Sanitize parameters, avoid shell interpolation, and pass arguments through structured command APIs where available.

Risk: Travel searches can include sensitive personal, itinerary, or travel-document details and the artifact includes a local execution log pattern.

Mitigation: Avoid entering sensitive personal or travel-document details and disable raw prompt logging by default.

## Reference(s):

- [Templates - night-market](references/templates.md)
- [Playbooks - night-market](references/playbooks.md)
- [Fallbacks - Attraction Category](references/fallbacks.md)
- [Runbook - Execution Log Schema](references/runbook.md)
- [Night Bazaar ClawHub Page](https://clawhub.ai/xiejinsong/skills/night-bazaar)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, status messages, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel data, includes Book links from detailUrl values, and avoids raw JSON in user-facing responses.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
