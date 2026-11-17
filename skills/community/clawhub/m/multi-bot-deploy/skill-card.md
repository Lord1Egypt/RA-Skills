## Description:

Deploys multiple OpenClaw Feishu bot agents by turning user-provided bot names, roles, model choices, and Feishu credentials into agent creation, account configuration, route binding, gateway restart, and validation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bacon-123](https://clawhub.ai/user/bacon-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to set up and connect multiple Feishu bot agents with consistent naming, account configuration, route binding, and validation output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Feishu app credentials and writes them into OpenClaw channel configuration.

Mitigation: Use it only in a controlled admin environment, avoid pasting secrets into normal chat where possible, and rotate any credentials that may have been exposed.

Risk: The skill changes live OpenClaw agents, route bindings, and gateway state.

Mitigation: Validate bot IDs, roles, model choices, and bindings before execution, keep a configuration backup, and review the resulting agent list and bindings after restart.

Risk: OpenClaw configuration backups can retain Feishu credentials.

Mitigation: Restrict access to backup files and review or remove old backups after deployment.

## Reference(s):

- [OpenClaw Agents documentation](https://docs.openclaw.ai/cli/agents)
- [OpenClaw Channels documentation](https://docs.openclaw.ai/cli/channels)
- [Feishu Open Platform documentation](https://open.feishu.cn/document)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks, configuration summaries, and validation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single setup flow that may update OpenClaw agent, Feishu channel, route binding, and gateway state.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
