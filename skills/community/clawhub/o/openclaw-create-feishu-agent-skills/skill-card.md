## Description:

Create and wire a new OpenClaw agent with a fixed Feishu-only workflow for agent runtime setup, routing configuration, gateway restart, and binding verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaowen-0725](https://clawhub.ai/user/xiaowen-0725)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create an OpenClaw agent and update Feishu routing for either a dedicated bot account or a peer-based group/direct binding. It guides required inputs, backs up and upserts OpenClaw configuration, restarts the gateway, and reports binding verification results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app secrets can be exposed when passed through command-line arguments, terminal output, shell history, or logs.

Mitigation: Do not pass real Feishu app secrets through --app-secret unless secret handling is changed to use a protected input path and redact output; rotate any secret that may already have been exposed.

Risk: The skill can make persistent OpenClaw Feishu routing changes and restart the gateway.

Mitigation: Install and use it only when those changes are intended; review the target account or peer route, keep the generated backup, and verify bindings after restart.

## Reference(s):

- [Routing Modes Reference](references/routing-modes.md)
- [ClawHub Skill Page](https://clawhub.ai/xiaowen-0725/skills/openclaw-create-feishu-agent-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command results, config-change summaries, and verification status.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
