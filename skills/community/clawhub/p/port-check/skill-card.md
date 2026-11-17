## Description:

Check if services are responding on given host:port pairs. Supports TCP and HTTP checks with configurable timeout. Use for service monitoring, health checks, and network debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check whether TCP or HTTP services respond on specific host:port targets during service monitoring, health checks, and network debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make TCP and HTTP connection attempts to user-specified hosts and ports.

Mitigation: Use explicit host:port targets only for systems you own or administer, and avoid broad or unauthorized network scanning.

Risk: Invalid or unusual host, port, or timeout values are unsupported.

Mitigation: Validate inputs before execution and keep timeout values within expected operational ranges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogue-agent1/skills/port-check)
- [ClawHub publisher profile](https://clawhub.ai/user/rogue-agent1)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks and command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces exit-code-aware checks for user-supplied targets; requires nc and curl.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
