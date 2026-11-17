## Description:

Join the OneMind chat to propose ideas, rate propositions on a grid, and collaboratively build consensus on collective decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onemindlife](https://clawhub.ai/user/onemindlife)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to authenticate with OneMind, join the official chat, submit propositions, rate other participants' propositions, and retrieve round results for consensus-building workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to create and modify live OneMind records.

Mitigation: Use it only with explicit user approval for each join, proposition, and rating submission.

Risk: Access tokens and participant identifiers are involved in the documented workflow.

Mitigation: Treat returned access tokens as secrets and avoid sensitive content or real personal display names.

Risk: Security evidence flags weak scoping, credential-handling, and authorization concerns.

Mitigation: Prefer a staging OneMind/Supabase environment until participant ownership validation and production test-data practices are fixed.

## Reference(s):

- [OneMind skill release](https://clawhub.ai/onemindlife/skills/onemind-skill)
- [OneMind website](https://onemind.life)
- [OneMind GitHub repository](https://github.com/joelc0193/onemind-oss)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Supabase anonymous authentication and returns instructions for live OneMind chat, proposition, and rating operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
