## Description:

Helps agents reduce paid xAI/API token spend by preferring local Ollama workflows, compact responses, and explicit consent before metered model runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to guide budget-conscious model selection, local processing, and confirmation steps before expensive API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Companion scripts and dependency installs may access API keys.

Mitigation: Review the skill and companion repositories before installation, verify dependencies independently, and use the skill only in a controlled workspace.

Risk: Vault, proxy, cron, background, or metered model commands can change execution context or incur cost.

Mitigation: Require explicit confirmation before running those commands and avoid exposing both main and alternate API keys to the same process.

## Reference(s):

- [Quick reference](references/QUICK.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise budget-saving instructions for agent operation; no generated runtime artifact is produced.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
