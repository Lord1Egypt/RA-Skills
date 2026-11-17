## Description:

Switches OpenClaw between local LM Studio models and the Kimi API with status, provider selection, configuration backup, and gateway restart guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endihunn](https://clawhub.ai/user/endihunn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to switch the active model provider between local LM Studio and the Kimi API based on privacy, quality, or GPU availability needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions reference an unverified placeholder repository.

Mitigation: Install only from a verified publisher-controlled repository or reviewed package, and do not use the placeholder repository URL.

Risk: API mode can send prompts, code, and other task context to Kimi.

Mitigation: Use local LM Studio for sensitive credentials, personal data, or proprietary code, and confirm external data-handling requirements before API mode.

Risk: Model switching can modify OpenClaw configuration and restart the gateway service.

Mitigation: Review the configuration backup and JSON changes before restart, validate syntax, and restore from backup if switching fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/endihunn/skills/lmstudio-model-switch)
- [Publisher profile](https://clawhub.ai/user/endihunn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend OpenClaw configuration edits, timestamped backups, JSON validation, and a gateway service restart.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
