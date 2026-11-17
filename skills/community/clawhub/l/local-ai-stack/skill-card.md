## Description:

Helps Mac users set up a local AI workstation with Ollama, OpenCode, selected local language models, usage commands, troubleshooting guidance, and optional model update scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaysclawd-cloud](https://clawhub.ai/user/jaysclawd-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to install and operate local coding and reasoning models on macOS while reducing cloud API dependence. It is most useful for privacy-sensitive, cost-sensitive, or offline local AI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to pipe a remote installer into a shell.

Mitigation: Prefer the official Ollama download or a verified package path, and review installer contents before execution.

Risk: The skill suggests recurring model update persistence through cron.

Mitigation: Add scheduled updates only after reviewing the local update script, confirming safe file permissions, and documenting how to disable the job.

Risk: The skill describes the setup as fully offline even though installation, model pulls, and updates require network access.

Mitigation: Treat setup and updates as internet-connected steps, then verify offline behavior only after required models and tools are already installed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaysclawd-cloud/skills/local-ai-stack)
- [Ollama download](https://ollama.com/download)
- [Ollama install script](https://ollama.com/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local model selection, installation steps, command examples, troubleshooting steps, file locations, and optional update scheduling guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
