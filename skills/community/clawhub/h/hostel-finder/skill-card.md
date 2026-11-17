## Description:

Helps agents search for flights to destinations with backpacker hostels and budget accommodations by using flyai CLI results and formatting bookable options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to collect flight search parameters, run route searches through flyai, and present bookable travel options for hostel or budget-accommodation trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and execute a third-party global npm package for travel searches.

Mitigation: Review and approve the dependency before installation, run it in a contained environment, and avoid automatic global installs.

Risk: Shell command templates can become unsafe if raw user input is interpolated into CLI parameters.

Mitigation: Validate origin, destination, date, sort, journey, and price values against the documented parameter set before execution.

Risk: The skill requires booking links and flyai branding in the result output.

Mitigation: Confirm each booking link comes from the CLI detailUrl field and disclose the third-party booking flow to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/hostel-finder)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output and should not emit raw JSON.]

## Skill Version(s):

3.2.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
