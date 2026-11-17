## Description:

RocketReach (rocketreach.co). Use this skill for ANY RocketReach request — searching and reading data. Whenever a task involves RocketReach, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search RocketReach people and companies and retrieve account information through an OOMOL-connected RocketReach account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing-tool setup directs the agent to run downloaded CLI code without a clear approval step.

Mitigation: Require approval before setup changes and review the CLI release before installation.

Risk: OOMOL mediates RocketReach queries and manages the connected account access.

Mitigation: Consider whether OOMOL is trusted to handle those queries and account access; review or disable automatic agent-skill synchronization.

## Reference(s):

- [RocketReach API documentation](https://docs.rocketreach.co/reference/rocketreach-api)
- [RocketReach](https://rocketreach.co)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-rocket-reach)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON inputs and structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available data depends on the selected RocketReach action and connected account.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
