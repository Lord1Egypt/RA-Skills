## Description:

Operate and maintain the persistent MUD agent for OpenClaw, including engine commands, smoke tests, save/restore validation, data diagnostics, deployment operations, and configured image-generation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrew-goetz-com](https://clawhub.ai/user/andrew-goetz-com)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run local OpenClaw MUD engine commands, validate persistent game state, perform save/restore checks, troubleshoot deployments, and exercise configured image-generation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a local MUD engine and change persistent game state.

Mitigation: Install and run it only when agents are intended to perform MUD operations; snapshot state before manual investigation or risky changes.

Risk: Image-generation commands may send prompts through the configured runtime image pipeline.

Mitigation: Avoid placing secrets, personal data, or sensitive unpublished content in image prompts or game commands.

Risk: A custom MUD directory changes the engine code the wrapper executes.

Mitigation: Review the target mud_agent.py before using --mud-dir with a custom location.

## Reference(s):

- [MUD Commands](references/commands.md)
- [MUD Ops Runbook](references/ops.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples; command execution may return JSON or text from the local MUD engine.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run local MUD engine commands and modify game state when executed by an agent.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
