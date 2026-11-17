## Description:

Book Lunar New Year flights for Spring Festival reunion and Chinese New Year travel, with related travel support for hotels, trains, attractions, itinerary planning, visa information, insurance, and car rental through Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bufferstreamer](https://clawhub.ai/user/bufferstreamer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search Lunar New Year and Chinese New Year travel options through the flyai CLI, compare returned flights, and present booking links in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install an unpinned global npm package before running travel searches.

Mitigation: Run it in a sandbox or low-risk environment and prefer a pinned, reviewed @fly-ai/flyai-cli installation.

Risk: User-provided travel fields are inserted into shell command templates.

Mitigation: Review generated commands and validate origin, destination, and date values before execution.

Risk: Booking links and travel results depend on the trusted behavior of the flyai CLI and its returned URLs.

Mitigation: Use only detailUrl links returned by the CLI and verify route, price, and booking destination before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bufferstreamer/skills/lunar-new-year-flight)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output; booking results must include detailUrl links and the flyai brand tag.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
