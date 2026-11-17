## Description:

Runs GitHub Copilot CLI from an agent shell to generate code, edit files, and automate shell tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binotaliu](https://clawhub.ai/user/binotaliu)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to invoke GitHub Copilot CLI for one-shot prompts, interactive coding assistance, file edits, and shell automation from an OpenClaw exec environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill demonstrates Copilot CLI usage with unrestricted access flags that may allow broad file, command, and network operations.

Mitigation: Run it in a limited workspace or container, avoid `--allow-all` unless required, and keep command output visible during file edits or shell tasks.

Risk: Copilot may receive prompts and repository context during use.

Mitigation: Use only with repositories and prompts that are appropriate to share with the configured Copilot service, and review AGENTS.md before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binotaliu/skills/openclaw-copilot-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Copilot CLI prompts, command examples, generated code, file edit guidance, and automation steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
