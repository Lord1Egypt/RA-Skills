## Description:

CLI assistance for querying Prometheus and PromQL-compatible engines, including instant queries, range queries, metric discovery, troubleshooting, and table, CSV, JSON, or graph output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to run PromQL queries, inspect metrics and labels, visualize range-query trends, and troubleshoot latency, errors, saturation, and other observability issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance references third-party binaries and system-wide placement.

Mitigation: Review install steps before use, prefer a user-local install path, pin an immutable version, and verify checksums or signatures for promql-cli before executing it.

Risk: Prometheus tokens, password files, TLS keys, or production monitoring data could be exposed if pasted into agent chat or passed through shell history.

Mitigation: Configure credentials manually in local files with restricted permissions and do not paste monitoring credentials into the agent conversation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/promql-cli)
- [Publisher homepage](https://github.com/samber/cc-skills)
- [promql-cli documentation](https://github.com/nalbury/promql-cli)
- [promql-cli releases](https://github.com/nalbury/promql-cli/releases)
- [Installation reference](references/installation.md)
- [Usage reference](references/usage.md)
- [Debugging methodology](references/debugging.md)
- [PromQL reference](references/promql-reference.md)
- [ASCII graphing reference](references/graphing.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline PromQL, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include table, CSV, JSON, raw API response, or ASCII graph output formats produced by promql-cli.]

## Skill Version(s):

1.1.3 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
