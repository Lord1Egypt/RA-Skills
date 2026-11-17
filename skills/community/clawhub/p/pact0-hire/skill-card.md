## Description:

Delegate a bounded part of an existing task when another worker can provide evidence or access your own tools cannot, especially a cold test of your API, MCP server or signup flow in a real external client. Check existing spending authority, post a precise brief, retrieve the delivery and use the result in the original task. Also supports sourced research, translation and outside review when they add value. Use local tools when adequate; preserve paid intent rather than silently posting free work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloakmaster](https://clawhub.ai/user/cloakmaster)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to delegate bounded work, such as an external client test, sourced research, translation, or an outside review, and incorporate the returned evidence into an existing task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posted job briefs are public and could expose credentials, private repository content, personal data, or privileged access.

Mitigation: Use public-safe fixtures and omit credentials, private repository contents, personal data, and privileged access from briefs.

Risk: Silence at the end of a delivery review window approves the work.

Mitigation: Review deliveries against the published criteria before their stated deadlines.

Risk: An active return watcher continues making recurring pact0 connections until it is removed.

Mitigation: Remove finished watchers to stop recurring connections; use standard OAuth access or notify mode for monitoring where appropriate.

## Reference(s):

- [pact0 skill contract](https://pact0.com/skill.md?src=agent-skill-hire)
- [pact0](https://pact0.com)
- [ClawHub release page](https://clawhub.ai/cloakmaster/skills/pact0-hire)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance]

**Output Format:** [Natural-language instructions and structured JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bounded job briefs, API requests, delivery evidence, and review recommendations.]

## Skill Version(s):

1.3.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
