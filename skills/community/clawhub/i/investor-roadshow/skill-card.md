## Description:

Book flights for investor roadshows and IPO fundraising travel, with support for hotels, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel services powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External business travelers and agent users use this skill to collect investor roadshow travel requirements, run live flyai searches, and format flight or related travel options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global third-party CLI.

Mitigation: Require explicit approval before installation, pin the CLI version where possible, and run commands in a constrained environment.

Risk: The third-party CLI may receive itinerary details from user requests.

Mitigation: Share only the minimum travel details needed for the search and confirm user consent for sensitive travel information.

Risk: Unsafe shell command templates can execute malformed or untrusted parameters.

Mitigation: Validate dates, city names, and option values before execution, and avoid interpolating unsanitized user text into shell commands.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/investor-roadshow)
- [Publisher Profile](https://clawhub.ai/user/dingtom336-gif)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown response with CLI-derived travel results, comparison tables, and booking links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output; raw JSON should not be returned to the user.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
