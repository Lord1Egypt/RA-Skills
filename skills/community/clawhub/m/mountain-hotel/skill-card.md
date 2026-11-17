## Description:

Helps agents search flights for mountain hotels and highland resort destinations, with related travel booking support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to collect route details, run live flyai flight searches, and return concise booking-oriented Markdown results for mountain hotel and highland resort travel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags automatic installation of an unpinned global npm CLI.

Mitigation: Ask before installing software, pin and verify the dependency, and prefer local or sandboxed execution.

Risk: Security evidence notes weak input scoping for route and date values and cautions against shell interpolation.

Mitigation: Validate route and date inputs, limit activation to explicit flight-search requests, and pass command arguments without shell interpolation.

Risk: The skill may present booking links from a third-party travel service.

Mitigation: Have users verify price, itinerary, provider terms, and payment details on the provider page before booking.

## Reference(s):

- [Skill Source](SKILL.md)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output and booking links for returned travel results.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
