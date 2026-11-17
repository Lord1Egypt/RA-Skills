## Description:

Port Manager tracks and manages system port usage for conflicts, queries, releases, and recorded service ports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[damiencronw](https://clawhub.ai/user/damiencronw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local port usage, record service-port assignments, check for conflicts, allocate available ports, and release occupied ports during local development and service setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can terminate local processes while releasing ports.

Mitigation: Use only in local development contexts, avoid elevated privileges, and verify the exact process and PID before approving any port release.

Risk: Loose port input handling can increase the chance of acting on the wrong target.

Mitigation: Validate port numbers before use, quote command arguments, and show every target PID before termination.

Risk: Bundled sample port records may be mistaken for user-specific state.

Mitigation: Remove or clearly label sample records before deployment.

## Reference(s):

- [ClawHub Port Manager skill page](https://clawhub.ai/damiencronw/skills/port-manager)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and local port-management guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local process termination commands for ports the user asks to release.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
