## Description:

Monitor network connectivity and diagnose latency issues using ping and traceroute.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support engineers use this skill to check host reachability, trace network routes, monitor uptime, sweep small authorized subnets, and analyze historical latency results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sweep small subnets and may probe hosts on networks where the user lacks authorization.

Mitigation: Run sweep only against networks you own or are explicitly authorized to test.

Risk: Ping, traceroute, monitor, compare, and sweep results are retained locally under ~/.ping.

Mitigation: Review and delete ~/.ping/data.jsonl when retained network history is no longer needed.

Risk: The export command writes to the caller-provided PING_OUTPUT path.

Mitigation: Set PING_OUTPUT only to an intended destination and avoid overwriting important files.

## Reference(s):

- [Ping ClawHub listing](https://clawhub.ai/xueyetianya/skills/ping)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and local JSON/CSV history exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local history and configuration under ~/.ping; export can write JSON or CSV to stdout or to PING_OUTPUT.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
