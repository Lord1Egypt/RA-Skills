## Description:

Local LLM Router helps agents route OpenAI-compatible and Ollama local LLM requests across multiple devices using fleet scoring, context protection, VRAM-aware fallback, and retry behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up, inspect, and operate a self-hosted Ollama routing layer across local machines. It provides setup commands, local API checks, dashboard and analytics queries, and guarded guidance for model-management actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running the router package may execute local software with access to the user's machine and local model fleet.

Mitigation: Use a virtual environment, avoid running pip or the router as root or administrator, and review or pin the package source where possible.

Risk: Model pull and delete actions can download very large files or remove locally available models.

Mitigation: Require explicit user approval before changing settings or pulling or deleting models.

Risk: The skill references local latency, trace, and log files that may contain operational data.

Mitigation: Inspect those files read-only and do not delete or modify files under ~/.fleet-manager/ unless the user explicitly approves.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/local-llm-router)
- [ollama-herd package](https://pypi.org/project/ollama-herd/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, Python, curl, and SQLite command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local setup, diagnostic, API, analytics, and guarded model-management guidance.]

## Skill Version(s):

1.0.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
