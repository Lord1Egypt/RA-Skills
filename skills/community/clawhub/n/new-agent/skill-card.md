## Description:

Create new OpenClaw agents and connect them to messaging channels (Telegram, Discord, Slack, Feishu, WhatsApp, Signal, Google Chat). Supports single and batch mode. Batch mode creates all agents at once with a single config write and gateway restart to avoid connection churn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joansongjr](https://clawhub.ai/user/joansongjr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create one or more OpenClaw agents, register dedicated workspaces, connect messaging channels, and verify gateway bindings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup scripts can make persistent changes to OpenClaw configuration and restart the gateway.

Mitigation: Review the manifest and scripts before execution, run them in a controlled environment, and keep configuration backups available for rollback.

Risk: Channel credentials may be supplied through manifests or configuration files.

Mitigation: Use only manifests you authored and inspected, avoid placing live tokens in chat or version-controlled JSON, and rotate any secrets that may have been exposed.

Risk: Batch setup can add agents to agent-to-agent permissions automatically.

Mitigation: Grant cross-agent permissions only when explicitly needed and remove automatic allow-list changes from local copies if they are not required.

Risk: Unsafe input handling in setup scripts can affect generated paths, identifiers, and configuration entries.

Mitigation: Validate agent IDs as simple slugs and inspect generated workspace paths and config entries before restarting the gateway.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of workspace files and OpenClaw gateway configuration updates.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
