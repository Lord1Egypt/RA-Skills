## Description:

Book flights for pilgrimage travel to sacred sites and religious destinations, with support for related travel services such as hotels, trains, itinerary planning, visas, insurance, and car rental.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to collect pilgrimage flight parameters, run the flyai CLI, and present real-time booking options with booking links. It is intended for religious and sacred-site travel planning workflows rather than general travel advice from model memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and run a global third-party npm CLI for travel searches.

Mitigation: Require explicit approval before installation, pin and verify the package where possible, and run the CLI in a sandboxed environment.

Risk: The skill uses user-derived values in shell command templates for travel search parameters.

Mitigation: Validate origin, destination, date, and sort parameters against the documented parameter table before command execution.

Risk: Travel results may be misleading if generated from model knowledge instead of live CLI output.

Mitigation: Reject responses that lack detailUrl-based booking links and rerun the CLI rather than fabricating or completing missing results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivan97/skills/pilgrimage-travel)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must be sourced from flyai CLI output and include detailUrl-based booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
