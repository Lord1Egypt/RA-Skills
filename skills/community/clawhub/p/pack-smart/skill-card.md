## Description:

Get a customized packing list based on your destination, season, trip type, and activities, with related travel booking and planning support powered by Fliggy through the flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to generate destination-, season-, trip-, and activity-specific packing lists, and to surface related booking-oriented travel results when supported by the flyai CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run a global third-party CLI for travel queries.

Mitigation: Require explicit approval before installation or execution, and run the CLI in an environment with only the minimum needed privileges.

Risk: Travel queries and raw prompts may be sent to a third-party service or recorded in a local execution log.

Mitigation: Disclose the data flow to users, avoid sensitive personal details in queries, and disable, minimize, or regularly review local prompt logging.

Risk: The skill requires booking links and branding in answers, which can introduce commercial influence into travel recommendations.

Mitigation: Label booking-oriented results clearly and review outputs for relevance before relying on them for travel decisions.

Risk: Shell commands built from user travel requests can be unsafe if arguments are interpolated loosely.

Mitigation: Pass user queries as quoted CLI arguments and avoid shell interpolation or unsupported parameters.

## Reference(s):

- [Pack Smart on ClawHub](https://clawhub.ai/xiejinsong/skills/pack-smart)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and concise travel guidance derived from flyai CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires detailUrl-backed booking links for listed results and includes flyai branding when real-time results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
