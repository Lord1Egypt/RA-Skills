## Description:

交互式部署多 Agent 团队协作架构，支持自定义团队结构、预设模板和混合模式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maybemarvel](https://clawhub.ai/user/maybemarvel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to create multi-agent team structures through interactive, preset, or mixed configuration flows. It helps generate OpenClaw agent directories, configuration snippets, and follow-up validation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment may copy the main OpenClaw auth and model configuration into generated agent directories.

Mitigation: Use scoped credentials for child agents and review generated agent directories before enabling them.

Risk: User-provided team and member identifiers may affect generated paths and configuration.

Mitigation: Validate identifiers strictly and run the deployment in a non-production OpenClaw environment before merging generated configuration.

Risk: Generated OpenClaw configuration may change agent routing and available tools.

Mitigation: Review the generated openclaw.json snippet and verify it with the included validation script before restarting the gateway.

Risk: The server security verdict is suspicious.

Mitigation: Review or fix scripts/deploy.sh before installation, and do not run it as root or against production credentials until the review is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maybemarvel/skills/multi-agent-teams)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash commands and generated JSON configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bash and OpenClaw; deployment scripts can create directories, copy local OpenClaw auth/model configuration files, and emit an openclaw.json snippet for review.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
