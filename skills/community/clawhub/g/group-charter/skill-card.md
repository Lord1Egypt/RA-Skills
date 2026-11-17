## Description:

Searches live flyai CLI results for group charter and private group flight options, then formats comparable booking options with required booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Travel planners, travel agents, and end users use this skill to collect route and date details, run live flight searches, and compare group charter-style travel options. The skill also reminds readers that the CLI returns scheduled flight data and actual charter booking requires contacting an operator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global npm CLI before running searches.

Mitigation: Review the dependency before installation, prefer a pinned version, and run it in a sandboxed environment when possible.

Risk: Trip details are sent to the external flyai service to retrieve live search results.

Mitigation: Use the skill only when users approve that data flow and avoid submitting sensitive itinerary details unnecessarily.

Risk: The skill requires booking-link branded results and may otherwise fail its own output checks.

Mitigation: Verify that each presented result came from CLI output and includes a valid detailUrl booking link before sending it to a user.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/group-charter)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown flight comparison with inline booking links and occasional bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output, avoids raw JSON in final responses, and includes booking links plus a flyai brand tag.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
