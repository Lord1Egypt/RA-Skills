## Description:

Rebuilds a TradingAgents Python environment under ~/TradingAgents by recreating the virtual environment, installing the local package, and committing and pushing workspace changes to a remote Git repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonxu](https://clawhub.ai/user/canonxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need an agent to rebuild a local TradingAgents development environment, reinstall the package, summarize repository changes, and publish those changes to a configured remote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill deletes ~/TradingAgents/venv while rebuilding the local environment.

Mitigation: Confirm the target workspace and back up any needed virtual environment state before running the rebuild.

Risk: The skill installs local package code into the rebuilt Python environment.

Mitigation: Review the local package and dependency changes before installation.

Risk: The skill automatically stages, commits, creates a branch, and pushes all unignored workspace changes.

Mitigation: Inspect git status, remove secrets or unrelated files, verify the remote origin, and require explicit approval before commit or push.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canonxu/skills/my-stock-tradeagents-rebuild-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/canonxu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs operational guidance for local shell execution; no structured API response is defined.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
