## Description:

Book flights for graduation trips and post-graduation vacations using the flyai CLI, with support for related travel planning tasks powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search and compare graduation-trip flight options from user-provided origins, destinations, and dates. The agent collects missing route details, runs flyai commands, and returns Markdown results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install an unpinned global npm package.

Mitigation: Require explicit user approval, pin and verify the CLI package, and prefer an isolated or local install before use.

Risk: Shell-style commands may be built from user travel text.

Mitigation: Validate and escape route and date parameters, invoke the CLI without a shell where possible, and allow only documented flags.

Risk: Flight searches may send itinerary details to flyai or Fliggy and return provider booking links.

Mitigation: Inform users before running searches and avoid sending unnecessary personal or sensitive travel details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/graduation-trip)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be grounded in flyai CLI results and include booking links for listed flight options.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
