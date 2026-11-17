## Description:

Grok Swarm gives agents a bridge to xAI Grok 4.20 Multi-Agent Beta for code analysis, refactoring, code generation, and complex reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khaentertainment](https://clawhub.ai/user/khaentertainment)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to send selected local files and prompts to Grok through OpenRouter for code review, refactoring, feature generation, and architectural reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local files may be sent to OpenRouter/Grok during analysis, refactoring, code generation, or reasoning tasks.

Mitigation: Review the file list before use, exclude secrets and sensitive data, and only provide files needed for the task.

Risk: Generated content can write local files, and the CLI includes an option to execute a command after generation.

Mitigation: Prefer dry-run behavior, review generated code before applying it, constrain output directories, and avoid the execute option unless the command is explicitly trusted.

Risk: The bridge can reuse OpenRouter credentials from shared OpenClaw auth profiles when no dedicated key is configured.

Mitigation: Use an explicit OPENROUTER_API_KEY or dedicated Grok Swarm config key, and verify shared auth profile reuse is intentional.

Risk: The installer creates a Python environment and installs dependencies during setup.

Mitigation: Review the installer dependency line and run installation in an environment where package changes are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/khaentertainment/skills/grok-swarm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text responses, with optional annotated code blocks and local file outputs when write/apply options are used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated files under a configured output directory and optional OpenAI-format tool-call JSON when tools are supplied.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
