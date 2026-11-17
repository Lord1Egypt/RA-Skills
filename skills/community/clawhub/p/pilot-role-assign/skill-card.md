## Description:

Assign and manage hierarchical roles within a swarm for coordinated task distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and swarm operators use this skill to advertise agent capabilities, assign role responsibilities, and query role distribution in Pilot Protocol swarms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Role-routing examples handle swarm-supplied values in commands, which can produce unsafe role assignment behavior when data is untrusted.

Mitigation: Use trusted swarm data, pass variables safely to jq, JSON-escape payloads, validate agent IDs and swarm names, and require exact peer matches before sending role assignments.

Risk: The security verdict is suspicious due to unsafe handling in example workflow commands.

Mitigation: Review before installing or using in production, and adapt the examples to local validation and command-safety requirements.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-role-assign)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilot-protocol, pilotctl on PATH, jq, base64, and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
