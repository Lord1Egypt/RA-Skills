## Description:

Finds flights during Chinese peak travel seasons including Spring Festival, Golden Week, Labor Day, and Dragon Boat, using the flyai CLI to return real-time travel results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travel agents, developers, and end users use this skill to search holiday flight availability, compare peak-season options, and format real-time flyai CLI results into readable Markdown with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run a third-party CLI globally, including possible sudo use.

Mitigation: Use a sandboxed or pinned local CLI installation, avoid sudo, and approve CLI execution only after reviewing the package source and permissions.

Risk: Raw travel queries may be logged persistently by the skill workflow.

Mitigation: Disable or restrict persistent logging unless users have reviewed and accepted the privacy implications for travel searches.

Risk: The skill relies on shell-style command execution for live travel results.

Mitigation: Limit the agent to documented flyai parameters, inspect generated commands before execution, and do not substitute model knowledge for failed CLI results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/holiday-flights)
- [Parameter and output templates](references/templates.md)
- [Holiday flight playbooks](references/playbooks.md)
- [Fallback recovery guidance](references/fallbacks.md)
- [Execution log runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires successful flyai CLI execution for travel data; final responses should include booking links and avoid raw JSON.]

## Skill Version(s):

v3.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
