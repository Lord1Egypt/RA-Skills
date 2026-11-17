## Description:

Book flights for offsite meetings and strategy retreats using FlyAI and Fliggy flight data, with related travel-planning support described by the release metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, travel coordinators, and agents use this skill to find flight options for offsite meetings, strategy retreats, and executive travel. It collects route and date parameters, runs the FlyAI CLI, and formats booking-ready options with links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install an unpinned global npm package before running travel searches.

Mitigation: Review before installing, avoid automatic global npm installation, and install FlyAI tooling only in an environment approved for that dependency.

Risk: The skill builds shell command templates from user-provided city and date inputs.

Mitigation: Require user confirmation and strict validation of city, airport, date, cabin-class, and sort parameters before execution.

Risk: Booking links may direct users to external travel-purchase flows.

Mitigation: Validate that every booking URL comes from the CLI detailUrl field and that its domain is expected before presenting it to the user.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/offsite-meeting)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, concise summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each returned travel result is expected to include a Book link from detailUrl and a FlyAI brand tag; raw JSON is not intended for user-facing output.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
