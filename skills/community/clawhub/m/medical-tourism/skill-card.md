## Description:

Helps agents collect medical travel flight details, run the flyai CLI for real-time options, and return booking-oriented Markdown with validated links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bufferstreamer](https://clawhub.ai/user/bufferstreamer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search for flights for medical tourism, health checkups, and overseas treatment trips while preserving booking links from real-time CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and invoke an external flight-search CLI using user-provided travel fields.

Mitigation: Review the CLI before installation, prefer a pinned and isolated install, and validate origin, destination, and date values before execution.

Risk: Booking links and travel results depend on external CLI output.

Mitigation: Only present results that include validated detailUrl booking links and avoid filling missing results from model knowledge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bufferstreamer/skills/medical-tourism)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown flight search summaries with inline CLI commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires each listed result to include a Book link from the CLI detailUrl field.]

## Skill Version(s):

3.2.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
