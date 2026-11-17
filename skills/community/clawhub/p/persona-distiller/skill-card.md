## Description:

Persona Distiller analyzes local chat records to produce structured persona models and reusable prompt snippets that help an agent respond in a selected person's style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcduann](https://clawhub.ai/user/jcduann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to analyze chat logs, generate structured persona JSON, and activate a persona style through a reusable system prompt snippet for later conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private chat logs may be transformed into persistent persona prompts.

Mitigation: Use only conversations you have permission to analyze, and review or redact generated persona JSON before activation.

Risk: Generated persona prompts may preserve sensitive details or misleading traits from the source chats.

Mitigation: Manually inspect the generated JSON and prompt snippet, remove sensitive content, and validate the persona before reuse.

Risk: Export and file-write behavior may expose or modify local data in ways the user did not intend.

Mitigation: Run the scripts in a controlled local directory, avoid automatic startup loading, and do not use Windows clipboard export until the PowerShell injection issue is fixed.

## Reference(s):

- [Distillation Guide](references/distillation-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/jcduann/skills/persona-distiller)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON persona files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated persona JSON and system prompt snippets are local artifacts that should be reviewed and redacted before activation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
