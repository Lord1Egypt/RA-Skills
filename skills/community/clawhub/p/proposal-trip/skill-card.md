## Description:

Book flights for proposal trips and romantic engagement getaways, with support for related travel planning tasks powered by Fliggy through the flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to search proposal-trip and romantic engagement getaway flights, collect route parameters, run flyai CLI searches, and present bookable flight options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags automatic installation of an unpinned global CLI.

Mitigation: Prefer manual, pinned installation of the flyai CLI in an isolated environment before enabling the skill.

Risk: The security evidence flags execution of user-derived shell commands without clear consent or input-safety controls.

Mitigation: Validate route, date, and option parameters, and require user consent before running installation or travel-search commands.

Risk: The skill depends on FlyAI/Fliggy travel results and provider booking links.

Mitigation: Treat returned prices, availability, and links as provider-sourced travel data that users should confirm before purchasing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivan97/skills/proposal-trip)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown flight recommendations with comparison tables, booking links, and concise CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results are expected to come from flyai CLI output and include provider booking links when available.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
