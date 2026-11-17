## Description:

OpenClaw+ supports chained developer workflows involving Python execution, package management, git, HTTP requests, file operations, process management, sub-agents, and webhook notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shindo957-official](https://clawhub.ai/user/shindo957-official)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate multi-step development tasks such as running code, installing packages, retrieving web or API data, editing files, managing processes, coordinating sub-agents, sending notifications, and committing results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines broad code execution, package installation, git, filesystem, process, network, sub-agent, and webhook capabilities.

Mitigation: Review each proposed action before execution and run the skill only in a disposable workspace, container, or virtual environment.

Risk: Package installation, system package installation, file deletion, commits, and background processes can alter the host environment or repository state.

Mitigation: Require explicit approval for installs, deletes, commits, and long-running processes; prefer pinned packages and isolated environments.

Risk: HTTP requests, API calls, sub-agent prompts, and webhooks can expose sensitive information if secrets are included.

Mitigation: Keep secrets in environment variables or a secret manager, redact them from prompts and logs, and restrict outbound destinations to reviewed HTTPS endpoints.

## Reference(s):

- [OpenClaw+ README](README.md)
- [OpenClaw+ Quick Start Guide](QUICKSTART.md)
- [OpenClaw+ Capability Reference](REFERENCE.md)
- [OpenClaw+ Evaluation Examples](evals/evals.json)
- [ClawHub Skill Page](https://clawhub.ai/shindo957-official/skills/openclaw-plus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with code blocks, command output summaries, JSON snippets, and file change descriptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in local file, git, package, process, network, sub-agent, or webhook actions depending on the host agent's execution policy.]

## Skill Version(s):

1.1.0 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
