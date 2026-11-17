## Description:

Create and repair durable OpenClaw agents, bindings, and runtime state with verification against live OpenClaw state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create, repair, route, and verify durable OpenClaw subagents while avoiding unsupported session-based spawning claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The creation script can delete or replace an existing target workspace.

Mitigation: Back up OpenClaw state first, validate agent IDs, enforce destinations under OPENCLAW_HOME/workspaces, and require explicit confirmation before overwriting any workspace.

Risk: The default cloning behavior can copy broad workspace contents.

Mitigation: Use an explicit trusted source workspace and patch the script to skip sensitive files and symlinks.

Risk: Untrusted agent IDs or source workspaces can cause unintended OpenClaw state changes.

Mitigation: Use only trusted agent IDs and source workspaces, then verify final agents and bindings with OpenClaw JSON output before reporting success.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matthewxmurphy/skills/openclaw-agent-orchestrator)
- [Publisher profile](https://clawhub.ai/user/matthewxmurphy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON verification output references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw CLI runtime state verification before reporting created agents or bindings.]

## Skill Version(s):

0.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
